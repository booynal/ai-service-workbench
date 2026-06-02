#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import os
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "outreach_packets" / "manifest.json"


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3):
        print(f"Usage: {argv[0]} <candidate-key> [--execute]", file=sys.stderr)
        return 1

    candidate = argv[1]
    execute = len(argv) == 3 and argv[2] == "--execute"

    data = json.loads(MANIFEST.read_text())
    if candidate not in data:
        print(f"Unknown candidate: {candidate}", file=sys.stderr)
        return 1

    item = data[candidate]
    target_url = item.get("target_url", "")
    message = item.get("message", "")

    print(f"Candidate: {candidate}")
    print(f"Target URL: {target_url}")
    print(f"Message file: {message}")

    if not execute:
        print("PREVIEW ONLY: no external send performed.")
        return 0

    if candidate != "csa-issue-2":
        print("Execute mode currently only supported for csa-issue-2.", file=sys.stderr)
        return 1

    gh_cmd = os.environ.get("GH_CMD", "gh")
    body_file = ROOT / message
    subprocess.run(
        [gh_cmd, "issue", "comment", "2", "--repo", "faisalabdullah-commits/csa", "--body-file", str(body_file)],
        check=True,
    )
    print("Comment sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
