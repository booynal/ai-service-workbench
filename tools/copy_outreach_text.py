#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "outreach_packets" / "manifest.json"


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 4):
        print(f"Usage: {argv[0]} <candidate-key> [--pbcopy-cmd <command>]", file=sys.stderr)
        return 1

    candidate = argv[1]
    pbcopy_cmd = "pbcopy"
    if len(argv) == 4:
        if argv[2] != "--pbcopy-cmd":
            print("Unknown option", file=sys.stderr)
            return 1
        pbcopy_cmd = argv[3]

    data = json.loads(MANIFEST.read_text())
    if candidate not in data:
        print(f"Unknown candidate: {candidate}", file=sys.stderr)
        return 1

    message_path = ROOT / data[candidate]["message"]
    text = message_path.read_text()

    subprocess.run(pbcopy_cmd, input=text, text=True, shell=True, check=True)
    print(f"Copied text from {data[candidate]['message']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
