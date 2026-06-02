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
    if item.get("proposal"):
        print(f"Proposal file: {item['proposal']}")
    if item.get("if_interested"):
        print(f"If interested: {item['if_interested']}")
    if item.get("if_asks_price"):
        print(f"If asks price: {item['if_asks_price']}")
    if item.get("followup_48h"):
        print(f"48h follow-up: {item['followup_48h']}")
    print(
        "Log command: "
        f'python3 tools/log_outreach_entry.py 触达记录模板.csv 2026-06-03 unknown "{candidate}" "{item["message"]}" sent "wait reply" "manual send"'
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
