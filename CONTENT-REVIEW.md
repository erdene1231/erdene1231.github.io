# Сургалтын агуулгын хүрээ, чанарын хяналт

2026-10-25. Энэ тайлан нь хэрэгжсэн контент ба дараагийн editorial ажлыг ялгана. Нийтлээгүй сэдвийг бэлэн tutorial гэж тоолоогүй. Анхны master prompt-ийн rating зохиохгүй гэсэн заалтыг хэрэглэгчийн дараагийн “бүх бодлогод CF rating” хүсэлтийн дагуу **тэмдэглэгээтэй author estimate** байдлаар хэрэгжүүлсэн; CF official утга хэвээр.

## Tutorial

Нийт 55 бүрэн MN/EN body: beginner 23, intermediate 26, advanced 6. Өмнөх серверийн 43 body-г суурь болгосон; админы өөрчлөлтүүдийг хадгалсан.

| Хүрээ | Бодит өөрчлөлт |
|---|---|
| Binary Search | Sorted order-оос хайлтын талыг хасах санаа; invariant ба зөв байдал; worst-case halving; initialization/loop/termination; overflow/bounds; full C++17, sample I/O, lower/upper/on-answer variants, practice, алхамчилсан demo. |
| Greedy | Шийдвэрээ локалаар сонгох боломжийг interval scheduling дээр гаргаж авах; exchange argument; буруу greedy-д counterexample; sort/scan-ийн cost; endpoint convention; full C++17, sample I/O, practice, demo. |
| Dynamic Programming | Brute force-ийн давтагдах state-оос DP гаргах; state/base/transition/order; induction; state × transition cost ба memory; ordered/unordered counting ялгаа; full C++17, sample I/O, variants, practice, demo. |
| 12 шинэ хичээл | Lower bound, Upper bound, Sliding window, Connected components, Bipartite graphs, Interval DP, Tree DP, Bellman–Ford, String hashing, Invariant, Debugging/stress testing, Subtask strategy. Нэг бүрд бодит жишээ, derivation, proof, үндэслэлтэй time/space, implementation хэсгүүд, full C++17/I/O, common mistakes, бодох асуулт/hint/answer бий. |
| Үлдсэн 40 body | Өмнөх дэлгэрэнгүй контент хадгалагдсан. Шинэ shared reader, variants/next, prerequisite order, practice, self-check, bookmark/plan/profile холбоосуудыг ашиглана. Бүгдийг энэ удаад эхнээс нь дахин бичсэн гэж тооцоогүй. |

Анхаарсан нарийн зүйлс:

- Tree DP-ийн reference нь урт chain дээр stack overflow өгөхгүй parent/order + reverse order боловсруулалттай; 200,000 оройтой path-ийг шалгасан. Segment tree-ийн үндсэн хичээл өмнөх recursive хувилбар хэвээр.
- Bellman–Ford нь in-place relaxation-ийн зөв invariant, reachable/unreachable negative cycle, INF guard болон long long-ийн нөхцөлийг тайлбарлана.
- String hashing нь магадлалтай арга. Double hash ч collision-ийг бүрэн арилгадаг гэж тайлбарлаагүй; adversarial оролтын талаар анхааруулсан.
- Debugging жишээ өөрөө input үүсгэнэ. Хоосон Input блок харуулахгүй, seeded stress test ашиглана; `assert` шаардлагагүй.
- Subtask strategy жишээ нь өөрийн сургалтын subset-sum загвар. Бодит IOI-ийн task/онооны схем болгож зохиогоогүй. Partial шийдлээ full solved гэж тэмдэглэхгүйг тайлбарласан.
- Reference code-ууд нийтлэг нэр, 4-space indentation, `long long`, хилийн шалгалттай. MN/EN дахь full program нэг эхтэй, compile/sample тест давсан.
- `read` нь уншсан тухай сурагчийн тэмдэглэгээ; `mastered` нь 5 self-check + тухайн сэдвийн priority practice solved үед тооцогдоно. Энэ нь judge-аар шалгасан сертификат биш.

## Practice ба relationship

`curriculum.json` дотор 55 lesson relationship байна. Нийт 146 unique бодлого curated practice-д орсон; тэдгээрийн 129-д primary topic-ийг тусгайлан тэмдэглэсэн. Нэг бодлого хэд хэдэн сэдвийн secondary practice байж болно. Primary topic нь бүх 702 бодлогод бүрэн хийгдсэн гэж тайлагнаагүй.

Ихэнх сэдэв 3–7 бодлоготой. Bellman–Ford, Floyd–Warshall, sparse table, bipartite зэрэгт одоогийн баталгаажсан сангаас шууд тохирох бодлого цөөн тул тоо дүүргэхээр холбоогүй бодлого нэмээгүй. Албан source/ref ба canonical URL-аар нэг бодлогын өөр progress хуулбар үүсэхээс сэргийлсэн. Priority rationale нь editor relationship JSON-д хадгалагдаж, admin-д харагдана.

Сонголтын жишээ: Factory Machines/Array Division → monotone feasibility, Movie Festival → exchange argument, Shortest Routes II → all-pairs shortest path, Cycle Finding → reachable/cycle reasoning, Polynomial Queries → lazy updates, Edit Distance → state/transition. Илүү ахисан даалгаврыг тухайн суурь алгоритмын шууд стандарт жишээ гэж андуурахгүйгээр challenge болгон ялгасан.

## Бодлогын metadata ба rating

Нийт 702: өмнөх 297 + шинэ 405. CSES-ийн 400 task-ийн official нэр/ID/URL нь official problemset index-ээс; AtCoder DP-ийн 26 task official task list-ээс.

- CF 267-ийн албан rating хадгалагдсан.
- Бусад 435 rating нь estimate. `≈` тэмдэглэгээ, rating basis/confidence/estimated date боломжтой үед хадгалагдана.
- Шинэ 405-аас 168 нь нэг бүрчлэн author estimate; 237 нь source category-ийн ерөнхий түвшнээс авсан `rough` estimate. Эдгээрийг нарийн хэмжсэн бодит Codeforces rating гэж үзэхгүй. Admin чанарын хэсэгт тусад нь жагсаана.
- Source category нь баталгаатай; category-аас бүх шийдлийн tags-ийг тааж олноор нэмээгүй. Curated practice-ийн хянасан холбоосуудын tags-ийг илүү тодруулсан.
- Шинэ олон зуун бодлогод баталгаагүй 3 hint зохиогоогүй; hint array хоосон. Өмнөх 3-level MN/EN hint, hide/show, private note систем хэвээр ажиллана.
- Дэлгэрэнгүй хяналт дуусаагүй эсвэл тохирох published prerequisite байхгүй task-ийг сангаас нээж болох ч бүх tutorial-д хүчээр холбоогүй. JOI/APIO/CEOI/COCI/Baltic/Balkan/USACO-оос шинэ task-ууд нэмэгдсэн гэж тооцоогүй; selection backlog нь `pending-imports.json`.

## 100 хоног

Өдөр бүр тусгай зорилго/ажиглалттай, prerequisite-д суурилсан 10 phase. 68 өдөр 3-аас олон/тэнцүү required бодлоготой, challenge-тай нийлүүлбэл 94 өдөр 3-аас олон/тэнцүү бодлоготой. Хүнд day-д 1–2 required байж болно. Review, debugging, editorial analysis, mock/virtual, subtask өдрүүд орсон. Review-гийн давталт зориудын spaced repetition; өөр өөр progress record үүсгэхгүй.

Өдрийн ачааллын минут нь баримжаа; 100 календарь өдрийн дотор ахисан түвшин баталгаатай эзэмшинэ гэсэн амлалт биш. Өмнөх required бодлого solved бол ахиц давхар дахин бодохыг шаардахгүй; self-check/checklist-ээр эргэн бататгана. IOI challenge-ийн full solution бэлэн биш үед хувийн note-д хүрсэн subtask/хязгаараа тэмдэглэнэ.

## Нийтлээгүй tutorial backlog

30 сэдэв `not_published` төлөвтэй, reader-д эвдэрсэн link/хоосон хуудас болж харагдахгүй. Үүнд standalone STL/arrays-strings/constructive, sweep line, rerooting/digit/profile/SOS/optimized DP, CHT/Li Chao, persistent tree/HLD/centroid/small-to-large, Mo/offline/parallel BS, SCC/bridges/flow/matching, Z/trie/Aho/suffix structures, matrix power/geometry орно.

Дараагийн editorial ажил нь дараах дарааллаар хийхэд зохистой:

1. Одоогийн 1300–1400 сурагчдын бодолтоор practice progression ба rough rating-уудыг нэг бүрчлэн хянах.
2. Sweep line, digit DP, rerooting, SCC, matching зэрэг ашигтай prerequisite сэдвүүдийг бодит бүтэн хичээл болгох.
3. JOI/APIO/CEOI/COCI/BOI/Balkan/USACO-гийн statement/editorial-ийг уншиж primary/secondary topic, subtask strategy-тай curated selection нэмэх.
4. Сурагч/багшийн хэрэглээгээр үлдсэн 40 хичээлийн найруулга болон implementation breakdown-ийг нягтлах.

## Ашигласан эх сурвалж

Эх сурвалжийн бүтэн өгүүлбэрүүдийг контент болгон хуулбарлаагүй. Tutorial-ийн тайлбар, жишээ, код нь өөрийн сургалтын найруулгатай.

- [CSES Problem Set](https://cses.fi/problemset/)
- [AtCoder Educational DP — official tasks](https://atcoder.jp/contests/dp/tasks?lang=en)
- [USACO Guide — Binary Search](https://usaco.guide/silver/binary-search)
- [USACO Guide — Greedy](https://usaco.guide/silver/greedy-sorting)
- [USACO Guide — Dynamic Programming](https://usaco.guide/gold/intro-dp)

Олон улсын дараагийн selection-ийн official archive-уудыг `pending-imports.json` дотор тусад нь хадгалсан. Archive URL шалгасан нь тухайн archive-ийн бүх бодлого, editorial, rating-ийг шалгасан гэсэн үг биш.
