# Explicit tutorial reading activity

This release adds separate Viewed and Complete reading controls to the actual
native tutorial reader in full and section modes, including lessons without
curriculum relations. Reading completion is independent of mastery checks and
practice solves. Opening a lesson, changing language, navigation and ordinary
saves do not create activity events.

The existing authenticated owner-only learning_records save route remains in
use. Migration040 adds two private SECURITY INVOKER trigger helpers and two
triggers, without tables, grants, RLS changes, public RPCs or existing-row writes.
The feature flag remains0 until installation and unchanged-data/access readback
are verified, then a receipt release enables version1.

An explicit click carries a stable event ID. The server accepts the event on the
actual insert/update, removes the intent, and stamps UTC activity times. A first
incomplete-to-all-sections-read transition records completedAt. Existing full-read
records without a date remain undated. Checks and all unrelated/unknown values
are preserved. Reading intents preserve current server checks/unknown fields and
merge section additions; intentional edits made while the same save is pending
remain explicit. Concurrent final-section additions can complete reading without
losing either section. Explicit viewing records viewedAt and a distinct Ulaanbaatar
viewedDays entry, so a later revisit does not erase an earlier week's activity.
No historical view day is inferred from readSections, checks or updated_at.

Known event IDs are idempotent even after an uncertain response. A new intent
older than ten minutes is rejected, preventing an old queued interaction from
being silently counted as today's activity; another explicit click can renew an
expired request. A fresh committed own-user row is read after upsert before the
store reports success, because an AFTER-trigger update is not reliably reflected
in the outer RETURNING row. Returned data merges only for the same account,
generation and unchanged pending object. Load failures do not enable dated
activity controls, and failed saves remain queued locally.

Verification includes synthetic model/store/SQL and actual native-reader browser
paths, plus independently overlapping sessions in an isolated PostgreSQL17.11
container with network none and no ports. The real PostgreSQL test observes lock
contention for concurrent insert/update intents, demonstrates stale RETURNING,
and verifies fresh readback, unchanged table grants/RLS, private helper EXEC
denial, legacy unknown dates, same-event retries and migration data preservation.
No real-user fixtures are written. Browser transport is synthetic; no
authenticated live-user browser claim is made.

The full1064-row schema rehearsal preserves all51 statement/editorial documents,
metadata/revisions/history, allocator and synthetic protected records. Fault
injection after DDL rolls the helpers/triggers back; stale catalog guards reject
before installation. The release's shared Node aggregate is recorded separately.

Other profiles' private tutorial dates are not exposed by the existing public
profile RPC. Later weekly/report UI must preserve that boundary and use actual
own-user dates, with unknown/private data labelled honestly. The other five UI
items and source-blocked olympiad URL resolution remain in the task checklist.

The refreshed aggregate passed430/430 tests across150 files in4m57s with
frozen source. A final isolated midnight adjustment was then covered by13
targeted model/store/guard tests, actual PostgreSQL contention/RLS checks,
the1064-row rehearsal and the native browser suite. New section clicks and
new Mongolia days use new intent IDs; retries retain IDs. The server captures
one accepted timestamp for both UTC time and Mongolia day. See
final-040-validation.json for exact changed-file hashes and scope.
