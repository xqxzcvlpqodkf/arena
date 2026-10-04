#!/usr/bin/env python3
"""Fix T8 watcher: build Lua string with chr(34) so no quote nesting issues."""
src = open('build_run.py').read()
# remove existing block
bad = src.find("# 14. watch every T8 write")
end = src.find("# 10. THE BIG ONE")
if bad != -1:
    src = src[:bad] + src[end:]

Q = ' + CHRQ + '  # placeholder
watch_lua = (
    " setmetatable ( T8 , { __newindex = function ( t , k , v ) "
    "__print ( CHRQ[T8W]CHRQ , tostring ( k ) , CHRQ=CHRQ , tostring ( v ) , "
    "CHRQLCHRQ , tostring ( __dbginfo ( 2 , CHRQlCHRQ ) ) ) "
    "rawset ( t , k , v ) end } ) "
)
watch_lua = watch_lua.replace('CHRQ', '"')

block = '\n'.join([
    "# 14. watch every T8 write",
    "_lines = payload.split('\\n')",
    "_hits = [i for i, t in enumerate(_lines) if 'T8 = { } T4 [ dQ [ dn [ 35569 ] ] ] = T8 ;' in t]",
    "assert len(_hits) == 1, 'T8 init hits: %d' % len(_hits)",
    "_i = _hits[0]",
    "_WATCH = " + repr(watch_lua),
    "_lines[_i] = _lines[_i] + _WATCH",
    "payload = '\\n'.join(_lines)",
    "inj.append('t8-watcher')",
    "",
]) + '\n'
src = src.replace("# 10. THE BIG ONE", block + "# 10. THE BIG ONE")
open('build_run.py', 'w').write(src)
print("patched; watch text:")
print(watch_lua)
