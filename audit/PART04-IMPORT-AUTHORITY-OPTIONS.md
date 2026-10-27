# Import authority options — planning only after42501

No additional production writes were performed.036is installed;245new imports remain0. Existing configured Supabase MCP connection works. Its SQL execution context has no app-user UUID and the existing authenticated import RPC correctly refused42501 before processing. No role claims,auth.uid,credentials,RLS or grants were changed.

## Existing supported route: signed-in app admin (preferred)

The project already exposes `admin_import_learning_problems(jsonb,boolean)` to `authenticated` and checks server-owned `is_admin()` every call.036makes its delegated save preserve required tags,priority and rating provenance. Each RPC handles1–50rows with a shared advisory lock,duplicate checking and an atomic transaction. Five batches are50+50+50+50+45. `admin_import_problems` is another installed authenticated admin RPC,but lacks the dry-run interface;prefer the first.

There is no existing owner-maintenance import-specific interface in the inspected project. The generic database migration/SQL operator is not an app-admin session. Do not silently reinterpret the refusal as permission to run raw DML.

User action for the preferred route: sign into the existing site with an already-authorized admin account. No credentials/tokens should be pasted into chat,exported,printed or given to this task. An import runner must execute in that user's own browser context using the normal Supabase SDK/session and the existing RPC. The currently deployed UI gates bulk import until newer rich-content backend flags,so its ordinary import button is not yet a supported036-only route. Do not enable backend34falsely. A separately reviewed036-compatible browser admin runner can load the three local metadata files,check `is_admin`,read admin catalog,check the immutable245allowlist,perform all dry-runs,then require a concrete import confirmation. Native SDK keeps its session internal;no service-role key or auth impersonation. This runner is proposed,not implemented/deployed/executed here.

RPC verification: stop on duplicate/changed identity or denied role. Save each transaction receipt before advancing. On timeout/uncertainty,requery supported admin catalog by source/ref/URL before retry;never blindly rerun. Any partially committed earlier batches remain clearly recorded,not rolled back by touching old rows. Recompare every inserted required field and all748before-state rows. Preserve real server IDs from receipts.

## Alternative: explicitly authorized one-off owner maintenance operation

This would be a NEW scoped maintenance data operation,not the denied app-user RPC and not an existing hidden import privilege. Authority must come from separate exact authorization for the connected database operator to execute this reviewed allowlisted job. Current permission to use the app-admin import is not treated as that authorization. No SQL job has been executed or exposed as a new persistent RPC.

Review specification for the exact job:

1. Pin `PART04-IMPORT-AUTHORITY-ALLOWLIST.json`:245source/ref/URL identities,per-row canonical metadata hashes and combined hash. Only the three metadata-only input files are permitted. No optional statement/editorial/hint publication or271URLupdate.
2. Immediately capture fresh schema/function fingerprints,all748problem rows with IDs/numbers/bodies/archive/revisions and relevant sequence/source state into private recovery. Reject any unreviewed drift. Confirm036functions are present and every quota row remains new;include archived rows and canonical CF aliases in dedup. Six required source names already exist;abort rather than writing the source registry if that changes.
3. Use a single explicit transaction,existing advisory lock72483160and catalog row-write exclusion. Recheck exact baseline identities/content/revisions after obtaining the lock. No progress/profile/Auth/Storage/tutorial locks or writes. All supplied metadata validates through036's problem validator;enforce numeric rating/provenance,three-tier priority,tags and allowed identities before allocating IDs.
4. Allocate numbers using the existing server sequence and the same036ID/pack rules;never guess749or reuse a number. Insert only new problem_catalog rows,revision1,archivedfalse. Serialize all required metadata exactly as036save;preserve additional curated metadata safely. Maintain problem_changes create history with **actor_id NULL**,per its existing nullable contract,explicitly identified as database maintenance in external receipts/migration journal. Never claim an app-admin UUID or forge auth.uid. No server-admin predicate/grant is weakened or replaced.
5. Capture exact actualID/number/source/ref/URL/provenance/body receipts inside the transaction. Assert245insertions,expected993total if the fresh count is still748,zero baseline changes and exact new metadata equality. Any failure raises and rolls back catalog/history insertions. PostgreSQL sequence increments can survive rollback:document gaps,do not reset/reuse numbers. Commit only after all assertions pass;uncertain outcome must be checked by actual identities/receipts before any retry.
6. After commit,re-read all245and all748baseline rows;verify metadata,IDs/revisions and source/table/access invariants. No code touches learner tables;do not mislabel legitimate concurrent learner progress as job mutation or overwrite it. Store a private before/after/receipt artifact and only sanitized aggregate evidence in Git. A separately approved one-off migration journal name can identify the maintenance operation;no reusable public bypass RPC or access expansion remains.

This is an exact review specification and immutable data allowlist,not a runnable approved script. If this alternative is chosen,next prepare the executable job and isolated failure/rollback/idempotency tests for review BEFORE requesting action-time execution. Do not execute raw DML simply to bypass42501.

## Separate035security approval

See `PART04-035-ACCESS-APPROVAL.md`. Owner-import authorization would not authorize035profile/Storage grants,optional content publication,271URLupdates,merge or deployment. These are independent choices. Package4remains incomplete and package2has not started.
