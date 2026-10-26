# Алхам 006 — revision comparison ба explicit draft recovery

Base main: `4ca1e851424e5c4f8c78c5e4c5e299abf19af966`. PR 5 merged гэдгийг fetch/log-оор баталсан.
005-ийн feature commit дахин хуулалгүй main merge дээр fast-forward хийсэн.
Main-д энэ task-аас push хийгээгүй; Pages deploy/live smoke шалгаагүй.

## Шаардлага ба хүрээ

requirements-02 Phase 2 (1061–1065) editor, draft/autosave/revisions-ийг tutorial
rewriting-ээс өмнө байрлуулсан. 006 нь local recovery/CAS зөрчлийн UI-г гүйцээнэ.
requirements-01-ийн жишиг 2–3 tutorial ба бүх content/topic/practice, plan/profile
ажлууд checklist-д хэвээр; editor complete эсвэл нийт project complete биш.

## Хэрэгжилт

Хувилбаруудыг харьцуулах товч local, own online draft, current published body-г
revision-тай нь expandable JSON байдлаар харуулна. TextContent ашиглана; HTML
ажиллуулахгүй. User сонголт хийх хүртэл save disabled. Сонголтыг зөвхөн
admin_rebase_tutorial_draft RPC-аар, харсан current_revision/draft_revision болон
actor-тай хадгална. Published body-г update хийхгүй. Private draft title/category,
body болон revision-ийг form/session-д шинэчилнэ; reload-д stale backup сэргээхгүй.

Compare үеэр autosave pause, pending request settle, form lock хэрэгжинэ.
Account солигдвол generation/actor gate хуучин response-г UI-д оруулахгүй.
Stale CAS үед save disabled; буцаж шинэ хувилбаруудыг дахин уншиж сонгоно.
Before-rebase local snapshot тусдаа account/document key-д хадгална. UI-аас
түүний JSON backup татна. Storage write бүтэлгүйтвэл rebase RPC дуудахгүй.
Энэ нь хамгийн сүүлийн before-rebase backup; бүрэн revision archive UI биш.

## Verification

npm test: 8 test file PASS. Targeted draft-session 6 case PASS; pause/resume,
backup isolation, accepted revision persistence, offline/late-response/CAS covered.
Real Chromium: 8 groups PASS; rebase selection, stale conflict, backup retention,
logout while RPC pending, existing reader/MN-only/autosave/learning regressions.
Comparison overflow 375/1440px checked, screenshot browser/step-006-comparison-*.
STEP-006-BROWSER.json болон бусад step-006 screenshots нотолгоо болно.
RPC mock хэрэглэсэн; production admin E2E биш. Production database request,
migration/content write энэ алхамд хийгээгүй. 021–023 дахин ажиллуулаагүй.

## Дараагийн ажил

Rich block authoring toolbar/section controls-ийг selective merge хийх. Дараа нь
024 publication, 025 media, 026 references, 027 batch тус бүр current schema audit
ба security/compatibility gate-тэй. _draftRelationsText raw private field-ийг
publication adapter parse/validate хийж public body-оос зайлуулах ёстой.
Editor-ийн суурь боломжууд дууссаны дараа Binary Search/Greedy жишиг semantic,
C++ болон browser review; үлдсэн content/topic/practice, plan/profile/UI ажил.

Upload: index.html, app.js, learning.js, tutorials.js, tutorial-editor.js,
tutorial-drafts.js, tutorial-draft-recovery.js, tutorial-model.js,
tutorial-block-renderer.js, tutorial-media.js (version 27 graph). Existing assets
хэвээр шаардагдана. Feature branch push нь website deploy биш.
