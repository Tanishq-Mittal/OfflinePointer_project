#!/usr/bin/env bash
# read_controls() from the contract.  Usage: ./controls/read_controls.sh TextEdit > controls.json
# Output: JSON array of {id,name,role,x,y,w,h,enabled}
DIR="$(cd "$(dirname "$0")" && pwd)"
APP="${1:-TextEdit}"
# Terminal is frontmost when you type, so bring the target app forward first.
osascript -e "tell application \"$APP\" to activate" >/dev/null 2>&1
sleep 0.5
TSV=$(osascript "$DIR/read_menus.applescript" "$APP") || { echo "reader failed (Accessibility permission?)" >&2; exit 1; }
printf '%s\n' "$TSV" | jq -R -s '
  split("\n") | map(select(length > 0) | split("\t")) | unique_by(.[0])
  | to_entries
  | map({
      id: ("c" + ((.key + 1) | tostring)),
      name: .value[0],
      role: "MenuItem",
      x: (.value[2] | tonumber), y: (.value[3] | tonumber),
      w: (.value[4] | tonumber), h: (.value[5] | tonumber),
      enabled: (.value[1] == "true")
    })'
