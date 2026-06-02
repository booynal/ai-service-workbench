#!/usr/bin/env bash
set -euo pipefail

if [ "$1" != "issue" ] || [ "$2" != "view" ]; then
  echo "unexpected gh invocation: $*" >&2
  exit 1
fi

cat tests/fixtures/sample_issue.md
