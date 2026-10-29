# Sparse table and Fenwick standalone rewrites

Two existing originals, not new lessons. Actual publication is recorded separately.

Read the supplied Competitive Programmer’s Handbook chapter 9, printed pages 85–88 (PDF 95–98), including rendered page layouts and complete prose, tables, diagrams and code. These focused tutorials supplement the already published containing Range queries chapter; no chapter number or curriculum identity is moved.

| Source coverage | Candidate location |
| --- | --- |
| Static minimum preprocessing versus all endpoint pairs | sparse-table / need |
| Every source power-of-two minimum on [1,3,4,8,6,1,4,2] | build: all four complete valid levels |
| Two-half recurrence and preprocessing cost | build |
| Source inclusive query [1,6], blocks [1,4] and [3,6], answers 3 and 1 | query: numerical table and three native highlighted arrays |
| Constant-time union of overlapping blocks | query; operation explains idempotence and gives sum/XOR counterexamples |
| Fenwick as dynamic prefixes in one array | fenwick-tree / need |
| Lowbit-defined interval ending at each 1-based index | structure: full interval table and native colored coverage diagram |
| Source tree [1,4,4,16,6,7,4,29] | need, structure |
| Prefix 7 partition and 16+7+4=27 | query: complete endpoint walk 7→6→4→0 |
| Subtract two prefix sums | query, rangeSum implementation |
| Source position-3 update affecting cells 3,4,8 | update, before/after table |
| Signed add and lowbit implementation | update, implementation, limits |

Source-facing coverage is complete for these two sections. Historical footnote narration is omitted from teaching prose; attribution stays centralized. Standalone signed/alternative numerical traces and all existing practice relationships remain. Added implementation material supplies compact size-constructed structs with real fragment explanations before full C++17 programs, integer logs, precise endpoint conversion, assignment-to-delta handling and index-zero preconditions. No one-token code placeholder, unrelated advanced structure or source-chapter duplication.

## Technical and language review

Sparse queries are nonempty, internally half-open. Powers and shifts fit the stated n≤200000 bound; values may span ll because only comparisons occur. Empty construction is supported but has no query. Unbuilt trailing cells are never read. O(1) overlapping queries rely on associative/idempotent min; the source numerical blocks sum to 21+19=40, not the actual 26. Static sum/XOR alternatives are distinguished without claiming this minimum program implements them.

Fenwick uses 1-based indices; sum(0) is valid and add(0) is explicitly forbidden, since its lowbit cannot advance. The constructor zeros n+1 cells; initial construction is honestly O(n log n). Core add accepts signed deltas, while main implements assignment and retains old values. Under n,q≤200000 and absolute assigned values≤10^9, sums≤2×10^14 and deltas≤2×10^9 fit ll. Arbitrary additive applications require separate accumulation bounds. Prefix and interval queries are not arbitrary dynamic minima or kth-element searches.

Read the MN/EN narratives in context, retaining the source sequence and causal steps. Unnecessary English “minimum” in Mongolian was replaced contextually with “хамгийн бага утга”; unavoidable technical names are explained. Math, code fragments and final programs correspond in both languages. Native diagrams label indices/intervals, so color is supplementary. IDs, tutorial priorities, prerequisites, practice IDs/flags, related/variant and next links are exact-preserved; chapter 9 stays segment-tree.

Compiled programs/independent naive oracles, local transactional failure/drift/replay guards and actual editor/reader fixtures are documented in the accompanying evidence files. Publication receipt, not this review, establishes live revisions and protected-state preservation. No owner acceptance, authenticated live visual test, new permission or deferred-feature completion is implied.
