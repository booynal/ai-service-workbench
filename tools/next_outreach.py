#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import csv
import sys


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"Usage: {argv[0]} <plan-csv> <log-csv>", file=sys.stderr)
        return 1

    plan_path = Path(argv[1])
    log_path = Path(argv[2])

    plan_rows = read_csv(plan_path)
    log_rows = read_csv(log_path)
    sent_targets = {row["target"] for row in log_rows if row.get("status") == "sent"}

    def rank(row: dict[str, str]) -> tuple[int, int]:
        notes = row.get("notes", "").lower()
        channel = row.get("channel", "")
        priority_bucket = 0 if "highest-priority" in notes else 1
        channel_bucket = 0 if channel == "wechat" else 1
        return (priority_bucket, channel_bucket)

    remaining = [
        row for row in plan_rows
        if row.get("target") not in sent_targets and row.get("status") == "drafted"
    ]

    if remaining:
        row = sorted(remaining, key=rank)[0]
        print(f"Next target: {row.get('target')}")
        print(f"Channel: {row.get('channel')}")
        print(f"Asset: {row.get('asset_used')}")
        print(f"Next action: {row.get('next_action')}")
        print(f"Notes: {row.get('notes')}")
        if row.get("channel") == "wechat" and "群" in row.get("asset_used", ""):
            print("Runbook: runbooks/wechat-group.md")
        elif row.get("channel") == "wechat":
            print("Runbook: runbooks/dm-direct.md")
        elif row.get("target") == "csa issue #2":
            print("Runbook: runbooks/csa-issue-2.md")
        return 0

    print("No remaining outreach targets in plan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
