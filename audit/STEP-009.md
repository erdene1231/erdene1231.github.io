# Алхам 009 — Tutorial image upload / private Storage

Base main `d479c2e72bdf6a6284a071b8b0ad900103c94370` (PR 8 merged).
Branch `codex/recovery-step-009-tutorial-images`. Recovery files were selectively
diffed into the existing editor/reader. Requirements 02 sections 4.2–4.3 updated
as PARTIAL because authenticated live Storage upload/deployment remain unverified.

## Production audit and migration

Fresh schema matched production-after-024 exactly. Storage audit found no media
bucket and only three avatar policies, all scoped to think-cp-avatars. Objects RLS
was enabled. Before apply, offline reconstruction showed only the new 025 objects
missing; no changed existing object. Fingerprint/absence gate rejects drift/replay.
025_tutorial_media applied successfully as **20261026064758**. Never replay it.

Private tutorial-media bucket: image/webp only, 5242880-byte limit. Upload RLS
requires current admin + own UUID path; no object UPDATE policy (no overwrite).
Owners may preview private media; anonymous/other admins may read only referenced
published media. A second editor cannot publish a guessed private path. Restoring
another editor's now-unpublished private media requires that owner to publish or
re-upload an authorized copy; historical references do not grant public read.

Reference metadata tracks published, per-editor draft and history bodies. Published
images must exist. Existing published images are checked transactionally before
commit. Cleanup requires admin, age >7 days and no reference in any scope; shared
advisory lock coordinates publish/reference/cleanup checks. Candidate RPC exists;
no deletion job/UI, Storage object deletion or production content edit was run.
Future cleanup must use Storage API, never direct storage.objects DELETE SQL.

Post-025 catalog reconstruction: **zero differences** in all eight groups.
Existing functions (including 021 prerequisite and 024 publication validators),
constraints, indexes, policies and triggers are unchanged. Added: reference table,
3 columns, 2 indexes, 2 constraints, 6 functions, 4 triggers, 3 Storage policies.
Bucket config/policies independently verified in STEP-009-STORAGE-AFTER.json.
Before/after catalog content fingerprints identical: **748 problems / 55 tutorials**.
No user profiles, progress records, private draft bodies or storage files fetched.

## Frontend

Picker, image paste and drag/drop; PNG/JPEG/WebP MIME/signature checks; real browser
decode and canvas WebP re-encoding (original metadata discarded), longest edge
<=2400px, decoded image <=40MP, input/output <=5MiB. SVG/HTML rejected. Storage
server enforces declared MIME/size, not independent codec/signature verification.
UUID paths and upsert:false prevent replacement of existing bytes. Replace creates
a new object; removing a block never immediately deletes an image or breaks history.
Alt/caption/alignment/width and signed preview are editable; only object path and
metadata enter draft/autosave/local backups, never image bytes or signed URLs.

Generation/actor/document/block guards prevent upload dispatch after decode if
context changes. Completed responses from an old account, deleted block or older
replacement are discarded. Already dispatched requests may leave an unreferenced
object; seven-day cleanup protects recovery. Published signed URLs last up to 600s,
private previews 60s. Unpublish stops new public signing; issued URLs/received bytes
cannot be immediately revoked. Reader's previous safe URL/account guards retained.

## Validation

37 individual Node cases across 11 files PASS, including role/privilege tests with
Supabase-like default grants, admin A/B/non-admin/anon, no-update policy, draft,
published and history references, missing/foreign private images, age cleanup and
replay rejection. Each test file also run directly to retain individual case counts.
PGlite fails under experimental --test-isolation=none (import.meta loader issue);
normal isolated runs and direct per-file runs pass. This is not a product failure.

Real Chromium: 12 existing reader/editor groups PASS; 6 new media groups PASS.
Real codecs, resizing, output decoding, SVG/spoof/corrupt/oversize failures,
account races, picker/paste/drop/replace/remove, metadata/preview and actual editor
private autosave adapter verified. Tests mock Auth/Storage, block external network;
preview uses synthetic WebP bytes. Screenshots at 375 and 1200px reviewed.
No production admin E2E, real Storage byte upload, live Pages/MathJax/CDN claim.

## Handoff

Next 010: audit then 026 embedded reference integrity. Then 027 batch/private
recovery and full history UI. Lazy frontend, tutorial quality/topic coverage and
other checklist requirements remain open. Main merge/frontend deploy not performed.
This branch uses v30 for the editor/reader import graph; deploy the complete
checkout. SQL is already applied independently of the static frontend deployment.
