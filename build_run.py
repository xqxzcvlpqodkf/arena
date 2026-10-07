#!/usr/bin/env python3
"""Build an instrumented Luau VM dumper for the supported wYnFuscate profile."""
import argparse
import re
import sys
from pathlib import Path

WORK = Path(__file__).resolve().parent

_parser = argparse.ArgumentParser()
_parser.add_argument(
    "--source",
    type=Path,
    default=WORK / "beautified.lua",
    help="beautified protected Luau input (default: beautified.lua)",
)
_parser.add_argument(
    "--output",
    type=Path,
    default=WORK / "run.txt",
    help="instrumented Luau output (default: run.txt)",
)
_args = _parser.parse_args()

prelude = (WORK / 'env_prelude.lua').read_text()
# fix the broken trailing print of the prelude
prelude = prelude.replace(
    '__print("[HARNESS] environment ready (" .. #CLIENV.string and "string" .. ")")',
    '__print("[HARNESS] environment ready")')

payload = _args.source.read_text(encoding="utf-8", errors="replace")
# line 1 contains the license comment AND the IIFE opener glued at the end
lines = payload.split('\n')
first = lines[0]
assert 'return ( function ( ... )' in first, "IIFE opener missing from line 1"
lines[0] = 'local __payloadres = ( function ( ... )'
payload = '\n'.join(lines)

inj = []

def sub1(pat, repl, text, tag, flags=0):
    m = re.compile(pat, flags)
    hits = m.findall(text)
    if len(hits) != 1:
        print(f"[FAIL] marker {tag}: {len(hits)} hits")
        sys.exit(1)
    text = m.sub(repl, text, count=1)
    inj.append(tag)
    return text


# --- checkpoints ---
CKPTS = [
    (r'local z9 = \{ \} local z8 = 0 local z7 = \{ \}', 'z9'),
    (r'local dn = \{ \} local Xk = dU', 'dn-build'),
    (r'local Ry = nil local Rj = 0 local Ru = false T4 \[ dQ \[ 62450 \] \] = function', 'V62450'),
    (r'local R2 = T4 \[ dQ \[ 19637 \] \] dY =', 'R2-done'),
    (r'T4 \[ dQ \[ 46486 \] \] =', 'hashfn'),
    (r'local c = nil T4 \[ dQ \[ dn \[ 33103 \] \] \]', 'c-def'),
    (r'T4 \[ dQ \[ 22816 \] \] = T4 \[ dQ \[ 35379 \] \] \( \{ \} , \{ __mode = .k. \} \) local Lf = \{ \} local LA = \{ \}', 'LA-def'),
    (r'do\s*local Lz = T1 \[ dS \( 648 , dF , 5 \) \] local LX = function \( Lp \)', 'LX-def'),
    (r'local Np =', 'Np-check'),
    (r'local H7 = \( \( 74 \* 1957 \+ 150 \* 9936 \+ 3356807841 \) % AT \)', 'c-hash-pre'),
]
for pat, tag in CKPTS:
    m = re.compile(pat)
    hits = m.findall(payload)
    print(f"[CKPT] {tag}: {len(hits)} hits")
    if len(hits) == 1:
        payload = m.sub(lambda mo: '__print("[CKPT] ' + tag + '") ' + mo.group(0), payload, count=1)


# --- fine checkpoints by line number in beautified.lua ---
import subprocess, tempfile, os
# These line-by-line checkpoints were useful while locating an integrity trap,
# but they perturb debug-line checks and are no longer needed for a clean dump.
FINE = []
_plines = payload.split('\n')
ok_lines = []
for ln in FINE:
    idx = ln - 1
    saved = _plines[idx]
    _plines[idx] = '__print("[CKPT] L' + str(ln) + '") ' + saved
    cand = '\n'.join(_plines)
    open('/tmp/cand.luau','w').write(prelude + "\nlocal chunk = function(...)\nlocal __print, __emit, __dbginfo = H.print, H.emit, H.debuginfo\n" + cand + "\nend\n")
    r = subprocess.run(['./luau-compile','/tmp/cand.luau'], capture_output=True)
    if r.returncode == 0:
        ok_lines.append(ln)
    else:
        _plines[idx] = saved
payload = '\n'.join(_plines)
print("[CKPT-FINE] inserted at", ok_lines)

# 1. Ab hang-trap -> error
payload = sub1(
    r'local Ab = function \( Af \)\s*repeat\s*Af = \( Af \* 48271 \+ 1 \) % Ad if Af == 0 then\s*Af = 1\s*end\s*until\s*Af == 0\s*end',
    'local Ab = function ( Af ) __print("[TRAP] Ab trap fired", Af) error("AB-TRAP") end',
    payload, 'Ab-trap')

# 2. head state print
payload = sub1(
    r'(local tc = bo \( bx , dC \( 1 \) \) local tZ = tc and bo \( tc , dC \( 60 \) \))',
    r'__print("[STATE] head: da=", da, " dI=", dI, " b4=", b4, " b1=", b1, " fl=", fl, " fq=", fq, " fH=", fH, " fm=", fm, " fN=", fN) \1',
    payload, 'head-state')

# 3. builder state print (before T4 creation marker)
payload = sub1(
    r'(local T8 local T5 local T7 local dT local dd local db local df local Tr local TO local dh local dA local dp local dt local dl local dY local dL local dq local dH local dm)( T4 \[ dQ \[ 32245 \] \] = T4)',
    r'\1 __print("[STATE] builder start: dI=", dI, " At=", At, " lKtype=", type(lK)) __print("[KEYS] dQ[9312]=", dQ[9312], " T4val=", type(T4[dQ[9312]]), " dQ[22542]=", dQ[22542], " dQ[50286]=", dQ[50286], " dQ[17130]=", dQ[17130])  setmetatable(T4, { __newindex = function ( t , k , v ) if k == 17398 then __print([[T4DEL-WRITE]] , type ( v ) , [[L]] , tostring ( __dbginfo ( 2 , [[l]] ) ) ) end rawset ( t , k , v ) end }) \2',
    payload, 'builder-state')

# 4. constants hash print
payload = sub1(
    r'(if HG ~= Hs then)',
    r'__print("[STATE] const-hash: HG=", HG, " Hs=", Hs) \1',
    payload, 'const-hash')

# 5. c-hash trap -> print + error
payload = sub1(
    r'if H5 ~= H7 then\s*do\s*local md = \( H5 \+ 1 \) ;\s*repeat\s*md = \( md \* 1103515245 \+ 12345 \) % AT\s*until\s*md == 0\s*end\s*end',
    'do __print("[STATE] c-hash: H5=", H5, " H7=", H7) if H5 ~= H7 then __print("[TRAP] c-hash MISMATCH") error("CHASH-TRAP") end end',
    payload, 'c-hash')

# 6. dr kill-switches (2 sites) - just print marker via global count sub
n_dr = len(re.findall(r'dr = 0\s*dI = 1\s*return', payload))
payload = re.sub(r'dr = 0\s*dI = 1\s*return',
                 'dr = 0 dI = 1 __print("[TRAP] dr-zeroed kill switch") return', payload)
inj.append(f'dr-zero({n_dr})')

# 7. NR hang loops are deliberate integrity traps. Skipping the loop body is
# enough; raising here prevents the prototype table from being completed.
n_nr = len(re.findall(r'repeat\s*NR = \( NR \* 1103515245 \+ 12345 \) % AT\s*until\s*NR == 0', payload))
payload = re.sub(r'repeat\s*NR = \( NR \* 1103515245 \+ 12345 \) % AT\s*until\s*NR == 0',
                 '__print("[BYPASS] NR loop")', payload)
inj.append(f'NR-loops({n_nr})')

# 8. the infinite md loops at 1103515245 elsewhere (md==0) - neutralize all remaining
n_md = len(re.findall(r'repeat\s*md = \( md \* 1103515245 \+ 12345 \) % AT\s*until\s*md == 0', payload))
payload = re.sub(r'repeat\s*md = \( md \* 1103515245 \+ 12345 \) % AT\s*until\s*md == 0',
                 '__print("[TRAP] md loop") error("MD-TRAP")', payload)
inj.append(f'md-loops({n_md})')

# 9. tail Ud check print
payload = sub1(
    r'(local Uf = \( 42 - 17 \) if Ud ~= Uf then)',
    r'__print("[STATE] tail: T2-key-count Ud=", Ud, " want=", (42-17)) \1',
    payload, 'tail-ud')

# 9b. tail T2[27367] check print
payload = sub1(
    r'(if T2 \[ \( 34 - 7 \) \* 1000 \+ 367 \] ~= \( 308 - 3 \) \* 100 \+ 77 then)',
    r'__print("[STATE] tail: T2[27367]=", T2[(34-7)*1000+367], " want=", (308-3)*100+77) \1',
    payload, 'tail-t2num')

# 9c. tail Ul check print
payload = sub1(
    r'(local Ul = \( Ut \( \) ~= Ut \( \) \) if Ul then)',
    r'__print("[STATE] tail: Ul=", (Ut()~=Ut())) \1',
    payload, 'tail-ul')

# 11c. T7 peasant-multiply stuck detector
_lines = payload.split('\n')
_hits = [i for i, t in enumerate(_lines) if 'T4 [ dQ [ 55733 ] ] = function ( zx , zC )' in t]
assert len(_hits) == 1, 'T7 def hits: %d' % len(_hits)
_i = _hits[0]
# the while loop is 1 line below
_w = _i + 1
assert 'while zx > 0 or zC > 0 do' in _lines[_w], 'T7 while not on next line: ' + _lines[_w][:80]
_lines[_w] = _lines[_w].replace('while zx > 0 or zC > 0 do',
    'local __t7n = 0 while zx > 0 or zC > 0 do __t7n = __t7n + 1 if __t7n > 300 then __print([[T7STUCK]] , zx , zC , zE , ze , T4[dQ[22542]] , T4[dQ[50286]] , (zO and zO[T4[dQ[22542]]]) , (zO and zO[T4[dQ[50286]]]) ) do local __pk , __pv = next ( zO ) local __cnt = 0 while __pk ~= nil and __cnt < 500 do __cnt = __cnt + 1 __print([[T8E]] , __cnt , tostring ( __pk ) , tostring ( __pv ) ) __pk , __pv = next ( zO , __pk ) end end error([[T7-STUCK]]) end', 1)
payload = '\n'.join(_lines)
inj.append('t7-detector')

# 14. watch every T8 write
_lines = payload.split('\n')
_hits = [i for i, t in enumerate(_lines) if 'T8 = { } T4 [ dQ [ dn [ 35569 ] ] ] = T8 ;' in t]
assert len(_hits) == 1, 'T8 init hits: %d' % len(_hits)
_i = _hits[0]
_WATCH = ' setmetatable ( T8 , { __newindex = function ( t , k , v ) __print ( [[T8W]] , tostring ( k ) , [[=]] , tostring ( v ) , [[L]] , tostring ( __dbginfo ( 2 , [[l]] ) ) ) rawset ( t , k , v ) end } ) '
_lines[_i] = _lines[_i] + _WATCH
payload = '\n'.join(_lines)
inj.append('t8-watcher')

# 15. instrument dI mutations
import re as _re2
_pat1 = _re2.compile(r'dI = dI \+ 1')
_n1 = len(_pat1.findall(payload))
payload = _pat1.sub('dI = dI + 1 __print([[DIPLUS1]] , tostring ( __dbginfo ( 1 , [[l]] ) ) )', payload)
_pat2 = _re2.compile(r'dI = \( dI or 0 \) \+ 1')
_n2 = len(_pat2.findall(payload))
payload = _pat2.sub('dI = ( dI or 0 ) + 1 __print([[DIPLUS1b]] , tostring ( __dbginfo ( 1 , [[l]] ) ) )', payload)
_pat3 = _re2.compile(r'dI = dI \+ da')
_n3 = len(_pat3.findall(payload))
payload = _pat3.sub('dI = dI + da __print([[DIPLUSDa]] , da , tostring ( __dbginfo ( 1 , [[l]] ) ) )', payload)
inj.append('di-instrument(%d,%d,%d)' % (_n1, _n2, _n3))

# 16. instrument dI += fl / _pox
payload = payload.replace('dI = dI + fl da =',
    'dI = dI + fl __print([[DIPLUSFL]] , fl) da =', 1)
payload = payload.replace('dI = dI + _pox da =',
    'dI = dI + _pox __print([[DIPLUSPOX]] , _pox , [[fq=]] , fq , [[fH=]] , fH , [[fm=]] , fm , [[fN=]] , fN) da =', 1)
inj.append('di-fl-pox')

# 17. probe PW T8-writer slots
_NEEDLE = 'T4 [ dQ [ dn [ 57077 ] ] ] ( T8 , T4 [ dQ [ dn [ 59907 ] ] ] , T4 [ dQ [ 35579 ] ] )'
assert payload.count(_NEEDLE) == 1, 'PW needle hits %d' % payload.count(_NEEDLE)
_PROBE = ('__print([[PWSLOTS]] , [[57077=]] , type ( T4 [ dQ [ dn [ 57077 ] ] ] ) , '
          '[[34460=]] , type ( T4 [ dQ [ dn [ 34460 ] ] ] ) , '
          '[[55870=]] , type ( T4 [ dQ [ dn [ 55870 ] ] ] ) , [[key55870=]] , tostring ( dQ [ dn [ 55870 ] ] ) , '
          '[[32150=]] , type ( T4 [ dQ [ dn [ 32150 ] ] ] ) , '
          '[[51520=]] , type ( T4 [ dQ [ dn [ 51520 ] ] ] ) ) ')
payload = payload.replace(_NEEDLE, _PROBE + _NEEDLE, 1)
inj.append('pw-slots')

# 18. probe PW call inputs
_NEEDLE = 'local PF = T4 [ dQ [ dn [ 32150 ] ] ] ( PM , PJ , Pn )'
assert payload.count(_NEEDLE) == 1, 'PW needle hits %d' % payload.count(_NEEDLE)
_PROBE = ('local PF = ( function ( ) __print([[PWCALL]] , [[PM=]] , type ( PM ) , tostring ( PM ) , [[PJ=]] , type ( PJ ) , '
          '[[Pn=]] , tostring ( Pn ) , [[PU=]] , tostring ( PU ) , [[chkkey=]] , tostring ( dQ [ dn [ 32150 ] ] ) , '
          '[[chk=]] , type ( T4 [ dQ [ dn [ 32150 ] ] ] ) , [[cur=]] , tostring ( T4 [ Pn ] ) , [[delkey=]] , tostring ( dQ [ dn [ 45464 ] ] ) , [[del=]] , type ( T4 [ dQ [ dn [ 45464 ] ] ] ) ) '
          'local __r = T4 [ dQ [ dn [ 32150 ] ] ] ( PM , PJ , Pn ) '
          '__print([[PWRESULT]] , tostring ( __r ) ) return __r end ) ( )')
payload = payload.replace(_NEEDLE, _PROBE, 1)
inj.append('pw-call-probe')

# 19. probe V(235) at failing check
assert payload.count('local Pc = T4 [ dQ [ 17893 ] ] and T4 [ dQ [ 17893 ] ] [ ( V ( ( ( 436 + - 113 - 88 ) ) , zs ) and Ry or nil ) ] return T4 [ dQ [ dn [ 39529 ] ] ] ( Pc , T4 , dQ [ 17130 ] , 14 )') == 1, 'V235 needle hits %d' % payload.count('local Pc = T4 [ dQ [ 17893 ] ] and T4 [ dQ [ 17893 ] ] [ ( V ( ( ( 436 + - 113 - 88 ) ) , zs ) and Ry or nil ) ] return T4 [ dQ [ dn [ 39529 ] ] ] ( Pc , T4 , dQ [ 17130 ] , 14 )')
payload = payload.replace('local Pc = T4 [ dQ [ 17893 ] ] and T4 [ dQ [ 17893 ] ] [ ( V ( ( ( 436 + - 113 - 88 ) ) , zs ) and Ry or nil ) ] return T4 [ dQ [ dn [ 39529 ] ] ] ( Pc , T4 , dQ [ 17130 ] , 14 )', 'local Pc = T4 [ dQ [ 17893 ] ] and T4 [ dQ [ 17893 ] ] [ ( V ( ( ( 436 + - 113 - 88 ) ) , zs ) and Ry or nil ) ] __print([[V235]] , tostring ( ( V ( 235 , zs ) and Ry or nil ) ) , [[Pc=]] , tostring ( Pc ) , [[cur=]] , tostring ( T4 [ dQ [ 17130 ] ] ) , [[zs=]] , zs ) return T4 [ dQ [ dn [ 39529 ] ] ] ( Pc , T4 , dQ [ 17130 ] , 14 )', 1)
inj.append('v235-probe')

# 20. probe dr after the t0 kill-switch
_n = payload.count('dB ( T1 , ( 316 + 96 ) , bo ( bx , dC ( 4 ) ) , 5 )')
assert _n == 1, 'dr needle hits %d' % _n
payload = payload.replace('dB ( T1 , ( 316 + 96 ) , bo ( bx , dC ( 4 ) ) , 5 )', '__print([[DR590]] , dr ) dB ( T1 , ( 316 + 96 ) , bo ( bx , dC ( 4 ) ) , 5 )', 1)
inj.append('dr590-probe')

# 21. instrument delegate checker body
N2 = "local Ph = T4 [ dQ [ 28686 ] ] if not Ph and Pf then"
P2 = ("local Ph = T4 [ dQ [ 28686 ] ] __print([[CHK-Ph]] , tostring ( Ph )) "
      "local __pc , __pr = pcall ( Ph , PT , ( V ( 264 , zs ) and Ry or nil ) ) "
      "__print([[CHK-PhCall]] , [[ok=]] , tostring ( __pc ) , [[Pz=]] , tostring ( __pr ) and ( __pr and string.sub ( tostring ( __pr ) , 1 , 60 ) or nil ) ) "
      "if not Ph and Pf then")
assert payload.count(N2) == 1, 'N2 hits %d' % payload.count(N2)
payload = payload.replace(N2, P2, 1)
inj.append('chk-body')

# 22. probe Np check values
assert payload.count('local _ , Hr = T4 [ dQ [ 50280 ] ] ( T4 [ dQ [ dn [ 24278 ] ] ] ) ;') == 1, 'H16908 n1 hits %d' % payload.count('local _ , Hr = T4 [ dQ [ 50280 ] ] ( T4 [ dQ [ dn [ 24278 ] ] ] ) ;')
payload = payload.replace('local _ , Hr = T4 [ dQ [ 50280 ] ] ( T4 [ dQ [ dn [ 24278 ] ] ] ) ;', 'local _ , Hr = T4 [ dQ [ 50280 ] ] ( T4 [ dQ [ dn [ 24278 ] ] ] ) ; __print([[H16908]] , [[Hr=]] , tostring ( Hr ) ) ;', 1)
assert payload.count('Np = ( T2 [ ( ( 49 + 99 - 89 ) ) ] ~= T4 [ dQ [ 16908 ] ] )') == 1, 'Np n2 hits %d' % payload.count('Np = ( T2 [ ( ( 49 + 99 - 89 ) ) ] ~= T4 [ dQ [ 16908 ] ] )')
payload = payload.replace('Np = ( T2 [ ( ( 49 + 99 - 89 ) ) ] ~= T4 [ dQ [ 16908 ] ] )', 'Np = ( T2 [ ( ( 49 + 99 - 89 ) ) ] ~= T4 [ dQ [ 16908 ] ] ) __print([[NPVALS]] , [[T2-59=]] , tostring ( T2 [ 59 ] ) , [[T4-16908=]] , tostring ( T4 [ dQ [ 16908 ] ] ) )', 1)
inj.append('np-probe')

# 23. watch T2[59] writes
assert payload.count('local T2 = { } ;') == 1, 'T2 init hits %d' % payload.count('local T2 = { } ;')
payload = payload.replace('local T2 = { } ;', 'local T2 = { } ; local T2mt = { __newindex = function ( t , k , v ) if k == 59 then __print([[T2-59-SET]] , tostring ( v ) , [[L]] , tostring ( __dbginfo ( 2 , [[l]] ) ) ) end rawset ( t , k , v ) end } setmetatable ( T2 , T2mt ) ;', 1)
inj.append('t2-59-watch')

# Decoder and page-loader integrity checks compare closures by identity. The
# dump harness intentionally wraps/instruments those closures, so bypass only
# these four identity checks while retaining all actual decoding logic.
for slot, index in ((62450, 1), (33346, 2), (16052, 3)):
    needle = f'if T4 [ dQ [ {slot} ] ] ~= ( Rg and Rg [ {index} ] ) then'
    assert payload.count(needle) == 1, (slot, payload.count(needle))
    payload = payload.replace(needle, 'if false then', 1)

needle = 'if T4 [ dQ [ 56219 ] ] ~= T4 [ dQ [ 45529 ] ] [ 4 ] then'
assert payload.count(needle) == 1, payload.count(needle)
payload = payload.replace(needle, 'if false then', 1)

# Decoding later root pages invokes the destructive post-run cleanup as a trap.
needle = 'if mb [ 1811 ] == 0 and mh > 0 and not mb [ 5966 ] then\n                                                                              T4 [ dQ [ dn [ 35114 ] ] ] ( )'
assert payload.count(needle) == 1, payload.count(needle)
payload = payload.replace(
    needle,
    'if mb [ 1811 ] == 0 and mh > 0 and not mb [ 5966 ] then\n'
    '                                                                              __print([[BYPASS main-page cleanup]])',
    1,
)

# After the protected wrapper clears globals, use raw references captured by
# the harness instead of a metatable-sensitive lookup.
needle = 'local nk = T4 [ dQ [ 45204 ] ] return nk and nk [ ng ]'
assert payload.count(needle) == 1, payload.count(needle)
payload = payload.replace(
    needle,
    'local __dk = __safe_rawget ( dQ , 45204 ) local nk = __safe_rawget ( T4 , __dk ) '
    '__fallback_n = __fallback_n + 1 if __fallback_n < 20 then '
    '__print([[FALLBACK]] , tostring(ng), tostring(__dk), type(nk), tostring(nk)) end '
    'return nk and nk [ ng ]',
    1,
)

# 10. THE BIG ONE: replace launch with pre-dump + run + post-dump
BIGDUMP = r'''
local table, string, math = __safe_table, __safe_string, __safe_math
local pairs, ipairs, type = __safe_pairs, __safe_ipairs, __safe_type
local tostring, pcall, rawget = __safe_tostring, __safe_pcall, __safe_rawget
__emit("=== PREDUMP v1 ===")
__print("[DUMP] pre-dump starting")
do
  local D = T4
  -- T4 inventory (types + simple values)
  local cnt = 0
  for k, v in pairs(D) do cnt = cnt + 1 end
  __emit("T4.count " .. cnt)
  local keys = {}
  for k in pairs(D) do keys[#keys+1] = k end
  table.sort(keys)
  for _, k in ipairs(keys) do
    local v = D[k]
    local t = type(v)
    if t == "number" then
      __emit("T4[" .. tostring(k) .. "] " .. t .. " " .. string.format("%.17g", v))
    elseif t == "boolean" then
      __emit("T4[" .. tostring(k) .. "] " .. t .. " " .. tostring(v))
    elseif t == "string" then
      __emit("T4[" .. tostring(k) .. "] string " .. tostring(v))
    elseif t == "table" then
      local n = 0
      for _ in pairs(v) do n = n + 1 end
      __emit("T4[" .. tostring(k) .. "] table n=" .. n)
    else
      __emit("T4[" .. tostring(k) .. "] " .. t)
    end
  end
  -- dQ / dn maps
  local dqk = {}
  for k in pairs(dQ) do dqk[#dqk+1] = k end
  table.sort(dqk)
  local parts = {}
  for _, k in ipairs(dqk) do parts[#parts+1] = tostring(k) .. ":" .. tostring(dQ[k]) end
  __emit("dQ " .. table.concat(parts, ","))
  local dnk = {}
  for k in pairs(dn) do dnk[#dnk+1] = k end
  table.sort(dnk)
  parts = {}
  for _, k in ipairs(dnk) do parts[#parts+1] = tostring(k) .. ":" .. tostring(dn[k]) end
  __emit("dn " .. table.concat(parts, ","))
  -- constants array
  local KC = D[dQ[18316]]
  local nparts = {}
  local mx = 0
  for k in pairs(KC) do if type(k) == "number" and k > mx then mx = k end end
  for i = 1, mx do
    local v = KC[i]
    if v == nil then nparts[#nparts+1] = "?" else nparts[#nparts+1] = string.format("%.17g", v) end
  end
  __emit("CONST.max " .. mx)
  __emit("CONST " .. table.concat(nparts, ","))
  -- R2 id list
  local np = {}
  for i = 1, 400 do
    local v = R2[i]
    np[#np+1] = (v == nil and "?" or tostring(v))
  end
  __emit("R2 " .. table.concat(np, ","))
  -- c stream
  if c ~= nil then
    if type(c) == "table" then
      local cp = {}
      local cm = 0
      for k in pairs(c) do if type(k) == "number" and k > cm then cm = k end end
      for i = 1, cm do cp[#cp+1] = (c[i] == nil and "?" or tostring(c[i])) end
      __emit("C.max " .. cm)
      __emit("C " .. table.concat(cp, ","))
    else
      __emit("C.type " .. type(c) .. " len " .. #c)
    end
  end
  -- z5 (decoded strings so far) via ID map
  local IM = D[dQ[25026]]
  if IM then
    local ik = {}
    for k in pairs(IM) do ik[#ik+1] = k end
    table.sort(ik)
    local out = {}
    for _, id in ipairs(ik) do
      local ok2, s = pcall(function() return z5[id] end)
      if ok2 and s ~= nil and type(s) == "string" then
        local hex = {}
        for i = 1, #s do hex[i] = string.format("%02x", string.byte(s, i)) end
        out[#out+1] = id .. "=" .. #s .. ":" .. table.concat(hex)
      end
    end
    __emit("Z5PRE " .. table.concat(out, " "))
  end
  -- Ho proto metadata
  local pids = {}
  for k in pairs(Ho) do pids[#pids+1] = k end
  table.sort(pids)
  for _, pi in ipairs(pids) do
    local p = Ho[pi]
    local pk = {}
    for k in pairs(p) do pk[#pk+1] = k end
    table.sort(pk)
    local pp = {}
    for _, k in ipairs(pk) do
      local v = p[k]
      local t = type(v)
      if t == "number" then pp[#pp+1] = k .. "=" .. string.format("%.17g", v)
      elseif t == "boolean" then pp[#pp+1] = k .. "=" .. tostring(v)
      elseif t == "table" then
        local n = 0
        for _ in pairs(v) do n = n + 1 end
        pp[#pp+1] = k .. "=<tbl:" .. n .. ">"
      elseif t == "string" then pp[#pp+1] = k .. "=<str:" .. #v .. ">"
      else pp[#pp+1] = k .. "=<" .. t .. ">" end
    end
    __emit("PROTO[" .. pi .. "] " .. table.concat(pp, " "))
    -- upvalue descriptors (1858)
    local uv = p[1858]
    if uv then
      local up = {}
      for k2, v2 in pairs(uv) do
        up[#up+1] = tostring(k2) .. ":" .. tostring(v2.HF) .. "/" .. tostring(v2.pn)
      end
      __emit("PROTO[" .. pi .. "].UV " .. table.concat(up, " "))
    end
    -- wrapped proto payload (276-key table) raw
  end
  __emit("=== END PREDUMP ===")
end
-- Prototype extraction does not need to execute the Roblox payload. Keeping
-- it dormant also prevents the deliberate root decoy loop from running.
local __ok, __r1, __r2, __r3, __r4, __r5, __r6, __r7, __r8 = true, nil, nil, nil, nil, nil, nil, nil, nil
if not __ok then __print("[DUMP] payload error: ", __r1) end
__emit("=== POSTDUMP v1 ===")
do
  local NPf = T4[dQ[56219]]
  local pids = {}
  for k in pairs(Ho) do pids[#pids+1] = k end
  table.sort(pids)
  for _, pi in ipairs(pids) do
    local p = Ho[pi]
    local q1 = rawget(p, 8076) or 0
    if type(q1) ~= "number" then q1 = 0 end
    local npages = math.floor((q1 + 63) / 64)
    for pg = 0, npages - 1 do
      local okp, errp = pcall(NPf, p, pg * 64 + 1, zs, qu)
      if not okp then __emit("PAGEFAIL[" .. pi .. "." .. pg .. "] " .. tostring(errp)) end
    end
    local function dumpArr(tag, t, n)
      if t == nil then return end
      if n == nil then
        n = 0
        for k in pairs(t) do if type(k) == "number" and k > n then n = k end end
      end
      local parts = {}
      for i = 1, n do
        local v = t[i]
        if v == nil then parts[#parts+1] = "?" else parts[#parts+1] = string.format("%.17g", v) end
      end
      __emit("P" .. pi .. "." .. tag .. " " .. table.concat(parts, ","))
    end
    dumpArr("op", rawget(p, 5447), q1)
    dumpArr("A", rawget(p, 5251), q1)
    dumpArr("B", rawget(p, 2117), q1)
    dumpArr("C", rawget(p, 2718), q1)
    dumpArr("D", rawget(p, 5390), q1)
    dumpArr("E", rawget(p, 9007), q1)
    dumpArr("F", rawget(p, 3995), q1)
    dumpArr("G", rawget(p, 8620), q1)
    dumpArr("code", rawget(p, 5811), q1)
    dumpArr("Cjump", rawget(p, 8615), q1)
    dumpArr("jump", rawget(p, 2492), nil)
  end
  -- all decoded strings via every valid id
  local IM = T4[dQ[25026]]
  if IM then
    local ik = {}
    for k in pairs(IM) do ik[#ik+1] = k end
    table.sort(ik)
    local out = {}
    for _, id in ipairs(ik) do
      local ok2, sv = pcall(function()
        local decoder = T4[dQ[62450]]
        if decoder(id, zs) then return Ry end
        return nil
      end)
      if ok2 and sv ~= nil and type(sv) == "string" then
        local hex = {}
        for j = 1, #sv do hex[j] = string.format("%02x", string.byte(sv, j)) end
        out[#out+1] = id .. "=" .. #sv .. ":" .. table.concat(hex)
      else
        out[#out+1] = id .. "=!" .. tostring(sv)
      end
    end
    __emit("Z5POST " .. table.concat(out, " "))
  end
  __emit("=== END POSTDUMP ===")
end
return __r1, __r2, __r3, __r4, __r5, __r6, __r7, __r8
'''

payload = sub1(
    r'local n7 = Ho \[ 0 \] local UT = T4 \[ dQ \[ 23556 \] \] \( n7 , \{ \} \) return UT \( \.\.\. \)',
    'local n7 = Ho [ 0 ] local UT = T4 [ dQ [ 23556 ] ] ( n7 , { } )' + BIGDUMP,
    payload, 'bigdump')

trailer = '''
__print("[HARNESS] payload finished")
__print("[HARNESS] dump lines:", #parts)
__print("=== DUMPFILE BEGIN ===")
for i = 1, #parts do print(parts[i]) end
__print("=== DUMPFILE END ===")
'''

safe_bindings = '''
local __safe_table, __safe_string, __safe_math = table, string, math
local __safe_pairs, __safe_ipairs, __safe_type = pairs, ipairs, type
local __safe_tostring, __safe_pcall, __safe_rawget = tostring, pcall, rawget
local __fallback_n = 0
'''
run = (prelude
       + safe_bindings
       + "\nlocal __print, __emit, __dbginfo = H.print, H.emit, H.debuginfo\n"
       + payload
       + "\n" + trailer)

_args.output.parent.mkdir(parents=True, exist_ok=True)
_args.output.write_text(run)
print(f"[OK] built {_args.output}", len(run), "bytes; injections:", inj)
