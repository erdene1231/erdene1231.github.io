# Native Input/Output block subtypes

All three selected Library JPEGs were materialized with current Library helpers
into consumer-local paths, byte-verified and viewed as pixels before selecting
any content. Their screenshots show CP Classes (`task-751`): its symbolic input
format and consecutive sample input/output blocks display generic `text`
toolbars. The image identity/byte hashes are in
[the inventory](atcoder-io-format/inventory.json); original screenshots remain
local and are not copied into the repository or back to Library.

The existing tutorial editor's **Кодын төрөл** selector has actual `Input` and
`Output` values. These are `type: "code"` blocks with `language: "Input"` or
`language: "Output"`; the existing native reader renders dedicated I/O panels.
No renderer imitation, HTML replacement, editor redesign or migration is needed.

Fresh live/public inventory contains51 native AtCoder statements, all revision2.
All51 share this formatting issue. The reviewed change affects exactly678 code
blocks across MN/EN:102 input-format blocks,288 sample inputs and288 sample
outputs. Final subtypes are390 Input and288 Output. No output-format code blocks
exist; output descriptions are explanatory prose and remain unchanged. All
other prose, examples, constraints, text characters, spaces, tabs, line breaks,
blank output, source provenance, problem metadata and relationships stay exact.

The exact current before-images and subtype paths are under
[atcoder-io-format](atcoder-io-format). Only `code.language` changes inside the
document; ordinary shared revision/timestamp and `edit` history advance once
per target. All1,013 other problem rows, the problem allocator,74 stored/73
public tutorials, eight private drafts and protected learner/profile/access
state remain outside the write scope. Historical migration038 and previous
problem histories996–1100 must never be replayed.

The generated SQL uses a pinned path allowlist, fresh whole-catalog/history and
target body/revision guards, exact expected PostgreSQL body hashes, native
validation, transactional rollback and postconditions. It updates no source
provenance and inserts no problem. Source, native editor/reader tests, live
publication/readback and final receipt results accompany this focused fix.

Validation passed: six targeted Node checks;204 actual-app MN/EN/mobile/desktop
reader cases covering1,356 native I/O panel instances; all678 actual native
Code subtype selector changes and51 serialize/save/lazy-reload roundtrips.
Input/output clipboard values retain exact literal whitespace. The separate
1,064-row rehearsal preserves all1,013 unrelated rows, every text value and the
allocator, and rolls back an injected failure after25 edits. The corrected CP
Classes mobile I/O panel pixels were inspected. No frontend or schema change.

The separately authorized independent Statement/Editorial controls and original
51-editorial request is retained in
[ATCODER-FOLLOWUP-CHECKLIST.md](ATCODER-FOLLOWUP-CHECKLIST.md). That phase begins
after this I/O fix has its own publication receipt.
