# Одоогийн шаардлагын checklist — алхам 009

Хавсралтуудыг бүтнээр уншсан. Хэрэглэгчийн шинэ baseline нь ZIP-ийн хуучин мэдээллийг орлоно.
`f7c5f2e820f01652e3a839f2db69c05b16c91adb`; 748 problems / 55 tutorials;
production prerequisite migration `20261026045125` нь recovery editor 021-ээс өөр.

## Энэ алхмын хэрэгжилт

| ID | Шаардлага | Төлөв | Local / тест | Live | Deploy |
|---|---|---|---|---|---|
| SYNC-01 | Батлагдсан commit ба ZIP provenance | VERIFIED_COMPLETE | HEAD, checksum, inventory | schema baseline таарсан | GitHub baseline батлагдсан |
| DB-01 | Migration дугаар/агуулгын reconciliation | VERIFIED_COMPLETE | EDITOR-MIGRATION-MAP.json, functions/dependencies reviewed | 021 тусдаа | 022–027 шинэ нэр |
| EDITOR-01 | Typed content blocks SQL contract | VERIFIED_COMPLETE | 022 + regression PASS | applied + rich block SELECT PASS | Frontend нэвтрүүлээгүй |
| SAFE-01 | Prerequisite validation хадгалах | VERIFIED_COMPLETE | invalid/null/31-ID тест PASS | live invalid ID → 22023 | 021 хамгаалалт хадгалагдсан |
| SAFE-02 | Энэ алхамд admin content, ID, progress хадгалах | VERIFIED_COMPLETE | no content DML; fixture preservation PASS | before/after content hashes/revisions identical | Content import байхгүй |
| READER-01 | Typed reader + legacy editor round-trip | LOCAL_VERIFIED | Node + Chromium, MN-only, XSS, media race PASS | frontend live шалгаагүй | үгүй |
| EDITOR-02 | Private drafts/CAS | PARTIAL | backend security/CAS/rebase tests PASS | 023 applied, schema verified | draft UI local tested; not deployed |
| EDITOR-03 | Explicit publish/lazy reader | PARTIAL | publish UI + SQL tests PASS; lazy frontend pending | 024 applied + public reads 55 | UI feature branch only |
| EDITOR-04 | Storage/media authorization | PARTIAL | upload/paste/drop/preview + codecs/RLS tests PASS | 025 applied, schema/bucket/policies verified; real admin upload smoke pending | UI branch, deploy unverified |
| EDITOR-05 | Embedded relation integrity | MISSING | recovery reviewed; pending 026 | байхгүй | үгүй |
| EDITOR-06 | Atomic batch/private recovery | MISSING | recovery reviewed; pending 027 | байхгүй | үгүй |
| CONTENT-01 | Binary Search / Greedy semantic + browser review | PARTIAL | recovery historical C++ evidence only | шинэ агуулга нийтлээгүй | үгүй |
| CONTENT-02 | Existing 55 individual quality reviews | PARTIAL | recovery claims 3; current hashes/review recheck pending | 55 row ≠ quality | үгүй |
| CATALOG-01 | BOI17 Toll stable ID reconciliation | BLOCKED | pending ID recovery only | импортлоогүй | үгүй |
| EXTRA-01 | Rating palette, extra quotas, 4-level importance | MISSING | өмнөх ажлуудын дараа | үгүй | үгүй |

Алхам 003: typed reader болон хуучин editor-ийн агуулга хадгалалтыг нэгтгэв.
Шинэ блок authoring, drafts/autosave/upload/publish нь бүрэн хэрэгжээгүй.
Production database өөрчлөгдөөгүй, frontend deploy хийгдээгүй.
Баримт: `STEP-003.md`, `STEP-003-BROWSER.json`, `tests/reader-compat.test.mjs`.

## Бүх эх шаардлагын бүртгэл

`REQUIREMENTS-CURRENT.json` нь хоёр эхийн хоосон биш, гарчиг биш мөр бүрийг stable
`R1-L####` / `R2-L####` ID, эх файл/мөр, context, evidence, local/test/live/deploy
талбартай хадгална. Жишээ/тайлбарын мөрүүд traceability зориулалттай; тусдаа feature
гэж зохиомлоор тоолохгүй. `PARTIAL + NOT_YET_REVIEWED` нь шалгалт дутууг илэрхийлнэ,
хэрэгжсэн гэсэн баталгаа биш. Үндсэн бүлгийн төлөвийг дээр товч нэгтгэв.

Topic мөр бүр тусдаа хадгалагдсан. Нэрээр олдсон canonical candidate нь semantic
coverage биш. Anchor ба alias нэгтгэл нотлогдоогүй үед `UNMAPPED_BACKLOG` эсвэл
`CANDIDATE_NEEDS_SEMANTIC_REVIEW` гэж үлдээнэ; label-ийг чимээгүй хасаагүй.
Recovery-ийн 41/55 гэсэн баталгаагүй тоог ашиглаагүй.

## Дараагийн ажил

022–025 backend live verified; draft/rebase/authoring/publication/image UI local verified.
Дараа нь 026 reference integrity → 027 batch/history. Real Storage upload smoke-гүйгээр editor
бүрэн live болсон гэж тэмдэглэхгүй. Үүний дараа Binary Search/Greedy semantic болон
browser review; үлдсэн content/topic/practice, plan/profile/UI regressions.

Бүртгэл: 1467 source мөр, 319 topic мөр (давхардалтай; тусдаа tutorial-ийн тоо биш).

Алхам 004: `STEP-004.md`; 023 version `20261026054052`, 748/55 ба content hash/revision unchanged.

Алхам 005: private draft UI/autosave/offline local recovery verified; revision comparison/rebase UI pending. `STEP-005.md`.

Алхам 006: revision comparison/explicit rebase + before-rebase backup local verified. Full rich authoring/media/publication/history UI pending. `STEP-006.md`.

Алхам 007: rich block authoring/section controls/Undo/Redo local verified. Image upload/publication/history pending. `STEP-007.md`.

Алхам 008: publication backend live verified, confirmation UI local verified. 748/55 unchanged; image upload дараагийн 009. `STEP-008.md`.

## Алхам 009 — зураг upload

025_tutorial_media (`20261026064758`) applied; existing schema objects and
748/55 content fingerprints unchanged. File picker/paste/drop, WebP conversion,
preview/width/alignment/alt/caption/replace/remove, private draft autosave local
verified. 37 Node cases + 12 reader/editor browser groups + 6 media groups PASS.
Storage API/Auth mocked in browser: real authenticated upload and deployed Pages
smoke remain open. SVG rejected; cleanup strategy is age/reference-protected
manual Storage API, no automatic deletion. Evidence: `STEP-009.md`.
Дараагийн 010: 026 embedded reference integrity; 027 batch/history дараа нь.

## Editor repair after 009

User-reported Bold/Italic and new tutorial gaps repaired; explicit ID/metadata and
English creation, private draft choices, new publication library insertion added.
Autosave, failed-load, stale-local recovery and refresh regressions fixed.
40 Node cases + 30 Chromium groups PASS; authenticated live behavior/deploy still
unverified. See `EDITOR-FIX.md`. Planned 010/026 and remaining checklist unchanged.

Recovery UX after PR 10: visible conflict version selection/backup and actual
editor continuation verified locally (41 Node / 39 browser groups). No live
admin E2E/deploy claim. See RECOVERY-UX.md. Next step still 010/026.
