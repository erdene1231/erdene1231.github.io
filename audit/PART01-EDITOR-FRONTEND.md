# Багц1 — editor frontend bug fixes, v40

Хэрэглэгчийн шинэ чиглэл: tutorial editor бараг бэлэн тул frontend сайжруулалт болон bug шалгаж засах. Энэ checkpoint нь энэ чиглэлийн frontend ажил; анхны багц1-ийн бүх58 item болон pending026/027 backend/bulk боломжуудыг дууссан гэж тэмдэглээгүй. Багц2 эхлээгүй.

## Олсон ба зассан алдаа

- Хоосон хичээл зөвшөөрсөн ч сүүлийн section устгах disabled байсан. Одоо устгаж0 sections болгоно, Undo/Redo сэргээнэ.
- Section add/duplicate80, block add/duplicate100, table rows100, checklist items100 хязгааргүй байсан. Одоо model-ийн дээд хязгаарт button disabled, handler guard-тай; image paste/drop мөн100-block хязгаарыг баримтална. Checklist-ийн цорын ганц мөрийг хасаж invalid block үүсгэхгүй; block-оо бүхлээр устгаж болно.
- Rich link input Enter нь parent form submit/save өдөөдөг байсан. Одоо Enter зөвхөн selection-д safe link хэрэглэнэ; form submit болохгүй.
- Closed section-ийг busy/locked үед нээхэд lazy-mounted талбарууд идэвхтэй үүсдэг байсан. Одоо бүх mounted inputs/contenteditable lock-той; unlock нь boundary disabled төлөвийг арилгахгүй. Undo/Redo callback мөн lock шалгана.
- Duplicate section нь хаалттай үлддэг байсан; шинэ duplicate нээлттэй харагдана.

## UI

Section count/empty-state guidance, grouped section/block actions, formatting/insert panels, visible keyboard focus, mobile44px controls, footer save feedback role=status. Approved footer болон explicit temporary-save/publish/reset semantics хэвээр. v40 static frontend module/CSS cache graph; complete graph deploy хийх.

## Баталгаажуулалт

`npm test`:19 test files PASS. Chromium synthetic fixtures:
- editor-frontend.py: empty delete/undo/redo, limits, rich formatting/link Enter, lock/lazy section, responsive.
- publication-workflow.py:5 checks: volatile refresh/temp-save/reset/MN-EN/direct update/empty publish/footer.
- tutorial-media.py:6 checks: real image codecs, invalid files, mock Storage, stale response/actor changes, real editor upload→private autosave.
- problem-dialog.py:17 checks: full748 fixture, numeric search/filter/priority/two-pane/bulk/undo/responsive.
- recovery-flow.py:9 checks: conflict choices/backup/CAS/late logout.
- reader-compat.py:12 checks + no page errors: typed DOM, safe paste, rich edit/code/undo, draft offline/rebase/publish, old body compatibility, scroll/mobile/light-dark.

Reader compatibility test-ийн հին “EN selector-ը պետք է մերժվի” սպասումը փոխարինվեց վերջին user requirement-ով՝ EN editor դատարկ բացվում է, MN-ին վերադառնալուց հին content պահպանվում է։ Draft fixture-ի autosave/offline/rebase checks-ը պահպանված են։

Այս browser tests-ը mock Auth/RPC/Storage են; իրական production account, upload/publish/delete/reset չեն օգտագործել։ Production DB read/write այս task-ում չի արվել։ Migration չի կրկնվել/ավելացվել։ Live/deploy NOT_VERIFIED; main merge/Actions/deploy առանձին են։

## Շարունակություն

Review/merge PR և completev40 deploy, ապա authorized live UI smoke ապահով fixture-ով։ Frontend scope-ի local acceptance PASS-ը չի փակել pending026/027, live Storage permissions, complete admin dashboard/reference-management backlog-ը։ Դրանք չեն անհետացել ledger-ից։ Հաջորդ փաթեթը ինքնաբերաբար չսկսել։
