# Package 4 remaining gates and proposed approval sequence

245/245 new selections are locally ready under the user's latest lightweight curation scope. Package 4 is **not complete**. Production imports: zero. No migration, permission change, publication, merge or deployment was executed in this batch.

## Local delivery

The strict quota and identity/import checks pass. Metadata-only previews contain 100 + 100 + 45 new rows, without assigned server IDs or optional statement/editorial/hint bodies. Original completed optional content remains preserved in full previews; unfinished drafts remain on backup branches. A local recovery/review ZIP now exists with manifest hashes, CRC and safe-path verification, credential-pattern scan, full-history bundle verification and an offline clone/fsck check. See `PART04-RECOVERY-ARCHIVES.json`. It captures code commit cbbc6ee and preserved draft branches; the archive receipt is a subsequent metadata-only commit. Fresh private live recovery is a different untracked ZIP, excluded from the code archive. Neither archive was uploaded to Library; final user-facing handoff is not claimed. Current tracked files and feature commits are the durable working checkpoint.

## Production inspection before any approval to write

A fresh read-only inspection and scoped private recovery capture completed on 2026-10-27 at 17:43 UTC. See `PART04-PRODUCTION-READONLY-20261027.json` and `PART04-APPROVAL-PLAN.md`. Actual schema matches after-031, problem identities/bodies/revisions match the frozen snapshot, and one tutorial has a newer unpublished revision that must be preserved. Recheck current state before any future write. The scoped capture is not a full database/PITR/media-binary backup. The old after-031 snapshot is historical evidence, not proof of current production state. Do not replay applied migrations 021–025 or 028–031. Pending 026/027 are not an automatic execution queue. No Supabase call was made for this final selection batch.

Only after that inspection can an exact action-time write proposal be approved. Proposed order is 032, then 033, then 034, subject to compatibility review:

- 032: three-tier priority metadata validation, admin save support and indexes; no blanket baseline reclassification/backfill.
- 033: private editorial current/history storage, canonical Codeforces identity and rating validation, shared admin save/import revision/atomicity guards, lazy public `get_problem_editorial`, and existing server admin checks. Review any referenced-media read permission changes explicitly.
- 034: optional native bilingual statement storage/history/provenance, lazy `get_problem_statement`, catalog presence flags without rich bodies, shared revision/archive/media lifecycle guards. Review proposed active-content read RPC grants to anonymous/authenticated users and restricted archived/admin access. No broad Storage write or profile-edit grant is implied.

Local SQL role/atomicity tests do not establish real parallel PostgreSQL behavior, live Auth or Storage permissions. These remain deployment checks after separate authorization.

## Data changes proposed separately

1. Codeforces URL-only update: `PART04-CF-URL-DATA-PLAN.json` records 271 snapshot candidates. Recount live before writing. Guard each old URL/current revision; change only the URL, preserving stable IDs, references, content, relationships and learner progress. Historical 35 priority-review proposals are not included automatically.
2. New problem metadata: use `PART04-IMPORT-METADATA-01.json`, `02.json`, `03.json`. Fresh dedup and server dry-run precede separately approved imports. Save actual server-ID/source/reference receipts before attaching relationships. Never guess ID 749. A total of 993 follows only if the actual baseline remains 748 and all 245 are still new.
3. Optional content publication is excluded from these metadata-only batches. Full previews preserve completed material, but this plan does not publish optional documents or unfinished drafts. Any subsequent publication needs its own reviewed scope and authorization.

## Unimplemented admin profile requirement

`PART04-ADMIN-PROFILE-PROPOSAL.md` is a proposal, not a working editor or executable permission diff. Field scope remains pending: proposed first name, last name, derived full name and school; username, bio and unspecified fields preserved. Email, password, auth data, roles/admin grants, solved/progress, friends and follows are excluded.

Avatar replacement requires a separately reviewed target-bound Storage design, real-image/MIME/size validation and reference-safe cleanup. No broad bucket grant is acceptable. After field scope is confirmed, prepare the exact local RPC/UI diff, server-admin checks per request, target validation, stale-edit protection and private audit, then synthetic role/conflict/UI tests. No actual user records have been edited. A production permission approval cannot be requested on the basis of this document alone.

## User merge, live verification and transition

PR 20 remains draft; the user merges. Backend compatibility must be established before deploying frontend features that depend on new RPCs. No auto-merge or deployment is authorized. Live signed-in role, concurrent save/import, media and email-link callback checks need an approved safe fixture; do not create real accounts/send real emails implicitly. Chromium's `ERR_CERT_AUTHORITY_INVALID` was not bypassed. The 1,000-row browser result is synthetic local latency, not a live-site measurement.

Historical BOI Toll mapping remains unresolved and outside the agreed 245-source quota; no guessed ID or quota credit. Li Chao lesson creation/review and other lesson changes belong to deferred package 2, not a revived package 4 tutorial backlog. Existing 748 metadata is accepted, not subject to blanket reassessment.

Automatic transition to package 2 is authorized only after truthful package 4 completion and verification, or an explicit user rescope of unresolved required functionality/delivery. Do not label these remaining gates complete to advance.
