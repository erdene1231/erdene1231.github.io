# Exact remaining approval plan — 2026-10-27 read-only findings

No approval is requested or production action executed by this document. It separates independently reviewable actions; none is an automatic queue. Exact proposal SHA-256 values are in `PART04-PRODUCTION-READONLY-20261027.json`.

## Confirmed current state

Read-only production inspection succeeded at 17:43 UTC. Actual schema/function bodies/ACL/RLS/indexes/triggers exactly match before-032/after-031. All three 032 baseline function guards match. Migrations 021–025 and 028–031 are already applied; never replay them. Pending-editor 026/027 remain excluded. Catalog: 748 problems, 56 tutorials. Existing problem IDs/bodies/revisions/archive states match the frozen baseline. One tutorial is now unpublished at revision 2, with unchanged body; preserve that concurrent change.

The 245 metadata selections have zero live identity/URL conflicts. The 271 CF URL proposals match live old URLs/revisions. These findings are point-in-time and must be rechecked immediately before any write. The private scoped catalog/schema snapshot is not a full database/PITR or media-binary backup.

## A. Metadata support — 032 only

Proposed file: `supabase/032-three-tier-priority.sql`. Adds a private priority validator; replaces existing problem validator, server-admin save and tutorial metadata validator; adds problem/tutorial priority indexes. Existing role checks and RPC grants remain. No new public read RPC or Storage policy, user-profile permission, content backfill or baseline priority reassessment. No data import is included. This is the smallest proposed schema step for three-tier metadata support, not a blanket approval of optional rich-content infrastructure.

After separately approved execution: re-read actual function/index/ACL metadata; compare catalog rows/revisions/counts with the private before-state; stop on unexpected changes. Do not replay 032 if its guard fails or it is already present.

## B. Optional preserved rich-content infrastructure — 033 then 034

033 and 034 are genuinely absent and depend on reviewed preceding stages. Their local SQL tests passed against a baseline exactly matching the current schema. They are additional access-bearing proposals, not necessary authorization implied by selecting 245 metadata records.

033 (`supabase/proposals/033-problem-editorials.sql`) creates two RLS-enabled editorial current/history tables and a history sequence. Direct PUBLIC/anon/authenticated table/sequence access is revoked; server-admin save/import keeps existing role checks, uses revision/atomicity guards, and adds canonical identity/new-rating validation. A new `get_problem_editorial(text)` SECURITY DEFINER read RPC is executable by anon/authenticated for active content, and existing server admins can read archived content. Private validation/trigger helpers are not exposed. Media-reference triggers preserve current/history references. `can_read_tutorial_media` changes effective read access through the existing Storage SELECT policy: referenced active problem images become public-readable; server admins can read referenced problem editorial images. No broad Storage INSERT/DELETE grant is proposed.

034 (`supabase/proposals/034-problem-statements.sql`) adds two RLS-enabled statement current/history tables and sequence with direct client access revoked. Adds `get_problem_statement(text)` for active-content anon/authenticated reads, with archived access confined to existing server admins. Existing admin save/catalog RPC implementations are renamed to private helpers and revoked from client roles; wrappers preserve the authenticated admin save/catalog checks. Public catalog remains executable by anon/authenticated and returns only presence flags, not rich bodies. Revision-guarded imports/archive and statement/media lifecycle wrappers are updated. Effective published/read-referenced media access extends to statement media; no broad Storage write permission or profile permission is included.

Approval of infrastructure does not approve publication of optional documents. Existing 42 bilingual statements and 74 editorial documents remain preserved; no new authoring or unfinished-draft publication is proposed. After any separately approved installation, verify actual ACLs/function guards, anonymous/non-admin/admin/archived behavior, unchanged catalogs, and live media/reference behavior with an authorized fixture before deployment.

## C. Separate production data actions

- CF URL-only change: exactly the current 271 guarded candidates in `PART04-CF-URL-DATA-PLAN.json`, changing only ordinary CF problem URLs to contest form. Preserve IDs/numbers/source/ref/content/progress/relationships; reject stale URL/revision. No Gym rewrite, unrelated URL change or old 35-priority-patch application.
- New problem metadata: server dry-run and explicit reviewed new-only imports from `PART04-IMPORT-METADATA-01.json` (100), `02.json` (100), `03.json` (45). Recheck live canonical identities first; import no optional bodies/hints, overwrite no baseline row, save real server ID/reference receipts and before/after counts. Sequence is currently 748 but never assign IDs from that assumption. No profile/progress/history cleanup is included.
- Optional completed content publication requires its own reviewed document/target/revision list and explicit authorization. Preservation in the code archive is not publication permission. No unfinished statements/editorials/C++ drafts are included in metadata import.

## D. Admin profile requirement — decision and local implementation remain

Parent is already asking for the ordinary field scope; do not send another approval prompt. Proposed fields: first name, surname, derived full name, school; avatar needs explicit target-bound upload authorization design. Email/password/auth/roles/solved/progress are excluded. No executable profile permission diff or working editor exists yet. After scope confirmation, prepare the exact local server-admin allowlist/CAS/private-audit RPC, UI and synthetic role/conflict/avatar tests. Only then can production access changes be reviewed concretely. Do not weaken owner RLS or grant bucket-wide writes.

## E. Delivery and live verification

Code recovery archive and private live recovery are separate local artifacts. Neither is a production restore action. User merges PR20; no merge/auto-merge/deploy is authorized here. Any frontend release must match installed backend support. Actual signed-in Auth/Storage/concurrency checks require a safe authorized fixture; no real account/email/user mutation is implicit. Do not bypass the live browser certificate warning. Local synthetic performance does not establish live user latency.

Package 4 remains incomplete while required admin functionality and these applicable delivery/live gates remain unresolved. No transition to package 2 yet. No further statement/editorial authoring or blanket baseline/tutorial review is proposed.
