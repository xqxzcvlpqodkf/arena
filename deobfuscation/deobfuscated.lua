--[[
    Supax Tech V2

    Readable reconstruction of message.txt.

    CONFIDENCE NOTE
    ----------------
    The UI, defaults, events, animation IDs, humanoid changes, body-mover
    cleanup, timing, and remote payloads below were observed at runtime.
    The target-facing CFrame expression in performSupaTech is an informed
    reconstruction; it is the one remaining portion not yet recovered
    instruction-for-instruction from the virtual machine.
]]

local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")
local UserInputService = game:GetService("UserInputService")
local RunService = game:GetService("RunService")
local CoreGui = game:GetService("CoreGui")

local player = Players.LocalPlayer
local tweenSpeed = 0.12
local height = 4.5

-- This mismatch is present in the payload: the backing flag starts true while
-- the initial GUI label says OFF.
local enabled = true
local movementActive = false
local lastTrigger = 0
local movementConnection

local character
local humanoid
local rootPart
local savedMovement

local function make(className, parent, properties)
    local object = Instance.new(className)
    for key, value in pairs(properties or {}) do
        object[key] = value
    end
    object.Parent = parent
    return object
end

local oldGui = CoreGui:FindFirstChild("SupaTechV2")
if oldGui then
    oldGui:Destroy()
end

local gui = make("ScreenGui", CoreGui, {
    Name = "SupaTechV2",
    ResetOnSpawn = false,
    ZIndexBehavior = Enum.ZIndexBehavior.Sibling,
    DisplayOrder = 9999,
})

local main = make("Frame", gui, {
    Size = UDim2.new(0, 80, 0, 80),
    Position = UDim2.new(0, 440, 0, 280),
    BackgroundColor3 = Color3.fromRGB(16, 16, 22),
    BorderSizePixel = 0,
})
make("UICorner", main, { CornerRadius = UDim.new(0, 16) })
local mainStroke = make("UIStroke", main, {
    Color = Color3.fromRGB(45, 45, 65),
    Thickness = 1.5,
})

local title = make("TextLabel", main, {
    Size = UDim2.new(1, 0, 0.44, 0),
    Position = UDim2.new(0, 0, 0.05, 0),
    BackgroundTransparency = 1,
    Text = "Supax\nTech",
    TextColor3 = Color3.fromRGB(160, 165, 200),
    TextSize = 10,
    Font = Enum.Font.GothamBold,
})

local configButton = make("TextButton", main, {
    Size = UDim2.new(0, 22, 0, 14),
    Position = UDim2.new(0.5, -11, 0, 52),
    BackgroundColor3 = Color3.fromRGB(30, 30, 45),
    BorderSizePixel = 0,
    Text = "T",
    TextColor3 = Color3.fromRGB(160, 165, 200),
    TextSize = 9,
    Font = Enum.Font.GothamBold,
    AutoButtonColor = false,
    ZIndex = 5,
})
make("UICorner", configButton, { CornerRadius = UDim.new(0, 5) })

local status = make("TextLabel", main, {
    Size = UDim2.new(1, 0, 0.2, 0),
    Position = UDim2.new(0, 0, 0.78, 0),
    BackgroundTransparency = 1,
    Text = "OFF",
    TextColor3 = Color3.fromRGB(90, 90, 115),
    TextSize = 10,
    Font = Enum.Font.GothamBold,
})

local config = make("Frame", gui, {
    Size = UDim2.new(0, 240, 0, 130),
    Position = UDim2.new(0.5, -120, 0.5, -80),
    BackgroundColor3 = Color3.fromRGB(14, 14, 20),
    BorderSizePixel = 0,
    Visible = false,
    ZIndex = 100,
})
make("UICorner", config, { CornerRadius = UDim.new(0, 14) })
make("UIStroke", config, {
    Color = Color3.fromRGB(45, 45, 65),
    Thickness = 1.5,
})

local configHeader = make("Frame", config, {
    Size = UDim2.new(1, 0, 0, 36),
    BackgroundColor3 = Color3.fromRGB(20, 20, 30),
    BorderSizePixel = 0,
    ZIndex = 101,
})
make("UICorner", configHeader, { CornerRadius = UDim.new(0, 14) })
make("Frame", configHeader, {
    Size = UDim2.new(1, 0, 0, 14),
    Position = UDim2.new(0, 0, 1, -14),
    BackgroundColor3 = Color3.fromRGB(20, 20, 30),
    BorderSizePixel = 0,
    ZIndex = 101,
})
make("TextLabel", configHeader, {
    Size = UDim2.new(1, -12, 1, 0),
    Position = UDim2.new(0, 12, 0, 0),
    BackgroundTransparency = 1,
    Text = "Config",
    TextColor3 = Color3.fromRGB(190, 195, 240),
    TextSize = 13,
    Font = Enum.Font.GothamBold,
    TextXAlignment = Enum.TextXAlignment.Left,
    ZIndex = 102,
})

local configBody = make("Frame", config, {
    Size = UDim2.new(1, 0, 1, -44),
    Position = UDim2.new(0, 0, 0, 40),
    BackgroundTransparency = 1,
    ZIndex = 100,
})
make("UIListLayout", configBody, {
    Padding = UDim.new(0, 8),
    SortOrder = Enum.SortOrder.LayoutOrder,
})
make("UIPadding", configBody, {
    PaddingTop = UDim.new(0, 8),
    PaddingLeft = UDim.new(0, 12),
    PaddingRight = UDim.new(0, 12),
    PaddingBottom = UDim.new(0, 8),
})

local function makeNumberRow(labelText, initialText)
    local row = make("Frame", configBody, {
        Size = UDim2.new(1, 0, 0, 30),
        BackgroundTransparency = 1,
        ZIndex = 100,
    })
    make("TextLabel", row, {
        Size = UDim2.new(0.55, 0, 1, 0),
        BackgroundTransparency = 1,
        Text = labelText,
        TextColor3 = Color3.fromRGB(160, 165, 200),
        TextSize = 12,
        Font = Enum.Font.GothamBold,
        TextXAlignment = Enum.TextXAlignment.Left,
        ZIndex = 101,
    })
    local box = make("TextBox", row, {
        Size = UDim2.new(0.4, 0, 0.72, 0),
        Position = UDim2.new(0.6, 0, 0.14, 0),
        BackgroundColor3 = Color3.fromRGB(22, 22, 32),
        TextColor3 = Color3.fromRGB(200, 205, 240),
        Text = initialText,
        TextSize = 12,
        Font = Enum.Font.GothamBold,
        ClearTextOnFocus = false,
        BorderSizePixel = 0,
        ZIndex = 101,
    })
    make("UICorner", box, { CornerRadius = UDim.new(0, 6) })
    make("UIPadding", box, { PaddingLeft = UDim.new(0, 6) })
    return box
end

local tweenSpeedBox = makeNumberRow("Tween Speed", "0.12")
local heightBox = makeNumberRow("Height", "4.5")

local function bindNumberBox(box, getter, setter)
    box.FocusLost:Connect(function()
        local value = tonumber(box.Text)
        if value then
            setter(value)
        else
            box.Text = tostring(getter())
        end
    end)
end

bindNumberBox(tweenSpeedBox, function()
    return tweenSpeed
end, function(value)
    tweenSpeed = value
end)

bindNumberBox(heightBox, function()
    return height
end, function(value)
    height = value
end)

-- The original creates this empty tween but does not call :Play().
configButton.Activated:Connect(function()
    config.Visible = not config.Visible
    TweenService:Create(configButton, TweenInfo.new(0.1), {})
end)

local function setEnabled(value)
    enabled = value

    local mainColor
    local strokeColor
    local titleColor
    if enabled then
        mainColor = Color3.fromRGB(40, 40, 62)
        strokeColor = Color3.fromRGB(100, 100, 220)
        titleColor = Color3.fromRGB(210, 215, 255)
    else
        mainColor = Color3.fromRGB(16, 16, 22)
        strokeColor = Color3.fromRGB(45, 45, 65)
        titleColor = Color3.fromRGB(160, 165, 200)
    end

    -- Runtime traces show Create calls with these exact goals and a duration of
    -- 0.15, but no Play calls for these three GUI tweens.
    TweenService:Create(main, TweenInfo.new(0.15), {
        BackgroundColor3 = mainColor,
    })
    TweenService:Create(mainStroke, TweenInfo.new(0.15), {
        Color = strokeColor,
    })
    TweenService:Create(title, TweenInfo.new(0.15), {
        TextColor3 = titleColor,
    })

    status.Text = enabled and "ON" or "OFF"
    status.TextColor3 = enabled
        and Color3.fromRGB(100, 210, 100)
        or Color3.fromRGB(90, 90, 115)
end

local function pointInGui(position, object)
    local topLeft = object.AbsolutePosition
    local size = object.AbsoluteSize
    return position.X >= topLeft.X
        and position.X <= topLeft.X + size.X
        and position.Y >= topLeft.Y
        and position.Y <= topLeft.Y + size.Y
end

-- Config-panel dragging. The virtual callbacks store the pointer's offset from
-- AbsolutePosition and rebuild the panel's UDim2 position while dragging.
local configDragging = false
local configDragOffsetX = 0
local configDragOffsetY = 0

config.InputBegan:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1
        or input.UserInputType == Enum.UserInputType.Touch
    then
        configDragging = true
        configDragOffsetX = input.Position.X - config.AbsolutePosition.X
        configDragOffsetY = input.Position.Y - config.AbsolutePosition.Y
    end
end)

UserInputService.InputChanged:Connect(function(input)
    if configDragging
        and (input.UserInputType == Enum.UserInputType.MouseMovement
            or input.UserInputType == Enum.UserInputType.Touch)
    then
        config.Position = UDim2.new(
            0,
            input.Position.X - configDragOffsetX,
            0,
            input.Position.Y - configDragOffsetY
        )
    end
end)

UserInputService.InputEnded:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1
        or input.UserInputType == Enum.UserInputType.Touch
    then
        configDragging = false
    end
end)

-- Main-panel click/drag handling. A press over the T button is excluded so its
-- Activated event can toggle the config panel.
local mainPointer
local mainDragging = false
local mainMoved = false
local mainOffsetX = 0
local mainOffsetY = 0

main.InputBegan:Connect(function(input)
    if pointInGui(input.Position, configButton) then
        return
    end
    if input.UserInputType ~= Enum.UserInputType.MouseButton1
        and input.UserInputType ~= Enum.UserInputType.Touch
    then
        return
    end

    mainPointer = input
    mainDragging = true
    mainMoved = false
    mainOffsetX = input.Position.X - main.AbsolutePosition.X
    mainOffsetY = input.Position.Y - main.AbsolutePosition.Y
end)

UserInputService.InputChanged:Connect(function(input)
    if not mainDragging or input ~= mainPointer then
        return
    end
    mainMoved = true
    main.Position = UDim2.new(
        0,
        input.Position.X - mainOffsetX,
        0,
        input.Position.Y - mainOffsetY
    )
end)

UserInputService.InputEnded:Connect(function(input)
    if input ~= mainPointer then
        return
    end
    mainPointer = nil
    mainDragging = false
    if not mainMoved then
        setEnabled(not enabled)
    end
end)

-- Separate global touch callbacks are present in the payload. They provide the
-- same tap-versus-drag behavior when the touch starts within the main panel.
local panelTouch
local panelTouchMoved = false

UserInputService.TouchStarted:Connect(function(input)
    if pointInGui(input.Position, main) and not pointInGui(input.Position, configButton) then
        panelTouch = input
        panelTouchMoved = false
    end
end)

UserInputService.TouchMoved:Connect(function(input)
    if input == panelTouch then
        panelTouchMoved = true
    end
end)

UserInputService.TouchEnded:Connect(function(input)
    if input == panelTouch then
        panelTouch = nil
        if not panelTouchMoved then
            setEnabled(not enabled)
        end
    end
end)

local moverClasses = {
    BodyVelocity = true,
    BodyPosition = true,
    BodyGyro = true,
    VectorForce = true,
    AlignPosition = true,
    AlignOrientation = true,
    LinearVelocity = true,
    AngularVelocity = true,
}

local moverNames = {
    movement = true,
    ["delete bv"] = true,
    BV = true,
}

local function removeBodyMovers()
    if not character then
        return
    end
    for _, object in ipairs(character:GetDescendants()) do
        if moverClasses[object.ClassName] or moverNames[object.Name] then
            object:Destroy()
        end
    end
end

local function findNearestTargetRoot()
    if not rootPart then
        return nil
    end

    local nearest
    local nearestDistance = 50
    for _, object in ipairs(workspace:GetDescendants()) do
        if object:IsA("Model") and object ~= character then
            local candidate = object:FindFirstChild("HumanoidRootPart")
            if candidate then
                local distance = (candidate.Position - rootPart.Position).Magnitude
                if distance < nearestDistance then
                    nearest = candidate
                    nearestDistance = distance
                end
            end
        end
    end
    return nearest
end

local function fireCommunicate(arguments)
    if not character then
        return
    end
    local communicate = character:FindFirstChild("Communicate")
    if communicate then
        communicate:FireServer(arguments)
    end
end

local function freezeCharacter()
    if not humanoid or not rootPart then
        return
    end
    savedMovement = {
        WalkSpeed = humanoid.WalkSpeed,
        JumpPower = humanoid.JumpPower,
        PlatformStand = humanoid.PlatformStand,
        AutoRotate = humanoid.AutoRotate,
    }
    humanoid.WalkSpeed = 0
    humanoid.JumpPower = 0
    humanoid.PlatformStand = true
    humanoid.AutoRotate = false
    rootPart.Velocity = Vector3.new(0, 0, 0)
    rootPart.RotVelocity = Vector3.new(0, 0, 0)
end

local function restoreCharacter()
    movementActive = false
    if movementConnection then
        movementConnection:Disconnect()
        movementConnection = nil
    end
    if humanoid and savedMovement then
        humanoid.WalkSpeed = savedMovement.WalkSpeed
        humanoid.JumpPower = savedMovement.JumpPower
        humanoid.PlatformStand = savedMovement.PlatformStand
        humanoid.AutoRotate = savedMovement.AutoRotate
    end
    savedMovement = nil
end

local function performSupaTech()
    if not enabled or movementActive or not humanoid or not rootPart then
        return
    end

    local targetRoot = findNearestTargetRoot()
    if not targetRoot then
        return
    end

    movementActive = true
    freezeCharacter()
    removeBodyMovers()

    movementConnection = RunService.Heartbeat:Connect(function()
        if not movementActive or not rootPart or not humanoid then
            return
        end
        rootPart.Velocity = Vector3.new(0, 0, 0)
        rootPart.RotVelocity = Vector3.new(0, 0, 0)
        humanoid.WalkSpeed = 0
        if humanoid:GetState() == Enum.HumanoidStateType.GettingUp then
            humanoid:ChangeState(Enum.HumanoidStateType.Physics)
        end
    end)

    fireCommunicate({
        Dash = Enum.KeyCode.W,
        Key = Enum.KeyCode.Q,
        Goal = "KeyPress",
    })

    removeBodyMovers()
    fireCommunicate({ Goal = "delete bv" })
    task.wait(0.2)
    humanoid:ChangeState(Enum.HumanoidStateType.Physics)

    -- This assignment, including the positive 60-degree X rotation, was
    -- recovered exactly by restoring CFrame in the callback harness.
    rootPart.CFrame = rootPart.CFrame
        * CFrame.Angles(math.rad(60), 0, 0)

    -- Inferred final geometry. The decoded bytecode unquestionably uses the
    -- target's CFrame/LookVector, X/Y/Z components, Vector3, CFrame.new,
    -- CFrame.Angles, math.rad, tweenSpeed, and height here. This expression is
    -- intentionally isolated until the remaining VM operations are lifted.
    local targetLook = targetRoot.CFrame.LookVector
    local horizontalLook = Vector3.new(targetLook.X, 0, targetLook.Z)
    local goalPosition = targetRoot.Position - horizontalLook * 2
        + Vector3.new(0, height, 0)
    local goalCFrame = CFrame.new(goalPosition, targetRoot.Position)
        * CFrame.Angles(math.rad(-90), 0, 0)

    local tween = TweenService:Create(
        rootPart,
        TweenInfo.new(tweenSpeed, Enum.EasingStyle.Quad, Enum.EasingDirection.Out),
        { CFrame = goalCFrame }
    )
    tween:Play()
end

local function onUppercutAnimation(track)
    if not enabled or not track or not track.Animation then
        return
    end

    local animationId = track.Animation.AnimationId
    local isUppercut = string.find(animationId, "10503381238", 1, true)
        or string.find(animationId, "13379003796", 1, true)
    if not isUppercut then
        return
    end

    task.delay(0.3, function()
        if not enabled or movementActive then
            return
        end
        if tick() - lastTrigger < 0.3 then
            return
        end
        lastTrigger = tick()

        task.spawn(performSupaTech)
        task.spawn(function()
            for _ = 1, 4 do
                task.wait(1)
            end
            restoreCharacter()
        end)
    end)
end

local function setupCharacter(newCharacter)
    restoreCharacter()
    character = newCharacter
    humanoid = character:WaitForChild("Humanoid")
    rootPart = character:WaitForChild("HumanoidRootPart")

    -- Both connections are made by the original payload. On clients where
    -- both signals fire for one animation, the tick/debounce guard suppresses
    -- the duplicate action.
    humanoid.AnimationPlayed:Connect(onUppercutAnimation)
    local animator = humanoid:FindFirstChildOfClass("Animator")
    if animator then
        animator.AnimationPlayed:Connect(onUppercutAnimation)
    end
end

player.CharacterAdded:Connect(setupCharacter)
if player.Character then
    setupCharacter(player.Character)
end
