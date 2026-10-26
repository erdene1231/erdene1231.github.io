# Tutorial draft actions, backup restore and priority labels

Parent main: PR15 merge a405495dde6f5f011046007ba9be2222db4cd9ff.
Branch codex/draft-editor-actions. Full frontend graph v38.

The editor toolbar now contains JSON export/import. The manual Compare versions
and Before-comparison backup buttons are removed. Automatic conflict recovery
remains available when reloading a stale draft, including a stale online base;
no version is chosen or published automatically. Last local snapshots are retained
for explicit recovery. Publication review scrolls into view instead of appearing
below an unseen disabled form.

Preview, Save draft, Publish, Temporary remove and Delete draft actions share the
bottom bar. Save displays Saving while pending, Saved/disabled once clean and
stored, and re-enables on the next edit. Edits queued during a save are drained
before showing Saved. Failed saves retain the local body and an enabled Retry/Save
button; feedback is visible beside the actions. A clean published document without
an owner draft still permits its first private save.

Temporary removal saves the editor's work, hides the public catalog row using024,
and represents the lesson as a draft. The footer Publish action explicitly
publishes the current draft; it does not silently restore an old public body.
Delete draft requires typing the exact ID. Archived catalog lessons use028 with
its dependency/revision/actor guards and remove that lesson's body/drafts/history.
Never-published private drafts use new030, deleting only the acting editor's row
with CAS/actor/admin/confirmation checks and requiring no catalog row to exist.
Local draft/before-rebase cache entries are cleared on success. Other editor
private drafts and learner progress are preserved. Private IDs are not globally
reserved by030; old revisioned writes fail CAS. Downloaded backups and unreferenced
Storage objects are not purged; cleanup remains a separate Storage API workflow.

JSON export produces the current body. Import accepts that body or a snapshot's
body, checks size/structure/safe content and exact current ID, then requests an
explicit confirmation. Incomplete own draft fields/placeholders round-trip without
relaxing publication validation. A before-import snapshot must persist locally
before replacement; backup/storage failure stops the import. Cancel/invalid files
preserve the current draft. Only the private draft is replaced/saved; a file never
supplies actor, base revision or an automatic publication. Actor switches invalidate
late reads and confirmations. Batch/different-ID import remains separate pending027.

Both problem-selector panes show ★ Priority on priority tasks with an accent line.

## Database verification

A fresh actual schema audit matched after029 across functions, constraints,
indexes, triggers, RLS, tables and columns.030 installs one missing admin RPC;
three baseline function hashes and an existence guard reject stale/replayed SQL.
No existing functions, policies or content were replaced by installation.
030_delete_private_tutorial_draft applied as20261026110831. Before/after production
catalog hashes/counts are identical:748 problems/56 tutorials. Draft/history/
progress/learning-record counts also match before and after installation. No real
removal/publication RPC was invoked for tests. Fresh after030 metadata matches
repository reconstruction with zero differences. Evidence: DRAFT-ACTIONS-APPLY,
HISTORY,FINGERPRINTS.json and supabase/audit/production-after-030.json.

## Tests and continuation

18 Node test files /56 cases pass, including real PGlite authorization/CAS/delete
preservation and backup parser rejection/round-trip.69 Chromium groups pass:
21 editor,19 lifecycle,17 priority/popup,12 reader. Real browser, synthetic
Auth/RPC/catalog; actual authenticated deployed UI remains unverified. Tests cover
save success/failure/queued edits, backup export/confirm/cancel/invalid ID, temporary
remove->draft->publish, new private deletion, permanent archived deletion, actor/
late-result guards, automatic recovery and numeric-key compatibility. Screenshots
are committed without overwriting previous checkpoint evidence.

Review/merge PR then deploy completev38. No manual SQL is required; do not replay
021-025/028/029/030. Pending026/027 remain unapplied and require a fresh audit,
including numeric references/deleted-ID/draft-delete compatibility. The latest ZIP
contains the exact verified remote SHA, bundle, manifest and continuation notes.
