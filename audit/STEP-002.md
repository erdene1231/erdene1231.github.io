# Алхам 002 — recovery reconciliation ба typed content validation

2026-10-26. User baseline `f7c5f2e820f01652e3a839f2db69c05b16c91adb`
checkout-д эхэлж баталгаажсан. `main` өөрчлөгдөөгүй.
Хавсралтын эрх/хуучин амжилтын тайланг шинэ нотолгоо гэж тооцоогүй.
START-HERE болон requirements-01/02 бүтнээр уншиж эхийг `requirements-source/`-д хадгалсан.
Recovery SHA256: `f615dc21b6c0ca40e78ebf4b745b7244a88757062f36bae2610e941257583914`.

## Нэгтгэлийн хүрээ

Recovery-ийн 411 site файл: 215 ижил, 17 өөр, 179 нэмэлт. Харьцуулалт, checksum
`RECOVERY-INVENTORY.json`-д бий. Энэ алхамд **зөвхөн editor SQL dependency**-г
сонгон нэгтгэв. `problems.json`, `tutorials.json`, edition hashes, curriculum,
app/editor/renderer болон admin-ийн live body-г snapshot-оор дарж хуулаагүй.
Snapshot нийт 749 problem байж болох ч production 748; түр BOI ID импортлоогүй.
Full frontend/recovery merge нь дараагийн жижиг алхмуудад үлдсэн.

| Recovery SQL | Одоогийн дугаар | Dependency / өөрчлөлт | Төлөв |
|---|---|---|---|
| 021 content blocks | 022 | 008 + production 021; 3 helper + body validator | APPLIED_VERIFIED |
| 022 drafts | 023 | 022; private draft tables/RPC, catalog published columns | PENDING |
| 023 publication | 024 | 022–023; trigger, publish/CAS, public reader RPC | PENDING |
| 024 media | 025 | 022–024 + Storage; private bucket/policies/reference index | PENDING |
| 025 references | 026 | 022–025; relation extraction/check trigger | PENDING |
| 026 batch drafts | 027 | 023–026; backup table/trigger, atomic import RPC | PENDING |

Pending SQL `supabase/pending-editor/`-д тусгаарлагдсан; root glob-аар ажиллахгүй.
Media bucket upsert, existing-body reference backfill, new publication triggers
нь later compatibility/security checks шаардана. Эдгээрийг одоо apply хийгээгүй.

## Бодит хэрэгжилт

022 нь rich text marks, H1–H4, callout/quote/checklist, image path metadata,
typed diagrams, embedded tutorial/problem reference **shape**-ийг шалгадаг.
Legacy блок хэвээр; MN-only body зөвшөөрөх ба том нийтлэлд лимит өсгөсөн.
Энэ нь renderer, Storage delivery эсвэл relation target existence-ийн баталгаа биш.

Шинэ prerequisite validation хэсгийг яг хадгалсан. Verified function fingerprint
таарахгүй эсвэл editor helper аль хэдийн байвал migration зогсоно.
Transaction-ийн төгсгөлд тухайн мөчийн бүх live tutorial-ийг шинэ validator-аар
шалгаж, алдаа гарвал DDL rollback хийнэ. Content INSERT/UPDATE/DELETE байхгүй.

MCP apply амжилттай: `022_tutorial_content_blocks`, version `20261026052253`.
History-д 021 (`20261026045125`) мөн хэвээр. Function-only pre-state нь
`supabase/audit/production-after-021.json`, post-state нь `production-after-022.json`.

## Verification

- `npm test`: 4 test file PASS (existing model/store + 021 + 022 regression).
- Эцсийн transactional live-body gate нэмсний дараа 022 targeted test дахин PASS.
- 55 local tutorial valid; bad/null/overlong prerequisites rejected; valid rich,
  diagram, heading, callout болон бусад shape accepted; unsafe input rejected.
- Anonymous/authenticated шууд validation helper дуудах эрхгүй.
- Synthetic content revisions/stable IDs/private progress fixture unchanged.
- Live rich block validation SELECT PASS; live invalid prerequisite ID → ERROR 22023.
- Production metadata: 3 helper нэмсэн, зөвхөн `validate_tutorial_body` replace;
  table/column/constraint/index/policy/trigger/бусад function unchanged.
- Offline schema reconstruction vs post-022 metadata: бүх бүлэгт 0 зөрүү.
- 748 problems / 55 tutorials хэвээр. Problem catalog aggregate fingerprint,
  tutorial ID/revision/body hashes before=after. User rows/PII татаж аваагүй.

## Хязгаар ба үргэлжлэл

Энэ нь **recovery checkpoint**, frontend release биш. Browser/admin account/Storage
upload/publish E2E энэ алхамд хийгдээгүй. 55 tutorial semantic review дуусаагүй;
шинэ authored body нийтлээгүй. Requirement source 1467 traceability мөр,
319 topic reference (duplicate label орсон) бүртгэсэн; candidate ID нь coverage биш.

## Verify / recovery

`node tools/compare_supabase_schema.mjs` нь local snapshot-тай харьцуулна.
Шинэ live metadata авахдаа `tools/snapshot_supabase_schema.py` ашигла.
Шаардлагатай runtime token-ийг environment-ээс л хэрэглэ.
022-ийг дахин бүү ажиллуул. Сэжигтэй шинэ schema байвал шинэ audit хийнэ.
Front-end өөрчлөгдөөгүй тул upload жагсаалт хоосон. DDL recovery шаардлагатай бол
021 snapshot-аас validator definition-ийг review хийж **шинэ forward-fix migration**
үүсгэнэ; шинэ блоктой live content байгаа эсэхийг шалгалгүй downgrade бүү хий.
Private draft/content/progress хүснэгтийг drop/delete хийх rollback хориотой.
