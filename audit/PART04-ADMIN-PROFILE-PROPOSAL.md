# Admin profile editor — implemented locally, disabled by default

Latest confirmed scope: **surname, first name, username and profile picture only**. This supersedes earlier school/avatar ambiguity and the abandoned email request. No email-change feature was implemented. School, bio, email, password, Auth identity, roles/admin grants, progress and relationships are untouched.

`admin-profile.js` supplies an accessible editor inside the Admin hub, with username/UUID lookup, original-field preservation, explicit save, stale conflict/reload behavior, account-switch/revocation cleanup and responsive theme styling. `adminProfileEditorEnabled` defaults false; no profile RPC or private form is enabled until this flag is deliberately enabled after separately approved backend installation. It is not an authorization mechanism.

`supabase/proposals/035-admin-profile-editor.sql` is proposal-only and independent of032–034. It creates private RLS-enabled audit/upload-reservation tables. Lookup, prepare-upload and save RPCs are executable only by authenticated clients and check existing server-owned `is_admin()` on every request. Profile row locks and full-row snapshot comparison reject concurrent owner/admin changes, including changes to fields not editable here. Names/combined full name <=100; username lowercases, validates3–24 ASCII characters, uses existing uniqueness and rejects newly assigned reserved names. The UPDATE allowlist is exactly first/last/derived full name, username and optional avatar path. Existing owner profile RLS is unchanged. UUID/progress identity remains stable when username changes.

## Proposed Storage access change requiring separate approval

The existing public `think-cp-avatars` bucket remains public, at2MiB, with its existing MIME allowlist; no bucket configuration change. A server-admin prepare RPC allocates a unique target-folder WebP path tied privately to actor/target and a15-minute reservation. Three authenticated Storage policies allow only that admin's reserved upload, narrow reservation inspection, and cleanup of that admin's unreferenced staged object. Cleanup cannot remove a current avatar or an avatar recorded in private audit history. Existing objects are never overwritten (`upsert:false`); prior avatars are not automatically deleted. No broad cross-user bucket grant is proposed.

The browser actually decodes and re-encodes permitted PNG/JPEG/WebP to WebP <=512px. Server save checks existing object, fixed bucket, reservation actor/target/expiry and actual Storage metadata MIME/size (1–2MiB), but does **not** independently decode pixel bytes. Synthetic SQL Storage fixtures and browser codec tests are not a live Storage-gateway test; that limitation must remain explicit before installation approval. Bucket/owner policies are preserved. Never delete Storage objects through SQL.

Private audit records actor/target and before/after permitted fields only; no public history/table grant. No privileged browser key, credential generation, impersonation or Auth-admin API is used.

## Evidence and remaining gates

Full Node suite82tests plus actual-browser admin image round-trip, default-disabled behavior, stale-save cleanup, account-switch invalidation and both themes/widths. SQL fixtures cover anon/non-admin/revoked denial, unknown fields, reserved/unique usernames, full-snapshot CAS, stable learner records, target-bound reservations, MIME/size/expiry, cleanup reference protection and replay guard. See `PART04-ADMIN-PROFILE-BROWSER.json` and `PART04-PR21-VERIFICATION.json`.

No production installation, user update, real avatar upload/deletion, permission change, merge or deployment occurred. Before any write: fresh actual profiles/Storage/ACL audit, scoped private before-state and exact035access-diff approval. Real Auth/Storage role and concurrency checks require an authorized safe fixture. Only after installation/verification may the feature flag be enabled.
