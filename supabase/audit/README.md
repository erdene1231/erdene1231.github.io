# Production reconciliation — 2026-10-26

Production was read through the session-aware HTTPS MCP client. No user records
were fetched. Initial baseline: `problem_catalog = 748`, `tutorial_catalog = 55`,
`list_migrations = []`. An empty history was not treated as an empty database.

## Comparison

`catalog.sql` captures public/study_private metadata, the app's auth trigger and
three avatar storage policies. `production-2026-10-26.json` is the pre-change
snapshot; `production-after-021.json` is the post-change snapshot.

The repository's schema.sql and numbered SQL files were reconstructed as DDL/ACL
in an isolated PGlite PostgreSQL instance with minimal auth/storage mocks and
Supabase default grants. No historical scripts were run against production.
The offline tool skips seed DML, DO blocks and application RPCs. This is a schema
comparison, not a content equivalence check or a full Supabase integration test.

Compared: 18 tables, 6 sequences, 1 view, 116 columns (including view columns),
83 PK/FK/unique/check constraints, 27 indexes, 19 RLS policies, 45 functions,
3 triggers, RLS flags and object ACLs. Column type, nullability, defaults and
identity settings were included. PostgreSQL 18's separate NOT NULL constraint
entries are excluded from constraint-name comparison; nullability is checked
through column metadata. Function CRLF/LF line endings and ACL ordering are
normalized; function bodies are otherwise compared in full.

The only substantive difference was missing optional `prerequisiteIds` validation
in `public.validate_tutorial_body(text,jsonb)`: array type, maximum 30 IDs, string
type and lowercase ID pattern. All other compared categories matched.

## Applied change

`021-tutorial-prerequisite-validation.sql` replaces only that function, retaining
its signature and privileges. It contains a baseline fingerprint guard to reject
unreviewed concurrent changes. No seed, row update, schema reset or historical
migration replay was performed.

MCP apply_migration returned `success: true`; history now contains:

- version: `20261026045125`
- name: `021_tutorial_prerequisite_validation`

Post-apply counts remain **748 / 55**. A second metadata snapshot confirms only
`validate_tutorial_body` changed. `comparison.json` reports zero remaining
schema differences. `comparison-before.json` records the original difference.

## Verification and reproduction

```sh
python -m unittest discover -s tests -p test_supabase_mcp.py
node --test tests/supabase-reconciliation.test.mjs
node tools/compare_supabase_schema.mjs
python tools/supabase_mcp.py
python tools/snapshot_supabase_schema.py /tmp/new-production-schema.json
```

Offline tests check per-process initialize/session propagation, absence of
credentials in logs, the client's restricted default tool access, invalid and
valid prerequisites, all repository tutorial payloads, ACL preservation and
unchanged existing fixture data. Production verification used metadata and
aggregate counts only; no test fixtures were inserted into production.

## Cloud availability

The current managed environment reports the network policy enforced and both
runtime bindings ready. `/workspace/shared/supabase_mcp.py` and
`/workspace/shared/start/SKILL.md` exist, and the canonical copies are tracked in
`tools/` and `start/`. `AGENTS.md` routes future repository tasks to the skill.

Reusable environment-image inclusion and environment-level Start skill
registration cannot be verified or changed with the available status-only tools.
A future fresh task must use a checkout containing this commit; local workspace
files and a local commit do not by themselves update a remote repository or a
reusable environment configuration. No such update is claimed.
