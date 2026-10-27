Title: Package 4 remaining: bounded admin profile editor and guarded rollout
Head: codex/part04-admin-remaining
Base: codex/part04-recovered
Open as draft first; verify actual assigned PR number. No PR has been created yet.

This follows PR20 at713f6e0. User merges PR20 first; recheck/retarget this follow-up to main after its base is present. No merge/auto-merge/deployment is requested.

Admin can edit surname, first name, username and profile picture only. No school/bio/email/password/Auth/roles/progress/relationship changes. Feature defaults disabled (`adminProfileEditorEnabled` absent/false). Proposed035checks existing server-admin authority on each RPC, targets/CAS/row locks, field allowlist, formatted/unique/reserved usernames, legacy/null-name preservation and private exact before/after audit.

Avatar replacement uses an actor/target-bound15-minute reservation and unique WebP path. Real browser decodes/re-encodes; server checks fixed bucket, reservation/MIME/size metadata. Narrow authenticated policies permit reserved upload/inspection and unreferenced staged cleanup, with current/audited avatars protected. No owner-profile RLS or bucket config change. Server does not independently decode pixel bytes; live Storage gateway behavior remains an approval/fixture gate.

Remaining rollout is tracked here:032–034proposals,245metadata imports,271URL updates,035installation/access review,approved live verification and final handoff. Prepared inert artifacts remain preserved in PR20; neither merge executes them. Keep backend31/adminfeaturefalse until matching support is separately approved/verified. No new problem content authoring, baseline review or tutorial lesson work. Package4incomplete;package2not started.

Validation:82/82Node; synthetic SQL roles/unknown-fields/CAS/unique-reserved/legacy-name/target/MIME/size/expiry/cleanup/replay guards; actual-browser real PNG→WebP, default-disabled, stale-save cleanup, account-switch/revocation, light/dark/mobile; backend31 basic-edit and problem-page regressions. No production accounts/avatars or permissions changed.

PR20code passed80tests and is mergeable but remains draft because automatic approval review rejected its ready-state action. This PR creation was also rejected in the child task; no alternate route/retry was attempted. See `audit/PART04-WORKFLOW-BLOCKERS.json`. Parent must resolve exact workflow authorization before publication/state changes.

Evidence: `audit/PART04-PR21-DELIVERY.md`, `PART04-PR21-VERIFICATION.json`, `PART04-ADMIN-PROFILE-PROPOSAL.md`, `supabase/proposals/035-admin-profile-editor.sql`.
