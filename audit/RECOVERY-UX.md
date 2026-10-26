# Recovery choice repair after PR 10

Base main: fa44b9880b86a83619981735f8a49ec3ca570bdc (PR 10 merged).
Branch: codex/fix-recovery-choice. Next numbered feature remains 010/026.

The user's screenshot shows a real usability failure: a stale local draft clears
current draft, comparison locks the form, but the empty form stays visible and
all choose controls are hidden inside closed JSON details. Backup is also locked
inside that form. The previous regression only checked attached selectors and
missed whether recovery could actually be completed.

The empty form is now hidden until a draft is opened. Recovery sits before the
editor, with visible title/summary cards and select buttons for local, online draft
and published content; JSON details are optional. A separate explicit save opens
the selected private draft in the actual editor. Backup is available immediately.
Cancel leaves visible resume/download actions and enables tutorial navigation/new.
Stale save errors provide a reload-comparison action with a new document read.
No version is selected automatically; draft/publication counters are labelled as
separate. Before-rebase backup must succeed before sending a mutation.

Conflict detachment no longer persists an older current session over a newer
localStorage candidate written by another tab. Other invalidation paths retain
normal backup persistence. Actor/generation/CAS checks are unchanged.

Validation: 41 Node cases across 11 files; 9 new Chromium recovery cases plus 30
existing editor/reader/media groups PASS. The screenshot state is reproduced with
synthetic local revision 1, online draft 2, published 5. Each choice goes through
explicit rebase -> populated editable form -> continued edit/save with revision 3
and base 5. Backup download, postpone/resume, stale CAS, storage failure and late
logout responses checked. 375/1200px screenshots inspected. Historical audit
outputs preserved; current outputs named RECOVERY-*.

No production database calls, migrations, content publication or upload in this
repair. Browser Auth/RPC/Storage are mocked. Live authenticated user-session
verification remains unperformed. Deploy the complete v32 import graph after
merging; do not replay migrations 021-025. Original local and live content are
never discarded automatically. Source requirements remain partially verified;
this repair does not mark the entire editor or project complete.
