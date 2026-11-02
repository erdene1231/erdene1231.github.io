# JOI native MN/EN statements — verified release

All **24 existing JOI problems** now have published native MN/EN statements:
**48 language versions**, with **332 actual Code Input/Output blocks** (172 Input,
160 Output). No editorials were added. The catalog remains 1,064 problems;
75 have native statements and the original 51 native editorials remain unchanged.

The earlier URL release is also closed: **16 changed to verified individual
oj.uz pages, 4 already correct, 4 unmatched 2015 links retained**. See the immutable
[URL evidence](../joi-ojuz/README.md) and [URL receipt](../joi-ojuz/publication-receipt.json)
(PR249/250). Statement publication preserved every approved URL and all ratings,
priorities, tags, titles, IDs and learner references.

Example: [Unique Cities — native MN/EN statement](https://erdeneclub.com/#problem/task-899).
The actual stable route, anonymous revision 3 and existing Low priority are
verified; the reader is visible without opening hints.

The table reconciles actual committed revisions and history IDs. Full current
body/document/provenance hashes are in [final-state.json](final-state.json), with
the exact reviewed native documents in [statement-plans.json](statement-plans.json).
All 1,040 unrelated catalog rows and the prior 51 statement/editorial pairs are
exact. No migration, permission, RLS, credential or allocator change occurred.

| ID | Existing catalog title | Statement revision | History | URL decision |
| --- | --- | --- | --- | --- |
| 720 | JOI 2018 — Commuter Pass | 1 → 2 | 1232 | already-correct |
| 721 | JOI 2019 — Coin Collecting | 1 → 2 | 1237 | already-correct |
| 722 | JOI 2017 — Long Distance Coach | 1 → 2 | 1227 | already-correct |
| 723 | JOI 2021 — Growing Vegetables is Fun 4 | 1 → 2 | 1238 | already-correct |
| 880 | Railroad Trip | 1 → 2 | 1219 | retain-unmatched |
| 881 | Cake 2 | 1 → 2 | 1220 | retain-unmatched |
| 882 | JOI Park | 1 → 2 | 1221 | retain-unmatched |
| 883 | Ball | 1 → 2 | 1222 | retain-unmatched |
| 884 | Oranges | 2 → 3 | 1223 | change-url |
| 885 | Collecting Stamps 2 | 2 → 3 | 1224 | change-url |
| 886 | Train Fare | 2 → 3 | 1225 | change-url |
| 887 | Territory | 2 → 3 | 1226 | change-url |
| 888 | Foehn Phenomena | 2 → 3 | 1228 | change-url |
| 889 | Semiexpress | 2 → 3 | 1229 | change-url |
| 890 | Kingdom of JOIOI | 2 → 3 | 1230 | change-url |
| 891 | Soccer | 2 → 3 | 1231 | change-url |
| 892 | Stove | 2 → 3 | 1233 | change-url |
| 893 | Art Exhibition | 2 → 3 | 1234 | change-url |
| 894 | Dango Maker | 2 → 3 | 1235 | change-url |
| 895 | Snake Escaping | 2 → 3 | 1236 | change-url |
| 896 | Bitaro the Brave | 2 → 3 | 1239 | change-url |
| 897 | Exhibition | 2 → 3 | 1240 | change-url |
| 898 | Growing Vegetables is Fun 3 | 2 → 3 | 1241 | change-url |
| 899 | Unique Cities | 2 → 3 | 1242 | change-url |

## Sources and rights

All 24 primary sources were captured: 23 original Japanese AtCoder task pages and
the original JOI 2017 Day 3 English PDF for Long Distance Coach. The 80 sample
pairs comprise 77 literal HTML `pre.text_content` pairs and 3 visually inspected
Coach PDF table pairs. HTML spaces, codepoints, newlines and terminal newlines
are retained. The PDF table adaptation explicitly uses one ASCII space between
printed numbers and LF rows with a terminal LF; it is not claimed to be raw
PDF-byte equivalence. Coach pages 1–4 of its 13-page bundle were rendered and
viewed. Unique Cities' canonical English PDF pages 1–4 were also viewed: page 2
visibly prints `A_i ≠ B_i`, lost by HTML/PDF text extraction. The exact PDF URL,
hash, page and visual clarification are retained in provenance and
[unique-cities-source-clarification.json](unique-cities-source-clarification.json).

The [original JOI archive](https://www.ioi-jp.org/problem_archive) explicitly grants
CC BY-SA 4.0 for the covered Final Round and Spring Camp years.
[rights.json](rights.json) retains the exact original grant and covered years.
Every document visibly credits the Japanese Committee for IOI, links its source,
grant and license, and identifies our translation, condensing and restructuring
as an unofficial adaptation. CC BY-SA 4.0 applies to the adapted statement
content only, not unrelated application code or catalog metadata.

Each task has a source-fact checklist for operations, objective, inequalities,
full/subtask bounds, I/O and samples. These are actual tutorial-schema editable
blocks with MathJax, task/input/output/constraint/example/source sections and
Input/Output code subtypes. The extra 12 Input blocks preserve six source input
formats in both languages. No solution or algorithm explanation was added to the
application statements.

## Verification and preservation

- 445/445 Node aggregate after the narrow provenance-preservation editor fix;
  12 final targeted native/backend/atomic cases cover all five batches. The broad
  aggregate was not repeated for pure content changes.
- 24 distinct actual native editor round trips and 96 reader combinations:
  MN/EN at 375 px light and 1,200 px dark. Actual admin Statement actions retain
  license/source metadata. The dual-document fixture also preserves sibling
  editorial/metadata drafts, undo-capable components and external CAS conflicts.
- All 80 official sample pairs and 446 bounded independent oracle/edge checks
  pass with `python3 tests/joi-statement-samples.py`; see
  [all-sample-verification.json](all-sample-verification.json). This checks task
  mathematics and examples, not full-constraint solution performance.
- Every batch used fresh full-body/revision CAS, immutable allowlists, current
  protected/authority/policy/history/allocator fingerprints, a single atomic
  transaction, exact anonymous all-24 readback and default-TLS deployed bytes.
  Midway rollback, stale/allowlist/protected drift and replay rejection are tested.
- A genuine learner-progress change between batches 03 and 04 was captured in the
  new fresh guard and preserved. Older progress was never restored. All other
  protected tutorial/draft/learning/profile tables remain exact; each batch also
  preserves its fresh current progress fingerprint.
- Canonical 45-second client read timeouts in batches 01, 04 and 05 were resolved
  by read-only active-job/history/body inspection. No transaction was resubmitted.

Browser Auth/RPC are isolated synthetic fixtures using the actual components
and bundled MathJax; installed backend validation is tested locally. Production
anonymous records and deployed bytes were independently checked over default TLS.
No authenticated real-user mutation or browser interaction is claimed.

## MathJax compatibility closure

The final actual-data route fixture exposed two renderer module instances
(`tutorials?v=87` and `?v=84`), each appending a MathJax bootstrap element. The
second execution threw a Package getter TypeError. The version-only
[PR260](https://github.com/erdene1231/erdene1231.github.io/pull/260) unifies all
consumers and entry caches at version 94. Pages **41383035015** succeeded, with
all 10 changed runtime/config/audit assets byte-exact over default TLS.

The actual app-entry regression now asserts one renderer module, one MathJax
script element and zero page errors. The real captured Low-priority example
passes four bilingual mobile/desktop cases. Thirteen targeted Node cases and
current Statement (24 reader/6 editor), Editorial (12 reader/3 editor), tutorial
math (4 layout cases) and dual-document actions (5 groups) pass. No rendering
algorithm, content, backend, permission or schema was changed. Evidence is in
[mathjax-module-fix.json](mathjax-module-fix.json),
[mathjax-fix-publication.json](mathjax-fix-publication.json) and
[public-example-flow.json](public-example-flow.json). This is an actual app/config
fixture with captured anonymous data and synthetic read-only transport; it is not
a live authenticated browser or production-pixel claim.

## Release receipts

| Batch | Source PR | Receipt PR | Statement histories |
| --- | --- | --- | --- |
| 01 | [251](https://github.com/erdene1231/erdene1231.github.io/pull/251) | [252](https://github.com/erdene1231/erdene1231.github.io/pull/252) | 1219–1222 |
| 02 | [253](https://github.com/erdene1231/erdene1231.github.io/pull/253) | [254](https://github.com/erdene1231/erdene1231.github.io/pull/254) | 1223–1226 |
| 03 | [255](https://github.com/erdene1231/erdene1231.github.io/pull/255) | [256](https://github.com/erdene1231/erdene1231.github.io/pull/256) | 1227–1231 |
| 04 | [257](https://github.com/erdene1231/erdene1231.github.io/pull/257) | [258](https://github.com/erdene1231/erdene1231.github.io/pull/258) | 1232–1236 |
| 05 | [259](https://github.com/erdene1231/erdene1231.github.io/pull/259) | Final receipt pending merge | 1237–1242 |

Individual `batchNN-publication-receipt.json` files retain exact guards, SQL/plan
hashes, source merge/Pages runs, anonymous readback and deployed asset evidence.
No target or source blocker remains. Never replay the successful publication SQL.
