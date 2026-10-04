#!/usr/bin/env python3
"""Flatten harness: payload at main-chunk level (executor-like C-caller frames)."""
src = open('build_run.py').read()

# 1) payload line 1: keep as assignment instead of return
old1 = "lines[0] = 'return ( function ( ... )'"
new1 = "lines[0] = 'local __payloadres = ( function ( ... )'"
assert old1 in src
src = src.replace(old1, new1)

# 2) trailer + assembly: no chunk wrapper, no pcall around payload
i = src.find("trailer = '''")
j = src.find("'''", i + len("trailer = '''")) + 3
assert i != -1 and j > i
new_trailer = '''trailer = \'\'\'
__print("[HARNESS] payload finished")
__print("[HARNESS] dump lines:", #parts)
__print("=== DUMPFILE BEGIN ===")
for i = 1, #parts do print(parts[i]) end
__print("=== DUMPFILE END ===")
\'\'\'

run = (prelude
       + "\\nlocal __print, __emit, __dbginfo = H.print, H.emit, H.debuginfo\\n"
       + payload
       + "\\n" + trailer)'''
src = src[:i] + new_trailer + src[j:]

open('build_run.py', 'w').write(src)
print("flattened")
