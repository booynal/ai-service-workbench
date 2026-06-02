#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <issue-file-or-issue-id> <output-dir>" >&2
  exit 1
fi

issue_input="$1"
output_dir="$2"

mkdir -p "$output_dir"

issue_copy="$output_dir/issue.md"
brief_file="$output_dir/brief.md"
proposal_file="$output_dir/proposal.md"

if [ -f "$issue_input" ]; then
  cp "$issue_input" "$issue_copy"
else
  gh_cmd="${GH_CMD:-gh}"
  "$gh_cmd" issue view "$issue_input" --repo booynal/ai-service-workbench --json body --jq .body >"$issue_copy"
fi

python3 tools/issue_to_brief.py "$issue_copy" "$brief_file"

proposal_cmd="${PROPOSAL_LAB_CMD:-./tools/proposal_lab.sh}"
"$proposal_cmd" "$brief_file" "$proposal_file"

echo "Issue saved to $issue_copy"
echo "Brief saved to $brief_file"
echo "Proposal saved to $proposal_file"
