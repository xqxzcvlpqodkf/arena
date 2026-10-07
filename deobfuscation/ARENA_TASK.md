# Arena.ai Agent Task: Reconstruct Functionality 1:1

## Goal

Reconstruct the protected Luau program as clean, readable Luau with the same
**observable functionality**. Original variable names, source layout, control-flow
structure, and comments do not matter. Behavioral equivalence does.

The final result must preserve all reachable behavior that can affect the Roblox
environment or caller, including:

- initial state and even apparent original bugs/inconsistencies;
- services and globals accessed;
- instances created, properties, parenting, and destruction;
- event connections, callback conditions, ordering, and captured state;
- task scheduling, waits, debounce windows, loops, and cancellation;
- remote calls with exact argument shapes, values, and order;
- CFrame/vector/math calculations and physics/humanoid state changes;
- cleanup, restoration, respawn handling, and disconnect behavior;
- returned values, errors, file/network/executor side effects if actually reachable.

## Non-goals

Do **not** try to reproduce the original formatting, local names, junk branches,
VM implementation, anti-analysis code, or obfuscator cleanup traps unless they are
part of normal payload behavior. The clean implementation may be structured
completely differently.

## Evidence in this bundle

Start with these files, in order:

1. `manifest.json`
2. `AI_CONTEXT.md`
3. `machine/protected-source.lua` and `machine/beautified-source.lua`
4. `machine/vm.json`, `machine/decoded-strings.tsv`, and `instructions/`
5. `known-traces/` and `known-reconstruction.lua` when present
6. `runtime/instrumented-vm.luau` for additional controlled experiments

The `code` field is a custom virtual dispatch stream, **not standard Luau
bytecode**. Never assign standard Luau opcode meanings merely because a numeric
dispatch byte resembles one. Prove handler semantics from the embedded interpreter
or runtime traces.

A portable Luau CLI is included under `runtime/`. Use it for all dynamic experiments; do not run the payload in Roblox or an executor.

## Required methodology

1. Establish a behavior inventory from decoded strings, constants, root execution,
   and every registered callback. Strings alone are evidence of availability, not
   proof that a path executes.
2. Separate protector/VM behavior from payload behavior. Bypass anti-analysis only
   narrowly and document each bypass.
3. Decode every prototype page and verify there are no page failures before relying
   on an instruction listing.
4. Execute the root in the fake environment. Capture every created instance,
   property assignment, service call, task, connection, remote call, and return.
5. Capture all virtual closures passed to `Connect`, `spawn`, `delay`, and `defer`.
   Invoke each with realistic fake Roblox values, covering true and false branches,
   mouse/touch variants, valid/invalid text, character lifecycle, animation IDs,
   target-found/target-missing cases, and cleanup paths.
6. Improve the fake datatypes as needed so Vector2/Vector3/CFrame/UDim arithmetic
   records exact constructor operands instead of collapsing to nil or opaque tables.
7. Lift only the custom VM handlers needed for still-unresolved behavior. Build a
   per-dispatch semantic map with evidence; do not guess.
8. Write `reconstructed.lua` without the virtual machine or loadstring wrapper.
9. Differentially test the reconstruction against captured protected-payload traces.
   Normalize object identities and addresses, then compare ordered side effects and
   callback results scenario by scenario.
10. Keep iterating until every behavior-affecting mismatch is resolved or is blocked
    by a genuinely unavailable external Roblox server response.

## Required deliverables

- `reconstructed.lua` — clean standalone functionality-equivalent Luau.
- `BEHAVIOR_CONTRACT.md` — exhaustive observed behavior and scenario matrix.
- `DIFFERENTIAL_RESULTS.md` — protected versus reconstructed trace comparison.
- `UNRESOLVED.md` — only genuinely blocked external behavior. Do not use this as a
  place to leave ordinary callback logic or VM operations unfinished.

## Acceptance standard

“Looks similar” is not enough. UI resemblance or matching decoded strings alone is
not enough. The reconstruction is complete when the same input scenarios produce
the same ordered externally visible effects, values, timing decisions, state
transitions, remote arguments, and cleanup behavior.

If an earlier readable reconstruction is present, treat it as a hypothesis. Verify
it against traces and virtual execution rather than copying its inferred sections.
