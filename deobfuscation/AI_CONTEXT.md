# AI deobfuscation context

## Read this first

This bundle is evidence, not a claim that arbitrary VM bytecode has already
been converted back into original source. `code` contains custom virtual
dispatch bytes, **not standard Lua/Luau opcodes**. Do not silently assign
standard opcode meanings to them. Preserve observed behavior separately from
inferences, and mark every inference.

For a functionality-equivalent reconstruction, use this priority order:

1. Runtime traces and observed side effects.
2. Decoded strings and numeric constants.
3. Per-prototype instruction arrays and proven dispatch semantics.
4. Structural inference only when the first three are insufficient.

## Manifest

```json
{
  "format": "arena-luau-vm-functionality-bundle-v2",
  "goal": "observable functionality equivalence; original source structure is irrelevant",
  "profile": "wynfuscate-supax-2026-10",
  "profile_confidence": "exact",
  "source": "machine/protected-source.lua",
  "source_origin": "message.txt",
  "source_sha256": "0527abcd05b22c0c170e7a444e8f099cf2e7862b52ac6ebeee69f058cc341cae",
  "beautified_source": "machine/beautified-source.lua",
  "beautified_source_origin": "beautified.lua",
  "beautified_source_sha256": "c2948ac9beefea86e6ec00f32e801fa0515f19465d2d4e8e9a3d16d65914bc7e",
  "instrumented_runner": "runtime/instrumented-vm.luau",
  "instrumented_runner_origin": "run.txt",
  "instrumented_runner_sha256": "121c0f47d3a12193cc78cfbf1f726c7c7f49599de6c42a7cf5f5346762e58a06",
  "portable_runtime": true,
  "portable_runtime_requested": true,
  "portable_runtime_platform": "Linux x86-64",
  "dump": "machine/raw-vm-dump.txt",
  "dump_origin": "/home/user/arena/deobfuscation/vm_dump.txt",
  "dump_sha256": "b300ae1d8e5b09f4d3778e713e8e683c587f865be525f784e292adbca7c10989",
  "prototype_count": 47,
  "instruction_count": 2033,
  "dispatch_byte_count": 111,
  "decoded_string_count": 359,
  "constant_count": 1664,
  "page_failures": [],
  "limitations": [
    "Custom dispatch bytes are not standard Luau opcodes.",
    "Behavioral equivalence requires callback and environment coverage, not only static strings.",
    "External Roblox server responses cannot be recreated from an offline sample unless captured.",
    "Original names/comments/layout may be unrecoverable, but they are not required for this goal."
  ]
}
```

## VM summary

- Prototypes: 47
- Instructions: 2033
- Distinct dispatch bytes: 111
- Decoded strings: 359
- Constants: 1664
- Page failures: 0

Dispatch histogram:

```text
0:13 1:15 2:4 3:10 4:46 5:53 6:23 7:40 8:35 9:44 10:28 11:66 12:14 13:15 14:29 15:14 18:15 21:34 22:47 42:3 48:13 56:3 57:4 66:9 67:4 68:3 73:10 74:18 76:2 77:8 78:9 79:5 90:2 92:5 93:2 94:3 95:2 98:49 99:2 101:10 104:4 115:10 116:5 117:7 120:9 121:11 123:2 124:3 126:5 128:18 129:24 130:3 132:2 134:8 135:2 137:7 138:4 139:6 143:2 144:1 149:2 151:15 163:29 165:2 174:1 189:1 190:1 192:27 194:30 195:29 196:12 197:136 198:49 202:6 203:35 204:8 205:5 206:12 207:2 209:2 210:7 212:22 213:11 214:2 215:19 216:61 218:1 219:5 220:11 221:76 222:1 223:2 224:16 228:63 230:1 232:3 233:3 234:1 236:15 237:1 238:3 239:1 243:12 244:31 245:30 248:29 249:35 250:66 251:54 254:114 255:89
```

## Numeric constants

The complete indexed array is in `machine/constants.json`. Value counts:

```text
0.050000000000000003:1 0.10000000000000001:1 0.12:1 0.14000000000000001:1 0.14999999999999999:1 0.20000000000000001:1 0.29999999999999999:1 0.40000000000000002:1 0.44:1 0.5:1 0.55000000000000004:1 0.59999999999999998:1 0.71999999999999997:1 0.78000000000000003:1 1:1 1.5:1 2:1 4.5:1 7:1 14:1 16:1 18:1 31:795 41:549 43:188 50:1 59:108 256:1
```

## Decoded strings

The TSV copy is in `machine/decoded-strings.tsv`. Empty byte strings are shown as `<empty>`.

```text
   1  pcall
   2  tostring
   3  1
   4  .*%:(%-?%d+)%:%s
   5  match
   6  .*%:(%-?%d+)%:
   7  getgenv
   8  restorefunction
   9  string
  10  byte
  11  char
  12  setmetatable
  13  rawget
  14  rawset
  15  pairs
  16  type
  17  getfenv
  18  setfenv
  19  game
  20  Players
  21  GetService
  22  TweenService
  23  UserInputService
  24  RunService
  25  LocalPlayer
  26  tweenSpeed
  27  height
  28  CoreGui
  29  SupaTechV2
  30  FindFirstChild
  31  PlayerGui
  32  Destroy
  33  Instance
  34  new
  35  ScreenGui
  36  Name
  37  ResetOnSpawn
  38  Enum
  39  ZIndexBehavior
  40  Sibling
  41  DisplayOrder
  42  Parent
  43  WaitForChild
  44  Frame
  45  UDim2
  46  Size
  47  Position
  48  Color3
  49  fromRGB
  50  BackgroundColor3
  51  BorderSizePixel
  52  UICorner
  53  UDim
  54  CornerRadius
  55  UIStroke
  56  Color
  57  Thickness
  58  TextLabel
  59  BackgroundTransparency
  60  Supax\nTech
  61  Text
  62  TextColor3
  63  TextSize
  64  Font
  65  GothamBold
  66  TextButton
  67  T
  68  AutoButtonColor
  69  ZIndex
  70  OFF
  71  Visible
  72  Config
  73  TextXAlignment
  74  Left
  75  UIListLayout
  76  Padding
  77  SortOrder
  78  LayoutOrder
  79  UIPadding
  80  PaddingTop
  81  PaddingLeft
  82  PaddingRight
  83  PaddingBottom
  84  Tween Speed
  85  Height
  86  InputBegan
  87  Connect
  88  InputChanged
  89  InputEnded
  90  Activated
  91  TouchStarted
  92  TouchMoved
  93  TouchEnded
  94  CharacterAdded
  95  Character
  96  islclosure
  97  delay
  98  __mode
  99  __pairs
 100  __call
 101  replaceclosure
 102  -inf
 103  __len
 104  running
 105  linedefined
 106  format
 107  string expected
 108  newcclosure
 109  S
 110  closed
 111  number expected
 112  hookfunc
 113  traceback
 114  error
 115  __metatable
 116  name
 117  info
 118  fmod
 119  sqrt
 120  currentline
 121  __index
 122  hookmetamethod
 123  getupvalue
 124  k
 125  concat
 126  boolean
 127  lastlinedefined
 128  _ENV
 129  jic
 130  max
 131  nan
 132  gethook
 133  l
 134  nSl
 135  reg
 136  abs
 137  setreadonly
 138  locked
 139  n
 140  nv_inline
 141  134
 142  f
 143  table expected
 144  dump
 145  C
 146  __newindex
 147  x
 148  hookfunction
 149  debug
 150  __uv
 151  unpack
 152  v
 153  [C]
 154  what
 155  floor
 156  random
 157  LocalScript:134: 2r9xee
 158  min
 159  inf
 160  nsl
 161  table
 162  setupvalue
 163  __tostring
 164  __ipairs
 165  jgc
 166  insert
 167  owner
 168  pack
 169  value
 170  gfvs
 171  func
 172  nups
 173  s
 174  function
 175  jit
 176  test error message
 177  source
 178  pow
 179  huge
 180  number
 181  nv_uv
 182  ceil
 183  getinfo
 184  gmatch
 185  nv
 186  sub
 187  islclosure
 188  delay
 189  __mode
 190  __pairs
 191  __call
 192  replaceclosure
 193  -inf
 194  __len
 195  running
 196  linedefined
 197  format
 198  string expected
 199  newcclosure
 200  S
 201  closed
 202  number expected
 203  hookfunc
 204  traceback
 205  error
 206  __metatable
 207  name
 208  info
 209  fmod
 210  sqrt
 211  currentline
 212  __index
 213  hookmetamethod
 214  getupvalue
 215  k
 216  concat
 217  boolean
 218  lastlinedefined
 219  _ENV
 220  jic
 221  max
 222  nan
 223  gethook
 224  l
 225  nSl
 226  reg
 227  abs
 228  setreadonly
 229  locked
 230  n
 231  nv_inline
 232  134
 233  f
 234  table expected
 235  dump
 236  C
 237  __newindex
 238  x
 239  hookfunction
 240  debug
 241  __uv
 242  unpack
 243  v
 244  [C]
 245  what
 246  floor
 247  random
 248  LocalScript:134: 2r9xee
 249  min
 250  inf
 251  nsl
 252  table
 253  setupvalue
 254  __tostring
 255  __ipairs
 256  jgc
 257  insert
 258  owner
 259  pack
 260  value
 261  gfvs
 262  func
 263  nups
 264  s
 265  function
 266  jit
 267  test error message
 268  source
 269  pow
 270  huge
 271  number
 272  nv_uv
 273  ceil
 274  getinfo
 275  gmatch
 276  nv
 277  sub
 278  bx}}5?>vzgvye|7}|3[tEmKMO
 279  <empty>
 280  workspace
 281  GetDescendants
 282  Model
 283  IsA
 284  HumanoidRootPart
 285  Magnitude
 286  KeyCode
 287  W
 288  Dash
 289  Q
 290  Key
 291  KeyPress
 292  Goal
 293  Communicate
 294  FireServer
 295  ClassName
 296  BodyVelocity
 297  moveme
 298  delete bv
 299  BV
 300  BodyPosition
 301  BodyGyro
 302  VectorForce
 303  AlignPosition
 304  AlignOrientation
 305  LinearVelocity
 306  AngularVelocity
 307  Heartbeat
 308  task
 309  wait
 310  CFrame
 311  Angles
 312  math
 313  rad
 314  WalkSpeed
 315  JumpPower
 316  PlatformStand
 317  AutoRotate
 318  Disconnect
 319  Vector3
 320  Velocity
 321  RotVelocity
 322  HumanoidStateType
 323  Physics
 324  ChangeState
 325  LookVector
 326  X
 327  Y
 328  Z
 329  TweenInfo
 330  EasingStyle
 331  Quad
 332  EasingDirection
 333  Out
 334  Create
 335  Play
 336  GettingUp
 337  ON
 338  TextBox
 339  ClearTextOnFocus
 340  FocusLost
 341  tonumber
 342  UserInputType
 343  MouseButton1
 344  Touch
 345  AbsolutePosition
 346  MouseMovement
 347  AbsoluteSize
 348  Vector2
 349  tick
 350  spawn
 351  Animation
 352  AnimationId
 353  find
 354  10503381238
 355  13379003796
 356  Humanoid
 357  Animator
 358  FindFirstChildOfClass
 359  AnimationPlayed
```

## Profile-specific recovered behavior

This dump matches the fully analyzed repository sample. The following
notes and reconstruction are available as additional evidence.

# `message.txt` deobfuscation notes

## Automated deobfuscator / Arena.ai exporter

`tools/deobfuscate.py` turns a supported wYnFuscate source into a portable
Arena.ai reconstruction task:

```bash
# Protected source -> beautified source -> VM dump -> Arena upload bundle
python3 tools/deobfuscate.py source message.txt -o analysis

# Or package a dump and its evidence without rerunning the protected wrapper
python3 tools/deobfuscate.py dump deobfuscation/vm_dump.txt -o analysis/ai \
  --source message.txt \
  --beautified beautified.lua \
  --instrumented run.txt \
  --portable-runtime
```

The source command produces `analysis/ai/arena-reconstruction-bundle.zip` and
`analysis/ai/ARENA_UPLOAD_MESSAGE.txt`. Upload the ZIP in a new Arena.ai Agent
conversation and paste the message file's contents. The ZIP embeds
`ARENA_TASK.md`, which explicitly requires a clean Luau reconstruction with
observable behavior matching 1:1. Original names, formatting, source layout,
control flow, and VM layout are non-goals.

The export contains the protected and beautified sources, raw and parsed VM
data, all decoded strings and constants, per-prototype instruction tables,
known runtime traces, the current readable reconstruction as a hypothesis,
analysis support scripts, the instrumented runner, and (by default in source
mode) portable `luau` and `luau-compile` binaries. Use
`--no-portable-runtime` to omit those binaries. In dump mode, binaries are
opt-in with `--portable-runtime`; source, beautified source, and an instrumented
runner can be supplied with the options shown above.

The embedded Arena task tells the next Agent to execute root and callback paths
in a fake environment, improve Vector/CFrame stubs, prove custom dispatch
semantics as needed, and differential-test ordered side effects. It forbids
stopping at a visual/UI approximation or guessing behavior from strings. Its
required deliverables are `reconstructed.lua`, `BEHAVIOR_CONTRACT.md`,
`DIFFERENTIAL_RESULTS.md`, and `UNRESOLVED.md`.

This is intentionally a **wYnFuscate profile**, not a universal Lua
deobfuscator. The dump/export stage accepts this repository's dump format. The
source stage recognizes the protected layout solved here; a newly randomized
protector can require another instrumentation profile. Custom dispatch bytes
are not standard Luau opcodes and must be proven from handler code or controlled
traces. The tool packages enough evidence and portable support for an Arena.ai
Agent to continue that analysis; it does not claim that static extraction alone
proves behavioral equivalence.

## Current result

The protected payload is a Roblox/Luau movement script named **Supax Tech V2**.
The decoder and paged virtual machine have been executed in a fake Roblox
environment without contacting Roblox or the network.

The runtime dump currently proves:

- 47 virtual prototypes, numbered 0–46.
- 2,033 virtual instructions.
- 111 distinct VM dispatch bytes.
- 359 decoded strings.
- No prototype page-decoding failures.
- The root prototype has 464 instructions and creates the complete GUI.
- The intended root branch is instruction 26 → 31. Instructions 27–28 are an
  infinite decoy loop.
- A post-execution cleanup routine tries to erase the VM's own tables and then
  enters a deliberate infinite loop. It was replaced with a no-op in the
  analysis harness so registered callbacks could be exercised.

`deobfuscated.lua` is the readable reconstruction. Its GUI, defaults, input
wiring, animation IDs, state changes, body-mover cleanup, and remote payloads
are based on runtime observations. The final target-facing CFrame expression
inside `performSupaTech` is still marked as inferred rather than byte-perfect.

## Confirmed behavior

### GUI

- `ScreenGui.Name = "SupaTechV2"`
- `ResetOnSpawn = false`
- `DisplayOrder = 9999`
- Compact 80×80 main panel with title `Supax`, config button `T`, and `OFF` /
  `ON` state text.
- The backing enabled flag starts as `true` even though the initial label says
  `OFF`. A matching animation schedules the action immediately after load; the
  first main-panel tap changes the flag to false and leaves the label `OFF`,
  and the second changes it back to true and displays `ON`.
- Hidden 240×130 `Config` panel.
- `Tween Speed` defaults to `0.12`.
- `Height` defaults to `4.5`.
- Invalid text-box input is replaced with the last valid value.
- The config button toggles panel visibility and creates an empty 0.1-second
  tween without playing it.
- The main panel's state transition creates three 0.15-second color tweens
  without playing them, then directly changes the state text and its color.
- Both panels have independent dragging logic. Main-panel input excludes the
  bounds of the `T` button. Global touch handlers distinguish a tap from a
  drag.

### Trigger and movement setup

The script listens to both `Humanoid.AnimationPlayed` and, when available,
`Animator.AnimationPlayed`. It matches either of these animation IDs using a
plain `string.find`:

- `10503381238` — TSBG uppercut
- `13379003796` — uppercut while holding a weapon

When enabled, a matching animation schedules a 0.3-second delayed closure. The
closure uses `tick()` for debouncing and starts two tasks. The movement worker:

1. Searches `workspace:GetDescendants()` for a nearby `Model` with a
   `HumanoidRootPart` (the bytecode contains a 50-stud limit).
2. Saves humanoid movement state.
3. Sets `WalkSpeed = 0`, `JumpPower = 0`, `PlatformStand = true`, and
   `AutoRotate = false`.
4. Zeros root-part `Velocity` and `RotVelocity`.
5. Removes legacy and modern body movers from the character.
6. Connects a temporary `RunService.Heartbeat` callback that keeps velocity
   zero and enforces the movement state.
7. Fires the game's `Communicate` remote with exactly:

   ```lua
   {
       Dash = Enum.KeyCode.W,
       Key = Enum.KeyCode.Q,
       Goal = "KeyPress",
   }
   ```

8. Cleans body movers again, then fires exactly `{ Goal = "delete bv" }`.
9. Waits 0.2 seconds and changes the humanoid state to
   `Enum.HumanoidStateType.Physics`.
10. Performs the confirmed assignment
    `rootPart.CFrame = rootPart.CFrame * CFrame.Angles(math.rad(60), 0, 0)`.
11. Uses additional CFrame/tween-related logic involving the selected target
    and the configured height and tween speed. The final high-level expression
    for this last phase remains the one explicitly inferred section in the
    readable reconstruction.

The second spawned task executes four `task.wait(1)` calls before resetting the
movement window and cleanup state.

### Body movers named by the payload

`BodyVelocity`, `movement`, `BV`, `BodyPosition`, `BodyGyro`, `VectorForce`,
`AlignPosition`, `AlignOrientation`, `LinearVelocity`, and `AngularVelocity`.

## Prototype map

| Prototype | Recovered purpose |
| ---: | --- |
| 0 | Root setup, GUI construction, and event registration |
| 5 | Nearest eligible model/root search |
| 6 | Root-part distance helper |
| 7–9 | KeyPress/delete-bv remote sequence and body-mover cleanup |
| 10 | Main movement worker |
| 11 | Capture humanoid movement state |
| 15 | Freeze humanoid and zero root velocity |
| 17–19 | Heartbeat enforcement helpers |
| 20 | Change humanoid state to `Physics` |
| 24 | Toggle enabled state and GUI colors/text |
| 26 | Shared numeric `FocusLost` validator |
| 27–29 | Config-panel drag callbacks |
| 30–31 | Config-panel visibility callback/helper |
| 32–34 | Main-panel mouse/touch begin/change/end callbacks |
| 35–37 | Global touch tap/drag callbacks |
| 40 | Delayed/debounced trigger scheduler |
| 41 | Movement-worker task wrapper |
| 42 | Four-second reset task |
| 43 | Animation ID filter/callback |
| 44–46 | Character setup and AnimationPlayed connections |

## Files

- `arena-reconstruction-bundle.zip` — ready-to-upload Arena.ai archive with
  embedded task instructions, evidence, analysis runtime, and support scripts.
- `ARENA_UPLOAD_MESSAGE.txt` — message to paste after attaching the ZIP in a new
  Arena.ai Agent conversation.
- `ARENA_TASK.md` — the same functionality-equivalence mandate embedded in the
  archive, also checked in for easy review.
- `AI_CONTEXT.md` — single-file, AI-oriented evidence package with all strings,
  profile notes, the readable reconstruction, and every virtual instruction.
- `../tools/deobfuscate.py` — end-to-end source unpacker and Arena.ai
  reconstruction-bundle exporter.
- `vm_dump.txt` — authoritative runtime dump containing all prototype arrays,
  constants, metadata, and decoded strings.
- `prototypes.json` — parsed machine-readable version of the dump.
- `decoded_strings.tsv` — all 359 strings, with tabs/newlines escaped.
- `vm_summary.txt` — instruction and dispatch statistics.
- `traces/ui_properties.tsv` — exact constructor/property observations for the
  GUI.
- `traces/callback_dispatch_trace.tsv` — callback-to-prototype dispatch traces.
- `traces/toggle_colors.log` — exact enabled/disabled tween goals, durations,
  status text, and status colors.
- `traces/animation_trigger.log` — concise execution evidence for enabling the
  GUI, matching the animation, freezing the humanoid, rotating the root part,
  and firing both remotes.
- `../tools/parse_vm_dump.py` — reproduces the JSON, TSV, and summary from the
  runtime dump.

## Reproducing the dump

From the repository root:

```bash
python3 build_run.py
chmod +x ./luau                 # only needed if the checkout lost tool modes
./luau run.txt > vm-run.out
python3 tools/parse_vm_dump.py vm-run.out \
  --json deobfuscation/prototypes.json \
  --strings deobfuscation/decoded_strings.tsv
```

The rebuilt runner has been checked against the persisted artifacts: it again
produces 47 prototypes, 2,033 instructions, 359 strings, and zero page failures;
its prototype arrays, constants, and strings are byte-for-byte equivalent after
parsing.


## Existing readable reconstruction

```lua
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

```

## Virtual instruction listings

Columns are `pc code op A B C D E F G Cjump`. A `_` is a missing value.
The same listings are split into one file per prototype under `instructions/`.

### Prototype 0

Instruction count: 464

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	174	35	169	116	0	0	0	0	0	0
2	144	0	0	0	0	0	0	0	0	4
3	244	2	74	1	0	0	0	0	0	8
4	189	0	35	169	0	0	0	0	0	12
5	98	3	1	0	0	0	0	0	0	16
6	4	2	2	3	0	0	0	0	0	20
7	215	0	2	1	3	0	0	0	0	24
8	244	3	7	96	0	0	0	0	0	32
9	210	3	1	2	0	0	0	0	0	36
10	22	2	3	0	0	0	0	0	0	44
11	220	4	2	2	116	2	115	2	0	48
12	74	4	69	180	0	0	0	0	0	56
13	220	4	2	2	48	166	49	166	0	60
14	12	48	56	110	0	0	0	0	0	68
15	151	4	4	48	0	0	0	0	0	72
16	137	3	4	230	81	0	0	0	0	76
17	14	5	0	0	0	0	0	0	0	84
18	78	3	168	182	5	0	0	0	0	88
19	216	50	197	4	1	0	0	0	0	96
20	21	4	0	0	0	0	0	0	0	104
21	74	4	194	182	0	0	0	0	0	108
22	14	6	220	5	0	0	0	0	0	112
23	104	6	85	184	3	0	0	0	0	116
24	216	171	198	4	1	0	0	0	0	124
25	216	236	198	4	0	0	0	0	0	132
26	8	4	124	184	0	0	0	0	0	140
27	237	7	1	8	0	0	0	0	0	144
28	6	171	71	0	0	0	0	0	0	152
29	6	88	71	0	0	0	0	0	0	156
30	6	241	184	0	0	0	0	0	0	160
31	245	0	154	21	0	0	0	0	0	164
32	244	1	33	40	0	0	0	0	0	168
33	8	1	60	186	0	0	0	0	0	172
34	238	1	1	2	21	112	0	0	0	176
35	236	2	1	8	0	0	0	0	0	184
36	248	2	1	157	243	0	0	0	0	192
37	236	3	2	4	0	0	0	0	0	200
38	22	3	0	0	0	0	0	0	0	208
39	8	3	160	188	0	0	0	0	0	212
40	215	4	0	5	2	0	0	0	0	216
41	197	6	6	240	148	243	148	0	0	224
42	4	4	3	1	0	0	0	0	0	232
43	215	3	0	4	2	0	0	0	0	236
44	197	5	5	170	25	168	25	0	0	244
45	5	3	3	1	0	0	0	0	0	252
46	215	3	0	4	2	0	0	0	0	256
47	245	5	86	69	0	0	0	0	0	264
48	5	3	3	1	0	0	0	0	0	268
49	215	3	0	4	2	0	0	0	0	272
50	245	5	254	126	0	0	0	0	0	280
51	4	3	3	1	0	0	0	0	0	284
52	215	3	0	4	2	0	0	0	0	288
53	245	5	175	183	0	0	0	0	0	296
54	5	3	3	1	0	0	0	0	0	300
55	215	3	0	4	2	0	0	0	0	304
56	245	5	72	240	0	0	0	0	0	312
57	5	3	3	1	0	0	0	0	0	316
58	215	3	0	4	2	0	0	0	0	320
59	245	5	229	41	0	0	0	0	0	328
60	5	3	3	1	0	0	0	0	0	332
61	215	3	0	4	2	0	0	0	0	336
62	245	5	158	98	0	0	0	0	0	344
63	5	3	3	1	0	0	0	0	0	348
64	215	3	0	4	2	0	0	0	0	352
65	245	73	86	0	0	0	0	0	0	360
66	4	0	0	0	0	0	0	0	0	364
67	215	0	0	0	199	0	0	0	0	368
68	244	0	0	0	0	0	0	0	0	376
69	4	0	0	0	0	0	0	0	0	380
70	7	0	0	0	0	0	0	0	0	384
71	98	0	0	0	0	0	0	0	0	388
72	4	0	0	0	0	0	0	0	0	392
73	245	0	0	0	0	0	0	0	0	396
74	206	0	0	0	0	0	0	0	0	400
75	22	0	0	0	0	0	0	0	0	408
76	244	0	0	0	0	0	0	0	0	412
77	206	0	0	0	0	0	0	88	124	416
78	18	0	0	0	0	0	0	0	0	424
79	22	0	0	0	0	0	0	0	0	428
80	244	0	0	0	0	0	0	0	0	432
81	206	0	0	0	0	0	0	0	0	436
82	22	0	0	0	0	0	0	0	0	444
83	245	0	0	0	0	0	0	0	0	448
84	206	0	0	0	0	0	0	0	0	452
85	22	0	0	0	0	0	0	0	0	460
86	249	0	0	0	0	0	0	0	0	464
87	190	0	0	0	0	0	0	0	0	472
88	14	0	0	0	0	0	0	0	0	480
89	224	0	0	0	0	0	0	0	0	484
90	21	0	0	0	0	0	0	0	0	488
91	21	0	0	0	0	0	0	0	0	492
92	14	0	0	0	0	0	0	0	0	496
93	56	0	0	0	0	0	0	0	0	500
94	101	0	0	0	0	0	0	0	0	504
95	15	0	0	0	0	0	0	0	0	508
96	250	0	0	0	0	0	0	0	0	512
97	15	0	0	0	0	0	0	0	0	520
98	250	0	0	0	0	0	0	0	0	524
99	98	0	0	0	0	0	0	0	0	532
100	98	0	0	0	0	0	0	0	0	536
101	98	0	0	0	0	0	0	0	0	540
102	244	0	0	0	0	0	0	0	0	544
103	206	0	0	0	0	0	0	0	0	548
104	22	0	0	0	0	0	0	0	0	556
105	220	0	0	0	0	0	0	0	0	560
106	73	0	0	0	0	0	0	0	0	568
107	220	0	0	0	0	0	0	0	0	572
108	9	0	0	0	0	0	0	0	0	580
109	248	0	0	0	0	0	0	0	0	584
110	220	0	0	0	0	0	0	0	0	592
111	7	0	0	0	0	0	0	0	0	600
112	8	0	0	0	0	0	0	0	0	604
113	219	0	0	0	0	0	0	0	0	608
114	6	0	0	0	0	0	0	0	0	616
115	197	0	0	0	0	0	0	0	0	620
116	207	0	0	0	0	0	0	0	0	628
117	205	0	43	0	0	0	0	0	0	636
118	250	0	0	0	0	0	0	0	0	644
119	204	0	0	0	0	0	0	0	0	652
120	195	0	71	241	152	41	0	0	0	660
121	250	0	0	0	0	0	0	0	0	668
122	203	0	0	70	0	0	0	0	126	676
123	245	0	0	0	0	0	0	0	0	684
124	98	0	0	145	216	105	0	0	0	688
125	5	0	0	0	190	0	0	0	0	692
126	249	0	0	0	0	0	0	0	0	696
127	245	0	216	89	225	0	0	0	0	704
128	206	0	0	0	0	0	0	0	0	708
129	67	0	0	0	223	138	166	0	0	716
130	220	0	0	0	113	0	0	0	0	724
131	251	0	0	0	0	0	0	0	0	732
132	7	0	0	0	0	0	0	0	0	740
133	197	0	0	0	0	0	0	0	0	744
134	207	0	0	0	0	0	0	0	0	752
135	22	0	0	0	0	0	0	0	0	760
136	197	0	0	0	0	0	0	0	0	764
137	221	0	0	0	0	0	0	0	0	772
138	14	0	0	0	0	0	0	0	0	780
139	228	0	0	0	0	0	0	0	0	784
140	250	0	0	0	0	0	0	0	0	792
141	197	0	0	0	0	0	0	0	0	800
142	221	0	0	0	0	0	0	0	0	808
143	192	0	0	0	0	0	0	0	111	816
144	228	225	118	8	150	206	207	0	0	820
145	251	0	0	0	0	0	0	0	0	828
146	197	0	0	0	0	0	0	0	0	836
147	221	0	0	0	0	0	0	0	0	844
148	228	0	0	0	0	0	0	0	0	852
149	250	0	0	0	0	0	0	0	0	860
150	203	0	0	0	0	0	0	0	0	868
151	250	0	0	0	0	0	0	0	0	876
152	197	0	0	0	0	0	0	0	0	884
153	12	0	0	0	0	0	0	0	0	892
154	212	0	0	0	0	0	0	0	0	896
155	197	0	0	0	0	0	0	0	0	904
156	213	0	0	0	0	0	0	0	0	912
157	250	0	0	0	0	0	0	0	0	920
158	197	0	0	0	0	0	0	0	0	928
159	12	0	0	0	0	0	0	0	0	936
160	212	0	0	0	0	0	0	0	0	940
161	22	0	0	0	0	0	0	0	0	948
162	197	0	0	0	0	0	0	0	0	952
163	221	0	0	0	0	0	0	0	0	960
164	228	0	0	0	0	0	0	0	0	968
165	250	0	0	0	0	0	0	0	0	976
166	224	0	0	0	0	0	0	0	0	984
167	250	0	0	0	0	0	0	0	0	988
168	197	0	0	0	0	0	0	0	0	996
169	12	0	0	0	0	0	0	0	0	1004
170	212	0	0	0	0	0	0	0	0	1008
171	22	0	0	0	0	0	0	0	0	1016
172	197	0	0	0	0	0	0	0	0	1020
173	221	0	0	0	177	137	62	112	70	1028
174	15	76	144	0	0	0	0	0	0	1036
175	228	0	0	0	26	72	0	0	0	1040
176	250	0	0	0	0	0	0	0	0	1048
177	197	0	0	0	0	0	0	0	0	1056
178	221	0	0	0	0	0	0	0	0	1064
179	224	0	0	0	0	0	0	0	0	1072
180	228	0	0	0	0	0	0	0	0	1076
181	251	0	0	0	0	0	0	0	0	1084
182	203	0	0	0	0	0	0	0	0	1092
183	202	0	0	0	0	0	0	0	0	1100
184	197	0	0	0	0	0	0	0	0	1108
185	221	0	0	0	0	0	0	0	0	1116
186	228	0	0	0	0	0	0	0	0	1124
187	251	0	0	0	0	0	0	0	0	1132
188	203	0	0	0	0	0	0	0	0	1140
189	195	0	0	0	0	0	0	0	0	1148
190	250	0	0	0	0	0	0	0	0	1156
191	197	0	0	0	0	0	0	0	0	1164
192	13	0	0	0	0	0	0	0	0	1172
193	212	174	250	0	0	0	0	0	0	1176
194	22	0	0	0	0	0	0	0	0	1184
195	197	0	0	0	0	0	0	0	0	1188
196	221	0	0	0	0	0	0	0	0	1196
197	192	0	0	0	0	0	0	0	0	1204
198	228	0	78	180	75	220	0	0	0	1208
199	251	0	0	0	223	3	129	0	0	1216
200	197	0	0	0	0	0	0	0	0	1224
201	15	0	0	167	0	0	0	0	0	1232
202	192	0	0	0	0	0	0	0	0	1236
203	134	231	83	138	75	105	0	0	0	1240
204	14	0	0	0	0	0	0	0	0	1244
205	228	0	0	0	0	77	165	0	0	1248
206	251	0	0	0	0	0	0	141	0	1256
207	197	0	0	0	0	231	83	138	0	1264
208	221	0	0	0	0	0	0	0	0	1272
209	228	0	0	0	0	0	0	0	0	1280
210	250	0	0	0	0	0	0	0	0	1288
211	203	0	0	0	0	0	0	0	0	1296
212	202	0	0	0	0	0	0	0	0	1304
213	197	0	0	0	0	0	0	0	0	1312
214	221	0	0	0	0	0	0	0	0	1320
215	228	0	0	0	0	0	0	0	0	1328
216	250	0	0	0	0	0	0	0	0	1336
217	203	0	0	0	0	0	0	0	0	1344
218	195	0	0	0	0	0	0	0	0	1352
219	251	0	0	0	0	0	0	0	0	1360
220	204	0	0	0	0	0	0	0	0	1368
221	203	0	0	0	0	0	0	0	0	1376
222	197	0	0	0	0	0	0	0	0	1384
223	12	0	0	0	0	0	0	0	0	1392
224	212	0	0	0	0	0	0	0	0	1396
225	197	0	0	0	0	0	0	0	0	1404
226	213	0	0	0	0	0	0	0	0	1412
227	251	0	0	0	0	0	0	0	0	1420
228	197	0	0	0	0	0	0	0	0	1428
229	13	0	0	0	0	0	0	0	0	1436
230	212	0	0	0	0	0	0	0	0	1440
231	22	0	0	0	0	0	0	0	0	1448
232	197	0	0	0	0	0	0	0	0	1452
233	221	0	0	0	0	0	0	0	0	1460
234	15	0	0	0	0	0	0	0	0	1468
235	228	0	0	0	0	0	0	0	0	1472
236	251	0	0	0	0	0	0	0	0	1480
237	197	0	0	0	0	0	0	0	0	1488
238	221	0	0	0	0	0	0	0	0	1496
239	224	0	0	119	84	0	0	0	0	1504
240	228	0	0	0	0	0	0	0	96	1508
241	250	0	0	0	0	0	0	0	0	1516
242	203	0	0	0	0	0	0	0	0	1524
243	202	0	0	0	0	0	0	0	0	1532
244	197	0	0	0	0	0	0	0	0	1540
245	221	0	0	0	0	0	0	0	0	1548
246	228	0	0	0	0	0	0	0	0	1556
247	251	0	0	0	0	0	0	0	0	1564
248	203	0	0	0	0	0	0	0	0	1572
249	195	0	0	0	0	0	0	0	0	1580
250	250	0	0	0	0	0	0	0	0	1588
251	98	0	0	0	0	0	0	0	0	1596
252	21	0	0	0	0	0	0	0	0	1600
253	197	0	0	0	0	0	0	0	0	1604
254	12	0	0	0	0	0	0	0	0	1612
255	212	0	0	0	0	0	0	0	0	1616
256	22	0	0	0	0	0	0	0	0	1624
257	197	0	0	0	197	0	0	0	0	1628
258	221	0	0	0	22	0	0	0	0	1636
259	14	0	0	0	117	0	0	0	0	1644
260	228	0	0	0	6	0	0	0	0	1648
261	250	0	0	0	0	0	0	0	0	1656
262	197	0	0	0	0	0	0	0	0	1664
263	224	0	0	0	0	0	0	0	0	1672
264	192	0	0	0	0	0	0	0	0	1676
265	134	0	0	0	0	0	0	0	0	1680
266	224	0	0	0	0	0	0	0	0	1684
267	14	0	0	0	0	0	0	0	0	1688
268	134	0	0	0	0	0	0	0	0	1692
269	4	0	0	0	0	0	0	0	0	1696
270	251	0	0	0	0	0	0	0	0	1700
271	197	0	0	0	0	0	0	0	0	1708
272	221	0	0	0	0	0	0	0	0	1716
273	228	0	0	0	0	0	0	0	0	1724
274	251	0	0	0	0	0	0	0	0	1732
275	203	0	0	0	0	0	0	0	0	1740
276	204	0	0	0	0	0	0	0	0	1748
277	203	0	0	0	0	0	0	0	0	1756
278	197	0	0	0	0	0	0	0	0	1764
279	13	226	0	0	0	0	0	0	0	1772
280	212	181	0	0	0	0	0	0	0	1776
281	197	0	0	0	0	0	0	0	0	1784
282	213	0	0	0	0	0	0	0	0	1792
283	250	0	0	0	0	0	0	0	0	1800
284	197	0	0	0	0	0	0	0	0	1808
285	12	0	0	0	0	0	0	0	0	1816
286	212	0	0	0	0	0	0	0	0	1820
287	22	0	0	0	0	0	0	0	0	1828
288	197	0	0	0	0	0	0	0	0	1832
289	221	0	0	0	0	0	0	0	0	1840
290	228	0	0	0	0	0	0	0	0	1848
291	250	0	0	0	0	0	0	0	0	1856
292	15	0	0	0	0	0	0	0	0	1864
293	250	0	0	214	0	0	0	0	30	1868
294	197	0	0	0	0	0	0	0	99	1876
295	13	0	0	0	0	0	0	0	0	1884
296	212	0	0	0	0	0	0	0	0	1888
297	22	0	0	0	0	0	0	0	226	1896
298	197	0	0	0	0	0	0	0	181	1900
299	221	0	0	0	0	0	0	0	0	1908
300	14	0	0	0	0	0	0	0	0	1916
301	228	0	0	0	0	0	0	0	0	1920
302	250	0	0	0	0	0	0	0	0	1928
303	197	0	0	0	0	0	0	0	0	1936
304	221	0	0	0	0	0	0	0	0	1944
305	228	0	0	0	0	0	0	0	0	1952
306	250	0	0	0	0	0	0	0	0	1960
307	203	0	0	0	0	0	0	0	0	1968
308	203	0	0	0	0	0	0	0	0	1976
309	197	0	0	0	0	0	0	0	0	1984
310	13	0	0	0	158	0	0	0	0	1992
311	212	0	0	0	247	0	0	0	0	1996
312	197	0	0	0	0	0	0	0	0	2004
313	213	0	0	0	0	0	0	0	0	2012
314	251	0	0	0	0	0	0	0	0	2020
315	197	0	0	0	0	0	0	0	0	2028
316	12	0	0	0	0	0	0	0	0	2036
317	212	0	0	0	0	0	0	0	0	2040
318	22	0	0	0	0	0	0	0	18	2048
319	197	0	0	0	0	0	0	0	157	2052
320	221	0	0	0	0	0	0	0	19	2060
321	192	0	0	0	0	0	0	0	0	2068
322	228	0	0	0	0	0	0	0	0	2072
323	250	0	0	0	0	0	0	0	0	2080
324	197	0	0	0	0	0	0	0	0	2088
325	221	0	0	0	0	0	0	0	0	2096
326	221	0	0	0	0	0	0	0	0	2104
327	134	0	0	0	0	0	0	0	0	2112
328	5	0	0	0	0	0	0	0	0	2116
329	251	0	0	0	0	0	0	0	0	2120
330	197	0	0	0	0	0	0	0	0	2128
331	221	0	0	0	0	0	0	0	0	2136
332	228	0	0	0	0	0	0	0	0	2144
333	250	0	0	0	0	0	0	0	0	2152
334	203	0	0	0	0	0	0	0	0	2160
335	203	0	0	0	0	0	0	0	0	2168
336	197	0	0	0	0	0	0	0	0	2176
337	13	0	0	0	0	0	0	0	0	2184
338	212	0	0	0	0	0	0	0	0	2188
339	22	0	0	0	0	0	0	0	0	2196
340	197	0	0	0	0	0	0	0	0	2200
341	221	0	0	0	0	0	0	0	0	2208
342	134	0	0	0	0	0	0	0	0	2216
343	14	0	0	0	0	0	0	0	0	2220
344	228	0	0	0	0	0	0	0	0	2224
345	251	0	0	0	0	0	0	0	0	2232
346	197	0	0	0	0	0	0	0	0	2240
347	221	0	0	0	0	0	0	0	0	2248
348	14	0	0	0	0	0	0	0	0	2256
349	228	0	0	0	0	0	0	0	0	2260
350	250	0	0	0	0	0	0	0	0	2268
351	203	0	0	0	0	0	0	0	0	2276
352	202	0	0	0	0	0	0	0	0	2284
353	197	0	0	0	0	0	0	0	246	2292
354	221	235	244	156	20	173	84	0	0	2300
355	228	0	0	0	0	0	0	0	0	2308
356	250	0	0	0	0	0	0	0	0	2316
357	203	0	0	0	0	0	0	0	0	2324
358	195	0	0	231	0	0	0	0	0	2332
359	250	0	141	0	0	0	0	0	229	2340
360	195	0	0	0	0	0	0	0	0	2348
361	251	0	0	0	0	0	0	0	0	2356
362	203	0	0	0	0	0	0	0	0	2364
363	197	0	0	0	0	0	0	0	0	2372
364	13	0	0	0	0	0	119	46	10	2380
365	212	0	0	0	0	0	0	0	0	2384
366	22	0	0	29	213	253	0	0	0	2392
367	197	0	0	0	0	0	0	0	0	2396
368	221	0	0	0	0	0	0	0	0	2404
369	221	0	0	0	0	248	0	0	0	2412
370	134	0	0	0	0	0	0	0	0	2420
371	4	0	0	0	0	0	0	0	0	2424
372	251	0	0	0	0	0	0	0	0	2428
373	197	0	0	0	0	72	0	0	0	2436
374	221	0	0	0	0	0	0	0	0	2444
375	192	0	0	0	0	0	0	0	0	2452
376	228	0	0	0	0	0	0	0	0	2456
377	251	0	139	69	0	0	0	0	0	2464
378	203	0	0	0	0	0	0	0	0	2472
379	203	0	0	0	0	0	0	0	0	2480
380	197	0	0	0	0	0	0	0	0	2488
381	13	0	0	0	0	0	0	0	0	2496
382	212	0	0	0	0	0	0	0	0	2500
383	22	0	0	0	0	0	0	0	0	2508
384	197	0	0	0	0	0	0	0	0	2512
385	213	212	0	0	0	0	0	0	0	2520
386	250	0	0	0	0	0	0	0	0	2528
387	195	0	0	0	0	0	0	0	0	2536
388	250	0	0	0	0	0	0	0	0	2544
389	197	0	0	0	0	0	0	0	0	2552
390	13	0	0	0	0	0	0	0	0	2560
391	212	0	0	0	176	18	246	75	11	2564
392	22	0	0	0	0	0	0	0	0	2572
393	197	0	0	0	0	0	0	0	0	2576
394	213	0	0	0	0	0	0	0	0	2584
395	251	0	0	0	0	0	0	0	0	2592
396	197	0	83	103	158	0	0	0	0	2600
397	213	0	0	0	0	0	0	0	0	2608
398	250	0	0	0	0	0	0	0	0	2616
399	197	0	0	0	0	0	0	0	0	2624
400	213	0	0	0	66	241	0	0	0	2632
401	251	0	0	0	0	0	0	0	0	2640
402	197	0	0	0	0	0	0	0	0	2648
403	213	0	0	0	0	0	0	0	0	2656
404	251	0	0	0	0	0	0	0	0	2664
405	98	0	0	0	0	0	0	0	0	2672
406	205	0	0	0	0	0	0	0	0	2676
407	13	0	0	0	0	0	0	0	0	2684
408	5	0	0	0	0	0	0	0	0	2688
409	205	0	0	0	0	0	0	0	0	2692
410	12	0	0	0	0	0	0	0	0	2700
411	5	0	13	0	0	0	0	0	0	2704
412	21	0	0	0	0	0	0	0	0	2708
413	221	0	0	0	0	0	0	0	0	2712
414	249	0	0	0	0	0	0	0	0	2720
415	98	0	0	0	0	0	0	0	0	2728
416	163	0	0	0	0	0	0	0	0	2732
417	248	0	0	0	0	0	0	0	0	2740
418	98	0	0	0	0	203	217	0	0	2748
419	163	0	0	0	0	0	0	0	0	2752
420	248	0	0	60	0	0	0	0	0	2760
421	98	0	0	0	0	0	0	0	0	2768
422	163	0	0	0	0	0	0	0	0	2772
423	98	0	0	0	0	0	0	0	0	2780
424	249	0	0	0	0	0	0	0	0	2784
425	98	0	0	0	0	0	0	0	0	2792
426	163	0	0	0	0	0	227	180	101	2796
427	21	236	0	0	0	0	0	0	0	2804
428	221	0	0	0	0	0	0	0	123	2808
429	14	0	0	0	0	0	0	0	0	2816
430	249	0	0	0	0	0	0	0	0	2820
431	98	0	0	0	0	0	0	0	0	2828
432	163	0	0	0	0	0	0	0	0	2832
433	249	0	0	0	0	0	0	0	0	2840
434	98	0	0	0	0	0	0	0	0	2848
435	163	0	0	0	0	0	0	0	0	2852
436	248	0	0	0	0	0	0	0	0	2860
437	98	0	0	0	0	0	0	0	0	2868
438	163	0	0	0	0	0	0	0	0	2872
439	21	0	0	0	0	0	0	0	0	2880
440	221	0	0	0	0	0	0	0	0	2884
441	14	0	0	0	0	0	0	0	0	2892
442	248	0	0	0	0	0	0	0	0	2896
443	98	0	0	0	0	0	0	0	0	2904
444	163	0	0	0	0	0	0	0	0	2908
445	248	0	0	0	0	0	0	0	0	2916
446	98	0	0	0	0	0	0	0	0	2924
447	163	0	0	0	0	0	0	0	0	2928
448	249	0	0	0	0	0	0	0	0	2936
449	98	0	0	0	0	0	0	0	0	2944
450	163	0	0	0	0	0	124	0	0	2948
451	48	0	0	0	0	0	0	0	191	2956
452	98	0	0	0	0	0	0	0	184	2960
453	98	0	0	0	0	0	0	0	0	2964
454	98	0	123	169	0	0	0	0	0	2968
455	98	0	0	0	104	0	0	0	0	2972
456	249	0	0	0	75	0	0	0	0	2976
457	218	0	0	0	0	0	0	0	0	2984
458	234	0	0	0	0	0	0	0	0	2992
459	22	0	0	0	0	0	0	0	0	3000
460	248	0	0	0	0	0	0	0	0	3004
461	4	0	0	0	0	0	0	0	0	3012
462	6	0	0	0	0	0	0	0	0	3016
463	66	0	0	0	0	0	0	0	0	3020
464	11	0	0	0	0	0	0	0	0	3024
```

### Prototype 1

Instruction count: 4

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	18	0	0	0	0	0	0	0	0	0
2	22	1	0	0	0	0	0	0	0	4
3	5	1	1	1	0	0	0	0	0	8
4	11	0	1	0	0	0	0	0	0	12
```

### Prototype 2

Instruction count: 119

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	48	0	0	0	0	0	0	0	0	0
2	221	1	255	0	2	1	0	0	0	4
3	14	3	0	0	0	0	0	0	0	12
4	92	1	32	181	0	0	0	0	0	16
5	197	4	4	8	88	10	88	0	0	20
6	210	4	3	2	0	0	0	0	0	28
7	117	4	0	3	0	0	0	0	0	36
8	94	1	145	73	0	0	0	0	0	40
9	98	1	3	0	0	0	0	0	0	44
10	192	4	91	0	0	0	0	0	0	48
11	137	3	4	216	203	0	0	0	0	52
12	192	6	28	0	0	0	0	0	0	60
13	137	5	6	215	103	0	0	0	0	64
14	129	2	3	5	0	0	0	0	0	72
15	197	3	3	132	190	135	190	0	0	76
16	48	4	0	0	0	0	0	0	0	84
17	14	5	1	0	0	0	0	0	0	88
18	48	6	0	0	0	0	0	0	0	92
19	221	7	1	0	8	1	0	0	0	96
20	117	8	6	7	0	0	0	0	0	104
21	192	7	2	0	0	0	0	0	0	108
22	239	8	6	7	58	210	0	0	0	112
23	221	7	3	0	8	1	0	0	0	120
24	117	8	6	7	0	0	0	0	0	128
25	120	6	4	5	0	0	0	0	0	132
26	48	5	0	0	0	0	0	0	0	136
27	48	6	0	0	0	0	0	0	0	140
28	221	7	1	0	8	8	0	0	0	144
29	245	10	142	239	0	0	0	0	0	152
30	48	11	0	0	0	0	0	0	0	156
31	101	12	137	145	0	0	0	0	0	160
32	222	12	221	0	13	4	0	0	0	164
33	5	10	3	2	0	0	0	0	0	172
34	215	9	10	10	9	0	0	0	0	176
35	66	0	0	0	0	0	0	0	0	184
36	11	10	2	0	0	0	0	0	0	188
37	221	2	0	0	3	1	0	0	0	192
38	221	4	7	0	5	1	0	0	0	200
39	14	6	0	0	0	0	0	0	0	208
40	92	4	47	181	0	0	0	0	0	212
41	139	7	0	67	140	0	0	0	0	216
42	139	8	1	54	125	0	0	0	0	224
43	67	7	69	179	8	0	0	0	0	232
44	128	2	2	3	0	0	0	0	0	240
45	7	244	178	0	0	0	0	0	0	244
46	129	9	0	7	0	0	0	0	0	248
47	138	0	9	53	73	0	0	0	0	252
48	129	9	1	8	0	0	0	0	0	260
49	138	1	9	197	123	0	0	0	0	264
50	143	3	3	2	0	0	0	0	0	272
51	94	4	23	71	0	0	0	0	0	280
52	22	4	2	0	0	0	0	0	0	284
53	11	4	2	0	0	0	0	0	0	288
54	255	3	0	0	0	0	0	0	0	292
55	115	2	3	1	0	0	0	0	0	296
56	18	4	0	0	0	0	0	0	0	300
57	68	2	17	178	4	0	0	0	0	304
58	254	6	0	0	0	0	0	0	0	312
59	115	5	6	1	0	0	0	0	0	316
60	10	5	2	0	0	0	0	0	0	320
61	254	3	1	0	0	0	0	0	0	324
62	116	2	3	1	0	0	0	0	0	328
63	18	3	0	0	0	0	0	0	0	332
64	77	2	123	180	3	0	0	0	0	336
65	18	4	0	0	0	0	0	0	0	344
66	10	4	2	0	0	0	0	0	0	348
67	57	3	2	0	0	0	0	0	0	352
68	56	4	2	1	0	0	0	0	0	356
69	12	5	252	37	0	0	0	0	0	360
70	22	6	4	0	0	0	0	0	0	364
71	123	6	6	0	0	0	0	0	0	368
72	221	7	1	0	8	1	0	0	0	372
73	93	6	77	186	0	0	0	0	0	380
74	22	9	5	0	0	0	0	0	0	384
75	254	11	2	0	0	0	0	0	0	388
76	255	12	3	0	0	0	0	0	0	392
77	255	13	4	0	0	0	0	0	0	396
78	214	13	4	8	2	0	0	0	0	400
79	254	18	5	0	0	0	0	0	0	408
80	137	19	3	233	209	0	0	0	0	412
81	128	17	18	19	0	0	0	0	0	420
82	128	16	17	8	0	0	0	0	0	424
83	139	14	16	63	22	0	0	0	0	428
84	4	12	3	2	0	0	0	0	0	436
85	116	10	11	12	0	0	0	0	0	440
86	215	20	9	21	10	0	0	0	0	444
87	149	9	20	21	0	0	0	0	0	452
88	165	5	9	6	213	59	0	0	0	456
89	57	6	2	2	0	0	0	0	0	464
90	8	6	165	187	0	0	0	0	0	468
91	22	7	5	0	0	0	0	0	0	472
92	10	7	2	0	0	0	0	0	0	476
93	254	6	6	0	0	0	0	0	0	480
94	192	7	0	0	0	0	0	0	0	484
95	90	7	133	189	6	0	0	0	0	488
96	254	9	7	0	0	0	0	0	0	496
97	255	10	6	0	0	0	0	0	0	500
98	115	8	9	10	0	0	0	0	0	504
99	9	8	124	190	0	0	0	0	0	508
100	254	11	0	0	0	0	0	0	0	512
101	254	13	7	0	0	0	0	0	0	516
102	255	14	8	0	0	0	0	0	0	520
103	115	12	13	14	0	0	0	0	0	524
104	18	15	0	0	0	0	0	0	0	528
105	120	15	11	12	0	0	0	0	0	532
106	7	128	191	0	0	0	0	0	0	536
107	255	6	0	0	0	0	0	0	0	540
108	117	5	6	1	0	0	0	0	0	544
109	255	6	7	0	0	0	0	0	0	548
110	254	7	8	0	0	0	0	0	0	552
111	120	1	6	7	0	0	0	0	0	556
112	254	8	8	0	0	0	0	0	0	560
113	254	9	6	0	0	0	0	0	0	564
114	132	7	8	9	0	0	0	0	0	568
115	135	6	7	223	152	0	0	0	0	572
116	1	6	8	0	0	0	0	0	0	580
117	7	163	194	0	0	0	0	0	0	584
118	22	6	5	0	0	0	0	0	0	588
119	11	6	2	0	0	0	0	0	0	592
```

### Prototype 3

Instruction count: 17

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	221	2	0	0	3	1	0	0	0	0
2	221	4	7	0	5	1	0	0	0	8
3	14	6	0	0	0	0	0	0	0	16
4	92	4	47	181	0	0	0	0	0	20
5	139	7	0	247	168	0	0	0	0	24
6	139	8	1	234	153	0	0	0	0	32
7	67	7	69	179	8	0	0	0	0	40
8	128	2	2	3	0	0	0	0	0	48
9	7	244	178	0	0	0	0	0	0	52
10	129	9	0	7	0	0	0	0	0	56
11	138	0	9	21	197	0	0	0	0	60
12	129	9	1	8	0	0	0	0	0	68
13	138	1	9	165	247	0	0	0	0	72
14	143	3	3	2	0	0	0	0	0	80
15	94	4	23	71	0	0	0	0	0	88
16	22	4	2	0	0	0	0	0	0	92
17	11	4	2	0	0	0	0	0	0	96
```

### Prototype 4

Instruction count: 66

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	255	3	0	0	0	0	0	0	0	0
2	115	2	3	1	0	0	0	0	0	4
3	18	4	0	0	0	0	0	0	0	8
4	68	2	17	178	4	0	0	0	0	12
5	254	6	0	0	0	0	0	0	0	20
6	115	5	6	1	0	0	0	0	0	24
7	10	5	2	0	0	0	0	0	0	28
8	254	3	1	0	0	0	0	0	0	32
9	116	2	3	1	0	0	0	0	0	36
10	18	3	0	0	0	0	0	0	0	40
11	77	2	123	180	3	0	0	0	0	44
12	18	4	0	0	0	0	0	0	0	52
13	10	4	2	0	0	0	0	0	0	56
14	57	3	2	0	0	0	0	0	0	60
15	56	4	2	1	0	0	0	0	0	64
16	12	5	99	99	0	0	0	0	0	68
17	22	6	4	0	0	0	0	0	0	72
18	123	6	6	0	0	0	0	0	0	76
19	221	7	1	0	8	1	0	0	0	80
20	93	6	77	186	0	0	0	0	0	88
21	22	9	5	0	0	0	0	0	0	92
22	254	11	2	0	0	0	0	0	0	96
23	255	12	3	0	0	0	0	0	0	100
24	255	13	4	0	0	0	0	0	0	104
25	214	13	4	8	2	0	0	0	0	108
26	254	18	5	0	0	0	0	0	0	116
27	137	19	3	29	171	0	0	0	0	120
28	128	17	18	19	0	0	0	0	0	128
29	128	16	17	8	0	0	0	0	0	132
30	139	14	16	16	49	0	0	0	0	136
31	4	12	3	2	0	0	0	0	0	144
32	116	10	11	12	0	0	0	0	0	148
33	215	20	9	21	10	0	0	0	0	152
34	149	9	20	21	0	0	0	0	0	160
35	165	5	9	6	213	59	0	0	0	164
36	57	6	2	2	0	0	0	0	0	172
37	8	6	165	187	0	0	0	0	0	176
38	22	7	5	0	0	0	0	0	0	180
39	10	7	2	0	0	0	0	0	0	184
40	254	6	6	0	0	0	0	0	0	188
41	192	7	0	0	0	0	0	0	0	192
42	90	7	133	189	6	0	0	0	0	196
43	254	9	7	0	0	0	0	0	0	204
44	255	10	6	0	0	0	0	0	0	208
45	115	8	9	10	0	0	0	0	0	212
46	9	8	124	190	0	0	0	0	0	216
47	254	11	0	0	0	0	0	0	0	220
48	254	13	7	0	0	0	0	0	0	224
49	255	14	8	0	0	0	0	0	0	228
50	115	12	13	14	0	0	0	0	0	232
51	18	15	0	0	0	0	0	0	0	236
52	120	15	11	12	0	0	0	0	0	240
53	7	128	191	0	0	0	0	0	0	244
54	255	6	0	0	0	0	0	0	0	248
55	117	5	6	1	0	0	0	0	0	252
56	255	6	7	0	0	0	0	0	0	256
57	254	7	8	0	0	0	0	0	0	260
58	120	1	6	7	0	0	0	0	0	264
59	254	8	8	0	0	0	0	0	0	268
60	254	9	6	0	0	0	0	0	0	272
61	132	7	8	9	0	0	0	0	0	276
62	135	6	7	86	17	0	0	0	0	280
63	1	6	8	0	0	0	0	0	0	288
64	7	163	194	0	0	0	0	0	0	292
65	22	6	5	0	0	0	0	0	0	296
66	11	6	2	0	0	0	0	0	0	300
```

### Prototype 5

Instruction count: 44

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	192	0	20	0	0	0	0	0	0	0
2	254	1	0	0	0	0	0	0	0	4
3	74	1	129	177	0	0	0	0	0	8
4	18	2	0	0	0	0	0	0	0	12
5	11	2	2	0	0	0	0	0	0	16
6	18	1	0	0	0	0	0	0	0	20
7	245	2	117	77	0	0	0	0	0	24
8	244	7	32	97	0	0	0	0	0	28
9	219	3	7	0	221	207	0	0	0	32
10	5	2	0	4	0	0	0	0	0	40
11	126	2	78	184	0	0	0	0	0	44
12	220	8	6	2	123	213	122	213	0	48
13	9	8	255	180	0	0	0	0	0	56
14	220	8	6	2	55	120	60	121	0	60
15	8	8	149	181	0	0	0	0	0	68
16	254	11	1	0	0	0	0	0	0	72
17	68	6	30	182	11	0	0	0	0	76
18	216	229	196	8	1	0	0	0	0	84
19	216	54	197	8	0	0	0	0	0	92
20	9	8	162	182	0	0	0	0	0	100
21	244	14	34	87	0	0	0	0	0	104
22	98	15	6	0	0	0	0	0	0	108
23	4	14	2	3	0	0	0	0	0	112
24	215	12	14	13	15	0	0	0	0	116
25	236	14	12	4	0	0	0	0	0	124
26	22	14	13	0	0	0	0	0	0	132
27	8	14	67	185	0	0	0	0	0	136
28	104	13	73	186	0	0	0	0	0	140
29	216	24	200	14	1	0	0	0	0	148
30	216	89	200	14	0	0	0	0	0	156
31	9	14	115	186	0	0	0	0	0	164
32	215	0	13	1	6	0	0	0	0	168
33	7	196	185	0	0	0	0	0	0	176
34	6	17	186	0	0	0	0	0	0	180
35	7	94	186	0	0	0	0	0	0	184
36	66	6	0	0	0	0	0	0	0	188
37	95	2	132	65	2	0	0	0	0	192
38	22	2	1	0	0	0	0	0	0	200
39	10	2	2	0	0	0	0	0	0	204
40	198	2	0	3	246	182	0	0	0	208
41	196	4	1	4	17	183	9	182	0	216
42	129	1	2	4	0	0	0	0	0	224
43	249	0	1	219	252	0	0	0	0	228
44	11	0	2	0	0	0	0	0	0	236
```

### Prototype 6

Instruction count: 5

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	198	2	0	3	208	216	0	0	0	0
2	196	4	1	4	110	105	118	104	0	8
3	129	1	2	4	0	0	0	0	0	16
4	249	0	1	222	50	0	0	0	0	20
5	11	0	2	0	0	0	0	0	0	28
```

### Prototype 7

Instruction count: 69

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	245	0	50	219	0	0	0	0	0	0
2	98	1	8	0	0	0	0	0	0	4
3	4	0	2	1	0	0	0	0	0	8
4	244	0	214	20	0	0	0	0	0	12
5	98	1	9	0	0	0	0	0	0	16
6	4	0	2	1	0	0	0	0	0	20
7	11	0	1	0	0	0	0	0	0	24
8	48	0	0	0	0	0	0	0	0	28
9	192	1	1	0	0	0	0	0	0	32
10	101	2	91	77	0	0	0	0	0	36
11	195	3	56	72	61	73	60	73	0	40
12	250	2	60	101	3	0	0	0	0	48
13	244	4	235	191	0	0	0	0	0	56
14	194	4	3	4	80	7	83	7	0	60
15	251	2	146	137	3	0	0	0	0	68
16	202	2	34	195	3	33	195	0	0	76
17	117	2	0	1	0	0	0	0	0	84
18	254	1	0	0	0	0	0	0	0	88
19	9	1	59	180	0	0	0	0	0	92
20	255	2	0	0	0	0	0	0	0	96
21	206	1	2	99	14	113	15	0	0	100
22	8	1	54	181	0	0	0	0	0	108
23	198	5	0	6	165	165	0	0	0	112
24	244	6	61	144	0	0	0	0	0	120
25	210	6	0	0	0	0	0	0	0	124
26	3	4	5	128	101	0	0	0	0	132
27	4	4	0	1	0	0	0	0	0	140
28	7	96	182	0	0	0	0	0	0	144
29	10	0	1	0	0	0	0	0	0	148
30	18	0	0	0	0	0	0	0	0	152
31	255	1	0	0	0	0	0	0	0	156
32	9	1	210	177	0	0	0	0	0	160
33	244	2	189	59	0	0	0	0	0	164
34	254	7	0	0	0	0	0	0	0	168
35	219	3	7	0	195	125	0	0	0	172
36	4	2	0	4	0	0	0	0	0	180
37	126	2	79	184	0	0	0	0	0	184
38	248	9	6	154	62	0	0	0	0	188
39	243	9	10	8	0	190	5	0	0	196
40	216	234	194	8	1	0	0	0	0	204
41	21	8	0	0	0	0	0	0	0	212
42	8	8	215	180	0	0	0	0	0	216
43	248	11	6	215	253	0	0	0	0	220
44	243	11	12	8	0	154	238	0	0	228
45	216	83	196	8	1	0	0	0	0	236
46	216	164	196	8	0	0	0	0	0	244
47	8	8	108	182	0	0	0	0	0	252
48	22	0	6	0	0	0	0	0	0	256
49	7	7	182	0	0	0	0	0	0	260
50	42	2	240	69	2	0	0	0	0	264
51	6	173	182	0	0	0	0	0	0	272
52	7	242	182	0	0	0	0	0	0	276
53	48	1	0	0	0	0	0	0	0	280
54	192	2	1	0	0	0	0	0	0	284
55	223	3	3	228	50	229	56	229	0	288
56	250	3	107	117	0	0	0	0	0	296
57	120	3	1	2	0	0	0	0	0	304
58	255	2	0	0	0	0	0	0	0	308
59	9	2	102	185	0	0	0	0	0	312
60	254	3	0	0	0	0	0	0	0	316
61	206	2	2	83	14	65	15	0	0	320
62	9	2	97	186	0	0	0	0	0	328
63	198	6	0	7	245	117	0	0	0	332
64	244	7	93	136	0	0	0	0	0	340
65	210	7	1	0	0	0	0	0	0	344
66	3	5	6	64	221	0	0	0	0	352
67	5	5	0	1	0	0	0	0	0	360
68	6	130	187	0	0	0	0	0	0	364
69	11	0	1	0	0	0	0	0	0	368
```

### Prototype 8

Instruction count: 22

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	48	0	0	0	0	0	0	0	0	0
2	192	1	1	0	0	0	0	0	0	4
3	101	2	246	225	0	0	0	0	0	8
4	195	3	120	135	125	134	124	134	0	12
5	250	2	236	17	3	0	0	0	0	20
6	244	4	199	58	0	0	0	0	0	28
7	194	4	3	4	150	121	149	121	0	32
8	251	2	98	53	3	0	0	0	0	40
9	202	2	239	118	3	236	118	0	0	48
10	117	2	0	1	0	0	0	0	0	56
11	254	1	0	0	0	0	0	0	0	60
12	9	1	59	180	0	0	0	0	0	64
13	255	2	0	0	0	0	0	0	0	68
14	206	1	2	129	174	147	175	0	0	72
15	8	1	54	181	0	0	0	0	0	80
16	198	5	0	6	71	7	0	0	0	84
17	244	6	9	11	0	0	0	0	0	92
18	210	6	0	0	0	0	0	0	0	96
19	3	4	5	184	78	0	0	0	0	104
20	4	4	0	1	0	0	0	0	0	112
21	7	96	182	0	0	0	0	0	0	116
22	10	0	1	0	0	0	0	0	0	120
```

### Prototype 9

Instruction count: 40

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	18	0	0	0	0	0	0	0	0	0
2	255	1	0	0	0	0	0	0	0	4
3	9	1	210	177	0	0	0	0	0	8
4	244	2	217	20	0	0	0	0	0	12
5	254	7	0	0	0	0	0	0	0	16
6	219	3	7	0	248	116	0	0	0	20
7	4	2	0	4	0	0	0	0	0	28
8	126	2	79	184	0	0	0	0	0	32
9	248	9	6	3	240	0	0	0	0	36
10	243	9	10	8	0	125	176	0	0	44
11	216	234	194	8	1	0	0	0	0	52
12	21	8	0	0	0	0	0	0	0	60
13	8	8	215	180	0	0	0	0	0	64
14	248	11	6	80	175	0	0	0	0	68
15	243	11	12	8	0	71	157	0	0	76
16	216	83	196	8	1	0	0	0	0	84
17	216	164	196	8	0	0	0	0	0	92
18	8	8	108	182	0	0	0	0	0	100
19	22	0	6	0	0	0	0	0	0	104
20	7	7	182	0	0	0	0	0	0	108
21	42	2	240	69	2	0	0	0	0	112
22	6	173	182	0	0	0	0	0	0	120
23	7	242	182	0	0	0	0	0	0	124
24	48	1	0	0	0	0	0	0	0	128
25	192	2	1	0	0	0	0	0	0	132
26	223	3	52	13	5	12	15	12	0	136
27	250	3	219	25	0	0	0	0	0	144
28	120	3	1	2	0	0	0	0	0	152
29	255	2	0	0	0	0	0	0	0	156
30	9	2	102	185	0	0	0	0	0	160
31	254	3	0	0	0	0	0	0	0	164
32	206	2	2	61	238	47	239	0	0	168
33	9	2	97	186	0	0	0	0	0	176
34	198	6	0	7	195	11	0	0	0	180
35	244	7	49	97	0	0	0	0	0	188
36	210	7	1	0	0	0	0	0	0	192
37	3	5	6	8	132	0	0	0	0	200
38	5	5	0	1	0	0	0	0	0	208
39	6	130	187	0	0	0	0	0	0	212
40	11	0	1	0	0	0	0	0	0	216
```

### Prototype 10

Instruction count: 279

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	255	0	0	0	0	0	0	0	0	0
2	121	0	0	0	0	0	0	0	0	4
3	73	0	112	177	0	0	0	0	0	8
4	254	0	1	0	0	0	0	0	0	12
5	121	0	0	0	0	0	0	0	0	16
6	73	0	91	178	0	0	0	0	0	20
7	254	0	2	0	0	0	0	0	0	24
8	121	0	0	0	0	0	0	0	0	28
9	8	0	79	179	0	0	0	0	0	32
10	11	0	1	0	0	0	0	0	0	36
11	233	0	3	1	2	0	0	0	0	40
12	22	1	0	0	0	0	0	0	0	48
13	74	1	103	180	0	0	0	0	0	52
14	11	0	1	0	0	0	0	0	0	56
15	220	2	0	2	217	74	210	75	0	60
16	215	1	2	2	1	0	0	0	0	68
17	74	2	156	181	0	0	0	0	0	76
18	11	0	1	0	0	0	0	0	0	80
19	48	2	0	0	0	0	0	0	0	84
20	244	3	150	68	0	0	0	0	0	88
21	98	4	11	0	0	0	0	0	0	92
22	4	3	2	1	0	0	0	0	0	96
23	18	3	0	0	0	0	0	0	0	100
24	98	4	12	0	0	0	0	0	0	104
25	254	5	1	0	0	0	0	0	0	108
26	121	5	5	0	0	0	0	0	0	112
27	74	5	173	184	0	0	0	0	0	116
28	254	5	2	0	0	0	0	0	0	120
29	121	5	5	0	0	0	0	0	0	124
30	74	5	136	185	0	0	0	0	0	128
31	255	5	0	0	0	0	0	0	0	132
32	121	5	5	0	0	0	0	0	0	136
33	8	5	112	186	0	0	0	0	0	140
34	66	2	0	0	0	0	0	0	0	144
35	10	0	1	0	0	0	0	0	0	148
36	244	5	86	116	0	0	0	0	0	152
37	98	6	15	0	0	0	0	0	0	156
38	4	5	2	1	0	0	0	0	0	160
39	245	5	245	173	0	0	0	0	0	164
40	254	10	0	0	0	0	0	0	0	168
41	219	6	10	0	61	47	0	0	0	172
42	4	5	0	4	0	0	0	0	0	180
43	126	5	201	194	0	0	0	0	0	184
44	248	11	9	200	34	0	0	0	0	188
45	243	11	13	8	0	120	31	0	0	196
46	216	237	204	12	1	0	0	0	0	204
47	21	12	0	0	0	0	0	0	0	212
48	73	12	1	191	0	0	0	0	0	216
49	243	11	14	8	0	232	219	0	0	220
50	216	5	206	12	1	0	0	0	0	228
51	216	86	206	12	0	0	0	0	0	236
52	74	12	37	192	0	0	0	0	0	244
53	243	11	15	8	0	109	151	0	0	248
54	216	57	207	12	1	0	0	0	0	256
55	216	122	207	12	0	0	0	0	0	264
56	74	12	121	193	0	0	0	0	0	272
57	243	11	16	8	0	230	83	0	0	276
58	216	93	208	12	1	0	0	0	0	284
59	216	158	208	12	0	0	0	0	0	292
60	74	12	157	194	0	0	0	0	0	300
61	243	11	17	8	0	99	15	0	0	304
62	216	113	209	12	1	0	0	0	0	312
63	216	194	209	12	0	0	0	0	0	320
64	74	12	177	195	0	0	0	0	0	328
65	243	11	18	8	0	220	203	0	0	332
66	216	149	210	12	1	0	0	0	0	340
67	216	230	210	12	0	0	0	0	0	348
68	73	12	213	196	0	0	0	0	0	356
69	243	11	19	8	0	89	135	0	0	360
70	216	201	211	12	1	0	0	0	0	368
71	216	10	212	12	0	0	0	0	0	376
72	73	12	233	197	0	0	0	0	0	384
73	243	11	20	8	0	170	67	0	0	388
74	216	237	212	12	1	0	0	0	0	396
75	216	46	213	12	0	0	0	0	0	404
76	8	12	34	199	0	0	0	0	0	412
77	245	21	194	127	0	0	0	0	0	416
78	98	22	16	0	0	0	0	0	0	420
79	4	21	2	1	0	0	0	0	0	424
80	7	51	199	0	0	0	0	0	0	428
81	66	9	0	0	0	0	0	0	0	432
82	42	5	244	52	2	0	0	0	0	436
83	198	5	4	6	159	93	0	0	0	444
84	22	8	5	0	0	0	0	0	0	452
85	98	9	17	0	0	0	0	0	0	456
86	163	7	8	3	2	96	0	0	0	460
87	22	3	7	0	0	0	0	0	0	468
88	233	5	5	1	1	0	0	0	0	472
89	197	5	5	219	229	218	229	0	0	480
90	15	6	147	172	0	0	0	0	0	488
91	4	5	2	1	0	0	0	0	0	492
92	244	5	246	156	0	0	0	0	0	496
93	98	6	20	0	0	0	0	0	0	500
94	5	5	2	1	0	0	0	0	0	504
95	254	5	2	0	0	0	0	0	0	508
96	9	5	43	204	0	0	0	0	0	512
97	254	6	2	0	0	0	0	0	0	516
98	198	8	2	9	52	139	0	0	0	520
99	197	10	10	97	75	96	75	0	0	528
100	197	11	11	245	32	244	32	0	0	536
101	14	12	60	0	0	0	0	0	0	544
102	124	22	12	0	0	0	0	0	0	548
103	4	11	2	2	0	0	0	0	0	552
104	192	12	0	0	0	0	0	0	0	556
105	228	10	4	2	0	0	0	0	0	560
106	130	7	8	10	0	0	0	0	0	568
107	251	6	166	217	7	0	0	0	0	572
108	7	47	207	0	0	0	0	0	0	580
109	198	5	6	6	214	240	0	0	0	584
110	245	6	206	242	0	0	0	0	0	592
111	98	7	21	0	0	0	0	0	0	596
112	5	6	2	1	0	0	0	0	0	600
113	197	6	6	171	13	170	13	0	0	604
114	210	6	5	1	0	0	0	0	0	612
115	244	6	138	81	0	0	0	0	0	620
116	98	7	22	0	0	0	0	0	0	624
117	5	6	2	1	0	0	0	0	0	628
118	22	6	4	0	0	0	0	0	0	632
119	5	6	1	1	0	0	0	0	0	636
120	66	1	0	0	0	0	0	0	0	640
121	10	0	1	0	0	0	0	0	0	644
122	255	0	0	0	0	0	0	0	0	648
123	198	1	1	2	70	45	0	0	0	652
124	250	0	90	165	1	0	0	0	0	660
125	255	0	0	0	0	0	0	0	0	668
126	198	1	1	2	177	3	0	0	0	672
127	250	0	235	201	1	0	0	0	0	680
128	255	0	0	0	0	0	0	0	0	688
129	198	1	1	2	168	217	0	0	0	692
130	250	0	120	237	1	0	0	0	0	700
131	255	0	0	0	0	0	0	0	0	708
132	198	1	1	2	135	175	0	0	0	712
133	251	0	137	17	1	0	0	0	0	720
134	10	0	1	0	0	0	0	0	0	728
135	255	0	0	0	0	0	0	0	0	732
136	9	0	68	177	0	0	0	0	0	736
137	198	0	0	1	30	105	0	0	0	740
138	8	0	206	177	0	0	0	0	0	748
139	245	2	170	25	0	0	0	0	0	752
140	98	3	13	0	0	0	0	0	0	756
141	5	2	2	1	0	0	0	0	0	760
142	7	171	178	0	0	0	0	0	0	764
143	245	0	218	101	0	0	0	0	0	768
144	98	1	14	0	0	0	0	0	0	772
145	5	0	2	1	0	0	0	0	0	776
146	11	0	1	0	0	0	0	0	0	780
147	254	1	0	0	0	0	0	0	0	784
148	163	0	1	2	1	76	1	0	0	788
149	11	0	1	0	0	0	0	0	0	796
150	254	0	0	0	0	0	0	0	0	800
151	9	0	56	177	0	0	0	0	0	804
152	254	1	0	0	0	0	0	0	0	808
153	198	2	1	3	122	137	0	0	0	812
154	224	6	74	108	0	0	0	0	0	820
155	151	2	2	6	0	0	0	0	0	824
156	250	1	90	37	2	0	0	0	0	828
157	255	0	0	0	0	0	0	0	0	836
158	198	1	1	2	241	67	0	0	0	840
159	15	6	200	107	0	0	0	0	0	848
160	151	1	1	6	0	0	0	0	0	852
161	250	0	75	97	1	0	0	0	0	856
162	254	0	0	0	0	0	0	0	0	864
163	198	1	1	2	116	253	0	0	0	868
164	21	6	0	0	0	0	0	0	0	876
165	151	1	1	6	0	0	0	0	0	880
166	251	0	184	157	1	0	0	0	0	884
167	255	0	0	0	0	0	0	0	0	892
168	198	1	1	2	143	183	0	0	0	896
169	21	6	1	0	0	0	0	0	0	904
170	151	1	1	6	0	0	0	0	0	908
171	251	0	169	217	1	0	0	0	0	912
172	6	242	182	0	0	0	0	0	0	920
173	254	0	2	0	0	0	0	0	0	924
174	9	0	151	183	0	0	0	0	0	928
175	254	1	2	0	0	0	0	0	0	932
176	197	2	2	138	244	254	245	0	0	936
177	221	3	0	0	4	0	0	0	0	944
178	228	2	4	2	0	0	0	0	0	952
179	251	1	48	57	2	0	0	0	0	960
180	255	0	2	0	0	0	0	0	0	968
181	197	1	1	240	41	132	40	0	0	972
182	221	2	0	0	3	0	0	0	0	980
183	228	1	4	2	0	0	0	0	0	988
184	251	0	1	117	1	0	0	0	0	996
185	6	167	186	0	0	0	0	0	0	1004
186	11	0	1	0	0	0	0	0	0	1008
187	254	0	0	0	0	0	0	0	0	1012
188	203	0	25	162	1	0	0	0	0	1016
189	254	0	0	0	0	0	0	0	0	1024
190	203	0	60	170	1	0	0	0	0	1028
191	255	0	0	0	0	0	0	0	0	1036
192	204	0	96	237	1	1	0	0	0	1040
193	255	0	0	0	0	0	0	0	0	1048
194	204	0	37	145	1	0	0	0	0	1052
195	255	0	1	0	0	0	0	0	0	1060
196	197	1	1	162	192	214	193	0	0	1064
197	221	2	0	0	3	0	0	0	0	1072
198	228	1	4	2	0	0	0	0	0	1080
199	250	0	112	41	1	0	0	0	0	1088
200	254	0	1	0	0	0	0	0	0	1096
201	197	1	1	232	245	156	244	0	0	1100
202	221	2	0	0	3	0	0	0	0	1108
203	228	1	4	2	0	0	0	0	0	1116
204	250	0	65	101	1	0	0	0	0	1124
205	11	0	1	0	0	0	0	0	0	1132
206	254	1	0	0	0	0	0	0	0	1136
207	163	0	1	2	1	35	0	0	0	1140
208	10	0	1	0	0	0	0	0	0	1148
209	255	0	0	0	0	0	0	0	0	1152
210	8	0	92	177	0	0	0	0	0	1156
211	244	1	10	113	0	0	0	0	0	1160
212	98	2	18	0	0	0	0	0	0	1164
213	5	1	2	1	0	0	0	0	0	1168
214	7	25	178	0	0	0	0	0	0	1172
215	254	0	1	0	0	0	0	0	0	1176
216	9	0	10	179	0	0	0	0	0	1180
217	198	0	1	1	250	9	0	0	0	1184
218	9	0	132	179	0	0	0	0	0	1192
219	245	2	106	9	0	0	0	0	0	1196
220	98	3	19	0	0	0	0	0	0	1200
221	4	2	2	1	0	0	0	0	0	1204
222	6	97	180	0	0	0	0	0	0	1208
223	11	0	1	0	0	0	0	0	0	1212
224	255	0	0	0	0	0	0	0	0	1216
225	197	1	1	88	29	44	28	0	0	1220
226	221	2	0	0	3	0	0	0	0	1228
227	228	1	4	2	0	0	0	0	0	1236
228	250	0	192	133	1	0	0	0	0	1244
229	254	0	0	0	0	0	0	0	0	1252
230	197	1	1	158	78	234	79	0	0	1256
231	221	2	0	0	3	0	0	0	0	1264
232	228	1	4	2	0	0	0	0	0	1272
233	251	0	209	193	1	0	0	0	0	1280
234	11	0	1	0	0	0	0	0	0	1288
235	254	0	0	0	0	0	0	0	0	1292
236	203	0	249	98	1	0	0	0	0	1296
237	11	0	1	0	0	0	0	0	0	1304
238	254	1	0	0	0	0	0	0	0	1308
239	195	2	56	68	69	69	68	69	0	1312
240	163	0	1	3	1	86	1	0	0	1320
241	11	0	1	0	0	0	0	0	0	1328
242	198	1	0	2	98	170	0	0	0	1332
243	196	4	0	4	161	75	178	75	0	1340
244	137	3	4	117	201	0	0	0	0	1348
245	129	0	1	3	0	0	0	0	0	1356
246	197	2	2	235	190	138	191	0	0	1360
247	197	3	3	108	151	24	150	0	0	1368
248	248	4	0	1	106	0	0	0	0	1376
249	248	7	0	63	144	0	0	0	0	1384
250	198	8	1	9	222	58	0	0	0	1392
251	128	5	7	8	0	0	0	0	0	1400
252	249	6	0	215	2	0	0	0	0	1404
253	4	3	4	0	0	0	0	0	0	1412
254	4	2	0	2	0	0	0	0	0	1416
255	197	10	10	233	79	232	79	0	0	1420
256	197	11	11	125	36	124	36	0	0	1428
257	192	12	60	0	0	0	0	0	0	1436
258	124	22	12	0	0	0	0	0	0	1440
259	5	11	2	2	0	0	0	0	0	1444
260	14	12	0	0	0	0	0	0	0	1448
261	228	10	4	2	0	0	0	0	0	1452
262	130	1	2	10	0	0	0	0	0	1460
263	255	4	2	0	0	0	0	0	0	1464
264	254	5	3	0	0	0	0	0	0	1468
265	197	6	6	98	181	28	180	0	0	1472
266	254	7	4	0	0	0	0	0	0	1480
267	195	8	56	72	77	73	76	73	0	1484
268	195	9	120	63	15	62	14	62	0	1492
269	4	6	4	2	0	0	0	0	0	1500
270	101	7	33	29	0	0	0	0	0	1504
271	250	7	230	137	1	0	0	0	0	1508
272	2	3	4	164	71	0	0	0	0	1516
273	5	3	5	2	0	0	0	0	0	1524
274	163	2	3	2	1	97	1	0	0	1528
275	11	0	1	0	0	0	0	0	0	1536
276	255	1	0	0	0	0	0	0	0	1540
277	195	2	184	238	197	239	243	239	0	1544
278	163	0	1	3	1	86	1	0	0	1552
279	11	0	1	0	0	0	0	0	0	1560
```

### Prototype 11

Instruction count: 13

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	255	0	0	0	0	0	0	0	0	0
2	198	1	1	2	120	203	0	0	0	4
3	250	0	42	249	1	0	0	0	0	12
4	255	0	0	0	0	0	0	0	0	20
5	198	1	1	2	83	161	0	0	0	24
6	250	0	187	29	1	0	0	0	0	32
7	255	0	0	0	0	0	0	0	0	40
8	198	1	1	2	78	119	0	0	0	44
9	250	0	200	65	1	0	0	0	0	52
10	255	0	0	0	0	0	0	0	0	60
11	198	1	1	2	165	77	0	0	0	64
12	251	0	89	101	1	0	0	0	0	72
13	10	0	1	0	0	0	0	0	0	80
```

### Prototype 12

Instruction count: 52

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	255	0	0	0	0	0	0	0	0	0
2	9	0	68	177	0	0	0	0	0	4
3	198	0	0	1	50	189	0	0	0	8
4	8	0	206	177	0	0	0	0	0	16
5	245	2	98	39	0	0	0	0	0	20
6	98	3	13	0	0	0	0	0	0	24
7	5	2	2	1	0	0	0	0	0	28
8	7	171	178	0	0	0	0	0	0	32
9	245	0	146	115	0	0	0	0	0	36
10	98	1	14	0	0	0	0	0	0	40
11	5	0	2	1	0	0	0	0	0	44
12	11	0	1	0	0	0	0	0	0	48
13	254	1	0	0	0	0	0	0	0	52
14	163	0	1	2	1	76	1	0	0	56
15	11	0	1	0	0	0	0	0	0	64
16	254	0	0	0	0	0	0	0	0	68
17	9	0	56	177	0	0	0	0	0	72
18	254	1	0	0	0	0	0	0	0	76
19	198	2	1	3	22	221	0	0	0	80
20	224	6	184	186	0	0	0	0	0	88
21	151	2	2	6	0	0	0	0	0	92
22	250	1	186	221	2	0	0	0	0	96
23	255	0	0	0	0	0	0	0	0	104
24	198	1	1	2	173	151	0	0	0	108
25	15	6	54	185	0	0	0	0	0	116
26	151	1	1	6	0	0	0	0	0	120
27	250	0	171	25	1	0	0	0	0	124
28	254	0	0	0	0	0	0	0	0	132
29	198	1	1	2	32	81	0	0	0	136
30	21	6	0	0	0	0	0	0	0	144
31	151	1	1	6	0	0	0	0	0	148
32	251	0	152	85	1	0	0	0	0	152
33	255	0	0	0	0	0	0	0	0	160
34	198	1	1	2	187	11	0	0	0	164
35	21	6	1	0	0	0	0	0	0	172
36	151	1	1	6	0	0	0	0	0	176
37	251	0	137	145	1	0	0	0	0	180
38	6	242	182	0	0	0	0	0	0	188
39	254	0	2	0	0	0	0	0	0	192
40	9	0	151	183	0	0	0	0	0	196
41	254	1	2	0	0	0	0	0	0	200
42	197	2	2	214	106	162	107	0	0	204
43	221	3	0	0	4	0	0	0	0	212
44	228	2	4	2	0	0	0	0	0	220
45	251	1	16	241	2	0	0	0	0	228
46	255	0	2	0	0	0	0	0	0	236
47	197	1	1	28	159	104	158	0	0	240
48	221	2	0	0	3	0	0	0	0	248
49	228	1	4	2	0	0	0	0	0	256
50	251	0	97	45	1	0	0	0	0	264
51	6	167	186	0	0	0	0	0	0	272
52	11	0	1	0	0	0	0	0	0	276
```

### Prototype 13

Instruction count: 3

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	254	1	0	0	0	0	0	0	0	0
2	163	0	1	2	1	76	1	0	0	4
3	11	0	1	0	0	0	0	0	0	12
```

### Prototype 14

Instruction count: 37

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	254	0	0	0	0	0	0	0	0	0
2	9	0	56	177	0	0	0	0	0	4
3	254	1	0	0	0	0	0	0	0	8
4	198	2	1	3	132	175	0	0	0	12
5	224	6	59	189	0	0	0	0	0	20
6	151	2	2	6	0	0	0	0	0	24
7	250	1	106	41	2	0	0	0	0	28
8	255	0	0	0	0	0	0	0	0	36
9	198	1	1	2	27	105	0	0	0	40
10	15	6	187	188	0	0	0	0	0	48
11	151	1	1	6	0	0	0	0	0	52
12	250	0	91	101	1	0	0	0	0	56
13	254	0	0	0	0	0	0	0	0	64
14	198	1	1	2	146	35	0	0	0	68
15	21	6	0	0	0	0	0	0	0	76
16	151	1	1	6	0	0	0	0	0	80
17	251	0	72	161	1	0	0	0	0	84
18	255	0	0	0	0	0	0	0	0	92
19	198	1	1	2	21	221	0	0	0	96
20	21	6	1	0	0	0	0	0	0	104
21	151	1	1	6	0	0	0	0	0	108
22	251	0	185	221	1	0	0	0	0	112
23	6	242	182	0	0	0	0	0	0	120
24	254	0	2	0	0	0	0	0	0	124
25	9	0	151	183	0	0	0	0	0	128
26	254	1	2	0	0	0	0	0	0	132
27	197	2	2	100	211	16	210	0	0	136
28	221	3	0	0	4	0	0	0	0	144
29	228	2	4	2	0	0	0	0	0	152
30	251	1	32	61	2	0	0	0	0	160
31	255	0	2	0	0	0	0	0	0	168
32	197	1	1	170	4	222	5	0	0	172
33	221	2	0	0	3	0	0	0	0	180
34	228	1	4	2	0	0	0	0	0	188
35	251	0	49	121	1	0	0	0	0	196
36	6	167	186	0	0	0	0	0	0	204
37	11	0	1	0	0	0	0	0	0	208
```

### Prototype 15

Instruction count: 19

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	254	0	0	0	0	0	0	0	0	0
2	203	0	117	186	1	0	0	0	0	4
3	254	0	0	0	0	0	0	0	0	12
4	203	0	40	194	1	0	0	0	0	16
5	255	0	0	0	0	0	0	0	0	24
6	204	0	60	89	1	1	0	0	0	28
7	255	0	0	0	0	0	0	0	0	36
8	204	0	241	253	1	0	0	0	0	40
9	255	0	1	0	0	0	0	0	0	48
10	197	1	1	150	138	226	139	0	0	52
11	221	2	0	0	3	0	0	0	0	60
12	228	1	4	2	0	0	0	0	0	68
13	250	0	16	113	1	0	0	0	0	76
14	254	0	1	0	0	0	0	0	0	84
15	197	1	1	220	191	168	190	0	0	88
16	221	2	0	0	3	0	0	0	0	96
17	228	1	4	2	0	0	0	0	0	104
18	250	0	97	173	1	0	0	0	0	112
19	11	0	1	0	0	0	0	0	0	120
```

### Prototype 16

Instruction count: 3

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	254	1	0	0	0	0	0	0	0	0
2	163	0	1	2	1	35	0	0	0	4
3	10	0	1	0	0	0	0	0	0	12
```

### Prototype 17

Instruction count: 29

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	255	0	0	0	0	0	0	0	0	0
2	8	0	92	177	0	0	0	0	0	4
3	244	1	74	1	0	0	0	0	0	8
4	98	2	18	0	0	0	0	0	0	12
5	5	1	2	1	0	0	0	0	0	16
6	7	25	178	0	0	0	0	0	0	20
7	254	0	1	0	0	0	0	0	0	24
8	9	0	10	179	0	0	0	0	0	28
9	198	0	1	1	26	105	0	0	0	32
10	9	0	132	179	0	0	0	0	0	40
11	245	2	170	153	0	0	0	0	0	44
12	98	3	19	0	0	0	0	0	0	48
13	4	2	2	1	0	0	0	0	0	52
14	6	97	180	0	0	0	0	0	0	56
15	11	0	1	0	0	0	0	0	0	60
16	255	0	0	0	0	0	0	0	0	64
17	197	1	1	248	109	140	108	0	0	68
18	221	2	0	0	3	0	0	0	0	76
19	228	1	4	2	0	0	0	0	0	84
20	250	0	192	197	1	0	0	0	0	92
21	254	0	0	0	0	0	0	0	0	100
22	197	1	1	62	158	74	159	0	0	104
23	221	2	0	0	3	0	0	0	0	112
24	228	1	4	2	0	0	0	0	0	120
25	251	0	209	1	1	0	0	0	0	128
26	11	0	1	0	0	0	0	0	0	136
27	254	0	0	0	0	0	0	0	0	140
28	203	0	89	34	1	0	0	0	0	144
29	11	0	1	0	0	0	0	0	0	152
```

### Prototype 18

Instruction count: 11

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	255	0	0	0	0	0	0	0	0	0
2	197	1	1	6	210	114	211	0	0	4
3	221	2	0	0	3	0	0	0	0	12
4	228	1	4	2	0	0	0	0	0	20
5	250	0	144	17	1	0	0	0	0	28
6	254	0	0	0	0	0	0	0	0	36
7	197	1	1	76	7	56	6	0	0	40
8	221	2	0	0	3	0	0	0	0	48
9	228	1	4	2	0	0	0	0	0	56
10	251	0	225	77	1	0	0	0	0	64
11	11	0	1	0	0	0	0	0	0	72
```

### Prototype 19

Instruction count: 3

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	254	0	0	0	0	0	0	0	0	0
2	203	0	117	186	1	0	0	0	0	4
3	11	0	1	0	0	0	0	0	0	12
```

### Prototype 20

Instruction count: 4

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	254	1	0	0	0	0	0	0	0	0
2	195	2	248	153	133	152	132	152	0	4
3	163	0	1	3	1	86	1	0	0	12
4	11	0	1	0	0	0	0	0	0	20
```

### Prototype 21

Instruction count: 34

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	198	1	0	2	208	216	0	0	0	0
2	196	4	0	4	0	105	19	105	0	8
3	137	3	4	177	91	0	0	0	0	16
4	129	0	1	3	0	0	0	0	0	24
5	197	2	2	69	89	36	88	0	0	28
6	197	3	3	222	46	170	47	0	0	36
7	248	4	0	68	164	0	0	0	0	44
8	248	7	0	112	202	0	0	0	0	52
9	198	8	1	9	76	104	0	0	0	60
10	128	5	7	8	0	0	0	0	0	68
11	249	6	0	10	60	0	0	0	0	72
12	4	3	4	0	0	0	0	0	0	80
13	4	2	0	2	0	0	0	0	0	84
14	197	10	10	187	230	186	230	0	0	88
15	197	11	11	203	191	202	191	0	0	96
16	192	12	60	0	0	0	0	0	0	104
17	124	22	12	0	0	0	0	0	0	108
18	5	11	2	2	0	0	0	0	0	112
19	14	12	0	0	0	0	0	0	0	116
20	228	10	4	2	0	0	0	0	0	120
21	130	1	2	10	0	0	0	0	0	128
22	255	4	2	0	0	0	0	0	0	132
23	254	5	3	0	0	0	0	0	0	136
24	197	6	6	208	76	174	77	0	0	140
25	254	7	4	0	0	0	0	0	0	148
26	195	8	248	193	141	192	140	192	0	152
27	195	9	56	184	79	185	78	185	0	160
28	4	6	4	2	0	0	0	0	0	168
29	101	7	38	41	0	0	0	0	0	172
30	250	7	54	61	1	0	0	0	0	176
31	2	3	4	204	114	0	0	0	0	184
32	5	3	5	2	0	0	0	0	0	192
33	163	2	3	2	1	97	1	0	0	196
34	11	0	1	0	0	0	0	0	0	204
```

### Prototype 22

Instruction count: 4

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	255	1	0	0	0	0	0	0	0	0
2	195	2	248	153	133	152	179	152	0	4
3	163	0	1	3	1	86	1	0	0	12
4	11	0	1	0	0	0	0	0	0	20
```

### Prototype 23

Instruction count: 5

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	255	0	0	0	0	0	0	0	0	0
2	244	2	173	238	0	0	0	0	0	4
3	206	1	2	211	206	217	206	0	0	8
4	250	0	191	4	1	0	0	0	0	16
5	11	0	1	0	0	0	0	0	0	24
```

### Prototype 24

Instruction count: 72

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	0	0	0	0	0	0	0	0	0	0
2	254	3	1	0	0	0	0	0	0	4
3	254	4	2	0	0	0	0	0	0	8
4	197	5	5	40	128	86	129	0	0	12
5	15	6	57	189	0	0	0	0	0	20
6	4	5	2	2	0	0	0	0	0	24
7	101	6	197	177	0	0	0	0	0	28
8	236	7	0	24	0	0	0	0	0	32
9	197	7	7	10	180	13	180	0	0	40
10	221	8	40	0	9	40	0	0	0	48
11	228	7	4	2	62	0	0	0	0	56
12	74	7	152	180	0	0	0	0	0	64
13	197	7	7	66	16	69	16	0	0	68
14	221	8	16	0	9	16	0	0	0	76
15	228	7	4	2	22	0	0	0	0	84
16	251	6	231	148	7	0	0	0	0	92
17	2	2	3	60	72	0	0	0	0	100
18	5	2	5	2	0	0	0	0	0	108
19	163	1	2	2	1	97	1	0	0	112
20	254	3	1	0	0	0	0	0	0	120
21	254	4	3	0	0	0	0	0	0	124
22	197	5	5	52	158	74	159	0	0	128
23	224	6	211	83	0	0	0	0	0	136
24	5	5	2	2	0	0	0	0	0	140
25	101	6	80	89	0	0	0	0	0	144
26	236	7	0	24	0	0	0	0	0	148
27	197	7	7	6	210	1	210	0	0	156
28	221	8	100	0	9	100	0	0	0	164
29	228	7	4	2	220	0	0	0	0	172
30	74	7	186	185	0	0	0	0	0	180
31	197	7	7	94	46	89	46	0	0	184
32	221	8	45	0	9	45	0	0	0	192
33	228	7	4	2	65	0	0	0	0	200
34	251	6	9	108	7	0	0	0	0	208
35	2	2	3	108	126	0	0	0	0	216
36	5	2	5	2	0	0	0	0	0	224
37	163	1	2	2	1	97	1	0	0	228
38	254	3	1	0	0	0	0	0	0	236
39	254	4	4	0	0	0	0	0	0	240
40	197	5	5	48	188	78	189	0	0	244
41	224	6	69	233	0	0	0	0	0	252
42	5	5	2	2	0	0	0	0	0	256
43	101	6	235	1	0	0	0	0	0	260
44	236	7	0	24	0	0	0	0	0	264
45	197	7	7	2	240	5	240	0	0	272
46	221	8	210	0	9	215	0	0	0	280
47	228	7	4	2	255	0	0	0	0	288
48	74	7	220	190	0	0	0	0	0	296
49	197	7	7	90	76	93	76	0	0	300
50	221	8	160	0	9	165	0	0	0	308
51	228	7	4	2	200	0	0	0	0	316
52	250	6	214	68	7	0	0	0	0	324
53	3	2	3	220	180	0	0	0	0	332
54	5	2	5	2	0	0	0	0	0	340
55	163	1	2	2	1	97	1	0	0	344
56	254	1	5	0	0	0	0	0	0	352
57	236	2	0	4	0	0	0	0	0	356
58	13	2	218	103	0	0	0	0	0	364
59	12	11	142	96	0	0	0	0	0	368
60	151	2	2	11	0	0	0	0	0	372
61	250	1	1	176	2	0	0	0	0	376
62	255	1	5	0	0	0	0	0	0	384
63	236	2	0	24	0	0	0	0	0	388
64	197	2	2	136	229	143	229	0	0	396
65	221	3	100	0	4	210	0	0	0	404
66	228	2	4	2	100	0	0	0	0	412
67	74	2	194	195	0	0	0	0	0	420
68	197	2	2	192	65	199	65	0	0	424
69	221	3	90	0	4	90	0	0	0	432
70	228	2	4	2	115	0	0	0	0	440
71	250	1	102	40	2	0	0	0	0	448
72	11	0	1	0	0	0	0	0	0	456
```

### Prototype 25

Instruction count: 101

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	197	3	3	237	252	236	252	0	0	0
2	13	4	57	182	0	0	0	0	0	8
3	255	5	0	0	0	0	0	0	0	12
4	4	3	3	2	0	0	0	0	0	16
5	22	2	3	0	0	0	0	0	0	20
6	197	3	3	191	47	170	47	0	0	24
7	221	4	1	0	5	0	0	0	0	32
8	192	6	0	0	0	0	0	0	0	40
9	228	3	5	2	30	0	0	0	0	44
10	250	2	131	76	3	0	0	0	0	52
11	203	2	158	223	3	1	0	0	0	60
12	203	2	189	227	3	100	0	0	0	68
13	197	4	4	85	16	84	16	0	0	76
14	13	5	4	110	0	0	0	0	0	84
15	212	4	2	2	0	0	0	0	0	88
16	22	3	4	0	0	0	0	0	0	96
17	197	4	4	153	108	140	108	0	0	100
18	224	5	81	84	0	0	0	0	0	108
19	221	6	0	0	7	1	0	0	0	112
20	228	4	5	2	0	0	0	0	0	120
21	251	3	243	208	4	0	0	0	0	128
22	203	3	228	11	4	1	0	0	0	136
23	250	3	97	232	0	0	0	0	0	144
24	197	4	4	184	77	191	77	0	0	152
25	221	5	160	0	6	165	0	0	0	160
26	228	4	4	2	200	0	0	0	0	168
27	250	3	166	24	4	0	0	0	0	176
28	203	3	84	35	4	12	0	0	0	184
29	195	4	184	166	215	166	214	166	0	192
30	250	3	52	60	4	0	0	0	0	200
31	195	4	56	148	67	148	66	148	0	208
32	251	3	128	84	4	0	0	0	0	216
33	203	3	39	55	4	101	0	0	0	224
34	197	4	4	51	179	50	179	0	0	232
35	12	5	31	241	0	0	0	0	0	240
36	212	4	2	2	0	0	0	0	0	244
37	22	3	4	0	0	0	0	0	0	252
38	197	4	4	127	15	106	15	0	0	256
39	15	5	229	131	0	0	0	0	0	264
40	14	6	0	0	0	0	0	0	0	268
41	224	7	66	233	0	0	0	0	0	272
42	228	4	5	2	0	0	0	0	0	276
43	251	3	211	216	4	0	0	0	0	284
44	197	4	4	147	25	134	25	0	0	292
45	15	5	53	181	0	0	0	0	0	300
46	192	6	0	0	0	0	0	0	0	304
47	224	7	158	27	0	0	0	0	0	308
48	228	4	5	2	0	0	0	0	0	312
49	251	3	48	32	4	0	0	0	0	320
50	197	4	4	196	35	195	35	0	0	328
51	221	5	22	0	6	22	0	0	0	336
52	228	4	4	2	32	0	0	0	0	344
53	251	3	247	80	4	0	0	0	0	352
54	197	4	4	28	127	27	127	0	0	360
55	221	5	200	0	6	205	0	0	0	368
56	228	4	4	2	240	0	0	0	0	376
57	250	3	198	128	4	0	0	0	0	384
58	245	4	95	22	0	0	0	0	0	392
59	254	6	1	0	0	0	0	0	0	396
60	116	5	6	1	0	0	0	0	0	400
61	232	4	2	2	3	57	72	0	0	404
62	203	3	48	171	4	12	0	0	0	412
63	195	4	56	116	87	116	86	116	0	420
64	250	3	148	212	4	0	0	0	0	428
65	204	3	167	63	4	0	0	0	0	436
66	203	3	139	187	4	0	0	0	0	444
67	203	3	131	191	4	101	0	0	0	452
68	197	4	4	215	65	214	65	0	0	460
69	13	5	232	36	0	0	0	0	0	468
70	212	4	3	2	0	0	0	0	0	472
71	197	7	7	165	198	184	198	0	0	480
72	213	7	2	0	0	6	0	0	0	488
73	251	4	187	64	7	0	0	0	0	496
74	197	5	5	99	75	98	75	0	0	504
75	13	6	169	0	0	0	0	0	0	512
76	212	5	3	2	0	0	0	0	0	516
77	22	4	5	0	0	0	0	0	0	524
78	197	5	5	71	167	90	167	0	0	528
79	213	5	2	0	0	6	0	0	0	536
80	251	4	136	148	5	0	0	0	0	544
81	248	5	3	178	160	0	0	0	0	552
82	98	6	26	0	0	0	0	0	0	560
83	163	4	5	3	1	96	0	0	0	564
84	66	1	0	0	0	0	0	0	0	572
85	11	0	1	0	0	0	0	0	0	576
86	244	1	195	43	0	0	0	0	0	580
87	198	2	0	3	85	36	0	0	0	584
88	4	1	2	2	0	0	0	0	0	592
89	236	0	1	16	0	0	0	0	0	596
90	255	1	1	0	0	0	0	0	0	604
91	255	2	2	0	0	0	0	0	0	608
92	120	0	1	2	0	0	0	0	0	612
93	7	139	178	0	0	0	0	0	0	616
94	255	0	0	0	0	0	0	0	0	620
95	245	1	155	213	0	0	0	0	0	624
96	254	3	1	0	0	0	0	0	0	628
97	254	4	2	0	0	0	0	0	0	632
98	115	2	3	4	0	0	0	0	0	636
99	232	1	2	2	0	33	216	0	0	640
100	7	170	180	0	0	0	0	0	0	648
101	10	0	1	0	0	0	0	0	0	652
```

### Prototype 26

Instruction count: 16

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	244	1	95	218	0	0	0	0	0	0
2	198	2	0	3	115	202	0	0	0	4
3	4	1	2	2	0	0	0	0	0	12
4	236	0	1	16	0	0	0	0	0	16
5	255	1	1	0	0	0	0	0	0	24
6	255	2	2	0	0	0	0	0	0	28
7	120	0	1	2	0	0	0	0	0	32
8	7	139	178	0	0	0	0	0	0	36
9	255	0	0	0	0	0	0	0	0	40
10	245	1	31	134	0	0	0	0	0	44
11	254	3	1	0	0	0	0	0	0	48
12	254	4	2	0	0	0	0	0	0	52
13	115	2	3	4	0	0	0	0	0	56
14	232	1	2	2	0	181	96	0	0	60
15	7	170	180	0	0	0	0	0	0	68
16	10	0	1	0	0	0	0	0	0	72
```

### Prototype 27

Instruction count: 24

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	249	2	0	160	192	0	0	0	0	0
2	195	3	248	153	191	152	190	152	0	8
3	77	2	35	178	3	0	0	0	0	16
4	216	235	192	1	1	0	0	0	0	24
5	21	1	0	0	0	0	0	0	0	32
6	73	1	76	178	0	0	0	0	0	36
7	249	5	0	114	164	0	0	0	0	40
8	195	6	120	99	63	98	33	98	0	48
9	77	5	28	180	6	0	0	0	0	56
10	216	173	194	1	1	0	0	0	0	64
11	216	238	194	1	0	0	0	0	0	72
12	9	1	11	180	0	0	0	0	0	80
13	21	8	1	0	0	0	0	0	0	84
14	1	8	0	0	0	0	0	0	0	88
15	194	3	2	0	24	136	114	137	0	92
16	196	4	1	4	131	133	170	133	0	100
17	129	1	2	4	0	0	0	0	0	108
18	0	1	2	0	0	0	0	0	0	112
19	194	3	2	0	208	144	187	145	0	116
20	196	4	1	4	199	141	239	141	0	124
21	129	1	2	4	0	0	0	0	0	132
22	0	1	3	0	0	0	0	0	0	136
23	6	242	182	0	0	0	0	0	0	140
24	11	0	1	0	0	0	0	0	0	144
```

### Prototype 28

Instruction count: 29

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	255	1	0	0	0	0	0	0	0	0
2	8	1	9	177	0	0	0	0	0	4
3	249	2	0	134	12	0	0	0	0	8
4	195	3	120	135	63	134	35	134	0	16
5	77	2	181	178	3	0	0	0	0	24
6	216	133	193	1	1	0	0	0	0	32
7	21	1	0	0	0	0	0	0	0	40
8	73	1	218	178	0	0	0	0	0	44
9	248	5	0	88	240	0	0	0	0	48
10	195	6	248	81	191	80	161	80	0	56
11	77	5	174	180	6	0	0	0	0	64
12	216	59	195	1	1	0	0	0	0	72
13	216	132	195	1	0	0	0	0	0	80
14	7	97	180	0	0	0	0	0	0	88
15	9	1	86	181	0	0	0	0	0	92
16	255	8	1	0	0	0	0	0	0	96
17	197	9	9	153	108	140	108	0	0	100
18	192	10	0	0	0	0	0	0	0	108
19	194	15	14	0	208	144	186	145	0	112
20	255	16	2	0	0	0	0	0	0	120
21	129	11	14	16	0	0	0	0	0	124
22	14	12	0	0	0	0	0	0	0	128
23	194	18	17	0	168	152	195	153	0	132
24	255	19	3	0	0	0	0	0	0	140
25	129	13	17	19	0	0	0	0	0	144
26	4	9	5	2	0	0	0	0	0	148
27	251	8	208	24	9	0	0	0	0	152
28	7	95	184	0	0	0	0	0	0	160
29	11	0	1	0	0	0	0	0	0	164
```

### Prototype 29

Instruction count: 16

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	249	2	0	160	192	0	0	0	0	0
2	195	3	248	153	191	152	190	152	0	8
3	77	2	35	178	3	0	0	0	0	16
4	216	235	192	1	1	0	0	0	0	24
5	21	1	0	0	0	0	0	0	0	32
6	74	1	76	178	0	0	0	0	0	36
7	249	5	0	114	164	0	0	0	0	40
8	195	6	120	99	63	98	33	98	0	48
9	76	5	28	180	6	0	0	0	0	56
10	216	173	194	1	1	0	0	0	0	64
11	216	238	194	1	0	0	0	0	0	72
12	8	1	59	180	0	0	0	0	0	80
13	21	8	0	0	0	0	0	0	0	84
14	1	8	0	0	0	0	0	0	0	88
15	7	170	180	0	0	0	0	0	0	92
16	11	0	1	0	0	0	0	0	0	96
```

### Prototype 30

Instruction count: 33

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	1	0	0	0	0	0	0	0	0	0
2	254	0	1	0	0	0	0	0	0	4
3	230	0	203	106	1	0	0	0	0	8
4	255	2	2	0	0	0	0	0	0	16
5	254	3	3	0	0	0	0	0	0	20
6	197	4	4	212	46	170	47	0	0	24
7	224	5	137	35	0	0	0	0	0	32
8	5	4	2	2	0	0	0	0	0	36
9	101	5	46	25	0	0	0	0	0	40
10	254	6	0	0	0	0	0	0	0	44
11	8	6	91	180	0	0	0	0	0	48
12	197	6	6	208	57	215	57	0	0	52
13	221	7	60	0	8	60	0	0	0	60
14	228	6	4	2	100	0	0	0	0	68
15	74	6	82	181	0	0	0	0	0	76
16	197	6	6	40	149	47	149	0	0	80
17	221	7	30	0	8	30	0	0	0	88
18	228	6	4	2	45	0	0	0	0	96
19	251	5	87	184	6	0	0	0	0	104
20	255	6	0	0	0	0	0	0	0	112
21	9	6	5	183	0	0	0	0	0	116
22	197	6	6	92	159	91	159	0	0	120
23	221	7	220	0	8	225	0	0	0	128
24	228	6	4	2	255	0	0	0	0	136
25	74	6	60	184	0	0	0	0	0	144
26	197	6	6	148	251	147	251	0	0	148
27	221	7	160	0	8	165	0	0	0	156
28	228	6	4	2	200	0	0	0	0	164
29	251	5	6	48	6	0	0	0	0	172
30	3	1	2	116	113	0	0	0	0	180
31	4	1	5	2	0	0	0	0	0	188
32	163	0	1	2	1	97	1	0	0	192
33	11	0	1	0	0	0	0	0	0	200
```

### Prototype 31

Instruction count: 5

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	255	0	0	0	0	0	0	0	0	0
2	254	1	1	0	0	0	0	0	0	4
3	121	1	1	0	0	0	0	0	0	8
4	5	0	2	1	0	0	0	0	0	12
5	10	0	1	0	0	0	0	0	0	16
```

### Prototype 32

Instruction count: 48

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	249	1	0	160	192	0	0	0	0	0
2	195	2	248	153	191	152	190	152	0	8
3	67	1	199	177	2	0	0	0	0	16
4	11	0	1	0	0	0	0	0	0	24
5	198	1	0	3	107	161	0	0	0	28
6	198	2	0	4	28	147	0	0	0	36
7	194	5	4	0	136	120	226	121	0	44
8	249	6	1	113	202	0	0	0	0	52
9	79	6	74	180	4	0	0	0	0	60
10	216	161	194	3	1	0	0	0	0	68
11	21	3	0	0	0	0	0	0	0	76
12	8	3	109	180	0	0	0	0	0	80
13	194	8	7	0	252	132	150	133	0	84
14	249	10	1	47	174	0	0	0	0	92
15	248	11	2	220	212	0	0	0	0	100
16	128	9	10	11	0	0	0	0	0	108
17	78	7	147	182	9	0	0	0	0	112
18	216	229	196	3	1	0	0	0	0	120
19	216	54	197	3	0	0	0	0	0	128
20	9	3	137	182	0	0	0	0	0	136
21	194	13	12	0	12	148	103	149	0	140
22	248	14	1	134	222	0	0	0	0	148
23	78	14	192	184	12	0	0	0	0	156
24	216	171	198	3	1	0	0	0	0	164
25	216	236	198	3	0	0	0	0	0	172
26	8	3	99	184	0	0	0	0	0	180
27	194	16	15	0	96	160	11	161	0	184
28	249	18	1	116	194	0	0	0	0	192
29	248	19	2	99	232	0	0	0	0	200
30	128	17	18	19	0	0	0	0	0	208
31	78	15	41	187	17	0	0	0	0	212
32	216	227	200	3	1	0	0	0	0	220
33	216	52	201	3	0	0	0	0	0	228
34	8	3	155	186	0	0	0	0	0	236
35	11	0	1	0	0	0	0	0	0	240
36	21	1	1	0	0	0	0	0	0	244
37	1	1	1	0	0	0	0	0	0	248
38	14	1	0	0	0	0	0	0	0	252
39	0	1	2	0	0	0	0	0	0	256
40	194	3	2	0	26	58	112	59	0	260
41	196	4	3	4	74	183	99	183	0	268
42	129	1	2	4	0	0	0	0	0	276
43	0	1	4	0	0	0	0	0	0	280
44	194	3	2	0	210	66	185	67	0	284
45	196	4	3	4	142	191	166	191	0	292
46	129	1	2	4	0	0	0	0	0	300
47	0	1	5	0	0	0	0	0	0	304
48	10	0	1	0	0	0	0	0	0	308
```

### Prototype 33

Instruction count: 37

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	254	1	0	0	0	0	0	0	0	0
2	9	1	117	177	0	0	0	0	0	4
3	248	2	0	134	12	0	0	0	0	8
4	195	3	120	135	63	134	35	134	0	16
5	77	2	181	178	3	0	0	0	0	24
6	216	137	193	1	1	0	0	0	0	32
7	216	202	193	1	0	0	0	0	0	40
8	9	1	143	179	0	0	0	0	0	48
9	197	7	7	76	181	28	180	0	0	52
10	194	10	8	0	246	254	156	255	0	60
11	194	11	9	0	64	128	43	129	0	68
12	5	7	3	2	0	0	0	0	0	76
13	197	12	12	4	17	84	16	0	0	80
14	196	15	1	15	225	129	200	129	0	88
15	255	18	2	0	0	0	0	0	0	96
16	128	13	15	18	0	0	0	0	0	100
17	196	19	1	19	210	135	250	135	0	104
18	255	22	3	0	0	0	0	0	0	112
19	128	14	19	22	0	0	0	0	0	116
20	4	12	3	2	0	0	0	0	0	120
21	129	6	7	12	0	0	0	0	0	124
22	249	5	6	244	222	0	0	0	0	128
23	0	5	4	0	0	0	0	0	0	136
24	254	1	1	0	0	0	0	0	0	140
25	197	2	2	41	36	60	36	0	0	144
26	14	3	0	0	0	0	0	0	0	152
27	194	8	7	0	96	160	10	161	0	156
28	255	9	2	0	0	0	0	0	0	164
29	129	4	7	9	0	0	0	0	0	168
30	14	5	0	0	0	0	0	0	0	172
31	194	11	10	0	56	168	83	169	0	176
32	254	12	3	0	0	0	0	0	0	184
33	129	6	10	12	0	0	0	0	0	188
34	5	2	5	2	0	0	0	0	0	192
35	251	1	80	120	2	0	0	0	0	196
36	7	167	186	0	0	0	0	0	0	204
37	11	0	1	0	0	0	0	0	0	208
```

### Prototype 34

Instruction count: 21

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	248	2	0	160	192	0	0	0	0	0
2	195	3	248	153	191	152	190	152	0	8
3	76	2	35	178	3	0	0	0	0	16
4	216	235	192	1	1	0	0	0	0	24
5	21	1	0	0	0	0	0	0	0	32
6	9	1	133	178	0	0	0	0	0	36
7	255	1	0	0	0	0	0	0	0	40
8	8	1	39	179	0	0	0	0	0	44
9	21	5	0	0	0	0	0	0	0	48
10	1	5	0	0	0	0	0	0	0	52
11	254	1	1	0	0	0	0	0	0	56
12	14	2	6	0	0	0	0	0	0	60
13	104	1	58	181	2	0	0	0	0	64
14	255	3	2	0	0	0	0	0	0	72
15	254	4	3	0	0	0	0	0	0	76
16	121	4	4	0	0	0	0	0	0	80
17	5	3	2	1	0	0	0	0	0	84
18	6	141	181	0	0	0	0	0	0	88
19	7	202	181	0	0	0	0	0	0	92
20	7	23	182	0	0	0	0	0	0	96
21	10	0	1	0	0	0	0	0	0	100
```

### Prototype 35

Instruction count: 77

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	8	1	16	177	0	0	0	0	0	0
2	10	0	1	0	0	0	0	0	0	4
3	198	1	0	3	15	189	0	0	0	8
4	198	2	0	4	184	175	0	0	0	16
5	198	3	1	5	107	161	0	0	0	24
6	198	4	1	6	28	147	0	0	0	32
7	194	7	6	0	136	120	226	121	0	40
8	249	8	3	113	202	0	0	0	0	48
9	79	8	108	180	6	0	0	0	0	56
10	216	161	194	5	1	0	0	0	0	64
11	21	5	0	0	0	0	0	0	0	72
12	8	5	79	180	0	0	0	0	0	76
13	194	10	9	0	252	132	150	133	0	80
14	249	12	3	47	174	0	0	0	0	88
15	249	13	4	220	212	0	0	0	0	96
16	128	11	12	13	0	0	0	0	0	104
17	78	9	181	182	11	0	0	0	0	108
18	216	229	196	5	1	0	0	0	0	116
19	216	54	197	5	0	0	0	0	0	124
20	8	5	235	182	0	0	0	0	0	132
21	194	15	14	0	12	148	103	149	0	136
22	249	16	3	134	222	0	0	0	0	144
23	79	16	226	184	14	0	0	0	0	152
24	216	171	198	5	1	0	0	0	0	160
25	216	236	198	5	0	0	0	0	0	168
26	9	5	77	184	0	0	0	0	0	176
27	194	18	17	0	96	160	11	161	0	180
28	249	20	3	116	194	0	0	0	0	188
29	248	21	4	99	232	0	0	0	0	196
30	128	19	20	21	0	0	0	0	0	204
31	79	17	75	187	19	0	0	0	0	208
32	216	227	200	5	1	0	0	0	0	216
33	216	52	201	5	0	0	0	0	0	224
34	9	5	197	186	0	0	0	0	0	232
35	10	0	1	0	0	0	0	0	0	236
36	194	5	4	0	66	50	40	51	0	240
37	248	6	1	250	24	0	0	0	0	248
38	78	6	143	188	4	0	0	0	0	256
39	216	238	202	3	1	0	0	0	0	264
40	21	3	0	0	0	0	0	0	0	272
41	8	3	170	188	0	0	0	0	0	276
42	194	8	7	0	182	62	220	63	0	280
43	249	10	1	168	252	0	0	0	0	288
44	248	11	2	165	34	0	0	0	0	296
45	128	9	10	11	0	0	0	0	0	304
46	78	7	232	190	9	0	0	0	0	308
47	216	58	205	3	1	0	0	0	0	316
48	216	123	205	3	0	0	0	0	0	324
49	9	3	206	190	0	0	0	0	0	332
50	194	13	12	0	198	78	173	79	0	336
51	249	14	1	1	44	0	0	0	0	344
52	78	14	5	193	12	0	0	0	0	352
53	216	224	206	3	1	0	0	0	0	360
54	216	49	207	3	0	0	0	0	0	368
55	9	3	168	192	0	0	0	0	0	376
56	194	16	15	0	58	90	81	91	0	380
57	248	18	1	255	16	0	0	0	0	388
58	249	19	2	234	54	0	0	0	0	396
59	128	17	18	19	0	0	0	0	0	404
60	78	15	110	195	17	0	0	0	0	408
61	216	56	209	3	1	0	0	0	0	416
62	216	121	209	3	0	0	0	0	0	424
63	8	3	160	194	0	0	0	0	0	432
64	21	20	1	0	0	0	0	0	0	436
65	1	20	2	0	0	0	0	0	0	440
66	192	3	0	0	0	0	0	0	0	444
67	1	3	3	0	0	0	0	0	0	448
68	194	5	4	0	2	114	104	115	0	452
69	249	6	1	26	216	0	0	0	0	460
70	129	3	4	6	0	0	0	0	0	468
71	0	3	4	0	0	0	0	0	0	472
72	194	5	4	0	218	122	177	123	0	476
73	248	6	1	47	112	0	0	0	0	484
74	129	3	4	6	0	0	0	0	0	492
75	1	3	5	0	0	0	0	0	0	496
76	7	15	198	0	0	0	0	0	0	500
77	10	0	1	0	0	0	0	0	0	504
```

### Prototype 36

Instruction count: 31

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	254	1	0	0	0	0	0	0	0	0
2	73	1	68	177	0	0	0	0	0	4
3	11	0	1	0	0	0	0	0	0	8
4	197	3	3	6	128	86	129	0	0	12
5	194	6	4	0	108	116	6	117	0	20
6	194	7	5	0	62	246	85	247	0	28
7	5	3	3	2	0	0	0	0	0	36
8	197	8	8	222	220	142	221	0	0	40
9	196	11	1	11	106	119	67	119	0	48
10	254	14	2	0	0	0	0	0	0	56
11	128	9	11	14	0	0	0	0	0	60
12	196	15	1	15	95	125	119	125	0	64
13	254	18	3	0	0	0	0	0	0	72
14	128	10	15	18	0	0	0	0	0	76
15	4	8	3	2	0	0	0	0	0	80
16	129	2	3	8	0	0	0	0	0	84
17	249	1	2	181	32	0	0	0	0	88
18	1	1	4	0	0	0	0	0	0	96
19	254	1	1	0	0	0	0	0	0	100
20	197	2	2	99	241	118	241	0	0	104
21	14	3	0	0	0	0	0	0	0	112
22	194	8	7	0	222	22	180	23	0	116
23	254	9	2	0	0	0	0	0	0	124
24	129	4	7	9	0	0	0	0	0	128
25	14	5	0	0	0	0	0	0	0	132
26	194	11	10	0	150	30	253	31	0	136
27	255	12	3	0	0	0	0	0	0	144
28	129	6	10	12	0	0	0	0	0	148
29	4	2	5	2	0	0	0	0	0	152
30	250	1	64	60	2	0	0	0	0	156
31	10	0	1	0	0	0	0	0	0	164
```

### Prototype 37

Instruction count: 15

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	255	0	0	0	0	0	0	0	0	0
2	121	0	0	0	0	0	0	0	0	4
3	9	0	145	177	0	0	0	0	0	8
4	11	0	1	0	0	0	0	0	0	12
5	21	0	0	0	0	0	0	0	0	16
6	0	0	0	0	0	0	0	0	0	20
7	255	0	1	0	0	0	0	0	0	24
8	14	1	10	0	0	0	0	0	0	28
9	104	0	237	179	1	0	0	0	0	32
10	254	2	2	0	0	0	0	0	0	40
11	254	3	3	0	0	0	0	0	0	44
12	121	3	3	0	0	0	0	0	0	48
13	4	2	2	1	0	0	0	0	0	52
14	6	97	180	0	0	0	0	0	0	56
15	11	0	1	0	0	0	0	0	0	60
```

### Prototype 38

Instruction count: 19

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	245	0	61	219	0	0	0	0	0	0
2	254	1	0	0	0	0	0	0	0	4
3	5	0	2	4	0	0	0	0	0	8
4	126	0	149	182	0	0	0	0	0	12
5	236	5	4	8	0	0	0	0	0	16
6	249	5	4	67	126	0	0	0	0	24
7	8	5	30	179	0	0	0	0	0	32
8	244	6	6	96	0	0	0	0	0	36
9	98	7	39	0	0	0	0	0	0	40
10	4	6	2	1	0	0	0	0	0	44
11	6	134	179	0	0	0	0	0	0	48
12	66	4	0	0	0	0	0	0	0	52
13	95	0	34	72	2	0	0	0	0	56
14	48	0	0	0	0	0	0	0	0	64
15	0	0	0	0	0	0	0	0	0	68
16	10	0	1	0	0	0	0	0	0	72
17	255	1	0	0	0	0	0	0	0	76
18	163	0	1	2	1	76	1	0	0	80
19	10	0	1	0	0	0	0	0	0	88
```

### Prototype 39

Instruction count: 3

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	255	1	0	0	0	0	0	0	0	0
2	163	0	1	2	1	76	1	0	0	4
3	10	0	1	0	0	0	0	0	0	12
```

### Prototype 40

Instruction count: 37

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	255	0	0	0	0	0	0	0	0	0
2	121	0	0	0	0	0	0	0	0	4
3	73	0	124	177	0	0	0	0	0	8
4	254	0	1	0	0	0	0	0	0	12
5	9	0	35	178	0	0	0	0	0	16
6	11	0	1	0	0	0	0	0	0	20
7	254	0	2	0	0	0	0	0	0	24
8	238	2	1	2	34	23	0	0	0	28
9	254	3	3	0	0	0	0	0	0	36
10	129	1	2	3	0	0	0	0	0	40
11	79	0	86	180	1	0	0	0	0	44
12	238	4	1	2	182	155	0	0	0	52
13	0	4	3	0	0	0	0	0	0	60
14	21	0	1	0	0	0	0	0	0	64
15	1	0	1	0	0	0	0	0	0	68
16	197	0	0	89	148	108	148	0	0	72
17	98	1	41	0	0	0	0	0	0	80
18	5	0	2	1	0	0	0	0	0	84
19	197	0	0	135	27	178	27	0	0	88
20	98	1	42	0	0	0	0	0	0	96
21	5	0	2	1	0	0	0	0	0	100
22	7	169	182	0	0	0	0	0	0	104
23	11	0	1	0	0	0	0	0	0	108
24	244	0	198	144	0	0	0	0	0	112
25	255	1	0	0	0	0	0	0	0	116
26	5	0	2	1	0	0	0	0	0	120
27	11	0	1	0	0	0	0	0	0	124
28	221	0	1	0	1	1	0	0	0	128
29	134	1	1	0	0	0	0	0	0	136
30	192	2	4	0	0	0	0	0	0	140
31	92	0	51	181	0	0	0	0	0	144
32	197	3	3	185	4	184	4	0	0	148
33	209	3	1	1	0	0	0	0	0	156
34	99	0	243	73	0	0	0	0	0	164
35	21	0	0	0	0	0	0	0	0	168
36	1	0	0	0	0	0	0	0	0	172
37	11	0	1	0	0	0	0	0	0	176
```

### Prototype 41

Instruction count: 4

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	244	0	50	219	0	0	0	0	0	0
2	255	1	0	0	0	0	0	0	0	4
3	5	0	2	1	0	0	0	0	0	8
4	11	0	1	0	0	0	0	0	0	12
```

### Prototype 42

Instruction count: 10

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	221	0	1	0	1	1	0	0	0	0
2	134	1	1	0	0	0	0	0	0	8
3	192	2	4	0	0	0	0	0	0	12
4	92	0	51	181	0	0	0	0	0	16
5	197	3	3	67	89	66	89	0	0	20
6	209	3	1	1	0	0	0	0	0	28
7	99	0	243	73	0	0	0	0	0	36
8	21	0	0	0	0	0	0	0	0	40
9	1	0	0	0	0	0	0	0	0	44
10	11	0	1	0	0	0	0	0	0	48
```

### Prototype 43

Instruction count: 34

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	236	1	0	8	0	0	0	0	0	0
2	249	1	0	163	230	0	0	0	0	8
3	9	1	50	177	0	0	0	0	0	16
4	244	3	215	20	0	0	0	0	0	20
5	249	4	1	123	88	0	0	0	0	24
6	12	11	1	159	0	0	0	0	0	32
7	151	4	4	11	0	0	0	0	0	36
8	5	3	2	2	0	0	0	0	0	40
9	22	2	3	0	0	0	0	0	0	44
10	197	3	3	206	139	189	138	0	0	48
11	205	4	2	5	123	1	0	0	0	56
12	192	6	1	0	0	0	0	0	0	64
13	21	7	1	0	0	0	0	0	0	68
14	5	3	5	2	0	0	0	0	0	72
15	9	3	44	181	0	0	0	0	0	76
16	197	8	8	89	148	222	149	0	0	80
17	15	9	141	33	0	0	0	0	0	88
18	254	10	0	0	0	0	0	0	0	92
19	5	8	3	1	0	0	0	0	0	96
20	11	0	1	0	0	0	0	0	0	100
21	197	3	3	232	200	155	201	0	0	104
22	205	4	2	5	124	1	0	0	0	112
23	192	6	1	0	0	0	0	0	0	120
24	21	7	1	0	0	0	0	0	0	124
25	5	3	5	2	0	0	0	0	0	128
26	9	3	79	184	0	0	0	0	0	132
27	197	8	8	119	211	240	210	0	0	136
28	224	9	66	82	0	0	0	0	0	144
29	255	10	0	0	0	0	0	0	0	148
30	5	8	3	1	0	0	0	0	0	152
31	11	0	1	0	0	0	0	0	0	156
32	7	135	185	0	0	0	0	0	0	160
33	7	204	185	0	0	0	0	0	0	164
34	10	0	1	0	0	0	0	0	0	168
```

### Prototype 44

Instruction count: 45

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	233	1	0	1	1	0	0	0	0	0
2	0	0	1	0	0	0	0	0	0	8
3	220	1	0	2	78	114	29	115	0	12
4	0	1	2	0	0	0	0	0	0	20
5	220	1	0	2	10	22	14	23	0	24
6	1	1	3	0	0	0	0	0	0	32
7	245	2	122	77	0	0	0	0	0	36
8	98	3	45	0	0	0	0	0	0	40
9	5	2	2	3	0	0	0	0	0	44
10	215	0	2	1	3	0	0	0	0	48
11	236	2	0	4	0	0	0	0	0	56
12	22	2	1	0	0	0	0	0	0	64
13	9	2	137	180	0	0	0	0	0	68
14	197	3	3	250	230	245	230	0	0	72
15	255	4	5	0	0	0	0	0	0	80
16	212	3	1	1	0	0	0	0	0	84
17	7	60	181	0	0	0	0	0	0	92
18	255	2	2	0	0	0	0	0	0	96
19	206	1	2	217	207	216	207	0	0	100
20	236	0	1	68	0	0	0	0	0	108
21	245	3	34	87	0	0	0	0	0	116
22	98	4	46	0	0	0	0	0	0	120
23	4	3	2	3	0	0	0	0	0	124
24	215	1	3	2	4	0	0	0	0	128
25	236	3	1	4	0	0	0	0	0	136
26	22	3	2	0	0	0	0	0	0	144
27	8	3	184	184	0	0	0	0	0	148
28	197	4	4	198	168	201	168	0	0	152
29	255	5	5	0	0	0	0	0	0	160
30	212	4	2	1	0	0	0	0	0	164
31	7	50	185	0	0	0	0	0	0	172
32	7	135	185	0	0	0	0	0	0	176
33	6	204	185	0	0	0	0	0	0	180
34	66	0	0	0	0	0	0	0	0	184
35	11	0	1	0	0	0	0	0	0	188
36	198	1	0	2	12	239	0	0	0	192
37	254	2	1	0	0	0	0	0	0	200
38	3	0	1	180	136	0	0	0	0	204
39	4	0	3	0	0	0	0	0	0	212
40	11	0	0	0	0	0	0	0	0	216
41	198	1	0	2	146	169	0	0	0	220
42	254	2	1	0	0	0	0	0	0	228
43	3	0	1	172	151	0	0	0	0	232
44	5	0	3	0	0	0	0	0	0	240
45	11	0	0	0	0	0	0	0	0	244
```

### Prototype 45

Instruction count: 5

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	198	1	0	2	98	217	0	0	0	0
2	254	2	1	0	0	0	0	0	0	8
3	3	0	1	108	31	0	0	0	0	12
4	4	0	3	0	0	0	0	0	0	20
5	11	0	0	0	0	0	0	0	0	24
```

### Prototype 46

Instruction count: 5

```text
pc	code	op	A	B	C	D	E	F	G	Cjump
1	198	1	0	2	98	217	0	0	0	0
2	254	2	1	0	0	0	0	0	0	8
3	3	0	1	108	31	0	0	0	0	12
4	5	0	3	0	0	0	0	0	0	20
5	11	0	0	0	0	0	0	0	0	24
```
