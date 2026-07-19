#!/bin/bash
# Polls every docs/*/annotations.json (3s interval) and prints one line per
# new/changed comment count, tagged with the doc slug — covers every doc in
# the hub automatically via the docs/*/ glob, no per-doc setup.
#
# Deliberately avoids bash associative arrays (declare -A) — not supported
# on bash 3.2, which is what macOS ships by default (Apple hasn't upgraded
# it since bash's GPLv3 relicense; `declare -A` silently misbehaves there
# instead of erroring, which caused this script to spam false "N -> 0"
# transitions every 3s in an earlier version). State is tracked in a plain
# "slug count" state file instead, for portability.
cd "$(dirname "$0")" || exit 1

STATE_FILE=$(mktemp)
trap 'rm -f "$STATE_FILE"' EXIT
: > "$STATE_FILE"

while true; do
  NEW_STATE=$(mktemp)
  for f in docs/*/annotations.json; do
    [ -f "$f" ] || continue
    slug=$(basename "$(dirname "$f")")
    count=$(python3 -c "import json,sys; print(len(json.load(open(sys.argv[1]))))" "$f" 2>/dev/null || echo 0)
    prev=$(awk -v s="$slug" '$1==s{print $2}' "$STATE_FILE")
    prev=${prev:-0}
    if [ "$count" != "$prev" ]; then
      echo "$slug: $prev -> $count comment(s)"
    fi
    echo "$slug $count" >> "$NEW_STATE"
  done
  mv "$NEW_STATE" "$STATE_FILE"
  sleep 3
done
