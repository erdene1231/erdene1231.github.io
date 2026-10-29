# Chapter 18: Tree queries

Existing `lca`, expected live revision 6. This is one original-55 rewrite, not a new lesson. Publication is pending until the receipt records the verified result. No other lesson ID, priority, prerequisites, practice mapping or private draft is changed.

## Actual source coverage and deliberate order

Uploaded Competitive Programmer’s Handbook, chapter 18, printed pages 163–172 (PDF pages 173–182), full text and all ten rendered pages inspected. The user's explicit LCA-first teaching order takes precedence over the source's ancestor-first order. Source/edition provenance stays in this audit; the reader contains direct teaching, with the central Tutorials acknowledgment unchanged.

- First: LCA meaning, deepest common ancestor, original eight-vertex example, ancestor/equal/root cases.
- 18.1: distinct ancestor-example labeling, both original ancestor queries, complete 1/2/4-step table, naive O(k), binary decomposition, recurrence, preprocessing/query bounds, missing ancestors. Added complete BinaryJump program.
- Requested extension: static edge and vertex path min/max/sum, disjoint lifting intervals, LCA once, empty edge paths, negative weights, prefix alternative, static-only limitation, order-sensitive aggregate caveat. Added complete PathJump program.
- 18.2: exact nine-vertex DFS order, sizes and values, original subtree-4 sum 11. The root-path illustration explicitly uses its different source values: root-to-7 sum 14; original before/after path arrays, four descendants affected by increasing vertex 4. Fenwick point/range difference reasoning and complete dynamic program.
- 18.3: depth alignment 8→6, both endpoints then meeting at 2, invariant and logarithmic lifting. Full repeated Euler tour, all 15 entries/depths, first positions 2/5 and minimum at position 3. RMQ reasoning, sparse-table overlap condition, complete EulerLCA program, original depth-1 distance example and explicit depth-0 code equivalence.
- 18.4: online/offline distinction, exact frequency maps for vertex 4 and its three children, small-to-large merge, meaningful duplicate-key complexity argument, constant swap qualification, complete frequency program. DSU offline LCA entry/exit protocol, original (5,8)/(2,7) set states, `top` separate from union-by-size representative, invariant and complete Tarjan program.
- Mastery exercises and the six existing independent practice relationships retained; no global problem priority changes.

## Substantive and native review

Both languages were read against source steps rather than only checking headings. Two differently labeled eight-vertex trees and the two different value assignments on the nine-vertex tree remain separate. Root depth 1 in the source table and 0 in code are explicitly reconciled. No min/max for empty edge paths is fabricated. Actual code fragments concatenate exactly to each complete C++17 program; prose explains constructors, state, traversal, transitions, query rules and input/output. All tree traversals use explicit stacks or parent-first processing; only union-by-size DSU find uses shallow recursion. Each structure is built once on a valid static connected tree.

No rigid 15-heading template, nested tutorials, new editor feature, new permission or deferred feature work. All original metadata except title/summary/sections and corresponding English content is exact preserved. The previous pending representative and saved struct branch candidate are archived without rewriting history; their historical tests remain tied to those exact artifacts.

## Verification

Six C++17 programs: 561 UBSan executions, independent parent-walk/path/subtree/mutable-value oracles; n=1, random roots, chains/stars, duplicate values, absent keys, negative and large sums, empty query batches, and n=200000 deep chains. Native reader 8 cases and MN/EN editor serialization/reload pass. Eleven native diagrams pass four desktop/mobile/theme cases without overlapping/wrapped nodes or document overflow; individual graph screenshots were visually inspected, with weighted-edge label offsets adjusted for readability. Schema/publication model/MathJax prose checks pass. Local publication fixture checks rollback at the target/history boundary, stale private-draft rejection, replay rejection, and unrelated data preservation.

Fresh live recovery, CAS/body, draft, validator/ACL/trigger and protected-state checks are required immediately before the one-time job. Production result is not implied by local tests. Existing live Chromium certificate limitation remains; no certificate bypass or authenticated live fixture is used.
