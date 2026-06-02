#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


def parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current = None
    for line in text.splitlines():
        if line.startswith("### "):
            current = line[4:].strip()
            sections[current] = ""
            continue
        if current is not None:
            sections[current] += (line + "\n")
    return {k: v.strip() for k, v in sections.items()}


def generate_message(data: dict[str, str]) -> str:
    service_type = data.get("Service type", "workflow support")
    problem = data.get("What problem do you want solved?", "").strip()
    summary = problem.split(".")[0].strip() if problem else "a workflow problem"

    return (
        "Hi,\n\n"
        f"I came across your issue and it looks like a real {service_type.lower()} problem rather than a routine backlog note.\n\n"
        f"My quick read is that the core issue is {summary.lower()}.\n"
        "I usually help with small first-pass automation or workflow setups, so if useful, I can share a short and concise view of:\n"
        "1. what the likely first deliverable is\n"
        "2. what information is still missing\n"
        "3. what a practical first version might look like\n\n"
        "No pressure — just offering a lightweight outside perspective if that would be useful.\n"
    )


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"Usage: {argv[0]} <brief-file> <output-file>", file=sys.stderr)
        return 1

    brief_file = Path(argv[1])
    output_file = Path(argv[2])
    if not brief_file.exists():
        print(f"Brief file not found: {brief_file}", file=sys.stderr)
        return 1

    data = parse_sections(brief_file.read_text())
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(generate_message(data))
    print(f"Wrote outreach message to {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
