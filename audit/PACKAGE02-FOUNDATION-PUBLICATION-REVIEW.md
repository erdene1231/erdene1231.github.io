# Three completed tutorial candidates: publication review

Binary Search, Greedy and DP now have complete local MN/EN candidates against all 15 content criteria and 20 semantic review items. This is **3 content-ready candidates, 0 production publications, 52 other curriculum lessons remaining**. Mongolia is excluded and completely unchanged.

The candidates use native structured blocks. Existing section indices 0–13 are preserved; the six-stage practice/mastery chapter is appended at index 14. All previous fallback practice identities and all variants/next/prerequisite/related links remain. The new explicit local core selection intentionally replaces the previous fallback star requirements. Stored solved/read/self-check records are not reset; derived mastery can reflect the revised core selection. Bank-wide problem priorities are untouched.

## Verified

- 98 Node tests pass on the final batch, including exact native publication serialization and isolated SQL draft-save → publish → reload using function definitions matching production.
- The three C++ programs are byte-identical to the 199 independently tested cases already recorded. Exact raw digest assertions permit that result to be reused; no changed program is credited with an old test result.
- 12 actual renderer/MathJax views, three native block editor edit/serialize/reload checks and all rendered practice-card actions/internal lesson links pass. Three MN mobile screenshots were visually inspected.
- Current Supabase publication validators accepted all three candidates read-only at 2026-10-28 00:46:49 UTC. No migration is required.
- Fresh target bodies remain revision 5/published. Mongolia remains revision 2/unpublished. The one Binary Search private draft differs only by a relationship-form field equivalent to the current fallback; it will be preserved unchanged.

See `PACKAGE02-FOUNDATION-LESSONS-REVIEW01.json`, `PACKAGE02-FOUNDATION-PRACTICE01.json`, `PACKAGE02-FOUNDATION-LESSONS-BROWSER01.json` and `PACKAGE02-FOUNDATION-PUBLISH-BATCH01.json`.

## Exact remaining publication decision

The existing Supabase SQL connection works, but its app-user context is absent and `is_admin()` is false. The supported authenticated tutorial publication RPC requires a real app-admin actor and private draft. No failing publication RPC was invoked, no app identity was forged, and no credentials or permissions were changed.

A separate, **unexecuted** owner maintenance statement has been prepared for explicit execution review. It does not reuse the old 245-problem maintenance approval.

- Private executable: `/workspace/package02-foundations-live/owner-publish-foundations-PROPOSED.sql`
- Size: 147612 bytes
- SHA-256: `55287149f786c5d607035acb62f4322f197b33f59e2b3e6b9530dd2963a6ad33`
- Only targets: `binary-search`, `greedy`, `dynamic-programming`; each revision 5 → 6, remaining published.
- Uses the existing database owner connection and explicitly requires no app-user impersonation. No new RPC/function/table/grant/RLS/Storage/Auth change.
- Pins actual target body hashes, revisions/status, seven function definitions/ACLs, publication triggers and the reviewed private-draft fingerprint. It validates all bodies and locks all targets before any update.
- Updates only the three tutorial bodies/revisions/publication timestamps. Maintenance attribution is NULL, never a forged user. Inserts exactly three history records containing the old and new bodies.
- Preserves every private draft unchanged, including its existing base revision; subsequent editing can require the normal conflict/rebase flow. It does not delete or rebase drafts.
- One atomic DO statement aborts on drift or any late failure. Non-target tutorials including Mongolia and all prior history are checked unchanged. Sequence gaps can remain after a failed transaction.
- Isolated tests verify successful exact bodies/history, replay rejection, draft-drift rejection, injected late-failure rollback, and preservation of drafts, Mongolia, the entire 993-problem fixture and learner records.

Before any approved execution, capture fresh scoped recovery and recheck these pinned guards. After an uncertain outcome, inspect actual revisions/body hashes/history before any retry. After success, verify exact bodies/relationships through the public read path and renderer. Until that happens, report these lessons as ready locally, not live.

Other lesson authoring and the independent interactive/communication inventory can continue while this publication route awaits its specific decision. No new problem statements/editorials or package 3 work is authorized.
