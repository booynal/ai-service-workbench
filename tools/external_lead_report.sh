#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <search-query> <output-dir>" >&2
  exit 1
fi

search_query="$1"
output_dir="$2"
mkdir -p "$output_dir"

gh_cmd="${GH_CMD:-gh}"

search_json="$(
  "$gh_cmd" search issues "$search_query" \
    --state open \
    --limit 10 \
    --json number,title,url,repository,state
)"

report_file="$output_dir/lead_report.md"

SEARCH_JSON="$search_json" python3 - <<'PY' >"$report_file"
import json
import os

items = json.loads(os.environ["SEARCH_JSON"])
print("# External Lead Report\n")
print("| Repo | Title | URL |")
print("|---|---|---|")
for item in items:
    print(f"| {item['repository']['nameWithOwner']} | {item['title']} | {item['url']} |")
PY

lead_info="$(
  SEARCH_JSON="$search_json" python3 - <<'PY'
import json
import os

items = json.loads(os.environ["SEARCH_JSON"])
if items:
    top = items[0]
    print(top["number"])
    print(top["repository"]["nameWithOwner"])
PY
)"

top_number="$(printf '%s\n' "$lead_info" | sed -n '1p')"
top_repo="$(printf '%s\n' "$lead_info" | sed -n '2p')"

if [ -n "${top_number:-}" ] && [ -n "${top_repo:-}" ]; then
  mkdir -p "$output_dir/$top_number"
  issue_file="$output_dir/$top_number/issue.md"
  "$gh_cmd" issue view "$top_number" --repo "$top_repo" --json body --jq .body >"$issue_file"
  python3 tools/issue_to_brief.py "$issue_file" "$output_dir/$top_number/brief.md"
  proposal_cmd="${PROPOSAL_LAB_CMD:-./tools/proposal_lab.sh}"
  "$proposal_cmd" "$output_dir/$top_number/brief.md" "$output_dir/$top_number/proposal.md"
fi

echo "Wrote external lead report to $report_file"
