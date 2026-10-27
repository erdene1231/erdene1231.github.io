Status: local code complete and pushed;new PR creation denied by automatic review,no actual PR number assigned. See `PART04-WORKFLOW-BLOCKERS.json`.

# Remaining package4 delivery — separate follow-up PR

Base is PR20 branch `codex/part04-recovered` at713f6e0. This stacked PR isolates admin-profile functionality and all still-unexecuted package4 rollout gates. No force push/history rewrite. User merges PR20 first; recheck/retarget follow-up to main after its base is present, preserving commits. Verify the actual new PR number rather than assuming21.

## Implemented local admin feature

Surname, first name, username, profile picture; no school/email/password/Auth/roles/progress changes. Native secure server-admin RPC/target/CAS/allowlist/private audit and reserved target-bound avatar workflow in proposed035. See `PART04-ADMIN-PROFILE-PROPOSAL.md`. Disabled by default; merging frontend code alone sends no admin-profile requests and grants no access. No production installation is part of PR merge permission.

## Remaining independent installation/data gates

The previously prepared032–034 SQL and245metadata/271URL artifacts remain preserved in PR20 as inert review material; their execution/rollout is tracked here, not silently performed by merge. See `PART04-APPROVAL-PLAN.md` for exact proposal stages and access impacts. Metadata-only032 and optional033/034 are independent review choices, not an automatic queue.035 has separate profile/Storage access impacts and depends on the audited existing profile schema, not on032–034.

Before action-time approval, re-audit current schema/functions/ACL/RLS/Storage/catalog/revisions; preserve the one newer unpublished tutorial and all existing IDs/data. Snapshot findings from17:43UTC are historical at a future write. Do not replay applied021–025/028–031 or automatically run pending026/027. Current imported0.245new rows have no assigned IDs; save actual server receipts before relations.271URL-only updates require matching current old URL/revision and must not apply old priority reclassification patches. No baseline reassessment or new statement/editorial authoring.

## Verification and release boundaries

PR20 has a default31-compatible legacy edit path. Keep `problemBackendVersion:31` until corresponding production support is separately approved/verified. Keep `adminProfileEditorEnabled:false` (or absent) until035is installed/verified. Public config flags never replace server authorization. No automatic SQL/import/Storage jobs or release process is added.

After approved backend installation, live role/CAS/concurrent save/import/Storage checks require an authorized safe fixture, and production imports/publication/URL changes need their separate approved exact scope. Do not create real accounts/send emails/upload avatars implicitly. Do not bypass certificate trust failures. User merges; no auto-merge/deploy. Final handoff/download delivery and fresh source-code archive beyond cbbc6ee remain distinct from the existing verified checkpoint ZIP.

## Current external workflow block

PR20 compatibility commit713f6e0was pushed and verified. GitHub metadata update returnedisError and remote metadata remained unchanged. Automatic approval review explicitly rejected marking PR20ready, stating no trusted user message authorized that exact state change. No retry or alternate-route bypass was attempted. PR20therefore remains draft despite passing code checks. Parent must resolve that exact workflow block; do not ask repetitive user approvals for unrelated local work.

Package4 is not complete merely because the work is split. Package2 has not started. Completed optional statements/editorials and isolated unfinished branches remain preserved; authoring stays deferred until fresh explicit request.
