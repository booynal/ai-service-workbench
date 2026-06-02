#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def parse_next_outreach(text: str) -> dict[str, str]:
    result = {}
    for line in text.splitlines():
        if ": " in line:
            k, v = line.split(": ", 1)
            result[k.strip()] = v.strip()
    return result


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <output-runbook-file>", file=sys.stderr)
        return 1

    output_file = Path(argv[1])
    proc = subprocess.run(
        ["python3", str(ROOT / "tools" / "next_outreach.py"), "触达计划.csv", "触达日志模板.csv"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    info = parse_next_outreach(proc.stdout)
    target = info.get("Next target", "")
    runbook = info.get("Runbook", "")
    if not runbook:
      print("No runbook available for next outreach target.", file=sys.stderr)
      return 1

    subprocess.run(
        ["python3", str(ROOT / "tools" / "render_outreach_runbook.py"), target.replace("group outreach", "wechat-group").replace("direct outreach", "dm-direct").replace("csa issue #2", "csa-issue-2"), str(output_file)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    print(f"Next target: {target}")
    print(f"Runbook generated: {output_file}")
    print("After sending, log it with tools/log_outreach_entry.py into 触达日志模板.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
