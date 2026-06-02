#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys


SECTION_RE = re.compile(r"^### (.+?)\n\n(.*?)(?=^### |\Z)", re.S | re.M)


def parse_issue(markdown: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for heading, body in SECTION_RE.findall(markdown):
        result[heading.strip()] = body.strip()
    return result


def build_brief(data: dict[str, str]) -> str:
    lines = [
        "# Imported Service Request",
        "",
        f"Service type: {data.get('Service type', 'Unknown')}",
        f"Delivery window: {data.get('Delivery window', 'Unknown')}",
        f"Budget range: {data.get('Budget range', 'Unknown')}",
        "",
        "## Problem",
        "",
        data.get("What problem do you want solved?", ""),
        "",
        "## Desired output",
        "",
        data.get("What final output do you need?", ""),
        "",
        "## Existing materials",
        "",
        data.get("What materials already exist?", ""),
        "",
        "## Constraints",
        "",
        data.get("Hard constraints or things that must not be touched", ""),
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"Usage: {argv[0]} <issue-markdown> <output-brief>", file=sys.stderr)
        return 1

    issue_path = Path(argv[1])
    out_path = Path(argv[2])

    if not issue_path.exists():
        print(f"Issue file not found: {issue_path}", file=sys.stderr)
        return 1

    data = parse_issue(issue_path.read_text())
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_brief(data))
    print(f"Wrote brief to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
