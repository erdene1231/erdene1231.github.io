# Erdene Club — дэлгэрэнгүй ажлын бүрэн жагсаалт

Гүйцэтгэх үндсэн төлөвлөгөө: [яг8 дэд хэсэг](EIGHT-PART-PLAN.md).185 ажлын задаргаа; багц бүрийг дуусгаад дараагийн хэрэглэгчийн зааврыг хүлээнэ.

2026-10-26. Энэ шинэчлэлт нь шаардлага задлах, төлөвлөх ажил. Код болон production database өөрчлөөгүй.

## Эх сурвалж, уншсан хүрээ, төлөвийн утга

START-HERE.md (220 мөр), requirements-01.txt (1197 мөр), requirements-02.txt (1239 мөр)-ийг эхнээс нь дуустал уншив. Доорх нь эх баримтын өгүүлбэрийг хуулсан хүснэгтээс гадна гүйцэтгэж, хүлээн авах боломжтой ажил болгон задалсан жагсаалт юм. Эх баримтын түүхэн тоо/зааврыг одоогийн нотолгоо болон хэрэглэгчийн сүүлийн шийдвэртэй ялгав.

Эрэмбэ: хэрэглэгчийн хамгийн сүүлийн шийдвэр → START-HERE-ийн нэгтгэсэн нөхцөл → requirements-02 → requirements-01 → хуучин audit. Эх файлуудыг өөрчлөхгүй.

- **L**: тухайн хүрээнд локал хэрэгжилт/тестийн баримт бий; production UI баталгаа биш.
- **D**: DB migration хэрэгжсэн тухай хадгалсан нотолгоо бий; энэ удаа шинээр холбогдож шалгаагүй.
- **A**: аудитлаж баталгаажуулах буюу дутууг нөхөх ажил. Бүгдийг MISSING гэж таамаглаагүй.
- **P**: өмнөх checkpoint-д pending гэж тогтоосон ажил.
- **O**: сонголттой нэмэлт; үндсэн ажлаас өмнө хийхгүй.
- **S**: хуучин заалтыг хэрэглэгчийн сүүлийн шийдвэр орлосон.

`[ ]` нь энэ жагсаалтын хүлээн авах бүх нөхцөл хараахан батлагдаагүйг илэрхийлнэ. Нэг функц L/D байсан ч live/deployed дутуу байж болно. VERIFIED_COMPLETE-д код + холбогдох тест + бодит өгөгдлийн зөв байдал + шаардлагатай live баталгаа орно.

Эх мөр бүрийн stable ID, хуучин төлөв, evidence нь [REQUIREMENTS-CURRENT.json](REQUIREMENTS-CURRENT.json), [DELIVERY-PLAN.json](DELIVERY-PLAN.json)-д хэвээр. Тэдгээрийн 1467 мөр нь **1467 тусдаа feature** гэсэн үг биш. Сэдвийн 319 мөр нь **319 шинэ tutorial** гэсэн үг биш. Жишээ, давталт, alias-ийг чимээгүй хасахгүй; canonical ID/anchor-аар тайлбарлаж холбоно. Автомат keyword ангиллыг семантик аудитын оронд ашиглахгүй.

Одоогийн checkout: `649d76ff7f84a6c8825b327ae9354c20e4785914`, `codex/tutorial-publication-workflow`, PR17. Энэ нь deployment эсвэл merge баталгаа биш. Хамгийн сүүлийн хадгалсан production аудит: 748 problem, 56 tutorial; ZIP-ийн 55 нь түүхэн baseline. Бүх 56 tutorial чанарын review давсан гэж үзэхгүй.

## 00. Өгөгдөл, эх код, нотолгооны суурь

Эх: START §1–4, §12–13; R1 §1,10–11,14–15; R2 §1,9,14.

- [ ] B01 — GitHub checkout/recovery snapshot/live DB гэсэн гурван inventory-г version/hash-тай тулгах. Бүхэл snapshot-оор main эсвэл live custom content-ийг дарж солихгүй. **A; нэгтгэлийн түүх бий.**
- [ ] B02 — Actual tables, columns/types/defaults, constraints, indexes, RLS, functions, triggers, Storage policies-г repository SQL-тай diff хийх; өөрчлөлтийн өмнө шинэчлэх. **A/D.**
- [ ] B03 — Tutorial/problem IDs, URL, solved/progress болон admin revision/body hashes-ийн хамгаалах baseline гаргах. Publish/import бүр expected revision/hash-тай; хүний шинэ засвар байвал conflict, автомат overwrite хийхгүй. **A.**
- [ ] B04 — Applied ledger-ийг content/dependency-аар тулгах. Хэрэгжсэн021–025,028–031-ийг replay хийхгүй. Recovery021 нь production021-тэй нэр/дугаараар адил гэж үзэхгүй. **D.**
- [ ] B05 — Pending026-г numeric/legacy problem keys, optional content, reset/delete/media guards-тай нийцүүлж review хийх. Зөвхөн үнэхээр дутуу delta-г шинэ сул дугаартай migration болгох;032-г эхлээд чөлөөтэй эсэхийг шалгах. **P.**
- [ ] B06 — Pending027 batch-drafts SQL-г одоогийн contracts-тай дахин review хийх; auth, atomicity, revision conflict, partial failure, retry, backup/restore-ийг isolated DB-д шалгах. **P.**
- [ ] B07 — Нэг migration нэг зорилго, dependency, transaction боломж, verify queries, forward-fix/recovery; том content INSERT/schema migration-ийг холихгүй. **A, тасралтгүй дүрэм.**
- [ ] B08 — Versioned JSON/CSV import: configurable small batch, dry-run, schema validation, source dedup, idempotent retry, actionable logs, progress preservation. **A/P.**
- [ ] B09 — tracked MCP client + Start skill-ийг fresh checkout-оос ашиглах заавар; шинэ process initialize, session memory-only, UA хадгалах. Secret/token/session-ийг код/log/ZIP-д оруулахгүй. Repo-д байгаа нь cloud environment image-д бүртгэгдсэн баталгаа биш. **L/A.**
- [ ] B10 — Requirement бүрийн local implementation/test/live/deploy төлөв, evidence, blocker, next action-ийг ялгаж хадгалах. Counts/гарчиг/file presence-ээр COMPLETE өгөхгүй. **A.**

Хүлээн авах: бодит schema diff, applied/pending map, хамгаалах ID/hash snapshot, source-mapped requirement ledger. Account эсвэл progress устгах recovery ашиглахгүй.

## 01. Хэрэглэгчийн сүүлийн editor болон Problems шийдвэрүүд

Эх: ZIP-ийн дараах чатны шийдвэрүүд; audit/PUBLICATION-WORKFLOW.md, NUMERIC-REFERENCES.md, DRAFT-ACTIONS.md, CATALOG-SELECTION-UI.md. Эдгээрийг анхны ZIP-ийн шаардлага мэт тайлагнахгүй.

- [ ] U01 — **Ноорог** footer: Урьдчилан харах | Хадгалах | Нийтлэх | Ноорог устгах. Save амжилттай бол Хадгалагдсан/disabled; edit хийхэд дахин идэвхтэй, failure үед retry боломжтой. **L.**
- [ ] U02 — **Нийтлэл** footer: Урьдчилан харах | Түр хадгалах | Нийтлэх | Reset | Түр устгах. Publish одоогийн засварыг шууд public-д хадгална. **L/D.**
- [ ] U03 — Published editor-ийн Түр хадгалах зөвхөн хувийн editable хувилбарыг хадгална; public-д нөлөөлөхгүй. Товч дараагүй засвар refresh-д арилна; өмнө explicit хадгалсан private draft-ийг сэргээж болно. **L; хуучин unconditional autosave заалтад S.**
- [ ] U04 — Reset засвар байхад идэвхтэй; одоогийн live published хувилбарыг дахин уншиж, өөрийн private draft-ийг цэвэрлэнэ; өөр admin draft/history/progress хэвээр. Анхны түүхэн publish эсвэл бусдын шинэ publish-ийг overwrite хийхгүй; latest published revision-ийг суурь болгоно. **L/D; энэ тайлбар latest implementation тул live acceptance-аар тулгана.**
- [ ] U05 — Түр устгах нь public-оос draft төлөв рүү шилжүүлнэ. Draft үед Түр устгах харагдахгүй, Ноорог устгах харагдана; published үед эсрэгээр. Draft publish → нийтлэл. **L/D.**
- [ ] U06 — Ноорог устгах нь permanent action; dependency/ownership шалгалт, explicit confirmation. Үлдсэн tutorial ID, account/progress өөрчлөхгүй. Бодит production хичээлээр smoke deletion хийхгүй. **L/D.**
- [ ] U07 — Шинэ tutorial хоосон эхэлнэ; нэр заавал, агуулга болон бусад optional field хоосон байж болно. Нэрээс slug ID; numeric fallback үгүй. Хуучин IDs-г дахин нэрлэхгүй. Empty lesson publish хийх боломж нь curriculum quality-pass гэсэн үг биш. **L/D/S.**
- [ ] U08 — Англи хувилбар нэмэх тусдаа товчгүй; Засах хэл selector; MN/EN edit state бие даасан. Хоосон EN-г чанартай translation гэж тэмдэглэхгүй. **L/S.**
- [ ] U09 — JSON backup export/import товч үлдээнэ; manual хувилбар харьцуулах/харьцуулахаас өмнө backup татах товчгүй. Conflict recovery ба дотоод revision evidence хадгалагдана. Single matching-ID import ба bulk import-ийг ялгана. **L; bulk P.**
- [ ] U10 — Preview, bold/italic болон бүх toolbar/footer/section/block товчийг desktop/mobile дээр давтаж шалгах. Time Complexity existing lesson editor load, шинэ хоосон tutorial field visibility-г regression кейс болгох. **L/A.**
- [ ] U11 — Tutorial Input/Output cards: уншихад эвтэй monospace/spacing/header/copy, утга болон copy output яг хэвээр; mobile overflow. **L.**
- [ ] U12 — Бүх problem chooser нэг shared modal: full authoritative catalog, title/internal ID/official ID/tag search, source, own status, tag, min/max, sort; Rating band selectorгүй. **L.**
- [ ] U13 — Main болон popup-д `#1`, `#001` яг internal1-ийг олно;10/100-г дагуулж гаргахгүй. Шинэ reference key numeric, хуучин source|ref уншилтыг дэмжинэ; existing progress/IDs-г дахин дугаарлахгүй. **L/D.**
- [ ] U14 — Popup зүүн талд filtered unselected, баруунд бүх selected; filter reset сонголтыг алдахгүй. Зүүн select-all-filtered; баруун checkbox, select-all, remove-marked/clear; filter сольсон ч сонголт хадгална. Хоёр талд Priority харагдана. **L.**
- [ ] U15 — Main дээр All/01/02/... pack-tab мөргүй; internal collections өгөгдөл/progress устгахгүй. **L/S.**
- [ ] U16 — Tags нуусан ч solved task tags харагдана; unsolved tags нуугдана; tags байгаа/үгүй мөрийн өндөр адил. Main/detail болон view modes-ийг шалгах. **L; өмнөх hide-all-tags заалтад S.**
- [ ] U17 — Hint0/3–3/3 bordered badge яг status-ийн зүүнд;0 ногоон,3 улбар шар, завсрын өнгө шатлалтай, тоо/label-аар ялгарна. Hint use state зөв. **L.**

Хүлээн авах: v39 локал баримтыг дахин ажил хийсэн мэт давтахгүй; deployed version/cache, бодит authorized admin UI, save/reload/reset conflict-ийг зохих fixture-ээр батлах. Одоогоор энэ баримт live deployment батлахгүй.

## 02. Rich editor-ийн анхны бүрэн хүрээг шалгаж хаах

Эх: R2 §4.1–4.10; START §6. U01–U17 өөрчилсөн хэсэгт сүүлийн шийдвэрийг дагана. **Бүх мөр A, зарим нь өмнө L; хэрэгжээгүй гэж нийтэд нь таамаглаагүй.**

- [ ] E01 — H1,H2,H3,H4, paragraph үүсгэх/өөрчлөх; selection/caret хадгалалт.
- [ ] E02 — Bold, italic, underline, strike, inline code; nested formatting, toolbar active state, undo/redo.
- [ ] E03 — Bulleted/numbered list, checklist, blockquote, table, horizontal separator.
- [ ] E04 — External link, stable internal tutorial link, numeric problem link; URL sanitization, missing-target warning.
- [ ] E05 — Callout, warning, important note, example, collapsible section; published renderer-т round-trip.
- [ ] E06 — Section/block add/delete/duplicate/reorder; олон image/code/proof/table-ийг дурын дарааллаар; related problems өгүүллийн дунд.
- [ ] E07 — Reusable Algorithm explanation, Complexity, Proof, Observation, Mistake, Code walkthrough, Example, Priority, Related tutorial, Practice checklist blocks; blank creation-д forced template үгүй.
- [ ] E08 — C++17 болон language selection; syntax highlight, monospace, indentation/auto-indent, copy, long-line scroll, line spacing; code өөрчлөгдөхгүй.
- [ ] E09 — Inline/block MathJax editor preview болон published renderer; literal $, escaping, dynamic rerender, code block-д math боловсруулахгүй.
- [ ] E10 — Array/graph/tree/DP table/segment tree/state transition visual материал; diagram/styled blocks эхний хэрэгжилт байж болно. Interactive visualization сонголттой; script/unsafe SVG/Mermaid-ээс хамгаалах.
- [ ] E11 — File picker + drag/drop PNG/JPEG/WebP; paste боломжийг үнэлж дэмжсэн/дэмжээгүйг тодорхой тайлагнах. SVG зөвхөн sanitizer батлагдвал.
- [ ] E12 — Image preview, resize, align, caption, alt, replace/delete; хэд хэдэн image, mobile phone upload.
- [ ] E13 — Supabase Storage admin-only upload, real role authorization, MIME ба decode/type/size, unique path, safe published delivery, broken asset prevention. Image bytes localStorage-д хадгалахгүй.
- [ ] E14 — Draft/private/history asset access; unused/orphan detection, reference-safe cleanup strategy. Asset устгал нь live/history хэрэглээг эвдэхгүй.
- [ ] E15 — Save indicator, preview-before-publish, unsaved warning, draft autosave/conflict/offline recovery; published explicit-save семантикийг зөрчихгүй.
- [ ] E16 — Revision history, өмнөх хувилбарыг private draft-д restore; latest public-ийг автоматаар сольж нийтлэхгүй. Manual compare товчийг буцааж нэмэхгүй.
- [ ] E17 — Legacy tutorial → editor → save → renderer round-trip; unknown/old field/custom admin content алдагдахгүй.
- [ ] E18 — HTML/Markdown XSS, unsafe link/code/math/image payload, unauthorized user, revoked admin, owner A/B, stale revision/hash тест.
- [ ] E19 — Empty content зөвшөөрсөн ч invalid typed block, dangling reference, unsafe payload, over-limit body-г server талд reject; publish field-errors ойлгомжтой.

Хүлээн авах: функц бүрийн desktop/mobile fixture + save/reload evidence; Storage/auth-д бодит authorized шалгалт тусдаа. Snapshot-ийн isolated test-ийг live upload PASS гэж тооцохгүй.

## 03. Tutorial management ба агуулгын чанарын удирдлага

Эх: R2 §10–11; R1 §13.6; START §6. **A/P.**

- [ ] M01 — Tutorial search, level/category/status filter, last edited date; draft/public ойлгомжтой.
- [ ] M02 — Missing content, practice, prerequisites, EN translation, metadata warning; optional хоосон field-ийг fatal publish error болгохгүй.
- [ ] M03 — Dashboard: чанарын стандарт дутуу, practiceгүй, Priorityгүй, variationsгүй tutorials.
- [ ] M04 — Broken tutorial/source links, duplicate problems, unrated/missing difficulty metadata, unused images.
- [ ] M05 — Tutorial-гүй problem, incomplete100-day assignment, unpublished content; aggregate report нь private draft/PII-г unauthorized хэрэглэгчид харуулахгүй.
- [ ] M06 — Single matching-ID JSON restore-ийн validation/dry-run/confirmation/backup; аюултай өгөгдлийг public-д шууд оруулахгүй.
- [ ] M07 — Multi-record/bulk drafts import/update: schema checks, per-record actionable errors, duplicate detection, revision/hash guard, atomic batch, retry, before-state backup, safe restore. Pending027-г шууд ажиллуулахгүй.
- [ ] M08 — Content review body hash **болон relationship hash**, reviewed date, reviewer record, code tests, sources, known gaps; агуулга өөрчлөгдвөл review stale болно.

Хүлээн авах: dashboard-ын synthetic known-gap fixtures зөв тоологдох; bulk stale/unauthorized/partial failure үед live content өөрчлөгдөхгүй.

## 04. Одоо байгаа tutorial бүрийг чанартай болгох

Эх: R1 §2,12,Эхлэх заавар; R2 §3,11; START §5. **A/P — бүх current lesson-д тус бүр давтана.**

- [x] C01 — Одоогийн56 tutorial-ийн ID/title/status/MN/EN/body hash/prerequisites/practice/variants inventory; actual current content-оос gaps тогтоох.
- [x] C02 — Binary Search-ийн authored draft ба live admin content diff; semantic review, шинэ desktop/mobile math/code/visual review-г дуусгах.
- [x] C03 — Greedy-д мөн адил; exchange proof, counterexample, scheduling болон бусад хэрэглээ үнэхээр заасан эсэх.
- [x] C04 — DP introduction-г гурав дахь жишиг болгон state/transition/invariant/implementation/practice-тай бүрэн review хийх.
- [x] C05 — Tree Basics/LCA/Sparse Table-ийн түүхэн reviewed hashes одоогийн body-той таарч буй эсэх; таарвал баримтыг reuse, өөрчлөгдвөл зөвхөн өөрчлөгдсөн хэсгийг дахин review.
- [x] C06 — Үлдсэн tutorial бүрийг дараах15 агуулгын шалгуур,20 review шалгуураар шалгах; сул хичээлд хэдэн paragraph нэмээд COMPLETE өгөхгүй, шаардлагатайг бүтнээр дахин найруулах.
- [x] C07 — ID/URL/progress/relationships хадгалж, latest admin хувилбартай merge; revision guard-тай жижиг content publish batch.
- [x] C08 — MN найруулга textbook-quality, техник үгс binary search/grid/dp/array хэвээр; машин орчуулгагүй. EN байвал ижил утга/бүтэц/чанартай, дутууг ил тод тэмдэглэх.
- [x] C09 — Бүх reference C++17-ийг compile/run; boundary, overflow/indexing, meaningful brute-force/differential/random tests. Oracle нь implementation-ийн хуулбар биш.
- [x] C10 — Beginner-friendly variable names, spacing/indentation, comments; шаардлагагүй assert, compressed macros үгүй. Суурь Segment Tree recursive, iterative нь variation.
- [x] C11 — Segment Tree/Dijkstra/Tree DP/Digit DP/Flow зэрэг том сэдэвт олон жишээ, олон code section, гүн proof. Ижил template/урт/хиймэл paragraph quota үгүй.
- [x] C12 — Тус бүрийг renderer дээр inspect: proof/math/range notation, code copy/highlight/scroll, diagrams/alt, TOC/anchors, internal/source links.

**Tutorial бүрийн заавал хангах15 агуулгын хэсэг:**

1. Яагаад хэрэгтэй — сурагчид бодит асуудлыг эхэлж үзүүлэх.
2. Naive/brute-force solution болон сул тал.
3. Ажиглалтыг алхам алхмаар нээх.
4. Intuition, algorithm, invariant.
5. Жижиг жишээний бүх алхам/төлөвийн trace.
6. Correctness: invariant/induction/contradiction/exchange/greedy-stays-ahead зэрэг тухайн сэдэвт тохирох proof.
7. Time/space, үйлдлийн тоонд суурилсан intuitive+математик тайлбар; worst/amortized шаардлагатай үед; constraints болон хангалтгүй болох нөхцөл.
8. C++17: data structures, initialization, main logic, updates/transitions, result, complete implementation; хэсэг бүрийн учир.
9. Boundary/edge cases.
10. Common mistakes, жижиг counterexample.
11. Variations, prerequisite, related, advanced, next — canonical links/anchors.
12. Хэзээ хэрэглэх/хэрэглэхгүй; observation, constraints, improving brute force.
13. Warm-up → Standard → Observation → Application → Challenge → Olympiad extension practice.
14. ⭐ Priority сонголт, editor-only rationale; difficulty-тай адилтгахгүй.
15. Дүгнэлт/checklist; унших, ойлгох, код бичих, бодлого бодох/mastery ялгаатай.

**20-item review тус бүрийн evidence:** why, naive, observation, intuition, worked example, correctness, time reasoning, space, C++ implementation, walkthrough, edge cases, mistakes, related, prerequisites, practice, priority, checklist, MN quality, code correctness, working links. Heading/compile байгаа төдийд semantic PASS биш.

Хүлээн авах: tutorial бүрийн body/relationship hashes-тай review card, actual C++ results, source links, MN/EN status, current IDs, browser checks. Editor хоосон нийтлэл зөвшөөрсөн нь энэ curriculum шалгуурыг сулруулахгүй.

- [x] C13 — Багц4-ийн шинэчилсэн сангаас tutorial **бүрд** сэдвийг эзэмшихэд хэрэгтэй practice сонгох: intended solution/observation/prerequisite/stage/objective/rationale-г хянах. Зайлшгүй хэрэгтэй mastery task-ийг High, өндөр өгөөжтэй нэмэлт practice-г Medium зэрэг шалгуураар үнэлж, global problem priority-г үндэслэлтэй өсгөх; бүх attached task-ийг автоматаар High болгохгүй.
- [x] C14 — Нэг task олон tutorial-д ашиглагдвал source-of-truth global priority/rationale shared; local stage/objective тусдаа. Lesson тус бүрийн хувьд essential/useful/extension шалтгааныг хадгалж, publish үед revision guard-тай priority promotion хийх. Relation хасагдлаа гээд global priority-г автоматаар бууруулахгүй; tags/reading/solved events priority өөрчлөхгүй.

## 05. Дутуу бүх сэдвийг prerequisite дарааллаар нөхөх

Эх: R1 §3, R2 §2. **A/P.** Сэдэв бүрийн бүрэн эх жагсаалт доорх хавсралтад байна.

- [ ] T01 — Бүх319 topic mention-ийг canonical lesson ID/anchor/alias reason-тай тулгах; одоогийн coverage зөвхөн нэрээр бус тайлбар/жишээ/proof/practice-тай эсэх.
- [ ] T02 — Prerequisite DAG; self-link, missing target, cycle, unpublished prerequisite-г илрүүлэх. Shared concepts-ийг холбоно; сэдвийг чимээгүй хасахгүй.
- [ ] T03 — Суурь: complexity/STL/array/string/sort/prefix/difference/search/two-pointers/recursion/bitwise/math/proof.
- [ ] T04 — Greedy/observation/constructive: exchange/stays-ahead/scheduling/sweep/event/backwards/invariants/modeling/constraints/counterexamples/offline.
- [ ] T05 — Structures: basic containers → monotonic → DSU/Fenwick/sparse/segment/lazy → persistent/dynamic/merge-sort/wavelet/ordered/Mo/Li-Chao/small-to-large.
- [ ] T06 — Graphs: representation/BFS/DFS → DAG/shortest path/MST → SCC/bridges/biconnected/Euler/functional → matching/flow/mincut/mincost/2-SAT/modeling.
- [ ] T07 — Trees: roots/traversal/diameter/centers/subtrees/Euler → LCA/lifting/distances/DP/reroot → HLD/centroid/virtual/small-to-large.
- [ ] T08 — DP: state/memo/bottom-up/1D/2D/grid/knapsack/LIS/LCS → interval/DAG/tree/mask/digit/profile/SOS/probability/expectation/game → optimizations/modeling.
- [ ] T09 — Strings: matching/prefix/KMP/Z/hash/double-hash/trie → Aho/suffix array/LCP/automaton/Manacher/palindrome/string DP.
- [ ] T10 — Math: primes/sieves/gcd/extended Euclid/mod/inverse/Fermat/Euler/phi/CRT → combinatorics/inclusion/pigeonhole/matrix/recurrences/probability/games/FFT/NTT/polynomials.
- [ ] T11 — Geometry: vector/dot/cross/orientation/intersections/polygon → hull/calipers/closest-pair/sweep/circle/precision/advanced.
- [ ] T12 — Olympiad skills: subtasks/partial scoring/stress/random/debug/interactive/communication/output-only/time management/editorial/failed attempts/transformations/combinations.
- [ ] T13 — R1-only broad labels ба variations-ийг алдалгүй cover: parallel binary search, offline queries, proof-based problem solving, brute-force optimization, advanced graph/tree techniques гэх мэт; exact source appendix-тай тулгах.
- [ ] T14 — Шинэ tutorial бүрд C01–C12 чанарын цикл болон practice matching хамт; fake empty lessons-ээр coverage нэмэгдүүлэхгүй. Нэг том tutorial эсвэл тусдаа variation сонголтыг reasoning-тай бүртгэх.

Хүлээн авах: source topic → canonical ID → anchor → reviewed content/practice/hash гэсэн coverage matrix. 319 мөрийн тоог distinct tutorial quota болгон ашиглахгүй.

- [ ] T15 — Багц3-т tutorial бүрийн Low/Medium/High priority-г хэрэглээ/сургалтын өгөөж/түгээмэл байдлаар rubric+rationale-тай review хийх; Low сэдвүүдийг coverage-оос хасахгүй. Li Chao Tree = Low; beginner/advanced түвшинтэй адилтгахгүй. Practice problems-ийн priority-г мөн багц2-ын mastery/creativity дүрмээр үргэлжлүүлэн review хийх.

## 06. Бодлогын сан, practice холбоос, hints

Эх: R1 §2.10–11,4; R2 §5; START §7. **A/P; numeric-key contract L/D.**

- [ ] P01 — Existing748 catalog-ийн source/official ID/URL/name/tags/rating/hints/tutorial associations audit; gap болон duplicate report.
- [ ] P02 — Source+official ID/normalized URL dedup; site stable numeric ID ба official ID ялгах; concurrent-safe server allocation, хуучин IDs-г renumber хийхгүй.
- [ ] P03 — Recovery BOI17 Toll placeholder-ийг бодит existing/new server ID-тай reconcile; pending ID/749-г таамгаар production-д оноохгүй.
- [ ] P04 — CSES өргөн coverage: Introductory, Sorting/Searching, DP, Graph, Range, Tree, Mathematics, String, Geometry, Advanced Techniques, Additional; official set-тэй gap list. Боломжтой бол бараг бүх relevant set, зохиомол exact quotaгүй.
- [ ] P05 — IOI,EGOI,JOI,APIO,CEOI,COCI,BOI,Balkan OI,USACO,OJ.uz,AtCoder,CF curated tasks; event/year/source нэр, URL, ID-г батлах.
- [ ] P06 — Statement/editorial/intended solution-г судалж primary/secondary topics, prerequisite, learning objective тодорхойлох; tag таарсан гэдгээр attach хийхгүй.
- [ ] P07 — Official CF rating-ийг эхээр шалгах. Non-CF estimated rating-д rationale/confidence/provenance; unknown/unrated тусдаа. Official мэт зохиохгүй.
- [ ] P08 —900–2800 ба2000+ practice хэрэгцээг хангах, илүү хүндийг зөв advanced шатанд;1300–1400 сурагчийн хөгжлийн дараалал.
- [ ] P09 — Tutorial бүр Warm-up/Standard/Observation/Application/Challenge/Olympiad6-stage progression; ихэнхэд5–12 бол чиглэл, сэдэвт тааруулна, hard quota биш.
- [ ] P10 — Priority нь сургалтын өгөөж: core use, important observation, mistakes, new application, next foundation. Editor-only rationale, сурагчид spoilerгүй; hardest/tag-matched-all биш.
- [ ] P11 — Practice attach/remove/order/category/priority/objective admin edit; validated persistent relation, бусад lesson-ийн shared progress-той холбоо.
- [ ] P12 — Problem row/detail metadata: title/source/internal+official IDs/rating type/category/priority/status/tutorial/day/source link; nonexistent-task dead-endгүй.
- [ ] P13 — Missing verified practice tasks-ийг small dry-run import-оор оруулж real ID-тай attach; single/multiple JSON upload, validation/error/dedup, source option автоматаар/гараар нэмэх.
- [ ] P14 — Existing3-level hints нэг бүрийн correctness/gradual reveal/MN найруулга/EN toggle/hide-show audit:1 observation,2 algorithm,3 implementation. Proof/intended solution-той тулгах, full editorial болгож spoiler хийхгүй.
- [ ] P15 — Өмнө hint хэрэггүй гэсэн2000+/HTML batch-д hint хүчээр нэмэхгүй. Original HTML байхгүй бол BLOCKED_SOURCE, өөр бодлогоор сольж done гэхгүй.
- [ ] P16 — Copyright: шаардлагагүй бүтэн statement хуулж хадгалахгүй; verified source links, unavailable metadata pending.

Хүлээн авах: per-task verified provenance/dedup/import ledger, per-lesson matching rationale, hints review, stable IDs/progress. Шинэ quota-г доорх11 хэсэгт тусдаа тоолно.

## 07. 100 хоногийн сургалтын төлөвлөгөө

Эх: R1 §5; R2 §7; START §9. **A — өгөгдөл бий, бүх өдөр чанарын аудит давсан нь батлагдаагүй.**

- [ ] D01 — Яг100 өдөр/10 phase, duplicate/missing dayгүй; current data-г audit, дахин зохиож overwrite хийхгүй.
- [ ] D02 —1–10 foundations/complexity/brute/observation;11–20 sorting/binary/two-pointers/greedy;21–30 prefix/sweep/stacks/structures.
- [ ] D03 —31–40 BFS/DFS/graphs;41–50 DP;51–60 trees/DSU/LCA/treeDP;61–70 segment/Fenwick/range.
- [ ] D04 —71–80 advanced DP/strings/graphs;81–90 olympiad/constructive;91–100 mixed/virtual/review. Prerequisite шалтгаанаар сайжруулж болно, өөрчлөлтийг тэмдэглэх.
- [ ] D05 — Өдөр бүр topic/objective/tutorial IDs/key observations/required/priority/challenge/time estimate/checklist/completion rule.
- [ ] D06 — Бодит published tutorial/problem IDs, missing/archived targetгүй; шинэ canonical lessons-тэй холбоос шинэчлэх, old day IDs/progress хадгалах.
- [ ] D07 — Ихэнх өдөр3–5 problems чиглэлтэй, heavy/mock/review-д ачаалал тохируулах; олон шинэ algorithms шахахгүй, бие даан бодох цаг.
- [ ] D08 — Observation/revision/mixed/virtual/debugging/editorial/subtask days; spaced repetition сэдэв/хугацааны audit.
- [ ] D09 — Start/current day/completed days/%/required solved/tutorial completion/pause-resume/bookmark/past/incomplete persistence.
- [ ] D10 — Tutorial нээсэн төдийд completion/masteryгүй; explicit reading/checklist/required solve rule, logout/login болон device reload-д тогтвортой.
- [ ] D11 — Нэг problem solved event банк/tutorial/day/profile/stats-д нэг эх сурвалжаас шинэчлэгдэх; duplicate solve countгүй.
- [ ] D12 —1300–1400-д бодитой100-day core; бүх advanced сэдвийг шахахгүй. Нэмэлт Advanced/IOI roadmap canonical lessons/prerequisites-тай.

Хүлээн авах:100 мөртэй day-by-day review, dependency/reference validator, workload review, completion/pause/bookmark tests; existing user dates/history хэвээр.

## 08. Profile, activity, statistics

Эх: R1 §6; R2 §8; START §9. **A.**

- [ ] S01 — Нүүр → Profile → Бодлогууд navigation; own/public тусдаа profile route.
- [ ] S02 — Full name,username,avatar,school,bio,joined date; edit зөвхөн owner/authorized admin; private fields leakгүй.
- [ ] S03 — Unique solved, trying, saved-for-later, Priority progress,100-day progress; current tasks-оос шууд үргэлжлүүлэх.
- [ ] S04 — GitHub-style daily heatmap: count/intensity/tooltip, current/longest streak;7/30/365/all-time.
- [ ] S05 — Historical solve timestampгүй бол date зохиохгүй; timezone/day/week boundary, duplicate solve/unsolve/resolved семантик тодорхой.
- [ ] S06 — Solved rating bar chart; official/estimated/unrated ялгаа, highest/average-ийг зөв тооцох.
- [ ] S07 — Tag donut + tag/count legend; multi-tags нийлбэр unique solved-оос их болохыг тайлбарлах, denominator зөв.
- [ ] S08 — Weekly phase date/solved/attempted/highest/average/prev-week change/actual problem list; previous phase navigation.
- [ ] S09 — Submission count,AC/WA/TLE зөвхөн жинхэнэ verdict өгөгдөлтэй үед; manual solved-ийг judge AC гэж нэрлэхгүй, CF stats-тай адилтгахгүй.
- [ ] S10 — Known synthetic histories-оор counts/charts/weekly/timezone/unknown rating/archived tasks шалгах; account switching болон unauthorized access.

Хүлээн авах: chart харагдах төдий биш, урьдчилан бодсон expected counts/series-тэй таарах тест; real PII dumpгүй.

## 09. Problems, Tutorial library/detail, theme/navigation UI

Эх: R1 §7–9; R2 §6; START §8. **A; зарим catalog fixes L.**

- [ ] F01 — Main search/filter/sort эх сурвалж,own status,tag,min/max,priority; exact numeric search. Rating band/pack tabs буцаахгүй; source collections өгөгдлийг хадгалах.
- [ ] F02 — Desktop compact filter panel, mobile collapsible drawer, active filter chips/reset; query/sort/page state зөв, empty/error/loading ойлгомжтой.
- [ ] F03 —100 problems/page, pagination/filter өөрчлөхөд page clamp/reset, compact/comfortable view; row title/source/official ID/rating/primary-secondary tags/status/priority/tutorial холбоос.
- [ ] F04 — Detail: source/difficulty/tags/priority/tutorial/day/3hints/progress/personal notes if present; keyboard/dialog close/focus.
- [ ] F05 — Мянга+ tasks performance: indexes/query strategy/pagination/efficient render, lazy tutorial body; бүх том body-г нэг дор татахгүй; measured payload/render checks.
- [ ] F06 — Library level/category/search/prerequisite indicator/reading progress/recommended order; unready/empty quality status ойлгомжтой.
- [ ] F07 — Tutorial detail title/level/reading time/prerequisites/TOC/anchors/visual/code/complexity/proof/mistakes/variations/priority/next; урт нийтлэл унших typography/spacing.
- [ ] F08 — Sticky TOC боломжтой үед, responsive anchors/navigation; empty content үед fake TOC/reading timeгүй.
- [ ] F09 — MathJax dynamic/static, syntax highlighting/copy, code/table/diagram horizontal overflow; mobile layout/long MN title.
- [ ] F10 — Light palette white/neutral: #FFFFFF/#F8FAFC cards, #E5E7EB borders, #111827 primary, #64748B secondary, forest-green accent; actual contrast шалгах.
- [ ] F11 — Dark үндсэн төрх хэвээр; theme persistence, all Home/Problems/Tutorial/Profile/Plan/Admin consistency; хэт жижиг font/шахцалдсан өнгөт хүснэгтгүй.
- [ ] F12 — Login/signup тусдаа UI, password recovery/session regression; бүх navigation section тусдаа route/page, browser back/deep-link/refresh.
- [ ] F13 — Home professional/simple, “Бодлого ба алгоритм”, Бодлогын сан/Tutorial CTA; CMS compact link Tutorials-ийн хажууд → judge root new tab + noopener noreferrer. Judge SSO/integration хийхгүй.
- [ ] F14 — Desktop/mobile/light/dark keyboard/focus/contrast/overflow/error/offline; хуучин cached frontend/data undefinedгүй, logout/account switching state leakгүй.

Хүлээн авах: page-by-page screenshot/functional matrix + large-catalog measurement; latest tags/hints/picker requirements U12–17 мөн PASS.

## 10. Өмнө ажиллаж байсан функцуудын regression

Эх: START §10. Эдгээрийг шинээр хүссэн feature мэт бүтээхгүй; эхлээд ажиллаж байгааг шалгана. **A.**

- [ ] G01 — Username, immutable email workflow, email-code password recovery, avatar/name/school editing.
- [ ] G02 — Leaderboard unique solved count ба problem solvers list зөв.
- [ ] G03 — Friend request/accept, following дурын user; өмнө тохирсон request/accept auto-follow behavior.
- [ ] G04 — Existing admin seed/roles/grants inspect; admin grant/revoke, server-side auth; бүх хэрэглэгчид admin өгөхгүй. Seed identity-г эх баримтаас, тайланд хувийн мэдээлэл олшруулахгүй.
- [ ] G05 — Admin problem/tutorial CRUD, hint editing, JSON import, source management; revoked-role deny.
- [ ] G06 — Private/public study groups, admin/member хэрэглэгч нэмэх, group access/private report visibility, site-admin moderation.
- [ ] G07 — Report selected dates, optional solved list/count/difficulty/topics/notes; own log edit, group/site-admin moderation, history ownership.
- [ ] G08 — Teacher notes зөвхөн authorized admin, unauthorized edit deny; report/note history зөв.
- [ ] G09 — Excel selected dates (sheet/day), weekdays, students; овог/нэр/solved/count/difficulty/topics/teacher notes. Membership/updated date/note status/school/username columns хассан хэвээр.
- [ ] G10 — A4 LaTeX/PDF compact/multi-column, MN fonts, long notes clippingгүй; same dates/weekdays/students filters; page count/readability.
- [ ] G11 — Hint toggle, dark persistence, stale cache/old schema compatibility, logout/account change, progress retention cross-page.
- [ ] G12 — SMTP асуудал шийдэгдсэн гэж эхэд өгсөн: SMTP/Cloudflare/Ubuntu/CMS configuration-д scope нэмэхгүй.

Хүлээн авах: existing agreed behavior-ийн PASS/FAIL report; засах bug байвал тусдаа regression test, unrelated replacementгүй.

## 11. Бодлогын нэмэлт quota, rating өнгө, importance

Эх: START §11. Сүүлийн хэрэглэгчийн шийдвэрээр эдгээрийг шинэ8 багцын4 дэх багцад хамтад нь дуусгана. Үндсэн curriculum шаардлагыг хасахгүй. **A/P.**

- [ ] X01 — Rating palette800–1100 gray/newbie;1200–1300 green/pupil;1400–1500 cyan/specialist;1600–1800 blue/expert.
- [ ] X02 —1900–2000 magenta/CM;2100–2300 orange/master;2400–2900 red/GM;3000+ black/LGM. Default CF palette руу өөрчлөхгүй.
- [ ] X03 —100-step boundary tests; arbitrary intermediate value mapping-г баримтжуулах, rating-ийг өнгөнд тааруулж өөрчлөхгүй; official/estimate/unrated independent label, dark black contrast, color-blind readable.
- [ ] X04 — Нэмэлт quota эхлэх baseline ID set/provenance freeze; existing edit/duplicate-г шинэ task гэж тооцохгүй. Өмнө баттай оруулсан бол evidence reuse.
- [ ] X05 — **IOI +30**, **EGOI +30**, **JOI +20**, **APIO +15**, **Codeforces +100**, **AtCoder +50** буюу доод нийлбэр245 verified unique new tasks. CF/AtCoder сонголт нь чанартай, сургалтын өгөөж/priority өндөр байна. Тоонууд нь existing source totals биш.
- [ ] X06 — Problem **Low/Medium/High priority**3 түвшин нь хуучин boolean Priority-ийн шинэ хувилбар. Extreme/тусдаа4importance сонголт хийхгүй. DB validation, audited backfill, admin selector, JSON import/export, badge/filter/sort, popup/main/detail бүгд ижил утгатай.
- [ ] X07 — Tutorial мөн **Low/Medium/High priority**3 түвшинтэй: хэрэгцээ/сургалтын өгөөж/түгээмэл хэрэглээ. Problem priority нь topic mastery-д зайлшгүй хэрэгтэй эсэх, бүтээлч observation/логик сэтгэлгээний чанараар өснө; difficulty эсвэл tag match дангаараа өсгөхгүй. Problem/tutorial аль алинд Extreme болон тусдаа давхар importance үүсгэхгүй.

Хүлээн авах: source-specific new-ID quota ledger, verified statements/editorials/source metadata, safe import; problem/tutorial3-tier priority round-trip ба palette boundary/contrast tests.

- [ ] X08 — Багц4-т problem/tutorial priority-ийн canonical3-tier contracts, constraints/indexes/RLS-aware edit, backfill dry-run, import/export compatibility, High→Medium→Low sort, all/level filters, badges/shared popup/learning-card/editor controls. Old boolean metadata/rationale-г audit хийж хадгалж шилжүүлэх; stale overwrite болон progress/ID өөрчлөлтгүй.
- [ ] X09 — Багц4-т existing tutorial inventory-ийн provisional priority audit; **Li Chao Tree = Low**. Багц3-т бүх canonical/new tutorial-ийн priority-г reviewed rationale-тай бүрэн үнэлэх. Related variants/advanced lessons-ийн багатай түгээмэл хэрэглээг topic deletion эсвэл draft болгох шалтаг болгохгүй.

## 12. Сонголттой өргөтгөлүүд

Эх: R1 §13.1–13.5, START §9. **O; үндсэн requirement-ийн оронд хийхгүй.**

- [ ] O01 — Learning path: learner level/progress-д тохирсон next tutorial/problem recommendation; rule болон тайлбар.
- [ ] O02 — Prerequisite graph: canonical DAG харагдах дүрслэл; DFS→traversal→Euler→LCA→HLD жишиг chain.
- [ ] O03 — Review queue: failed/hint-used task-ийг хугацаатай дахин санал болгох; progress data үнэн зөв.
- [ ] O04 — Private problem journal: observation/яагаад гацсан/алдаа/сурсан зүйл; owner-only default.
- [ ] O05 — Tutorial feedback: unclear section/error report, admin review workflow; private мэдээлэл хамгаалах.

Тохиромж/өгөөж/хамаарал/шийдвэрийг бүртгэнэ. Хойшлуулбал OPTIONAL_DEFERRED, үндсэн дутуу ажлыг “optional” болгож нуухгүй. Quality dashboard R2-д заавал тул03 хэсэгт үндсэн хүрээнд орсон.

## 13. Тест, GitHub, deployment, тасралтгүй хадгалалт

Эх: START §12–13; R1 §14–16; R2 §12–14. **Алхам бүрд хэрэгжүүлэх A дүрэм.**

- [ ] R01 — Өөрчлөлтөд тохирох unit/model/browser/SQL tests; өмнөх PASS-ийг өөрчлөлтгүй үед шалтгаангүй давтахгүй.
- [ ] R02 — Auth matrix: anonymous/userA/userB/admin/revoked admin; RLS ownership, RPC validation, conflict/size/unsafe content, Storage draft/public access.
- [ ] R03 — Meaningful C++ compile/execution/proof/content review; browser math/code/image/search/pagination/progress/charts/export desktop/mobile light/dark.
- [ ] R04 — Production өөрчлөлтийн өмнө private before-state/recovery; public Git/ZIP-д PII dump, token, session, service-role/password байхгүй.
- [ ] R05 — Нэг reviewable unit → tests → ledger/topic/migration report → NEXT-STEPS → secret scan → commit. SHA болон branch тодорхой.
- [ ] R06 — Feature branch remote push, existing remote changes overwrite/force-pushгүй; remote SHA дахин уншиж батлах; PR үүсгэж холбоос өгөх. Permissionгүй бол exact blocker.
- [ ] R07 — Downloadable ZIP: эх файлууд, SQL, frontend upload list, apply order, verify/recovery, commit manifest/checksum, continuation; CRC/content/bundle шалгах. Recovery ба deploy-ready release ялгаатай.
- [ ] R08 — Main merge, GitHub Actions deploy, actual deployed frontend/cache version, Supabase applied schema тусдаа status. Commit/push-ийг deploy гэж тайлагнахгүй.
- [ ] R09 — Fresh Codex task GitHub-оос client/Start skill/audit/requirements/content/tests-г авч үргэлжлүүлэх; environment registration ба Git tracking ялгаатай.
- [ ] R10 — Live authenticated smoke хийх эрх/fixture хүрэхгүй бол NOT_VERIFIED/BLOCKED, mock test-ийг live PASS гэж нэрлэхгүй.
- [ ] R11 — Session тасрахын өмнө exact requirement/topic/file/SHA/next command; unfinished work preserved; chat memory цорын ганц эх сурвалж биш.
- [ ] R12 — Final report: tutorials total/existing/new/rewritten/reviewed/pending/canonical/MN-EN/practice/prerequisites; problem baseline/new/source quotas/dedup/rating; editor live;100day/profile/theme/auth/group/export; migrations/Git/PR/deploy/known gaps.

## Blog — шинээр нэмсэн үндсэн хүрээ

Эх: хэрэглэгчийн энэ удаагийн нэмэлт; анхны ZIP-ийн шаардлага биш. **P, хэрэгжилт эхлээгүй.** Blog/comment нь хэрэглэгчийн контент; tutorial admin эрхийг нийт хэрэглэгчдэд нээхгүй.

- [ ] H01 — Navigation-д Blog цэс, тусдаа list/detail/new/edit routes; public нийтлэл унших, өөрийн блог үүсгэж удирдах.
- [ ] H02 — Нэвтэрсэн дурын хэрэглэгч блог бичиж болно; title/body/author/status/timestamps/stable ID; private draft ба public published lifecycle. Owner edit/delete, site-admin moderation, бусдын draft харахгүй.
- [ ] H03 — Blog editor tutorial editor-той бараг адил shared block/formatting бүтэц: headings, bold/italic/lists, tables, links, quote/callout, code, math, images, block add/reorder/delete; tutorial-only practice/curriculum metadata-г заавал шаардахгүй.
- [ ] H04 — Preview/save indicator/unsaved warning/private draft/publish/update; revision conflict хамгаалалт. Existing tutorial save/reset үйлдлийг эвдэхгүй shared components-ийг reuse.
- [ ] H05 — Blog зураг upload тусдаа owner-scoped Storage policy/size/MIME/decode validation; public published asset delivery, draft privacy, reference-safe cleanup. Tutorial admin bucket-д бүх user-д upload эрх өгөхгүй.
- [ ] H06 — Blog list/detail: title, author public identity, date, content; code/math/images responsive rendering, loading/empty/error state. Title/content search ба newest sort-ийг эхний UX шийдэл болгон төлөвлөх.
- [ ] H07 — Upvote/downvote: нэвтэрсэн нэг хэрэглэгч нэг блогт нэг санал; change/undo, unique constraint, server atomic tally, double-click/concurrency зөв; anonymous read-only. Өөрийн блогт санал өгөх эсэхийг хэрэгжүүлэх үеийн тодорхой дүрэм болгон баримтжуулах.
- [ ] H08 — Comment list/create/edit/delete: author ownership, public published блогт comment; draft/hidden блогийн private мэдээлэл leakгүй; admin moderation. Reply threading болон comment voting энэ хүсэлтэд заавал биш.
- [ ] H09 — Comment editor tutorial-тай төстэй shared rich blocks/formatting/code/math/link/image дэмжлэгтэй; plain textarea-аар хязгаарлахгүй. Compact toolbar, preview, draft text recovery, submit errors; blog editor-оос permissions/limits-ийг тусдаа тохируулах.
- [ ] H10 — Blog/comment XSS/unsafe HTML/URL/image protection, body/upload limits, spam/rate-limit хамгаалалт, owner/admin RLS/RPC; tutorial/progress permissions өөрчлөгдөхгүй.
- [ ] H11 — Small additive migrations, indexes, constraints, policy/role tests; userA/userB/admin/anonymous, draft/public/edit/delete/vote/concurrent/comment/upload fixtures. Production бодит контентоор destructive smoke хийхгүй.
- [ ] H12 — Desktop/mobile/light/dark/keyboard, publish/reload/comment/vote error/retry end-to-end; commit/verified push/PR/ZIP/continuation. Бодит live authorization шалгалтгүй бол COMPLETE гэж тэмдэглэхгүй.

Хүлээн авах: хэрэглэгчA блог бичиж нийтэлнэ;B уншиж санал/comment өгнө; санал солих/буцаахад count зөв; зөвхөн owner/admin засна; draft хувийн; tutorial editor болон progress regressionгүй. Vote/comment-ийг хэрэглэгч боломжтой гэж санал болгосныг энэ төлөвлөгөөнд хэрэгжүүлэх хүрээнд оруулсан, одоогоор ажилладаг гэж тайлагнаагүй.

## 14. Яг8 дэд хэсгээр гүйцэтгэх дараалал

Гүйцэтгэх үндсэн8 багц, item mapping, acceptance нь [EIGHT-PART-PLAN.md](EIGHT-PART-PLAN.md), machine-readable нь [EIGHT-PART-PLAN.json](EIGHT-PART-PLAN.json). Эндхийн00–13 болон Blog бүлэг нь дэлгэрэнгүй requirement reference болохоос нэмэлт execution үе шат биш. Өмнөх A0–A14/P0–P8 ангиллыг шинэ8 багц орлоно.

**Нэг удаад нэг багц:** тухайн багцын бүх дэд ажил/тест/баримт/commit/remote verification/ZIP-г дуусгаад тайлагнаж зогсоно. Дараагийн багцыг хэрэглэгч “дараагийн хэсгийг үргэлжлүүл” гэж хэлсний дараа эхлүүлнэ. Багц дотроо олон жижиг migration/content batch/commit хийж болно; энэ нь нэг багцыг орхиж нөгөө рүү үсрэх зөвшөөрөл биш. Runtime тасарвал ижил багцын checkpoint-оос үргэлжлүүлнэ; бүрэн дуусаагүйг дууссан гэж нэрлэхгүй. Blocker байвал тодорхой тайлагнаж, дараагийн багц руу автоматаар шилжихгүй.

Сүүлийн дараалал: **1 →4 →2 →3 →5 →6 →7 →8**. Багц1 frontend checkpoint хийгдсэн; өргөн backlog/deploy/live нөхцөлийг тусад нь хэвээр хадгална. Энэ task зөвхөн шинэ priority/дарааллын төлөвлөгөө; багц4 хэрэгжүүлээгүй.

## 15. Бүх сэдвийн эх жагсаалт — нэг ч нэрийг чимээгүй хасахгүй

Доорх319 мөр нь хоёр эх файлын topic inventory-г яг хадгалсан. Checkbox нь “шинээр tutorial үүсгэ” биш, “энэ шаардлагын утга canonical lesson/anchor дээр бүрэн заагдсан бөгөөд review evidence-тай эсэхийг хаа” гэсэн утгатай. Alias/давталтыг нэг lesson-д нэгтгэж болно; mapping reason заавал. Existing ledger-ийн coverage нь UNVERIFIED тул энэ жагсаалт semantic PASS зохиохгүй.

### Эх 1 — Анхан шат

- [ ] **R1-L0363** — Complexity analysis; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0364** — C++ STL; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0365** — Arrays, strings; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0366** — Prefix sum, difference array; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0367** — Sorting; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0368** — Binary search; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0369** — Two pointers; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0370** — Sliding window; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0371** — Brute force; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0372** — Recursion, backtracking; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0373** — Basic greedy; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0374** — Bit manipulation; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0375** — Basic number theory; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0376** — Basic combinatorics; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0377** — Basic constructive algorithms; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.

### Эх 1 — Дунд шат

- [ ] **R1-L0381** — Coordinate compression; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0382** — Sweep line; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0383** — Monotonic stack/queue; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0384** — DSU; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0385** — BFS, DFS; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0386** — Graph representations; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0387** — Connected components; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0388** — Bipartite graphs; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0389** — Topological sorting; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0390** — Shortest paths; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0391** — Dijkstra; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0392** — Bellman-Ford; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0393** — MST; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0394** — Tree traversal; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0395** — LCA; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0396** — Binary lifting; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0397** — Introductory DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0398** — Knapsack DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0399** — Grid DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0400** — Interval DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0401** — Bitmask DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0402** — Fenwick tree; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0403** — Segment tree; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0404** — Sparse table; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.

### Эх 1 — Ахисан шат

- [ ] **R1-L0408** — Tree DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0409** — Rerooting DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0410** — Digit DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0411** — Profile DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0412** — SOS DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0413** — Divide and conquer DP optimization; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0414** — Knuth optimization; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0415** — Convex Hull Trick; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0416** — Li Chao tree; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0417** — Lazy propagation; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0418** — Persistent segment tree; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0419** — Heavy-light decomposition; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0420** — Centroid decomposition; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0421** — Small-to-large; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0422** — Mo's algorithm; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0423** — Offline queries; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0424** — Parallel binary search; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0425** — SCC; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0426** — Bridges/articulation points; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0427** — Network flow; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0428** — Bipartite matching; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0429** — String hashing; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0430** — KMP, Z-function; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0431** — Trie, Aho-Corasick; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0432** — Suffix array, suffix automaton; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0433** — Modular arithmetic; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0434** — Matrix exponentiation; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0435** — Computational geometry; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0436** — Advanced graph and tree techniques; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.

### Эх 1 — Problem-solving techniques

- [ ] **R1-L0442** — Ажиглалт хийх арга; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0443** — Constraint-аас алгоритм сонгох; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0444** — Greedy шийдлийг нээх; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0445** — Greedy proof; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0446** — Invariant; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0447** — Exchange argument; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0448** — Working backwards; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0449** — Constructive reasoning; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0450** — State design in DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0451** — Brute force optimization; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0452** — Subtask-oriented thinking; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0453** — Partial scoring strategy; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0454** — Debugging; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0455** — Counterexample construction; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0456** — Stress testing; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R1-L0457** — Proof-based problem solving; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.

### Эх 2 — 2.1. Суурь алгоритмууд

- [ ] **R2-L0095** — Time complexity; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0096** — Space complexity; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0097** — C++ STL; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0098** — Arrays; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0099** — Strings; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0100** — Sorting; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0101** — Prefix sum; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0102** — 2D prefix sum; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0103** — Difference array; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0104** — Two pointers; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0105** — Sliding window; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0106** — Binary search; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0107** — Lower bound; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0108** — Upper bound; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0109** — Binary search on answer; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0110** — Binary search on real numbers; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0111** — Brute force; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0112** — Complete search; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0113** — Recursion; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0114** — Backtracking; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0115** — Bitmask enumeration; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0116** — Basic greedy; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0117** — Basic constructive algorithms; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0118** — Frequency counting; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0119** — Coordinate compression; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0120** — Basic combinatorics; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0121** — Basic modular arithmetic; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0122** — Basic number theory; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0123** — Bit manipulation; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0124** — XOR techniques; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0125** — Invariants; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0126** — Basic proof techniques; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.

### Эх 2 — 2.2. Greedy болон Problem-Solving

- [ ] **R2-L0130** — Greedy algorithms; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0131** — Greedy correctness; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0132** — Exchange argument; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0133** — Greedy stays ahead; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0134** — Sorting-based greedy; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0135** — Interval scheduling; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0136** — Sweep line; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0137** — Event processing; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0138** — Working backwards; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0139** — Maintaining invariants; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0140** — Finding observations; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0141** — Constructive reasoning; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0142** — Counterexample construction; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0143** — Transforming problems; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0144** — Mathematical modeling; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0145** — Constraint analysis; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0146** — Improving brute force; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0147** — Case analysis; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0148** — Problem decomposition; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0149** — Offline processing; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.

### Эх 2 — 2.3. Data Structures

- [ ] **R2-L0153** — Stack; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0154** — Queue; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0155** — Deque; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0156** — Priority queue; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0157** — Set and multiset; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0158** — Map and unordered_map; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0159** — Monotonic stack; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0160** — Monotonic queue; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0161** — DSU; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0162** — Fenwick tree; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0163** — Segment tree; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0164** — Lazy propagation; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0165** — Sparse table; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0166** — Range minimum/maximum queries; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0167** — Persistent segment tree; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0168** — Dynamic segment tree; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0169** — Merge sort tree; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0170** — Wavelet tree; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0171** — Ordered data structures; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0172** — Trie; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0173** — Li Chao tree; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0174** — Small-to-large merging; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0175** — Mo's algorithm; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0176** — Advanced offline queries; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.

### Эх 2 — 2.4. Graph Algorithms

- [ ] **R2-L0180** — Graph representations; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0181** — BFS; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0182** — DFS; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0183** — Connected components; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0184** — Bipartite graphs; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0185** — Cycle detection; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0186** — Topological sorting; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0187** — DAG algorithms; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0188** — Shortest paths; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0189** — Dijkstra; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0190** — 0-1 BFS; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0191** — Bellman-Ford; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0192** — Floyd-Warshall; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0193** — Minimum spanning tree; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0194** — Kruskal; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0195** — Prim; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0196** — Strongly connected components; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0197** — Kosaraju; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0198** — Tarjan; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0199** — Bridges; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0200** — Articulation points; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0201** — Biconnected components; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0202** — Eulerian paths; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0203** — Eulerian circuits; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0204** — Functional graphs; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0205** — Binary lifting on functional graphs; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0206** — Bipartite matching; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0207** — Maximum flow; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0208** — Minimum cut; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0209** — Network flow modeling; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0210** — Min-cost max-flow; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0211** — 2-SAT; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0212** — Advanced graph modeling; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.

### Эх 2 — 2.5. Tree Algorithms

- [ ] **R2-L0216** — Tree properties; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0217** — Tree DFS; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0218** — Tree BFS; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0219** — Tree diameter; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0220** — Tree centers; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0221** — Rooted trees; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0222** — Subtree sizes; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0223** — Euler tour; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0224** — LCA; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0225** — Binary lifting; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0226** — Distance queries; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0227** — Tree DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0228** — Rerooting DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0229** — Subtree queries; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0230** — Path queries; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0231** — Heavy-light decomposition; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0232** — Centroid decomposition; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0233** — Tree flattening; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0234** — Virtual tree; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0235** — Small-to-large on trees; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0236** — Advanced tree techniques; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.

### Эх 2 — 2.6. Dynamic Programming

- [ ] **R2-L0240** — DP introduction; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0241** — State and transition design; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0242** — Memoization; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0243** — Bottom-up DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0244** — 1D DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0245** — 2D DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0246** — Grid DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0247** — Knapsack DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0248** — LIS; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0249** — LCS; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0250** — Interval DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0251** — DAG DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0252** — Tree DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0253** — Rerooting; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0254** — Bitmask DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0255** — Digit DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0256** — Profile DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0257** — SOS DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0258** — Probability DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0259** — Expected value DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0260** — Game DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0261** — DP with prefix sums; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0262** — DP with data structures; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0263** — Divide and conquer optimization; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0264** — Knuth optimization; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0265** — Convex hull trick; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0266** — Li Chao optimization; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0267** — Monotone queue optimization; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0268** — State compression; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0269** — Advanced DP modeling; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.

### Эх 2 — 2.7. String Algorithms

- [ ] **R2-L0273** — String matching; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0274** — Prefix function; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0275** — KMP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0276** — Z-function; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0277** — String hashing; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0278** — Double hashing; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0279** — Trie; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0280** — Aho-Corasick; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0281** — Suffix array; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0282** — LCP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0283** — Suffix automaton; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0284** — Manacher; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0285** — Palindromes; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0286** — String DP; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0287** — Advanced string techniques; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.

### Эх 2 — 2.8. Number Theory ба Mathematics

- [ ] **R2-L0291** — Prime numbers; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0292** — Sieve of Eratosthenes; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0293** — Linear sieve; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0294** — GCD and LCM; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0295** — Euclidean algorithm; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0296** — Extended Euclidean algorithm; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0297** — Modular arithmetic; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0298** — Modular exponentiation; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0299** — Modular inverse; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0300** — Fermat's little theorem; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0301** — Euler's theorem; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0302** — Euler phi; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0303** — Chinese remainder theorem; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0304** — Combinatorics; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0305** — Factorials and binomial coefficients; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0306** — Inclusion-exclusion; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0307** — Pigeonhole principle; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0308** — Matrix exponentiation; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0309** — Linear recurrences; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0310** — Probability; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0311** — Expected value; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0312** — Grundy numbers; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0313** — Combinatorial games; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0314** — Fast Fourier Transform; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0315** — Number Theoretic Transform; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0316** — Polynomial algorithms; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.

### Эх 2 — 2.9. Geometry

- [ ] **R2-L0320** — Points and vectors; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0321** — Dot product; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0322** — Cross product; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0323** — Orientation; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0324** — Line intersection; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0325** — Segment intersection; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0326** — Polygon area; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0327** — Point in polygon; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0328** — Convex hull; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0329** — Rotating calipers; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0330** — Closest pair of points; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0331** — Sweep line geometry; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0332** — Circle geometry; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0333** — Computational geometry precision; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0334** — Advanced geometry techniques; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.

### Эх 2 — 2.10. Олимпиадын Problem-Solving Skills

- [ ] **R2-L0338** — Observation-driven problem solving; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0339** — Creative reasoning; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0340** — Subtask-oriented solutions; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0341** — Partial scoring strategy; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0342** — Deriving algorithms from constraints; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0343** — Choosing DP states; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0344** — Greedy proof; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0345** — Constructing counterexamples; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0346** — Stress testing; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0347** — Random test generators; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0348** — Debugging C++; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0349** — Interactive problems; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0350** — Communication tasks; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0351** — Output-only tasks; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0352** — Contest time management; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0353** — Editorial analysis; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0354** — Learning from failed attempts; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0355** — Recognizing problem transformations; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.
- [ ] **R2-L0356** — Combining multiple algorithms; canonical ID/anchor: аудитлана; coverage: UNVERIFIED.

## 16. Анхны мөр бүрийн бүрэн traceability

1467 эх мөрийн ID/source/line/section/requirement/status/evidence/next болон319 сэдэв нь REQUIREMENTS-CURRENT.json болон DELIVERY-PLAN.json-д хэвээр. Энд ажлын багц болгон нэгтгэсэн нь эх мөрийг устгах, бүгдийг complete болгох, эсвэл эхийн жишээг шинэ feature болгох зөвшөөрөл биш. START-HERE220 мөрийн нэмэлт constraints-ийг00–14 хэсэгт оруулсан; эх файлыг бүтнээр нь audit/requirements-source/START-HERE.md-ээс уншина.


## Package 2 tutorial sub-workstream reconciliation

All 55 existing non-Mongolia lessons are published and reconciled against current anonymous bodies. C01–C14 above are closed for this existing tutorial scope using individual lesson semantic/code/reader evidence plus audit/PACKAGE02-TUTORIAL-RECONCILIATION.json. The bounded reconciliation is not a substitute for those reviews or a claim of user acceptance. Current sorting revision 7 and its previously verified code are preserved; Mongolia remains unpublished revision 2, unchanged against fresh guards. No missing package 3 topics were created. The interactive/communication bank follow-up remains incomplete, so package 2 is not complete.


## Handbook Tree queries — verified 2026-10-29

Existing `lca` revision 7/history 230 is published and anonymously verified after PR #130. LCA-first ordering, full chapter 18 examples/subtopics and requested static edge/vertex path aggregates are complete. Original rewrite cycle: 16/55 public-verified, 39 remaining; Introduction and SCC are separate additions. Catalog stays 58 stored/57 public tutorials and 1010 problems. All unrelated rows, eight drafts, learner and authority state are unchanged. See TREE-QUERY-PUBLICATION-RECEIPT; its successful one-time SQL must never be replayed. No deferred feature was implemented and owner acceptance is not inferred.


## Handbook Paths and circuits — verified 2026-10-29

New `paths-circuits` revision 1/history 231 is public-verified after PR #132 and v65 deployment. Contains all four chapter 19 subsections with exact source routes/boards, five explained C++17 programs, 931 UBSan runs, native MN/EN roundtrips and guarded publication checks. Medium tutorial priority; only two new tutorial-core relationships, no global problem-priority updates. All prior 58 rows, eight drafts, Mongolia, 1010 problems, learner/profile and authority state are unchanged. Original cycle 16/55; three separate new additions; 59 stored/58 public. See PATHS-PUBLICATION-RECEIPT; successful SQL must never be replayed. All three deferred features remain deferred, no owner acceptance inferred.


## Handbook Flows and cuts — verified 2026-10-29

New `flows-cuts` is published revision 1 / history 232 after PR #134 merge `114bd513b7f17f0bd700bd3198636b0e3c5fa073`. Pages run 40890724209 succeeded; 15 v66 assets match deployed bytes under normal TLS. Exact anonymous body matches the reviewed candidate. All prior 59 tutorial rows, eight private drafts, Mongolia, 1010 problems, learner/profile and authority fingerprints remain unchanged. Catalog: 60 stored / 59 public.

The complete chapter 20 retains all four source subsections, residual cancellation, max-flow/min-cut proof, disjoint paths, matching/Hall/Kőnig and DAG covers/Dilworth, with 32 native diagrams, four explained C++17 programs, 766 independent UBSan/oracle executions and 246 passing Node tests. Native MN/EN editor round-trips and responsive/theme reader checks passed. See audit/PACKAGE03-FLOWS-PUBLICATION-RECEIPT.json. No live authenticated/browser visual success or owner acceptance is inferred.

One-time SQL SHA-256 `0364e5de9e23e9e84761ab9a4bc1053e23eb7605b52efc8c4da9ee58d81ccd63` SUCCEEDED; NEVER REPLAY. No migration, security, editor or deferred-feature changes. Original rewrite cycle remains 16/55, with 39 remaining; Introduction, SCC, Paths/circuits and Flows/cuts are four separate additions. Next is full source chapter 21 Number theory: map its complete source to stable existing IDs and fresh owner/draft guards before editing. All three deferred backlog features remain deferred. Never submit GitHub APPROVE reviews without specific confirmation.


## Handbook Number theory and visible order — verified 2026-10-29

Stable `number-theory` is published revision 7 / history 233 after PR #136 merge `3e67536fdf37310b81eefb8d0141ec23b5a3c268`. Pages run 40895484781 succeeded; all nine v67 affected assets match deployed bytes under normal TLS. The exact anonymous public body matches the reviewed candidate. All other 59 rows, all eight private drafts, Mongolia, 1010 problems, learner/profile and authority fingerprints remain unchanged. Catalog: 60 stored / 59 public.

The full chapter 21 retains its four source subsections and worked examples, adding six explained C++17 programs with 719 independent UBSan/oracle executions. Full Node suite: 249 passed; final affected tests and native MN/EN reader/editor checks passed. Historical 33-cube/proof slips and numeric-domain issues are corrected without dropping the examples. Existing target priority, prerequisites, practice and focused gcd/sieve/fast-power IDs are preserved. See NUMBER-REVIEW and NUMBER-PUBLICATION-RECEIPT.

Actual default Tutorials order now follows handbook chapters across levels. Main topics show source chapter numbers; focused extras have unnumbered Supplement / Нэмэлт labels beside their containing topic. Explicit priority sorting and all filters remain. Native listing tests verify all 59 public identities, both responsive/theme cases and priority controls; deployed v67 files match. No security, schema, bank metadata, editor or deferred-feature changes.

One-time SQL SHA-256 `60b3cfc09ebb0a6a6912c8f496137420354bc5d467d70f4f0d1ce13571a5ca17` SUCCEEDED; NEVER REPLAY. Original handbook rewrite cycle: 17/55 public-verified, 38 remaining. Introduction, SCC, Paths/circuits and Flows/cuts remain four separate additions. Next is full chapter 22 Combinatorics: read actual source, map to stable existing IDs and use fresh guards before editing. No owner acceptance or live authenticated/browser visual success is inferred. Never submit GitHub APPROVE reviews without specific confirmation. All three deferred backlog features stay deferred.


## Handbook Combinatorics — verified 2026-10-29

Stable `combinatorics` is published revision 7 / history 234 after PR #138 merge `d1c0a3ca7a0715ff573227bad81d0962ca54f791`. Pages run 40900464206 succeeded; all nine existing v67 runtime assets match deployed bytes under normal TLS. Exact anonymous public body matches the reviewed candidate. All other 59 stored rows, all eight private drafts, Mongolia, 1010 problems, learner/profile and authority fingerprints remain unchanged. Catalog stays 60 stored / 59 public.

Full chapter 22 retains all five source main subsections and worked examples, plus the prelude and preserved mastery/independent practice. Seven explained C++17 programs pass 676 independent UBSan/oracle executions, including all Prüfer codes through five vertices versus independently enumerated tree edge sets, a 200000-vertex chain and 1000000 factorial/derangement boundary. Full Node suite: 251 passed; final affected tests and native MN/EN editor/reader checks pass. All 34 graphs and four grids preserve examples including 10/15/6 box placements, Catalan ordered shapes, four necklace rotations, 16 labeled trees and [4,4,2] Prüfer trace. No MathJax errors, node collisions or document overflow in native theme/mobile tests. See COMBINATORICS-REVIEW and COMBINATORICS-PUBLICATION-RECEIPT.

One-time SQL SHA-256 `099799d43f146d1602c1b8e4ffbcd7488bb1691e011632f5bc9d84a93d7404aa` SUCCEEDED; NEVER REPLAY. No migration, runtime/editor/security/bank or deferred-feature changes. Existing target priority, prerequisites, practice and relationships are exact preserved, as is deployed handbook listing order/source numbering v67. The language glossary records genuinely read contextual Mongolian teaching sources without claiming an official standard.

Original handbook rewrite cycle: 18/55 public-verified, 37 remaining. Introduction, SCC, Paths/circuits and Flows/cuts remain four separate new additions. Next is full source chapter 23 Matrices: inspect the full source and current stable-ID inventory before deciding the containing lesson; preserve focused existing topics and private edits. No owner acceptance or live authenticated/browser visual success is inferred. All three deferred backlog features stay deferred. Never submit GitHub APPROVE reviews without specific confirmation or replay any successful publication/migration.


## Handbook Matrices — verified 2026-10-29

New stable `matrices` is published revision 1 / history 235 after PR #140 merge `458df7dc116a9c76fff79b3cfb9963db036115a8`. Pages run 40905886414 succeeded; all 16 v68 runtime/JSON assets match deployed bytes under normal TLS. Exact anonymous body matches the reviewed candidate. All previous 60 stored rows, all eight private drafts, Mongolia, 1010 problems, learner/profile and authority fingerprints remain unchanged. Catalog: 61 stored / 60 public.

The full chapter 23 retains all three source main subsections, original matrices/derivations, Fibonacci/companion states, four-edge walk counts/costs and Kirchhoff’s three trees. Seven explained C++17 programs pass 670 independent UBSan/oracle executions, including exact rational inverses, dense dimension80 overflow boundaries and dimension 150 Kirchhoff. Full Node suite: 254 passed; final content/atomic/cache tests and native MN/EN editor/reader checks pass. Six graphs and three colored grids pass responsive/theme checks, with zero MathJax errors or document overflow. Source walk-versus-simple-path, numeric inverse domains and principal-minor/cofactor signs are explicit. See MATRICES-REVIEW and MATRICES-PUBLICATION-RECEIPT.

One-time SQL SHA-256 `6408821f7801ab2e9c4a63ef4217f35f0302102b7325d1138e338f80fefb03f9` SUCCEEDED; NEVER REPLAY. No migration/security/editor/bank/deferred-feature changes. Chapter 23 follows Combinatorics in actual default listing; v68 updates only its curriculum/order import closure and preserves grid 62/graph 63 fixes. Matrix-exponentiation is contained here rather than a duplicate future lesson. Existing primary-topic mappings and 100-day plan are unchanged; only new tutorial-local practice relations were added.

Original handbook rewrite cycle stays 18/55 public-verified, 37 remaining. Separate new additions are Introduction, SCC, Paths/circuits, Flows/cuts and Matrices: 5 total. Next is full source chapter 24 Probability: inspect actual source and current stable-ID inventory before authoring. No owner acceptance or live authenticated/browser visual success is inferred. All three deferred backlog features remain deferred. Never submit GitHub APPROVE reviews without specific confirmation or replay any successful job/migration.


## Full curriculum reconciliation — read-only audit, 2026-10-29

See `audit/PACKAGE03-CURRICULUM-RECONCILIATION.md` and its JSON for the complete 55-ID inventory and continuation batches. Fresh anonymous retrieval confirms 65 public lessons: 21 rewritten originals + 34 remaining originals + 10 separate additions. All 31 new-cycle completed bodies match their latest successful publication receipts; all 34 remaining bodies are exact unchanged since the pre-Introduction snapshot. Conceptual coverage inside a containing chapter and historical package2 review do not count as new standalone completion. Mongolia remains excluded. No production or GitHub mutation occurred during this audit.

Next concrete batch: binary-search, lower-bound, upper-bound, followed by binary-search-answer, using full source 3.3 and focused existing IDs/practice. Do not republish completed Sorting or any prior SQL. Continue containers → recursion → DP → amortized/range → bit/traversal/shortest/tree/DSU → arithmetic → string additions → unnumbered methodology, as mapped in the report. All 34 stable IDs are explicitly assigned.

Outstanding focused additions: bridges/articulation, HLD, centroid decomposition, digit DP, grouped DP optimizations, Aho, suffix array/adjacent LCP, interactive/communication. Existing KMP/Z/rolling hash, static LCA-first binary lifting, functional graphs, SCC/2SAT, Euler and flow/matching are substantive published coverage; no duplicate lessons needed. HLD/Aho/suffix array are not implemented just because backlog labels or general substring-LCP code exist.

Audit found one confirmed visible numbering mismatch: chapter9 is currently assigned to old prefix-sums, while the full published Range queries body is segment-tree and appears as a supplement. Plan a later narrow tested mapping/order fix, preserving both IDs/progress. This audit changed no runtime. Binary-search-answer placement after Greedy can be aligned with chapter3 supplements in its batch. Historical generic backlog duplicates (flow/matching, Mo/offline, persistent) are not new mandatory lessons. The 118-section source ledger publication fields are reconciled locally; original completion still uses the 55-ID ledger.

Chapter30 is the last numbered handbook chapter; no chapter31. Package3 remains incomplete. Preserve all private drafts/user edits/learner records/problems and three deferred UI items; no security expansion, APPROVE review or successful SQL replay. This audit does not infer owner acceptance or claim authenticated live visual verification.


## Search supplements and chapter9 mapping — verified 2026-10-29

PR156 merged as `4d3e6892ee2adf42db75b3fcad0f5b40d248cc89`, including the prior local reconciliation608c727. Pages40949247000 succeeded; all16 cache75 runtime/JSON files match default-TLS deployed bytes. Existing binary-search revision8→9/history244, lower-bound2→3/history245 and upper-bound2→3/history246 published atomically at20:27:59UTC. Exact anonymous MN/EN bodies match reviewed candidates. Catalog remains66 stored/65 public; all63 non-target rows, all8 private drafts (one target draft),1010 problems, learner/profile and authority fingerprints are exact unchanged. No draft rebase, migration/security/editor feature or deferred UI work.

The standalone lessons retain distinct purposes: exact membership with closed interval/jump halving; first not-less boundary; first strictly-greater boundary/equal counts. Full original MN/EN reasoning/traces, master/independent practice and compact int/ll C++17 fragments before full programs.278 Node tests plus final3;4283 array cases/96817 naive+stdlib comparisons under UBSan, exhaustive ternary arrays through length7,1000 random arrays,200000 elements and ll endpoints. Native MN/EN editor and responsive/theme reader checks pass, including actual anonymous public-body fixtures. Chapter9 now correctly labels full Range queries at segment-tree, before unnumbered prefix-sums; all IDs/progress/sort options preserved and visible regression tested.

One-time exact three-target SQL SHA256 `8403a2c959fa1988ca4381e859763605f8af06714f51a1d5267d774e56fcdd3f` SUCCEEDED; NEVER REPLAY. Private recovery/intent/result: `/workspace/package03-search-execution`; exact post-state/anonymous/deployed evidence: `/workspace/package03-search-postpublish`. Safe receipt: `audit/PACKAGE03-SEARCH-PUBLICATION-RECEIPT.json`. Initial metadata SELECT preparation had a syntax error, corrected before any content write; no bypass or auth impersonation. No APPROVE review or certificate bypass. Local native and anonymous/file checks do not imply owner acceptance/authenticated live visual success.

Current original handbook cycle24/55 verified,31 remaining; separate additions stay10. Full55-ID reconciliation JSON/Markdown updated with only these three completion credits. Next original: binary-search-answer, then stack-queue/priority-queue in handbook order. Preserve all other remaining originals and eight explicit pending focused additions (bridges/articulation,HLD,centroid,digitDP,DP optimizations,Aho,suffix-array/LCP,interactive/communication). No chapter31 or package5; book chapter30 is final. Never replay any prior successful publication or035/036/037; no deferred UI implementation.


## Binary search on answer — verified 2026-10-29

Existing binary-search-answer is published revision4→5/history247 at20:49:26UTC after PR158 merge `042a18cc482b8526754f1731d20eb9cdaa731fbd`. Pages40952387283 succeeded; all16 existing cache75 runtime/JSON assets match default-TLS deployed bytes. Exact anonymous MN/EN body and its native reader/editor fixture pass. Catalog stays66 stored/65 public, with all65 non-target rows, eight private drafts,1010 problems, learner/profile and authority fingerprints exact unchanged. No target draft, migration/security/editor or deferred UI change.

Full standalone rewrite derives monotone feasibility, first-true bounds and last-true contrast, preserving machine3/2/5 goal7→8 and adding rope4/7/9 k5→3. Two exact explained C++17 programs use safe remaining-demand predicates, deliberate int/ll and overflow-safe lower/upper midpoints through LLONG_MAX.281 Node tests plus final3 pass;1445 array cases,114218 brute-force optimum and942300 predicate checks under UBSan plus200000-item/extreme/all/no feasible/endpoint/complete IO tests pass. Both predicate and final answer are independently checked. Bounded−1 means no answer inside[0,B], not global impossibility. Source attribution remains centralized and flexible native MN/EN teaching is used.

One-time SQL SHA256 `ac1408489721b4aeb3d4981f392b811cddd7ee3e3e714a11369b9256cedcd249` SUCCEEDED; NEVER REPLAY. Private recovery/intent/result: `/workspace/package03-answer-execution`; post-publication proof: `/workspace/package03-answer-postpublish`. Safe receipt: `audit/PACKAGE03-ANSWER-PUBLICATION-RECEIPT.json`. Preserve search histories244–246 and all prior successful publications/migrations. No APPROVE review, credential/access change, Auth impersonation or certificate bypass; no owner acceptance/authenticated live visual claim.

Actual prerequisite review found Greedy is still required for this focused lesson/practice. Preserve its post-Greedy placement; full chapter3.3 is already in Sorting. No runtime reordering/cache increment was necessary; chapter9 correction and default book chapter sequence remain intact.

Original handbook cycle now25/55 verified,30 remaining;10 separate additions unchanged. All35 completed live bodies match receipts and remaining30 retain their previous bodies. Full inventory/checklist updated with only one completion credit. Next coherent batch: stack-queue and priority-queue, then recursion in source order. Keep all remaining original IDs and eight pending explicit groups (bridges/articulation,HLD,centroid,digitDP,DP optimizations,Aho,suffix-array/LCP,interactive/communication). Preserve Mongolia/private drafts/learner data/problem bank and three deferred UI tasks; no package5 or chapter31.
