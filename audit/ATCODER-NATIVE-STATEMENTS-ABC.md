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
adds an owner-private validator. Existing table/RPC privileges, policies, RLS,
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

Live schema installation, atomic publication, anonymous readback and deployed
asset verification are recorded in the publication receipt after execution.
