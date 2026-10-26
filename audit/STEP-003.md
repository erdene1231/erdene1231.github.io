# Алхам 003 — typed reader ба legacy editor-ийн нийцэл

2026-10-26. Parent `0438ac6ee0b01388474041a42f9c0e87316fd668`.
Recovery source-оос зөвхөн reader/model-ийн хэсгийг diff-ээр нэгтгэсэн.
Production database-д энэ алхмаар хүсэлт, migration, content write хийгээгүй.
Root 021/022 SQL болон pending 023–027 өөрчлөгдөөгүй.

## Хэрэгжсэн өөрчлөлт

- Typed rich text, headings, quote/callout/checklist, array/DP/graph/tree,
  tutorial/problem холбоос, image metadata-г DOM API-аар дүрслэнэ. HTML execute
  хийхгүй; code доторх tag ч text хэвээр. Content H1-ийг article дотор H2 болгоно.
- Typed inline links зөвхөн explicit HTTPS эсвэл зөвшөөрсөн internal route.
  Unknown/invalid block-ийг тайлбартай харуулна. SVG нь typed nodes/edges-ээс
  үүснэ; responsive resize үед ирмэг/оройн координат таарна.
- MN-only tutorial унших fallback бий. Legacy admin form English байхгүй үед
  түүнийг Монгол агуулгатай alias болгохгүй. Шинэ блокуудыг textarea болгохгүй,
  read-only хадгална; stable ID, revision/CAS болон үл мэдэх metadata хэвээр.
- Embedded problem нь одоогийн catalog/progress card-ыг ашиглана. MN-only
  variant target-ийг English reader-ээс нээхэд алдаа үүсэхгүй.
- Signed image reader зөвхөн Storage path ашиглаж, алдаанд retry харуулна.
  Account солигдвол өмнөх pending URL-г хаяна. Same-account progress sync нь
  media-г дахин ачаалж reader scroll/focus-ийг reset хийхгүй.
- Одоогийн eager `get_tutorials`, curriculum/edition hash gates, live content
  merge, learning store болон progress schema-г хэвээр хадгалсан.

## Тест ба нотолгооны хүрээ

`npm test`: 6 test file PASS. 55 checked-in tutorial body mutation-гүй validate;
typed round trip, malformed content, unsafe links, prerequisite checks, MN-only
editable fallback refusal, signed delivery/account race; existing model/store ба
021/022 isolated SQL regression орсон. Энэ нь 55 tutorial-ийн semantic quality
review эсвэл өнөөдрийн live content dump биш.

`python3 tests/browser/reader-compat.py`: real Chromium, real DOM/styles/modules,
synthetic fixtures, mock RPC. External network requests хаалттай. XSS-like text,
typed DOM, legacy rich-block preservation/MN-only save, mobile/desktop overflow,
light/dark болон diagram alignment шалгасан. Нэмэлт learning integration-ийн
үр дүн `STEP-003-BROWSER.json`-д (5 group PASS, page error 0); screenshot `browser/step-003-*.png`.

Auth/mock save бол production admin E2E биш. Real Storage policy/upload/delivery,
actual MathJax network rendering, clipboard success, published site behavior энэ
шалгалтаар батлагдаагүй. Existing offline SQL reconstruction нь post-022 snapshot
ашигладаг; live schema-г дахин уншсан гэж тооцохгүй.

`node tools/compare_supabase_schema.mjs`: tables/columns/constraints/indexes/
policies/functions/triggers/views бүгд 0 зөрүү (offline post-022 snapshot).
Tracked + new 283 файлд credential-pattern/runtime-token scan: 0 илэрц.
`git diff --check`: PASS. Secret/session утгыг output/file-д гаргаагүй.
Client болон Start skill-ийн `/workspace/shared` mirror нь repository хувилбартай
таарч байгаа; ирээдүйн environment image-д автоматаар бүртгэгдсэн гэж батлаагүй.

## Хийх үлдсэн ажил

Rich authoring toolbar, drafts/autosave/revisions, explicit publish, lazy reader,
Storage upload authorization, reference integrity, batch import нь pending.
Reader integration нь full editor completion биш. Frontend deploy хийгдээгүй.
Шинэ typed body-г production-д нийтлэхийн өмнө reader deployment/live smoke хэрэгтэй.
Дараагийн implementation нь 023 drafts/CAS security tests ба current schema audit.

## Frontend upload жагсаалт

Дараах 11 файлыг нэг release болгон хамтад нь байрлуулна. Query version `v=25`
нь шинэ module graph-ийг заана. Content JSON болон SQL-ийг frontend upload-аар солихгүй.

1. `index.html`
2. `app.js`
3. `learning.js`
4. `tutorials.js`
5. `tutorial-model.js`
6. `tutorial-editor.js`
7. `tutorial-editor-compat.js`
8. `tutorial-blocks.js`
9. `tutorial-block-renderer.js`
10. `tutorial-blocks.css`
11. `tutorial-media.js`

Existing styles/vendor/content файлууд өмнөх release-ээс хэвээр шаардагдана.
Archive бүх tracked site файлыг агуулна. Main merge/deploy хийгээгүй.
Feature branch push-ийн бодит remote SHA-г archive `MANIFEST.json` болон тухайн
task-ийн тайлангаас шалгана; local commit өөрөө remote synchronization-ийн
нотолгоо биш.
