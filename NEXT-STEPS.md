# Үргэлжлүүлэх — алхам 004

Branch: `codex/recovery-step-004-private-drafts`.
Parent: `42d0261f6e90a2f969e7a886f4ff91def9fc086c`, GitHub дээр батлагдсан.
Checkpoint SHA болон remote verification-ийг ZIP-ийн `MANIFEST.json`-оос авна.
Эхлээд `start/SKILL.md`, `audit/STEP-004.md`, `audit/REQUIREMENTS-CURRENT.md` унш.

1. Production history: 021 prerequisite (`20261026045125`), 022 blocks
   (`20261026052253`). Сүүлийн live шалгалт 748/55, content hashes unchanged.
   023 private drafts (`20261026054052`) мөн хэрэгжсэн.
   **021/022/023-ийг replay хийхгүй.** Алхам 004 content hash/revision unchanged.
2. Typed reader local/browser тесттэй. Legacy editor шинэ блокуудыг read-only
   хадгалж, English байхгүй үед Монгол агуулгыг English болгон overwrite хийхгүй.
   Frontend deploy хийгдээгүй. `audit/STEP-003.md` дахь 11 файлыг хамтад нь deploy
   хийж live reader-ийг шалгасны дараа л шинэ төрлийн body нийтэлж болно.
3. Дараагийн эхний дутуу ажил: recovery draft editor UI-г diff-ээр нэгтгэ.
   023 backend-ийн owner A/B/admin/revoked/CAS/rebase тест PASS, production schema
   verified. UI autosave/account switching/offline recovery-г browser-т шалга.
   Publish controls-ийг 024 батлагдахаас өмнө идэвхжүүлэхгүй. 024 publication/lazy
   reader, 025 Storage, 026 references, 027 batch тусдаа audit/test/apply gate-тэй.
4. Current eager reader RPC, edition hash gates, live content IDs/revisions,
   progress хэвээр. `problems.json`, `tutorials.json`, curriculum болон editions-ийг
   recovery хувилбараар бүхлээр нь солихгүй. Admin content merge нь current
   body/revision/hash болон CAS-д тулгуурлана.
5. Image reader signed URL хүсэж чадна; Storage policy/upload ажиллаж байгаа
   гэсэн баталгаа биш. Account солигдох үеийн late URL-г хаяна. 025-ын бодит
   authorization/upload smoke дуусахаас өмнө media complete гэж тэмдэглэхгүй.
6. Recovery-ийн үлдсэн frontend/content нь энэ checkpoint-д ороогүй. Original
   handoff ZIP-ийг хадгал: recovery SHA256
   `f615dc21b6c0ca40e78ebf4b745b7244a88757062f36bae2610e941257583914`.
   Full recovery archive-ийг GitHub-д давхар оруулаагүй; user-ийн эх хавсралтаас
   сэргээнэ. Pending SQL, requirements эх, inventory GitHub-д бий.
7. Editor work дуусмагц Binary Search/Greedy semantic + browser review;
   historical 3 tutorial review-г current hash-аар дахин нягтал. 41/55 гэсэн
   баталгаагүй тоо ашиглахгүй. Pending BOI17 Toll ID-г server-аас reconcile
   хийхгүйгээр импорт/нийтлэл complete гэж тэмдэглэхгүй.

Local: `npm ci`, `npm test`, `node tools/compare_supabase_schema.mjs`.
Browser: Python `playwright`, `/usr/bin/chromium` болон loopback socket access
байхад `python3 tests/browser/reader-compat.py`. Энэ нь external network-ийг
хааж, auth/storage RPC-г mock хийдэг; live E2E/MathJax/CDN тест биш.

Runtime: SUPABASE_WRITE_TOKEN network secret, SUPABASE_PROJECT_REF env,
allowed `mcp.supabase.com`. Token/session-ийг файл, Git, ZIP, тайланд гаргахгүй.
Client/Start skill Git-д байгаа; reusable environment image registration нь
тусдаа тохиргоо бөгөөд одоогийн workspace mirror үүнийг батлахгүй.

Алхам бүр: scoped diff → tests → audit/checklist → commit → feature branch push
+ remote SHA verify → downloadable ZIP + CRC/checksums + next steps.
Main merge/frontend deploy нь тусдаа.
