#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <output-runbook-file>", file=sys.stderr)
        return 1

    output_file = Path(argv[1])

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
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
