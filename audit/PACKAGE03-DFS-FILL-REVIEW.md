# DFS and flood-fill focused rewrites

Two existing original IDs, not new lessons or a replacement for the containing Graph traversal chapter. Publication receipts are separate.

Read the supplied handbook chapter 12 DFS section, printed 117–118 (PDF 127–128), both rendered pages and full text/code, plus the connectivity application principle after printed 120. Preserve the exact five-vertex graph and movement 1→2→3→5, returning before 4; its adjacency order is explicit. Native graph labels/positions/edges match the source. The original seven-vertex disconnected example and all 14 entry/exit timestamps remain intact. Flood fill is the original grid application supplement, not a claim that the source has a separate full grid chapter.

| Teaching coverage | Candidate location |
| --- | --- |
| DFS starts at a vertex, follows a branch and returns | dfs / idea, exact source graph and two states |
| Mark discovery before following edges; cycle 2–3–5 | recursion |
| Recursive suspended neighbor loop and finish after return | recursion, full event trace and explained complete small-input program |
| Safe large-graph alternative preserving exact recursive events | frames, constructor, (vertex,next-neighbor) invariant and full program |
| Disconnected components, isolated vertex, parent path and timestamps | forest, exact original seven-vertex table |
| O(n+m), stack memory and non-shortest-path/cycle caveats | forest, limits |
| Grid as implicit four-neighbor graph, no diagonal connection | flood-fill / model |
| Mark before insertion, not on removal | discovery |
| Distinct area versus geometric boundary tests | boundary; includes hole perimeter |
| All original 4×5 map cells, three components, areas3/6/4 and perimeters8/12/10 | trace: native labeled/colored grid and numerical table |
| Constructor, stack fill, row-major roots and complete C++17 | implementation |
| Reachability proof, boundary/empty dimensions and application limitations | checks, practice |

Three complete C++17 programs are explained through actual fragments before full sources in both languages. The recursive DFS is a small-input illustration only (n≤200, with platform-dependent stack caveat); the primary explicit-frame DFS is independently stress-tested on a 200000-vertex chain. A plain vertex stack may find the same reachable set but is not claimed to preserve recursive parents/timestamps. Grid fill needs only component statistics and uses a simple discovery-marked heap stack, with no deep recursion.

## Technical and editorial review

DFS timer≤2n and grid area≤10^6/perimeter≤4×10^6 fit int. Every constructor/init field is explained. No unnecessary ll or wrapper scaffolding. Frame indices advance before pushing; no reference survives vector growth. Undirected self-loops/multiedges are allowed for traversal, but the lesson does not incorrectly reuse a parent-vertex rule for multiedge cycle detection or call DFS-root counts directed SCC counts.

Flood fill bounds checks precede indexing by short-circuit evaluation. Visited open neighbors are not walls. Perimeter includes hole boundaries and satisfies P=4A−2E; a fully open rectangle, diagonal-separated cells and center-hole ring are explicit checks. Zero dimensions have no regions; no character rows are read when width is zero. The original area/perimeter goal remains rather than being reduced to Counting Rooms output only.

Read MN/EN narratives in context for causal discovery/return explanations and consistent row/column terms. Source credit remains centralized; no repetitive book/edition prose. Stable IDs, tutorial priorities, prerequisites, problem references/flags/stages, variants and next links remain exact. Core practice stays Building Roads for DFS and Counting Rooms for fill; unrelated problems are not promoted. Native graphs and grids retain text labels so color is supplementary.

Independent BFS connectivity plus parent/event invariants validate graphs; recursive and frame outputs are compared exactly on small inputs. Grid components use a BFS oracle, with perimeter computed separately by canceling geometric unit edges. Actual exhaustive/random counts, sanitizers, maximum-chain/million-cell tests, native reader/editor/order checks and protected publication evidence are in the companion files. No user acceptance, authenticated live fixture, security change or deferred feature completion is inferred.

Native fixture synchronization was tightened after a screenshot could be taken between URL assignment and the hashchange handler. It now waits for the actual active TOC link and visible target section before capture. This is a test-only race correction, not a runtime navigation change; the affected native checks are rerun and exact-public-body verification uses the same stronger condition.
