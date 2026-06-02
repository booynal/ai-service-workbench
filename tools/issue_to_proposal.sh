#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <issue-file> <output-dir>" >&2
  exit 1
fi

issue_file="$1"
output_dir="$2"

if [ ! -f "$issue_file" ]; then
  echo "Issue file not found: $issue_file" >&2
  exit 1
fi

mkdir -p "$output_dir"

issue_copy="$output_dir/issue.md"
brief_file="$output_dir/brief.md"
proposal_file="$output_dir/proposal.md"

cp "$issue_file" "$issue_copy"

python3 tools/issue_to_brief.py "$issue_copy" "$brief_file"

proposal_cmd="${PROPOSAL_LAB_CMD:-./tools/proposal_lab.sh}"
"$proposal_cmd" "$brief_file" "$proposal_file"

echo "Issue saved to $issue_copy"
echo "Brief saved to $brief_file"
echo "Proposal saved to $proposal_file"
