# Graph Report - OfflinePointer_Starter_Project_v2  (2026-10-25)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 59 nodes · 135 edges · 13 communities (4 shown, 9 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c6c25152`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5

## God Nodes (most connected - your core abstractions)
1. `Control` - 16 edges
2. `check_capability()` - 12 edges
3. `Result` - 9 edges
4. `find_control()` - 9 edges
5. `verify()` - 8 edges
6. `main()` - 7 edges
7. `chat()` - 6 edges
8. `_ask()` - 6 edges
9. `select_control()` - 5 edges
10. `make_shortlist()` - 5 edges

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

## Communities (13 total, 9 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.32
Nodes (7): check_capability(), test_bold_variations_are_supported(), test_center_alignment_variations_are_supported(), test_font_size_variations_are_supported(), test_italic_variations_are_supported(), test_save_variations_are_supported(), test_unsupported_requests_are_rejected()

### Community 1 - "Community 1"
Cohesion: 0.36
Nodes (5): chat(), _ask(), find_control(), _rank_controls(), PickerOutput

### Community 2 - "Community 2"
Cohesion: 0.42
Nodes (3): load_controls(), main(), select_control()

### Community 3 - "Community 3"
Cohesion: 0.62
Nodes (5): Control, Result, test_disabled_control_caption(), test_verifier_rejects_unknown_id(), verify()

## Knowledge Gaps
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Control` connect `Community 3` to `Community 0`, `Community 1`, `Community 2`, `Community 4`, `Community 5`, `Community 7`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `Control` (e.g. with `_ask()` and `find_control()`) actually correct?**
  _`Control` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Why does `check_capability()` connect `Community 0` to `Community 1`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `verify()` (e.g. with `Control` and `Result`) actually correct?**
  _`verify()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Why does `find_control()` connect `Community 1` to `Community 0`, `Community 2`, `Community 3`, `Community 5`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._