#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import csv
import sys


def main(argv: list[str]) -> int:
    if len(argv) != 9:
        print(
            f"Usage: {argv[0]} <csv-file> <date> <channel> <target> <asset_used> <status> <next_action> <notes>",
            file=sys.stderr,
        )
        return 1

    csv_file = Path(argv[1])
    row = argv[2:]
    csv_file.parent.mkdir(parents=True, exist_ok=True)

    if not csv_file.exists():
        csv_file.write_text("date,channel,target,asset_used,status,next_action,notes\n")

    with csv_file.open("a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

    print(f"Appended outreach entry to {csv_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
