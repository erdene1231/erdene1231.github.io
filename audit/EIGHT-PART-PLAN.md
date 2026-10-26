# Erdene Club — гүйцэтгэх8 дэд хэсгийн төлөвлөгөө

Энэ нь хуучин P0–P8/A0–A14 execution ангиллыг орлоно. Дэлгэрэнгүй эх checklist: [MASTER-WORK-CHECKLIST.md](MASTER-WORK-CHECKLIST.md). Эх файлууд болон1467 мөр/319 сэдвийн traceability-г устгаагүй.

**Нэг багцыг бүрэн дуусгаад зогсоно. Дараагийн багцыг зөвхөн хэрэглэгчийн дараагийн заавраар эхлүүлнэ.** Багц дотроо жижиг, шалгагддаг commits/migrations/content batches хийнэ. Нэг хичээл/нэг commit нь бүх багц дууссан гэсэн үг биш. Runtime хүрэхгүй бол ижил багцын checkpoint-оос үргэлжлүүлнэ.

## Нэмэлт бодлогын quota

| Source | Шинээр нэмэх доод тоо | Сонголт |
|---|---:|---|
| IOI |30| Verified, сургалтын өгөөжтэй |
| EGOI |30| Verified, сургалтын өгөөжтэй |
| APIO |15| Verified, сургалтын өгөөжтэй |
| JOI |20| Verified, сургалтын өгөөжтэй |
| Codeforces |100| Чанартай, priority өндөр recommended |
| AtCoder |50| Чанартай, priority өндөр recommended |

Доод нийлбэр **245 шинэ unique бодлого**. Өмнөх quota-г давтаж баталсан болохоос дахин нэмж30/30/15/20/100 давхар импортлох хүсэлт биш. CF100+, AtCoder50+ зорилтод илүү нэмж болно; duplicate/edit-ийг шинэ гэж тооцохгүй. Baseline IDs ба source provenance-г freeze; өмнө баттай импортолсон кредит байвал evidence-тай reuse.

## Rating өнгө — багц4

800–1100 саарал;1200–1300 ногоон;1400–1500 cyan;1600–1800 blue;1900–2000 magenta;2100–2300 orange;2400–2900 red;3000+ black. Official/estimated/unrated label тусдаа; dark contrast болон boundary tests.

## Priority-ийн шинэ үндсэн дүрэм

Эх: хэрэглэгчийн сүүлийн2 нэмэлт. Хуучин boolean Priority болон4түвшинтэй importance төлөвлөгөөг орлоно. **Problem, tutorial тус бүр зөвхөн Low / Medium / High**; difficulty-гаас тусдаа. Код/DB энэ checkpoint-д өөрчлөгдөөгүй.

| Түвшин | Problem | Tutorial |
|---|---|---|
| High | Сэдэв эзэмшихэд зайлшгүй хэрэгтэй, эсвэл маш бүтээлч бөгөөд чанартай логик/observation шаарддаг | Өргөн хэрэглээтэй, олон чухал сэдвийн суурь, суралцах өгөөж өндөр |
| Medium | Сайн бататгал/шинэ хэрэглээ боловч зайлшгүй цөм биш | Ашигтай боловч илүү тусгай хэрэглээтэй, тодорхой шатанд хэрэгтэй |
| Low | Хязгаарлагдмал нэмэлт өгөөжтэй эсвэл тусгай practice; чанаргүй гэсэн үг биш | Ховор хэрэглээтэй, нарийн advanced extension; **Li Chao Tree = Low** |

Hard rating = High priority гэсэн дүрэм үгүй. Бүх practice task-ийг High болгохгүй. Tutorial Low байсан ч түүнд зориулагдсан problem mastery-д зайлшгүй бол High байж болно; хоёр entity-ийн үнэлгээг шууд хуулж болохгүй. Багц4-т contracts/UI/legacy conversion, багц2-т existing lesson practice+problem priority review, багц3-т бүх canonical/new lesson priority+practice review-г дуусгана.

**Багц4-ийн ажил:**

- Problem болон tutorial-д validated3-tier field, safe migration/backfill, revision/auth guards; бодит schema-г эхэлж уншина, applied migration replayгүй.
- Admin editor selector, JSON export/import, list/detail/cards/shared picker badges; all/Low/Medium/High filters, priority sort. Хуучин “⭐ Priority л харах” нь High-тэй нийцэх display/filter болно; legacy data/rationale-г transition audit-гүй арилгахгүй.
- Existing boolean утгаас audited mapping хийнэ, хуучин true бүгд бодитоор High гэж нотолгоогүй зарлахгүй. Үндэслэлгүй default/rank таамаглахгүй; missing values-ийг backfill review ledger-т шийднэ.
- Existing tutorial inventory-г baseline priority review хийх, Li Chao Tree Low-г хадгалах. Багц3 дараа нь бүх сэдвийн бүрэн editorial үнэлгээг хийнэ.
- Migration dry-run, import/export round-trip, all filters/sort/popup labels, concurrency/stale updates, IDs/progress before-after checks.245+ verified task quota болон rating palette хэвээр.

**Багц2-ийн ажил:** tutorial бүрийн intended solution/observations/prerequisites-т тохирох mastery practice сонгох,6-stage progression/objective/rationale. Essential task-ийг High болгох, бусад хэрэгтэй task-ийн priority-г өгөөжөөр өсгөх; mere attach нь automatic promotion биш. Global problem priority нь нэг эх сурвалжтай; тухайн lesson-ийн stage/objective/selection rationale тусдаа. Нэг lesson-оос салгахад бусад lesson-д хэрэгтэй task-ийг автоматаар downgrade хийхгүй.

**Багц3-ийн ажил:** хичээл бүрийн priority-г usefulness/necessity/frequency rubric+rationale-тай баталгаажуулах. Low topic-ийг хөтөлбөрөөс хасахгүй; шинэ хичээлийн practice priority-д багц2-ын дүрэм үйлчилнэ.

**Өмнөх багц1 backlog:** frontend ажил local verified, PR18 merged нь GitHub-оор батлагдсан; deploy/authenticated live check тусдаа. Багц4 эхлэхдээ түүнд үнэхээр шаардлагатай schema/auth/reference dependencies-г шалгаж хаана. Хамааралгүй pending026/027-ыг сохроор prerequisite болгохгүй, шаардлагатай safety-г алгасахгүй. Энэ өөрчлөлт бүгдийг complete болгосон гэсэн үг биш.

## Багцууд

### 01. Tutorial editor, өгөгдлийн аюулгүй суурь ба admin удирдлагыг дуусгах

**Хийх ажил:** Actual schema/hash audit, pending026/027 зөвхөн дутуу delta, RLS/media/import; сүүлд тохирсон footer/save/reset/empty lesson, rich editor, Storage, backup/bulk/dashboard, library/detail.

**Checklist IDs:** B01, B02, B03, B04, B05, B06, B07, B08, B09, B10, U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, E01, E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, M01, M02, M03, M04, M05, M06, M07, M08, F06, F07, F08, F09.

**Дууссан гэж үзэх нөхцөл:** Legacy/custom content round-trip; role/conflict/import/Storage/editor desktop-mobile tests; бодит live authorization баталгаа эсвэл ил тод blocker; IDs/progress хэвээр.

**Хаахдаа:** тохирох тест, requirement evidence, migration/content ledger, commit, verified push/PR, downloadable ZIP/checksum, NEXT-STEPS; дараагийн багцыг эхлүүлэхгүй.

### 04. Бодлогын сан, нэмэлт245+, rating өнгө ба Problems UI

**Хийх ажил:** Existing catalog/CSES/international provenance/dedup/hints audit; IOI30+, EGOI30+, APIO15+, JOI20+, CF100+ high-priority, AtCoder50+ high-priority; rating palette, problem/tutorial Low/Medium/High priority; shared numeric progress, popup/search/tags/hints/performance.

**Checklist IDs:** P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13, P14, P15, P16, X01, X02, X03, X04, X05, X06, X07, X08, X09, F01, F02, F03, F04, F05.

**Дууссан гэж үзэх нөхцөл:** Source-specific NEW unique ID ledger quota бүр хүрсэн; repeated request-г давхар тоолоогүй; official/estimated/unrated зөв; palette boundary/contrast, hints/relations/picker/filter/performance/progress tests.

**Хаахдаа:** тохирох тест, requirement evidence, migration/content ledger, commit, verified push/PR, downloadable ZIP/checksum, NEXT-STEPS; дараагийн багцыг эхлүүлэхгүй.

### 02. Одоо байгаа бүх tutorial-ийг чанарын стандартад хүргэх

**Хийх ажил:** Current inventory; Binary Search → Greedy → DP жишиг; дараа нь бусад бүх existing lessons-ийн review/rewrite.15 агуулгын хэсэг,20 чанарын шалгуур, MN/EN, C++17 proof/tests; багц4-ийн сангаас tutorial бүрд mastery practice нэмэх, essential/creative task priority-г rationale-тай өсгөх.

**Checklist IDs:** C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, C12, C13, C14.

**Дууссан гэж үзэх нөхцөл:** Lesson бүр body/relationship hash-тай semantic review, C++ tests, source/practice links, browser review; existing IDs/admin засвар/progress хадгалагдсан. Нэг хичээл дууссан нь энэ багц дууссан гэсэн үг биш.

**Хаахдаа:** тохирох тест, requirement evidence, migration/content ledger, commit, verified push/PR, downloadable ZIP/checksum, NEXT-STEPS; дараагийн багцыг эхлүүлэхгүй.

### 03. Дутуу бүх алгоритм, сэдвийн tutorial санг бүрэн нөхөх

**Хийх ажил:** 319 эх topic mention → canonical lesson/anchor mapping; prerequisite DAG; foundations/greedy/structures/graphs/trees/DP/strings/math/geometry/olympiad skills, variations, practice; tutorial бүрийн3-tier priority/usefulness/frequency review, Li Chao Tree Low.

**Checklist IDs:** T01, T02, T03, T04, T05, T06, T07, T08, T09, T10, T11, T12, T13, T14, T15.

**Дууссан гэж үзэх нөхцөл:** Эх сэдэв бүр reviewed teaching coverage эсвэл justified alias/anchor-тай; missing topic үлдээгүй; lesson бүр quality/code/practice tests.319 нь319 шинэ tutorial гэсэн үг биш.

**Хаахдаа:** тохирох тест, requirement evidence, migration/content ledger, commit, verified push/PR, downloadable ZIP/checksum, NEXT-STEPS; дараагийн багцыг эхлүүлэхгүй.

### 05. 100 хоногийн төлөвлөгөө ба Advanced/IOI roadmap

**Хийх ажил:** Exactly100 days/10 phases; objective/tutorial/problem/observations/priority/challenge/time/checklist, realistic1300–1400 workload, review/virtual/subtasks; start/pause/resume/bookmark/completion.

**Checklist IDs:** D01, D02, D03, D04, D05, D06, D07, D08, D09, D10, D11, D12.

**Дууссан гэж үзэх нөхцөл:** Өдөр бүр reference/prerequisite/workload review PASS; persisted completion зөв; read≠mastery; old day IDs/progress хадгалагдсан; advanced roadmap тусдаа.

**Хаахдаа:** тохирох тест, requirement evidence, migration/content ledger, commit, verified push/PR, downloadable ZIP/checksum, NEXT-STEPS; дараагийн багцыг эхлүүлэхгүй.

### 06. Profile, statistics ба суралцах нэмэлт хэрэгслүүд

**Хийх ажил:** Own/public profile, heatmap/streaks, rating/tag charts, weekly phases, active/saved tasks, shared progress. Optional learning path/prereq graph/review queue/private journal/feedback-ийн өгөөжийг үнэлж шийдэх.

**Checklist IDs:** S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, O01, O02, O03, O04, O05.

**Дууссан гэж үзэх нөхцөл:** Synthetic known histories/timezone/missing timestamps/ratings/multi-tag/weekly counts зөв; ownership/privacy PASS. Optional бүр implemented эсвэл documented OPTIONAL_DEFERRED; үндсэн дутуу requirement-г optional болгохгүй.

**Хаахдаа:** тохирох тест, requirement evidence, migration/content ledger, commit, verified push/PR, downloadable ZIP/checksum, NEXT-STEPS; дараагийн багцыг эхлүүлэхгүй.

### 07. Blog цэс, хэрэглэгчийн blog/comment rich editor, санал

**Хийх ажил:** Any signed-in user authoring; public list/detail/private draft; shared tutorial-like block editor ба uploads; upvote/downvote; rich comments; ownership/moderation/security.

**Checklist IDs:** H01, H02, H03, H04, H05, H06, H07, H08, H09, H10, H11, H12.

**Дууссан гэж үзэх нөхцөл:** UserA author / userB vote-comment / admin moderation flow; one-vote/change/undo/concurrency; private drafts, XSS/role/upload tests; desktop/mobile/light/dark. Tutorial admin эрх, progress хэвээр.

**Хаахдаа:** тохирох тест, requirement evidence, migration/content ledger, commit, verified push/PR, downloadable ZIP/checksum, NEXT-STEPS; дараагийн багцыг эхлүүлэхгүй.

### 08. Нийт UI/theme, хуучин функцуудын regression, release/deploy

**Хийх ажил:** White-neutral light/approved dark, Home/navigation/login/signup/CMS; account/friends/follow/groups/reports/teacher notes/Excel/A4 PDF; final cross-page security/performance/regression; GitHub/deploy/archive/handoff.

**Checklist IDs:** G01, G02, G03, G04, G05, G06, G07, G08, G09, G10, G11, G12, R01, R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, R12, F10, F11, F12, F13, F14.

**Дууссан гэж үзэх нөхцөл:** Source-wide evidence consolidation; clean checkout, auth/export/mobile tests; verified remote SHA/PR/ZIP, actual deploy/cache/live checks тусдаа. Blocked/live-unverified-г ил тод; бүх зүйл дууссан гэж нотолгоогүй хэлэхгүй.

**Хаахдаа:** тохирох тест, requirement evidence, migration/content ledger, commit, verified push/PR, downloadable ZIP/checksum, NEXT-STEPS; дараагийн багцыг эхлүүлэхгүй.

## Хамаарал ба ажиллах дүрэм

**1 →4 →2 →3 →5 →6 →7 →8.** Багцын ID-г өөрчлөхгүй; багц4 нь багц2/3-ын өмнө хийгдэнэ. Гэхдээ schema/security/revision хамгаалалт болон тест/commit/ZIP нь зөвхөн1/8-д биш **багц бүрд** үйлчилнэ.2/3 дахь хичээлд practice task үнэхээр дутагдвал баталгаажуулж импортлох нь тухайн багцын dependency; нэмэлт quota-г4-д нэгтгэж тоолно.

Шинэ blog/comment feature нь tutorial shared editor-г reuse хийх боловч admin-only tutorial grants-ийг бүх хэрэглэгчид өгөхгүй. Blog comment/vote-ийг энэ төлөвлөгөөнд оруулсан; хэрэгжсэн гэж тэмдэглээгүй. Reply threading/comment voting заавал биш.

Optional O01–05 нь үнэлэх хүрээ; үндсэн шаардлагыг орлохгүй, documented deferral боломжтой.

Энэ checkpoint зөвхөн төлөвлөгөө шинэчилсэн. Дараагийн implementation багц **04**; хэрэглэгч эхлүүлэхийг заасны дараа хэрэгжүүлнэ. Багц2/3 эхлээгүй. Өмнөх completion evidence-г хадгална.
