#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "outreach_packets" / "manifest.json"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <candidate-key>", file=sys.stderr)
        return 1

    candidate = argv[1]
    data = json.loads(MANIFEST.read_text())
    if candidate not in data:
        print(f"Unknown candidate: {candidate}", file=sys.stderr)
        return 1

    item = data[candidate]
    print(f"Candidate: {candidate}")
    print(f"Priority: {item['priority']}")
    print(f"Target URL: {item['target_url']}")
    print(f"Message file: {item['message']}")
    print(f"Proposal file: {item['proposal']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
