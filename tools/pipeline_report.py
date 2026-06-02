#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import os
import subprocess
import sys


def fetch_issues(gh_cmd: str) -> list[dict]:
    proc = subprocess.run(
        [
            gh_cmd,
            "issue",
            "list",
            "--repo",
            "booynal/ai-service-workbench",
            "--state",
            "all",
            "--limit",
            "100",
            "--json",
            "number,title,state,labels,url",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(proc.stdout)


def build_report(issues: list[dict]) -> str:
    open_issues = [i for i in issues if str(i.get("state", "")).upper() == "OPEN"]
    closed_issues = [i for i in issues if str(i.get("state", "")).upper() == "CLOSED"]
    proposal_sent = [
        i
        for i in open_issues
        if "proposal-sent" in {label["name"] for label in i.get("labels", [])}
    ]

    lines = [
        "# Lead Pipeline Report",
        "",
        f"Open leads: {len(open_issues)}",
        f"Proposal sent: {len(proposal_sent)}",
        f"Closed leads: {len(closed_issues)}",
        "",
        "| # | Title | State | Labels | URL |",
        "|---|---|---|---|---|",
    ]

    for issue in issues:
        labels = ", ".join(label["name"] for label in issue.get("labels", []))
        lines.append(
            f"| {issue['number']} | {issue['title']} | {issue['state']} | {labels} | {issue['url']} |"
        )

    lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <output-file>", file=sys.stderr)
        return 1

    output_file = Path(argv[1])
    gh_cmd = os.environ.get("GH_CMD", "gh")
    issues = fetch_issues(gh_cmd)
    report = build_report(issues)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(report)
    print(f"Wrote pipeline report to {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
