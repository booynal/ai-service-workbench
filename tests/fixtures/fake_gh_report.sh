#!/usr/bin/env bash
set -euo pipefail

if [ "$1" = "issue" ] && [ "$2" = "list" ]; then
  cat <<'EOF'
[{"number":21,"title":"Lead A","state":"OPEN","labels":[{"name":"inbound-lead"},{"name":"client-request"}],"url":"https://example.com/21"},{"number":22,"title":"Lead B","state":"OPEN","labels":[{"name":"inbound-lead"},{"name":"client-request"},{"name":"proposal-sent"}],"url":"https://example.com/22"},{"number":23,"title":"Lead C","state":"CLOSED","labels":[{"name":"inbound-lead"},{"name":"client-request"},{"name":"proposal-sent"}],"url":"https://example.com/23"}]
EOF
  exit 0
fi

echo "unexpected gh invocation: $*" >&2
exit 1
