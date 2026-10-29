# Next original batch — preparation, not completed lessons

GitHub receipt recovery is finished: preserved e063c29 and its audit correction f154d95 were pushed using the existing command-scoped gh helper, then PR165 merged as6dafe1b2fff288fd7e0372208ea230780e64a7df. No credential/config/security changes or SQL replay. The earlier CLI401 cause remains unverified. Branch for this next batch starts at that verified remote main.

## Source and identity mapping

Read full retained handbook7.2, printed70–71, and inspected rendered PDF80 (source array, arrows and per-ending lengths); PDF81 was already read for the adjacent source7.3. Preserve source[6,2,5,1,7,4,8,3], end lengths[1,1,2,1,3,2,4,2], and optimal[2,5,7,8]. Existing `lis` revision6 is an original standalone supplement to the already published full DP chapter; preserve ID, priority, prerequisite and practice109/322/693/359/349/355. Its rewrite must derive quadratic ending-state DP first, then minimum-tail dominance, binary search, strict versus nondecreasing bounds, and reconstruction. Final tails[1,3,7,8] are not an actual source subsequence; demonstrate why parent indices are necessary. Never sort the original array. Keep natural MN/EN and the confirmed terminology эрс өсөх/үл буурах.

`interval-dp` revision2 is a useful supplemental topic, not an explicit subsection of handbook chapter7. Preserve original[10,20,30,40] example,190 optimum, source-independent last-merge reasoning, stable ID, priority, dynamic-programming/prefix-sums prerequisites and practice690/81/688/350/526/673. Explain contiguous original intervals, why total interval mass is history-independent, last split, singleton base0 and increasing interval length. Add full interval table, prefix sums, exact merge-tree reconstruction and why first-adjacent-min greedy fails on[6,4,4,6](42 versus40). Nonadjacent Huffman merges solve a different problem. Do not silently teach advanced optimization/negative weights or rename the existing goal.

## Completed code foundation

Four complete compact C++17 programs plus exact ordered parts are retained in `audit/package03-work/lis-interval-*`:
- Quadratic LIS with parent reconstruction: intended teaching bound0≤n≤2000, ll comparison values in±10^18, int indices/lengths.
- Fast strict LIS with lower_bound, minimum tails/positions and saved predecessors;0≤n≤200000. Parent is recorded before replacing the current tail.
- Nondecreasing variant with upper_bound under the same bounds, independently compiled/tested rather than an unverified prose replacement.
- Adjacent merge DP in a compact owning struct with explained-constructor work pending. Intended0≤n≤400, nonnegative weights≤10^9, ll prefix/cost, int indices/cuts. INF2^60 exceeds all bounded costs. Return0 for empty input; emit original one-based l/k/r triples in postorder for nonempty input, not changing current-pile numeric positions. Explain constructor allocations/base initialization and recursion depth O(n), with environment-dependent stack caveat.

`tests/package03-lis-interval-code.py` passes all four with UBSan.1,568 arrays checked against all-index-subset optimum, including every length0..5 over{-1,0,1,2}, duplicates, empty/extreme signed values and randomized arrays. Reconstructed original indices and inequalities verified.1,469 merge cases checked against recursively enumerating the FIRST adjacent merge (independent of final-split DP), including all lengths0..5 over{0,1,2,3}; every emitted operation joins actual adjacent current original-index blocks, with exact total cost and n−1 operations. Stress: fast200000, quadratic2000, merge400; large totals exceed32 bits. No code changes followed this successful run.

## Remaining before readiness/publication

Write actual complete MN/EN native lesson candidates, explained meaningful fragments followed by these exact full programs, worked traces/tables and staged mastery/independent practice. Review Mongolian and source coverage substantively. Preserve fresh concurrent owner edits/private drafts/Mongolia/relationships/progress. Then exact-body/hash/metadata tests, actual native editor/reader math/TOC/theme/mobile checks, fresh live schema/revision/body/draft recovery guards and tested exact-pair owner SQL. Only then ready/merge/publish and verify actual public bodies; do not count this code-only preparation as lesson completion. Current original count remains30/55 with25 pending,10 additions separate. All old publication jobs, especially histories251/252, remain non-replayable; no deferred UI work or access changes.
