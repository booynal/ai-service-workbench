#!/usr/bin/env bash
set -euo pipefail

if [ "$1" = "search" ] && [ "$2" = "issues" ]; then
  cat <<'EOF'
[{"number":101,"title":"Need automation for support ticket triage","state":"open","url":"https://github.com/example/repo/issues/101","repository":{"nameWithOwner":"example/repo"}},{"number":102,"title":"Looking for report generator help","state":"open","url":"https://github.com/example/reports/issues/102","repository":{"nameWithOwner":"example/reports"}}]
EOF
  exit 0
fi

if [ "$1" = "issue" ] && [ "$2" = "view" ]; then
  cat tests/fixtures/sample_issue.md
  exit 0
fi

echo "unexpected gh invocation: $*" >&2
exit 1
