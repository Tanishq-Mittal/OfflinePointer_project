#!/usr/bin/env bash
# Khushi's own bash stub so main.sh works before Mohit's find_control lands.
# Usage: stub_find.sh "request" controls.json  -> prints a Result JSON
REQ="$1"; FILE="$2"
jq --arg q "$REQ" '
  ($q | ascii_downcase | split(" ") | map(select(length > 2))) as $w
  | map(. as $c | $c + {s: ([$w[] | . as $x | select($c.name | ascii_downcase | contains($x))] | length)})
  | sort_by(-.s) as $r
  | if ($r[0].s // 0) == 0
    then {status:"not_found", control_id:null, confidence:0, candidates:[], model_used:"stub", latency_ms:0, tokens_per_sec:0}
    else {status:"ok", control_id:$r[0].id, confidence:0.5, candidates:($r[:3] | map(.id)), model_used:"stub", latency_ms:0, tokens_per_sec:0}
    end' "$FILE"
