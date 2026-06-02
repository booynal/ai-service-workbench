#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "outreach_packets" / "manifest.json"


def read(path_str: str) -> str:
    return (ROOT / path_str).read_text().strip()


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"Usage: {argv[0]} <candidate-key> <output-file>", file=sys.stderr)
        return 1

    candidate = argv[1]
    output_file = Path(argv[2])
    data = json.loads(MANIFEST.read_text())
    if candidate not in data:
        print(f"Unknown candidate: {candidate}", file=sys.stderr)
        return 1

    item = data[candidate]
    lines = [
        "# Outreach Runbook",
        "",
        f"Candidate: {candidate}",
        f"Priority: {item['priority']}",
        f"Target: {item['target_url']}",
        "",
        "## First Message",
        "",
        read(item["message"]),
    ]

    if item.get("if_interested"):
        lines += ["", "## If Interested", "", read(item["if_interested"])]
    if item.get("if_asks_price"):
        lines += ["", "## If Asks Price", "", read(item["if_asks_price"])]
    if item.get("followup_48h"):
        lines += ["", "## 48h Follow-up", "", read(item["followup_48h"])]
    if item.get("proposal"):
        lines += ["", "## Proposal Path", "", item["proposal"]]

    lines += [
        "",
        "## Log Command",
        "",
        f'python3 tools/log_outreach_entry.py 触达记录模板.csv 2026-06-03 unknown "{candidate}" "{item["message"]}" sent "wait reply" "manual send"',
        "",
    ]

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(lines))
    print(f"Wrote outreach runbook to {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
