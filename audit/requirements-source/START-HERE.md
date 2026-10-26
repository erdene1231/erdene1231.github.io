# Erdene Club — Codex-д шилжүүлэх үндсэн даалгавар

Огноо: 2026-10-26. Энэ файлыг эхнээс нь уншаад хавсаргасан хоёр шаардлагыг БҮТНЭЭР унш. Зөвхөн төлөвлөгөө гаргалгүй, дутуу ажлуудыг дарааллаар нь бодитоор гүйцээ. Энэ бол шинэ сайт бүтээх ажил биш; одоо ажиллаж байгаа төслийг үргэлжлүүлэх ажил.

## 1. Зорилго, эх сурвалж, эрх

- Сайт: https://erdeneclub.com/
- Одоогийн repository: erdene1231/erdene1231.github.io. think-cp гэдэг нь хуучин нэр; одоогийн repository-г шалга.
- CMS: https://judge.erdeneclub.com/ — тусдаа account системтэй. Зөвхөн root URL руу new-tab холбоос; SSO болон judge/server integration энэ ажилд орохгүй.
- GitHub Pages static frontend + Supabase архитектурыг хадгал. Одоо байгаа framework, routing, component, styling conventions-ийг дага.
- Зорилтот сурагч CF 1300–1400; анхан шатнаас IOI/EGOI түвшин хүрэх чанартай Монгол сургалтын сан. USACO Guide-ийг судалж жишиг болгох боловч Erdene Club-ийн өөрийн төрхийг хадгал.
- Хэрэглэгч шаардлагатай кодын өөрчлөлт болон Supabase migration/content update-ийг шууд хэрэгжүүлэх эрх өгсөн. Routine үйлдэл болгонд дахин зөвшөөрөл асуухгүй. Ажлын хүрээнээс гадуурх өгөгдөл устгах, database reset, account/progress алдагдуулах үйлдэл хийхгүй.
- Git commit, remote push/PR, production deploy гурвыг ялга. Frontend deploy хийх эрх/ажлын урсгал тодорхойгүй бол deploy-ready өөрчлөлт, тест, diff-ээ бүрэн бэлдээд зөвхөн тэр үлдсэн шийдвэрийг тодруул. Environment Publish нь website deploy биш.

Эрэмбэ: хэрэглэгчийн энэ хамгийн сүүлийн даалгавар болон дараах нэмэлтүүд → requirements-02.txt → requirements-01.txt → хуучин audit. Хуучин prompt-д 'чи төслийг аль хэдийн мэддэг' гэж бичсэн ч бодит кодыг уншихгүйгээр мэддэг мэт бүү ханд. Хавсралтын хуучин Work mode, гараар SQL ажиллуулах тухай зааврыг одоогийн Codex Cloud + шууд хэрэгжүүлэх эрхтэй нийцүүл. Жижиг SQL file, verification, backup шаардлага хэвээр.

## 2. Одоогийн нотолгоотой төлөв

Хэрэглэгчийн Codex setup task-аас дамжуулсан live үр дүн:
- initialize HTTP 200, initialized notification HTTP 202, SELECT 1 PASS.
- public.problem_catalog: 748 мөр; public.tutorial_catalog: 55 мөр.
- Migration history: [] (хоосон). Энэ нь өмнөх SQL өөрчлөлтүүд хийгдээгүй гэсэн үг БИШ. SQL Editor-оор хийгдсэн schema-г inspect хий; хуучин migration-уудыг сохроор replay хийхгүй.
- public хүснэгтүүд: admin_accounts, admin_grants, following, friendships, learning_records, problem_catalog, problem_changes, problem_sources, profiles, progress, study_group_members, study_groups, study_report_history, study_reports, study_teacher_note_history, study_teacher_notes, tutorial_catalog, tutorial_changes.
- apply_migration хэрэгсэл tools/list-д байгаа; write ажиллагааг одоогоор туршаагүй. Бичих шалгалтыг анхны шаардлагатай, review/test хийсэн migration-аар баталгаажуул; зөвхөн шалгахын тулд дурын production мөр үүсгэхгүй.

Cloud тохиргоо:
- Network secret SUPABASE_WRITE_TOKEN; зөвхөн mcp.supabase.com домэйнд дамжуулна.
- Environment variable SUPABASE_PROJECT_REF.
- Endpoint: https://mcp.supabase.com/mcp?project_ref=<SUPABASE_PROJECT_REF>&features=database
- User-Agent: ErdeneClub-Codex/1.0. Default Python urllib client өмнө Cloudflare 1010 авч байсан; энэ header-тай PASS болсон.
- initialize response-ийн Mcp-Session-Id-г санах ойд хадгалж, initialized болон дараагийн бүх хүсэлтэд дамжуул. Process бүр шинээр initialize хийнэ. Тохиролцсон protocol-оо ашигла.
- Setup task дахь /workspace/shared/supabase_mcp.py болон /workspace/shared/start/SKILL.md-ийг шалга. Хэрэглэгчийн тайлангаар файл хадгалагдсан ч Start skill талбарт бүртгэгдээгүй. Шинэ task-д эдгээр path заавал байна гэж бүү таамагла. Байвал ашигла; үгүй бол secret-ийн утгыг асуухгүйгээр тохиргоонд тулгуурлан сэргээ.
- Token, session ID, password, service-role key-г chat/log/Git/frontend/ZIP-д оруулахгүй. Secret placeholder-ийг зөвхөн зөвшөөрсөн домэйнд ашигла.
- features=database нь Storage tool автоматаар өгдөггүй. Production image upload шалгалтад одоогийн app-ийн authorized admin flow эсвэл шаардлагатай supported access-ийг хэрэглэ; хэрэгслийн хүрээг таамаглахгүй.

Хавсаргасан erdene-club-step-001-recovery.zip нь өмнөх ажлын recovery snapshot; production release биш.
- Git HEAD: e59b68865258955e1c12d75e75708fb9e6fc7e66.
- SHA256: f615dc21b6c0ca40e78ebf4b745b7244a88757062f36bae2610e941257583914.
- site/ эх файлууд, repository.bundle, MANIFEST.json, README-MN.txt агуулна.
- Өмнөх орчинд remote тохируулаагүй, GitHub write 403 байсан. Энэ Codex орчинд эрхийг дахин шалга; хуучин 403-г одоо ч хүчинтэй гэж бүү үз.
- Snapshot-ийг тусдаа хавтас/branch-д задлаад одоогийн GitHub код, live DB-тэй diff хийж нэгтгэ. main-ийг snapshot-оор бүхэлд нь дарж солихгүй; snapshot-ийн .git/config эсвэл тохиргоог одоогийн repo дээр сохроор хуулж болохгүй.
- Snapshot local catalog 749 байж болно: BOI17 Toll-ийн pending-boi17-toll түр ID орсон. Live 748. Үүнийг бодит server ID-гаар reconcile хийхээс өмнө deploy/import-complete гэж тэмдэглэхгүй; 749 дугаарыг production-д таамгаар оноохгүй.

Локал snapshot-д хадгалагдсан ажлын нотолгоо:
- Typed rich editor, draft/autosave/history, image policy, preview, safe backup/import, quality dashboard-ийн код болон isolated тестүүд бий. Бүгд live production дээр батлагдсан гэж үзэхгүй.
- Tree Basics, LCA, Sparse Table: authored MN semantic review бүртгэлтэй 3 tutorial.
- Binary Search, Greedy: шинэ authored эх болон asset хадгалагдсан, C++ differential тест PASS; semantic review болон шинэ desktop/mobile review дутуу. Эдгээрийг дээрх 3 дээр нэмж COMPLETE тооцохгүй.
- Өмнө '41/55 review давсан' гэж ярьсан тоог батлах эх/commit олдоогүй. Тэр тоог энэ ажлын baseline болгон ХЭРЭГЛЭХГҮЙ. 55 нь live row count болохоос чанарын баталгаа биш.
- 31 model test, editor 021–026 зургаан migration + 5 authored draft/publish round-trip isolated DB дээр PASS байсан. Binary Search 224027 query; Greedy 1600 scheduling + 1600 subset-sum oracle case, large input/UBSan PASS. Эдгээр нь түүхэн snapshot-ийн тестийн баримт; одоогийн өөрчлөлтийн үр дүнг тусад нь шалга.
- edition fingerprint build fix нь хуучин baseHashes-г хадгалдаг; admin custom body-г автоматаар overwrite хийхээс хамгаалсан.
- audit/REQUIREMENTS.md-ийн эхний хүснэгт хуучирсан: appended updates, audit/CHECKPOINT-2026-10-26.md, audit/EDITOR-BATCH-QUALITY-VERIFICATION.md, audit/tutorial-reviews/ болон бодит кодыг хамт унш.

## 3. Эхлэх ажил: нэгтгэл ба шаардлагын мөр бүрийн бүртгэл

1. AGENTS.md, README, schema/migrations, auth/RLS, data models, renderer/editor, tests, deployment workflow-г унш.
2. GitHub checkout, recovery snapshot, live DB гэсэн 3 эхийг тусад нь inventory хийж нийцүүл. Хэрэглэгчийн саяхан admin editor-оор хийсэн засварыг revision/hash-тай шалгаж хадгал.
3. requirements-01.txt ба requirements-02.txt-ийн БҮХ шаардлагыг stable requirement ID-тай хүснэгт болго. Төлөв: VERIFIED_COMPLETE / PARTIAL / MISSING / BROKEN / BLOCKED / OPTIONAL_DEFERRED. Local implemented, locally tested, live verified, deployed гэдгийг тус тусад нь бич.
4. Бүх topic label-ийг canonical tutorial ID болон хэрэгтэй бол section anchor-тай холбо. Snapshot-ийн 235 required label гэдэг нь 235 тусдаа tutorial гэсэн үг биш. Duplicate/alias нэгтгэж болно, шалтгаан ба яг хаана бүрэн заасныг бүртгэ. Сэдвийг чимээгүй хасахгүй. Topic нэр дурдсан төдийд covered гэж тооцохгүй.
5. Audit-аа дуусмагц бодит хэрэгжилтэд ор. Зөвхөн report бичээд зогсохгүй.

## 4. Хийх дараалал — өмнөх ажлыг дуусгалгүй шинэ нэмэлт рүү үсрэхгүй

A. Snapshot-ийг current repo-той аюулгүй нэгтгэх, live schema reconciliation, ажилласан client/start зааврыг хадгалах.
B. Tutorial engine/editor-ийн үлдсэн compatibility, security, production Storage болон publishing шалгалтыг дуусгах.
C. Binary Search, Greedy-ийн дутуу review-г дуусгаад одоо байгаа бүх 55 tutorial-ийг нэг бүрчлэн хянаж, шаардлага хангахгүйг бүтнээр дахин найруулах.
D. Хоёр хавсралтын бүх canonical сэдвийн дутуу tutorial-уудыг prerequisite дарааллаар нэмж, practice matching-ийг tutorial бүртэй хамт дуусгах.
E. Өмнөх олон улсын curated problem selection, existing ratings/hints audit, problems UI, 100-day plan, profile/statistics, light theme, login/signup болон regression ажлыг дуусгах.
F. Үүний дараа хамгийн сүүлд нэмсэн rating өнгө, нэмэлт problem quota, дөрвөн priority түвшинг хэрэгжүүлэх.
G. End-to-end verification, release/deployment status, үлдсэн асуудлын үнэн зөв эцсийн тайлан.

Нэг чанартай tutorial дуусгахын тулд practice problem импортлох нь тухайн ажлын dependency; шинэ quota ажлыг түрүүлж хийсэн гэж тооцохгүй. Блоклогдсон хэсгийг тодорхой баримттай тэмдэглээд боломжтой хуучин ажлаа үргэлжлүүл, шинэ feature рүү чимээгүй алгасахгүй.

## 5. Tutorial бүрийн чанарын заавал хангах стандарт

Дараах 15 хэсэг агуулгын хувьд бүрэн байна:
1. Яагаад хэрэгтэй вэ — сурагчид тулгарах асуудал.
2. Энгийн/brute-force шийдэл ба сул тал.
3. Гол observation-ийг алхам алхмаар гаргах.
4. Үндсэн intuition, algorithm, invariant.
5. Жижиг бодит жишээний алхам бүрийн trace.
6. Correctness proof: тохирох invariant/induction/contradiction/exchange argument.
7. Time болон space complexity-ийн үйлдлийн тоонд суурилсан математик, intuitive үндэслэл; worst-case, хэрэгтэй үед amortized; constraint ба хязгаар.
8. C++17 implementation: data structures, initialization, main logic, updates/transitions, result, complete code. Хэсэг бүрийн учрыг тайлбарла.
9. Edge cases.
10. Common mistakes болон counterexamples.
11. Variations, prerequisite, related/next tutorials — canonical ID холбоос.
12. Хэзээ хэрэглэх, хэзээ тохирохгүй, observation/problem-solving thinking.
13. Warm-up → Standard → Observation → Application → Challenge → Olympiad extension practice progression.
14. ⭐ Priority problems, editor-д харагдах сонголтын үндэслэл.
15. Дүгнэлт, сурагчийн checklist; reading ≠ mastery.

Монгол найруулга нь машин орчуулга шиг биш, textbook шиг ойлгомжтой байна. binary search, grid, dp, array зэрэг дассан technical үгийг англиар хадгал. EN хувилбар байвал ижил чанартай, MN-тэй бүтцийн зөрүүг шалга; хоосон/чанаргүй орчуулгыг published болгохгүй. Англи хувилбар дутууг ил тод тэмдэглэ.

MathJax: inline $...$, display $$...$$; хувьсагч, массивын муж a[i..j], томьёо, complexity бүгд зөв math notation-тай. Code block доторх кодыг MathJax болгохгүй. Literal $ болон escaping, preview/static/dynamic rendering-г шалга.

C++ reference code БҮГД: beginner friendly, сайн spacing/indentation, түгээмэл ойлгомжтой нэр, unnecessary assert болон compressed macro-heavy style-гүй. Суурь Segment Tree-г recursive байдлаар заа; iterative хувилбарыг дараагийн variation болгон тайлбарлаж болно. Copy button, C++ syntax colors, horizontal overflow зөв.

Segment Tree, Dijkstra, Tree DP, Digit DP, Network Flow зэрэг том сэдэвт олон жишээ, кодын олон хэсэг, гүн proof шаардлагатай. Бүх tutorial-ийг ижил template/уртаар дүүргэхгүй. Гарчиг, paragraph count эсвэл code compile-ийг semantic review гэж үзэхгүй.

Tutorial бүрд хавсралтын 20-item quality checklist-ийн бодит evidence, reviewed body/relationship hash, review date, code tests, source links, үлдсэн зүйлсийг хадгал. Агуулга өөрчлөгдвөл хуучин review-г автоматаар хүчинтэй гэж үлдээхгүй. ID, URL, progress болон problem relationships-г хадгал.

## 6. Tutorial editor ба library

Хоёр хавсралтын editor шаардлагыг мөр бүрээр шалгаж гүйцээ:
- H1–H4, paragraph, bold/italic/underline/strike, inline code, code block, lists/checklist, quote/table/separator, external/internal/problem links, callout/warning/example/collapsible blocks.
- Add/delete/duplicate/reorder sections болон blocks; reusable educational blocks; дурын дарааллаар олон зураг, код, proof/table байрлуулах.
- Image picker/drop, боломжтой бол paste; PNG/JPEG/WebP; SVG зөвхөн safe sanitizer байгаа үед. Preview/resize/align/caption/alt/replace/delete.
- Supabase Storage, admin-only upload, actor authorization, MIME/decode/size checks, unique paths, published delivery; draft/history asset хамгаалалт болон orphan cleanup.
- Code language/indentation/highlighting/copy/scroll, math preview, safe diagrams/visualizations.
- Draft, live preview, autosave, save indicator, unsaved warning, network/offline recovery, revisions, restore-to-draft, explicit publish.
- Stale revision/hash хамгаалалт, admin custom content-ийг overwrite хийхгүй; safe import validation/dry-run, batch atomicity, backup restore.
- Tutorial CRUD, level/category/status/search, missing EN/practice/prerequisites/metadata warnings, unused images, duplicates/broken links бүхий quality dashboard.
- Searchable practice relation editor: attach/remove/order/category/priority/objective; server validation.
- Old content/new editor round trip; XSS, unauthorized user, owner A/B, revoked admin, stale update тест.
- Library level/category/search/reading status/prerequisite/recommended order; detail TOC/anchors/reading time/next links, responsive typography.

## 7. Problem bank ба hints

- Source URL + official source ID-гаар normalize/deduplicate. Site internal stable ID болон official ID хоёрыг ялга. Шинэ internal дугаарыг server-ээс дарааллаар, concurrent-safe оноо; хуучныг renumber хийхгүй.
- CSES-ийн хэрэгтэй өргөн coverage, IOI/EGOI/JOI/APIO/CEOI/COCI/BOI/Balkan OI/USACO/AtCoder/CF/OJ.uz-аас чанартай сонголт. Statement/editorial/intended solution-г судалж topic match/learning objective тогтоо.
- CF rating-ийг official эхээр шалга; бусад олимпиадын CF-equivalent rating нь ESTIMATE гэдгийг UI/metadata-д ялга. 'Бүх бодлогод CF rating' гэдэг нь албан бус эхэд official rating зохиох зөвшөөрөл биш. Estimate rationale/confidence/provenance, unknown/unrated ялгааг хадгал; rough estimate-үүдийг хяна.
- 900–2800 болон 2000+ practice хэрэгцээг ханга; илүү хүнд бодлогыг тохирох advanced шатанд оруул.
- JSON upload: нэг/олон record, schema validation, duplicate dry-run, actionable errors, batch import. Шинэ source байвал source option-д оруулах; admin гараар source нэмэх.
- Priority-г хэцүүгээс нь бус сургалтын өгөөжөөр сонго; tag таарсан бүхнийг priority болгохгүй.
- Hint 1 observation, Hint 2 algorithm, Hint 3 implementation direction. Proof/intended solution-тэй тулгаж зөв эсэхийг нэг бүрчлэн шалга; MN найруулга, technical English, EN toggle, hide/show, spoiler-гүй gradual reveal.
- Өмнө 'энэ batch-д hint хэрэггүй' гэж өгсөн 2000+/HTML import-уудыг таньж hint бүү хүчээр нэм. Одоогийн package-д эх HTML байхгүй бол тухайн хүсэлтийг BLOCKED_SOURCE гэж тодорхой тэмдэглэ; өөр бодлогоор сольж дууссан гэж хэлэхгүй.
- Practice link бүр catalog-д бодитоор байх; 'багш сан шинэчилсний дараа progress боломжтой' гэсэн dead-end үлдээхгүй. Verified missing tasks-ийг импортлоод stable ID-тай холбо.

## 8. Problems UI, theme, navigation, account

- Search, sources/tags, min/max rating, priority/status/collections; 100/problem page, filter reset, active chips, mobile filter drawer, compact/comfortable view.
- Мөрөнд title/source/official ID/rating estimate distinction/primary-secondary tags/progress/priority/tutorial; detail-д hints, notes, study-day association, source URL.
- Мянга+ record-д payload/index/query pagination/lazy content; бүх том body-г нэг дор татахгүй. Filter/sort/page state зөв, empty/error/loading state ойлгомжтой.
- Light background white/neutral, forest green accent; #FFFFFF/#F8FAFC/#E5E7EB/#111827/#64748B чиглэл, contrast-ийг шалга. Dark theme-ийн одоогийн үндсэн төрхийг хадгал.
- Login болон signup тусдаа UI, password recovery/session regression; бүх navigation section тусдаа route/page; mobile overflow болон focus/accessibility.
- Нүүр: энгийн professional дизайн, 'Бодлого ба алгоритм', Бодлогын сан/Tutorials CTA хадгал. CMS compact card/link, Tutorials-ийн хажууд CMS, root URL, target=_blank, rel=noopener noreferrer; SSO хийхгүй.
- Profile route-ийг Нүүр → Profile → Бодлогууд дарааллаар уялдуул; өмнөх navigation functionality хадгал.

## 9. 100-day plan, progress, profile/statistics

- 100 өдөр, 10 phase; бодит tutorial/problem ID, өдөр бүр objective, observations, required/priority/challenge, time estimate, checklist/completion.
- Prerequisite болон difficulty progression, review/spaced repetition/observation/debugging/editorial analysis/subtasks/virtual contest. 1300–1400 сурагчид бодитой ачаалал; бүх advanced сэдвийг 100 өдөрт шахахгүй.
- Current day/start/completed/pause/resume/bookmark/past days/incomplete tasks хадгалах; tutorial нээсэн төдийд completed/mastered болохгүй.
- Нэмэлт Advanced/IOI roadmap, шинэ canonical tutorial-уудын холбоос.
- Public/own profile: username, овог нэр, avatar, school, bio, joined date, solved/trying/saved/priority/plan progress; зөв owner/admin эрх.
- Heatmap, 7/30/365/all-time, current/longest streak; үл мэдэгдэх хуучин solve date зохиохгүй.
- Rating histogram official/estimated/unrated ялгаатай; tag donut multiple tags-ийн double counting тайлбартай; unique solved count зөв.
- Weekly phases, prev week navigation, highest/average rating, solved/attempted list, timezone boundary, duplicate solve events. Submission/AC/WA/TLE зөвхөн бодит өгөгдөлтэй үед; manual solved status-г judge verdict гэж бүү нэрлэ.
- Нэг бодлогын progress bank/tutorial/plan/profile/stats-д нэг эх сурвалжаас шинэчлэгдэх.
- Optional learning path/prerequisite graph/private journal/review queue/tutorial feedback-ийг хавсралтад зааснаар үнэл; хийсэн эсэхийг тусдаа тэмдэглэ. Optional-ийг үндсэн шаардлагын оронд хийж болохгүй.

## 10. Өмнө байсан функцуудын regression checklist

Эдгээрийг шинээр дахин зохиохгүй; ажиллаж байгааг шалгаад дутуу/эвдэрснийг зас:
- Username, immutable email workflow, email-code password recovery, avatar/name/school, leaderboard solved count, problem solvers list.
- Friends requests/acceptance, following-д дурын хүн нэмэх, request/accept үед өмнөх тохирсон auto-follow semantics.
- Админ seed account bayarjargalmunkherdene12@gmail.com; одоогийн roles/grants-г inspect, бүх хүнийг admin болгохгүй. Admin grant, problem/tutorial CRUD/hint edit/import/source management, server-side authorization.
- Private/public study groups; admin болон members хэрэглэгч нэмэх; private reports зөвхөн group access-тай хэрэглэгчдэд, өмнөх тохирсон site-admin moderation эрхтэй.
- Огноо сонгон optional solved problem list/count/difficulty/topics/notes; own log editing, group/site admin moderation.
- Teacher notes зөвхөн эрх бүхий admin өөрчилнө; report/history ownership.
- Excel export selected dates (sheet/day), weekdays, students; овог/нэр/solved/count/difficulty/topics/teacher notes. Membership, updated date, note status, school, username багануудыг хассан хэвээр.
- A4 LaTeX + PDF export, хуудас хэмнэсэн compact/multi-column layout, Mongolian fonts, урт тэмдэглэл тасрахгүй; selected dates/weekdays/students filter.
- Dark theme persistence, hint toggle, cross-browser cached old data-аас undefined гарахгүй, logout/account switching, progress retention.
- Custom SMTP асуудлыг хэрэглэгч шийдсэн. SMTP/Cloudflare/Ubuntu/CMS configuration-д энэ ажлаар хүрэхгүй.

## 11. Өмнөх ажлуудын ДАРАА хийх хамгийн сүүлийн нэмэлтүүд

### 11.1 Rating өнгө
Хэрэглэгчийн өгсөн хязгаарыг өөрийн дураар standard CF palette руу сольж болохгүй:
- 800–1100: саарал — newbie
- 1200–1300: ногоон — pupil
- 1400–1500: cyan — specialist
- 1600–1800: blue — expert
- 1900–2000: magenta — candidate master
- 2100–2300: orange — master
- 2400–2900: red — grandmaster
- 3000+: black — legendary grandmaster
Албан/estimated/unrated тэмдэглэгээг өнгөнөөс тусад нь хадгал. 100-гийн алхамтай rating-уудыг шалга; завсрын arbitrary value байвал mapping-ийг баримтжуул, өгөгдлийг өнгөнд тааруулах гэж бүү өөрчил. Dark theme дээр хар badge-д contrast background/border хэрэглэ. Color-blind хэрэглэгчид label-аар ялгах боломжтой байна.

### 11.2 Нэмэлт verified problem quota
- IOI: нэмэлт 30+
- EGOI: нэмэлт 30+
- JOI: нэмэлт 20+
- APIO: нэмэлт 15+
- Codeforces: нэмэлт 100+ чанартай recommended бодлого
Эдгээр нь existing total биш, шинээр нэмэх хүсэлт. Quota эхлэхээс өмнө baseline IDs-г freeze хийж new unique IDs болон баталгаатай provenance-оор тоол. Existing row edit/duplicate-ийг шинэ бодлого гэж тооцохгүй. Өмнөх ажлаар аль хэдийн энэ нэмэлт хүсэлтийг хангаж импортолсон нотолгоо байвал давхар импортлохгүй, тухайн баримтыг ledger-т холбо. Дур мэдэн таамгаар кредит бүү өг.

### 11.3 Tutorial болон problem importance
Low priority / Medium priority / High priority / Extreme priority сонголтууд нэм. Энэ нь сэдэв/бодлогын түгээмэл, сургалтад чухал байдлыг илэрхийлнэ; difficulty биш.
- DB validation/default/backfill, admin editor, JSON import/export, badges/filter/sort-ыг уялдуул.
- Өмнөх ⭐ Priority practice selection-тэй утгын ялгаатай. Existing boolean-ийг сохроор дөрвөн түвшин болгон хөрвүүлэхгүй, mastery recommendation-г хадгал.
- Level бүрийн editorial шалгуур ба сонголтын үндэслэлийг баримтжуул; бүхнийг Extreme болгохгүй.

## 12. Database, testing, release, тасралтгүй хадгалалт

- Live schema introspection → current repo/snapshot comparison → жижиг additive migration → isolated test → authorized apply → verify. Хоосон migration history-г шинэ empty DB гэж үзэхгүй.
- Нэг migration нэг зорилготой, dependency тодорхой, боломжтой үед transaction/idempotency. Verification query, recovery/forward-fix арга; destructive rollback-оор сурагчийн шинэ өгөгдөл устгахгүй.
- Content imports schema migration-аас тусдаа, жижиг configurable batch, dry-run/validation/dedup, expected revision/hash guard. Partial failure/retry тэсвэртэй.
- Backup/recovery боломжийг шалгаж, өөрчлөгдөх өгөгдлийн before state-г зохих private байршилд хадгал. PII бүхий database dump-ийг public Git/ZIP-д оруулахгүй.
- C++ code-ийг compile + meaningful edge/differential tests; proof/complexity/content-г semantic review. Implementation-ийг өөрийг нь хуулсан oracle бүү хэрэглэ.
- RLS owner A/B/admin/anonymous, revoked roles, SQL/RPC conflict, XSS, storage draft/public permissions, safe bulk update.
- Desktop болон mobile browser, light/dark, navigation/auth/editor/MathJax/C++/images/search/pagination/progress/exports. Байхгүй account access-тай шалгалтыг хийсэн гэж бүү тайлагна.
- Tests pass бол шаардлагагүй давтан бүтэн suite ажиллуулахгүй; өөрчлөлт, шинэ алдаа, unresolved risk-д тохируул.

Алхам бүрийн дараа:
1. Requirement ledger, content/topic inventory, migration applied ledger, test report, NEXT-STEPS.md-ээ шинэчил.
2. Git commit хийж SHA/branch-аа бич. Remote эрхтэй бол feature branch-д push; эрхгүй бол 403/blocked-г үнэнээр хэл.
3. Downloadable ZIP гарга: өөрчилсөн эх файлууд, migration SQL, frontend upload жагсаалт, apply order, verify/recovery instructions, commit SHA, manifest/checksum. Recovery ба deploy-ready release-ийг тод ялга.
4. ZIP CRC/агуулгын бүрэн байдлыг шалга, татах холбоос өг. Local commit-ийг remote backup эсвэл production deploy гэж нэрлэхгүй.
5. Session тасарвал ямар tutorial/requirement дээр, яг ямар файл/commit-оос үргэлжлүүлэхийг хадгал. Боломжит runtime дуусахаас ӨМНӨ checkpoint хий. Чатны ой санамжийг цорын ганц хадгалалт болгож болохгүй.

## 13. Тайлан ба дууссан гэж үзэх шалгуур

Монгол хэлээр тогтмол, богино бодит update өг: юу батлагдсан, юу өөрчлөгдсөн, ямар шалгалт хийсэн, дараагийн ажил. Хийх санаагаа хийсэн мэт бүү бич.

Эцэст нь tutorial-ийн total/existing/new/rewritten/semantic-reviewed/pending, canonical coverage, MN/EN status, 6-stage practice/priority/prerequisites; problems-ийн baseline/new/source quota/dedup/ratings; editor-ийн live tests; 100-day validity/progress; profile/statistics; theme/auth/group/export regressions; SQL applied/verified; Git commit/push/PR/deploy status-ыг тусад нь тайлагна.

Шаардлага бүр evidence file + test + live/local status-тай байж байж VERIFIED_COMPLETE болно. Гарчиг байна, code file байна, row count өссөн гэдэг нь дангаараа чанарын баталгаа биш. Шинэ tutorial editor-т тохирсон бодит агуулгыг production-д зөв хадгалж/уншиж чаддагийг шалга.

ОДОО: Хавсаргасан recovery ZIP болон хоёр эх шаардлагыг унш. Одоогийн checkout/live DB-тэй diff хий. Шаардлагын checklist-ээ шинэчлээд хамгийн эхний дутуу dependency-г засаж эхэл. Бүх ажлыг нэг нэгээр нь дуусгаж, commit болон downloadable checkpoint-оор хадгалж яв.
