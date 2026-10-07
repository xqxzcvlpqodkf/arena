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
