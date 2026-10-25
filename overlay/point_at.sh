#!/usr/bin/env bash
# point_at(control, caption).  Usage: point_at.sh X Y W H "caption"
DIR="$(cd "$(dirname "$0")" && pwd)"
X="$1"; Y="$2"; W="$3"; H="$4"; CAPTION="${5:-}"
CX=$(awk -v x="$X" -v w="$W" 'BEGIN{print x + w/2}')
CY=$(awk -v y="$Y" -v h="$H" 'BEGIN{print y + h/2}')
osascript -l JavaScript "$DIR/fly.js" "$CX" "$CY"
[ -n "$CAPTION" ] && osascript -e 'on run argv' -e 'display notification (item 1 of argv) with title "OfflinePointer"' -e 'end run' "$CAPTION"
[ "${SPEAK:-0}" = 1 ] && say "$CAPTION" &
exit 0
