# Tutorials loading regression

Fresh anonymous public responses:76 tutorials,5,287,266 bytes and the actual1,002,059-byte problem-catalog object. Every published tutorial passes the current native validator. No current public body needs historical edition substitution.

The configured library unnecessarily awaited both the legacy2MB offline seed and `loadLearningContent()`, which now includes the1.3MB100-day plan. With either unrelated request stalled, a successful public tutorial RPC could not render the list. The source also left “Loading the tutorial library” visible after a successful list render. The latter was directly observed with the real SDK/public payloads; the dependency stall was reproduced by holding the unrelated requests. This does not prove which specific request stalled on the reporter's device.

Fix:configured libraries accept complete authoritative bodies directly and retain hardcoded verified handbook ordering. They neither download the offline seed nor await the course. The offline path retains its existing seed/edition behavior. Clear loading state upon acceptance and mark live readiness only after successful acceptance. No content, records, schema, access or quiz behavior changes.

Regression uses the actual current Supabase SDK, captured anonymous RPC bytes and real app routes, without successful synthetic catalog/schema stubs. Baseline commit dec16b24:0 cards while course/seed are held. Fixed:76 cards, empty loading message, old Complexity and new C++ routes render in normal and held-course cases; RPC503 yields an explicit error. Desktop/mobile widths tested. Hashes and exact evidence are in baseline.json/fixed.json. No production mutation. Live browser certificate denial remains; it was not bypassed.

The seven-module reverse import closure uses97 consistently, preserving one MathJax loader/queue. Native all100-day/quiz/editor roundtrips and aggregate checks are rerun. Deployment status is reported after merge; no SQL or migration is used for this repair.
