# Graph Report - OfflinePointer_project  (2026-10-25)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 78 nodes · 160 edges · 15 communities (5 shown, 10 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 9 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `96e2a6a8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 7
- Community 8
- Community 9

## God Nodes (most connected - your core abstractions)
1. `Control` - 17 edges
2. `check_capability()` - 12 edges
3. `Result` - 9 edges
4. `main()` - 9 edges
5. `find_control()` - 9 edges
6. `verify()` - 8 edges
7. `read_live()` - 7 edges
8. `chat()` - 6 edges
9. `_ask()` - 6 edges
10. `read_fixture()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `_ask()` --uses--> `Control`  [INFERRED]
  agents/picker.py → core/types.py
- `find_control()` --uses--> `Control`  [INFERRED]
  agents/picker.py → core/types.py
- `_rank_controls()` --uses--> `Control`  [INFERRED]
  agents/picker.py → core/types.py
- `read_fixture()` --uses--> `Control`  [INFERRED]
  controls/reader.py → core/types.py
- `main()` --uses--> `Control`  [INFERRED]
  main.py → core/types.py

## Import Cycles
- None detected.

## Communities (15 total, 10 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.22
Nodes (6): read_fixture(), main(), point(), read_live(), make_shortlist(), test_shortlist_keeps_all_when_small()

### Community 1 - "Community 1"
Cohesion: 0.26
Nodes (8): chat(), _ask(), find_control(), _rank_controls(), load_controls(), main(), select_control(), PickerOutput

### Community 2 - "Community 2"
Cohesion: 0.32
Nodes (7): check_capability(), test_bold_variations_are_supported(), test_center_alignment_variations_are_supported(), test_font_size_variations_are_supported(), test_italic_variations_are_supported(), test_save_variations_are_supported(), test_unsupported_requests_are_rejected()

### Community 3 - "Community 3"
Cohesion: 0.45
Nodes (5): Control, Result, test_disabled_control_caption(), test_verifier_rejects_unknown_id(), verify()

### Community 4 - "Community 4"
Cohesion: 0.83
Nodes (3): bad(), ok(), check_setup.sh script

## Knowledge Gaps
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Control` connect `Community 3` to `Community 0`, `Community 1`, `Community 2`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Control` (e.g. with `_ask()` and `find_control()`) actually correct?**
  _`Control` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Why does `check_capability()` connect `Community 2` to `Community 1`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Why does `find_control()` connect `Community 1` to `Community 0`, `Community 2`, `Community 3`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._