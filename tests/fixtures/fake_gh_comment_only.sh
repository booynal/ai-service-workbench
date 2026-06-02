#!/usr/bin/env bash
set -euo pipefail

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
  mkdir -p tmp_send_capture
  cp "$body_file" "tmp_send_capture/${issue_ref}.md"
  echo "commented ${issue_ref}"
  exit 0
fi

echo "unexpected gh invocation: $*" >&2
exit 1
