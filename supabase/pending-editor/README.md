# Pending recovery SQL — not an apply queue

022 (formerly recovery 021) is applied. These renumbered 023–027 files are reviewed
source candidates only, not production-verified migrations. Do not run the folder
as a batch. They retain recovery SQL except dependency/provenance comments.

Before each activation: inspect current schema and function definitions, verify
renderer/editor compatibility, isolate tests against actual baseline, inspect
admin content revisions/hashes, then move only that reviewed migration to the
root migration directory. Read `../../audit/STEP-002.md` and migration map.
Do not conflate old recovery 021 with production prerequisite 021.

025 changes bucket configuration and backfills media references. It requires real
Storage authorization/delivery checks. 024/026 add catalog triggers that affect
legacy writers; test these paths before rollout. 027 requires private draft and
history/media permissions to be tested before allowing batch imports.
