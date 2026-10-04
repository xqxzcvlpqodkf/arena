#!/usr/bin/env python3
"""Clean fix: T8 watcher + T7 stuck dump, using Lua [[...]] strings (no quotes)."""

src = open('build_run.py').read()

# --- remove old #14 block if present ---
bad = src.find("# 14. watch every T8 write")
end = src.find("# 10. THE BIG ONE")
if bad != -1:
    src = src[:bad] + src[end:]

# --- replace the whole T7 detector replacement string ---
i = src.find("'local __t7n = 0 __print")
j = src.find("end'", i)
assert i != -1 and j != -1, "T7 segment not found"
j += len("end'")

T7_NEW = (
    "'local __t7n = 0 __print([[T7enter]] , zx , zC) "
    "while zx > 0 or zC > 0 do __t7n = __t7n + 1 "
    "if __t7n > 300 then "
    "__print([[T7STUCK]] , zx , zC , zE , ze , T4[dQ[22542]] , T4[dQ[50286]] , "
    "(zO and zO[T4[dQ[22542]]]) , (zO and zO[T4[dQ[50286]]]) ) "
    "do local __pk , __pv = next ( zO ) local __cnt = 0 "
    "while __pk ~= nil and __cnt < 500 do __cnt = __cnt + 1 "
    "__print([[T8E]] , __cnt , tostring ( __pk ) , tostring ( __pv ) ) "
    "__pk , __pv = next ( zO , __pk ) end end "
    "error([[T7-STUCK]]) end'"
)
src = src[:i] + T7_NEW + src[j:]

# --- new T8 watcher block with [[...]] strings ---
WATCH = (
    " setmetatable ( T8 , { __newindex = function ( t , k , v ) "
    "__print ( [[T8W]] , tostring ( k ) , [[=]] , tostring ( v ) , [[L]] , "
    "tostring ( __dbginfo ( 2 , [[l]] ) ) ) "
    "rawset ( t , k , v ) end } ) "
)
block = '\n'.join([
    "# 14. watch every T8 write",
    "_lines = payload.split('\\n')",
    "_hits = [i for i, t in enumerate(_lines) if 'T8 = { } T4 [ dQ [ dn [ 35569 ] ] ] = T8 ;' in t]",
    "assert len(_hits) == 1, 'T8 init hits: %d' % len(_hits)",
    "_i = _hits[0]",
    "_WATCH = " + repr(WATCH),
    "_lines[_i] = _lines[_i] + _WATCH",
    "payload = '\\n'.join(_lines)",
    "inj.append('t8-watcher')",
    "",
]) + '\n'
src = src.replace("# 10. THE BIG ONE", block + "# 10. THE BIG ONE")
open('build_run.py', 'w').write(src)
print("patched clean")
