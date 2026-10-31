# Independent native problem documents

The problem editor now exposes separate Statement and Editorial save/reload
controls. Both mount the existing tutorial block editor and serialize its actual
bilingual native document schema. Metadata has its own save action; an invalid
unsaved document cannot silently join a metadata or sibling-document save.

Each panel retains its own existing problem revision. A successful local save
advances compatible bases; a reload following an external edit updates only the
requested panel. Other dirty panels and typed metadata stay intact and retain
stale CAS bases, so they cannot overwrite another operator's changes.

Migration039 extends the existing problem body/admin save/catalog functions.
The lazy reader uses the already-granted `problem_catalog` SELECT and its existing
active/admin RLS policy. No table, public reader RPC, grants, policies, auth,
Storage access, or user data is added. The new validator is private to ordinary
clients. Inline image uploads remain unsupported. Both native readiness probes
are guaranteed validation failures before allocation or catalog writes.

Validation: eleven targeted Node tests including actual PGlite publication/CAS/
rollback/roles/ACL/policy preservation, actual admin native-component independent
save/reload/error/logout tests, and first-three editorial reader/editor checks
(12 MN/EN mobile-light/desktop-dark reader combinations and three exact native
roundtrips). A logout-disabled-control regression was found and fixed.

The candidate first batch is not published by this integration change. Its three
original bilingual editorials cover Yokan Party (Binary search/Greedy), Cross Sum
(row/column aggregation), and CP Classes (sort/lower_bound). Source samples,
independent exhaustive/naive checks and boundary stress passed 766 compiled C++17
UBSan runs. Actual code fragments match the tested final programs. Live publication
requires its own fresh guarded batch and receipt; authored is not published.

Fresh preintegration capture at2026-10-31T14:05:28Z matched the prior verified I/O
release exactly:1064 catalog rows, history/protected data/source/allocator/authority
fingerprints and all schema metadata unchanged. Migration039 was absent.

Evidence: `audit/native-problem-editorials/`,
`tests/native-inline-editorials.test.mjs`,
`tests/browser/native-problem-doc-actions.py`,
`tests/browser/native-editorial-batch01.py`.

Migration039 is now installed once as20261031140841. Its45-second response
timeout was resolved by readonly inspection without retry. Exact schema/data/ACL
comparison and anonymous readback are recorded in
`audit/native-problem-editorials/integration-receipt.json`.
