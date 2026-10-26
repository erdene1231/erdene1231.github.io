# Одоогийн шаардлагын checklist — алхам 005

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
| EDITOR-03 | Explicit publish/lazy reader | MISSING | recovery reviewed; pending 024 | байхгүй | үгүй |
| EDITOR-04 | Storage/media authorization | MISSING | recovery reviewed; pending 025 | real upload smoke pending | үгүй |
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

022 live verified (`20261026052253`) → reader/editor compatibility local verified → 023 backend live verified → draft UI integration,
024 current metadata re-audit → 024–027 тус бүрийн rollout. Storage тестгүйгээр editor
бүрэн live болсон гэж тэмдэглэхгүй. Үүний дараа Binary Search/Greedy semantic болон
browser review; үлдсэн content/topic/practice, plan/profile/UI regressions.

Бүртгэл: 1467 source мөр, 319 topic мөр (давхардалтай; тусдаа tutorial-ийн тоо биш).

Алхам 004: `STEP-004.md`; 023 version `20261026054052`, 748/55 ба content hash/revision unchanged.

Алхам 005: private draft UI/autosave/offline local recovery verified; revision comparison/rebase UI pending. `STEP-005.md`.
