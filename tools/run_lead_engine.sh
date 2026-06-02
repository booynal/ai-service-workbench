#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <output-root-dir>" >&2
  exit 1
fi

output_root="$1"
mkdir -p "$output_root"

./tools/process_open_leads.sh "$output_root/leads"
python3 tools/pipeline_report.py "$output_root/pipeline_report.md"

echo "Lead engine completed in $output_root"
