# Үргэлжлүүлэх — editor repair after 009

Current branch: `codex/fix-tutorial-editor`; parent main/PR 9 merge:
`908ab18bf0bcb59d8de64bfcdd4460267d11984f`.
Read `audit/EDITOR-FIX.md` and Start skill. Formatting/new tutorial/draft recovery
repairs are locally verified; deploy the complete v31 graph. No new migration or
production content write in this repair. ZIP remote verification records exact SHA.
Browser repair: `python3 tests/browser/editor-regressions.py`.
Next planned step remains 010, schema audit then 026 reference integrity.

The following 009 handoff remains valid historical context:

# Үргэлжлүүлэх — алхам 009

Branch: `codex/recovery-step-009-tutorial-images`.
Parent main: `d479c2e72bdf6a6284a071b8b0ad900103c94370` (PR 8 merged).
Exact checkpoint and remote SHA: ZIP `REMOTE-VERIFICATION.json` / manifest.
Read `start/SKILL.md`, `audit/STEP-009.md`, `audit/REQUIREMENTS-CURRENT.md` first.

1. Applied versions: 021 `20261026045125`, 022 `20261026052253`,
   023 `20261026054052`, 024 `20261026062140`, **025 `20261026064758`**.
   **Do not replay 021–025.** Latest metadata: production-after-025.json.
   748 problems / 55 tutorials; body/ID/revision fingerprints unchanged.
2. 009 upload/preview/metadata UI and codecs/RLS have local tests. Production
   bucket/policies verified. Authenticated real Storage byte upload and deployed
   Pages smoke remain unverified. After merge/deploy use a real admin to upload a
   private draft image, check anonymous denial, explicitly publish approved content,
   and verify anonymous reader delivery. Do not create test users or publish content
   silently. No manual migration command needed from the user.
3. Next **010: 026 embedded reference integrity**. Read actual schema/functions,
   constraints/indexes/RLS/triggers and current live hashes before applying missing
   changes. Preserve 021 prerequisite, 024 publication and 025 media guards. Pending
   026/027 are not an automatic apply queue. Original recovery numbering differs.
4. Then 027 batch drafts/private recovery, full history UI and lazy frontend.
   Editor complete precedes Binary Search/Greedy semantic + browser review. Keep
   all topic requirements; 55 rows is not quality/coverage proof. BOI17 Toll stable
   ID reconciliation remains blocked. Never use the unverified 41/55 claim.
5. Preserve admin live content, IDs/progress. No wholesale recovery overwrite or
   seed replay. Tutorial images use private Storage paths, never localStorage bytes.
   Cleanup only through Storage API after age/reference checks; no cleanup ran.
   Private previews 60s / published signed URLs 600s; issued URLs can outlive unpublish.
6. GitHub holds client, Start skill, requirements, pending SQL and audit. Original
   full recovery archive is not duplicated there; retain attached handoff ZIP with
   SHA256 `f615dc21b6c0ca40e78ebf4b745b7244a88757062f36bae2610e941257583914`.
   A fresh cloud checkout can retrieve implemented code and instructions; remaining
   unmerged recovery source may require that original attachment.

Checks: `npm ci`, `npm test`, `node tools/compare_supabase_schema.mjs`.
Browser: `python3 tests/browser/reader-compat.py` and
`python3 tests/browser/tutorial-media.py` with Playwright, /usr/bin/chromium and
loopback socket permission. Auth/Storage mocked; not live E2E.
Runtime: SUPABASE_WRITE_TOKEN network placeholder, SUPABASE_PROJECT_REF variable,
allowed mcp.supabase.com. No credential/session values in files or reports.
Workspace shared client/Start mirrors do not prove reusable image registration.

Every step: scoped diff → tests → audit/checklist → commit → feature push + verified
remote SHA → create and attach PR → downloadable ZIP + CRC/checksums + handoff.
Do not omit the PR. Main merge/deploy is a separate action.
