# EGOI problem links

The requested source is https://oj.uz/problems/source/egoi. On 2026-10-31 the
source root, every linked year (2022–2026), and all 36 matched individual problem
pages were opened through the web tool. The five complete year listings contain
38 tasks and display both competition days followed by their footer; none has
pagination controls or further page links. No denied resource was bypassed.

The live catalog contains 45 EGOI tasks. Exactly 36 have verified matches, and all
36 currently require a URL change; zero are already correct. Nine tasks are
absent from this source and retain their existing URLs: Number of Zeros,
Shopping Fever, Luna likes Love, Railway, Twin Cookies, Lanterns, Angry Cows
(all 2021), Garden Decorations (2024), and Census (2026). Team Coding and Make
them Meet appear on oj.uz but have no existing catalog record and are not added.

The exact identity evidence and before/after URL allowlist are in
[egoi-ojuz/manifest.json](egoi-ojuz/manifest.json). Infinite Race is explicitly
matched to `EGOI24_infiniterace2`, the actual linked alias; its catalog ref lacks
the final `2`. SubsetMex/Subset Mex, Padel Prize Pursuit/PPP and Carnival
General/Carnival use their shared year and task identifiers. Catalog names and
refs stay unchanged.

Configured clients read the authoritative Supabase `get_catalog()` RPC.
`problems.json` serves unconfigured offline clients; its three matched entries
are synchronized. Historical seed SQL and completed import/publication receipts
are not edited or replayed. The manifest is the reviewed repository
representation of the complete live URL update.

`tools/egoi_url_job.mjs` generates a single operator maintenance statement.
It requires fresh whole-catalog/history fingerprints, each target body hash and
revision, owner execution without an Auth identity, unchanged protected data,
authority, sequence and sources, and absence of unexpected catalog/history
triggers. Every update changes only `body.url`, advances the normal revision and
timestamp, and appends an `edit` history record with exact previous/next bodies.
The statement verifies all 1,010 identities and unrelated fields before commit.
Failures roll back the statement; a submitted operation must never be retried
without inspecting its live outcome.

Validation: 14 focused tests pass, covering verified identity mapping, supported
catalog parsing and relationships, unchanged absent/fallback tasks, URL field
scope, history, stale revisions, protected drift, allowlist tampering, rollback
after 18 updates, and replay rejection. A separate rehearsal uses all 1,010
freshly captured production problem rows and current live validator definitions.
Publication/readback/deployment results are recorded in the final receipt.
