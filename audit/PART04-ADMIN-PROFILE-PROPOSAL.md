# Admin profile editing — bounded proposal, not implemented

Status: pending parent/user scope clarification and exact authorization review. No actual user rows have been fetched or changed, and no RPC/RLS/Storage permission has been changed. Independent package4 work may continue.

## Existing evidence

- `supabase/002-usernames-solvers.sql`: profiles SELECT/INSERT/UPDATE policies are owner-only; changing a UI target ID cannot authorize editing another user.
- `supabase/003-profiles-friends.sql`: full_name <=100, school <=160; avatar_path must be under the target user's UUID and a permitted image extension. Avatar INSERT/DELETE policies permit only auth.uid()'s folder.
- `supabase/013-study-groups.sql`: first_name and last_name <=100 each. `accounts.js cleanProfile` derives full_name from last+first and enforces its total <=100.
- `supabase/004-following-admin.sql`: public.is_admin() uses the server-owned admin_accounts table. Client metadata/email is not an authorization source.
- `accounts.js saveOwnProfile` writes the current user's profile and uploads/removes files under that user's namespace. It must not be reused by substituting an arbitrary target ID.

These are repository/schema-audit evidence, not a fresh production RLS verification.

## Proposed field scope

Default ordinary profile edit: first_name, last_name, derived full_name, school. Keep username stable unless separately confirmed (it participates in links and uniqueness). Preserve bio and unspecified fields. Email/password/auth credentials, admin/role grants, solved/progress, learning records, friendships and follows are excluded.

Avatar needs an explicit choice: permission to replace another user's image entails a new narrowly scoped Storage path authorization, not merely a text field. Prepare a target-bound upload design for review, with MIME/size/real-image validation, unique object names, failed-save cleanup and referenced-image retention. Do not grant broad bucket access, accept arbitrary URLs/paths, impersonate the target, or silently clear their avatar. Preserve current avatar until reviewed behavior is implemented.

## Proposed server contract for subsequent review

A narrow server RPC would require authenticated server-verified admin status on every request, accept an existing target UUID and an exact field allowlist, derive/validate full_name, reject unknown/security fields, and compare an expected existing snapshot/version before saving to prevent lost updates. A revoked admin must fail even if an editor was already open. Pin search_path; revoke default PUBLIC execution; return only permitted profile fields. Keep owner RLS unchanged and don't expose auth.users or private progress through a broad admin SELECT policy.

Use private audit history recording actor/target/time/changed field names; do not publish real profile snapshots in Git or downloadable reports. Proposed persistent authorization changes must be shown as an exact reviewed diff before execution. They are not authorized by draft PR permission.

## Required verification after scope is established

Anonymous/non-admin/userA/userB/revoked-admin denial; admin permitted fields only; stale edit conflict; malformed/missing target; length/normalization; field preservation; avatar namespace/MIME/size/references and rollback; mobile/light/dark UI and focus; no direct user-row write from browser. Use synthetic local fixtures before any separately authorized live check.
