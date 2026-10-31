# AtCoder native statements and ABC additions

The fresh catalog contains 78 AtCoder problems. Every individual task page was
inspected with the English language selected: 50 Typical90 tasks and ABC005 D
remain Japanese-only; all 26 Educational DP tasks and ABC203 D already provide
English. The bounded statement scope is therefore exactly 51 existing problems.
All 54 selected new ABC pages provide English, so they retain their official
links without redundant authored statements. The final catalog target is 1,064
problems, including 132 AtCoder tasks.

The inventory and bounded workload were reported before prolonged authoring.
An initial HTTP 429 stopped the parallel fetch immediately. After a cooldown,
the same ordinary client resumed sequentially at four-second intervals; all
78 existing and 54 new individual pages were obtained successfully. A separate
ABC092 listing was rate-limited and its candidate was replaced by ABC140 D.
Historical shared ABC/ARC aliases were resolved through actual contest links,
including `arc089_a`, `arc092_a`, `arc094_a`, `arc095_b`, `arc096_a`, `arc097_a`,
`arc098_b`, `arc099_a`, `arc100_a`, `arc101_a`, `arc102_a` and `arc103_a`.
No identity, proxy, host or TLS workaround was used.

## Native documents and rights

[AtCoder's terms](https://atcoder.jp/tos) reserve rights in service content;
public availability is not a blanket license to reproduce or translate its
stories. The site documents are independently worded factual mathematical
restatements, attributed as **Original functional restatement**, with direct
source links, source HTML hashes and bilingual semantic/rights review records.
They do not reproduce the expressive source narratives or claim to be official
translations. Complete source HTML stays in the local evidence directory.

Forty-two previously authored repository documents are reused only after
comparison with fresh authoritative pages: every complete normalized task text
matches the prior captured page. The 42 document bodies are unchanged, and all
135 numeric input/output sample pairs match the fresh source exactly. Their
provenance receives the current source hash and review date. None comes from
the eight private tutorial drafts, which remain outside this task.

Nine remaining documents were independently authored for Cluttered Paper, Long
Bricks, Loop Railway Plan, Magic For Balls, Two by Two, Friendly Group,
Multiplication 085, Snuke's Favorite Arrays and ABC005 D. Their task semantics,
input grammar, output, inclusive/exclusive bounds and integer domains were
checked against the Japanese task text. The final Loop Railway constraints
explicitly require an open cell. Every new example is original and independently
calculated by exhaustive or direct mathematical methods. The OR statement keeps
strictly ordered indices and the 60-bit domain; the factor triples retain
`a <= b <= c`; matrix queries retain the at-most-area bound. Unicode Mongolian,
mathematical operators and literal line breaks survive native serialization.

The actual tutorial document schema and `mountBlockEditor` component are used:
MN/EN task, input, output, constraints and examples are structured sections with
typed paragraph/math/code blocks. Documents are in
[statement-patches.json](atcoder-expansion/statement-patches.json), with scoped
public before-images in [before-targets.json](atcoder-expansion/before-targets.json).

## Compatibility and publication boundary

Optional migrations 032–034 are not replayed. Minimal new migration 038 modifies
only the existing problem validator, admin save and two catalog functions, and
adds an app-private validator (the existing postgres/service_role helper access
pattern, without anon/authenticated execution). Existing table/RPC privileges, policies, RLS,
authentication checks, stable IDs, shared revisions and edit history remain.
Native documents/provenance live inside the existing problem body; public/admin
catalog RPCs expose only `hasStatement`. The lazy reader/editor uses the table's
already-authorized, primary-key-filtered SELECT route. A real anonymous request
verified this route before activation, with no permission change.

An independent inline-statement capability enables the existing native editor;
optional editorial and bulk-import backends remain gated. The backend probe is
a guaranteed validation error before any allocator/source/catalog write. Inline
image blocks are rejected because this scope does not activate a new Storage
reference lifecycle. No new read RPC or new access grant is introduced.

The exact ABC allowlist is [abc-additions.json](atcoder-expansion/abc-additions.json).
It includes 54 individually verified, globally deduplicated tasks: 29 High,
22 Medium and three Low, with individual learning reasons and 49 distinct tags.
Ratings are explicitly rough author estimates on the catalog's CF-like scale,
not AtCoder points or official ratings. Existing ratings/priorities/tags are
untouched. Actual new IDs/numbers must come from the existing allocator.

`tools/atcoder_catalog_job.mjs` generates one pinned, fresh-guarded atomic
statement: 54 metadata creates and 51 native statement edits. It preserves every
unrelated field and row, checks all original history/protected fingerprints,
uses target body hashes/revisions, rejects canonical mirror duplicates, and
retains normal create/edit history. Failed allocation leaves gaps, which must
never be reset. Submitted SQL must never be replayed without inspecting its
actual outcome. Tutorial history through 405 and EGOI edits 960–995 stay committed.

## Validation

Thirty-eight focused Node checks pass, covering actual native SQL saves,
metadata/catalog contracts, old/new capability behavior, unchanged ACLs,
anonymous/nonadmin/archived row boundaries, document preservation/removal,
stale revisions, source/rights/sample validation, canonical mirror conflicts,
exact field scope, rollback and idempotency. The exact 1,010-row rehearsal
produces 1,064 rows, preserves all 959 unrelated rows and verifies rollback after
mutation 104 without recycling allocator gaps.

All 51 documents pass 204 actual native-reader MN/EN/theme/viewport cases with
bundled MathJax, plus 51 actual block-editor serialization/save/reload roundtrips
and an admin-flow payload save. These use synthetic Auth/RPC, not a live user
fixture. Nine original example pairs, 299 independent factor-splitting cases and
a no-cycle case pass. All 135 fresh source sample pairs in the reused documents
are exact. See the reports in [atcoder-expansion](atcoder-expansion).

Migration `038_native_inline_problem_statements` committed as version
`20261031095842`; fresh metadata confirms every existing ACL and every
table/column/index/policy/trigger/constraint/view unchanged. Only the four
intended definitions changed and the app-private validator was added.

The single content/import operation committed exactly once: 54 creates and
51 edits, history **996–1100**. The client's 45-second response read timed out;
the operation was **not replayed**. Fresh catalog, history, allocator, exact
native bodies and old-history/protected fingerprints prove the committed
result. Actual new IDs are `task-1011` through `task-1064`, allocated normally.
All 959 unrelated original rows are exact, and every original rating, priority,
tag, ID and reference is preserved. All 74 stored/73 public tutorials, eight
private drafts and tutorial history through 405 remain unchanged.

Anonymous retrieval verifies all 1,064 catalog rows and 51 exact lazy native
documents/provenance; the catalog carries no rich document payloads. Additional
actual-app route checks use these production payloads and the unchanged deployed
config: eight MN/EN/mobile/desktop cases show the real Medium ABC005 D and High
Yokan statements without hint actions. Actual target priorities remain 50 High
and one Medium. No target is Low; four explicitly synthetic Low regression
cases also pass. Mobile statement pixels were inspected. These checks do not
claim a live authenticated browser session.

Source PR [#216](https://github.com/erdene1231/erdene1231.github.io/pull/216)
merged at `22450c33d4c956f8658ff6a039d4b7a101556fc1`. Pages 41190751298 succeeded;
19 deployed runtime/JSON/config assets match with normal TLS. See the exact
[publication receipt](atcoder-expansion/publication-receipt.json) for source and
SQL hashes, actual row/history mappings, protected fingerprints, timeout
resolution and verification reports. Never replay 038 or the content SQL.
