#!/usr/bin/env python3
"""Instrument dI += fl and dI += _pox + extend head print with counters."""
src = open('build_run.py').read()

block = '\n'.join([
    "# 16. instrument dI += fl / _pox",
    "payload = payload.replace('dI = dI + fl da =',",
    "    'dI = dI + fl __print([[DIPLUSFL]] , fl) da =', 1)",
    "payload = payload.replace('dI = dI + _pox da =',",
    "    'dI = dI + _pox __print([[DIPLUSPOX]] , _pox , [[fq=]] , fq , [[fH=]] , fH , [[fm=]] , fm , [[fN=]] , fN) da =', 1)",
    "inj.append('di-fl-pox')",
    "",
]) + '\n'
if 'di-fl-pox' not in src:
    src = src.replace("# 10. THE BIG ONE", block + "# 10. THE BIG ONE")

# extend head-state print with fl/fq/fH/fm/fN
old_frag = '__print("[STATE] head: da=", da, " dI=", dI, " b4=", b4, " b1=", b1)'
new_frag = ('__print("[STATE] head: da=", da, " dI=", dI, " b4=", b4, " b1=", b1, '
            '" fl=", fl, " fq=", fq, " fH=", fH, " fm=", fm, " fN=", fN)')
assert old_frag in src, "head print fragment not found"
src = src.replace(old_frag, new_frag)
open('build_run.py', 'w').write(src)
print("patched")
