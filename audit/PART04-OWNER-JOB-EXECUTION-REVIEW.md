# Exact owner-maintenance operation awaiting action-time approval

**Preparation only. No production import was executed.036is already installed;245imports remain0.**

Executable file: `supabase/maintenance/part04-owner-245-PROPOSED.sql`.
SHA256: `faa73bd3d42dbca5bc22c83cedf071252bc9221a2631d0d3b8f39231e386ca23`.
Size:220577bytes. Full Node suite86/86passed,including3isolated owner-job scenarios. Exact generated SQL is compared with the checked-in executable artifact in tests. See `PART04-OWNER-JOB-VERIFICATION.json`.

## Authority and proposed consequence

This requires a NEW explicit authorization for the connected database owner to run this exact one-off maintenance data job. It is not the refused app-user RPC and is not authorized merely by preparation. Existing42501server-admin checks remain intact. No auth.uid/role-claim modification,credentials,new persistent RPC,grants,RLS change,035installation or privilege expansion. No browser runner was implemented/deployed.

With still-matching guards,one transaction inserts245new problem records and245create-history records,allocating IDs/numbers through the existing sequence/ID rules. Expected count748→993. All numeric ratings/provenance,tags,individual priority/rationale and additional curated metadata are retained. History actor_id is NULL under the existing nullable FK contract,not a forged app-admin UUID. The returned receipt explicitly labels the database-owner maintenance operation.

No existing record is updated/deleted. No source registry write (all six required sources exist). No progress/profile/Auth/tutorial/Storage/271URL/optional-content publication. Temporary manifest/before-state/receipt tables are session-private,not permanent app schema objects,and expire with the SQL session.

## Guards and transaction behavior

The file embeds the complete fixed245metadata manifest and its digest. It pins four installed function fingerprints,explicit-C-collation baseline748row digest,source-registry digest and sequence last_value/is_called. It requires database-owner membership and no app-user impersonation,shares existing import advisory lock72483160and excludes catalog writers while permitting reads. Unreviewed catalog/history triggers abort. Every row is validated/deduplicated (including archived records and CF URL aliases) before allocating any numbers. Final checks prove245new rows and exact original-row preservation and recheck function definitions. No silent skip/overwrite or automatic retry.

The tests insert all245with actual runtime IDs,check every supplied metadata field,old history and learner record preservation,and reject replay. An injected failure at number850rolls back all new catalog/history rows while leaving sequence850consumed;retry then refuses the stale sequence guard. Tests also reject baseline drift,CF-alias conflicts and modified manifests before sequence allocation. These are isolated PGlite tests,not a live execution claim.

Before any execution:verify this exact file hash,refresh scoped private recovery and compare current state to the pinned preflight. Drift means stop/review;do not remove guards to force execution. Use an approved SQL adapter that keeps this whole file on one connection and supports explicit BEGIN/COMMIT plus the final receipt SELECT. On error,the adapter must ROLLBACK or close the aborted transaction/connection. Do not fragment the file into autocommit statements. Lock timeout5s,statement timeout90s. Sequence increments can survive rollback;never reset/reuse numbers.

A timeout/transport error or missing receipt can occur after commit:stop and reconcile all245source/ref/URL identities,actual IDs/body metadata and create-history before deciding outcome. Never infer failure and rerun. Save private receipts/before-after verification;publish only sanitized aggregate evidence. The job returns full metadata receipts after commit using session-private temporary tables;close that SQL session after receipt capture.

## Separate035choice

Fresh read-only schema snapshot exactly matches verified after036;035is absent,its is_admin guard and existing profile/Storage RLS match expected baseline. No actual users/avatars read or changed.035still needs separate access approval for the four-field editor and three narrow reserved-avatar policies. Exact file/hash/access impact in `PART04-035-ACCESS-APPROVAL.md`. Metadata-job approval does not authorize035or live account/avatar testing,merge or deployment.

Parent can now present the executable job/hash/consequence and035access sheet together for informed independent choices. Neither operation should be executed from this preparation checkpoint.
