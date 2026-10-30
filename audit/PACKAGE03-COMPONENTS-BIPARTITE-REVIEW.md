# Connected components and bipartite focused rewrites

Two existing original IDs, not new lessons or a replacement of the containing Graph traversal chapter. Publication evidence is separate.

Read actual supplied handbook chapter 12 “Connectivity check” and “Bipartiteness check”, printed 121–122 (PDF 131–132), including complete text and rendered diagrams. The intervening cycle-finding section is already covered in the containing chapter and is not falsely claimed as a new standalone deliverable here.

| Source/retained coverage | Candidate location |
| --- | --- |
| A single traversal reaches one undirected component, not necessarily the graph | connected-components / meaning |
| Exact source graph {1,3,4} and {2,5}; triangle edges and separate 2–5 edge | meaning, native highlighted diagram |
| Outer undiscovered-root traversal for every component | traversal, complete iterative program |
| Original seven-city {1,2,3}/{4,5,6}/{7}, sizes and representatives | trace |
| Representative construction and minimum k−1 proof, empty/single-component handling | roads |
| Two colors, forced opposite neighbors and checking already colored endpoints | bipartite / meaning |
| Exact source six-edge graph, INCLUDING edge 4–5 | meaning, source-example |
| Source DFS trace 1→2→3→5 with equal colors at 2/5 | source-example: partial-color native graph |
| Why choosing the other initial color cannot fix a conflict | source-example |
| Complete constructive coloring or failure | implementation |
| Distinction from general 3-coloring | checks |
| Original even square plus separate pair and edge 1–3 odd obstruction | disconnected |

The chosen bipartite implementation is BFS. Its source-example partial coloring exposes edge 3–5, whereas the retained source DFS trace exposes 5–2. Both partial states and the reason for their difference are explicit; the text never promises identical partial colors on an impossible graph. On a valid connected component, colors are forced up to a whole-component swap. The odd-cycle equivalence is proved in both directions using tree-path parity, including self-loops. Parallel edges repeat constraints rather than creating a spurious odd obstruction. The program does not claim to output an odd-cycle witness.

## Technical and editorial review

Both complete C++17 programs use compact reusable structs with size constructors, −1 initialization, concise fields and explained ordered fragments before full code in MN/EN. Components stores id,sz,rep; main prints only new roads, not component count. The k=0 branch does not read rep[0]. Bipartite stores −1/0/1 internally and prints 1/2 only after full success; partial failed colors are not output. Both process all components, isolated vertices and empty input conventions. Input n,m≤200000 bounds all counts/indices to int; there are no weighted sums requiring ll. Both avoid deep recursion and run in O(n+m) time/space.

Read both language narratives for logical continuity and correct conditions. In particular an already-colored neighbor of the SAME color is the conflict, not a neighbor of a different color. Connectedness is undirected; directed single-source reachability, weak components and SCCs are explicitly distinguished. Ordinary static component IDs/DSU do not automatically solve coloring, matching or dynamic parity. Existing lesson IDs, priorities, prerequisites, practice flags/stages, variants and next links remain exact. Both original core problems remain core for components; no global problem priority changes.

Native source graph labels/positions/edges were compared with actual PDF pixels. Old seven-city and square/pair examples are retained without replacing the source examples. Colors have redundant numeric/text legends. Source attribution remains centralized; no repeated book/edition narration.

Independent Floyd–Warshall reachability validates all pairs of component IDs, sizes and representatives; printed roads are actually added and checked for connectivity/minimal count. Brute-force all 2^n assignments independently validates bipartite feasibility, while each successful coloring is checked edge by edge. Exhaustive/random small cases and large closed-form chains/even/odd cycles/isolated graphs are recorded with UBSan evidence. Native reader/editor, ordering and exact-pair publication tests establish compatibility, rollback and preservation; the final receipt establishes real publication. No owner acceptance, authenticated live-user fixture, security change or deferred UI feature is inferred.

Final rendered review distinguished literal C++ unassigned tests from mathematical notation: id/col conditions use native inline-code marks in both languages, avoiding a split math fragment inside a code token. The affected model/SQL tests and native MN/EN fixtures were rerun on the final body. Earlier prepared SQL was superseded before submission; no publication job was replayed.
