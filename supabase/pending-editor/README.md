# Pending recovery SQL — not an apply queue

022–025 are applied and verified in the root migration directory. Only 026/027
remain source candidates here; do not run this folder as a batch or replay applied
migrations. Recovery numbering differs from production prerequisite 021.

Before each activation inspect current schema/functions, constraints/indexes/RLS/
triggers and admin content fingerprints. Compare dependencies, isolate tests, then
move only the reviewed missing migration to the root. Read ../../NEXT-STEPS.md,
../../audit/STEP-009.md and ../../audit/EDITOR-MIGRATION-MAP.json.

026 adds catalog triggers affecting legacy writers; preserve 021 prerequisite,
024 publication and 025 media validation. 027 needs private draft/history/media
permission tests before batch imports. 025 bucket/policies are live; authenticated
Storage API byte upload and deployed frontend smoke are still unverified. No
cleanup job has run; any cleanup must use Storage API after reference/age checks.
