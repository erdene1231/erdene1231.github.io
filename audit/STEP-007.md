# Алхам 007 — rich block authoring ба section controls

Base main `d24c8c422f92000233d1c6f7329479776986fbfe` (PR 6 merged), fast-forward хийсэн; source snapshot-ийг
бүхлээр нь дарж хуулаагүй. Requirements-02 Phase 2, 4.1/4.4/4.6/4.7/4.9-ийн
editor authoring хүрээнд recovery tutorial-block-editor.js-г selective merge хийв.

## Хэрэгжилт

Rich text marks/link, headings, code/indentation, math, lists/checklist, table,
quote/callout/note, typed diagrams, problem/tutorial links, divider authoring.
Block/section нэмэх, хувилах, дээш/доош зөөх, хасах, 25 snapshot Undo/Redo.
Сүүлийн section/block-ийг хасахгүй. Existing unknown metadata ба typed body
нээгээд хадгалахад хэвээр. Plain paragraph нь зөвхөн засах үед rich болдог.
Quote/callout rich content-ийн marks-ийг plain text болгож алдахгүй.

Contenteditable paste/drop нь plain text хэрэглэнэ; arbitrary HTML оруулахгүй.
Links explicit HTTPS/internal safeLink шалгалттай. Renderer DOM text хэвээр.
Structural өөрчлөлтийн callback шууд draft session-д очно; хуучин textarea
collector нь шинэ бүтэц дээр давхар бичихгүй. Compare/load үеийн form lock
contenteditable-д мөн үйлчилнэ; account солигдоход хуучин editor destroy хийнэ.
Undo availability typing бүрд шинэчлэгдэнэ; detached selection reset хийнэ.

Зураг upload insert option идэвхгүй. Existing image block body-г хэвээр хадгална.
Storage policies/upload нь 025-аас хамаарах тусдаа ажил. Raw HTML/Mermaid import,
full version archive, publication энэ алхмын хүрээнд ороогүй.

## Verification

npm test: 8 test file PASS. Real Chromium: 10 groups PASS; rich text selection/
formatting, safe paste, section duplicate/reorder, Undo/Redo, model validation,
actual editor rich edit → private draft autosave; MN-only, offline, rebase/late
response, learning/reader regressions. 375/1440px light/dark authoring screenshots
browser/step-007-authoring-*; STEP-007-BROWSER.json. RPC mock тул production admin
E2E биш. Clipboard paste event synthetic; actual OS clipboard permission тест биш.
Image upload ба actual MathJax CDN rendering батлагдаагүй.

Production database request/migration/content write хийгээгүй. 021–023 replay
хийгээгүй. Problem/tutorial JSON, IDs/progress импорт/overwrite байхгүй.
Full editor/project completion гэж тэмдэглээгүй. Feature push нь main merge эсвэл
website deploy биш.

## Үргэлжлэл

Дараагийн ажил: 024 explicit publication dependency-г live metadata-тай тулгаж,
private draft → validated public body adapter (including _draftRelationsText
parse/validate/remove), CAS/admin security tests. Дараа нь 025 image Storage,
026 references, 027 batch тусдаа gate-тэй. Үүний дараа Binary Search/Greedy жишиг
semantic/C++/browser review, бүх tutorial/topic/practice болон plan/profile/UI.

Deploy file set: index.html, app.js, learning.js, tutorials.js, tutorial-editor.js,
tutorial-model.js, tutorial-block-renderer.js, tutorial-media.js,
tutorial-block-editor.js, tutorial-block-editor.css. Version 28 graph; existing
assets/draft/recovery modules хэвээр хэрэгтэй. Main/site deploy энэ task-д хийгээгүй.
