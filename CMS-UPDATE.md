# CMS frontend холбоос

Өөрчилсөн frontend файлууд: `index.html`, `styles.css`.

## Хийсэн өөрчлөлт

- Navigation-д `Tutorials`-ийн яг дараа `CMS` нэмсэн. Одоогийн navigation-ийн
  typography, spacing, hover болон theme-ийн загварыг ашиглана.
- Нүүрийн hero дотор `Online Judge / CMS` гэсэн compact card нэмсэн.
  `Бодлого ба алгоритм` гарчиг, `Бодлогын сан`, `Tutorials` товчнууд хэвээр.
- Navigation болон card-ийн хоёр холбоос зөвхөн `https://judge.erdeneclub.com/`
  үндсэн хаяг руу чиглэнэ. `target="_blank"`, `rel="noopener noreferrer"`-тэй.
- Card-д CMS тусдаа account ашигладгийг товч тэмдэглэсэн.
- Шинэ CSS-ийг ачаалуулахын тулд `styles.css?v=21` болгосон.

JavaScript, routing, login, Supabase, сервер, CMS backend болон domain тохиргоонд
өөрчлөлт оруулаагүй. SSO, API эсвэл шинэ landing page нэмээгүй.

## Шалгалт

- GitHub-ийн одоогийн `index.html`, `styles.css` нь өөрчлөлт эхлэхийн өмнөх
  локал эхтэй яг таарч байгааг шалгасан.
- HTML-ийн ID давхардаагүй, CMS нь зөв байрлалд, хоёр холбоосын URL/target/rel
  шаардлагад нийцсэн. `erdene-test` рүү чиглэсэн холбоос нэмээгүй.
- Desktop болон mobile preview дээр харагдацыг нягталсан. Mobile цонхны бодит
  агуулгын өргөн 375 px, scrollWidth 375 px: хажуу тийш халиагүй.
- Гэрэлтэй болон бараан theme дээр card, navigation, товчийг шалгасан.
- Хоёр холбоосыг дарахад тусдаа tab-д `https://judge.erdeneclub.com/` хаягтай,
  `Choose a contest` гарчигтай хуудас нээгдсэн.
- Бодлогын сан болон Tutorials-ийн navigation ажиллаж байгааг шалгасан.
- `node --check app.js`, `node --check navigation.js` амжилттай.
  Static HTML/CSS сайт тул тусдаа build command, dependency суулгалт шаардлагагүй.

## GitHub Pages-д байрлуулах

1. ZIP-ийг задлаад `index.html`, `styles.css` хоёр файлыг
   `erdene1231/erdene1231.github.io` repository-ийн үндсэн хавтсанд ижил нэрээр солино.
2. GitHub Pages одоо ашиглаж буй branch-д commit/push хийнэ.
3. Одоогийн Pages deployment дууссаны дараа сайтаа дахин нээнэ.
   Хуучин загвар харагдвал `Ctrl + Shift + R` дарна.

Одоогийн `erdeneclub.com` domain/CNAME болон Pages тохиргоог өөрчлөхгүй.
SQL, Supabase, Cloudflare, Ubuntu эсвэл CMS дээр команд ажиллуулах шаардлагагүй.

Энэ нь байршуулж ашиглахад бэлэн багц; GitHub-д автоматаар push/deploy хийгээгүй.
