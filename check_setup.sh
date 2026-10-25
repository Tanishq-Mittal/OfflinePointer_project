#!/usr/bin/env bash
# Run once: ./check_setup.sh   (do the brew install parts while online)
ok(){ echo "OK   $1"; }; bad(){ echo "FAIL $1"; }
command -v osascript >/dev/null && ok osascript || bad "osascript missing (not macOS?)"
command -v jq >/dev/null && ok jq || bad "jq missing -> brew install jq (while online)"
command -v python3 >/dev/null && ok python3 || bad "python3 missing"
curl -s -m 2 http://localhost:11434/api/tags >/dev/null && ok "Ollama on localhost:11434" || bad "Ollama not running (open the Ollama app)"
osascript -e 'tell application "System Events" to get name of menu bar item 1 of menu bar 1 of process "Finder"' >/dev/null 2>&1 \
  && ok "Accessibility permission" \
  || bad "Grant Terminal: System Settings > Privacy & Security > Accessibility (and Automation), then restart Terminal"
