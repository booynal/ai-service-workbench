#!/usr/bin/env bash
set -euo pipefail

src="/Users/ziv/tmp/20260603/launchd/com.booynal.ai-service-workbench.plist"
target_dir="$HOME/Library/LaunchAgents"
target="$target_dir/com.booynal.ai-service-workbench.plist"

mkdir -p "$target_dir"
cp "$src" "$target"
echo "Copied $src -> $target"

if [ "${DRY_RUN:-0}" = "1" ]; then
  echo "DRY_RUN=1, skipping launchctl bootstrap"
  exit 0
fi

launchctl bootout "gui/$(id -u)" "$target" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$(id -u)" "$target"
echo "Bootstrapped $target"
