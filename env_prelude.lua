-- ============================================================
-- Arena sandbox harness for wYnFuscate-protected Luau payload
-- Fake executor environment injected into getfenv(0) via rawset.
-- NO setfenv on the payload chunk (breaks Luau closure caching
-- which the armor's Ut()/Ut() identity check depends on).
-- ============================================================
local G = getfenv(0)

local H = {}          -- harness helpers handed to the chunk as upvalues
local parts = {}      -- dump lines
H.parts = parts

local function __print(...)
    local n = select('#', ...)
    local out = {}
    for i = 1, n do
        local v = select(i, ...)
        local t = type(v)
        if t == "string" then out[i] = v
        elseif t == "number" then out[i] = string.format("%.17g", v)
        else out[i] = tostring(v) end
    end
    print(table.concat(out, "\t"))
end
H.print = __print
H.debuginfo = debug.info

local function __emit(s)
    parts[#parts + 1] = s
end
H.emit = __emit

__print("[HARNESS] environment ready")

-- ---------- fake Roblox instance layer ----------
local services = {}
local makeFakeInstance

makeFakeInstance = function(path)
    local proxy = newproxy(true)
    local mt = getmetatable(proxy)
    local store = {}
    local auto = {}
    mt.__index = function(_, k)
        if k == "GetService" then
            return function(_, svc)
                __print("[CALL]", path .. ":GetService", tostring(svc))
                svc = tostring(svc)
                if not services[svc] then services[svc] = makeFakeInstance("game." .. svc) end
                return services[svc]
            end
        elseif k == "FindFirstChild" or k == "FindFirstChildOfClass" or k == "FindFirstChildWhichIsA" or k == "WaitForChild" then
            return function(_, n2) __print("[CALL]", path .. ":" .. k, tostring(n2)) return nil end
        elseif k == "GetChildren" or k == "GetDescendants" then
            return function(_) __print("[CALL]", path .. ":" .. k) return {} end
        elseif k == "IsA" then
            return function(_, c) return c == "Instance" or c == "BasePart" or c == "LocalPlayer" end
        elseif k == "Clone" then
            return function(_) return makeFakeInstance(path .. ":Clone()") end
        elseif k == "Destroy" or k == "remove" then
            return function(_) __print("[CALL]", path .. ":Destroy()") end
        end
        local sv = store[k]
        if sv ~= nil then return sv end
        local c = auto[k]
        if not c then c = makeFakeInstance(path .. "." .. tostring(k)) auto[k] = c end
        return c
    end
    mt.__newindex = function(_, k, v)
        store[k] = v
        __print("[SET]", path .. "." .. tostring(k), "=", tostring(v))
    end
    mt.__tostring = function() return path end
    mt.__call = function(_, ...)
        local args = {}
        for i = 1, select('#', ...) do args[i] = tostring((select(i, ...))) end
        __print("[CALL]", path .. "()", "(" .. table.concat(args, ", ") .. ")")
        return nil
    end
    mt.__eq = function(a, b) return rawequal(a, b) end
    mt.__len = function() return 0 end
    mt.__concat = function(a, b)
        if rawequal(a, b) then return path .. path end
        return tostring(a) .. tostring(b)
    end
    return proxy
end

local fakeGame = makeFakeInstance("game")
local fakeWorkspace = makeFakeInstance("workspace")
local fakeScript = makeFakeInstance("script")

local function newStub(name)
    return function(...)
        local args = {}
        for i = 1, select('#', ...) do args[i] = tostring((select(i, ...))) end
        __print("[ENV]", name, "(" .. table.concat(args, ", ") .. ")")
        return nil
    end
end

local function httpStub(name)
    return function(opts)
        __print("[HTTP]", name, tostring(opts))
        return { Success = true, StatusCode = 200, Status = "200", Headers = {}, Body = '{"ok":true}' }
    end
end

-- wait budget so infinite loops unwind to the post-dump
local waitBudget = 5000
local function budgetError()
    waitBudget = waitBudget - 1
    if waitBudget <= 0 then error("HARNESS: wait budget exceeded", 2) end
end

local function runSpawned(f, tag, a1, a2, a3)
    if type(f) ~= "function" then __print("[ENV]", tag, "non-function arg:", tostring(f)) return end
    local ok, err = coroutine.wrap(f)(a1, a2, a3)
    if not ok then __print("[ENV]", tag, "error:", tostring(err)) end
end

-- ---------- my string clone with fake dump ----------
local myString = {}
for k, v in pairs(G.string) do myString[k] = v end
-- fake debug: wraps real debug but makes our fake dump look like a C function
local fakeDebug = setmetatable({}, { __index = debug })
local realInfo = debug.info
fakeDebug.info = function(f, opt)
    if f == myString.dump then
        -- pretend to be a C function like a real builtin
        if type(opt) ~= "string" then return nil end
        local out = {}
        for ch in opt:gmatch(".") do
            if ch == "s" then out[#out+1] = "[C]"
            elseif ch == "l" then out[#out+1] = -1
            elseif ch == "n" then out[#out+1] = nil
            else out[#out+1] = nil end
        end
        return table.unpack(out)
    end
    if type(f) == "number" then
        -- we add one stack frame; shift level so the caller sees the same frames
        return realInfo(f + 1, opt)
    end
    return realInfo(f, opt)
end

myString.dump = function(f)
    if type(f) ~= "function" then
        error("bad argument #1 to 'dump' (function expected, got " .. type(f) .. ")", 2)
    end
    if f == myString.dump or f == fakeDebug.info or realInfo(f, "s") == "[C]" then
        -- real string.dump is a C function and cannot dump C functions (incl. itself)
        error("unable to dump given function", 2)
    end
    return "\27LuaQ\x00\x00\x00" .. string.char(#tostring(f) % 251 + 1) .. "arena-fake-dump"
end
rawset(G, "debug", fakeDebug)

local GENV = {}
GENV.restorefunction = function(f, h)
    __print("[ENV]", "restorefunction", tostring(f), tostring(h))
    return f
end
GENV._G = GENV

-- ---------- inject everything into the global table ----------
rawset(G, "string", myString)
rawset(G, "game", fakeGame)
rawset(G, "workspace", fakeWorkspace)
rawset(G, "Workspace", fakeWorkspace)
rawset(G, "script", fakeScript)
rawset(G, "task", {
    spawn = function(f, ...) budgetError() runSpawned(f, "task.spawn", ...) end,
    wait = function(t) budgetError() __print("[ENV]", "task.wait", tostring(t)) return 0 end,
    delay = function(t, f) budgetError() runSpawned(f, "task.delay") end,
    defer = function(f) budgetError() runSpawned(f, "task.defer") end,
    cancel = function() end,
    synchronize = function() end,
    desynchronize = function() end,
    clock = function() return os.clock() end,
})
rawset(G, "Instance", {
    new = function(cls, parent)
        __print("[ENV]", "Instance.new", tostring(cls), tostring(parent))
        return makeFakeInstance("Instance.new(" .. tostring(cls) .. ")")
    end,
})
rawset(G, "wait", function(t) budgetError() __print("[ENV]", "wait", tostring(t)) return 0 end)
rawset(G, "spawn", function(f) budgetError() runSpawned(f, "spawn") end)
rawset(G, "delay", function(t, f) budgetError() runSpawned(f, "delay") end)
rawset(G, "shared", {})
rawset(G, "settings", function() return makeFakeInstance("settings()") end)
rawset(G, "UserSettings", function() return makeFakeInstance("UserSettings()") end)
rawset(G, "Tick", function() return os.clock() end)
rawset(G, "time", function() return os.time() end)
rawset(G, "elapsedTime", function() return os.clock() end)
rawset(G, "stats", function() return makeFakeInstance("stats()") end)
rawset(G, "Version", function() return "0.900.1" end)
rawset(G, "UDim2", { new = function(...) return setmetatable({}, { __tostring = function() return "UDim2" end }) end })
rawset(G, "UDim", { new = function(...) return setmetatable({}, { __tostring = function() return "UDim" end }) end })
rawset(G, "Vector2", { new = function(a, b) return { X = a or 0, Y = b or 0 } end })
rawset(G, "Vector2int16", { new = function(a, b) return { X = a or 0, Y = b or 0 } end })
rawset(G, "Vector3", { new = function(a, b, c) return { X = a or 0, Y = b or 0, Z = c or 0 } end })
rawset(G, "Vector3int16", { new = function(a, b, c) return { X = a or 0, Y = b or 0, Z = c or 0 } end })
rawset(G, "Region3int16", { new = function(...) return setmetatable({}, { __tostring = function() return "Region3int16" end }) end })
rawset(G, "RotationCurveKey", { new = function(...) return setmetatable({}, { __tostring = function() return "RotationCurveKey" end }) end })
rawset(G, "FloatCurveKey", { new = function(...) return setmetatable({}, { __tostring = function() return "FloatCurveKey" end }) end })
rawset(G, "SharedTable", { new = function(...) return setmetatable({}, { __tostring = function() return "SharedTable" end }) end })
rawset(G, "CFrame", { new = function(...) return setmetatable({}, { __tostring = function() return "CFrame" end }) end })
rawset(G, "Color3", { new = function(...) return setmetatable({}, { __tostring = function() return "Color3" end }) end })
rawset(G, "ColorSequence", { new = function(...) return setmetatable({}, { __tostring = function() return "ColorSequence" end }) end })
rawset(G, "NumberSequence", { new = function(...) return setmetatable({}, { __tostring = function() return "NumberSequence" end }) end })
rawset(G, "getgenv", function() return GENV end)
rawset(G, "getsenv", function() return G end)
rawset(G, "writefile", function(p, d) __print("[ENV]", "writefile", tostring(p), tostring(d)) end)
rawset(G, "appendfile", function(p, d) __print("[ENV]", "appendfile", tostring(p), tostring(d)) end)
rawset(G, "readfile", function(p) __print("[ENV]", "readfile", tostring(p)) return nil end)
rawset(G, "isfile", function(p) __print("[ENV]", "isfile", tostring(p)) return false end)
rawset(G, "isfolder", function(p) return false end)
rawset(G, "listfiles", function(p) __print("[ENV]", "listfiles", tostring(p)) return {} end)
rawset(G, "makefolder", function(p) __print("[ENV]", "makefolder", tostring(p)) end)
rawset(G, "hookfunction", function(f, t) __print("[ENV]", "hookfunction", tostring(f), tostring(t)) return f end)
rawset(G, "getconnections", function(sig) __print("[ENV]", "getconnections", tostring(sig)) return {} end)
rawset(G, "fireclickdetector", newStub("fireclickdetector"))
rawset(G, "request", httpStub("request"))
rawset(G, "http_request", httpStub("http_request"))
rawset(G, "HttpGet", httpStub("HttpGet"))
rawset(G, "syn", { request = httpStub("syn.request"), websocket = {} })
rawset(G, "http", { request = httpStub("http.request") })
rawset(G, "identifyexecutor", function() return "ArenaSandbox" end)

__print("[HARNESS] globals injected")
