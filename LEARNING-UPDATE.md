# Erdene Club — сургалтын шинэчлэл

Огноо: 2026-10-25. Энэ багц нь ажиллаж байгаа static GitHub Pages frontend + Supabase төслийн нэмэлт шинэчлэл. Production-д SQL ажиллуулаагүй, GitHub руу push/deploy хийгээгүй. GitHub connector-ийн бичих эрх 403 өгсөн тул татаж авч суулгах багцаар хүргэж байна.

## Бодитоор хэрэгжүүлсэн зүйл

- Өмнөх 297 бодлогын ID, дугаар, CF-ийн албан rating-ийг хадгалсан. Шинээр CSES 379, AtCoder Educational DP 26 бодлогын metadata нэмсэн. Нийт 702: CF 267, CSES 400, EGOI 5, IOI 4, AtCoder 26.
- Бүх бодлого тоон rating-тай. CF-ийн албан rating болон зохиогчийн CF хэмжээст estimate-ийг `≈` тэмдэглэгээгээр ялгана. 237 шинэ бодлогын estimate нь ерөнхий ангиллаас авсан урьдчилсан утга; нэг бүрчлэн дахин хянах шаардлагатай.
- 55 Монгол/English tutorial: өмнөх 43-аас Binary Search, Greedy, DP-ийг гүнзгийрүүлж, 12 шинэ хичээл бичсэн. MathJax, C++ highlight/copy, хэсэгчлэн унших, prerequisite/variant/next холбоос, practice, checklist, 3 алхамчилсан demo нэмсэн.
- 100 өдөр, 10 шаттай хөтөлбөр. Өдөр бүр бодит problem key/tutorial ID, зорилго, ажиглалт, required/challenge, хугацаа, checklist-тэй. Уншсан/нээсэн төдийд өдөр дуусахгүй. Required бодлогуудын solved төлөв + хичээлийн 5 өөрийн үнэлгээ + өдрийн checklist шаардлагатай. Pause/resume, current day, account тус бүрийн хадгалалттай.
- Тусдаа Profile route, bio, бодсон/оролдох/хадгалсан/дахин бодох жагсаалт, activity heatmap, streak, rating bar chart, tag donut, долоо хоногийн тайлан. Хуучин огноогүй progress-оос solve date зохиож үүсгэхгүй.
- Compact/comfortable бодлогын жагсаалт, 100/page, одоогийн шүүлтүүрүүд, холбоотой хичээл/өдөр. Light theme цагаан neutral болсон; dark theme-ийн үндсэн өнгө хадгалагдсан.
- Admin → Сургалт: batch dry run/import, шинэ tutorial бүртгэх, rough estimate/холбоос/metadata/backlog хянах хэсэг. Одоогийн tutorial editor дотор relationship засах боломжтой.

Account, friends/following, private groups, багшийн тэмдэглэл, Excel/PDF export-ийн үндсэн модулиудыг өөрчлөөгүй. CMS холбоосууд `https://judge.erdeneclub.com/` хэвээр, тусдаа tab-д `noopener noreferrer`-тай нээгдэнэ. SSO/backend integration байхгүй.

## Суурь төлөв ба суулгах дараалал

Энэ нь шинэ repository биш, одоогийн `erdene1231/erdene1231.github.io` repository дээр тавих update. Багцад `config.js`, `CNAME`, secret эсвэл service-role key ороогүй. Одоогийн config, domain болон vendor assets-аа хадгал.

1. Одоогийн repository дээр backup branch/tag эсвэл ZIP үүсгэ. Frontend rollback хийх commit-оо тэмдэглэ.
2. Database backup/restore боломжоо шалга. Тухайн project дээр backup байхгүй бол `profiles`, `progress`, `problem_catalog`, `problem_changes`, `problem_sources`, `tutorial_catalog`, `tutorial_changes` хүснэгтүүдийн нөөц, доорх function definition-уудыг тусад нь ав. Хувийн progress/тэмдэглэлийг public repository руу бүү commit хий.
3. Доорх 6 жижиг migration-ийг **нэг нэгээр нь**, дугаарын дарааллаар Supabase SQL Editor дээр ажиллуул. Нэг бүрийн дараа verify query-г шалга. Эдгээр нь content seed биш.
4. ZIP-ийн `site/` доторх файлуудыг existing repository-ийн root руу ижил замаар хуул. `site/` гэдэг давхар хавтас үүсгэж сайт байрлуулахгүй.
5. Боломжтой бол эхлээд staging/preview дээр бодит test account-аар доорх smoke test-үүдийг хий. Дараа нь GitHub Pages publish хий.
6. Admin account-аар **Admin · Сургалт** хэсэгт орж, эхлээд **Dry run · Бичилтгүй шалгах**, дараа нь **Шинэ бодлогуудыг импортлох** товчийг дар. Default batch 20, 1–50 болгож тохируулж болно.
7. **Шинэ tutorial нэмэх** товчоор шинэ 12 ID-г database-д бүртгэ. Дараа нь tutorial admin editor-оор ердийн байдлаар засаж болно.

Шинэ сан импортлохоос өмнө онлайн catalog нь одоогийн 297 бодлогоо харуулна. JSON файл хуулсан төдийд server catalog автоматаар 702 болохгүй. Багцад байгаа 405 мөртэй `learning-problems.json`-ийг хуучин 200 мөрийн хязгаартай ердийн JSON uploader руу бүхлээр нь өгөхгүй; шинэ Admin · Сургалт batch importer-ийг ашигла.

## SQL migration бүр

Одоогийн project дээр `schema.sql`, public profile/username (002/003), problem catalog (004/007), tutorials (008) аль хэдийн суусан байх ёстой. Хуучин том seed SQL болон 010–014 content update-ийг энэ багцын төлөө дахин ажиллуулах шаардлагагүй.

| Файл | Зорилго, dependency | Өгөгдөл ба verify |
|---|---|---|
| `015-problem-metadata.sql` | 007-ийн problem validation/admin save-ийг metadata, unrated compatibility, шинэ CSES/AtCoder stable ID-тай болгоно. | Existing row/ID/number-ийг migration өөрөө шинэчлэхгүй. `validate_learning_problem(jsonb)` function бий эсэхийг шалга. |
| `016-learning-records.sql` | Суурь auth schema. Tutorial/plan/bookmark private records ба owner RLS. | Өмнөх progress өөрчлөгдөхгүй. `pg_policies`-д owner policy, RLS идэвхтэй эсэхийг шалга. |
| `017-real-progress-dates.sql` | Суурь progress хүснэгт. First attempted/solved timestamp, intent flag, trigger/index. | Backfill хийхгүй. Өмнөх огноогүй solved мөрүүд null хэвээр. Frontend-ийн шинэ төлөвийн үйлдэл л timestamp авна; backup сэргээх болон хуучин client огноо үүсгэхгүй. |
| `018-learning-profiles.sql` | Public profile helper (003), 016, 017. Bio ба шинэ public profile RPC. | Email, хувийн note, hint, learning record-ийн бүх агуулгыг задруулахгүй. Зөвхөн public facts ба plan-ийн товч aggregate. |
| `019-safe-learning-import.sql` | 015. Admin-only 1–50 мөрийн insert-only importer. | Dry run ба import ижил validation хэрэглэнэ. Source/ref, normalized URL, archived row-аар dedup хийнэ. Нэг batch алдаатай бол тэр batch бүхлээрээ rollback. |
| `020-new-tutorials.sql` | 008. Шинэ tutorial insert, existing tutorial-ийн revision-тэй edit wrapper. | Existing хичээл автоматаар overwrite хийхгүй. Revision зөрвөл conflict өгнө. |

Бүх файл transaction-тай. Ижил migration-ийг давтан ажиллуулах local шалгалт давсан. Production-ийн өмнөх schema өөр байвал тухайн SQL-ийн алдааг эхлээд шийд; дараагийн файл руу шууд алгасаж болохгүй.

Read-only шалгалтууд `supabase/VERIFY-learning.sql` файлд бий. Энэ нь дахин migration биш.

Migration-ээс өмнө хадгалах function definition-ууд:

```sql
select p.oid::regprocedure as signature, pg_get_functiondef(p.oid) as definition
from pg_proc p
join pg_namespace n on n.oid = p.pronamespace
where n.nspname = 'public'
  and p.proname in (
    'admin_save_problem', 'admin_import_problems',
    'get_public_profile', 'get_public_progress', 'admin_save_tutorial'
  );
```

Энэ query-ийн үр дүнг database backup-тай хамт хувийн байдлаар хадгал.

## Импорт, ID, custom content хамгаалалт

- 405 шинэ бодлогын statement/testdata-г хуулж оруулаагүй; title/source/ref/HTTPS URL болон сургалтын metadata байна. Энэ нь CMS task upload ZIP биш.
- Source type байхгүй бол өмнөх admin source системээр үүснэ.
- Importer existing, archived болон өөр URL хэлбэртэй ижил бодлогыг шинэ хуулбараар оруулахгүй. Archived бодлогыг автоматаар сэргээхгүй; админ өмнөх editor-оор шийднэ.
- Тухайн үед insert болсон дарааллаар database `number` олгоно. Өөр админ зэрэг нэмсэн бол шинэ бодлогын дэлгэцийн дугаар offline JSON-оос зөрж болно. Progress-ийн гол холбоос нь тогтвортой ID. Existing 297 ID/дугаар өөрчлөгдөхгүй.
- Practice/plan нь `source|official-ref` canonical key-ээр бодит catalog ID-г олно. Жишээ: CSES Number Spiral-ийн хуучин `task-87`-г `cses-1071` болгож солихгүй.
- 3 жишиг tutorial-ийн шинэ body-г зөвхөн авсан baseline-тай SHA-256 нь яг таарсан үед frontend overlay хэрэглэнэ. Админы түүнээс хойших custom edit-ийг автоматаар дарж бичихгүй. Overlay-г editor дээр нээгээд ердийн Save хийвэл database revision/audit-аар хадгалагдана.
- Шинэ 12 хичээл database-д хараахан байхгүй бол local seed-ээс уншигдана. Бүртгэх товч нь existing ID-уудыг алгасана.
- Шинэ систем account бүрийн private records-ийг салгаж хадгална. Зочны record-ийг account руу автоматаар зөөхгүй. `learning_records` нь бодлогын хуучин status/notes хүснэгтийг давхар орлохгүй.
- Offline үйлдлийн өөрийн profile дахь local огноо, дараа sync хийх үеийн server receipt огноо нь удаан offline байсан үед ялгаатай байж болно. Онлайн server огноог гол баримт болгоно. Энэ нь гаднын judge-ийн AC timestamp биш.

## Шалгалт

Runtime frontend нь build шаарддаггүй static ES modules. Node/PGlite нь зөвхөн local verification-д хэрэглэгдэнэ.

```bash
npm ci
npm test
npm run test:content
npm run test:sql
```

`test:content`-д Python 3, g++ (C++17) хэрэгтэй. Бодит browser test нь тусгаарласан config-тай preview дээр хийгдсэн; production account/database-д бичилт хийгээгүй.

- 13 model/store тест: 702 schema/ratings, baseline ID, relationship DAG, 100 өдөр, opening ≠ completion, timezone/week, missing practice, edition hash, filters, account солигдох, failed sync, archived progress.
- 55 reference program C++17 compile/sample тест; хоёр хэлний full code ижил. Нэмэлтээр duplicate/empty boundary, unreachable/negative cycle, 200,000 оройтой tree chain, meet-in-the-middle-ийг exhaustive шийдэлтэй 30 харьцуулалт.
- PGlite дотор 6 migration болон actual 405 insert: owner/other user/anon/admin RLS, dry run/validation/dedup, stable IDs, атомик batch, revision conflict, private notes, repeated migrations. Supabase-ийн network auth/session integration-ийг үүгээр орлуулж бүрэн баталсан гэж үзэхгүй.
- Desktop ба 390px iframe mobile: MN/EN, MathJax/C++ highlight, step reader, demo, saved note/bookmark, hint hide/show/English, rating min/max, 100/page, density reload, profile charts, pause/resume/checklist reload, Day 1 completion → Day 2, light/dark, CMS root links.
- Missing curriculum fixture дээр үндсэн problems/account хэсгийн graceful fallback; admin editor fixture дээр invalid relationship хориглох, MathJax preview, шинэ tutorial save method шалгасан.

Production/staging account-аар нэмж шалгах зүйлс:

1. Энгийн A/B account тус бүрээр tutorial/plan/bookmark үүсгээд бусдын private record харагдахгүйг шалгах.
2. A → sign out → B → A үед status, notes, checklist солигдохгүй байх; өөр browser-оор дахин нэвтэрч sync шалгах.
3. Нууц үг сэргээх, avatar/овог нэр/сургууль, friends/following, private group/teacher note, Excel/PDF export-ийн existing урсгалууд.
4. Энгийн хэрэглэгч admin RPC/import ашиглаж чадахгүй; админ dry run/import/edit/revision conflict хэвийн.
5. Migration-ээс өмнөх огноогүй solved-ууд null хэвээр; шинэ manual solve огноотой, backup restore огноо зохиохгүй.

Эдгээр бодит auth smoke test-ийг одоогийн орчинд хийсэн гэж тайлагнаагүй.

## Алдаа гарвал recovery

- SQL файл transaction дотроо алдаатай дуусвал тэр файлын өөрчлөлт commit болохгүй. Error message-ээ хадгалж, зассаны дараа **тэр файлыг** дахин ажиллуул. Data table drop/truncate хийх хэрэггүй.
- Importer нэг batch дээр зогсвол өмнөх амжилттай batch-ууд үлдэнэ. Дахин dry run/import хийхэд existing мөрүүд алгасагдана. Сурагчийн progress устгах шаардлагагүй.
- Frontend асуудал гарвал өмнөх Git commit/ZIP-ээ сэргээж Pages-д дахин publish хий. Шинэ additive хүснэгт/багануудыг database-д үлдээж болно; хуучин client шинэ intent flag-ийг илгээхгүй тул худал date үүсгэхгүй.
- 015-ийн function өөрчлөлтийг буцаах шаардлагатай бол хадгалсан хуучин `admin_save_problem` definition болон execute grants-ийг transaction-аар сэргээ. Шинэ stable ID-тай бодлогуудыг үүнээс болж дахин дугаарлаж болохгүй.
- 018-ийн public profile RPC-д асуудал гарвал frontend нь өмнөх public profile/progress RPC руу fallback хийнэ. Сурагчийн private data-г public болгох байдлаар policy-г сулруулж засахгүй.
- Content импортлолтыг бөөн DELETE-ээр буцаахгүй. Audit-аар зөвхөн энэ импортын шинэ problem ID-уудыг шалгаж, шаардлагатайг өмнөх admin editor-оор archive хий; progress хэвээр үлдэнэ. Tutorial-ийг audit/өмнөх body-оор revision-тэйгээр сэргээ.

## GitHub Pages publish

Existing repository-ийн Pages source branch/root тохиргоог хэвээр ашигла. Build workflow байгаа бол өмнөх workflow-г өөрчлөх шаардлагагүй; `index.html` болон module/JSON файлууд root-д байна.

1. Шинэ файлуудаа repository root руу хуулж commit/push хийнэ.
2. GitHub → Actions/Pages deployment амжилттай болсныг шалгана.
3. `https://erdeneclub.com/` дээр hard refresh. `#tutorial/binary-search`, `#profile`, `#plan`, `#library` route-уудыг шалгана.
4. CMS-ийн хоёр холбоос зөвхөн `https://judge.erdeneclub.com/` рүү нээгдэж буйг шалгана.
5. Admin · Сургалт-аар content import хийгээд сангийн count, хичээлийн practice/day холбоосыг дахин шалгана.

30 ахисан draft сэдэв, 237 rough rating болон нэмэлт олон улсын эх сурвалжийн selection/editorial review-г бэлэн болсон гэж тооцоогүй. Нарийвчилсан контентын хүрээ `CONTENT-REVIEW.md` дотор бий.
