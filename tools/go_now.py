#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 4):
        print(f"Usage: {argv[0]} <output-runbook-file> [--pbcopy-cmd <command>]", file=sys.stderr)
        return 1

    output_file = Path(argv[1])
    pbcopy_cmd = None
    if len(argv) == 4:
        if argv[2] != "--pbcopy-cmd":
            print("Unknown option", file=sys.stderr)
            return 1
        pbcopy_cmd = argv[3]

    preflight = subprocess.run(
        ["python3", str(ROOT / "tools" / "preflight_check.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    print(preflight.stdout.strip())
    print()

    today = subprocess.run(
        ["python3", str(ROOT / "tools" / "today_actions.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    print(today.stdout.strip())
    print()

    start = subprocess.run(
        ["python3", str(ROOT / "tools" / "start_today.py"), str(output_file)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    print(start.stdout.strip())

    copy_cmd = ["python3", str(ROOT / "tools" / "copy_outreach_text.py"), "wechat-group"]
    if pbcopy_cmd is not None:
        copy_cmd.extend(["--pbcopy-cmd", pbcopy_cmd])
    copy = subprocess.run(
        copy_cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    print(copy.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
