#!/usr/bin/env python3
"""Probe PW safe-call inputs and the checker slot."""
src = open('build_run.py').read()
block = '\n'.join([
    "# 18. probe PW call inputs",
    "_NEEDLE = 'local PF = T4 [ dQ [ dn [ 32150 ] ] ] ( PM , PJ , Pn )'",
    "assert payload.count(_NEEDLE) == 1, 'PW needle hits %d' % payload.count(_NEEDLE)",
    "payload = payload.replace(_NEEDLE,",
    "    'local PF = ( function ( ) __print([[PWCALL]] , [[PM=]] , type ( PM ) , tostring ( PM ) , [[PJ=]] , type ( PJ ) , [[Pn=]] , tostring ( Pn ) , [[PU=]] , tostring ( PU ) , [[chkkey=]] , tostring ( dQ [ dn [ 32150 ] ] ) , [[chk=]] , type ( T4 [ dQ [ dn [ 32150 ] ] ] ) ) local __r = T4 [ dQ [ dn [ 32150 ] ] ] ( PM , PJ , Pn ) __print([[PWRESULT]] , tostring ( __r ) ) return __r end ) ( )', 1)",
    "inj.append('pw-call-probe')",
    "",
]) + '\n'
if 'pw-call-probe' not in src:
    src = src.replace("# 10. THE BIG ONE", block + "# 10. THE BIG ONE")
    open('build_run.py', 'w').write(src)
    print("patched")
else:
    print("already")
