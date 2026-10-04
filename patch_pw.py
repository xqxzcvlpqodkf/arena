#!/usr/bin/env python3
"""Probe nil slots at the PW T8-writer line."""
src = open('build_run.py').read()
block = '\n'.join([
    "# 17. probe PW T8-writer slots",
    "_NEEDLE = 'T4 [ dQ [ dn [ 57077 ] ] ] ( T8 , T4 [ dQ [ dn [ 59907 ] ] ] , T4 [ dQ [ 35579 ] ] )'",
    "assert payload.count(_NEEDLE) == 1, 'PW needle hits %d' % payload.count(_NEEDLE)",
    "_PROBE = ('__print([[PWSLOTS]] , [[57077=]] , type ( T4 [ dQ [ dn [ 57077 ] ] ] ) , '",
    "          '[[34460=]] , type ( T4 [ dQ [ dn [ 34460 ] ] ] ) , '",
    "          '[[55870=]] , type ( T4 [ dQ [ dn [ 55870 ] ] ] ) , '",
    "          '[[32150=]] , type ( T4 [ dQ [ dn [ 32150 ] ] ] ) , '",
    "          '[[51520=]] , type ( T4 [ dQ [ dn [ 51520 ] ] ] ) ) ')",
    "payload = payload.replace(_NEEDLE, _PROBE + _NEEDLE, 1)",
    "inj.append('pw-slots')",
    "",
]) + '\n'
if 'pw-slots' not in src:
    src = src.replace("# 10. THE BIG ONE", block + "# 10. THE BIG ONE")
    open('build_run.py', 'w').write(src)
    print("patched")
else:
    print("already")
