# Үргэлжлүүлэх — алхам 002

Branch: `codex/recovery-step-002-editor-blocks` (baseline ancestor `f7c5f2e`).
Checkpoint commit SHA-г archive `MANIFEST.json` болон Git log-оос авна.
Эхлээд `start/SKILL.md`, `audit/STEP-002.md`, `audit/REQUIREMENTS-CURRENT.md` унш.

1. Production history: 021 prerequisite (`20261026045125`), 022 blocks
   (`20261026052253`). 748/55, content hashes unchanged. **Алийг нь ч replay хийхгүй.**
2. Current frontend нь legacy хэвээр. Recovery renderer/editor-ийг diff-ээр нэгтгэж,
   old content/new editor round-trip, XSS, MN-only, lazy reader болон mobile/browser
   compatibility-г шалга. New block body-г reader бэлэн болтол production-д нийтлэхгүй.
3. Дараа нь `supabase/pending-editor/023-tutorial-drafts.sql`-ийг current schema-тай
   дахин тулгаж owner A/B/admin/revoked/stale-CAS тестээр баталгаажуул.
   024 publication, 025 Storage, 026 references, 027 batch тусдаа apply gate-тэй.
4. Existing admin-edited content-ийг current ID/revision/hash-аар дахин уншиж,
   explicit merge/CAS without content overwrite. `problems.json` болон
   `tutorials.json`-ийг recovery хувилбараар бүхлээр нь солихгүй.
5. Recovery frontend source энэ алхамд merge хийгдээгүй. Original handoff ZIP-ийг
   хадгал: recovery SHA256 нь `f615dc21b6c0ca40e78ebf4b745b7244a88757062f36bae2610e941257583914`.
   Full recovery archive энэ checkpoint-д давхар оруулаагүй; user-ийн эх хавсралтаас
   сэргээнэ. Pending SQL, эх requirements, inventory нь GitHub-д хадгалагдана.
6. Editor compatibility дуусмагц Binary Search/Greedy semantic + browser review;
   3 historical reviewed tutorial-ийг шинэ hash-аар дахин нягтал. 41/55 гэх
   баталгаагүй тоо ашиглахгүй. Pending BOI17 Toll ID-г server-аас reconcile хийхгүйгээр
   импорт/нийтлэл complete гэж тэмдэглэхгүй.

Local smoke: `npm test`; `node tools/compare_supabase_schema.mjs`.
Runtime bindings: network secret SUPABASE_WRITE_TOKEN, env SUPABASE_PROJECT_REF,
allowed mcp.supabase.com. Token/session-ийг файл, Git, ZIP, тайланд гаргахгүй.

Алхам бүр: scoped changes → tests → audit/checklist update → commit → feature
branch push + remote SHA verify → downloadable ZIP + CRC/checksums + next steps.
Main merge/frontend deploy нь тусдаа; environment publish-ийг website deploy гэж бүү нэрлэ.
