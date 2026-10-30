# Bitmask DP standalone rewrite

One existing original ID, not a new lesson or a duplicate of Bit operations/DP. Publication is separate from candidate completion.

Read the supplied Competitive Programmer’s Handbook, chapter 10 “Dynamic programming”, printed 102–106 (PDF 112–116): actual full text, all price/weight/value examples, recurrence derivations, code and rendered pages. Preserve the three source applications in their relative order, with the existing matching example first to introduce the stable lesson’s original goal. Submask enumeration is a prerequisite supplement for the final source example.

| Source teaching coverage | Candidate location |
| --- | --- |
| Subsets as integer DP states | masks |
| All 24 original prices, day/product coordinates and optimal 2+2+1=5 schedule | optimal-selection: native colored diagram |
| Day-indexed total(S,d), empty/singleton bases, skip/buy recurrence and O(days×k×2^k) | optimal-selection: complete numerical day/state table and rolling-layer implementation |
| Permutations versus subsets, 20! versus 2^20 | elevator |
| Original weights 2,3,3,5,6, capacity 10 and groups {0,2,3}/{1,4} | elevator |
| rides/last pair, example {1,3,4}→(2,5), base {1,0}, choose last person and state order | elevator: dominance argument and explained complete implementation |
| Assigned values of all eight subsets and sum({0,2})=10 | subset-sums |
| Restricted-removal partial(S,i), base −1, partial({0,2},1)=6, two-branch recurrence | subset-sums |
| Bit-outer in-place update and why the source value is still from the previous phase | subset-sums: all numeric phases and full program |

The lesson keeps source examples and intermediate reasoning, rather than merely mentioning the algorithms. Implementation gaps are filled with five complete independent C++17 programs, each preceded by its actual ordered fragments and explanations in MN/EN. Source credit remains centralized, with no repeated edition/book narration.

## Additional review and contracts

Retain the original 3×3 matching matrix, two assignments and every reachable/dead mask. Count modulo 10^9+7 with int residues; the addition of two reduced residues fits int. Other costs, weights and sums use ll. Every shift is on a bounded nonnegative int mask with at most 20 bits; selecting over up to 100 days is deliberately limited to 15 products. Positive weights fit capacity individually. Empty matching has one solution, empty selection costs zero, and empty elevator input returns zero despite the internal empty-ride base. Unreachable selection states are skipped before adding prices.

Submask enumeration explicitly processes zero before breaking, and handles s=0 exactly once. Distinguish O(2^popcount(s)) for one query, O(3^n) across all submask pairs, and O(n2^n) for SOS. SOS includes both the empty set and the full queried set; signed assigned values and v[0]≠0 are supported. Explain why swapping the outer bit loop is invalid. State practical time/memory bounds, including extra endpoint dimensions; mask width alone does not make an algorithm feasible.

Read both language narratives contextually for state meaning, causal transitions, correctness and termination. Code fragments concatenate byte-exactly to tested full programs. Native diagrams retain readable captions/values so color is supplemental. All IDs, priority, prerequisites, practice flags/stages and next/variant links remain exact. The only core practice is the already-prioritized Matching reference; group the body accordingly without promoting any problem. Apple Division and the remaining applications stay independent/extension practice.

Naive exhaustive assignment/day-choice/bin-partition/subset models and maximum-bound UBSan checks are recorded in CODE evidence. The guarded exact-one publication contract is tested locally for rollback, drift, replay, private-state preservation and Mongolia rejection. Candidate/public editor/reader evidence and final receipt establish actual checks; no owner acceptance or authenticated live-browser check is inferred. No runtime/schema/security change or deferred UI work.
