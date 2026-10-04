#!/usr/bin/env python3
"""Watch T4 writes for key 51511 (the checker) via metatable."""
src = open('build_run.py').read()
# replace the KEYS-print injection's tail with a metatable watcher (rebuild the builder-state injection text)
old_frag = 'dQ[17130]=", dQ[17130])'
i = src.find(old_frag)
assert i != -1
# find end of that replacement string literal (the r'...' line)
j = src.find("\\2'", i)
assert j != -1
watcher = (" setmetatable(T4, { __newindex = function ( t , k , v ) if k == 51511 then "
           "__print([[T4CHK-WRITE]] , type ( v ) , [[L]] , tostring ( __dbginfo ( 2 , [[l]] ) ) ) "
           "end rawset ( t , k , v ) end }) \\2'")
src = src[:j] + watcher + src[j+3:]
open('build_run.py', 'w').write(src)
print("patched")
