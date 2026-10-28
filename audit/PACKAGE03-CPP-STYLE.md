# Readable competitive-programming C++17

Use familiar concise names when the role is clear: `n`, `m`, `a`, `adj`, `dist`, `dp`, `par`, `sz`, `l`, `r`, `mid`. Prefer `idx`, `cnt`, `sum`, `root`, `depth`, `pref`, `lazy`, `find`, `unite` to long narrative names. Keep meaningful function names, such as `dijkstra`, `merge_sort`, `prefix_function`, and descriptive names where two short alternatives would be ambiguous.

Use four spaces per block level, spaces around operators and after commas, attached opening braces, and readable control-flow blocks. Do not code-golf, invent dangerous macros or compress several logical steps onto one line. Existing consistent aligned continuation indentation is acceptable.

A short data-structure class/struct is useful when it owns related state, such as DSU, a tree query structure or two hash arrays. Do not add generic frameworks, wrappers or defensive machinery unrelated to the lesson. Preserve necessary bounds, empty-case and overflow handling, and preserve recursive merge sort and the recursive basic segment tree.

For existing lessons, change only implementation identifiers and directly corresponding code references in both languages. Keep fragments and the complete program synchronized. Unrelated prose, traces, samples, practice, priorities, identifiers and private drafts stay unchanged. Verify identifier substitution is injective, string/comment/preprocessor tokens remain intact, compile changed programs and run samples plus relevant representative independent oracles. Native editor/reader checks and fresh revision/hash/draft guards precede publication.

## Explicit reusable-data-structure convention

The user requires reusable structures such as segment trees and union-find to be compact `struct`s. This takes precedence over any general advice against wrappers: owning related arrays and operations is useful CP structure. Explain member fields, the size-taking constructor, initialization, each operation, and usage in `main`, then show the complete program.

For a recursive segment tree, explain `Segtree(int _n) { n = _n; tree.resize(n * 4 + 5); }`: the parameter is the logical element count; the member records that size; the allocation reserves heap-indexed storage for the recursive binary interval layout. Use the correct identity/default for the operation, and explain why the usual `4n` bound with a small margin is sufficient, including non-power-of-two lengths. Keep the main implementation recursive.

For DSU, use concise `par` and `sz` fields, initialize each element as its own parent with size one, and explain path compression and union by size. Constructors and method calls are part of the teaching, not unexplained scaffolding. Do not convert old code-only snapshots into finished new-cycle lessons; apply this convention during their original handbook rewrites.
