# Tutorial lifecycle, problem picker and sample presentation

Parent: main `31b66a95cf155cd6ef18c1796fc138865385ba4b` (PR 11 merged).
Branch: `codex/tutorial-removal`. Frontend graph: v33. Exact final commit, remote
SHA, PR and archive checksum are recorded in the downloadable handoff.

## Behavior

Published lessons now offer **Түр устгах** with an explicit review/confirmation.
The existing 024 RPC removes the lesson from public readers, keeps its catalog
body, private drafts, ID, history and progress, and allows **Сэргээх**. A restore
publishes the last catalog body; it never publishes the editor's private changes.
Private changes are saved before visibility review; stale draft/base/catalog
revisions stop the action and leave recovery/backup available.

An archived lesson also offers **Үүрд устгах**. The admin must review what will
be erased, type the exact lesson ID, then confirm. 028 requires the matching
catalog revision, actor/admin checks and prior unpublishing. Incoming links from
other catalog lessons or private drafts block removal without disclosing private
draft contents. Permanent removal deletes only that lesson's catalog body, all
editor drafts and history. An ID-only tombstone prevents later reuse/resurrection;
all other tutorial IDs, bodies, revisions and learner progress remain stable.
`admin_tutorial_document` returns an admin-only `deleted` flag for new-ID checks.
Private-only drafts do not use catalog lifecycle deletion.

Both actions update the current public list/reader without restoring seed rows.
Configured production clients wait for an authoritative catalog and report an
initial fetch failure without showing outdated bundled lessons. Null-client
offline demos still use seed content. Logout clears the previous editor document,
private options and controls. Late responses cannot reopen another actor's editor.

The problem picker no longer truncates at 30. It searches stable IDs, visible
numbers, source IDs, names, source/ref, URL and canonical keys; selections retain
canonical CSES keys. It uses the active catalog, preserves selected/missing
references when filtering, displays match totals, refreshes on focus/search and
gives separate Undo checkpoints for separate selections.

Adjacent Input/Output samples have compact paired panels, stacked on mobile,
light/dark colors, keyboard-scrollable code and accessible copy feedback. Text,
whitespace, ordering and clipboard contents are preserved.

## Production evidence

Fresh pre-change metadata (`production-before-028.json`) matched the verified
025 snapshot across schema, constraints, indexes, policies, functions and triggers.
Only confirmed missing changes were installed through `028-tutorial-deletion.sql`;
pending 026/027 were neither replayed nor silently renumbered. Eight baseline
function fingerprints guard the migration. Existing prerequisite/publication/media
validation remains unchanged; the only replaced RPC is `admin_tutorial_document`
with its additive `deleted` flag.

028 was applied as **20261026091603**. `TUTORIAL-LIFECYCLE-APPLY.json` and
`TUTORIAL-LIFECYCLE-HISTORY.json` contain the actual tool results. Fresh after
metadata matches repository reconstruction with **zero differences** across all
eight catalog groups. See `TUTORIAL-LIFECYCLE-SCHEMA.json` and
`supabase/audit/comparison.json`.

Actual production count is **748 problems / 56 tutorials**. The prior 55 count is
historical. Before/after catalog fingerprints and draft/history/progress counts
are identical (`TUTORIAL-LIFECYCLE-FINGERPRINTS.json`). Installation did not call
the removal RPC, publish/import content, remove a tutorial or modify progress.
Metadata and aggregates were read; no personal user rows or credentials were fetched.

Storage objects are deliberately not deleted through SQL. Reference metadata is
updated with deletion; object cleanup remains a separate, reference/age-checked
Storage API task. Issued signed URLs can live until their TTL expires; downloaded
backups and bundled historical source are not erased by catalog removal.
Temporary removal retains the existing incoming-prerequisite guard; complete
unpublish reference integrity remains the separate pending 026 work.

## Validation and continuation

`TUTORIAL-LIFECYCLE-VERIFICATION.json` records test results. Chromium uses a real
browser with synthetic fixtures and mocked Auth/RPC/Storage, external network
blocked. Coverage includes explicit confirmations/cancellation, stale versions,
failed saves, dependencies, duplicate clicks, actor/logout races, preserving the
private draft, surviving IDs and progress, active-reader removal/restoration,
full 748-problem selection, and sample clipboard/text preservation across the 55
checked-in tutorials in both languages. These are not live authenticated UI tests.

Review/merge the PR and deploy the complete v33 graph; deployment is separate.
No manual Supabase SQL is needed for 028 and it must not be replayed. Do not use
real content deletion as an automated smoke test. Next planned feature remains
010: re-audit the now-current 028 baseline before evaluating pending 026, then027.
The original source requirements remain intact; supplemental user requests and
local/live/deployment distinctions are in REQUIREMENTS-CURRENT.json.
