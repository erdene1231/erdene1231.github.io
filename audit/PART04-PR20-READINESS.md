# PR20 code readiness and remaining-work split

PR20 contains completed frontend work and the 245 curated metadata records. It is a code review/release unit compatible with the actual after-031 backend; merging it does not install SQL, import the new bank, or publish optional content. The user merges. No auto-merge/deploy is requested.

Latest main was fetched and merged without rewriting history (main b8c2eb2). New public `problemBackendVersion` declaration defaults strictly to 31; it is a deployment capability flag, never an authorization source. Do not set it to 32/33/34 until corresponding separately approved migrations are installed and verified.

At default31, existing problem basic edits preserve legacy priority/IDs/hints and use existing RPCs without probing missing editorial/statement RPCs. Unsafe new writes are disabled: three-tier priority controls, new problem creation, rich-content editing and bulk imports. Existing advanced rows fail closed rather than dropping metadata. Readers do not display placeholders for problems lacking optional content. Existing rich content remains preserved in previews/branches; it is not silently discarded or published.

All 245 selections are code artifacts, not live imported rows. Frozen748 metadata is unchanged. The already prepared 032–034 SQL files remain inert review artifacts; no automatic migration runner exists. Their production installation, data dry-run/import/URL actions, authenticated live verification and the new admin-profile feature belong to the separate remaining-work PR. Final archive receipts describe the earlier source checkpoint; later merge-readiness commits are preserved in Git and are not falsely claimed inside that ZIP.

Validation: full Node80/80, actual after-031 SQL legacy edit/CAS test, real browser default31 basic-edit/missing-RPC gating, rich-content34 mock regression, auth-link flows and final bank/problem-page checks. See associated audit JSON reports. No production account/content mutations or remote CI success is implied.

Remaining-work field scope is surname, first name, username and profile picture only. No school/email/password/auth/role/progress edits. Package4 remains incomplete until remaining PR scope and applicable installation/live/delivery gates are truthfully resolved; package2 has not started.
