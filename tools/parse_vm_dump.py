#!/usr/bin/env python3
"""Parse the runtime dump produced while unpacking message.txt.

The VM uses P<n>.code as its dispatch stream. P<n>.op is only another
operand array; treating it as the opcode stream was an early false lead.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path
from typing import Any

ARRAY_RE = re.compile(
    r"^P(?P<proto>\d+)\.(?P<name>op|A|B|C|D|E|F|G|code|Cjump|jump) (?P<data>.*)$"
)
PROTO_RE = re.compile(r"^PROTO\[(?P<proto>\d+)\] (?P<data>.*)$")
STRING_RE = re.compile(r"(?P<id>\d+)=(?P<size>\d+):(?P<hex>[0-9a-f]*)")


def parse_number(value: str) -> int | float | None:
    if value == "?":
        return None
    number = float(value)
    return int(number) if number.is_integer() else number


def parse_dump(path: Path) -> dict[str, Any]:
    prototypes: dict[int, dict[str, Any]] = {}
    metadata: dict[int, str] = {}
    strings: dict[int, bytes] = {}
    constants: list[int | float | None] = []
    page_failures: list[str] = []

    for raw_line in path.read_text(errors="replace").splitlines():
        line = raw_line.strip()
        match = ARRAY_RE.match(line)
        if match:
            values = [parse_number(item) for item in match["data"].split(",")]
            prototypes.setdefault(int(match["proto"]), {})[match["name"]] = values
            continue

        match = PROTO_RE.match(line)
        if match:
            metadata[int(match["proto"])] = match["data"]
            continue

        if line.startswith("CONST "):
            constants = [parse_number(item) for item in line[6:].split(",")]
            continue

        if line.startswith("Z5POST "):
            for string_match in STRING_RE.finditer(line):
                value = bytes.fromhex(string_match["hex"])
                expected_size = int(string_match["size"])
                if len(value) != expected_size:
                    raise ValueError(
                        f"decoded string {string_match['id']} has {len(value)} bytes, "
                        f"expected {expected_size}"
                    )
                strings[int(string_match["id"])] = value
            continue

        if line.startswith("PAGEFAIL["):
            page_failures.append(line)

    return {
        "prototypes": prototypes,
        "metadata": metadata,
        "strings": strings,
        "constants": constants,
        "page_failures": page_failures,
    }


def make_serializable(parsed: dict[str, Any]) -> dict[str, Any]:
    return {
        "constants": parsed["constants"],
        "metadata": {str(key): value for key, value in parsed["metadata"].items()},
        "page_failures": parsed["page_failures"],
        "prototypes": {
            str(key): value for key, value in sorted(parsed["prototypes"].items())
        },
        "strings": {
            str(key): value.decode("utf-8", errors="backslashreplace")
            for key, value in sorted(parsed["strings"].items())
        },
    }


def write_strings(path: Path, strings: dict[int, bytes]) -> None:
    lines = ["id\tlength\tvalue"]
    for string_id, value in sorted(strings.items()):
        escaped = value.decode("utf-8", errors="backslashreplace")
        escaped = escaped.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")
        lines.append(f"{string_id}\t{len(value)}\t{escaped or '<empty>'}")
    path.write_text("\n".join(lines) + "\n")


def print_summary(parsed: dict[str, Any]) -> None:
    prototypes = parsed["prototypes"]
    dispatch_counts: collections.Counter[int] = collections.Counter()
    instruction_count = 0
    for prototype in prototypes.values():
        code = prototype.get("code", [])
        dispatch_counts.update(code)
        instruction_count += len(code)

    print(f"prototypes: {len(prototypes)}")
    print(f"instructions: {instruction_count}")
    print(f"dispatch bytes: {len(dispatch_counts)}")
    print(f"decoded strings: {len(parsed['strings'])}")
    print(f"constants: {len(parsed['constants'])}")
    print(f"page failures: {len(parsed['page_failures'])}")
    print("prototype instruction counts:")
    for prototype_id, prototype in sorted(prototypes.items()):
        print(f"  {prototype_id:2}: {len(prototype.get('code', []))}")
    print("dispatch histogram:")
    print("  " + " ".join(f"{key}:{dispatch_counts[key]}" for key in sorted(dispatch_counts)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dump", type=Path, help="runtime VM dump")
    parser.add_argument("--json", type=Path, help="write all parsed data as JSON")
    parser.add_argument("--strings", type=Path, help="write decoded strings as TSV")
    args = parser.parse_args()

    parsed = parse_dump(args.dump)
    if args.json:
        args.json.write_text(json.dumps(make_serializable(parsed), indent=2) + "\n")
    if args.strings:
        write_strings(args.strings, parsed["strings"])
    print_summary(parsed)


if __name__ == "__main__":
    main()
