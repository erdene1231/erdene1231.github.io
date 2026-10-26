# Алхам 005 — private draft UI ба autosave

Base: GitHub main `55173c0ad6f5c8ac3010d156ae7e59d0c1efde3f` (PR 1–4 merged).
Main merge-үүдийг fetch хийж feature branch-ийг fast-forward болгосон.
Website deployment амжилттай эсэхийг энэ алхмаар шалгаагүй.

Одоогийн editor form owner-specific admin_tutorial_document-оос ноорог уншиж,
admin_save_tutorial_draft-аар хадгална. Шууд publish RPC дуудахгүй. Manual save,
1.8 секунд autosave, online retry, account-scoped local recovery, JSON download,
unsaved unload warning нэмсэн. Existing rich blocks read-only хэвээр хадгалагдана.
Incomplete body private draft-д хадгалж болно. Relations JSON raw text нь
_draftRelationsText талбарт хадгалагдана; future publication adapter энэ талбарыг
parse/validate хийж, public body-оос зайлуулах ёстой.

Generation guard нь account/document солигдсон үеийн late response-г хаяна.
In-flight save үеийн шинэ засвар дараагийн CAS save-д орно. Revision conflict
local payload-г хадгалж, автоматаар overwrite/rebase хийхгүй. Local revision
server-тай зөрвөл form load зогсож JSON backup боломжтой; conflict comparison ба
explicit rebase UI дараагийн ажил. Different document сонгож болно.

Tests: npm test 8 files PASS. Draft-session tests: offline retry, owner isolation,
late account response, in-flight newer edit, conflict no retry-loop. Browser:
6 groups PASS; actual form autosave, offline recovery/retry, private-only RPC,
MN-only/rich preservation, reader/learning/mobile regressions. RPC mock тул
production admin E2E биш. Evidence STEP-005-BROWSER.json + browser/step-005-*.
Timer overlap regression илэрч, in-flight drain хийхээс өмнө debounce timer-ийг
цуцалдаг болгосон. Secret/session утга файлд ороогүй.

Database хүсэлт/migration/content write энэ алхамд хийгээгүй. 021–023 replay
хийгээгүй. Published bodies/IDs/progress импортлоогүй. 024–027 pending.
Full rich authoring toolbar/media upload/publication/history/rebase UI pending.

Deploy хийхдээ index.html, app.js, learning.js, tutorials.js, tutorial-model.js,
tutorial-editor.js, tutorial-drafts.js, tutorial-block-renderer.js, tutorial-media.js
нэг release болгон байрлуул. Existing assets/model/compat modules хэвээр хэрэгтэй.
Version 26 module graph. Feature branch push нь main merge/site deploy биш.
