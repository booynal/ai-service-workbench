#!/usr/bin/env bash
set -euo pipefail

if [ "$1" = "issue" ] && [ "$2" = "list" ]; then
  cat <<'EOF'
[{"number":11,"labels":[{"name":"inbound-lead"},{"name":"client-request"}]},{"number":12,"labels":[{"name":"inbound-lead"},{"name":"client-request"},{"name":"proposal-sent"}]}]
EOF
  exit 0
fi

if [ "$1" = "issue" ] && [ "$2" = "view" ]; then
  cat tests/fixtures/sample_issue.md
  exit 0
fi

if [ "$1" = "issue" ] && [ "$2" = "comment" ]; then
  issue_ref="$3"
  shift 3
  body_file=""
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --body-file)
        body_file="$2"
        shift 2
        ;;
      *)
        shift 1
        ;;
    esac
  done
  mkdir -p tmp_batch_capture
  cp "$body_file" "tmp_batch_capture/${issue_ref}.md"
  echo "commented ${issue_ref}"
  exit 0
fi

if [ "$1" = "issue" ] && [ "$2" = "edit" ]; then
  issue_ref="$3"
  shift 3
  label=""
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --add-label)
        label="$2"
        shift 2
        ;;
      *)
        shift 1
        ;;
    esac
  done
  mkdir -p tmp_batch_capture
  printf '%s\n' "$label" > "tmp_batch_capture/${issue_ref}.label"
  echo "edited ${issue_ref}"
  exit 0
fi

echo "unexpected gh invocation: $*" >&2
exit 1
