#!/usr/bin/env bash
set -euo pipefail

if [ "$1" = "issue" ] && [ "$2" = "list" ]; then
  state="open"
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --state)
        state="$2"
        shift 2
        ;;
      *)
        shift 1
        ;;
    esac
  done

  if [ "$state" = "open" ]; then
    cat <<'EOF'
[{"number":31,"title":"Lead X","state":"OPEN","labels":[{"name":"inbound-lead"},{"name":"client-request"}],"url":"https://example.com/31"},{"number":32,"title":"Lead Y","state":"OPEN","labels":[{"name":"inbound-lead"},{"name":"client-request"},{"name":"proposal-sent"}],"url":"https://example.com/32"}]
EOF
  else
    cat <<'EOF'
[{"number":31,"title":"Lead X","state":"OPEN","labels":[{"name":"inbound-lead"},{"name":"client-request"}],"url":"https://example.com/31"},{"number":32,"title":"Lead Y","state":"OPEN","labels":[{"name":"inbound-lead"},{"name":"client-request"},{"name":"proposal-sent"}],"url":"https://example.com/32"},{"number":33,"title":"Lead Z","state":"CLOSED","labels":[{"name":"inbound-lead"},{"name":"client-request"},{"name":"proposal-sent"}],"url":"https://example.com/33"}]
EOF
  fi
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
  mkdir -p tmp_engine_capture
  cp "$body_file" "tmp_engine_capture/${issue_ref}.md"
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
  mkdir -p tmp_engine_capture
  printf '%s\n' "$label" > "tmp_engine_capture/${issue_ref}.label"
  echo "edited ${issue_ref}"
  exit 0
fi

echo "unexpected gh invocation: $*" >&2
exit 1
