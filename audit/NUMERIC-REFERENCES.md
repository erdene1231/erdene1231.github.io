# Numeric problem references and exact number search

PR14 now includes the complete v36 graph. Shared main/modal search matches #1 or
#001 exactly to catalog number1, not10/100. Popup rows show #number. Rating-band
controls are removed from both main and popup; Min/Max rating remain.

New popup choices store the problem number as a string key (e.g. "1") in embedded
problemKey and learningRelations.practice[].key. Editor clones normalize known old
references to current catalog numbers, including valid private relation JSON.
Priority/stage/reason metadata is preserved across conversion. No global catalog
or curriculum/progress ID is renumbered. Legacy source|ref references remain
readable aliases for historical lessons, drafts, plans and checked-in curriculum.
Existing published bodies are not mass-rewritten; subsequent admin authoring saves
normalized numeric references. Unknown references are preserved for explicit repair.
Reader resolution maps numeric keys to original problem IDs so progress stays intact;
reverse lesson links also resolve both formats. Default new problem blocks require
an explicit selection rather than silently linking a default source task.

Fresh actual metadata matched after028 across schema/constraints/indexes/RLS/
functions/triggers. Only missing029_numeric_problem_references was applied as
20261026100333. It updates the extended-block shape validator and publication
lookup to accept numbers while retaining old references. Unknown numeric practice
or embedded targets are rejected; the original prerequisite/body validator, actor,
CAS, deleted-ID/media guards and ACLs are unchanged. Two baseline function hashes
guard replay. No content/progress DML is in this migration.

Actual before/after hashes and counts are identical:748 problems/56 tutorials.
The first migration-history read timed out after successful installation; only the
read was retried in a fresh session. History confirms029. No migration was replayed.
Fresh after029 metadata matches repository reconstruction with zero differences.
See NUMERIC-REFERENCES-APPLY/HISTORY/FINGERPRINTS.json and production-after-029.json.

Verification:16 Node test files, numeric alias/SQL tests,16 editor Chromium groups
and11 popup groups pass. Includes exact #1 modal lookup, missing Rating dropdown,
bulk748 number-key insertion/Undo, metadata preservation, old/new SQL compatibility,
unknown numeric rejection and stable IDs. Browser uses synthetic Auth/RPC/catalog;
live authenticated frontend remains unverified. No real content was published,
deleted or renamed for testing.

Review/merge PR14, deploy completev36. Do not replay021-025/028/029. Pending026/027
remain unapplied. Pending026 currently assumes legacy source keys and must be
re-audited/adapted for numeric references before installation; it is not an apply queue.
