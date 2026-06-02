#!/usr/bin/env bash
set -euo pipefail

target="$HOME/Library/LaunchAgents/com.booynal.ai-service-workbench.plist"

if [ "${DRY_RUN:-0}" != "1" ] && [ -f "$target" ]; then
  launchctl bootout "gui/$(id -u)" "$target" >/dev/null 2>&1 || true
fi

rm -f "$target"
echo "Removed $target"
