# Handbook curriculum reconciliation — 2026-10-29

Original read-only audit of the fresh anonymous65-lesson catalog and successful publication receipts, now updated with verified search publications PR156 and single-target PR158. Only those four target bodies/history changed; no private draft/learner/problem/access change. Mongolia remains excluded; no private draft bodies were inspected by this audit.

55 originals =25 newly rewritten +30 still pre-handbook standalone bodies. Ten separate additions yield65 public lessons;66 stored including the last-verified excluded Mongolia. **The counts are consistent.** All 35 rewritten/new live bodies exactly match their latest successful receipts. All 30 remaining bodies exactly match the pre-Introduction recovery snapshot: concept coverage elsewhere has not rewritten these IDs. Previous package2 quality work is historical, not new-cycle credit.

## The 25 rewritten original IDs

| Stable ID | Live revision | Source chapter | Latest matching receipt |
|---|---:|---:|---|
| `complexity` | 12 | 2 | [PACKAGE03-DIRECT-TEACHING-PUBLICATION-RECEIPT.json](PACKAGE03-DIRECT-TEACHING-PUBLICATION-RECEIPT.json) |
| `sorting` | 9 | 3 | [PACKAGE03-DIRECT-TEACHING-PUBLICATION-RECEIPT.json](PACKAGE03-DIRECT-TEACHING-PUBLICATION-RECEIPT.json) |
| `binary-search` | 9 | 3 | [PACKAGE03-SEARCH-PUBLICATION-RECEIPT.json](PACKAGE03-SEARCH-PUBLICATION-RECEIPT.json) |
| `lower-bound` | 3 | 3 | [PACKAGE03-SEARCH-PUBLICATION-RECEIPT.json](PACKAGE03-SEARCH-PUBLICATION-RECEIPT.json) |
| `upper-bound` | 3 | 3 | [PACKAGE03-SEARCH-PUBLICATION-RECEIPT.json](PACKAGE03-SEARCH-PUBLICATION-RECEIPT.json) |
| `binary-search-answer` | 5 | 3 | [PACKAGE03-ANSWER-PUBLICATION-RECEIPT.json](PACKAGE03-ANSWER-PUBLICATION-RECEIPT.json) |
| `set-map` | 6 | 4 | [PACKAGE03-DIRECT-TEACHING-PUBLICATION-RECEIPT.json](PACKAGE03-DIRECT-TEACHING-PUBLICATION-RECEIPT.json) |
| `brute-force` | 5 | 5 | [PACKAGE03-DIRECT-TEACHING-PUBLICATION-RECEIPT.json](PACKAGE03-DIRECT-TEACHING-PUBLICATION-RECEIPT.json) |
| `greedy` | 9 | 6 | [PACKAGE03-GREEDY-PUBLICATION-RECEIPT.json](PACKAGE03-GREEDY-PUBLICATION-RECEIPT.json) |
| `dynamic-programming` | 9 | 7 | [PACKAGE03-DOMINO-PUBLICATION-RECEIPT.json](PACKAGE03-DOMINO-PUBLICATION-RECEIPT.json) |
| `two-pointers` | 7 | 8 | [PACKAGE03-AMORTIZED-PUBLICATION-RECEIPT.json](PACKAGE03-AMORTIZED-PUBLICATION-RECEIPT.json) |
| `segment-tree` | 7 | 9 | [PACKAGE03-RANGE-PUBLICATION-RECEIPT.json](PACKAGE03-RANGE-PUBLICATION-RECEIPT.json) |
| `bit-operations` | 6 | 10 | [PACKAGE03-BITS-PUBLICATION-RECEIPT.json](PACKAGE03-BITS-PUBLICATION-RECEIPT.json) |
| `graph-basics` | 5 | 11 | [PACKAGE03-GRAPHS-PUBLICATION-RECEIPT.json](PACKAGE03-GRAPHS-PUBLICATION-RECEIPT.json) |
| `bfs` | 7 | 12 | [PACKAGE03-TRAVERSAL-PUBLICATION-RECEIPT.json](PACKAGE03-TRAVERSAL-PUBLICATION-RECEIPT.json) |
| `dijkstra` | 7 | 13 | [PACKAGE03-SHORTEST-PUBLICATION-RECEIPT.json](PACKAGE03-SHORTEST-PUBLICATION-RECEIPT.json) |
| `tree-basics` | 5 | 14 | [PACKAGE03-TREES-PUBLICATION-RECEIPT.json](PACKAGE03-TREES-PUBLICATION-RECEIPT.json) |
| `kruskal` | 5 | 15 | [PACKAGE03-SPANNING-PUBLICATION-RECEIPT.json](PACKAGE03-SPANNING-PUBLICATION-RECEIPT.json) |
| `topological-sort` | 8 | 16 | [PACKAGE03-DIRECTED-PUBLICATION-RECEIPT.json](PACKAGE03-DIRECTED-PUBLICATION-RECEIPT.json) |
| `lca` | 7 | 18 | [PACKAGE03-TREE-QUERY-PUBLICATION-RECEIPT.json](PACKAGE03-TREE-QUERY-PUBLICATION-RECEIPT.json) |
| `number-theory` | 7 | 21 | [PACKAGE03-NUMBER-PUBLICATION-RECEIPT.json](PACKAGE03-NUMBER-PUBLICATION-RECEIPT.json) |
| `combinatorics` | 7 | 22 | [PACKAGE03-COMBINATORICS-PUBLICATION-RECEIPT.json](PACKAGE03-COMBINATORICS-PUBLICATION-RECEIPT.json) |
| `kmp` | 7 | 26 | [PACKAGE03-STRINGS-PUBLICATION-RECEIPT.json](PACKAGE03-STRINGS-PUBLICATION-RECEIPT.json) |
| `string-hashing` | 3 | 26 | [PACKAGE03-STRINGS-PUBLICATION-RECEIPT.json](PACKAGE03-STRINGS-PUBLICATION-RECEIPT.json) |
| `lazy-segment-tree` | 7 | 28 | [PACKAGE03-SEGREVISIT-PUBLICATION-RECEIPT.json](PACKAGE03-SEGREVISIT-PUBLICATION-RECEIPT.json) |

## The 30 remaining originals — preserve every ID

“Covered by” identifies already published concepts, not completion of the standalone rewrite. Each body was inspected for its current goal/section structure; this bounded inventory is not a new complete semantic/code review.

| Stable ID | Live revision | Source mapping / covered by | Standalone work still needed |
|---|---:|---|---|
| `stack-queue` | 4 | 4.5 → `set-map#other-structures` | LIFO/FIFO focused usage and pop/empty semantics; keep both containers distinct. |
| `priority-queue` | 4 | 4.5 → `set-map#other-structures` | Heap selection and room-allocation application; not a sorted sequence. |
| `recursion` | 4 | 5.1–5.4 → `brute-force#subsets` | Recursion/call-return foundation with Hanoi supplement; source generation/backtracking gives broader context. |
| `grid-dp` | 4 | 7.3 → `dynamic-programming#grid` | Source maximum-sum path plus existing obstacle-path counting; distinguish recurrence/objective. |
| `knapsack` | 6 | 7.4 → `dynamic-programming#knapsack` | Source subset-sum/variants plus useful existing 0/1 maximum-value goal; update direction/base states. |
| `lis` | 6 | 7.2 → `dynamic-programming#lis` | Source LIS derivation plus tails/reconstruction extension; strictly increasing vs non-decreasing. |
| `interval-dp` | 2 | supplement to 7 → `dynamic-programming` | Adjacent-merge interval DP is useful existing supplemental material, not an explicit chapter 7 subsection. |
| `sliding-window` | 2 | 8.1/8.3 → `two-pointers#two-pointers` | Keep positive-sum counting and connect to minimum/deque; positivity is essential. |
| `monotonic-stack` | 6 | 8.2 → `two-pointers#nearest-smaller` | Nearest-smaller source versus existing next-greater application; explain inequality/tie choices. |
| `prefix-sums` | 6 | 9.1 → `segment-tree#static` | Static sums and source examples; still old standalone body despite displayed chapter 9 number. |
| `prefix-sums-2d` | 4 | 9.1 → `segment-tree#static` | 2D source inclusion-exclusion plus existing rectangle queries; derive all four terms. |
| `hash-compression` | 6 | 9.4 → `segment-tree#additional` | Coordinate compression with sorted unique ranks, preserving order but not distance; currently early beside Sorting. |
| `difference-array` | 4 | 9.4 → `segment-tree#additional` | Difference representation/range-add and reconstruction; preserve boundaries and signed updates. |
| `sparse-table` | 6 | 9.1 → `segment-tree#static` | Static RMQ, power-of-two blocks/idempotence; distinguish sum queries and no updates. |
| `fenwick-tree` | 6 | 9.2 → `segment-tree#fenwick` | Compact struct/size constructor, index domains, low bit, sums/updates; focused worked trace. |
| `bitmask-dp` | 6 | 10.5 (+7) → `bit-operations#dp` | Subset-state DP/assignment existing goal versus source subset transitions; no credit from concept overlap alone. |
| `dfs` | 6 | 12.1 → `bfs#depth-first` | DFS entry/exit and explicit call-frame stack; retain robust iterative deep-graph application. |
| `flood-fill` | 6 | 12.1–12.3 supplement → `bfs#applications` | Implicit grid graph/four-neighbor connectivity extension; preserve its actual movement contract. |
| `connected-components` | 2 | 12.3 → `bfs#applications` | Traverse every unvisited root, components and minimum connecting-edge argument. |
| `bipartite` | 2 | 12.3 → `bfs#applications` | Two-coloring/odd-cycle criterion; not matching, handle disconnected/self-loop cases. |
| `bellman-ford` | 2 | 13.1 → `dijkstra#bellman-ford` | Focused negative-cycle influence/reachability supplements full chapter; preserve affected-target semantics. |
| `floyd-warshall` | 4 | 13.3 → `dijkstra#floyd` | All-pairs intermediate-vertex invariant, unreachable and parallel edges, negative-cycle conditions. |
| `tree-dp` | 2 | 14.1/14.3 supplement → `tree-basics#traversal` | Existing independent-set counting is supplemental; connect to subtree states and reroot/all-longest paths without dropping its goal. |
| `dsu` | 6 | 15.2 → `kruskal#dsu` | Compact struct with par[i]=i, sz[i]=1, constructor, compression and union by size. |
| `gcd` | 4 | 21.1/21.3 → `number-theory` | Euclidean gcd plus extended-Euclidean connection; retain zero/numeric contracts. |
| `sieve` | 4 | 21.1 → `number-theory` | Prime/SPF preprocessing and factorization, start-at-square/bounds and actual complexity. |
| `fast-power` | 4 | 21.2 (+23.1) → `number-theory` | Binary modular exponentiation and theorem preconditions; indices/exponents/products typed deliberately. |
| `invariant` | 2 | methodology supplement; no source subsection → `greedy` | Existing smallest-unformable-sum proof; source correctness reasoning as benchmark, not invented chapter. |
| `debugging` | 2 | methodology supplement; no full source stress-test subsection → `introduction` | Counterexamples/oracles/sanitizers and existing broken-prefix example; preserve useful extra teaching. |
| `subtask-strategy` | 2 | 5.5 plus contest-methodology supplement → `brute-force#meet-in-the-middle` | Source meet-in-the-middle plus existing subtask strategy; not a claim the source has a whole subtask chapter. |

## Ten published additions

| ID | Revision | Chapter | Matching receipt |
|---|---:|---:|---|
| `introduction` | 2 | 1 | [PACKAGE03-DIRECT-TEACHING-PUBLICATION-RECEIPT.json](PACKAGE03-DIRECT-TEACHING-PUBLICATION-RECEIPT.json) |
| `scc` | 1 | 17 | [PACKAGE03-SCC-PUBLICATION-RECEIPT.json](PACKAGE03-SCC-PUBLICATION-RECEIPT.json) |
| `paths-circuits` | 1 | 19 | [PACKAGE03-PATHS-PUBLICATION-RECEIPT.json](PACKAGE03-PATHS-PUBLICATION-RECEIPT.json) |
| `flows-cuts` | 1 | 20 | [PACKAGE03-FLOWS-PUBLICATION-RECEIPT.json](PACKAGE03-FLOWS-PUBLICATION-RECEIPT.json) |
| `matrices` | 1 | 23 | [PACKAGE03-MATRICES-PUBLICATION-RECEIPT.json](PACKAGE03-MATRICES-PUBLICATION-RECEIPT.json) |
| `probability` | 1 | 24 | [PACKAGE03-PROBABILITY-PUBLICATION-RECEIPT.json](PACKAGE03-PROBABILITY-PUBLICATION-RECEIPT.json) |
| `game-theory` | 1 | 25 | [PACKAGE03-GAME-PUBLICATION-RECEIPT.json](PACKAGE03-GAME-PUBLICATION-RECEIPT.json) |
| `sqrt-algorithms` | 1 | 27 | [PACKAGE03-SQRT-PUBLICATION-RECEIPT.json](PACKAGE03-SQRT-PUBLICATION-RECEIPT.json) |
| `geometry` | 1 | 29 | [PACKAGE03-GEOMETRY-PUBLICATION-RECEIPT.json](PACKAGE03-GEOMETRY-PUBLICATION-RECEIPT.json) |
| `sweep-line` | 1 | 30 | [PACKAGE03-SWEEP-PUBLICATION-RECEIPT.json](PACKAGE03-SWEEP-PUBLICATION-RECEIPT.json) |

## Requested additions and extensions — actual state

| Requirement | Status | Evidence and remaining scope |
|---|---|---|
| sweep/offline queries | covered | `sweep-line; sqrt-algorithms#mo; lca#offline-lca`. Events/Fenwick, Mo and guarded offline tree applications are published; no extra generic duplicate needed. |
| SCC | covered | `scc#kosaraju`. Full Kosaraju and applications published. |
| bridges/articulation | pending | `no public lesson/implementation`. Backlog bridges-articulation only. Directed DP low[] keyword hits are path-length bounds, not low-link bridges. |
| Euler paths | covered | `paths-circuits#euler`. Full directed/undirected Euler implementation and source applications. |
| functional graphs | covered | `topological-sort#successor and #cycle`. Read successor-jump and Floyd/visited cycle programs; a separate new top-level duplicate is unnecessary. |
| matching/flow/mincut | covered | `flows-cuts#flow,#matching,#covers`. Actual maxflow/mincut, matching and applications present; old network-flow/bipartite-matching backlog labels are stale duplicates. |
| 2-SAT | covered | `scc#2sat`. Actual clause/implication/SCC-assignment teaching and full program, not a passing mention. |
| HLD | pending | `no public ID/title/body HLD match`. heavy-light-decomposition is a backlog entry only. Existing LCA path queries are static binary lifting, not HLD. |
| centroid decomposition | pending | `no public lesson/body coverage`. centroid-decomposition backlog only. |
| digit DP | pending | `no public lesson/body coverage`. digit-dp backlog only; subset/profile DP is different. |
| DP optimizations | pending | `no substantial published optimization algorithm`. interval-dp has a future heading only; grouped focused addition still needed. Do not turn every old advanced backlog item into a mandatory new lesson. |
| trie/Aho | partial | `kmp#trie published; Aho absent`. Basic trie has four explained/full code blocks; Aho failure links/multipattern matching unimplemented. |
| geometry | covered | `geometry`. Complete chapter 29 published. |
| game theory | covered | `game-theory`. Complete chapter 25 published. |
| interactive/communication tutorial | pending | `introduction#input-output contains flushing caveat only`. Problem-bank classifications/imports are complete historical work, not a substitute for the requested tutorial. |
| suffix array/LCP | pending | `no suffix-array lesson or construction program`. kmp#hashing has general substring LCP comparison; it is not a suffix array or Kasai adjacent-LCP algorithm. |
| Z function | covered | `kmp#z`. Actual Z implementation and examples already published; do not republish just to create an extra ID. |
| KMP/prefix function extension | covered | `kmp#prefix-kmp`. Four code blocks incl explained complete prefix/KMP program. |
| rolling hash extension | covered | `kmp#hashing; string-hashing#rolling/#palindrome`. Actual rolling/substrings/palindrome implementations with honest collision limitations. |
| LCA-first / binary jump static paths | covered | `lca#lca-first → #ancestors → #static-paths`. Actual min/max/sum for edge/vertex values, single LCA inclusion, static/no-update and directional caveats read. |

## Visible ordering and bookkeeping

The 118-entry source-subtopic ledger had stale unfinished statuses for chapters18–23 and 27–30, plus an intermediate DP revision. Its publication fields are now reconciled locally to current containing-topic IDs/revisions/hashes/receipts. This fixes bookkeeping only; it does not mark any of the 30 focused originals rewritten.

All 30 chapter labels occur in increasing handbook order, Introduction first. Focused extras use “Нэмэлт”, not invented chapter numbers. The fresh-catalog native reader test checks actual listing, numbering, explicit priority sort/filter and 390/1200px layouts; deployed order/runtime/curriculum bytes match cache75 under normal TLS. These are local native and deployed-file checks, not a certificate-bypassed live-browser claim.

Confirmed issue: chapter 9 number currently belongs to old `prefix-sums`, while the complete Range queries lesson is `segment-tree` and is labeled supplementary. Fix later by moving only the chapter-number mapping and containing-first9-cluster order; preserve both IDs, content/progress and explicit sort controls. No runtime fix in this audit.

`binary-search-answer` retains its existing Greedy prerequisite and post-Greedy supplement placement after review. Full source3.3 is already in Sorting, so no prerequisite is moved behind its dependent lesson. Compression beside Sorting is defensible, with a9.4 cross-link. Methodology lessons remain unnumbered after the book. New HLD/centroid/etc should be unnumbered near prerequisites, not chapters31 onward.

Backlog placeholders are not a completion ledger: network-flow/bipartite-matching, Mo/offline and persistent trees already have real containing-section implementations. Reconcile their labels later rather than create duplicate lessons. In particular a `low` length array in Directed graphs is NOT bridge low-link, generic substring LCP is NOT suffix-array/LCP, and an I/O flush caveat is NOT a complete interactive/communication lesson.

## Prioritized continuation — handbook order

| Batch | Order | Existing IDs | Plan |
|---|---|---|---|
| A | 3 Sorting supplements | Complete | All four focused originals published. Do not repeat them or Sorting. |
| B | 4 Containers | `stack-queue`, `priority-queue` | Use 4.5 plus room-allocation application, no wholesale set-map rewrite. |
| C | 5 Complete-search foundation | `recursion` | Use 5.1–5.4; keep useful call-return/Hanoi example. |
| D | 7 DP supplements | `grid-dp`, `knapsack`, `lis`, `interval-dp` | Preserve goal-specific extensions; digit-DP/grouped DP optimizations remain explicit supplementary additions. |
| E | 8 Amortized techniques | `sliding-window`, `monotonic-stack` | Connect source 8.1–8.3 and preserve distinct existing problem contracts. |
| F | 9 Range-query supplements | `prefix-sums`, `prefix-sums-2d`, `hash-compression`, `difference-array`, `sparse-table`, `fenwick-tree` | Correct chapter 9 containing-topic numbering via a separately tested narrow software change; retain all focused IDs and their own progress. |
| G | 10 Subset-state DP | `bitmask-dp` | Tie masks/state transitions to 10.5, preserve assignment application. |
| H | 12 Traversal supplements | `dfs`, `flood-fill`, `connected-components`, `bipartite` | Bridge/articulation supplement follows DFS; no new duplicate component basics. |
| I | 13 Shortest-path supplements | `bellman-ford`, `floyd-warshall` | Preserve useful target-negative-cycle and all-pairs contracts. |
| J | 14 Tree DP | `tree-dp` | Keep independent-set goal and align subtree reasoning; later HLD/centroid supplements beside14/18. |
| K | 15 Union-find | `dsu` | Apply constructor/init/struct style and existing component-size practice. |
| L | 21 Arithmetic supplements | `gcd`, `sieve`, `fast-power` | Align21.1–21.3 without repeating whole number-theory. |
| M | 26 Explicit string additions | Explicit additions only | Suffix-array/LCP and Aho as focused supplements; Z/KMP/rolling hash are done, no duplicate lessons. |
| N | Unnumbered contest/methodology supplements | `invariant`, `debugging`, `subtask-strategy` | Keep clearly supplemental, with relevant book links. Interactive/communication teaching is a separate modest supplement. |

**Next concrete batch:** `stack-queue` and `priority-queue`. Use source4.5 and retain distinct LIFO/FIFO/heap rules and useful room-allocation practice. Keep natural MN/EN, compact explained C++17, native roundtrips and fresh guarded publication. All four search originals are complete; do not replay their SQL.

Remaining focused new groups: bridges/articulation; HLD; centroid decomposition; digit DP; grouped DP optimizations; Aho; suffix array with adjacent LCP; interactive/communication. Place according to prerequisites. Z, KMP, rolling hash, functional graphs,2SAT, matching/flow, Euler and static binary lifting are already substantively covered. Do not add duplicate top-level lessons.

Book chapter 30 is final; no next numbered chapter. All 30 originals plus explicit requested additions still need tracked execution, and package3 is not complete. No package5, deferred progress/profile UI, problem statements/editorials, security expansion or approval review. Every future completed unit still needs real bilingual teaching review, correct compact CP code, native editor/reader checks and fresh guarded publication; source attribution stays centralized.

Machine-readable identities, hashes, receipt links, mapping and bounds: [PACKAGE03-CURRICULUM-RECONCILIATION.json](PACKAGE03-CURRICULUM-RECONCILIATION.json).
