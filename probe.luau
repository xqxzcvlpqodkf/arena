local names = {"getfenv","setfenv","typeof","rawlen","rawequal","bit32","string","os","debug","coroutine","task","game","Instance","workspace","Vector3int16","writefile","getgenv","getgc","hookfunction","restorefunction","select","unpack","newproxy","gcinfo"}
for _, n in ipairs(names) do
    local v = rawget(getfenv(), n) -- may fail if no getfenv
    print(n, v ~= nil and tostring(v) or "MISSING")
end
print("---")
print("string.dump:", string.dump)
print("pcall(string.dump, function() end):", pcall(string.dump, function() return 1 end))
print("debug.info:", debug and debug.info)
if debug and debug.info then
    print("debug.info(debug.info,'s'):", pcall(function() return debug.info(debug.info, "s") end))
    print("debug.info(debug.info,'what'):", pcall(function() return debug.info(debug.info, "what") end))
    print("debug.getinfo:", debug.getinfo)
end
print("typeof({}):", typeof({}))
print("_G == getfenv():", _G == getfenv())
print("_VERSION:", _VERSION)
