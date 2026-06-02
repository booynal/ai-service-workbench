#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <issue-id-or-url> <output-dir>" >&2
  exit 1
fi

issue_ref="$1"
output_dir="$2"

./tools/issue_to_proposal.sh "$issue_ref" "$output_dir"

proposal_file="$output_dir/proposal.md"
if [ ! -f "$proposal_file" ]; then
  echo "Proposal file not found: $proposal_file" >&2
  exit 1
fi

gh_cmd="${GH_CMD:-gh}"
"$gh_cmd" issue comment "$issue_ref" --repo booynal/ai-service-workbench --body-file "$proposal_file"
"$gh_cmd" issue edit "$issue_ref" --repo booynal/ai-service-workbench --add-label proposal-sent

echo "Commented proposal back to issue $issue_ref"
