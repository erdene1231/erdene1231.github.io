# Named tutorial IDs, shared problem selection and editor repair

Parent main is the PR12 merge, 1da43e8 (full SHA in ZIP verification). Branch:
`codex/problem-selection-dialog`. Complete frontend graph: v34.

New tutorials ask for a name, prefill the title, and derive a lowercase stable slug
(e.g. Binary Search on Answer -> binary-search-on-answer). Mongolian Cyrillic is
transliterated. Empty/numeric-only names are rejected. Duplicate or permanently
reserved IDs are rejected; no numeric fallback/suffix is invented. Existing IDs
and subsequent title edits do not rewrite catalog IDs, links or progress.

Shared modal problem selection replaces embedded dropdowns and adds practice
selection. Admin problem editing also opens the same dialog in single-selection
mode. All use catalog.js filterProblems/getTags: query tokens, source, own status,
tag, rating band/min/max and sort have the main Problems page's exact semantics.
Rows have checkboxes, match/selected counts, select-all-filtered and clear actions.
Selections persist across filter changes; cancel makes no edit. Account/lock and
block-lifetime guards reject stale applications. Editor block multi-selection is
one Undo step, with overflow split into sections of at most100 blocks. Practice
selection preserves existing per-key stage/priority/reason metadata. New practices
start nonpriority; reasons/priority are configured in the existing relation editor.
Its existing server max30 is displayed/enforced without silently truncating.

The popup now gets the active catalog/progress directly from the app, so a failed
learning component cannot hide all problems. Archived problems are excluded from
authoring, and admin editing can include them through its existing archive toggle.

Preview previously called publication-grade validation, so incomplete metadata,
empty blocks or unfinished practice settings prevented opening the dialog. It now
collects the private draft without publication validation, renders supported content,
marks incomplete blocks and supplies missing-title/summary placeholders. Published
reader and publication validation remain strict. Preview never publishes a draft.

The workspace has a grouped toolbar, collapsible advanced IDs/search/link settings,
larger title and metadata inputs, structured section cards and sticky Preview/Save
bar. Boundary move/remove-section controls are disabled instead of silently doing
nothing. The before-rebase backup button is hidden when no such backup exists.
New-document inputs are locked during in-flight loads; logout/recovery protections
remain. Desktop/mobile screenshots are in audit/browser/editor-dialog-*.

Validation: npm test (50 Node cases); real Chromium editor regression and shared
popup tests, synthetic Auth/RPC/catalog only, no external requests. Exact results
are in EDITOR-DIALOG-VERIFICATION.json. Tests cover preview on unfinished new names,
formatting/save/recovery/translation/publication, bulk748 selection split/Undo,
query/filter parity, selection persistence, cancel, stale actor and responsive UI.
Deployed authenticated UI remains unverified.

No production/Supabase calls, migrations, content imports, deletes or progress
writes in this task. 028 remains already applied; do not replay021-025 or028.
Review/merge PR and deploy completev34 graph. NEXT-STEPS and Start skill retain
pending026/027 as separate work, requiring a fresh schema audit first.
