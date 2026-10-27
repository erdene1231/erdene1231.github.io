# Latest scope override

New editorials/hints/C++are optional;further authoring deferred until a fresh explicit user request. Completed material preserved,unfinished drafts isolated.245new selections satisfy metadata/source quotas;see PART04-READINESS.json. Earlier coverage/backlog counts below are historical and are not current completion gates. No tutorial lesson or blanket baseline review belongs to this package.

# Package4 problem editorials and routable detail — local implementation

Production status: neither032nor033applied; imports0; no merge/deploy/security change performed.033is a review proposal in `supabase/proposals/`, not an approved migration. Fresh actual-schema/ACL/Storage audit and private recovery are required before proposing its execution.

## Frontend behavior

`#problem/{stable-id}` replaces the old problem popup. Numeric aliases resolve to the unchanged stable ID. Back/forward/direct URL/refresh work; returning to the list restores filters, sort, pagination and scroll. Share URLs omit query parameters. Existing other dialogs/routes remain. The page presents source/rating/priority, progress/notes, explicit hint/editorial/source/solver actions and responsive reading layout.

Hidden unsolved tags are omitted from the problem page DOM, topic links and metadata; explicit reveal or solved state exposes them. Low exposes no hint controls/content and preserves stored hints/progress. Hints and rich editorial math use the existing safe MathJax integration. Existing public solver RPC/pagination is reused without changing its SQL, privacy rules or grants; browser never queries raw solver progress or private notes.

`problem-editorial.js` reuses the actual tutorial document validator, block editor, renderer, MathJax and safe private-media upload/delivery helpers. Editorial JSON stays outside catalog bodies. `hasEditorial` is metadata; full documents load only when opened. Admin editing uses the problem revision for atomic save, protects dirty edits and rejects stale responses/account changes. Every problem save/import (and new editorial media upload) checks for the new backend before writing; an older backend fails closed instead of silently discarding tiers/rich bodies/provenance. This intentionally means the draft frontend must not be deployed ahead of its separately approved backend.

## Exact proposed backend/permission changes for review

- Add `problem_editorials` and private `problem_editorial_changes`; enable RLS and revoke all direct anon/authenticated/PUBLIC table/sequence privileges. No fake tutorial rows or baseline backfill.
- Add security-definer `get_problem_editorial(text)`, with a pinned search_path, executable by anon/authenticated. Return only the rich document and revisions for active catalog problems. Archived documents are returned only when the existing server `is_admin()` check succeeds.
- Keep existing admin save/import RPC signatures and ACLs; server-admin checks remain. Update them to validate the tutorial/publication schema, High bilingual hints+substantive editorial, numeric/provenance ratings for new entries, Low's non-destructive historical hint policy, and canonical ordinary CF URL identity. CAS, advisory allocation lock, stable IDs, audit entries and whole-batch transactions remain. Learning-import dry run applies the same new-content/publication gates without writes.
- Extend the existing media read predicate so a server-verified admin can view images in current problem editorials, including archived documents. Anonymous delivery still requires an active published media reference. Reuse existing private bucket/upload owner rules; add no broad Storage write grant. Existing signed URLs retain their current up-to600second lifetime after archive; new anonymous signed delivery is denied after references are removed.
- Add current/history media-reference triggers using `problem:` scope-ID prefixes, including archive transitions. History protects removed images from cleanup without making them public. No Storage objects are deleted by this proposal.
- Fingerprint guards require the simulated post032function baseline and reject replay/drift/unexpected legacy inline bodies. This is not a fresh live-schema approval. Do not apply pending026/027or replay any old migration.

Admin profile permissions are a separate pending scope decision, described in PART04-ADMIN-PROFILE-PROPOSAL.md; this proposal does not grant profile, auth-user, role, email/password or progress editing.

## Verification and remaining scope

Actual browser checks cover the page URL/history/refresh, hidden-tag DOM, progress/auth interruption, safe sharing, solver50+1pagination, loading/empty/error states, both themes/mobile, MathJax, lazy/stale reader behavior, admin authoring, backend-missing failure, dirty switch cancellation and logout invalidation.23authored/proposed documents (21new+2baseline) pass the existing validator/editor/renderer/MathJax roundtrip with no MathJax errors. Synthetic PGlite checks cover roles/revocation/CAS, catalog body separation, all21new server document saves,2baseline updates,>70KB rich-body loading, rating/content/date rejection, CF aliases, learning dry-run and import rollback, media history/archive and preservation. These are not live authenticated/provider tests.

Data:92new source-reviewed (AtCoder50,CF42),21content/local-import-ready (AtCoder3,CF18),71prepared entries need content and153additional source reviews remain. Baseline35/748reviewed,713pending;30rating-rationale proposals and2new baseline High editorials unapplied. Tutorial55instructional semantic/practice/translation audits and other checklist/performance/delivery gaps remain; joke tutorial preserved. Package4is incomplete and PR20must remain draft.

## Latest authoring policy

23authored/proposed documents were reviewed for inline math;126authored MN/EN hint strings lint clean. The browser verifies actual L/R/n/m rendering and code exclusion.8existing tutorials require contextual bare-variable review. The3authored full C++17implementations now have meaningful state/preprocessing/algorithm/output explanations,4space layout and descriptive roles; exact code compiles warning-free and passes180seeded oracles.196existing tutorial C++blocks(110full programs across languages) are inventoried for manual review, not automatically rewritten or called complete.
