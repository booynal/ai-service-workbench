#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    proc = subprocess.run(
        ["python3", str(ROOT / "tools" / "next_outreach.py"), "触达计划.csv", "触达日志模板.csv"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    print("# Today Actions\n")
    print(proc.stdout.strip())
    print("\nSuggested next step:")
    if "group outreach" in proc.stdout:
        print("- Open runbooks/wechat-group.md")
    elif "direct outreach" in proc.stdout:
        print("- Open runbooks/dm-direct.md")
    elif "csa issue #2" in proc.stdout:
        print("- Open runbooks/csa-issue-2.md")
    print("- After sending, append a row to 触达日志模板.csv with tools/log_outreach_entry.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
