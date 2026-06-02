#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <brief-file> <output-file>" >&2
  exit 1
fi

brief_file="$1"
output_file="$2"

mkdir -p "$(dirname "$output_file")"

{
  echo "# Fake Proposal"
  echo
  echo "Source brief:"
  echo
  cat "$brief_file"
} >"$output_file"

echo "Wrote fake proposal to $output_file"
