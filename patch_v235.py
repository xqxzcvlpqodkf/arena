#!/usr/bin/env python3
"""Print V(235) decode at the failing check site."""
src = open('build_run.py').read()
NEEDLE = ("local Pc = T4 [ dQ [ 17893 ] ] and T4 [ dQ [ 17893 ] ] "
          "[ ( V ( ( ( 436 + - 113 - 88 ) ) , zs ) and Ry or nil ) ] "
          "return T4 [ dQ [ dn [ 39529 ] ] ] ( Pc , T4 , dQ [ 17130 ] , 14 )")
PROBE = ("local Pc = T4 [ dQ [ 17893 ] ] and T4 [ dQ [ 17893 ] ] "
         "[ ( V ( ( ( 436 + - 113 - 88 ) ) , zs ) and Ry or nil ) ] "
         "__print([[V235]] , tostring ( ( V ( 235 , zs ) and Ry or nil ) ) , [[Pc=]] , tostring ( Pc ) , "
         "[[cur=]] , tostring ( T4 [ dQ [ 17130 ] ] ) , [[zs=]] , zs ) "
         "return T4 [ dQ [ dn [ 39529 ] ] ] ( Pc , T4 , dQ [ 17130 ] , 14 )")
block = '\n'.join([
    "# 19. probe V(235) at failing check",
    "assert payload.count(" + repr(NEEDLE) + ") == 1, 'V235 needle hits %d' % payload.count(" + repr(NEEDLE) + ")",
    "payload = payload.replace(" + repr(NEEDLE) + ", " + repr(PROBE) + ", 1)",
    "inj.append('v235-probe')",
    "",
]) + '\n'
if 'v235-probe' not in src:
    src = src.replace("# 10. THE BIG ONE", block + "# 10. THE BIG ONE")
    open('build_run.py', 'w').write(src)
    print("patched")
else:
    print("already")
