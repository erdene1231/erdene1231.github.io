> Дэлгэрэнгүй үндсэн checklist: [MASTER-WORK-CHECKLIST.md](MASTER-WORK-CHECKLIST.md). Доорх P0–P8 нь хуучин ерөнхий ангилал; шинэ баримтын concrete tasks/acceptance/dependencies-ийг дагана. Эх мөрийн хүснэгт traceability зориулалтаар хэвээр.

# Бүх эх шаардлагын хэрэгжилтийн төлөвлөгөө

1467 эх мөр, 319 topic traceability мөрийг хадгалсан. Жишээ/тайлбар нь тусдаа feature quota биш. Шинэ хэрэглэгчийн шийдвэр хуучин зөрчилтэй шаардлагыг орлоно.

Мөр бүрийн дэлгэрэнгүй ажил/баримт/одоогийн төлөв: DELIVERY-PLAN.json. Local тест нь live/deploy баталгаа биш.

## P0 — Баталгаажуулалт ба хадгалалт

Editor workflow, exact footer states, blank lessons, optional metadata, saved drafts, Reset, tags. Merge/deploy then authenticated smoke; no real deletion as smoke.

Шалгалт: Node + Chromium + SQL CAS/RLS tests; remote SHA, archive manifest.

Төлөв: Local workflow verified; live deployment unverified

## P1 — Өгөгдлийн холбоос ба импорт

Re-audit031; adapt pending026 to numeric/legacy keys and empty lessons, preserve reset/delete/media guards. Audit broken references before preparing a new migration. Then review027 batch draft import with atomic backup/rollback and actor checks.

Шалгалт: PGlite invalid/missing references; snapshot/fingerprint equality; dry-run batches.

Төлөв: Audit first; no blind replay of026/027

## P2 — Одоогийн tutorial-уудын чанар

Review each current lesson by original source criteria: motivating problem, naive approach, observation, proof, complexity, annotated C++17, edge cases, pitfalls, variants, worked example and checklist. Start Binary Search/Greedy. Compare live body hashes; never replace admin edits wholesale.

Шалгалт: Per-lesson semantic review, C++ execution with brute-force/random edge tests and bilingual browser review.

Төлөв: Per-lesson review backlog; row counts are not quality proof

## P3 — Дутуу сэдвүүд

Map every source topic to canonical lessons by meaning; validate aliases, prerequisites and coverage. Add missing topics in dependency order: foundations, techniques/greedy, structures, graphs/trees, DP, strings, math, geometry, olympiad skills.

Шалгалт: Topic-to-lesson evidence matrix; proofs/examples/C++ tests per topic; no invented quota.

Төлөв: 319 topic traceability rows retained, not319 new tutorials

## P4 — Бодлогын сан ба practice

Verify CSES/olympiad sources, deduplicate stable IDs/URLs, recover BOI17 Toll mapping before import. Curate difficulty progression and genuine priority rationale for each tutorial; check links, hints and variants.

Шалгалт: Source verification, dry-run import, duplicate/ref integrity and progress preservation tests.

Төлөв: No seed replay; imports only verified missing rows

## P5 — 100 хоногийн төлөвлөгөө

Audit all100 days against published tutorial/practice prerequisites and realistic workload. Reconcile reading, solving and self-check rules; maintain old progress IDs/dates.

Шалгалт: Day-by-day dependency coverage plus completion/statistics/date boundary tests.

Төлөв: Current plan exists; full pedagogical review pending

## P6 — Profile ба statistics

Review profile, activity heatmap, rating/tag distribution, weekly phases, active tasks, review queue/journal/feedback and dashboard source requirements. Implement only missing behavior after auditing current data contracts.

Шалгалт: Known synthetic histories, timezone/weekly boundaries, missing/unrated/archived task tests; no user PII export.

Төлөв: Audit pending; local UI existence is not full completion

## P7 — UI/UX ба accessibility

Audit Problems/library/detail, light/dark, responsive tables/filters, numeric IDs, priority/importance palette, rating colors, mathematical rendering, navigation and loading/error states. Preserve approved current layout decisions.

Шалгалт: Desktop/mobile light/dark screenshots, keyboard/focus/overflow, large catalog performance.

Төлөв: Current catalog fixes local verified; source-wide audit pending

## P8 — Release ба үйл ажиллагаа

Consolidate requirement evidence, docs, migration map and handoff. Verify GitHub head, PR checks, merge/deploy as authorized, then real authenticated read/upload/save smoke on approved nonproduction fixtures.

Шалгалт: Clean checkout build/tests, secret scan, remote SHA, ZIP CRC/hash/bundle, deployed version/cache verification.

Төлөв: Merge/deploy/live checks remain separate from local tests

## Гүйцэтгэлийн дүрэм

Нэг жижиг өөрчлөлт → тохирох тест → source мөрийн evidence шинэчлэх → secret scan → commit → verified remote push + PR → ZIP/manifest/handoff. Production өөрчлөлтийн өмнө бодит schema/content hashes audit; шинэ дугаар, зөвхөн дутуу migration. Сургалтын агуулгыг live admin хувилбартай diff хийж нэгтгэнэ. Бөглөсөн мөрийг дахин ажиллуулахгүй.

## Бүх эх мөрийн жагсаалт

| ID | Үе | Одоогийн төлөв | Шаардлага |
|---|---|---|---|
| R1-L0005 | P8 | PARTIAL | Чи бол **Erdene Club сайтыг өмнө нь хөгжүүлж, кодын бүтэц, GitHub repository, Supabase database, authentication, admin system, UI/UX, tutorials болон problems системийг аль хэдийн сайн мэддэг ChatGPT Work mode дахь миний хөгжүүлэлтийн туслах** юм. |
| R1-L0007 | P8 | PARTIAL | Өмнөх ажлын контекст, хэрэгжүүлсэн функцууд, өгөгдлийн бүтэц, хийсэн шийдвэрүүдээ ашигла. Төслийг шинээр эхлүүлж байгаа мэт хандах хэрэггүй. |
| R1-L0009 | P8 | PARTIAL | Вэбсайт: https://erdeneclub.com/ |
| R1-L0011 | P8 | PARTIAL | CMS judge: https://judge.erdeneclub.com/ |
| R1-L0013 | P8 | PARTIAL | Энэ төслийн зорилго бол Erdene Club-ийг **Монголын мэдээлэлзүйн олимпиадад бэлдэж буй сурагчдад зориулсан USACO Guide-тэй харьцуулахуйц, чанартай сургалтын платформ** болгох. |
| R1-L0015 | P8 | PARTIAL | Платформ дараах чадваруудыг онцгой хөгжүүлэх ёстой: |
| R1-L0017 | P8 | PARTIAL | - Алгоритмын үндсэн ойлголт |
| R1-L0018 | P8 | PARTIAL | - Ажиглалт хийх чадвар |
| R1-L0019 | P8 | PARTIAL | - Бие даан бодлого бодох |
| R1-L0020 | P8 | PARTIAL | - Creative problem solving |
| R1-L0021 | P8 | PARTIAL | - Математик сэтгэлгээ |
| R1-L0022 | P8 | PARTIAL | - Алгоритмын зөв байдлыг батлах |
| R1-L0023 | P8 | PARTIAL | - Хугацааны болон санах ойн нийлмэл байдлыг шинжлэх |
| R1-L0024 | P8 | PARTIAL | - Алгоритмыг бие даан хэрэгжүүлэх |
| R1-L0025 | P8 | PARTIAL | - IOI-style subtasks болон partial scoring |
| R1-L0026 | P8 | PARTIAL | - Шинэ, урьд өмнө хараагүй бодлогын шийдлийг нээх |
| R1-L0028 | P8 | PARTIAL | **Үндсэн зорилтот сурагчид:** Codeforces 1300–1400 түвшний сурагчид. |
| R1-L0030 | P8 | PARTIAL | Гэхдээ анхан шатнаас IOI/EGOI/JOI/APIO түвшин хүртэл ахих боломжтой сургалтын систем бий болго. |
| R1-L0032 | P8 | PARTIAL | Энэхүү ажил нь зөвхөн дизайны шинэчлэл биш. Сургалтын агуулга, бодлогын сан, сургалтын дараалал, хэрэглэгчийн ахиц, статистик, өгөгдлийн архитектурыг бүхэлд нь сайжруулах ажил юм. |
| R1-L0038 | P8 | PARTIAL | 1. Одоо ажиллаж байгаа сайтыг эхнээс нь дахин бүтээхгүй. |
| R1-L0039 | P8 | PARTIAL | 2. Өмнө нь хийсэн ажлаа болон төслийн архитектурыг ашигла. |
| R1-L0040 | P8 | PARTIAL | 3. Байгаа account, profiles, progress, problems, tutorials, hints, collections, admin features болон CMS navigation-ийг хадгал. |
| R1-L0041 | P8 | PARTIAL | 4. Өмнө нь бодсон бодлогуудын solved status алдагдаж болохгүй. |
| R1-L0042 | P8 | PARTIAL | 5. Database дээр destructive migration хийхгүй. |
| R1-L0043 | P8 | PARTIAL | 6. Одоо байгаа problem ID болон tutorial ID-г боломжтой бол өөрчлөхгүй. |
| R1-L0044 | P8 | PARTIAL | 7. Бүх өөрчлөлт GitHub Pages болон Supabase архитектуртай нийцсэн байна. |
| R1-L0045 | P8 | PARTIAL | 8. Dark theme-ийн одоогийн дизайн маш сайн байгаа. Үндсэн төрхийг нь хадгал. |
| R1-L0046 | P8 | PARTIAL | 9. UI-г desktop болон mobile дээр зөв ажиллуул. |
| R1-L0047 | P8 | PARTIAL | 10. Агуулгын тоог нэмэхийн тулд чанаргүй, давхардсан, хоосон мэдээлэл үүсгэхгүй. |
| R1-L0048 | P8 | PARTIAL | 11. Бодлого, rating, source URL, олимпиадын нэр, он, tutorial association зэрэг мэдээллийг зохиож болохгүй. |
| R1-L0049 | P8 | PARTIAL | 12. Хийгдсэн ажил болон зөвхөн төлөвлөсөн ажлыг тодорхой ялгаж тайлагна. |
| R1-L0050 | P8 | PARTIAL | 13. Надаас хэрэггүй баталгаажуулалт давтан асуулгүй, өмнөх контекст болон repository-д тулгуурлан ажлаа үргэлжлүүл. |
| R1-L0051 | P8 | PARTIAL | 14. Бүх тайлбар, ажлын тайланг монголоор бич. |
| R1-L0053 | P8 | PARTIAL | Эхлээд одоогийн repository болон database-ийн холбогдох хэсгүүдийг шалга. Өмнө нь мэдэж байсан архитектураа дахин ашиглаж, зөвхөн шаардлагатай өөрчлөлтийг хий. |
| R1-L0059 | P2 | PARTIAL | Энэ бол төслийн **хамгийн өндөр ач холбогдолтой** хэсэг. |
| R1-L0061 | P2 | PARTIAL | Одоогийн DSA tutorial-уудын тайлбар хангалттай гүн биш байна. Тэдгээрийг USACO Guide шиг дэлгэрэнгүй, ойлгомжтой, логик дараалалтай, жинхэнэ сурах бичгийн чанартай болго. |
| R1-L0063 | P2 | PARTIAL | Tutorial бүр дараах бүтцийг баримтална. |
| R1-L0067 | P2 | PARTIAL | Tutorial-ийн эхэнд шууд алгоритмын тодорхойлолт бичиж болохгүй. |
| R1-L0069 | P2 | PARTIAL | Эхлээд сурагчид тулгарч болох асуудлыг тайлбарла. |
| R1-L0071 | P2 | PARTIAL | Жишээлбэл, Binary Search tutorial: |
| R1-L0073 | P2 | PARTIAL | - Бидэнд эрэмбэлэгдсэн 1,000,000 элементтэй массив байна. |
| R1-L0074 | P2 | PARTIAL | - Нэг элементийг олохын тулд бүгдийг нь шалгавал юу болох вэ? |
| R1-L0075 | P2 | PARTIAL | - Яагаад энэ арга үр ашиг муутай вэ? |
| R1-L0076 | P2 | PARTIAL | - Массив эрэмбэлэгдсэн гэдэг мэдээллийг хэрхэн ашиглаж болох вэ? |
| R1-L0077 | P2 | PARTIAL | - Яаж хайлтын талбайг багасгах вэ? |
| R1-L0079 | P2 | PARTIAL | Энэ мэтчилэн сурагч алгоритм сурахаасаа өмнө **тухайн алгоритмыг хэрэглэх шаардлагыг ойлгох** ёстой. |
| R1-L0081 | P2 | PARTIAL | Алгоритмыг ямар бодлогод, ямар нөхцөлд хэрэглэх нь тохиромжтойг тайлбарла. |
| R1-L0085 | P2 | PARTIAL | Алгоритмын эцсийн хувилбарыг шууд өгч болохгүй. |
| R1-L0087 | P2 | PARTIAL | Дараах дарааллаар ойлгуул: |
| R1-L0089 | P2 | PARTIAL | 1. Энгийн, шууд шийдэл. |
| R1-L0090 | P2 | PARTIAL | 2. Шууд шийдлийн сул тал. |
| R1-L0091 | P2 | PARTIAL | 3. Асуудлыг хялбарчлах ажиглалт. |
| R1-L0092 | P2 | PARTIAL | 4. Илүү үр ашигтай шийдэлд хүрэх үндсэн санаа. |
| R1-L0093 | P2 | PARTIAL | 5. Алгоритмыг бүрэн гарган авах. |
| R1-L0095 | P2 | PARTIAL | Ингэснээр сурагч зөвхөн алгоритмыг цээжлэх биш, **ижил төстэй шинэ алгоритмыг өөрөө нээж сурах** ёстой. |
| R1-L0099 | P2 | PARTIAL | Алгоритмыг жижиг жишээгээр тайлбарла. |
| R1-L0101 | P2 | PARTIAL | Шаардлагатай үед: |
| R1-L0103 | P2 | PARTIAL | - Массивын төлөв |
| R1-L0104 | P2 | PARTIAL | - Заагчдын байрлал |
| R1-L0105 | P2 | PARTIAL | - Графын traversal |
| R1-L0106 | P2 | PARTIAL | - Модны өөрчлөлт |
| R1-L0107 | P2 | PARTIAL | - DP хүснэгт |
| R1-L0108 | P2 | PARTIAL | - Segment tree-ийн бүтэц |
| R1-L0109 | P2 | PARTIAL | - Алгоритмын алхам бүрийн төлөв |
| R1-L0111 | P2 | PARTIAL | зэргийг дүрслэн үзүүл. |
| R1-L0113 | P2 | PARTIAL | Боломжтой үед интерактив visualization нэм. |
| R1-L0115 | P2 | PARTIAL | Гэхдээ интерактив дүрслэл нэмэхийн тулд хуудасны performance-ийг муутгаж болохгүй. |
| R1-L0119 | P2 | PARTIAL | Алгоритмын зөв байдлыг тайлбарла. |
| R1-L0121 | P2 | PARTIAL | Шаардлагатай үед: |
| R1-L0123 | P2 | PARTIAL | - Loop invariant |
| R1-L0124 | P2 | PARTIAL | - Induction |
| R1-L0125 | P2 | PARTIAL | - Exchange argument |
| R1-L0126 | P2 | PARTIAL | - Contradiction |
| R1-L0127 | P2 | PARTIAL | - Greedy stays ahead |
| R1-L0128 | P2 | PARTIAL | - DP state болон transition-ийн зөв байдал |
| R1-L0129 | P2 | PARTIAL | - Graph algorithm correctness |
| R1-L0131 | P2 | PARTIAL | зэргийг ашигла. |
| R1-L0133 | P2 | PARTIAL | 1300–1400 түвшний сурагч ойлгохуйц энгийн тайлбараас эхэлж, дараа нь албан ёсны баталгааг гарга. |
| R1-L0135 | P2 | PARTIAL | Зөв байдлын баталгааг алгасаж, зөвхөн код үзүүлдэг tutorial битгий хий. |
| R1-L0139 | P2 | PARTIAL | Алгоритмын хугацааны нийлмэл байдлыг зөвхөн томьёогоор хэлээд орхиж болохгүй. |
| R1-L0141 | P2 | PARTIAL | Жишээлбэл: |
| R1-L0143 | P2 | PARTIAL | **Binary Search: O(log n)** |
| R1-L0145 | P2 | PARTIAL | Яагаад? |
| R1-L0147 | P2 | PARTIAL | - Нэг алхамд боломжит хариултын муж ойролцоогоор хоёр дахин багасдаг. |
| R1-L0148 | P2 | PARTIAL | - n элементээс n/2, n/4, n/8 ... болж багасна. |
| R1-L0149 | P2 | PARTIAL | - Ойролцоогоор log₂(n) алхмын дараа ганц боломж үлдэнэ. |
| R1-L0151 | P2 | PARTIAL | Ингэж ойлгуул. |
| R1-L0153 | P2 | PARTIAL | Tutorial бүрд: |
| R1-L0155 | P2 | PARTIAL | - Time complexity |
| R1-L0156 | P2 | PARTIAL | - Space complexity |
| R1-L0157 | P2 | PARTIAL | - Хамгийн муу тохиолдол |
| R1-L0158 | P2 | PARTIAL | - Шаардлагатай үед amortized complexity |
| R1-L0159 | P2 | PARTIAL | - Хязгаарлалтаас боломжит алгоритм сонгох логик |
| R1-L0161 | P2 | PARTIAL | зэргийг тайлбарла. |
| R1-L0163 | P2 | PARTIAL | Мөн ямар нөхцөлд тухайн алгоритм хангалтгүй болохыг дурд. |
| R1-L0167 | P2 | PARTIAL | Бүх implementation үндсэндээ C++17 байна. |
| R1-L0169 | P2 | PARTIAL | Зөвхөн бүтэн код өгөөд өнгөрч болохгүй. |
| R1-L0171 | P2 | PARTIAL | Дараах байдлаар тайлбарла: |
| R1-L0173 | P2 | PARTIAL | **1-р хэсэг — Өгөгдлийн бүтэц болон хувьсагчид** |
| R1-L0175 | P2 | PARTIAL | Ямар хувьсагч юуг илэрхийлж байгаа, яагаад хэрэгтэйг тайлбарла. |
| R1-L0177 | P2 | PARTIAL | **2-р хэсэг — Initialization** |
| R1-L0179 | P2 | PARTIAL | Анхны төлөвийг яагаад ингэж сонгосныг тайлбарла. |
| R1-L0181 | P2 | PARTIAL | **3-р хэсэг — Гол алгоритм** |
| R1-L0183 | P2 | PARTIAL | Loop, condition, transition, update бүрийн логикийг тайлбарла. |
| R1-L0185 | P2 | PARTIAL | **4-р хэсэг — Зөв хариу гаргах** |
| R1-L0187 | P2 | PARTIAL | Алгоритм дуусахад ямар invariant биелж байгааг тайлбарла. |
| R1-L0189 | P2 | PARTIAL | **5-р хэсэг — Бүтэн implementation** |
| R1-L0191 | P2 | PARTIAL | Дээрх хэсгүүдийг нэгтгэсэн цэвэр, ойлгомжтой C++17 код харуул. |
| R1-L0193 | P2 | PARTIAL | Implementation хэсэг бүрийг expand/collapse хийх боломжтой байж болно. |
| R1-L0195 | P2 | PARTIAL | Кодын шаардлага: |
| R1-L0197 | P2 | PARTIAL | - Syntax highlighting |
| R1-L0198 | P2 | PARTIAL | - Copy button |
| R1-L0199 | P2 | PARTIAL | - Зөв indentation |
| R1-L0200 | P2 | PARTIAL | - Ойлгомжтой variable naming |
| R1-L0201 | P2 | PARTIAL | - Шаардлагатай comments |
| R1-L0202 | P2 | PARTIAL | - Boundary cases |
| R1-L0203 | P2 | PARTIAL | - Overflow, indexing зэрэг анхаарах зүйлс |
| R1-L0207 | P8 | PARTIAL | Алгоритм бүрд Common Mistakes хэсэг нэм. |
| R1-L0209 | P8 | PARTIAL | Тухайн алгоритмд тохирох алдаануудыг тайлбарла. |
| R1-L0211 | P8 | PARTIAL | Жишээ нь Binary Search: |
| R1-L0213 | P8 | PARTIAL | - Infinite loop |
| R1-L0214 | P8 | PARTIAL | - Off-by-one error |
| R1-L0215 | P8 | PARTIAL | - `mid` буруу тооцох |
| R1-L0216 | P8 | PARTIAL | - Monotonic condition буруу тодорхойлох |
| R1-L0217 | P8 | PARTIAL | - `lower_bound` болон `upper_bound`-ийг андуурах |
| R1-L0219 | P8 | PARTIAL | Алдаа бүрд боломжтой бол жижиг counterexample өг. |
| R1-L0223 | P2 | PARTIAL | Энэ хэсгийг заавал хэрэгжүүл. |
| R1-L0225 | P2 | PARTIAL | Алгоритм бүрийн холбогдох хувилбарууд болон өргөтгөлүүдийг харуул. |
| R1-L0227 | P2 | PARTIAL | Жишээ нь Binary Search: |
| R1-L0229 | P2 | PARTIAL | - Standard binary search |
| R1-L0230 | P2 | PARTIAL | - Lower bound |
| R1-L0231 | P2 | PARTIAL | - Upper bound |
| R1-L0232 | P2 | PARTIAL | - Binary search on answer |
| R1-L0233 | P2 | PARTIAL | - Binary search on real numbers |
| R1-L0234 | P2 | PARTIAL | - Parallel binary search |
| R1-L0236 | P2 | PARTIAL | Эдгээрийн ялгаа, хэрэглээ, шаардлагатай өмнөх мэдлэгийг товч тайлбарла. |
| R1-L0238 | P2 | PARTIAL | **Хувилбар бүрийн нэр дээр дарахад тухайн tutorial руу очдог байх ёстой.** |
| R1-L0240 | P2 | PARTIAL | Мөн: |
| R1-L0242 | P2 | PARTIAL | - Prerequisite tutorials |
| R1-L0243 | P2 | PARTIAL | - Related tutorials |
| R1-L0244 | P2 | PARTIAL | - Advanced extensions |
| R1-L0245 | P2 | PARTIAL | - Next recommended tutorial |
| R1-L0247 | P2 | PARTIAL | гэсэн холбоосуудтай болго. |
| R1-L0249 | P2 | PARTIAL | Холбоосыг текст дотор таамгаар бичих биш, тогтвортой tutorial ID дээр суурилсан relationship ашигла. |
| R1-L0251 | P2 | PARTIAL | Одоогоор тухайн tutorial байхгүй бол холбоос эвдэрсэн байдалтай бүү харуул. Харин backlog-д бүртгэж, шаардлагатай tutorial-ийг бүтээ. |
| R1-L0255 | P2 | PARTIAL | Tutorial бүрд **"Ажиглалт ба бодлого бодох арга"** хэсэг нэм. |
| R1-L0257 | P2 | PARTIAL | Энэ хэсэгт: |
| R1-L0259 | P2 | PARTIAL | - Бодлогын өгүүлбэрээс ямар мэдээлэл чухал вэ? |
| R1-L0260 | P2 | PARTIAL | - Ямар constraint алгоритмыг санал болгож байна вэ? |
| R1-L0261 | P2 | PARTIAL | - Ямар invariant ажиглагдаж байна вэ? |
| R1-L0262 | P2 | PARTIAL | - Шууд шийдлийг хэрхэн сайжруулах вэ? |
| R1-L0263 | P2 | PARTIAL | - Энэ алгоритмыг хэрэглэх эсэхийг хэрхэн таних вэ? |
| R1-L0264 | P2 | PARTIAL | - Ямар үед энэ алгоритм буруу сонголт болох вэ? |
| R1-L0266 | P2 | PARTIAL | гэдгийг бодлогын жишээтэй тайлбарла. |
| R1-L0268 | P2 | PARTIAL | Энэ хэсэг Erdene Club-ийн гол ялгарах онцлог байх ёстой. |
| R1-L0272 | P4 | PARTIAL | Tutorial бүрийн төгсгөлд: |
| R1-L0274 | P4 | PARTIAL | **"Энэ сэдвийг эзэмших бодлогууд"** |
| R1-L0276 | P4 | PARTIAL | гэсэн хэсэг оруул. |
| R1-L0278 | P4 | PARTIAL | Бодлогуудыг дараах шатлалаар ангил: |
| R1-L0280 | P4 | PARTIAL | - Warm-up |
| R1-L0281 | P4 | PARTIAL | - Standard |
| R1-L0282 | P4 | PARTIAL | - Observation |
| R1-L0283 | P4 | PARTIAL | - Application |
| R1-L0284 | P4 | PARTIAL | - Challenge |
| R1-L0285 | P4 | PARTIAL | - Olympiad extension |
| R1-L0287 | P4 | PARTIAL | Тохирох тооны, чанартай бодлого сонго. Ихэнх tutorial-д 5–12 бодлого байж болно, гэхдээ сэдвээс хамааран өөрчил. |
| R1-L0289 | P4 | PARTIAL | **Priority бодлогуудыг ⭐ тэмдэглэгээтэй, бусдаас тодорхой ялгаруулж харуул.** |
| R1-L0291 | P4 | PARTIAL | Priority гэдэг нь зүгээр хамгийн хүнд бодлого гэсэн үг биш. |
| R1-L0293 | P4 | PARTIAL | Тухайн сэдвийг эзэмшихэд хамгийн өндөр өгөөжтэй бодлого байх ёстой. |
| R1-L0295 | P4 | PARTIAL | Priority сонгох шалгуур: |
| R1-L0297 | P4 | PARTIAL | - Гол алгоритмыг оновчтой ашиглуулдаг |
| R1-L0298 | P4 | PARTIAL | - Чухал ажиглалт шаарддаг |
| R1-L0299 | P4 | PARTIAL | - Түгээмэл алдааг ойлгуулдаг |
| R1-L0300 | P4 | PARTIAL | - Шинэ төрлийн хэрэглээг үзүүлдэг |
| R1-L0301 | P4 | PARTIAL | - Дараагийн түвшинд суурь болдог |
| R1-L0302 | P4 | PARTIAL | - Сурагчийн бодох чадварыг хөгжүүлдэг |
| R1-L0304 | P4 | PARTIAL | Priority бодлого бүрийн хувьд редакторт харагдах богино үндэслэл хадгал. |
| R1-L0306 | P4 | PARTIAL | Сурагчид бодлогын шийдлийг spoiler болгож харуулахгүй. |
| R1-L0308 | P4 | PARTIAL | Бодлогын жагсаалтад: |
| R1-L0310 | P4 | PARTIAL | - Нэр |
| R1-L0311 | P4 | PARTIAL | - Source |
| R1-L0312 | P4 | PARTIAL | - Rating эсвэл estimated difficulty |
| R1-L0313 | P4 | PARTIAL | - Difficulty category |
| R1-L0314 | P4 | PARTIAL | - Priority |
| R1-L0315 | P4 | PARTIAL | - Solved/attempted/unsolved |
| R1-L0316 | P4 | PARTIAL | - Холбогдох tutorial |
| R1-L0317 | P4 | PARTIAL | - Хэрэв байгаа бол 100-day plan-ийн өдөр |
| R1-L0318 | P4 | PARTIAL | - Бодлого руу орох линк |
| R1-L0320 | P4 | PARTIAL | харагдана. |
| R1-L0324 | P8 | PARTIAL | Байгаа 3-level hint системийг хадгал. |
| R1-L0326 | P8 | PARTIAL | Шаардлагатай бол сайжруул. |
| R1-L0328 | P8 | PARTIAL | - Hint 1: Гол ажиглалтад чиглүүлнэ. |
| R1-L0329 | P8 | PARTIAL | - Hint 2: Алгоритмын санаанд ойртуулна. |
| R1-L0330 | P8 | PARTIAL | - Hint 3: Шийдлийг хэрэгжүүлэх чухал алхмыг ойлгуулна. |
| R1-L0332 | P8 | PARTIAL | Hint нээхээс өмнө сурагчид өөрөө бодох боломж үлдээ. |
| R1-L0334 | P8 | PARTIAL | Бүтэн шийдэл болон editorial-ийг hints-тэй андуурч болохгүй. |
| R1-L0338 | P2 | PARTIAL | Tutorial бүрийн эцэст сурагч өөрийгөө шалгах боломжтой болго. |
| R1-L0340 | P2 | PARTIAL | Жишээ нь: |
| R1-L0342 | P2 | PARTIAL | - Энэ алгоритм яагаад хэрэгтэйг тайлбарлаж чадна. |
| R1-L0343 | P2 | PARTIAL | - Time complexity-г өөрөө гаргаж чадна. |
| R1-L0344 | P2 | PARTIAL | - Зөв ажиллах шалтгааныг ойлгосон. |
| R1-L0345 | P2 | PARTIAL | - Implementation-ийг харалгүй бичиж чадна. |
| R1-L0346 | P2 | PARTIAL | - Priority бодлогуудыг бодсон. |
| R1-L0347 | P2 | PARTIAL | - Түгээмэл алдааг таньж чадна. |
| R1-L0349 | P2 | PARTIAL | Эдгээрийг tutorial progress-тэй холбож болно. |
| R1-L0351 | P2 | PARTIAL | **Чухал:** Tutorial уншсан эсэх болон алгоритмыг эзэмшсэн эсэх нь өөр ойлголт. Progress системд энэ ялгааг хадгал. |
| R1-L0357 | P3 | PARTIAL | Одоогийн tutorial санг хадгалж, илүү олон сэдэвтэй болго. |
| R1-L0359 | P3 | PARTIAL | Сэдвүүдийг prerequisite-д суурилсан дарааллаар ангил. |
| R1-L0363 | P3 | PARTIAL | - Complexity analysis |
| R1-L0364 | P3 | PARTIAL | - C++ STL |
| R1-L0365 | P3 | PARTIAL | - Arrays, strings |
| R1-L0366 | P3 | PARTIAL | - Prefix sum, difference array |
| R1-L0367 | P3 | PARTIAL | - Sorting |
| R1-L0368 | P3 | PARTIAL | - Binary search |
| R1-L0369 | P3 | PARTIAL | - Two pointers |
| R1-L0370 | P3 | PARTIAL | - Sliding window |
| R1-L0371 | P3 | PARTIAL | - Brute force |
| R1-L0372 | P3 | PARTIAL | - Recursion, backtracking |
| R1-L0373 | P3 | PARTIAL | - Basic greedy |
| R1-L0374 | P3 | PARTIAL | - Bit manipulation |
| R1-L0375 | P3 | PARTIAL | - Basic number theory |
| R1-L0376 | P3 | PARTIAL | - Basic combinatorics |
| R1-L0377 | P3 | PARTIAL | - Basic constructive algorithms |
| R1-L0381 | P3 | PARTIAL | - Coordinate compression |
| R1-L0382 | P3 | PARTIAL | - Sweep line |
| R1-L0383 | P3 | PARTIAL | - Monotonic stack/queue |
| R1-L0384 | P3 | PARTIAL | - DSU |
| R1-L0385 | P3 | PARTIAL | - BFS, DFS |
| R1-L0386 | P3 | PARTIAL | - Graph representations |
| R1-L0387 | P3 | PARTIAL | - Connected components |
| R1-L0388 | P3 | PARTIAL | - Bipartite graphs |
| R1-L0389 | P3 | PARTIAL | - Topological sorting |
| R1-L0390 | P3 | PARTIAL | - Shortest paths |
| R1-L0391 | P3 | PARTIAL | - Dijkstra |
| R1-L0392 | P3 | PARTIAL | - Bellman-Ford |
| R1-L0393 | P3 | PARTIAL | - MST |
| R1-L0394 | P3 | PARTIAL | - Tree traversal |
| R1-L0395 | P3 | PARTIAL | - LCA |
| R1-L0396 | P3 | PARTIAL | - Binary lifting |
| R1-L0397 | P3 | PARTIAL | - Introductory DP |
| R1-L0398 | P3 | PARTIAL | - Knapsack DP |
| R1-L0399 | P3 | PARTIAL | - Grid DP |
| R1-L0400 | P3 | PARTIAL | - Interval DP |
| R1-L0401 | P3 | PARTIAL | - Bitmask DP |
| R1-L0402 | P3 | PARTIAL | - Fenwick tree |
| R1-L0403 | P3 | PARTIAL | - Segment tree |
| R1-L0404 | P3 | PARTIAL | - Sparse table |
| R1-L0408 | P3 | PARTIAL | - Tree DP |
| R1-L0409 | P3 | PARTIAL | - Rerooting DP |
| R1-L0410 | P3 | PARTIAL | - Digit DP |
| R1-L0411 | P3 | PARTIAL | - Profile DP |
| R1-L0412 | P3 | PARTIAL | - SOS DP |
| R1-L0413 | P3 | PARTIAL | - Divide and conquer DP optimization |
| R1-L0414 | P3 | PARTIAL | - Knuth optimization |
| R1-L0415 | P3 | PARTIAL | - Convex Hull Trick |
| R1-L0416 | P3 | PARTIAL | - Li Chao tree |
| R1-L0417 | P3 | PARTIAL | - Lazy propagation |
| R1-L0418 | P3 | PARTIAL | - Persistent segment tree |
| R1-L0419 | P3 | PARTIAL | - Heavy-light decomposition |
| R1-L0420 | P3 | PARTIAL | - Centroid decomposition |
| R1-L0421 | P3 | PARTIAL | - Small-to-large |
| R1-L0422 | P3 | PARTIAL | - Mo's algorithm |
| R1-L0423 | P3 | PARTIAL | - Offline queries |
| R1-L0424 | P3 | PARTIAL | - Parallel binary search |
| R1-L0425 | P3 | PARTIAL | - SCC |
| R1-L0426 | P3 | PARTIAL | - Bridges/articulation points |
| R1-L0427 | P3 | PARTIAL | - Network flow |
| R1-L0428 | P3 | PARTIAL | - Bipartite matching |
| R1-L0429 | P3 | PARTIAL | - String hashing |
| R1-L0430 | P3 | PARTIAL | - KMP, Z-function |
| R1-L0431 | P3 | PARTIAL | - Trie, Aho-Corasick |
| R1-L0432 | P3 | PARTIAL | - Suffix array, suffix automaton |
| R1-L0433 | P3 | PARTIAL | - Modular arithmetic |
| R1-L0434 | P3 | PARTIAL | - Matrix exponentiation |
| R1-L0435 | P3 | PARTIAL | - Computational geometry |
| R1-L0436 | P3 | PARTIAL | - Advanced graph and tree techniques |
| R1-L0440 | P3 | PARTIAL | Эдгээрийг алгоритмтай адил чухалд тооц. |
| R1-L0442 | P3 | PARTIAL | - Ажиглалт хийх арга |
| R1-L0443 | P3 | PARTIAL | - Constraint-аас алгоритм сонгох |
| R1-L0444 | P3 | PARTIAL | - Greedy шийдлийг нээх |
| R1-L0445 | P3 | PARTIAL | - Greedy proof |
| R1-L0446 | P3 | PARTIAL | - Invariant |
| R1-L0447 | P3 | PARTIAL | - Exchange argument |
| R1-L0448 | P3 | PARTIAL | - Working backwards |
| R1-L0449 | P3 | PARTIAL | - Constructive reasoning |
| R1-L0450 | P3 | PARTIAL | - State design in DP |
| R1-L0451 | P3 | PARTIAL | - Brute force optimization |
| R1-L0452 | P3 | PARTIAL | - Subtask-oriented thinking |
| R1-L0453 | P3 | PARTIAL | - Partial scoring strategy |
| R1-L0454 | P3 | PARTIAL | - Debugging |
| R1-L0455 | P3 | PARTIAL | - Counterexample construction |
| R1-L0456 | P3 | PARTIAL | - Stress testing |
| R1-L0457 | P3 | PARTIAL | - Proof-based problem solving |
| R1-L0459 | P3 | PARTIAL | **Шаардлага:** Сэдвийн тоог хиймлээр нэмэхгүй. Бүх tutorial бодит сургалтын агуулгатай байна. |
| R1-L0465 | P4 | PARTIAL | Одоо байгаа бодлогын санг эхлээд ашигла. |
| R1-L0467 | P4 | PARTIAL | Шинээр бодлого нэмэхээс өмнө: |
| R1-L0469 | P4 | PARTIAL | 1. Одоо байгаа бодлогуудыг судал. |
| R1-L0470 | P4 | PARTIAL | 2. Сэдэв болон хүндрэлийг ангил. |
| R1-L0471 | P4 | PARTIAL | 3. Давхардлыг илрүүл. |
| R1-L0472 | P4 | PARTIAL | 4. Tutorial-тай холбогдоогүй бодлогуудыг тодорхойл. |
| R1-L0473 | P4 | PARTIAL | 5. Ямар сэдэвт сайн бодлого дутагдаж байгааг гарга. |
| R1-L0477 | P4 | PARTIAL | https://cses.fi/problemset/ |
| R1-L0479 | P4 | PARTIAL | CSES-ийн IOI болон ахлах сургуулийн мэдээлэлзүйн олимпиадад хэрэгтэй бодлогуудыг өргөн хүрээнд нэм. |
| R1-L0481 | P4 | PARTIAL | Боломжтой бол бараг бүх CSES Problem Set-ийг хамруул. |
| R1-L0483 | P4 | PARTIAL | Ялангуяа: |
| R1-L0485 | P4 | PARTIAL | - Introductory Problems |
| R1-L0486 | P4 | PARTIAL | - Sorting and Searching |
| R1-L0487 | P4 | PARTIAL | - Dynamic Programming |
| R1-L0488 | P4 | PARTIAL | - Graph Algorithms |
| R1-L0489 | P4 | PARTIAL | - Range Queries |
| R1-L0490 | P4 | PARTIAL | - Tree Algorithms |
| R1-L0491 | P4 | PARTIAL | - Mathematics |
| R1-L0492 | P4 | PARTIAL | - String Algorithms |
| R1-L0493 | P4 | PARTIAL | - Geometry |
| R1-L0494 | P4 | PARTIAL | - Advanced Techniques |
| R1-L0495 | P4 | PARTIAL | - Additional Problems |
| R1-L0497 | P4 | PARTIAL | Бодлого бүрд official URL, source ID, нэр, tag, difficulty, priority, tutorial relationship хадгал. |
| R1-L0499 | P4 | PARTIAL | CSES бодлогод Codeforces-ийн албан ёсны rating байхгүйг анхаар. |
| R1-L0501 | P4 | PARTIAL | Difficulty estimate хийж болно, гэхдээ estimate гэдгийг ялгаж харуул. |
| R1-L0505 | P4 | PARTIAL | Дараах эх сурвалжуудаас чанартай бодлого сонго: |
| R1-L0507 | P4 | PARTIAL | - IOI |
| R1-L0508 | P4 | PARTIAL | - EGOI |
| R1-L0509 | P4 | PARTIAL | - JOI |
| R1-L0510 | P4 | PARTIAL | - APIO |
| R1-L0511 | P4 | PARTIAL | - CEOI |
| R1-L0512 | P4 | PARTIAL | - COCI |
| R1-L0513 | P4 | PARTIAL | - BOI |
| R1-L0514 | P4 | PARTIAL | - Balkan OI |
| R1-L0515 | P4 | PARTIAL | - USACO |
| R1-L0516 | P4 | PARTIAL | - OJ.uz |
| R1-L0517 | P4 | PARTIAL | - AtCoder |
| R1-L0518 | P4 | PARTIAL | - Codeforces |
| R1-L0520 | P4 | PARTIAL | Ялангуяа creative observation, DP, greedy, graphs, trees, data structures, constructive algorithms болон subtasks шаарддаг бодлогуудыг түлхүү сонго. |
| R1-L0522 | P4 | PARTIAL | Бодлого бүрийн metadata-г шалгаж баталгаажуул. |
| R1-L0524 | P4 | PARTIAL | Дур мэдэн rating зохиохгүй. |
| R1-L0526 | P4 | PARTIAL | Нэг бодлого олон tutorial-д харьяалагдаж болно. |
| R1-L0528 | P4 | PARTIAL | Гэхдээ тухайн бодлогын primary topic болон secondary topics-ийг ялга. |
| R1-L0532 | P4 | PARTIAL | Бодлогыг зөвхөн тагтай нь тааруулж сонгож болохгүй. |
| R1-L0534 | P4 | PARTIAL | Боломжтой бол бодлогын өгүүлбэр, шийдлийн гол санаа, editorial-ийг судал. |
| R1-L0536 | P4 | PARTIAL | Яагаад тухайн tutorial-д тохирохыг тогтоо. |
| R1-L0538 | P4 | PARTIAL | Нэн ялангуяа 1300–1400 түвшний сурагчдад ойлгомжтойгоос хүнд рүү шатлан хөгжих боломжтой бодлогуудыг сонго. |
| R1-L0540 | P4 | PARTIAL | Олимпиадын өндөр түвшний бодлогуудыг тохирох ахисан tutorial болон Challenge хэсэгт байрлуул. |
| R1-L0544 | P1 | PARTIAL | Ижил бодлогыг давхар оруулахгүй. |
| R1-L0546 | P1 | PARTIAL | Source + official problem ID-г ашиглан deduplication хий. |
| R1-L0548 | P1 | PARTIAL | Import script нь: |
| R1-L0550 | P1 | PARTIAL | - Давтан ажиллуулахад аюулгүй |
| R1-L0551 | P1 | PARTIAL | - Existing progress-г устгахгүй |
| R1-L0552 | P1 | PARTIAL | - Metadata-г баталгаажуулдаг |
| R1-L0553 | P1 | PARTIAL | - Dry-run боломжтой |
| R1-L0554 | P1 | PARTIAL | - Алдааг логддог |
| R1-L0556 | P1 | PARTIAL | байх ёстой. |
| R1-L0558 | P1 | PARTIAL | Гадаад эх сурвалжийг шалгах боломжгүй бол худал metadata үүсгэхгүй, pending import list-д үлдээ. |
| R1-L0560 | P1 | PARTIAL | Эх сурвалжийн зохиогчийн эрхийг хүндэтгэж, шаардлагагүйгээр бүтэн бодлогын өгүүлбэр хуулж хадгалахгүй. |
| R1-L0566 | P5 | PARTIAL | Сайтын navigation-д шинэ хэсэг нэм: |
| R1-L0568 | P5 | PARTIAL | **100 хоног** |
| R1-L0570 | P5 | PARTIAL | Мэдээлэлзүйн олимпиадад бэлдэх 100 өдрийн системтэй сургалтын төлөвлөгөө бий болго. |
| R1-L0572 | P5 | PARTIAL | Зорилтот эхлэх түвшин: Codeforces 1300–1400. |
| R1-L0574 | P5 | PARTIAL | Зорилго: Сурагчдыг сууриа бататгахаас эхлээд ахисан түвшний үндэсний олимпиад болон IOI-style бодлогууд дээр бие даан ажиллах чадвартай болгох. |
| R1-L0578 | P8 | PARTIAL | 100 өдрийг 10 шат болгон зохион байгуул. |
| R1-L0580 | P8 | PARTIAL | - 1–10: Foundations, complexity, brute force, observation |
| R1-L0581 | P8 | PARTIAL | - 11–20: Sorting, binary search, two pointers, greedy |
| R1-L0582 | P8 | PARTIAL | - 21–30: Prefix sums, sweep line, stacks, data structures |
| R1-L0583 | P8 | PARTIAL | - 31–40: BFS, DFS, graph algorithms |
| R1-L0584 | P8 | PARTIAL | - 41–50: Dynamic programming |
| R1-L0585 | P8 | PARTIAL | - 51–60: Trees, DSU, LCA, tree DP |
| R1-L0586 | P8 | PARTIAL | - 61–70: Segment tree, Fenwick tree, range queries |
| R1-L0587 | P8 | PARTIAL | - 71–80: Advanced DP, strings, graph algorithms |
| R1-L0588 | P8 | PARTIAL | - 81–90: Advanced olympiad techniques, constructive reasoning |
| R1-L0589 | P8 | PARTIAL | - 91–100: Mixed olympiad practice, virtual contests, review |
| R1-L0591 | P8 | PARTIAL | Энэ бол суурь бүтэц. Сэдвүүдийн prerequisite болон хүндрэлд нийцүүлэн сайжруулж болно. |
| R1-L0595 | P5 | PARTIAL | 100 өдөр бүр бодит агуулгатай байна. |
| R1-L0597 | P5 | PARTIAL | Өдөр бүр: |
| R1-L0599 | P5 | PARTIAL | - Өдрийн сэдэв |
| R1-L0600 | P5 | PARTIAL | - Зорилго |
| R1-L0601 | P5 | PARTIAL | - Үзэх tutorial-ууд |
| R1-L0602 | P5 | PARTIAL | - Суралцах гол ажиглалтууд |
| R1-L0603 | P5 | PARTIAL | - Заавал бодох бодлогууд |
| R1-L0604 | P5 | PARTIAL | - Priority бодлогууд |
| R1-L0605 | P5 | PARTIAL | - Нэмэлт Challenge |
| R1-L0606 | P5 | PARTIAL | - Тооцоолсон хугацаа |
| R1-L0607 | P5 | PARTIAL | - Өдрийн checklist |
| R1-L0608 | P5 | PARTIAL | - Completion status |
| R1-L0610 | P5 | PARTIAL | байх ёстой. |
| R1-L0612 | P5 | PARTIAL | Ихэнх өдөр 3–5 бодлого өгч болно. |
| R1-L0614 | P5 | PARTIAL | Хэт хүнд сэдэв, mock contest болон review day дээр ачааллыг зохистой тохируул. |
| R1-L0616 | P5 | PARTIAL | **100 өдрийн бүх даалгаврыг бодит problem ID болон tutorial ID-тай холбо.** |
| R1-L0618 | P5 | PARTIAL | Эвдэрсэн холбоос, байхгүй бодлого, хоосон өдөр үүсгэхгүй. |
| R1-L0622 | P5 | PARTIAL | Зөвхөн алгоритм үзэх өдрүүд биш: |
| R1-L0624 | P5 | PARTIAL | - Observation day |
| R1-L0625 | P5 | PARTIAL | - Revision day |
| R1-L0626 | P5 | PARTIAL | - Mixed problem day |
| R1-L0627 | P5 | PARTIAL | - Virtual contest day |
| R1-L0628 | P5 | PARTIAL | - Debugging day |
| R1-L0629 | P5 | PARTIAL | - Editorial analysis day |
| R1-L0630 | P5 | PARTIAL | - Subtask practice day |
| R1-L0632 | P5 | PARTIAL | оруул. |
| R1-L0634 | P5 | PARTIAL | Spaced repetition ашиглаж өмнө үзсэн сэдвүүдийг тодорхой хугацааны дараа давт. |
| R1-L0636 | P5 | PARTIAL | Өдөр бүр хэт олон шинэ алгоритм оруулахгүй. |
| R1-L0638 | P5 | PARTIAL | Сурагчид бодлогыг бодох цаг үлдээ. |
| R1-L0642 | P5 | PARTIAL | Хэрэглэгч бүр өөрийн 100-day progress-тэй байна. |
| R1-L0644 | P5 | PARTIAL | - Start plan |
| R1-L0645 | P5 | PARTIAL | - Current day |
| R1-L0646 | P5 | PARTIAL | - Completed days |
| R1-L0647 | P5 | PARTIAL | - Completion percentage |
| R1-L0648 | P5 | PARTIAL | - Required problems solved |
| R1-L0649 | P5 | PARTIAL | - Tutorial completion |
| R1-L0650 | P5 | PARTIAL | - Pause/resume |
| R1-L0651 | P5 | PARTIAL | - Past days |
| R1-L0652 | P5 | PARTIAL | - Incomplete tasks |
| R1-L0654 | P5 | PARTIAL | Дахин нэвтрэхэд progress хадгалагдсан байна. |
| R1-L0656 | P5 | PARTIAL | Tutorial-ийг нээсэн төдийд өдөр completed болохгүй. |
| R1-L0658 | P5 | PARTIAL | Plan completion-ийг бодит даалгавар болон тодорхой дүрмээр тооц. |
| R1-L0664 | P6 | PARTIAL | Navigation-ийн дарааллыг: |
| R1-L0666 | P6 | PARTIAL | **Нүүр → Profile → Бодлогууд** |
| R1-L0668 | P6 | PARTIAL | болго. |
| R1-L0670 | P6 | PARTIAL | Profile-ийг тусдаа route/page болго. |
| R1-L0672 | P6 | PARTIAL | Хэрэглэгч өөрийн болон public profile үзэх боломжтой байна. |
| R1-L0676 | P8 | PARTIAL | - Овог нэр |
| R1-L0677 | P8 | PARTIAL | - Username |
| R1-L0678 | P8 | PARTIAL | - Profile picture |
| R1-L0679 | P8 | PARTIAL | - Сургууль |
| R1-L0680 | P8 | PARTIAL | - Богино танилцуулга |
| R1-L0681 | P8 | PARTIAL | - Бүртгүүлсэн огноо |
| R1-L0682 | P8 | PARTIAL | - Нийт бодсон бодлого |
| R1-L0683 | P8 | PARTIAL | - Одоо бодож байгаа бодлогууд |
| R1-L0684 | P8 | PARTIAL | - Priority problem progress |
| R1-L0685 | P8 | PARTIAL | - 100-day plan progress |
| R1-L0687 | P8 | PARTIAL | Profile өөрчлөх эрхийг зөвхөн эзэмшигч болон зөвшөөрөгдсөн admin-д олго. |
| R1-L0691 | P6 | PARTIAL | Өмнө нь илгээсэн зурагтай төстэй GitHub-style activity calendar хий. |
| R1-L0693 | P6 | PARTIAL | - Өдөр бүрийн solve count |
| R1-L0694 | P6 | PARTIAL | - Өнгөний intensity |
| R1-L0695 | P6 | PARTIAL | - Hover tooltip |
| R1-L0696 | P6 | PARTIAL | - Current streak |
| R1-L0697 | P6 | PARTIAL | - Longest streak |
| R1-L0698 | P6 | PARTIAL | - Сүүлийн 7 хоног |
| R1-L0699 | P6 | PARTIAL | - Сүүлийн 30 хоног |
| R1-L0700 | P6 | PARTIAL | - Сүүлийн 1 жил |
| R1-L0701 | P6 | PARTIAL | - All-time statistics |
| R1-L0703 | P6 | PARTIAL | Хуурамч solve date үүсгэхгүй. |
| R1-L0705 | P6 | PARTIAL | Хэрэв хуучин solved progress-тimestamp байхгүй бол түүнийг зохиож heatmap-д байрлуулж болохгүй. |
| R1-L0709 | P6 | PARTIAL | Solved problems-ийг rating тус бүрээр харуулсан bar chart. |
| R1-L0711 | P6 | PARTIAL | CF official rating болон estimated rating-ийг ялгаж харуулах. |
| R1-L0713 | P6 | PARTIAL | Unrated problems-ийг тусад нь харуул. |
| R1-L0717 | P6 | PARTIAL | Solved problems-ийн tag distribution-ийг donut chart-аар харуул. |
| R1-L0719 | P6 | PARTIAL | Chart-ын хажууд: |
| R1-L0721 | P6 | PARTIAL | - Tag |
| R1-L0722 | P6 | PARTIAL | - Бодсон бодлогын тоо |
| R1-L0724 | P6 | PARTIAL | харуул. |
| R1-L0726 | P6 | PARTIAL | Нэг бодлого олон tag-тай байж болох тул tag count-ийн нийлбэр нь нийт unique solved count-оос их байж болохыг зөв тооц. |
| R1-L0730 | P6 | PARTIAL | Өмнө хавсаргасан Codeforces-style статистикийн screenshot-уудыг reference болго. |
| R1-L0732 | P6 | PARTIAL | 7 хоног бүрийг нэг phase гэж үз. |
| R1-L0734 | P6 | PARTIAL | Phase бүрд: |
| R1-L0736 | P6 | PARTIAL | - Огноо |
| R1-L0737 | P6 | PARTIAL | - Solved problems |
| R1-L0738 | P6 | PARTIAL | - Attempted problems |
| R1-L0739 | P6 | PARTIAL | - Submission count, хэрэв өгөгдөл байгаа бол |
| R1-L0740 | P6 | PARTIAL | - AC/WA/TLE, хэрэв бодит verdict хадгалагддаг бол |
| R1-L0741 | P6 | PARTIAL | - Highest-rated solved problem |
| R1-L0742 | P6 | PARTIAL | - Average solved rating |
| R1-L0743 | P6 | PARTIAL | - Previous week-тэй харьцуулсан өөрчлөлт |
| R1-L0744 | P6 | PARTIAL | - Тухайн долоо хоногт бодсон бодлогууд |
| R1-L0746 | P6 | PARTIAL | гэсэн мэдээлэл гарга. |
| R1-L0748 | P6 | PARTIAL | Previous phase navigation нэм. |
| R1-L0750 | P6 | PARTIAL | Огнооны зааг, timezone болон давхар solve event-ийн тооцооллыг зөв хэрэгжүүл. |
| R1-L0752 | P6 | PARTIAL | Гаднын Codeforces submission statistics-ийг Erdene Club-ийн progress-тэй автоматаар адилтгаж болохгүй. |
| R1-L0756 | P4 | PARTIAL | Attempted, unsolved болон saved-for-later бодлогуудыг тусдаа жагсаалтаар харуул. |
| R1-L0758 | P4 | PARTIAL | Тэндээс шууд үргэлжлүүлэн бодож болох байх ёстой. |
| R1-L0764 | P7 | PARTIAL | Problems page-ийн UI/UX-ийг илүү цэвэр, орчин үеийн, мэргэжлийн болго. |
| R1-L0766 | P7 | PARTIAL | Одоо байгаа функцуудыг хадгал: |
| R1-L0768 | P7 | PARTIAL | - Search |
| R1-L0769 | P7 | PARTIAL | - Collections |
| R1-L0770 | P7 | PARTIAL | - Rating filter |
| R1-L0771 | P7 | PARTIAL | - Source filter |
| R1-L0772 | P7 | PARTIAL | - Tag filter |
| R1-L0773 | P7 | PARTIAL | - Priority |
| R1-L0774 | P7 | PARTIAL | - Solved/attempted state |
| R1-L0775 | P7 | PARTIAL | - Hints |
| R1-L0776 | P7 | PARTIAL | - Admin management |
| R1-L0778 | P7 | PARTIAL | Нэмэлтээр: |
| R1-L0780 | P7 | PARTIAL | - Compact/comfortable view |
| R1-L0781 | P7 | PARTIAL | - Илүү ойлгомжтой difficulty badge |
| R1-L0782 | P7 | PARTIAL | - Priority star |
| R1-L0783 | P7 | PARTIAL | - Associated tutorial link |
| R1-L0784 | P7 | PARTIAL | - 100-day plan association |
| R1-L0785 | P7 | PARTIAL | - Filter reset |
| R1-L0786 | P7 | PARTIAL | - Clear status icons |
| R1-L0787 | P7 | PARTIAL | - Better mobile layout |
| R1-L0788 | P7 | PARTIAL | - Thousands of problems-д тохирох performance |
| R1-L0790 | P7 | PARTIAL | Rating-д: |
| R1-L0792 | P7 | PARTIAL | - Official CF rating |
| R1-L0793 | P7 | PARTIAL | - Estimated rating |
| R1-L0794 | P7 | PARTIAL | - Unrated |
| R1-L0796 | P7 | PARTIAL | гэсэн ялгааг зөв харуул. |
| R1-L0798 | P7 | PARTIAL | Нэг бодлогын solved status болон бусад progress-г хуудсуудын хооронд нэг эх сурвалжаас уншдаг болго. |
| R1-L0804 | P7 | PARTIAL | **Dark theme-д одоогийн үндсэн дизайн, өнгөний зохицлыг хадгал.** |
| R1-L0806 | P7 | PARTIAL | Light theme-ийн одоогийн арын цайвар ногоон өнгө таалагдахгүй байна. |
| R1-L0808 | P7 | PARTIAL | Үндсэн background-ийг цагаан эсвэл цагаанд маш ойр neutral background болго. |
| R1-L0810 | P7 | PARTIAL | Дизайны чиглэл: |
| R1-L0812 | P7 | PARTIAL | - Background: #FFFFFF |
| R1-L0813 | P7 | PARTIAL | - Secondary surface: #F8FAFC |
| R1-L0814 | P7 | PARTIAL | - Cards: #FFFFFF |
| R1-L0815 | P7 | PARTIAL | - Border: #E5E7EB |
| R1-L0816 | P7 | PARTIAL | - Primary text: #111827 |
| R1-L0817 | P7 | PARTIAL | - Secondary text: #64748B |
| R1-L0818 | P7 | PARTIAL | - Accent: Erdene Club-ийн forest green |
| R1-L0820 | P7 | PARTIAL | Эдгээрийг яг хуулбарлах албагүй. Харагдах байдал болон contrast-ийг туршиж хамгийн зохистой хувилбарыг сонго. |
| R1-L0822 | P7 | PARTIAL | Зорилго: |
| R1-L0824 | P7 | PARTIAL | - Цэвэрхэн |
| R1-L0825 | P7 | PARTIAL | - Уншихад амар |
| R1-L0826 | P7 | PARTIAL | - Хэт их ногоон tint-гүй |
| R1-L0827 | P7 | PARTIAL | - Орчин үеийн |
| R1-L0828 | P7 | PARTIAL | - Товч бөгөөд мэргэжлийн |
| R1-L0829 | P7 | PARTIAL | - Dark theme-тэй нэг брэндийн мэдрэмжтэй |
| R1-L0831 | P7 | PARTIAL | Tutorial, Problems, Profile, 100-Day Plan, Home болон Admin интерфэйсүүдэд дизайны нэгдмэл байдлыг ханга. |
| R1-L0833 | P7 | PARTIAL | Theme switch ажилладаг хэвээр байна. |
| R1-L0839 | P7 | PARTIAL | Tutorial library-ийг USACO Guide шиг ашиглахад хялбар болго. |
| R1-L0843 | P7 | PARTIAL | - Сэдвүүдийг шатлалаар харуулах |
| R1-L0844 | P7 | PARTIAL | - Search |
| R1-L0845 | P7 | PARTIAL | - Level filter |
| R1-L0846 | P7 | PARTIAL | - Topic category |
| R1-L0847 | P7 | PARTIAL | - Prerequisite indicator |
| R1-L0848 | P7 | PARTIAL | - Reading progress |
| R1-L0849 | P7 | PARTIAL | - Recommended learning order |
| R1-L0853 | P7 | PARTIAL | - Title |
| R1-L0854 | P7 | PARTIAL | - Level |
| R1-L0855 | P7 | PARTIAL | - Reading time |
| R1-L0856 | P7 | PARTIAL | - Prerequisites |
| R1-L0857 | P7 | PARTIAL | - Table of contents |
| R1-L0858 | P7 | PARTIAL | - Гол тайлбар |
| R1-L0859 | P7 | PARTIAL | - Algorithm visualization |
| R1-L0860 | P7 | PARTIAL | - Code sections |
| R1-L0861 | P7 | PARTIAL | - Complexity analysis |
| R1-L0862 | P7 | PARTIAL | - Proof of correctness |
| R1-L0863 | P7 | PARTIAL | - Common mistakes |
| R1-L0864 | P7 | PARTIAL | - Related algorithms |
| R1-L0865 | P7 | PARTIAL | - Priority practice problems |
| R1-L0866 | P7 | PARTIAL | - Next tutorial |
| R1-L0868 | P7 | PARTIAL | Урт tutorial-ийг хэсэг хэсгээр нь эвтэйхэн унших боломжтой болго. |
| R1-L0870 | P7 | PARTIAL | Боломжтой бол sticky table of contents болон anchor navigation ашигла. |
| R1-L0872 | P7 | PARTIAL | MathJax болон C++ syntax highlighting хэвийн ажиллах ёстой. |
| R1-L0874 | P7 | PARTIAL | Монгол хэл дээрх бичвэрийг найруулгын болон зөв бичгийн алдаагүй болго. |
| R1-L0876 | P7 | PARTIAL | Англи хэлний existing support-ийг хадгал. Англи хувилбар бэлэн биш бол хоосон, худал орчуулга нийтлэхгүй. |
| R1-L0882 | P1 | PARTIAL | Энэ хэсгийг онцгой анхаар. |
| R1-L0884 | P1 | PARTIAL | Өмнө нь том SQL command болон урт migration ажиллуулахад удирдах, шалгах, алдаа засахад хүндрэлтэй байсан. |
| R1-L0886 | P1 | PARTIAL | Тиймээс **Supabase SQL-ийг жижиг, ойлгомжтой, тус тусдаа ажиллуулж болох хэсгүүдэд хуваа.** |
| R1-L0890 | P1 | PARTIAL | Боломжтой бол: |
| R1-L0892 | P1 | PARTIAL | - Нэг migration = нэг тодорхой зорилго |
| R1-L0893 | P1 | PARTIAL | - Нэг migration нь богино, уншихад амар |
| R1-L0894 | P1 | PARTIAL | - Том schema update-ийг олон дараалсан migration болгон хуваах |
| R1-L0896 | P1 | PARTIAL | Жишээ: |
| R1-L0898 | P1 | PARTIAL | - 001 — Tutorial relationships |
| R1-L0899 | P1 | PARTIAL | - 002 — Tutorial prerequisites |
| R1-L0900 | P1 | PARTIAL | - 003 — Tutorial progress |
| R1-L0901 | P1 | PARTIAL | - 004 — Study plan structure |
| R1-L0902 | P1 | PARTIAL | - 005 — Study plan progress |
| R1-L0903 | P1 | PARTIAL | - 006 — Profile statistics support |
| R1-L0904 | P1 | PARTIAL | - 007 — Necessary indexes |
| R1-L0905 | P1 | PARTIAL | - 008 — RLS policies |
| R1-L0907 | P1 | PARTIAL | Энэ бол зөвхөн жишээ. Бодит schema-г эхлээд шалга. |
| R1-L0911 | P8 | PARTIAL | Migration бүрийн хувьд: |
| R1-L0913 | P8 | PARTIAL | 1. Юу өөрчлөхийг тайлбарла. |
| R1-L0914 | P8 | PARTIAL | 2. SQL-ийг тусдаа файлд хадгал. |
| R1-L0915 | P8 | PARTIAL | 3. Dependencies-г тодорхойл. |
| R1-L0916 | P8 | PARTIAL | 4. Боломжтой бол transaction ашигла. |
| R1-L0917 | P8 | PARTIAL | 5. Migration-ийг давхар ажиллуулах эрсдэлийг тооц. |
| R1-L0918 | P8 | PARTIAL | 6. Өмнөх өгөгдөлд нөлөөлөх эсэхийг шалга. |
| R1-L0919 | P8 | PARTIAL | 7. Амжилттай хэрэгжсэн эсэхийг verify хийх query өг. |
| R1-L0920 | P8 | PARTIAL | 8. Шаардлагатай rollback эсвэл recovery арга бэлд. |
| R1-L0922 | P8 | PARTIAL | **Бүх database өөрчлөлтийг нэг аварга SQL файл болгож болохгүй.** |
| R1-L0926 | P8 | PARTIAL | Сэдэв, бодлого, 100-day plan зэрэг олон зуун өгөгдлийг урт `INSERT` statement болгон SQL Editor руу оруулах шаардлагагүй. |
| R1-L0928 | P8 | PARTIAL | Үүний оронд: |
| R1-L0930 | P8 | PARTIAL | - Жижиг batch |
| R1-L0931 | P8 | PARTIAL | - Version-controlled JSON/CSV |
| R1-L0932 | P8 | PARTIAL | - Safe import scripts |
| R1-L0933 | P8 | PARTIAL | - Idempotent upsert |
| R1-L0934 | P8 | PARTIAL | - Duplicate prevention |
| R1-L0936 | P8 | PARTIAL | ашигла. |
| R1-L0938 | P8 | PARTIAL | Боломжтой бол batch хэмжээ тохируулдаг байх. |
| R1-L0940 | P8 | PARTIAL | Migration болон content import-ийг тусад нь удирд. |
| R1-L0944 | P1 | PARTIAL | - Existing RLS-г эвдэхгүй. |
| R1-L0945 | P1 | PARTIAL | - User progress-д user ownership хадгал. |
| R1-L0946 | P1 | PARTIAL | - Admin permissions зөв ажиллана. |
| R1-L0947 | P1 | PARTIAL | - Frontend-д service-role key байрлуулахгүй. |
| R1-L0948 | P1 | PARTIAL | - SQL policy-уудыг бодит account permission-тай шалга. |
| R1-L0949 | P1 | PARTIAL | - Өгөгдөл устгах migration хийхээс зайлсхий. |
| R1-L0950 | P1 | PARTIAL | - Production database-д нөлөөлөхөөс өмнө backup/recovery боломжийг шалга. |
| R1-L0956 | P1 | PARTIAL | Tutorial, Problem Bank, 100-Day Plan, Profile системүүд тус тусдаа салангид өгөгдөлтэй байж болохгүй. |
| R1-L0958 | P1 | PARTIAL | Нэг асуудлыг нэг эх сурвалжаас удирдах зарчим баримтал. |
| R1-L0960 | P1 | PARTIAL | Жишээлбэл: |
| R1-L0962 | P1 | PARTIAL | **Problem A** |
| R1-L0964 | P1 | PARTIAL | Энэ бодлого: |
| R1-L0966 | P1 | PARTIAL | - Problem Bank-д нэг л бүртгэлтэй байна. |
| R1-L0967 | P1 | PARTIAL | - Binary Search tutorial-д харьяалагдаж болно. |
| R1-L0968 | P1 | PARTIAL | - Greedy tutorial-д давхар холбоотой байж болно. |
| R1-L0969 | P1 | PARTIAL | - 100-day plan-ийн Day 15-д багтаж болно. |
| R1-L0970 | P1 | PARTIAL | - Сурагчийн profile дээр solved гэж харагдана. |
| R1-L0971 | P1 | PARTIAL | - Rating distribution болон tag statistics-д зөв тооцогдоно. |
| R1-L0973 | P1 | PARTIAL | Хэрэв сурагч бодлогыг solved болгосон бол бүх хэсэгт progress шинэчлэгдэнэ. |
| R1-L0975 | P1 | PARTIAL | Тухайн бодлогын өөр өөр хуулбарууд дээр solved status тус тусдаа хадгалагдаж болохгүй. |
| R1-L0981 | P2 | PARTIAL | Tutorial болон 100-day plan-ийн чанарыг зөвхөн автоматаар хуудас үүссэн эсэхээр дүгнэж болохгүй. |
| R1-L0983 | P2 | PARTIAL | Агуулга бүрд дараах шалгуур тавь: |
| R1-L0985 | P2 | PARTIAL | - Яагаад хэрэгтэйг тайлбарласан уу? |
| R1-L0986 | P2 | PARTIAL | - Гол санааг ойлгуулсан уу? |
| R1-L0987 | P2 | PARTIAL | - Зөв байдлыг тайлбарласан уу? |
| R1-L0988 | P2 | PARTIAL | - Complexity-г үндэслэсэн үү? |
| R1-L0989 | P2 | PARTIAL | - Implementation-ийг хэсэгчилж тайлбарласан уу? |
| R1-L0990 | P2 | PARTIAL | - Common mistakes байгаа юу? |
| R1-L0991 | P2 | PARTIAL | - Холбоотой algorithms байгаа юу? |
| R1-L0992 | P2 | PARTIAL | - Prerequisite зөв үү? |
| R1-L0993 | P2 | PARTIAL | - Practice problems тохиромжтой юу? |
| R1-L0994 | P2 | PARTIAL | - Priority problems үнэхээр чухал уу? |
| R1-L0995 | P2 | PARTIAL | - Difficulty progression логиктой юу? |
| R1-L0996 | P2 | PARTIAL | - Монгол найруулга ойлгомжтой юу? |
| R1-L0997 | P2 | PARTIAL | - Code зөв ажиллаж байна уу? |
| R1-L0998 | P2 | PARTIAL | - Гадаад холбоосууд хүчинтэй юу? |
| R1-L1000 | P2 | PARTIAL | Хэрэв чанартай tutorial бичиж амжаагүй бол хоосон tutorial-ийг published гэж тэмдэглэж болохгүй. |
| R1-L1002 | P2 | PARTIAL | Draft/published status ашиглаж болно. |
| R1-L1004 | P2 | PARTIAL | **Бодит агуулгын чанарыг тооноос дээгүүр тавь.** |
| R1-L1010 | P8 | OPTIONAL_DEFERRED | Дараах боломжуудыг хэрэгжүүлэхэд тохиромжтой эсэхийг үнэлж, үнэ цэнтэй бол нэмж болно. |
| R1-L1014 | P8 | OPTIONAL_DEFERRED | Сурагчийн одоогийн түвшинд тохирох next tutorial болон next problem санал болгох. |
| R1-L1018 | P8 | OPTIONAL_DEFERRED | Алгоритмуудын хоорондын хамаарлыг харагдах байдлаар дүрслэх. |
| R1-L1020 | P8 | OPTIONAL_DEFERRED | Жишээ: |
| R1-L1022 | P8 | OPTIONAL_DEFERRED | DFS → Tree traversal → Euler tour → LCA → Heavy-light decomposition |
| R1-L1026 | P6 | OPTIONAL_DEFERRED | Өмнө нь бодож чадаагүй эсвэл hint ашигласан бодлогуудыг дахин санал болгох. |
| R1-L1030 | P6 | OPTIONAL_DEFERRED | Бодлого бүр дээр сурагч өөрийн тэмдэглэл бичиж болно: |
| R1-L1032 | P6 | OPTIONAL_DEFERRED | - Гол ажиглалт |
| R1-L1033 | P6 | OPTIONAL_DEFERRED | - Яагаад гацсан |
| R1-L1034 | P6 | OPTIONAL_DEFERRED | - Ямар алдаа гаргасан |
| R1-L1035 | P6 | OPTIONAL_DEFERRED | - Юу сурсан |
| R1-L1037 | P6 | OPTIONAL_DEFERRED | Энэ тэмдэглэл анхнаасаа private байна. |
| R1-L1041 | P6 | OPTIONAL_DEFERRED | Сурагч ойлгомжгүй хэсгийг тэмдэглэж, алдаа мэдээлж болно. |
| R1-L1043 | P6 | OPTIONAL_DEFERRED | Admin эдгээрийг review хийх боломжтой байж болно. |
| R1-L1047 | P2 | OPTIONAL_DEFERRED | Админд: |
| R1-L1049 | P2 | OPTIONAL_DEFERRED | - Practice problem-гүй tutorial |
| R1-L1050 | P2 | OPTIONAL_DEFERRED | - Tutorial-тай холбогдоогүй problem |
| R1-L1051 | P2 | OPTIONAL_DEFERRED | - Broken links |
| R1-L1052 | P2 | OPTIONAL_DEFERRED | - Duplicate problems |
| R1-L1053 | P2 | OPTIONAL_DEFERRED | - Missing metadata |
| R1-L1054 | P2 | OPTIONAL_DEFERRED | - Unpublished tutorials |
| R1-L1055 | P2 | OPTIONAL_DEFERRED | - Missing 100-day assignments |
| R1-L1057 | P2 | OPTIONAL_DEFERRED | зэргийг харах боломж нэм. |
| R1-L1059 | P2 | OPTIONAL_DEFERRED | Эдгээр нь үндсэн ажлыг хойшлуулахгүйгээр дараагийн өргөтгөл болж болно. |
| R1-L1065 | P8 | PARTIAL | Энэ бол том хэмжээний ажил учраас логик дарааллаар хэрэгжүүл. |
| R1-L1069 | P8 | PARTIAL | Repository, database, tutorial engine, problem model, progress системийг шалга. |
| R1-L1071 | P8 | PARTIAL | Хуучин ажлаа дахин хийхгүй. |
| R1-L1075 | P8 | PARTIAL | Шинэ tutorial layout, агуулгын бүтэц, variants, prerequisites, practice problem relationships, priority badges зэргийг хэрэгжүүл. |
| R1-L1077 | P8 | PARTIAL | Эхлээд 2–3 tutorial-ийг бүрэн чанартай жишиг болгож хий. |
| R1-L1081 | P8 | PARTIAL | Одоогийн tutorial-уудыг найруулж сайжруул. |
| R1-L1083 | P8 | PARTIAL | Дараа нь шинэ сэдвүүд нэм. |
| R1-L1087 | P4 | PARTIAL | Existing problem pool-ийг ангил. |
| R1-L1089 | P4 | PARTIAL | CSES болон олон улсын олимпиадын баталгаажсан бодлогуудыг нэм. |
| R1-L1091 | P4 | PARTIAL | Tutorial бүрийн practice list-ийг бүрдүүл. |
| R1-L1095 | P5 | PARTIAL | Бодит tutorial болон problem ID-д суурилсан 100 өдрийн хөтөлбөр бүтээ. |
| R1-L1097 | P5 | PARTIAL | 100 өдрийн бүх холбоосыг шалга. |
| R1-L1101 | P6 | PARTIAL | Profile page, activity heatmap, rating distribution, tag distribution, weekly phases, attempted problems хэсгүүдийг хэрэгжүүл. |
| R1-L1105 | P7 | PARTIAL | Light theme-ийг цагаан, цэвэрхэн болго. |
| R1-L1107 | P7 | PARTIAL | Problems болон Tutorials хуудасны дизайныг сайжруул. |
| R1-L1109 | P7 | PARTIAL | Dark theme-ийн үндсэн төрхийг хадгал. |
| R1-L1113 | P8 | PARTIAL | Authentication, progress, Supabase, admin, filters, charts, plan, mobile, GitHub Pages болон CMS navigation-ийг шалга. |
| R1-L1115 | P8 | PARTIAL | Үе шат бүрийг боломжтой бол тусдаа commit болгон хадгал. |
| R1-L1117 | P8 | PARTIAL | Том өөрчлөлт хийхээс өмнө буцаах боломжтой төлөвийг баталгаажуул. |
| R1-L1123 | P8 | PARTIAL | Чи өмнө нь энэ сайтыг хөгжүүлж байсан тул шаардлагагүйгээр надаас repository-ийн үндсэн бүтэц, Supabase ашигладаг эсэх, GitHub Pages тохиргоо гэх мэт өмнө нь мэддэг зүйлсээ дахин асуух хэрэггүй. |
| R1-L1125 | P8 | PARTIAL | Гэхдээ бодит төлөв өмнөх контекстоос өөрчлөгдсөн байж болох тул хэрэгтэй хэсгийг шалгаж баталгаажуул. |
| R1-L1127 | P8 | PARTIAL | Үе шат бүрийн дараа монголоор: |
| R1-L1129 | P8 | PARTIAL | 1. Ямар ажил хийсэн |
| R1-L1130 | P8 | PARTIAL | 2. Ямар файл өөрчлөгдсөн |
| R1-L1131 | P8 | PARTIAL | 3. Ямар database өөрчлөлт орсон |
| R1-L1132 | P8 | PARTIAL | 4. Ямар migration ажилласан |
| R1-L1133 | P8 | PARTIAL | 5. Ямар контент бодитоор нэмэгдсэн |
| R1-L1134 | P8 | PARTIAL | 6. Ямар test амжилттай болсон |
| R1-L1135 | P8 | PARTIAL | 7. Ямар зүйл дутуу үлдсэн |
| R1-L1136 | P8 | PARTIAL | 8. Дараагийн алхам |
| R1-L1138 | P8 | PARTIAL | гэсэн товч тайлан өг. |
| R1-L1140 | P8 | PARTIAL | Зөвхөн төлөвлөгөө бичээд зогсохгүй, хэрэгжүүлэх боломжтой ажлуудыг бодитоор хий. |
| R1-L1142 | P8 | PARTIAL | Нэг дор хэт том SQL эсвэл frontend patch хийхээс зайлсхий. |
| R1-L1144 | P8 | PARTIAL | Хэрэв Supabase дээр миний гараар ажиллуулах шаардлагатай SQL байвал: |
| R1-L1146 | P8 | PARTIAL | - Богино хэсэг болгон хуваа. |
| R1-L1147 | P8 | PARTIAL | - Зөв дарааллаар өг. |
| R1-L1148 | P8 | PARTIAL | - Яг юу хийж байгааг тайлбарла. |
| R1-L1149 | P8 | PARTIAL | - Нэг хэсэг бүтэлгүйтвэл засварлахад амар байлга. |
| R1-L1151 | P8 | PARTIAL | Хэрэв Work mode шууд эрхтэй, аюулгүйгээр хэрэгжүүлж болох өөрчлөлт байвал өөрөө гүйцэтгэ. |
| R1-L1153 | P8 | PARTIAL | Production data-г алдагдуулах, permission сулруулах эсвэл буцаах боломжгүй үйлдэлд болгоомжтой ханд. |
| R1-L1159 | P8 | PARTIAL | Erdene Club-д орсон сурагч: |
| R1-L1161 | P8 | PARTIAL | 1. Profile-доо нэвтэрнэ. |
| R1-L1162 | P8 | PARTIAL | 2. Өөрийн progress-ийг харна. |
| R1-L1163 | P8 | PARTIAL | 3. 100 хоногийн төлөвлөгөөг эхлүүлнэ. |
| R1-L1164 | P8 | PARTIAL | 4. Өнөөдрийн сурах сэдвээ харна. |
| R1-L1165 | P8 | PARTIAL | 5. Тухайн алгоритм яагаад хэрэгтэйг ойлгоно. |
| R1-L1166 | P8 | PARTIAL | 6. Алгоритмын гол санааг алхам алхмаар сурна. |
| R1-L1167 | P8 | PARTIAL | 7. Яагаад зөв, яагаад хурдан ажилладгийг ойлгоно. |
| R1-L1168 | P8 | PARTIAL | 8. C++ implementation-ийг бие даан бичиж сурна. |
| R1-L1169 | P8 | PARTIAL | 9. Холбоотой алгоритмууд руу шилжинэ. |
| R1-L1170 | P8 | PARTIAL | 10. Тухайн сэдвийн хамгийн хэрэгтэй Priority бодлогуудыг бодно. |
| R1-L1171 | P8 | PARTIAL | 11. Шаардлагатай бол шаталсан hint ашиглана. |
| R1-L1172 | P8 | PARTIAL | 12. Өөрийн хийсэн ажиглалт, алдааг тэмдэглэнэ. |
| R1-L1173 | P8 | PARTIAL | 13. Өдөр тутмын progress-ийг хадгална. |
| R1-L1174 | P8 | PARTIAL | 14. Activity heatmap, rating distribution, tag statistics-аа харна. |
| R1-L1175 | P8 | PARTIAL | 15. Дараагийн түвшинд системтэй шилжинэ. |
| R1-L1177 | P8 | PARTIAL | Ингэснээр Erdene Club дараах системүүдийн сайн талуудыг хослуулах ёстой: |
| R1-L1179 | P8 | PARTIAL | **USACO Guide-ийн сургалтын чанар + CSES-ийн бодлогын зохион байгуулалт + Codeforces-ийн статистик + IOI-ийн problem-solving аргачлал + Erdene Club-ийн хувийн сургалтын төлөвлөгөө.** |
| R1-L1181 | P8 | PARTIAL | Гэхдээ бэлэн сайтын дизайныг шууд хуулбарлахгүй. Erdene Club-ийн өөрийн танигдах өнгө төрхийг хадгал. |
| R1-L1185 | P8 | PARTIAL | Өмнөх төслийн контекстээ ашиглан одоогийн код болон өгөгдлийг шалга. |
| R1-L1187 | P8 | PARTIAL | Хамгийн эхэнд tutorial engine болон өгөгдлийн холбоосуудыг сайжруул. |
| R1-L1189 | P8 | PARTIAL | Дараа нь жишиг болгон **Binary Search, Greedy, Dynamic Programming** гэсэн гурван tutorial-ийг дээрх шаардлагын дагуу үнэхээр чанартай шинэчил. |
| R1-L1191 | P8 | PARTIAL | Эдгээрийн бүтэц, problem relationships, implementation explanation, priority practice problems зөв ажиллаж байгааг баталгаажуул. |
| R1-L1193 | P8 | PARTIAL | Үүний дараа үлдсэн tutorial-ууд болон problem bank-ийг системтэй өргөтгө. |
| R1-L1195 | P8 | PARTIAL | Хэрэгжүүлэх явцад 100-day plan, profile, problems page, light theme зэрэг бусад шаардлагыг орхигдуулахгүй. |
| R1-L1197 | P8 | PARTIAL | **Чиний зорилго бол зүгээр олон feature нэмэх биш, сурагчдын мэдээлэлзүйн олимпиадын бэлтгэлд бодит үр дүн өгдөг, чанартай сургалтын платформ бүтээх юм.** |
| R2-L0005 | P8 | PARTIAL | Чи бол Erdene Club сайтыг өмнө нь хөгжүүлсэн, repository, Supabase database, GitHub Pages deployment, authentication, problems, tutorials, admin tools болон UI/UX архитектурыг сайн мэддэг ChatGPT Work mode дахь миний хөгжүүлэлтийн туслах юм. |
| R2-L0007 | P8 | PARTIAL | Саяхан бид Erdene Club-д томоохон шинэчлэл хийсэн. Сайт шинэчлэгдсэн боловч **өмнөх prompt-д заасан олон шаардлага дутуу хэрэгжсэн байна.** |
| R2-L0009 | P8 | PARTIAL | Одоогийн сайт: |
| R2-L0011 | P8 | PARTIAL | https://erdeneclub.com/ |
| R2-L0013 | P8 | PARTIAL | Tutorials: |
| R2-L0015 | P8 | PARTIAL | https://erdeneclub.com/#tutorials |
| R2-L0017 | P8 | PARTIAL | Өмнөх шинэчлэлээр ойролцоогоор 55 tutorial бий болсон. Гэхдээ би өмнөх prompt-д анхан шатнаас IOI-ийн ахисан түвшин хүртэлх маш олон алгоритм, өгөгдлийн бүтэц, бодлого бодох аргачлалын tutorial нэмэхийг шаардсан. |
| R2-L0019 | P8 | PARTIAL | Одоогийн 55 tutorial энэ шаардлагыг бүрэн хангахгүй байна. |
| R2-L0021 | P8 | PARTIAL | Түүнчлэн: |
| R2-L0023 | P8 | PARTIAL | - Олон tutorial-ийн агуулга хангалттай гүн биш. |
| R2-L0024 | P8 | PARTIAL | - Зарим tutorial өмнө заасан сургалтын бүтцийг мөрдөөгүй. |
| R2-L0025 | P8 | PARTIAL | - Tutorial editor-ийн боломж хязгаарлагдмал. |
| R2-L0026 | P8 | PARTIAL | - Tutorial-д зураг болон визуал материал оруулах боломжийг сайжруулах хэрэгтэй. |
| R2-L0027 | P8 | PARTIAL | - Problems хэсгийн дизайныг илүү сайн болгох шаардлагатай. |
| R2-L0028 | P8 | PARTIAL | - Өмнөх prompt-ийн зарим шаардлага бүрэн хэрэгжээгүй байж болзошгүй. |
| R2-L0030 | P8 | PARTIAL | **Энэ удаагийн зорилго бол өмнөх шаардлагуудыг дахин өнгөц хэрэгжүүлэх биш, дутуу зүйл бүрийг илрүүлж, жинхэнэ утгаар нь бүрэн гүйцээх юм.** |
| R2-L0032 | P8 | PARTIAL | Өмнөх харилцан ярианд өгсөн томоохон хөгжүүлэлтийн prompt-ийг энэ даалгаврын үндсэн шаардлагын баримт бичиг гэж үз. |
| R2-L0034 | P8 | PARTIAL | Шинэ prompt нь өмнөх шаардлагуудыг орлохгүй, харин илүү нарийвчилж, хэрэгжилтийг шалгаж, дуусгах зориулалттай. |
| R2-L0040 | P8 | PARTIAL | Ажлаа эхлэхдээ одоогийн GitHub repository, Supabase schema, байгаа tutorial болон problem өгөгдөл, deployed website-ийг шалга. |
| R2-L0042 | P8 | PARTIAL | Мөн өмнөх prompt, өмнөх Work conversation, өмнө хэрэгжүүлсэн өөрчлөлтүүдийг ашигла. |
| R2-L0044 | P8 | PARTIAL | Дараах асуултуудад бодитоор хариул: |
| R2-L0046 | P8 | PARTIAL | 1. Өмнөх prompt-д нийт ямар шаардлагууд байсан бэ? |
| R2-L0047 | P8 | PARTIAL | 2. Аль нь бүрэн хэрэгжсэн бэ? |
| R2-L0048 | P8 | PARTIAL | 3. Аль нь хэсэгчлэн хэрэгжсэн бэ? |
| R2-L0049 | P8 | PARTIAL | 4. Аль нь огт хэрэгжээгүй вэ? |
| R2-L0050 | P8 | PARTIAL | 5. Аль нь зөвхөн frontend-д байгаа боловч database болон progress-тэй бүрэн холбогдоогүй вэ? |
| R2-L0051 | P8 | PARTIAL | 6. Аль нь кодод бичигдсэн боловч production сайт дээр ажиллахгүй байгаа вэ? |
| R2-L0052 | P8 | PARTIAL | 7. Аль tutorial-ууд өмнөх сургалтын стандартыг хангахгүй байна вэ? |
| R2-L0053 | P8 | PARTIAL | 8. Ямар алгоритм болон problem-solving сэдвүүд tutorial санд байхгүй байна вэ? |
| R2-L0054 | P8 | PARTIAL | 9. Ямар tutorial-д хангалттай practice problems байхгүй вэ? |
| R2-L0055 | P8 | PARTIAL | 10. Profile, 100-day plan, Problems, UI/UX, Admin Editor дээр юу дутуу байна вэ? |
| R2-L0059 | P2 | PARTIAL | Өмнөх болон одоогийн бүх шаардлагыг нэгтгэсэн checklist үүсгэ. |
| R2-L0061 | P2 | PARTIAL | Шаардлага бүр дараах төлөвтэй байна: |
| R2-L0063 | P2 | PARTIAL | - COMPLETE — бүрэн хэрэгжсэн, шалгасан |
| R2-L0064 | P2 | PARTIAL | - PARTIAL — хэсэгчлэн хэрэгжсэн |
| R2-L0065 | P2 | PARTIAL | - MISSING — хэрэгжээгүй |
| R2-L0066 | P2 | PARTIAL | - BROKEN — хэрэгжсэн боловч ажиллахгүй |
| R2-L0067 | P2 | PARTIAL | - BLOCKED — гадаад эрх эсвэл мэдээлэл шаардлагатай |
| R2-L0069 | P2 | PARTIAL | Requirement бүрийг тухайн код, database table, tutorial эсвэл UI component-той холбож шалга. |
| R2-L0071 | P2 | PARTIAL | **Зөвхөн файл байгаа учраас COMPLETE гэж тэмдэглэж болохгүй.** |
| R2-L0073 | P2 | PARTIAL | Ажиллаж байгаа эсэх, бодит өгөгдөлтэй эсэх, чанарын шаардлага хангасан эсэхийг баталгаажуул. |
| R2-L0075 | P2 | PARTIAL | Аудитыг repository дотор Markdown report хэлбэрээр хадгал. |
| R2-L0077 | P2 | PARTIAL | Дараа нь бүх MISSING, PARTIAL, BROKEN шаардлагыг хэрэгжүүлэх ажлаа үргэлжлүүл. |
| R2-L0083 | P3 | PARTIAL | Одоогийн 55 tutorial-оор хязгаарлагдаж болохгүй. |
| R2-L0085 | P3 | PARTIAL | Өмнөх prompt-д дурдсан бүх сэдвийг дахин нэг бүрчлэн шалгаж, байхгүй сэдвүүдийг нэм. |
| R2-L0087 | P3 | PARTIAL | Мөн мэдээлэлзүйн олимпиадад зайлшгүй хэрэгтэй боловч өмнөх жагсаалтад ороогүй сэдвүүд байвал нэмж болно. |
| R2-L0089 | P3 | PARTIAL | Сэдвийн тоог зохиомлоор хязгаарлахгүй. |
| R2-L0091 | P3 | PARTIAL | Жишээлбэл, Binary Search-ийн олон чухал хувилбар байвал бүгдийг нэг хэт урт tutorial-д шахахын оронд тусдаа, сайн холбогдсон tutorial-ууд болго. |
| R2-L0095 | P3 | PARTIAL | - Time complexity |
| R2-L0096 | P3 | PARTIAL | - Space complexity |
| R2-L0097 | P3 | PARTIAL | - C++ STL |
| R2-L0098 | P3 | PARTIAL | - Arrays |
| R2-L0099 | P3 | PARTIAL | - Strings |
| R2-L0100 | P3 | PARTIAL | - Sorting |
| R2-L0101 | P3 | PARTIAL | - Prefix sum |
| R2-L0102 | P3 | PARTIAL | - 2D prefix sum |
| R2-L0103 | P3 | PARTIAL | - Difference array |
| R2-L0104 | P3 | PARTIAL | - Two pointers |
| R2-L0105 | P3 | PARTIAL | - Sliding window |
| R2-L0106 | P3 | PARTIAL | - Binary search |
| R2-L0107 | P3 | PARTIAL | - Lower bound |
| R2-L0108 | P3 | PARTIAL | - Upper bound |
| R2-L0109 | P3 | PARTIAL | - Binary search on answer |
| R2-L0110 | P3 | PARTIAL | - Binary search on real numbers |
| R2-L0111 | P3 | PARTIAL | - Brute force |
| R2-L0112 | P3 | PARTIAL | - Complete search |
| R2-L0113 | P3 | PARTIAL | - Recursion |
| R2-L0114 | P3 | PARTIAL | - Backtracking |
| R2-L0115 | P3 | PARTIAL | - Bitmask enumeration |
| R2-L0116 | P3 | PARTIAL | - Basic greedy |
| R2-L0117 | P3 | PARTIAL | - Basic constructive algorithms |
| R2-L0118 | P3 | PARTIAL | - Frequency counting |
| R2-L0119 | P3 | PARTIAL | - Coordinate compression |
| R2-L0120 | P3 | PARTIAL | - Basic combinatorics |
| R2-L0121 | P3 | PARTIAL | - Basic modular arithmetic |
| R2-L0122 | P3 | PARTIAL | - Basic number theory |
| R2-L0123 | P3 | PARTIAL | - Bit manipulation |
| R2-L0124 | P3 | PARTIAL | - XOR techniques |
| R2-L0125 | P3 | PARTIAL | - Invariants |
| R2-L0126 | P3 | PARTIAL | - Basic proof techniques |
| R2-L0130 | P3 | PARTIAL | - Greedy algorithms |
| R2-L0131 | P3 | PARTIAL | - Greedy correctness |
| R2-L0132 | P3 | PARTIAL | - Exchange argument |
| R2-L0133 | P3 | PARTIAL | - Greedy stays ahead |
| R2-L0134 | P3 | PARTIAL | - Sorting-based greedy |
| R2-L0135 | P3 | PARTIAL | - Interval scheduling |
| R2-L0136 | P3 | PARTIAL | - Sweep line |
| R2-L0137 | P3 | PARTIAL | - Event processing |
| R2-L0138 | P3 | PARTIAL | - Working backwards |
| R2-L0139 | P3 | PARTIAL | - Maintaining invariants |
| R2-L0140 | P3 | PARTIAL | - Finding observations |
| R2-L0141 | P3 | PARTIAL | - Constructive reasoning |
| R2-L0142 | P3 | PARTIAL | - Counterexample construction |
| R2-L0143 | P3 | PARTIAL | - Transforming problems |
| R2-L0144 | P3 | PARTIAL | - Mathematical modeling |
| R2-L0145 | P3 | PARTIAL | - Constraint analysis |
| R2-L0146 | P3 | PARTIAL | - Improving brute force |
| R2-L0147 | P3 | PARTIAL | - Case analysis |
| R2-L0148 | P3 | PARTIAL | - Problem decomposition |
| R2-L0149 | P3 | PARTIAL | - Offline processing |
| R2-L0153 | P3 | PARTIAL | - Stack |
| R2-L0154 | P3 | PARTIAL | - Queue |
| R2-L0155 | P3 | PARTIAL | - Deque |
| R2-L0156 | P3 | PARTIAL | - Priority queue |
| R2-L0157 | P3 | PARTIAL | - Set and multiset |
| R2-L0158 | P3 | PARTIAL | - Map and unordered_map |
| R2-L0159 | P3 | PARTIAL | - Monotonic stack |
| R2-L0160 | P3 | PARTIAL | - Monotonic queue |
| R2-L0161 | P3 | PARTIAL | - DSU |
| R2-L0162 | P3 | PARTIAL | - Fenwick tree |
| R2-L0163 | P3 | PARTIAL | - Segment tree |
| R2-L0164 | P3 | PARTIAL | - Lazy propagation |
| R2-L0165 | P3 | PARTIAL | - Sparse table |
| R2-L0166 | P3 | PARTIAL | - Range minimum/maximum queries |
| R2-L0167 | P3 | PARTIAL | - Persistent segment tree |
| R2-L0168 | P3 | PARTIAL | - Dynamic segment tree |
| R2-L0169 | P3 | PARTIAL | - Merge sort tree |
| R2-L0170 | P3 | PARTIAL | - Wavelet tree |
| R2-L0171 | P3 | PARTIAL | - Ordered data structures |
| R2-L0172 | P3 | PARTIAL | - Trie |
| R2-L0173 | P3 | PARTIAL | - Li Chao tree |
| R2-L0174 | P3 | PARTIAL | - Small-to-large merging |
| R2-L0175 | P3 | PARTIAL | - Mo's algorithm |
| R2-L0176 | P3 | PARTIAL | - Advanced offline queries |
| R2-L0180 | P3 | PARTIAL | - Graph representations |
| R2-L0181 | P3 | PARTIAL | - BFS |
| R2-L0182 | P3 | PARTIAL | - DFS |
| R2-L0183 | P3 | PARTIAL | - Connected components |
| R2-L0184 | P3 | PARTIAL | - Bipartite graphs |
| R2-L0185 | P3 | PARTIAL | - Cycle detection |
| R2-L0186 | P3 | PARTIAL | - Topological sorting |
| R2-L0187 | P3 | PARTIAL | - DAG algorithms |
| R2-L0188 | P3 | PARTIAL | - Shortest paths |
| R2-L0189 | P3 | PARTIAL | - Dijkstra |
| R2-L0190 | P3 | PARTIAL | - 0-1 BFS |
| R2-L0191 | P3 | PARTIAL | - Bellman-Ford |
| R2-L0192 | P3 | PARTIAL | - Floyd-Warshall |
| R2-L0193 | P3 | PARTIAL | - Minimum spanning tree |
| R2-L0194 | P3 | PARTIAL | - Kruskal |
| R2-L0195 | P3 | PARTIAL | - Prim |
| R2-L0196 | P3 | PARTIAL | - Strongly connected components |
| R2-L0197 | P3 | PARTIAL | - Kosaraju |
| R2-L0198 | P3 | PARTIAL | - Tarjan |
| R2-L0199 | P3 | PARTIAL | - Bridges |
| R2-L0200 | P3 | PARTIAL | - Articulation points |
| R2-L0201 | P3 | PARTIAL | - Biconnected components |
| R2-L0202 | P3 | PARTIAL | - Eulerian paths |
| R2-L0203 | P3 | PARTIAL | - Eulerian circuits |
| R2-L0204 | P3 | PARTIAL | - Functional graphs |
| R2-L0205 | P3 | PARTIAL | - Binary lifting on functional graphs |
| R2-L0206 | P3 | PARTIAL | - Bipartite matching |
| R2-L0207 | P3 | PARTIAL | - Maximum flow |
| R2-L0208 | P3 | PARTIAL | - Minimum cut |
| R2-L0209 | P3 | PARTIAL | - Network flow modeling |
| R2-L0210 | P3 | PARTIAL | - Min-cost max-flow |
| R2-L0211 | P3 | PARTIAL | - 2-SAT |
| R2-L0212 | P3 | PARTIAL | - Advanced graph modeling |
| R2-L0216 | P3 | PARTIAL | - Tree properties |
| R2-L0217 | P3 | PARTIAL | - Tree DFS |
| R2-L0218 | P3 | PARTIAL | - Tree BFS |
| R2-L0219 | P3 | PARTIAL | - Tree diameter |
| R2-L0220 | P3 | PARTIAL | - Tree centers |
| R2-L0221 | P3 | PARTIAL | - Rooted trees |
| R2-L0222 | P3 | PARTIAL | - Subtree sizes |
| R2-L0223 | P3 | PARTIAL | - Euler tour |
| R2-L0224 | P3 | PARTIAL | - LCA |
| R2-L0225 | P3 | PARTIAL | - Binary lifting |
| R2-L0226 | P3 | PARTIAL | - Distance queries |
| R2-L0227 | P3 | PARTIAL | - Tree DP |
| R2-L0228 | P3 | PARTIAL | - Rerooting DP |
| R2-L0229 | P3 | PARTIAL | - Subtree queries |
| R2-L0230 | P3 | PARTIAL | - Path queries |
| R2-L0231 | P3 | PARTIAL | - Heavy-light decomposition |
| R2-L0232 | P3 | PARTIAL | - Centroid decomposition |
| R2-L0233 | P3 | PARTIAL | - Tree flattening |
| R2-L0234 | P3 | PARTIAL | - Virtual tree |
| R2-L0235 | P3 | PARTIAL | - Small-to-large on trees |
| R2-L0236 | P3 | PARTIAL | - Advanced tree techniques |
| R2-L0240 | P3 | PARTIAL | - DP introduction |
| R2-L0241 | P3 | PARTIAL | - State and transition design |
| R2-L0242 | P3 | PARTIAL | - Memoization |
| R2-L0243 | P3 | PARTIAL | - Bottom-up DP |
| R2-L0244 | P3 | PARTIAL | - 1D DP |
| R2-L0245 | P3 | PARTIAL | - 2D DP |
| R2-L0246 | P3 | PARTIAL | - Grid DP |
| R2-L0247 | P3 | PARTIAL | - Knapsack DP |
| R2-L0248 | P3 | PARTIAL | - LIS |
| R2-L0249 | P3 | PARTIAL | - LCS |
| R2-L0250 | P3 | PARTIAL | - Interval DP |
| R2-L0251 | P3 | PARTIAL | - DAG DP |
| R2-L0252 | P3 | PARTIAL | - Tree DP |
| R2-L0253 | P3 | PARTIAL | - Rerooting |
| R2-L0254 | P3 | PARTIAL | - Bitmask DP |
| R2-L0255 | P3 | PARTIAL | - Digit DP |
| R2-L0256 | P3 | PARTIAL | - Profile DP |
| R2-L0257 | P3 | PARTIAL | - SOS DP |
| R2-L0258 | P3 | PARTIAL | - Probability DP |
| R2-L0259 | P3 | PARTIAL | - Expected value DP |
| R2-L0260 | P3 | PARTIAL | - Game DP |
| R2-L0261 | P3 | PARTIAL | - DP with prefix sums |
| R2-L0262 | P3 | PARTIAL | - DP with data structures |
| R2-L0263 | P3 | PARTIAL | - Divide and conquer optimization |
| R2-L0264 | P3 | PARTIAL | - Knuth optimization |
| R2-L0265 | P3 | PARTIAL | - Convex hull trick |
| R2-L0266 | P3 | PARTIAL | - Li Chao optimization |
| R2-L0267 | P3 | PARTIAL | - Monotone queue optimization |
| R2-L0268 | P3 | PARTIAL | - State compression |
| R2-L0269 | P3 | PARTIAL | - Advanced DP modeling |
| R2-L0273 | P3 | PARTIAL | - String matching |
| R2-L0274 | P3 | PARTIAL | - Prefix function |
| R2-L0275 | P3 | PARTIAL | - KMP |
| R2-L0276 | P3 | PARTIAL | - Z-function |
| R2-L0277 | P3 | PARTIAL | - String hashing |
| R2-L0278 | P3 | PARTIAL | - Double hashing |
| R2-L0279 | P3 | PARTIAL | - Trie |
| R2-L0280 | P3 | PARTIAL | - Aho-Corasick |
| R2-L0281 | P3 | PARTIAL | - Suffix array |
| R2-L0282 | P3 | PARTIAL | - LCP |
| R2-L0283 | P3 | PARTIAL | - Suffix automaton |
| R2-L0284 | P3 | PARTIAL | - Manacher |
| R2-L0285 | P3 | PARTIAL | - Palindromes |
| R2-L0286 | P3 | PARTIAL | - String DP |
| R2-L0287 | P3 | PARTIAL | - Advanced string techniques |
| R2-L0291 | P3 | PARTIAL | - Prime numbers |
| R2-L0292 | P3 | PARTIAL | - Sieve of Eratosthenes |
| R2-L0293 | P3 | PARTIAL | - Linear sieve |
| R2-L0294 | P3 | PARTIAL | - GCD and LCM |
| R2-L0295 | P3 | PARTIAL | - Euclidean algorithm |
| R2-L0296 | P3 | PARTIAL | - Extended Euclidean algorithm |
| R2-L0297 | P3 | PARTIAL | - Modular arithmetic |
| R2-L0298 | P3 | PARTIAL | - Modular exponentiation |
| R2-L0299 | P3 | PARTIAL | - Modular inverse |
| R2-L0300 | P3 | PARTIAL | - Fermat's little theorem |
| R2-L0301 | P3 | PARTIAL | - Euler's theorem |
| R2-L0302 | P3 | PARTIAL | - Euler phi |
| R2-L0303 | P3 | PARTIAL | - Chinese remainder theorem |
| R2-L0304 | P3 | PARTIAL | - Combinatorics |
| R2-L0305 | P3 | PARTIAL | - Factorials and binomial coefficients |
| R2-L0306 | P3 | PARTIAL | - Inclusion-exclusion |
| R2-L0307 | P3 | PARTIAL | - Pigeonhole principle |
| R2-L0308 | P3 | PARTIAL | - Matrix exponentiation |
| R2-L0309 | P3 | PARTIAL | - Linear recurrences |
| R2-L0310 | P3 | PARTIAL | - Probability |
| R2-L0311 | P3 | PARTIAL | - Expected value |
| R2-L0312 | P3 | PARTIAL | - Grundy numbers |
| R2-L0313 | P3 | PARTIAL | - Combinatorial games |
| R2-L0314 | P3 | PARTIAL | - Fast Fourier Transform |
| R2-L0315 | P3 | PARTIAL | - Number Theoretic Transform |
| R2-L0316 | P3 | PARTIAL | - Polynomial algorithms |
| R2-L0320 | P3 | PARTIAL | - Points and vectors |
| R2-L0321 | P3 | PARTIAL | - Dot product |
| R2-L0322 | P3 | PARTIAL | - Cross product |
| R2-L0323 | P3 | PARTIAL | - Orientation |
| R2-L0324 | P3 | PARTIAL | - Line intersection |
| R2-L0325 | P3 | PARTIAL | - Segment intersection |
| R2-L0326 | P3 | PARTIAL | - Polygon area |
| R2-L0327 | P3 | PARTIAL | - Point in polygon |
| R2-L0328 | P3 | PARTIAL | - Convex hull |
| R2-L0329 | P3 | PARTIAL | - Rotating calipers |
| R2-L0330 | P3 | PARTIAL | - Closest pair of points |
| R2-L0331 | P3 | PARTIAL | - Sweep line geometry |
| R2-L0332 | P3 | PARTIAL | - Circle geometry |
| R2-L0333 | P3 | PARTIAL | - Computational geometry precision |
| R2-L0334 | P3 | PARTIAL | - Advanced geometry techniques |
| R2-L0338 | P3 | PARTIAL | - Observation-driven problem solving |
| R2-L0339 | P3 | PARTIAL | - Creative reasoning |
| R2-L0340 | P3 | PARTIAL | - Subtask-oriented solutions |
| R2-L0341 | P3 | PARTIAL | - Partial scoring strategy |
| R2-L0342 | P3 | PARTIAL | - Deriving algorithms from constraints |
| R2-L0343 | P3 | PARTIAL | - Choosing DP states |
| R2-L0344 | P3 | PARTIAL | - Greedy proof |
| R2-L0345 | P3 | PARTIAL | - Constructing counterexamples |
| R2-L0346 | P3 | PARTIAL | - Stress testing |
| R2-L0347 | P3 | PARTIAL | - Random test generators |
| R2-L0348 | P3 | PARTIAL | - Debugging C++ |
| R2-L0349 | P3 | PARTIAL | - Interactive problems |
| R2-L0350 | P3 | PARTIAL | - Communication tasks |
| R2-L0351 | P3 | PARTIAL | - Output-only tasks |
| R2-L0352 | P3 | PARTIAL | - Contest time management |
| R2-L0353 | P3 | PARTIAL | - Editorial analysis |
| R2-L0354 | P3 | PARTIAL | - Learning from failed attempts |
| R2-L0355 | P3 | PARTIAL | - Recognizing problem transformations |
| R2-L0356 | P3 | PARTIAL | - Combining multiple algorithms |
| R2-L0358 | P3 | PARTIAL | Энэ жагсаалтыг өмнөх prompt-ийн сэдвүүдтэй нэгтгэнэ. |
| R2-L0360 | P3 | PARTIAL | Давхардсан сэдвүүдийг ойлгомжтой canonical tutorial болгон зохион байгуулж болно. |
| R2-L0362 | P3 | PARTIAL | **Гэхдээ сэдвийг жагсаалтаас чимээгүй хасаж болохгүй.** Хэрэв нэг tutorial-д нэгтгэвэл requirement report-д хаана орсныг нь тодорхой тэмдэглэ. |
| R2-L0368 | P2 | PARTIAL | Энэ бол маш чухал шаардлага. |
| R2-L0370 | P2 | PARTIAL | Одоогийн 55 tutorial байгаа гэдэг нь тэдгээрийг хангалттай сайн гэсэн үг биш. |
| R2-L0372 | P2 | PARTIAL | **Tutorial бүрийг нэг бүрчлэн шалга.** |
| R2-L0374 | P2 | PARTIAL | Хэрэв өмнөх prompt-д заасан бүтцийг хангаагүй бол тухайн tutorial-ийг дахин найруул. |
| R2-L0376 | P2 | PARTIAL | Хангалтгүй tutorial-ийг хэдхэн догол мөр нэмээд COMPLETE гэж тэмдэглэж болохгүй. |
| R2-L0378 | P2 | PARTIAL | Шаардлагатай үед хуучин тайлбарыг бүтнээр нь шинээр бич. |
| R2-L0380 | P2 | PARTIAL | Гэхдээ tutorial ID, progress, URL болон problem relationships-г хадгал. |
| R2-L0386 | P2 | PARTIAL | Сурагчид тулгарч буй асуудлыг эхлээд үзүүл. |
| R2-L0388 | P2 | PARTIAL | Алгоритм байхгүй үед ямар бэрхшээл гарч байгааг тайлбарла. |
| R2-L0392 | P2 | PARTIAL | Brute force эсвэл илүү хялбар аргаар яаж шийдэхийг харуул. |
| R2-L0396 | P2 | PARTIAL | Энгийн шийдлээс илүү сайн шийдэлд хүргэх observation-ийг алхам алхмаар тайлбарла. |
| R2-L0400 | P2 | PARTIAL | Тухайн алгоритм яг юу хийдэг, ямар invariant хадгалдгийг ойлгуул. |
| R2-L0404 | P2 | PARTIAL | Бодит, жижиг жишээгээр алхам бүрийг үзүүл. |
| R2-L0408 | P2 | PARTIAL | Correctness proof оруул. |
| R2-L0410 | P2 | PARTIAL | Шаардлагатай үед induction, contradiction, exchange argument, loop invariant ашигла. |
| R2-L0414 | P2 | PARTIAL | Time complexity-ийн томьёог зүгээр бичээд орхихгүй. |
| R2-L0416 | P2 | PARTIAL | Яагаад ийм нийлмэл байдалтай болдгийг математик болон intuitive талаас нь тайлбарла. |
| R2-L0420 | P2 | PARTIAL | Кодыг логик хэсгүүдэд хуваа: |
| R2-L0422 | P2 | PARTIAL | - Data structures |
| R2-L0423 | P2 | PARTIAL | - Initialization |
| R2-L0424 | P2 | PARTIAL | - Main algorithm |
| R2-L0425 | P2 | PARTIAL | - Updates/transitions |
| R2-L0426 | P2 | PARTIAL | - Result computation |
| R2-L0427 | P2 | PARTIAL | - Complete code |
| R2-L0429 | P2 | PARTIAL | Хэсэг бүрийг ойлгомжтой тайлбарла. |
| R2-L0433 | P2 | PARTIAL | Хамгийн чухал boundary cases-ийг харуул. |
| R2-L0437 | P2 | PARTIAL | Түгээмэл алдаа болон counterexample үзүүл. |
| R2-L0441 | P2 | PARTIAL | Related variations-ийг тайлбарлаж, холбогдох tutorial руу чиглүүл. |
| R2-L0445 | P2 | PARTIAL | Бодлогын ямар шинж тэмдэг тухайн алгоритмыг санал болгодгийг тайлбарла. |
| R2-L0449 | P4 | PARTIAL | Warm-up → Standard → Observation → Application → Challenge → Olympiad extension. |
| R2-L0453 | P8 | PARTIAL | Тухайн сэдвийг эзэмшихэд хамгийн чухал бодлогуудыг ⭐ Priority гэж тодруул. |
| R2-L0457 | P2 | PARTIAL | Сурагч юу ойлгож, юу хийж чаддаг болсон байх ёстойг тодорхойл. |
| R2-L0461 | P2 | PARTIAL | Tutorial-ууд: |
| R2-L0463 | P2 | PARTIAL | - Сурах бичиг шиг ойлгомжтой |
| R2-L0464 | P2 | PARTIAL | - Монгол хэлний зөв найруулгатай |
| R2-L0465 | P2 | PARTIAL | - Математикийн тэмдэглэгээ зөв |
| R2-L0466 | P2 | PARTIAL | - Ойлголтууд логик дараалалтай |
| R2-L0467 | P2 | PARTIAL | - Хэт товч биш |
| R2-L0468 | P2 | PARTIAL | - Хэрэггүй давталтгүй |
| R2-L0469 | P2 | PARTIAL | - Бодит жишээтэй |
| R2-L0470 | P2 | PARTIAL | - Алгоритм нээх сэтгэлгээг хөгжүүлдэг |
| R2-L0472 | P2 | PARTIAL | байх ёстой. |
| R2-L0474 | P2 | PARTIAL | Шууд англи эхээс машин орчуулга шиг найруулж болохгүй. |
| R2-L0478 | P2 | PARTIAL | Tutorial бүрийг ижил урттай болгох шаардлагагүй. |
| R2-L0480 | P2 | PARTIAL | Суурь жижиг ойлголтын tutorial богино байж болно. |
| R2-L0482 | P2 | PARTIAL | Харин Segment Tree, Dijkstra, Tree DP, Digit DP, Network Flow зэрэг том сэдэвт дэлгэрэнгүй тайлбар, олон жишээ, олон implementation section хэрэгтэй. |
| R2-L0484 | P2 | PARTIAL | Хоосон template бөглөж байгаа мэт агуулга үүсгэхгүй. |
| R2-L0488 | P2 | PARTIAL | Монгол хувилбар үндсэн чанарын стандартыг бүрэн хангасан байна. |
| R2-L0490 | P2 | PARTIAL | Англи хувилбар байгаа бол мөн чанартай байна. |
| R2-L0492 | P2 | PARTIAL | Монгол болон англи агуулгын бүтцийн ялгааг хяна. |
| R2-L0494 | P2 | PARTIAL | Хоосон, дутуу, автоматаар үүсгэсэн чанаргүй англи орчуулгыг published болгохгүй. |
| R2-L0500 | P0 | PARTIAL | Одоогийн tutorial editor хязгаарлагдмал байна. |
| R2-L0502 | P0 | PARTIAL | Би tutorial-уудыг админы хувьд чөлөөтэй бичиж, засварлаж, зураг, код, хүснэгт, математик томьёо, тайлбар, интерактив материал нэмэх боломжтой болмоор байна. |
| R2-L0504 | P0 | PARTIAL | Editor нь зүгээр нэг plain text textarea байж болохгүй. |
| R2-L0506 | P0 | PARTIAL | Боломжтой бол **Notion, GitHub Markdown Editor, Medium болон орчин үеийн rich-text editor-ийн сайн талуудыг хослуулсан** content editor болго. |
| R2-L0508 | P0 | PARTIAL | Гэхдээ хэт төвөгтэй, удаан, тогтворгүй editor хийхээс зайлсхий. |
| R2-L0512 | P0 | PARTIAL | Дараахыг дэмж: |
| R2-L0514 | P0 | PARTIAL | - Headings H1–H4 |
| R2-L0515 | P0 | PARTIAL | - Paragraph |
| R2-L0516 | P0 | PARTIAL | - Bold |
| R2-L0517 | P0 | PARTIAL | - Italic |
| R2-L0518 | P0 | PARTIAL | - Underline |
| R2-L0519 | P0 | PARTIAL | - Strikethrough |
| R2-L0520 | P0 | PARTIAL | - Inline code |
| R2-L0521 | P0 | PARTIAL | - Code block |
| R2-L0522 | P0 | PARTIAL | - Bulleted list |
| R2-L0523 | P0 | PARTIAL | - Numbered list |
| R2-L0524 | P0 | PARTIAL | - Checklist |
| R2-L0525 | P0 | PARTIAL | - Blockquote |
| R2-L0526 | P0 | PARTIAL | - Tables |
| R2-L0527 | P0 | PARTIAL | - Horizontal separator |
| R2-L0528 | P0 | PARTIAL | - Links |
| R2-L0529 | P0 | PARTIAL | - Internal tutorial links |
| R2-L0530 | P0 | PARTIAL | - Problem links |
| R2-L0531 | P0 | PARTIAL | - Callout boxes |
| R2-L0532 | P0 | PARTIAL | - Collapsible sections |
| R2-L0533 | P0 | PARTIAL | - Warning boxes |
| R2-L0534 | P0 | PARTIAL | - Important notes |
| R2-L0535 | P0 | PARTIAL | - Example boxes |
| R2-L0537 | P0 | PARTIAL | Formatting toolbar эсвэл slash-command menu ашиглаж болно. |
| R2-L0541 | P0 | PARTIAL | Энэ шаардлагыг заавал хэрэгжүүл. |
| R2-L0543 | P0 | PARTIAL | Админ tutorial бичиж байхдаа өөрийн компьютер эсвэл утаснаас зураг upload хийж болно. |
| R2-L0545 | P0 | PARTIAL | Дэмжих формат: |
| R2-L0547 | P0 | PARTIAL | - PNG |
| R2-L0548 | P0 | PARTIAL | - JPG/JPEG |
| R2-L0549 | P0 | PARTIAL | - WebP |
| R2-L0550 | P0 | PARTIAL | - SVG — зөвхөн аюулгүй sanitization болон security шаардлага хангасан тохиолдолд |
| R2-L0552 | P0 | PARTIAL | Зураг оруулахдаа: |
| R2-L0554 | P0 | PARTIAL | - Drag and drop |
| R2-L0555 | P0 | PARTIAL | - File picker |
| R2-L0556 | P0 | PARTIAL | - Clipboard paste, боломжтой бол |
| R2-L0557 | P0 | PARTIAL | - Image preview |
| R2-L0558 | P0 | PARTIAL | - Resize |
| R2-L0559 | P0 | PARTIAL | - Alignment |
| R2-L0560 | P0 | PARTIAL | - Caption |
| R2-L0561 | P0 | PARTIAL | - Alt text |
| R2-L0562 | P0 | PARTIAL | - Replace image |
| R2-L0563 | P0 | PARTIAL | - Delete image |
| R2-L0565 | P0 | PARTIAL | гэсэн боломжуудтай байлга. |
| R2-L0567 | P0 | PARTIAL | Зураг нь tutorial дотор зөв байрлалд харагдах ёстой. |
| R2-L0571 | P1 | PARTIAL | Зургийг browser-ийн localStorage-д хадгалж болохгүй. |
| R2-L0573 | P1 | PARTIAL | Supabase Storage ашиглах боломжийг одоогийн архитектурт нийцүүлэн судалж хэрэгжүүл. |
| R2-L0575 | P1 | PARTIAL | Шаардлага: |
| R2-L0577 | P1 | PARTIAL | - Admin-only upload |
| R2-L0578 | P1 | PARTIAL | - MIME/type validation |
| R2-L0579 | P1 | PARTIAL | - File size limits |
| R2-L0580 | P1 | PARTIAL | - Unique file paths |
| R2-L0581 | P1 | PARTIAL | - Secure storage policy |
| R2-L0582 | P1 | PARTIAL | - Broken link prevention |
| R2-L0583 | P1 | PARTIAL | - Orphaned image cleanup strategy |
| R2-L0584 | P1 | PARTIAL | - Safe public delivery for published tutorial images |
| R2-L0586 | P1 | PARTIAL | Service-role key-г frontend-д байрлуулж болохгүй. |
| R2-L0588 | P1 | PARTIAL | Image upload нь GitHub Pages static frontend дээр аюулгүй ажиллах ёстой. |
| R2-L0592 | P0 | PARTIAL | Tutorial дотор C++ code block оруулахад: |
| R2-L0594 | P0 | PARTIAL | - Syntax highlighting |
| R2-L0595 | P0 | PARTIAL | - Language selection |
| R2-L0596 | P0 | PARTIAL | - Copy button |
| R2-L0597 | P0 | PARTIAL | - Auto indentation |
| R2-L0598 | P0 | PARTIAL | - Proper monospace font |
| R2-L0599 | P0 | PARTIAL | - Long code horizontal scrolling |
| R2-L0600 | P0 | PARTIAL | - Readable line spacing |
| R2-L0602 | P0 | PARTIAL | байх ёстой. |
| R2-L0604 | P0 | PARTIAL | Боломжтой бол code block-ийг editor дотор шууд засахад эвтэйхэн болго. |
| R2-L0608 | P8 | PARTIAL | MathJax эсвэл одоогийн math rendering engine-ийг хадгалж сайжруул. |
| R2-L0610 | P8 | PARTIAL | Inline math болон block math дэмж. |
| R2-L0612 | P8 | PARTIAL | Математикийн томьёог editor дээр preview хийж болдог байх ёстой. |
| R2-L0616 | P0 | PARTIAL | Tutorial-д: |
| R2-L0618 | P0 | PARTIAL | - Array visualization |
| R2-L0619 | P0 | PARTIAL | - Graph visualization |
| R2-L0620 | P0 | PARTIAL | - Tree diagram |
| R2-L0621 | P0 | PARTIAL | - DP table |
| R2-L0622 | P0 | PARTIAL | - Segment tree diagram |
| R2-L0623 | P0 | PARTIAL | - State transition illustration |
| R2-L0625 | P0 | PARTIAL | зэрэг материалыг оруулж болох уян хатан structure бий болго. |
| R2-L0627 | P0 | PARTIAL | Эхний ээлжид зураг, diagram, styled content block-уудаар хэрэгжүүлж болно. |
| R2-L0629 | P0 | PARTIAL | Боломжтой үед interactive visualization component ашиглаж болно. |
| R2-L0631 | P0 | PARTIAL | Гэхдээ SVG, Mermaid эсвэл бусад дүрслэлийн хэлбэрийн security болон rendering асуудлыг тооц. |
| R2-L0635 | P0 | PARTIAL | Админ давтан ашиглаж болох боловсролын content block-уудтай байвал сайн. |
| R2-L0637 | P0 | PARTIAL | Жишээ: |
| R2-L0639 | P0 | PARTIAL | - Algorithm explanation |
| R2-L0640 | P0 | PARTIAL | - Complexity analysis |
| R2-L0641 | P0 | PARTIAL | - Proof |
| R2-L0642 | P0 | PARTIAL | - Observation |
| R2-L0643 | P0 | PARTIAL | - Common mistake |
| R2-L0644 | P0 | PARTIAL | - Code walkthrough |
| R2-L0645 | P0 | PARTIAL | - Example |
| R2-L0646 | P0 | PARTIAL | - Priority problems |
| R2-L0647 | P0 | PARTIAL | - Related tutorials |
| R2-L0648 | P0 | PARTIAL | - Practice checklist |
| R2-L0650 | P0 | PARTIAL | Эдгээрийг editor toolbar эсвэл insert menu-ээс нэмж болно. |
| R2-L0652 | P0 | PARTIAL | Энгийн админд ч ашиглахад хялбар байх ёстой. |
| R2-L0656 | P0 | PARTIAL | Дараахыг нэм: |
| R2-L0658 | P0 | PARTIAL | - Draft хадгалах |
| R2-L0659 | P0 | PARTIAL | - Published status |
| R2-L0660 | P0 | PARTIAL | - Live preview |
| R2-L0661 | P0 | PARTIAL | - Save indicator |
| R2-L0662 | P0 | PARTIAL | - Unsaved changes warning |
| R2-L0663 | P0 | PARTIAL | - Auto-save |
| R2-L0664 | P0 | PARTIAL | - Revision history, боломжтой бол |
| R2-L0665 | P0 | PARTIAL | - Restore previous version |
| R2-L0666 | P0 | PARTIAL | - Preview before publish |
| R2-L0668 | P0 | PARTIAL | Одоогийн tutorial агуулга алдагдахгүй байх ёстой. |
| R2-L0670 | P0 | PARTIAL | Auto-save нь өгөгдлийг санамсаргүй overwrite хийхгүй, сүлжээ тасарсан үед зохистой ажиллана. |
| R2-L0674 | P0 | PARTIAL | Editor нь нэг хатуу layout-д баригдах ёсгүй. |
| R2-L0676 | P0 | PARTIAL | Би шаардлагатай үед: |
| R2-L0678 | P0 | PARTIAL | - Нэг сэдэвт олон зураг оруулах |
| R2-L0679 | P0 | PARTIAL | - Кодын олон хэсэг оруулах |
| R2-L0680 | P0 | PARTIAL | - Тайлбарын хайрцаг нэмэх |
| R2-L0681 | P0 | PARTIAL | - Дурын дарааллаар content block байрлуулах |
| R2-L0682 | P0 | PARTIAL | - Урт tutorial бичих |
| R2-L0683 | P0 | PARTIAL | - Хүснэгт үүсгэх |
| R2-L0684 | P0 | PARTIAL | - Хоёр алгоритмыг харьцуулах |
| R2-L0685 | P0 | PARTIAL | - Математикийн баталгаа оруулах |
| R2-L0686 | P0 | PARTIAL | - Тусдаа анхааруулга гаргах |
| R2-L0687 | P0 | PARTIAL | - Related problems-ийг өгүүллийн дунд байрлуулах |
| R2-L0689 | P0 | PARTIAL | боломжтой байх ёстой. |
| R2-L0691 | P0 | PARTIAL | Гэхдээ content editor-ийн чөлөөт байдал нь нийт сайтын дизайныг эвдэж болохгүй. |
| R2-L0693 | P0 | PARTIAL | Responsive typography, spacing болон аюулгүй rendering-г хадгал. |
| R2-L0697 | P1 | PARTIAL | Rich-text editor нэвтрүүлэхдээ XSS болон unsafe HTML injection-оос хамгаал. |
| R2-L0699 | P1 | PARTIAL | Хэрэглэгчийн өгсөн HTML/Markdown-ийг аюулгүй render хий. |
| R2-L0701 | P1 | PARTIAL | Admin authorization-г зөв хэрэгжүүл. |
| R2-L0703 | P1 | PARTIAL | Сайтын бусад хэрэглэгчид tutorial-ийг зөвшөөрөлгүй өөрчилж болохгүй. |
| R2-L0709 | P4 | PARTIAL | Tutorial бүрийн хамгийн чухал хэсгүүдийн нэг нь practice problems юм. |
| R2-L0711 | P4 | PARTIAL | Одоо байгаа бодлогын сангаас тухайн сэдэвт хамгийн тохирох бодлогуудыг сонго. |
| R2-L0713 | P4 | PARTIAL | Хэрэв хангалтгүй бол: |
| R2-L0715 | P4 | PARTIAL | - CSES |
| R2-L0716 | P4 | PARTIAL | - Codeforces |
| R2-L0717 | P4 | PARTIAL | - AtCoder |
| R2-L0718 | P4 | PARTIAL | - USACO |
| R2-L0719 | P4 | PARTIAL | - IOI |
| R2-L0720 | P4 | PARTIAL | - EGOI |
| R2-L0721 | P4 | PARTIAL | - JOI |
| R2-L0722 | P4 | PARTIAL | - APIO |
| R2-L0723 | P4 | PARTIAL | - CEOI |
| R2-L0724 | P4 | PARTIAL | - COCI |
| R2-L0725 | P4 | PARTIAL | - BOI |
| R2-L0726 | P4 | PARTIAL | - OJ.uz |
| R2-L0728 | P4 | PARTIAL | зэрэг эх сурвалжаас verified бодлогууд нэм. |
| R2-L0732 | P4 | PARTIAL | Зөвхөн tag таарч байна гэдэг шалтгаанаар tutorial-д бодлого холбож болохгүй. |
| R2-L0734 | P4 | PARTIAL | Бодлогын intended solution, гол observation, difficulty болон prerequisite-ийг харгалз. |
| R2-L0738 | P4 | PARTIAL | Tutorial бүрд боломжийн тооны ⭐ Priority бодлого сонго. |
| R2-L0740 | P4 | PARTIAL | Priority бодлого нь: |
| R2-L0742 | P4 | PARTIAL | - Алгоритмын гол санааг ойлгуулдаг |
| R2-L0743 | P4 | PARTIAL | - Шинэ ажиглалт шаарддаг |
| R2-L0744 | P4 | PARTIAL | - Түгээмэл хэрэглээг харуулдаг |
| R2-L0745 | P4 | PARTIAL | - Дараагийн сэдвийн суурь болдог |
| R2-L0746 | P4 | PARTIAL | - Сурагчийн ойлголтыг шалгадаг |
| R2-L0748 | P4 | PARTIAL | байх ёстой. |
| R2-L0750 | P4 | PARTIAL | Хамгийн хүнд бодлогыг автоматаар Priority болгож болохгүй. |
| R2-L0754 | P5 | PARTIAL | Бодлогууд: |
| R2-L0756 | P5 | PARTIAL | Warm-up → Standard → Observation → Challenge → Olympiad |
| R2-L0758 | P5 | PARTIAL | гэсэн логик дараалалтай байна. |
| R2-L0762 | P4 | PARTIAL | Админ editor-оос: |
| R2-L0764 | P4 | PARTIAL | - Бодлого хайх |
| R2-L0765 | P4 | PARTIAL | - Tutorial-д холбох |
| R2-L0766 | P4 | PARTIAL | - Холбоос устгах |
| R2-L0767 | P4 | PARTIAL | - Дараалал өөрчлөх |
| R2-L0768 | P4 | PARTIAL | - Priority болгох |
| R2-L0769 | P4 | PARTIAL | - Difficulty category сонгох |
| R2-L0770 | P4 | PARTIAL | - Learning objective бичих |
| R2-L0772 | P4 | PARTIAL | боломжтой болго. |
| R2-L0774 | P4 | PARTIAL | Эдгээр өөрчлөлт Supabase-д найдвартай хадгалагдана. |
| R2-L0780 | P7 | PARTIAL | Одоогийн Problems page-ийн дизайн хангалттай сайн биш байна. |
| R2-L0782 | P7 | PARTIAL | Энэ удаа өнгө, padding бага зэрэг өөрчлөөд зогсохгүй **Problems page-ийн мэдээллийн зохион байгуулалт болон хэрэглэгчийн туршлагыг бодитоор сайжруул.** |
| R2-L0784 | P7 | PARTIAL | Сайтын бусад хэсгийн дизайнтай нийцсэн, орчин үеийн, цэвэрхэн problem browser бүтээ. |
| R2-L0788 | P7 | PARTIAL | Дараахыг сайжруул: |
| R2-L0790 | P7 | PARTIAL | - Problem listing |
| R2-L0791 | P7 | PARTIAL | - Search |
| R2-L0792 | P7 | PARTIAL | - Filters |
| R2-L0793 | P7 | PARTIAL | - Sorting |
| R2-L0794 | P7 | PARTIAL | - Difficulty badges |
| R2-L0795 | P7 | PARTIAL | - Tags |
| R2-L0796 | P7 | PARTIAL | - Priority indicator |
| R2-L0797 | P7 | PARTIAL | - Solved status |
| R2-L0798 | P7 | PARTIAL | - Attempted status |
| R2-L0799 | P7 | PARTIAL | - Collections |
| R2-L0800 | P7 | PARTIAL | - Pagination |
| R2-L0801 | P7 | PARTIAL | - Mobile responsiveness |
| R2-L0805 | P7 | PARTIAL | Бодлого бүрийн мөрийг уншихад ойлгомжтой болго. |
| R2-L0807 | P7 | PARTIAL | Харуулах мэдээлэл: |
| R2-L0809 | P7 | PARTIAL | - Problem title |
| R2-L0810 | P7 | PARTIAL | - Source |
| R2-L0811 | P7 | PARTIAL | - Official ID |
| R2-L0812 | P7 | PARTIAL | - Rating эсвэл estimated difficulty |
| R2-L0813 | P7 | PARTIAL | - Primary tag |
| R2-L0814 | P7 | PARTIAL | - Secondary tags |
| R2-L0815 | P7 | PARTIAL | - Solved/attempted/unsolved |
| R2-L0816 | P7 | PARTIAL | - Priority |
| R2-L0817 | P7 | PARTIAL | - Associated tutorial |
| R2-L0819 | P7 | PARTIAL | Rating өнгө нь Codeforces-ийн ерөнхий difficulty color system-тэй ойлгомжтой байж болно. |
| R2-L0821 | P7 | PARTIAL | Гэхдээ site-ийн өөрийн brand identity-г хадгал. |
| R2-L0825 | P7 | PARTIAL | Олон filter нэг дор бөөгнөрсөн, төвөгтэй харагдахгүй байх ёстой. |
| R2-L0827 | P7 | PARTIAL | Desktop дээр компакт, ойлгомжтой filter panel. |
| R2-L0829 | P7 | PARTIAL | Mobile дээр collapsible filter drawer ашиглаж болно. |
| R2-L0831 | P7 | PARTIAL | Active filters-ийг chips байдлаар харуулж болно. |
| R2-L0833 | P7 | PARTIAL | Reset all filters товч ажиллах ёстой. |
| R2-L0837 | P7 | PARTIAL | Бодлогын дэлгэрэнгүй хэсэгт: |
| R2-L0839 | P7 | PARTIAL | - Source link |
| R2-L0840 | P7 | PARTIAL | - Difficulty |
| R2-L0841 | P7 | PARTIAL | - Tags |
| R2-L0842 | P7 | PARTIAL | - Priority |
| R2-L0843 | P7 | PARTIAL | - Related tutorials |
| R2-L0844 | P7 | PARTIAL | - Associated 100-day plan |
| R2-L0845 | P7 | PARTIAL | - Three-level hints |
| R2-L0846 | P7 | PARTIAL | - Progress controls |
| R2-L0847 | P7 | PARTIAL | - Personal notes, хэрэв хэрэгжсэн бол |
| R2-L0849 | P7 | PARTIAL | харуул. |
| R2-L0853 | P7 | PARTIAL | Бодлогын сан мянга гаруй болох үед UI удааширч болохгүй. |
| R2-L0855 | P7 | PARTIAL | Pagination, indexing, filtering, efficient rendering ашигла. |
| R2-L0857 | P7 | PARTIAL | Хэрэггүй бүх өгөгдлийг client руу нэг дор татахаас зайлсхий. |
| R2-L0861 | P7 | PARTIAL | Dark theme-ийн одоогийн сайн дизайн хэвээр байх ёстой. |
| R2-L0863 | P7 | PARTIAL | Light theme нь white/neutral, цэвэрхэн, уншихад эвтэйхэн байна. |
| R2-L0865 | P7 | PARTIAL | Problems page нь хэт олон өнгөтэй, хэт жижиг font-той, шахцалдсан хүснэгт шиг харагдаж болохгүй. |
| R2-L0871 | P5 | PARTIAL | Өмнөх ажлаар 100-day plan-ийн өгөгдөл үүссэн гэж мэдээлсэн. |
| R2-L0873 | P5 | PARTIAL | Гэхдээ дараахыг баталгаажуул: |
| R2-L0875 | P5 | PARTIAL | - Яг 100 өдөр байгаа юу? |
| R2-L0876 | P5 | PARTIAL | - Өдөр бүр бодит tutorial-тай юу? |
| R2-L0877 | P5 | PARTIAL | - Өдөр бүр бодит бодлоготой юу? |
| R2-L0878 | P5 | PARTIAL | - Сэдвүүд prerequisite дарааллаар явж байгаа юу? |
| R2-L0879 | P5 | PARTIAL | - Difficulty progression зөв үү? |
| R2-L0880 | P5 | PARTIAL | - Review day-ууд байгаа юу? |
| R2-L0881 | P5 | PARTIAL | - Observation day-ууд байгаа юу? |
| R2-L0882 | P5 | PARTIAL | - Virtual contest болон subtask practice байгаа юу? |
| R2-L0883 | P5 | PARTIAL | - Priority problems зөв сонгогдсон уу? |
| R2-L0884 | P5 | PARTIAL | - User progress хадгалагдаж байна уу? |
| R2-L0885 | P5 | PARTIAL | - Bookmark, pause/resume ажиллаж байна уу? |
| R2-L0886 | P5 | PARTIAL | - Шинээр нэмсэн tutorial-уудыг төлөвлөгөөнд зөв холбосон уу? |
| R2-L0888 | P5 | PARTIAL | Хэрэв дутуу бол сайжруул. |
| R2-L0890 | P5 | PARTIAL | **Шинээр нэмэгдсэн олон алгоритмын tutorial-уудтай 100-day plan-ийг уялдуул.** |
| R2-L0892 | P5 | PARTIAL | Гэхдээ 100 хоногт бүх ахисан алгоритмыг заавал шахаж оруулах шаардлагагүй. |
| R2-L0894 | P5 | PARTIAL | Үндсэн 100-day plan нь 1300–1400 түвшний сурагчдад бодитой байг. |
| R2-L0896 | P5 | PARTIAL | Маш ахисан сэдвүүдийг нэмэлт Advanced/IOI roadmap болгон санал болгож болно. |
| R2-L0902 | P6 | PARTIAL | Өмнөх prompt-д дараахыг шаардсан: |
| R2-L0904 | P6 | PARTIAL | - Profile page |
| R2-L0905 | P6 | PARTIAL | - Profile picture |
| R2-L0906 | P6 | PARTIAL | - Full name |
| R2-L0907 | P6 | PARTIAL | - Username |
| R2-L0908 | P6 | PARTIAL | - School |
| R2-L0909 | P6 | PARTIAL | - Solved problems |
| R2-L0910 | P6 | PARTIAL | - Attempted problems |
| R2-L0911 | P6 | PARTIAL | - Rating distribution |
| R2-L0912 | P6 | PARTIAL | - Tag distribution |
| R2-L0913 | P6 | PARTIAL | - Activity heatmap |
| R2-L0914 | P6 | PARTIAL | - Weekly phases |
| R2-L0915 | P6 | PARTIAL | - 100-day progress |
| R2-L0917 | P6 | PARTIAL | Эдгээрийг нэг бүрчлэн шалга. |
| R2-L0919 | P6 | PARTIAL | Өгөгдөл бодит эсэхийг баталгаажуул. |
| R2-L0921 | P6 | PARTIAL | Solved count, tag count, rating histogram болон weekly statistics буруу тооцоологдох ёсгүй. |
| R2-L0923 | P6 | PARTIAL | Одоогоор хэрэгжээгүй шаардлагуудыг гүйцээ. |
| R2-L0929 | P1 | PARTIAL | Өмнөх шаардлага хүчинтэй хэвээр. |
| R2-L0931 | P1 | PARTIAL | Database migration-уудыг нэг аварга SQL command болгож болохгүй. |
| R2-L0933 | P1 | PARTIAL | Дараах зарчим баримтал: |
| R2-L0935 | P1 | PARTIAL | - Нэг migration = нэг тодорхой зорилго |
| R2-L0936 | P1 | PARTIAL | - Dependency дараалал зөв |
| R2-L0937 | P1 | PARTIAL | - Богино SQL |
| R2-L0938 | P1 | PARTIAL | - Transaction, боломжтой үед |
| R2-L0939 | P1 | PARTIAL | - Idempotent migration |
| R2-L0940 | P1 | PARTIAL | - Backup/recovery |
| R2-L0941 | P1 | PARTIAL | - Verification query |
| R2-L0942 | P1 | PARTIAL | - Existing progress preservation |
| R2-L0944 | P1 | PARTIAL | Жишээ: |
| R2-L0946 | P1 | PARTIAL | 001 — Tutorial content blocks |
| R2-L0948 | P1 | PARTIAL | 002 — Tutorial image metadata |
| R2-L0950 | P1 | PARTIAL | 003 — Tutorial revisions |
| R2-L0952 | P1 | PARTIAL | 004 — Tutorial-practice relationships |
| R2-L0954 | P1 | PARTIAL | 005 — Tutorial prerequisites |
| R2-L0956 | P1 | PARTIAL | 006 — Learning progress |
| R2-L0958 | P1 | PARTIAL | 007 — Necessary indexes |
| R2-L0960 | P1 | PARTIAL | 008 — RLS policies |
| R2-L0962 | P1 | PARTIAL | Энэ жагсаалт жишээ бөгөөд одоогийн schema-г шалгаж шийд. |
| R2-L0964 | P1 | PARTIAL | Олон зуун tutorial болон problem record-ийг нэг асар урт SQL INSERT болгон оруулахгүй. |
| R2-L0966 | P1 | PARTIAL | Batch import script ашигла. |
| R2-L0968 | P1 | PARTIAL | Supabase Storage ашиглавал bucket policy болон upload authorization-г зөв тохируул. |
| R2-L0970 | P1 | PARTIAL | Frontend-д service-role key оруулахгүй. |
| R2-L0976 | P1 | PARTIAL | Tutorial-ийн тоо өсөхөөр контентыг удирдах систем илүү чухал болно. |
| R2-L0978 | P1 | PARTIAL | Админд дараах хэрэгслүүдийг нэмж өг: |
| R2-L0982 | P2 | PARTIAL | - Search tutorials |
| R2-L0983 | P2 | PARTIAL | - Filter by level |
| R2-L0984 | P2 | PARTIAL | - Filter by category |
| R2-L0985 | P2 | PARTIAL | - Draft/published status |
| R2-L0986 | P2 | PARTIAL | - Missing content warning |
| R2-L0987 | P2 | PARTIAL | - Missing practice problems |
| R2-L0988 | P2 | PARTIAL | - Missing prerequisites |
| R2-L0989 | P2 | PARTIAL | - Missing English translation |
| R2-L0990 | P2 | PARTIAL | - Last edited date |
| R2-L0994 | P8 | PARTIAL | - Стандарт хангаагүй tutorials |
| R2-L0995 | P8 | PARTIAL | - Practice problem-гүй tutorials |
| R2-L0996 | P8 | PARTIAL | - Priority problem-гүй tutorials |
| R2-L0997 | P8 | PARTIAL | - Broken tutorial links |
| R2-L0998 | P8 | PARTIAL | - Broken source links |
| R2-L0999 | P8 | PARTIAL | - Duplicate problems |
| R2-L1000 | P8 | PARTIAL | - Missing difficulty metadata |
| R2-L1001 | P8 | PARTIAL | - Missing tutorial variations |
| R2-L1002 | P8 | PARTIAL | - Unused images |
| R2-L1006 | P1 | PARTIAL | Аюулгүй batch import/update боломжтой болго. |
| R2-L1008 | P1 | PARTIAL | Гэхдээ bulk update хийснээр хуучин tutorial-ууд санамсаргүй overwrite болохгүй байх ёстой. |
| R2-L1014 | P2 | PARTIAL | Бүх tutorial-д автомат болон шаардлагатай үед content-level validation хий. |
| R2-L1016 | P2 | PARTIAL | Tutorial бүрийн хувьд дараах checklist ашигла: |
| R2-L1018 | P2 | PARTIAL | 1. Яагаад хэрэгтэй вэ? |
| R2-L1019 | P2 | PARTIAL | 2. Brute-force/naive approach |
| R2-L1020 | P2 | PARTIAL | 3. Гол ажиглалт |
| R2-L1021 | P2 | PARTIAL | 4. Алгоритмын intuition |
| R2-L1022 | P2 | PARTIAL | 5. Алхамчилсан жишээ |
| R2-L1023 | P2 | PARTIAL | 6. Зөв байдлын тайлбар |
| R2-L1024 | P2 | PARTIAL | 7. Time complexity-ийн үндэслэл |
| R2-L1025 | P2 | PARTIAL | 8. Space complexity |
| R2-L1026 | P2 | PARTIAL | 9. C++ implementation |
| R2-L1027 | P2 | PARTIAL | 10. Code walkthrough |
| R2-L1028 | P2 | PARTIAL | 11. Edge cases |
| R2-L1029 | P2 | PARTIAL | 12. Common mistakes |
| R2-L1030 | P2 | PARTIAL | 13. Related algorithms |
| R2-L1031 | P2 | PARTIAL | 14. Prerequisite links |
| R2-L1032 | P2 | PARTIAL | 15. Practice problems |
| R2-L1033 | P2 | PARTIAL | 16. Priority problems |
| R2-L1034 | P2 | PARTIAL | 17. Learning checklist |
| R2-L1035 | P2 | PARTIAL | 18. Монгол найруулгын чанар |
| R2-L1036 | P2 | PARTIAL | 19. Code correctness |
| R2-L1037 | P2 | PARTIAL | 20. Working links |
| R2-L1039 | P2 | PARTIAL | Энэ checklist-ийг зөвхөн гарчиг байгаа эсэхээр шалгаж болохгүй. |
| R2-L1041 | P2 | PARTIAL | Жишээлбэл "Proof of Correctness" гэсэн гарчиг байгаад доор нь "This algorithm is correct" гэсэн ганц өгүүлбэр байвал шаардлага хангаагүй. |
| R2-L1043 | P2 | PARTIAL | Complexity analysis ч мөн адил O(n log n) гэсэн ганц мөр биш, тайлбартай байх ёстой. |
| R2-L1045 | P2 | PARTIAL | **Дутуу tutorial-ийг чанартай болгосны дараа л COMPLETE гэж тэмдэглэ.** |
| R2-L1051 | P8 | PARTIAL | Энэ ажлыг олон үе шаттайгаар бодитоор гүйцэтгэ. |
| R2-L1055 | P8 | PARTIAL | Өмнөх prompt болон одоогийн implementation-ийг харьцуул. |
| R2-L1057 | P8 | PARTIAL | Requirement checklist үүсгэ. |
| R2-L1059 | P8 | PARTIAL | Дутуу tutorial-уудын жагсаалт гарга. |
| R2-L1063 | P0 | PARTIAL | Rich-text editor, image upload, content blocks, preview, draft, autosave, revisions болон admin controls-ийг хэрэгжүүл. |
| R2-L1065 | P0 | PARTIAL | Editor-ийн compatibility-г хуучин tutorial-уудтай шалга. |
| R2-L1069 | P8 | PARTIAL | Одоо байгаа бүх tutorial-ийг чанарын стандартаар шалгаж, хангалтгүйг дахин бич. |
| R2-L1071 | P8 | PARTIAL | Эхлээд чухал суурь сэдвүүдийг чанартай болго. |
| R2-L1075 | P8 | PARTIAL | Өмнөх prompt болон энэ prompt-ийн сэдвүүдийг бүрэн хамарсан tutorial library бий болго. |
| R2-L1077 | P8 | PARTIAL | Сэдэв бүрийг canonical ID болон prerequisite relationship-тай болго. |
| R2-L1081 | P4 | PARTIAL | Tutorial бүрийн бодлогыг судалж сонго. |
| R2-L1083 | P4 | PARTIAL | Priority problems-ийг зөв тодорхойл. |
| R2-L1085 | P4 | PARTIAL | Дутуу бодлогуудыг баталгаажсан эх сурвалжаас нэм. |
| R2-L1089 | P8 | PARTIAL | Problems page-ийн layout, filtering, rating badges, problem rows, detail views болон responsive design-ийг сайжруул. |
| R2-L1093 | P8 | PARTIAL | 100-day plan, Profile, stats, progress, light theme болон өмнөх prompt-ийн бусад шаардлагыг audit-д үндэслэн гүйцээ. |
| R2-L1097 | P8 | PARTIAL | Database migrations, auth, admin permissions, editor uploads, tutorial rendering, problem links, progress, responsive layout болон GitHub Pages-ийг шалга. |
| R2-L1103 | P8 | PARTIAL | Ажлын төгсгөлд дараах тайланг гарга. |
| R2-L1107 | P2 | PARTIAL | - Нийт tutorial-ийн тоо |
| R2-L1108 | P2 | PARTIAL | - Өмнө байсан tutorial-ийн тоо |
| R2-L1109 | P2 | PARTIAL | - Шинээр нэмэгдсэн tutorial-ийн тоо |
| R2-L1110 | P2 | PARTIAL | - Бүрэн дахин бичсэн tutorial-ийн тоо |
| R2-L1111 | P2 | PARTIAL | - Quality checklist хангасан tutorial-ийн тоо |
| R2-L1112 | P2 | PARTIAL | - Дутуу үлдсэн tutorial-ийн тоо |
| R2-L1113 | P2 | PARTIAL | - Prerequisite холбоостой tutorial-ийн тоо |
| R2-L1114 | P2 | PARTIAL | - Practice problems-той tutorial-ийн тоо |
| R2-L1115 | P2 | PARTIAL | - Priority problems-той tutorial-ийн тоо |
| R2-L1119 | P0 | PARTIAL | - Image upload ажиллаж байгаа эсэх |
| R2-L1120 | P0 | PARTIAL | - Rich-text formatting ажиллаж байгаа эсэх |
| R2-L1121 | P0 | PARTIAL | - Code blocks ажиллаж байгаа эсэх |
| R2-L1122 | P0 | PARTIAL | - Math rendering ажиллаж байгаа эсэх |
| R2-L1123 | P0 | PARTIAL | - Draft/publish ажиллаж байгаа эсэх |
| R2-L1124 | P0 | PARTIAL | - Preview ажиллаж байгаа эсэх |
| R2-L1125 | P0 | PARTIAL | - Autosave ажиллаж байгаа эсэх |
| R2-L1126 | P0 | PARTIAL | - Admin permissions зөв эсэх |
| R2-L1130 | P8 | PARTIAL | - Нийт бодлогын тоо |
| R2-L1131 | P8 | PARTIAL | - Шинээр нэмэгдсэн бодлогын тоо |
| R2-L1132 | P8 | PARTIAL | - Duplicate detection |
| R2-L1133 | P8 | PARTIAL | - Difficulty metadata coverage |
| R2-L1134 | P8 | PARTIAL | - Tutorial relationships |
| R2-L1135 | P8 | PARTIAL | - Priority problem coverage |
| R2-L1139 | P5 | PARTIAL | - 100 өдөр бүрэн байгаа эсэх |
| R2-L1140 | P5 | PARTIAL | - Tutorial relationships |
| R2-L1141 | P5 | PARTIAL | - Problem relationships |
| R2-L1142 | P5 | PARTIAL | - Progress tracking |
| R2-L1143 | P5 | PARTIAL | - Missing assignments |
| R2-L1147 | P8 | PARTIAL | - GitHub repository-д өөрчлөлт хадгалагдсан эсэх |
| R2-L1148 | P8 | PARTIAL | - Production сайт дээр шинэчлэгдсэн эсэх |
| R2-L1149 | P8 | PARTIAL | - Supabase migrations хэрэгжсэн эсэх |
| R2-L1150 | P8 | PARTIAL | - Browser tests |
| R2-L1151 | P8 | PARTIAL | - Mobile tests |
| R2-L1152 | P8 | PARTIAL | - Known issues |
| R2-L1154 | P8 | PARTIAL | **Нотолгоогүйгээр "бүх зүйл бүрэн боллоо" гэж хэлж болохгүй.** |
| R2-L1156 | P8 | PARTIAL | Хэрэв аль нэг хэсгийг дуусгаж чадаагүй бол яг аль requirement дутуу, яагаад дутуу, юуг хийснээ тодорхой тайлагна. |
| R2-L1164 | P2 | PARTIAL | Гэхдээ чанарыг шалтаг болгож өмнө шаардсан олон сэдвийг орхиж болохгүй. |
| R2-L1166 | P2 | PARTIAL | **Зорилго бол өргөн сэдвийн хамрах хүрээ + өндөр чанартай сургалтын агуулга.** |
| R2-L1170 | P2 | PARTIAL | Бүх tutorial нэг ижил ерөнхий өгүүлбэртэй байж болохгүй. |
| R2-L1172 | P2 | PARTIAL | Алгоритм бүрийн онцлог, reasoning, proof, implementation, common mistakes ялгаатай байх ёстой. |
| R2-L1176 | P8 | PARTIAL | Таг таарсан бүх бодлогыг Priority гэж тэмдэглэж болохгүй. |
| R2-L1180 | P8 | PARTIAL | Tutorial дахин бичихдээ өмнөх ID, хэрэглэгчийн progress, холбоосуудыг эвдэхгүй. |
| R2-L1184 | P0 | PARTIAL | Админ контентоо хүссэнээрээ зохион байгуулж болох ч сайт аюулгүй, хурдан, responsive хэвээр байна. |
| R2-L1188 | P7 | PARTIAL | Одоогийн dark theme-ийн дизайныг эвдэхгүй. |
| R2-L1192 | P8 | PARTIAL | Зөвхөн audit report эсвэл төлөвлөгөө гаргаад зогсож болохгүй. |
| R2-L1194 | P8 | PARTIAL | Боломжтой ажлуудыг шууд хэрэгжүүл. |
| R2-L1196 | P8 | PARTIAL | Хэт том ажил бол хэсэгчлэн хийсэн ажлаа бодитоор commit хийж, үлдсэн шаардлагуудыг тодорхой backlog-д хадгал. |
| R2-L1200 | P8 | PARTIAL | Work session тасарсан эсвэл шинэ session эхэлсэн ч үргэлжлүүлэх боломжтой байхаар: |
| R2-L1202 | P8 | PARTIAL | - Requirement checklist |
| R2-L1203 | P8 | PARTIAL | - Content inventory |
| R2-L1204 | P8 | PARTIAL | - Completed migrations |
| R2-L1205 | P8 | PARTIAL | - Pending tasks |
| R2-L1206 | P8 | PARTIAL | - Test results |
| R2-L1207 | P8 | PARTIAL | - Deployment status |
| R2-L1209 | P8 | PARTIAL | зэргийг repository дотор хадгал. |
| R2-L1211 | P8 | PARTIAL | Нэгэнт хийсэн ажлыг шаардлагагүйгээр дахин бүү хий. |
| R2-L1217 | P8 | PARTIAL | Erdene Club нь: |
| R2-L1219 | P8 | PARTIAL | - Олон сэдвийг бүрэн хамарсан алгоритмын номын сантай |
| R2-L1220 | P8 | PARTIAL | - Алгоритм бүрийг ойлгомжтой, дэлгэрэнгүй тайлбарладаг |
| R2-L1221 | P8 | PARTIAL | - Яагаад хэрэгтэй, яагаад зөв, яагаад хурдан ажилладгийг ойлгуулдаг |
| R2-L1222 | P8 | PARTIAL | - C++ implementation-ийг алхам бүрээр заадаг |
| R2-L1223 | P8 | PARTIAL | - Related algorithms болон variations-тай |
| R2-L1224 | P8 | PARTIAL | - Tutorial бүртээ чанартай Priority бодлоготой |
| R2-L1225 | P8 | PARTIAL | - Хэрэглэгчийн суралцах progress-ийг хадгалдаг |
| R2-L1226 | P8 | PARTIAL | - 100 хоногийн олимпиадын төлөвлөгөөтэй |
| R2-L1227 | P8 | PARTIAL | - Хүчирхэг, зураг оруулдаг tutorial editor-той |
| R2-L1228 | P8 | PARTIAL | - Том, чанартай бодлогын сантай |
| R2-L1229 | P8 | PARTIAL | - Орчин үеийн Problems интерфэйстэй |
| R2-L1230 | P8 | PARTIAL | - Хэрэглэгчийн статистик болон ахицыг харуулдаг |
| R2-L1231 | P8 | PARTIAL | - Монгол хэл дээр жинхэнэ сурах бичгийн чанартай контенттой |
| R2-L1233 | P8 | PARTIAL | платформ болсон байх ёстой. |
| R2-L1235 | P8 | PARTIAL | USACO Guide-ийн сургалтын аргачлалыг жишиг болгон ашигла, гэхдээ Erdene Club-ийн өөрийн өвөрмөц онцлог, дизайн болон аудиторио хадгал. |
| R2-L1237 | P8 | PARTIAL | **Чиний гол зорилго: өмнөх prompt-д заасан боловч хэрэгжээгүй бүх шаардлагыг илрүүлж, чанартайгаар дуусгах.** |
| R2-L1239 | P8 | PARTIAL | Одоо байгаа Work conversation болон өмнөх implementation-аа ашиглаад шууд аудит, засвар, хөгжүүлэлтийн ажлаа эхлүүл. |
