#!/bin/bash
# Polls every docs/*/annotations.json (3s interval) and prints one line per
# new/changed comment count, tagged with the doc slug — covers every doc in
# the hub automatically via the docs/*/ glob, no per-doc setup.
cd "$(dirname "$0")" || exit 1

declare -A last_counts

while true; do
  for f in docs/*/annotations.json; do
    [ -f "$f" ] || continue
    slug=$(basename "$(dirname "$f")")
    count=$(python3 -c "import json,sys; print(len(json.load(open(sys.argv[1]))))" "$f" 2>/dev/null || echo 0)
    prev="${last_counts[$slug]:-0}"
    if [ "$count" != "$prev" ]; then
      echo "$slug: $prev -> $count comment(s)"
      last_counts[$slug]=$count
    fi
  done
  sleep 3
done
