# Алхам 004 — private draft backend

2026-10-26. Parent commit `42d0261f6e90a2f969e7a886f4ff91def9fc086c`.
Live metadata-г эхэлж уншсан: post-022 snapshot-тай яг ижил, 023 объект байхгүй.
Migration history хоосон гэж хуучин SQL replay хийгээгүй.

Recovery 022 drafts-ийг collision-free 023 болгон өмнө remap хийсэн. Одоо
`supabase/023-tutorial-drafts.sql` root-д шилжүүлж, verified validator fingerprint
болон шинэ объектуудын absence gate нэмсэн. Partial rollout/replay бол rollback.
023 нь prerequisite/content validator-ийг солихгүй; 021/022 хамгаалалт хэвээр.

## Хэрэгжилт

- `tutorial_drafts`: (tutorial_id, editor_id) primary key, owner FK, revision,
  base_revision, JSON/size constraints, RLS enabled, direct anon/authenticated access revoked.
- 6 security-definer RPC: workspace/document, save/rebase, history/history body.
  Empty search_path, admin check, write actor match, own-draft filtering.
- Save/rebase нь advisory transaction lock + row locks + expected revision CAS.
  Incomplete draft хадгалж болно; publication validation дараагийн 024-д байна.
- Catalog-д published=true default, nullable published_at нэмсэн. Existing reader,
  catalog content/body/revision, problem IDs, progress schema өөрчлөгдөөгүй.

## Verification

`npm test`: 7 test file PASS. Шинэ PGlite тест нь owner A/B тусгаарлалт, non-admin,
anon, revoked admin, actor spoofing, direct table denial, invalid draft, stale CAS,
base revision refusal, explicit rebase, history access, replay gate шалгасан.
Хоёр queued same-revision save-ээс нэг нь амжилттай, нөгөө нь 40001 болсон.
PGlite нэг connection тул энэ нь multi-connection lock stress test биш.
55 synthetic catalog fixture, progress fixture, validator definition unchanged.

Live apply: `023_tutorial_drafts`, version `20261026054052`, success=true.
`STEP-004-APPLY.json`, `STEP-004-HISTORY.json`-д tool receipts хадгалсан.
Before/after COUNT: 748 problems, 55 tutorials. Aggregate hashes дотор stable IDs,
body/revision болон updated_at багтсан; unchanged. User rows/PII татаж аваагүй.
`STEP-004-CONTENT-FINGERPRINTS.json` query + үр дүнг хадгална.

Post-state: `supabase/audit/production-after-023.json`. Existing metadata бүх
объект дээр unchanged; нэмэгдсэн нь table 1, columns 8, index 1, functions 6,
constraints 6. Existing policies/triggers unchanged. `STEP-004-SCHEMA-DELTA.json`.
Offline SQL reconstruction comparison: бүх бүлэгт 0 зөрүү.

Эхний fingerprint SELECT нь problem_catalog.id гэж буруу нэрлэж SQL 42703
(column id does not exist), MCP HTTP 200 алдаа өгсөн. Apply хараахан дуудагдаагүй.
Catalog metadata дахь problem_id болгож зассаны дараа query/apply/after PASS.
Migration зөвхөн нэг удаа амжилттай дуудагдсан. 021/022/023 дахин ажиллуулахгүй.

## Үлдсэн ажил

Draft backend applied; full editor UI, autosave, recovery, publish/media бүрэн
болоогүй. Production admin account-аар real draft writes/E2E туршаагүй.
Одоогийн admin form published content save хэвээр; private drafts-д автоматаар
шилжсэн гэж бүү тайлагна. Дараагийн ажил нь recovery draft editor-ийн selective
merge ба browser tests; 024 publication-аас өмнө publish controls хаалттай байна.
Frontend файл өөрчлөгдөөгүй, upload жагсаалт хоосон; main/deploy өөрчлөгдөөгүй.

Client/Start skill repository-д, workspace mirror шинэчлэгдсэн. Шинэ cloud task
feature branch-ийг checkout хийж үргэлжлүүлнэ; runtime credentials тусдаа.
Original handoff ZIP нь нэгтгээгүй editor/content эхэд шаардлагатай хэвээр.
