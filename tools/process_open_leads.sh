#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <output-root-dir>" >&2
  exit 1
fi

output_root="$1"
mkdir -p "$output_root"

gh_cmd="${GH_CMD:-gh}"

issue_json="$(
  "$gh_cmd" issue list \
    --repo booynal/ai-service-workbench \
    --state open \
    --json number,labels
)"

issue_numbers_file="$(mktemp)"
trap 'rm -f "$issue_numbers_file"' EXIT

ISSUE_JSON="$issue_json" python3 - <<'PY' >"$issue_numbers_file"
import json
import os

issues = json.loads(os.environ["ISSUE_JSON"])
for issue in issues:
    labels = {label["name"] for label in issue.get("labels", [])}
    if "proposal-sent" not in labels:
        print(issue["number"])
PY

while IFS= read -r issue_number; do
  [ -n "$issue_number" ] || continue
  ./tools/issue_to_proposal_and_comment.sh "$issue_number" "$output_root/$issue_number"
done <"$issue_numbers_file"
