# Tutorial editor repair — after step 009

User reported inactive Bold/Italic, incomplete new tutorial authoring, and inability
to edit the first Time Complexity tutorial. Based on merged PR 9/main
`908ab18bf0bcb59d8de64bfcdd4460267d11984f`. Branch `codex/fix-tutorial-editor`.
This repair precedes step 010; no pending migration was activated.

## Reproduced and fixed

- Formatting formerly required a non-collapsed selection and only wrapped tags.
  Bold/Italic/Underline/Strike now use the browser's inline editing commands:
  selected text toggles, caret-first typing, keyboard shortcuts and active toolbar
  states. Semantic tags serialize into typed marks, including native STRIKE.
  Text-only paste/XSS protections retained. Inline code and links use selected text.
  Native execCommand is deprecated but still supported in the tested Chromium;
  Firefox/Safari/mobile device E2E was not run.
- Draft flush now drains edits queued during an in-flight save before resolving.
  Closing comparison resumes autosave. Invalid/stale save responses retain local
  work. CAS/actor guards and conflict non-overwrite behavior remain in place.
- Failed loads clear stale blocks and disable editing while keeping retry/backup
  available. A conflicting local draft opens comparison instead of leaving a dead
  editor. Nothing automatically overwrites the local or server version.
- Catalog refresh preserves the current draft, language, DOM and undo history.
  Removing the final block now works and can be undone; incomplete drafts remain
  private and publication validation still requires at least one valid block.

## Complete the missing authoring path

New tutorial UI checks a unique immutable ID, starts a private base-revision-0
noorog, and exposes title, summary, prerequisites, aliases, related/prerequisite IDs,
level/order/category and section/block authoring. Duplicate IDs are refused without
writing. English translation can be started explicitly without aliasing MN data.
Admin workspace metadata supplies unpublished and owner-private draft choices.
Fresh publication is appended to the actual tutorial library and routes correctly.
Existing 023/024 RPCs supply the backend; no new SQL is required.

## Time Complexity and verification

Read only the current published complexity body and its public catalog metadata.
It is revision 5 with 14 sections. All 14 sections/blocks mounted in the repaired
editor locally. Also reproduced first-tutorial stale-local conflict and verified
that recovery comparison opens without an automatic save. The user's own browser
storage/authenticated session was not inspected; this does not establish that a
local conflict was the exact cause in that browser.

40 individual Node cases across 11 files PASS. Real Chromium: 12 new editor repair
cases + 12 reader/editor regression groups + 6 media groups PASS. Tests exercise
real browser formatting/codecs/DOM, with mocked RPC/Auth/Storage. Existing fixture
save responses were corrected to increment draft revisions like the real RPC.
Screenshots at 375/1200px were reviewed. Prior step-009 audit evidence is preserved;
repair test outputs have EDITOR-FIX names.

No production writes, migrations, uploads, tutorial publication, user/progress row
reads or content replacements occurred. Live admin save/upload/publish smoke after
deployment remains unverified. Complete v31 import graph must deploy together.
Credentials and sessions are not in code, audit or ZIP. Main merge/deploy is separate.
Next planned numbered step remains 010 / audit then 026 reference integrity.
