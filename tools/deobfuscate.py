#!/usr/bin/env python3
"""Unpack supported wYnFuscate and build an Arena.ai reconstruction bundle.

There are two useful modes:

    # Raw protected source -> instrumented VM dump -> Arena upload bundle
    python3 tools/deobfuscate.py source message.txt -o analysis

    # Existing runtime dump -> Arena upload bundle
    python3 tools/deobfuscate.py dump deobfuscation/vm_dump.txt -o analysis/ai

The source unpacker is a *profile*, not a universal Lua deobfuscator. It targets
the wYnFuscate layout reverse-engineered in this repository. The dump-to-bundle
stage is generic for dumps in the P<n>.<field>/Z5POST format. Every export embeds
instructions requiring observable-functionality equivalence rather than original
source structure.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import shutil
import subprocess
import sys
import textwrap
import zipfile
from pathlib import Path
from typing import Any

from parse_vm_dump import make_serializable, parse_dump, write_strings

REPO = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
KNOWN_SOURCE_SHA256 = "0527abcd05b22c0c170e7a444e8f099cf2e7862b52ac6ebeee69f058cc341cae"
PROFILE_NAME = "wynfuscate-supax-2026-10"
ARRAY_COLUMNS = ("code", "op", "A", "B", "C", "D", "E", "F", "G", "Cjump")


class DeobfuscationError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_checked(
    command: list[str],
    *,
    cwd: Path,
    timeout: int,
    log_path: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise DeobfuscationError(
            f"command timed out after {timeout}s: {' '.join(command)}"
        ) from error
    except OSError as error:
        raise DeobfuscationError(
            f"could not execute {' '.join(command)}: {error}"
        ) from error

    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(result.stdout, errors="replace")
    if result.returncode != 0:
        tail = "\n".join(result.stdout.splitlines()[-25:])
        raise DeobfuscationError(
            f"command failed with exit code {result.returncode}:\n"
            f"  {' '.join(command)}\n\n{tail}"
        )
    return result


def luau_command(binary: Path, runner: Path) -> list[str]:
    """Run the bundled ELF even when Git checked it out without executable bits."""
    if os.access(binary, os.X_OK):
        return [str(binary), str(runner)]
    for loader in (
        Path("/lib64/ld-linux-x86-64.so.2"),
        Path("/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2"),
    ):
        if loader.exists():
            return [str(loader), str(binary), str(runner)]
    raise DeobfuscationError(
        f"{binary} is not executable and no ELF loader was found; run chmod +x {binary}"
    )


def check_source_profile(source: Path, force: bool) -> tuple[str, str]:
    if not source.is_file():
        raise DeobfuscationError(f"source file does not exist: {source}")
    source_hash = sha256(source)
    prefix = source.read_bytes()[:512]
    banner_found = b"Protected by wYnFuscate" in prefix
    if not banner_found and not force:
        raise DeobfuscationError(
            "input does not contain the supported wYnFuscate banner; "
            "use --force-profile to try the profile anyway"
        )
    confidence = "exact" if source_hash == KNOWN_SOURCE_SHA256 else "experimental"
    return source_hash, confidence


def unpack_source(args: argparse.Namespace) -> Path:
    source = args.input.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    source_hash, confidence = check_source_profile(source, args.force_profile)
    if confidence != "exact":
        print(
            "[warning] source hash is not the fully tested sample; attempting the "
            "same wYnFuscate profile",
            file=sys.stderr,
        )

    source_copy = output / "protected-source.lua"
    if source != source_copy:
        shutil.copyfile(source, source_copy)

    beautified = output / "beautified.lua"
    instrumented = output / "instrumented-vm.luau"
    dump = output / "vm-dump.txt"
    build_log = output / "build.log"

    run_checked(
        [sys.executable, str(REPO / "beautify.py"), str(source), str(beautified)],
        cwd=REPO,
        timeout=args.timeout,
        log_path=output / "beautify.log",
    )

    try:
        build_result = run_checked(
            [
                sys.executable,
                str(REPO / "build_run.py"),
                "--source",
                str(beautified),
                "--output",
                str(instrumented),
            ],
            cwd=REPO,
            timeout=args.timeout,
        )
    except DeobfuscationError as error:
        build_log.write_text(str(error) + "\n")
        raise DeobfuscationError(
            "the wYnFuscate profile did not match this sample. The protector "
            "randomized or changed a structure that still needs a new profile. "
            f"Diagnostic: {build_log}"
        ) from error
    build_log.write_text(build_result.stdout)

    if args.no_execute:
        metadata = {
            "profile": PROFILE_NAME,
            "profile_confidence": confidence,
            "source": str(source),
            "source_sha256": source_hash,
            "instrumented_runner": str(instrumented),
            "executed": False,
        }
        (output / "unpack-manifest.json").write_text(json.dumps(metadata, indent=2) + "\n")
        print(instrumented)
        return instrumented

    luau = REPO / "luau"
    command = luau_command(luau, instrumented)
    run_result = run_checked(command, cwd=REPO, timeout=args.timeout)
    dump.write_text(run_result.stdout, errors="replace")

    metadata = {
        "profile": PROFILE_NAME,
        "profile_confidence": confidence,
        "source": str(source),
        "source_sha256": source_hash,
        "instrumented_runner": str(instrumented),
        "dump": str(dump),
        "executed": True,
        "execution_note": (
            "The wrapper ran in the bundled Luau CLI with fake Roblox/executor "
            "globals. The generated profile does not execute the recovered root payload."
        ),
    }
    (output / "unpack-manifest.json").write_text(json.dumps(metadata, indent=2) + "\n")

    ai_output = output / "ai"
    create_ai_bundle(
        dump,
        ai_output,
        source_path=source,
        beautified_path=beautified,
        instrumented_path=instrumented,
        include_runtime=not args.no_portable_runtime,
        source_hash=source_hash,
        profile_confidence=confidence,
    )
    print(f"VM dump: {dump}")
    print(f"Arena instructions: {ai_output / 'ARENA_TASK.md'}")
    print(f"Upload to Arena: {ai_output / 'arena-reconstruction-bundle.zip'}")
    print(f"Paste this message: {ai_output / 'ARENA_UPLOAD_MESSAGE.txt'}")
    return ai_output


def printable_string(value: bytes) -> str:
    if not value:
        return "<empty>"
    decoded = value.decode("utf-8", errors="backslashreplace")
    return decoded.replace("\\", "\\\\").replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t")


def format_value(value: Any) -> str:
    if value is None:
        return "_"
    if isinstance(value, float):
        return f"{value:.17g}"
    return str(value)


def instruction_rows(prototype: dict[str, Any]) -> list[str]:
    instruction_count = len(prototype.get("code", []))
    rows = ["pc\t" + "\t".join(ARRAY_COLUMNS)]
    for index in range(instruction_count):
        values = []
        for name in ARRAY_COLUMNS:
            field = prototype.get(name, [])
            value = field[index] if index < len(field) else None
            values.append(format_value(value))
        rows.append(f"{index + 1}\t" + "\t".join(values))
    return rows


def known_profile_for_dump(dump: Path, source_hash: str | None) -> bool:
    if source_hash == KNOWN_SOURCE_SHA256:
        return True
    known_dump = REPO / "deobfuscation" / "vm_dump.txt"
    return known_dump.exists() and sha256(dump) == sha256(known_dump)


def make_ai_context(
    parsed: dict[str, Any],
    manifest: dict[str, Any],
    known_profile: bool,
) -> str:
    prototypes = parsed["prototypes"]
    strings = parsed["strings"]
    constants = parsed["constants"]
    dispatch_counts: collections.Counter[int] = collections.Counter()
    for prototype in prototypes.values():
        dispatch_counts.update(prototype.get("code", []))

    lines = [
        "# AI deobfuscation context",
        "",
        "## Read this first",
        "",
        "This bundle is evidence, not a claim that arbitrary VM bytecode has already",
        "been converted back into original source. `code` contains custom virtual",
        "dispatch bytes, **not standard Lua/Luau opcodes**. Do not silently assign",
        "standard opcode meanings to them. Preserve observed behavior separately from",
        "inferences, and mark every inference.",
        "",
        "For a functionality-equivalent reconstruction, use this priority order:",
        "",
        "1. Runtime traces and observed side effects.",
        "2. Decoded strings and numeric constants.",
        "3. Per-prototype instruction arrays and proven dispatch semantics.",
        "4. Structural inference only when the first three are insufficient.",
        "",
        "## Manifest",
        "",
        "```json",
        json.dumps(manifest, indent=2),
        "```",
        "",
        "## VM summary",
        "",
        f"- Prototypes: {len(prototypes)}",
        f"- Instructions: {sum(len(item.get('code', [])) for item in prototypes.values())}",
        f"- Distinct dispatch bytes: {len(dispatch_counts)}",
        f"- Decoded strings: {len(strings)}",
        f"- Constants: {len(constants)}",
        f"- Page failures: {len(parsed['page_failures'])}",
        "",
        "Dispatch histogram:",
        "",
        "```text",
        " ".join(f"{key}:{dispatch_counts[key]}" for key in sorted(dispatch_counts)),
        "```",
        "",
        "## Numeric constants",
        "",
    ]

    constant_counts = collections.Counter(value for value in constants if value is not None)
    lines.extend(
        [
            "The complete indexed array is in `machine/constants.json`. Value counts:",
            "",
            "```text",
            " ".join(
                f"{format_value(value)}:{count}"
                for value, count in sorted(constant_counts.items(), key=lambda item: float(item[0]))
            ),
            "```",
            "",
            "## Decoded strings",
            "",
            "The TSV copy is in `machine/decoded-strings.tsv`. Empty byte strings are shown as `<empty>`.",
            "",
            "```text",
        ]
    )
    for string_id, value in sorted(strings.items()):
        lines.append(f"{string_id:4}  {printable_string(value)}")
    lines.extend(["```", ""])

    if known_profile:
        notes = REPO / "deobfuscation" / "README.md"
        readable = REPO / "deobfuscation" / "deobfuscated.lua"
        lines.extend(
            [
                "## Profile-specific recovered behavior",
                "",
                "This dump matches the fully analyzed repository sample. The following",
                "notes and reconstruction are available as additional evidence.",
                "",
            ]
        )
        if notes.exists():
            lines.extend([notes.read_text(errors="replace"), ""])
        if readable.exists():
            lines.extend(
                [
                    "## Existing readable reconstruction",
                    "",
                    "```lua",
                    readable.read_text(errors="replace"),
                    "```",
                    "",
                ]
            )

    lines.extend(
        [
            "## Virtual instruction listings",
            "",
            "Columns are `pc code op A B C D E F G Cjump`. A `_` is a missing value.",
            "The same listings are split into one file per prototype under `instructions/`.",
            "",
        ]
    )
    for prototype_id, prototype in sorted(prototypes.items()):
        lines.extend(
            [
                f"### Prototype {prototype_id}",
                "",
                f"Instruction count: {len(prototype.get('code', []))}",
                "",
                "```text",
                *instruction_rows(prototype),
                "```",
                "",
            ]
        )
    return "\n".join(lines)


def copy_known_evidence(output: Path) -> None:
    reconstruction = REPO / "deobfuscation" / "deobfuscated.lua"
    if reconstruction.exists():
        shutil.copyfile(reconstruction, output / "known-reconstruction.lua")
    traces_source = REPO / "deobfuscation" / "traces"
    traces_output = output / "known-traces"
    if traces_source.exists():
        traces_output.mkdir(exist_ok=True)
        for source in traces_source.iterdir():
            if source.is_file():
                shutil.copyfile(source, traces_output / source.name)


def make_arena_task(manifest: dict[str, Any]) -> str:
    """Instructions embedded in every export for a fresh Arena.ai Agent session."""
    runtime_available = manifest.get("portable_runtime", False)
    runtime_note = (
        "A portable Luau CLI is included under `runtime/`. Use it for all dynamic "
        "experiments; do not run the payload in Roblox or an executor."
        if runtime_available
        else
        "No Luau binary is bundled. Use the Luau tooling already present in the "
        "Arena repository, or install/build a sandboxed CLI before dynamic experiments."
    )
    source_note = (
        "3. `machine/protected-source.lua` and `machine/beautified-source.lua`\n"
        if manifest.get("source") and manifest.get("beautified_source")
        else "3. Any protected/beautified source present under `machine/`\n"
    )
    runner_note = (
        "6. `runtime/instrumented-vm.luau` for additional controlled experiments"
        if manifest.get("instrumented_runner")
        else "6. `runtime/README.txt` for rebuilding or extending controlled experiments"
    )
    return textwrap.dedent(
        f"""\
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
        {source_note.rstrip()}
        4. `machine/vm.json`, `machine/decoded-strings.tsv`, and `instructions/`
        5. `known-traces/` and `known-reconstruction.lua` when present
        {runner_note}

        The `code` field is a custom virtual dispatch stream, **not standard Luau
        bytecode**. Never assign standard Luau opcode meanings merely because a numeric
        dispatch byte resembles one. Prove handler semantics from the embedded interpreter
        or runtime traces.

        {runtime_note}

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
        """
    )


def make_arena_upload_message() -> str:
    return textwrap.dedent(
        """\
        I attached an Arena reconstruction bundle produced by tools/deobfuscate.py.
        Extract it, read ARENA_TASK.md first, and reconstruct functionality-equivalent
        clean Luau. Original structure and names do not matter; observable functionality
        must match 1:1. Use the bundled sandbox/runtime evidence, continue dynamic callback
        tracing where needed, and do not stop at a UI-only or string-based reconstruction.
        Produce reconstructed.lua plus the behavior contract and differential results
        required by ARENA_TASK.md.
        """
    )


def copy_runtime_kit(
    output: Path,
    instrumented_path: Path | None,
    include_runtime: bool,
) -> None:
    runtime = output / "runtime"
    runtime.mkdir(exist_ok=True)
    if instrumented_path and instrumented_path.exists():
        shutil.copyfile(instrumented_path, runtime / "instrumented-vm.luau")

    for name in ("env_prelude.lua", "build_run.py", "beautify.py"):
        source = REPO / name
        if source.exists():
            shutil.copyfile(source, runtime / name)

    runtime_tools = runtime / "tools"
    runtime_tools.mkdir(exist_ok=True)
    for source in (TOOLS / "parse_vm_dump.py", Path(__file__).resolve()):
        if source.exists():
            shutil.copyfile(source, runtime_tools / source.name)

    if include_runtime:
        for name in ("luau", "luau-compile"):
            source = REPO / name
            if source.exists():
                shutil.copyfile(source, runtime / name)

    binary_note = (
        "Bundled binaries: run `chmod +x runtime/luau runtime/luau-compile`, then "
        "use `runtime/luau runtime/instrumented-vm.luau > runtime-output.txt`."
        if include_runtime
        else
        "Luau binaries were not included; use a sandboxed Luau CLI available in the "
        "Arena workspace."
    )
    runner_note = (
        "The instrumented runner dumps VM state without executing the recovered root "
        "payload. Make a working copy before adding root/callback execution patches."
        if instrumented_path and instrumented_path.exists()
        else
        "No instrumented runner was supplied. Rebuild one with the included scripts "
        "when the protected and beautified sources match the supported profile."
    )
    (runtime / "README.txt").write_text(
        textwrap.dedent(
            f"""\
            These files are for controlled analysis in Arena's sandbox.

            {binary_note}
            Parse a new dump with `python3 runtime/tools/parse_vm_dump.py runtime-output.txt`.

            {runner_note}
            Never run the protected source in Roblox or a live executor.
            """
        )
    )


def write_archive(output: Path) -> Path:
    archive = output / "arena-reconstruction-bundle.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as handle:
        for path in sorted(output.rglob("*")):
            if path.is_file() and path != archive:
                handle.write(path, path.relative_to(output))
    return archive


def create_ai_bundle(
    dump: Path,
    output: Path,
    *,
    source_path: Path | None = None,
    beautified_path: Path | None = None,
    instrumented_path: Path | None = None,
    include_runtime: bool = False,
    source_hash: str | None = None,
    profile_confidence: str = "unknown",
) -> Path:
    dump = dump.resolve()
    named_inputs = (
        ("VM dump", dump),
        ("protected source", source_path),
        ("beautified source", beautified_path),
        ("instrumented runner", instrumented_path),
    )
    for label, input_path in named_inputs:
        if input_path is not None and not input_path.is_file():
            raise DeobfuscationError(f"{label} file does not exist: {input_path}")

    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    managed_paths = [
        *(output / name for name in ("machine", "instructions", "runtime", "known-traces")),
        *(output / name for name in (
            "manifest.json",
            "AI_CONTEXT.md",
            "ARENA_TASK.md",
            "ARENA_UPLOAD_MESSAGE.txt",
            "README-FIRST.txt",
            "known-reconstruction.lua",
            "PROMPT.txt",
            "ai-bundle.zip",
            "arena-reconstruction-bundle.zip",
        )),
    ]
    for input_path in (dump, source_path, beautified_path, instrumented_path):
        if input_path is None:
            continue
        resolved_input = input_path.resolve()
        if any(
            resolved_input == managed
            or (managed.is_dir() and managed in resolved_input.parents)
            for managed in managed_paths
        ):
            raise DeobfuscationError(
                f"input {input_path} is inside generated output {output}; "
                "choose a separate output directory"
            )

    # Validate before replacing a prior bundle in a reused output directory.
    parsed = parse_dump(dump)
    if not parsed["prototypes"]:
        raise DeobfuscationError(
            "dump contains no P<n>.code arrays; pass the complete instrumented VM output"
        )
    if parsed["page_failures"]:
        print(
            f"[warning] dump contains {len(parsed['page_failures'])} page failures",
            file=sys.stderr,
        )

    # A reused output directory must not leak binaries/evidence from a prior export.
    for generated_dir in ("machine", "instructions", "runtime", "known-traces"):
        path = output / generated_dir
        if path.exists():
            shutil.rmtree(path)
    for generated_file in (
        "manifest.json",
        "AI_CONTEXT.md",
        "ARENA_TASK.md",
        "ARENA_UPLOAD_MESSAGE.txt",
        "README-FIRST.txt",
        "known-reconstruction.lua",
        "PROMPT.txt",
        "ai-bundle.zip",
        "arena-reconstruction-bundle.zip",
    ):
        path = output / generated_file
        if path.exists():
            path.unlink()

    machine = output / "machine"
    instructions = output / "instructions"
    machine.mkdir()
    instructions.mkdir()

    known_profile = known_profile_for_dump(dump, source_hash)
    runtime_available = include_runtime and all(
        (REPO / name).is_file() for name in ("luau", "luau-compile")
    )
    if include_runtime and not runtime_available:
        print(
            "[warning] portable runtime requested, but luau/luau-compile are not both available",
            file=sys.stderr,
        )
    serializable = make_serializable(parsed)
    manifest = {
        "format": "arena-luau-vm-functionality-bundle-v2",
        "goal": "observable functionality equivalence; original source structure is irrelevant",
        "profile": PROFILE_NAME if known_profile else "unknown-custom-luau-vm",
        "profile_confidence": "exact" if known_profile else profile_confidence,
        "source": "machine/protected-source.lua" if source_path else None,
        "source_origin": str(source_path) if source_path else None,
        "source_sha256": source_hash,
        "beautified_source": "machine/beautified-source.lua" if beautified_path else None,
        "beautified_source_origin": str(beautified_path) if beautified_path else None,
        "beautified_source_sha256": sha256(beautified_path) if beautified_path else None,
        "instrumented_runner": "runtime/instrumented-vm.luau" if instrumented_path else None,
        "instrumented_runner_origin": str(instrumented_path) if instrumented_path else None,
        "instrumented_runner_sha256": sha256(instrumented_path) if instrumented_path else None,
        "portable_runtime": runtime_available,
        "portable_runtime_requested": include_runtime,
        "portable_runtime_platform": "Linux x86-64" if runtime_available else None,
        "dump": "machine/raw-vm-dump.txt",
        "dump_origin": str(dump),
        "dump_sha256": sha256(dump),
        "prototype_count": len(parsed["prototypes"]),
        "instruction_count": sum(
            len(item.get("code", [])) for item in parsed["prototypes"].values()
        ),
        "dispatch_byte_count": len(
            {
                opcode
                for item in parsed["prototypes"].values()
                for opcode in item.get("code", [])
            }
        ),
        "decoded_string_count": len(parsed["strings"]),
        "constant_count": len(parsed["constants"]),
        "page_failures": parsed["page_failures"],
        "limitations": [
            "Custom dispatch bytes are not standard Luau opcodes.",
            "Behavioral equivalence requires callback and environment coverage, not only static strings.",
            "External Roblox server responses cannot be recreated from an offline sample unless captured.",
            "Original names/comments/layout may be unrecoverable, but they are not required for this goal.",
        ],
    }

    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (machine / "vm.json").write_text(json.dumps(serializable, indent=2) + "\n")
    (machine / "constants.json").write_text(
        json.dumps(parsed["constants"], indent=2) + "\n"
    )
    write_strings(machine / "decoded-strings.tsv", parsed["strings"])
    shutil.copyfile(dump, machine / "raw-vm-dump.txt")
    if source_path:
        shutil.copyfile(source_path, machine / "protected-source.lua")
    if beautified_path:
        shutil.copyfile(beautified_path, machine / "beautified-source.lua")

    for prototype_id, prototype in sorted(parsed["prototypes"].items()):
        (instructions / f"prototype-{prototype_id:02}.tsv").write_text(
            "\n".join(instruction_rows(prototype)) + "\n"
        )

    context = make_ai_context(parsed, manifest, known_profile)
    (output / "AI_CONTEXT.md").write_text(context)
    arena_task = make_arena_task(manifest)
    (output / "ARENA_TASK.md").write_text(arena_task)
    (output / "ARENA_UPLOAD_MESSAGE.txt").write_text(make_arena_upload_message())
    (output / "README-FIRST.txt").write_text(
        "Upload arena-reconstruction-bundle.zip to Arena.ai and paste the contents "
        "of ARENA_UPLOAD_MESSAGE.txt. The agent must read ARENA_TASK.md first.\n"
    )

    if known_profile:
        copy_known_evidence(output)
    copy_runtime_kit(output, instrumented_path, runtime_available)
    archive = write_archive(output)
    print(f"Wrote {output / 'ARENA_TASK.md'}")
    print(f"Wrote {output / 'AI_CONTEXT.md'}")
    print(f"Wrote {archive}")
    return output


def bundle_dump(args: argparse.Namespace) -> Path:
    return create_ai_bundle(
        args.input,
        args.output,
        source_path=args.source,
        beautified_path=args.beautified,
        instrumented_path=args.instrumented,
        include_runtime=args.portable_runtime,
        source_hash=sha256(args.source) if args.source else None,
    )


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description="Unpack a supported custom Luau VM or package a dump for Arena.ai reconstruction."
    )
    commands = root.add_subparsers(dest="command", required=True)

    source = commands.add_parser("source", help="protected Luau source -> VM dump -> AI bundle")
    source.add_argument("input", type=Path)
    source.add_argument("-o", "--output", type=Path, required=True)
    source.add_argument("--timeout", type=int, default=120)
    source.add_argument(
        "--force-profile",
        action="store_true",
        help="attempt the wYnFuscate profile even when its banner is absent",
    )
    source.add_argument(
        "--no-execute",
        action="store_true",
        help="stop after producing the instrumented Luau runner",
    )
    source.add_argument(
        "--no-portable-runtime",
        action="store_true",
        help="omit bundled Luau CLI binaries from the Arena reconstruction bundle",
    )
    source.set_defaults(handler=unpack_source)

    dump = commands.add_parser("dump", help="existing VM dump -> AI bundle")
    dump.add_argument("input", type=Path)
    dump.add_argument("-o", "--output", type=Path, required=True)
    dump.add_argument("--source", type=Path, help="optional protected source to include and hash")
    dump.add_argument("--beautified", type=Path, help="optional beautified source to include for VM-handler lifting")
    dump.add_argument("--instrumented", type=Path, help="optional instrumented Luau runner to include")
    dump.add_argument(
        "--portable-runtime",
        action="store_true",
        help="include repository Luau CLI binaries and runtime support in the bundle",
    )
    dump.set_defaults(handler=bundle_dump)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        args.handler(args)
    except DeobfuscationError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
