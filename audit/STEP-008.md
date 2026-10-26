# Алхам 008 — validated explicit publication

Base main `f2cfeec5ec8d83681577678333c1a2934e3d2acf` (PR 7 merged). Production metadata эхэлж уншсан:
post-023 snapshot-тай яг ижил; 024 объект байхгүй. Recovery 023 publication-ийг
өмнөх mapping-ийн 024 болгон, fingerprint/absence/transaction compatibility
хамгаалалттайгаар нэгтгэсэн. Historical migration replay хийгээгүй.

## Database

`024_tutorial_publication` applied, version `20261026062140`, success=true.
Existing validate_tutorial_body болон prerequisite validation хэвээр.
Шинэ validate_tutorial_publication helper, publication trigger, publish/unpublish
RPC, public index/document RPC нэмэгдсэн. get_tutorials зөвхөн published row буцаана.
Existing tables/columns/constraints/indexes/policies болон хуучин triggers unchanged.
6 function, 1 trigger нэмэгдсэн; зөвхөн existing get_tutorials definition өөрчлөгдсөн.

Helper нь body shape, private _draftRelationsText refusal, prerequisites/cycles,
practice IDs/stage/priority/reason, variants/next published target-ийг шалгана.
Publish actor/admin + own draft revision + base/public revision CAS хэрэглэнэ.
Unpublish нь published prerequisite dependents байвал татгалзана.
Unchanged body draft устаж болно; sanitized body өөр бол owner draft шинэ base,
revision-тай үлдэнэ. Other editors-ийн drafts болон progress rows өөрчлөхгүй.
Embedded rich/image reference integrity нь 025/026 dependency-д үлдсэн.

Transaction-ийн төгсгөлд бүх live published body-г helper-ээр SELECT validation
хийж, алдаанд бүх DDL rollback болох gate-тэй. Content DML/backfill байхгүй.
Before/after: 748 problems, 55 tutorials; catalog body/ID/revision/updated_at
aggregate hashes unchanged. STEP-008-CONTENT-FINGERPRINTS.json.
Live get_tutorials/index read COUNT: 55/55 (STEP-008-LIVE-READ.json).
User private rows татаж аваагүй; no production tutorial published/unpublished.

## Frontend

Publication adapter нь draft-ийг clone хийж _draftRelationsText parse/validate,
public body-оос remove хийнэ. Existing metadata/relations objective-ийг хадгална;
missing English-ийг зохиохгүй. Invalid JSON/model/priority нь publish-ээс өмнө алдаа.
Review → explicit confirmation товч дарсны дараа л publish RPC явна. Private save
дууссан байх ёстой; review үеэр autosave paused, form locked. Stale CAS үед дахин
review шаардана. Account generation/actor checks late response-г хаяна.

Reader нь successful online result-ийг authoritative гэж үзнэ: хоосон/хассан
published list-ийг local seed-ээр нөхөхгүй. Existing eager get_tutorials reader
хэвээр; lazy index API database-д бий ч full lazy frontend integration pending.
Old static/offline copies of previously public content remain outside unpublish
control. No frontend unpublish toggle added in this step; server RPC is available.

## Verification

npm test: 35 cases across 10 files PASS. Эцсийн SQL target-existence/CAS нэмэлтийн
дараа targeted publication SQL test дахин PASS. Covers anon/non-admin/revoked,
actor mismatch, other editor draft + cross-admin stale publication, malformed
prerequisites/unsafe content/private metadata, unchanged baseline/progress,
private drafts, retained drafts, public read filtering, unpublish and replay gate.

Real Chromium: 12 groups PASS, including explicit publish confirmation,
private metadata stripping, stale conflict, authoritative empty catalog,
existing rich editor/autosave/rebase/reader regressions. RPC mocked, production
admin account E2E биш. publication 375/1440 screenshots reviewed; actual MathJax,
Storage upload болон Pages live smoke батлагдаагүй.
Offline SQL reconstruction vs post-024 snapshot: бүх бүлэгт 0 зөрүү.

## Үргэлжлэл

Дараагийн 009: 025 image Storage authorization/upload. Current schema дахин уншиж,
admin-only upload, draft vs public image access, MIME/size, account races тестэлнэ.
026 reference integrity, 027 batch/history тусдаа gate. Content tutorial review,
missing topics, practice, plan/profile/UI checklist-д хэвээр.
021/022/023/024-ийг дахин ажиллуулахгүй. Main merge/frontend deployment энэ task-д
хийгээгүй. Production publish request-ийг зөвхөн админ explicit confirm хийнэ.

Upload files: index.html, app.js, learning.js, tutorials.js, tutorial-editor.js,
tutorial-model.js, tutorial-block-renderer.js, tutorial-media.js,
tutorial-block-editor.js, tutorial-publication.js (version 29 graph). Existing
styles/draft/recovery modules бас шаардагдана. SQL-ийг static upload-аар ажиллуулахгүй.
