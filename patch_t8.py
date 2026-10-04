#!/usr/bin/env python3
"""Inject T8 write watcher into build_run.py."""
src = open('build_run.py').read()

WATCH = (' setmetatable ( T8 , { __newindex = function ( t , k , v ) '
         '__print ( PT8W , tostring ( k ) , PEQ , tostring ( v ) , PL , '
         'tostring ( __dbginfo ( 2 , PLQ ) ) ) '
         'rawset ( t , k , v ) end } ) ')
WATCH = WATCH.replace('PT8W', '"[T8W]"').replace('PEQ', '"="').replace('PL', '"L"').replace('PLQ', '"l"')

block_lines = [
    "# 14. watch every T8 write",
    "_lines = payload.split('\\n')",
    "_hits = [i for i, t in enumerate(_lines) if 'T8 = { } T4 [ dQ [ dn [ 35569 ] ] ] = T8 ;' in t]",
    "assert len(_hits) == 1, 'T8 init hits: %d' % len(_hits)",
    "_i = _hits[0]",
]
block_lines.append("_lines[_i] = _lines[_i] + " + repr(WATCH))
block_lines.append("payload = '\\n'.join(_lines)")
block_lines.append("inj.append('t8-watcher')")
block_lines.append("")
block = '\n'.join(block_lines) + '\n\n'

if 't8-watcher' not in src:
    src = src.replace("# 10. THE BIG ONE", block + "# 10. THE BIG ONE")
    open('build_run.py', 'w').write(src)
    print("patched")
else:
    print("already patched")
