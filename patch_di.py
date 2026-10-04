#!/usr/bin/env python3
"""Instrument every dI mutation in the head with a line-number print."""
src = open('build_run.py').read()
block = '\n'.join([
    "# 15. instrument dI mutations",
    "import re as _re2",
    "_pat1 = _re2.compile(r'dI = dI \\+ 1')",
    "_n1 = len(_pat1.findall(payload))",
    "payload = _pat1.sub('dI = dI + 1 __print([[DIPLUS1]] , tostring ( __dbginfo ( 1 , [[l]] ) ) )', payload)",
    "_pat2 = _re2.compile(r'dI = \\( dI or 0 \\) \\+ 1')",
    "_n2 = len(_pat2.findall(payload))",
    "payload = _pat2.sub('dI = ( dI or 0 ) + 1 __print([[DIPLUS1b]] , tostring ( __dbginfo ( 1 , [[l]] ) ) )', payload)",
    "_pat3 = _re2.compile(r'dI = dI \\+ da')",
    "_n3 = len(_pat3.findall(payload))",
    "payload = _pat3.sub('dI = dI + da __print([[DIPLUSDa]] , da , tostring ( __dbginfo ( 1 , [[l]] ) ) )', payload)",
    "inj.append('di-instrument(%d,%d,%d)' % (_n1, _n2, _n3))",
    "",
]) + '\n'
if 'di-instrument' not in src:
    src = src.replace("# 10. THE BIG ONE", block + "# 10. THE BIG ONE")
    open('build_run.py', 'w').write(src)
    print("patched")
else:
    print("already")
