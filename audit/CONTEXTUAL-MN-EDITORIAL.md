# Contextual Mongolian editorial review — 73 current public lessons

All 73 current published lessons were read in Mongolian and English by GPT Astra with high reasoning. The review compared prose with its actual mathematical conditions, code and examples. It proposes 615 exact-path edits in 540 string fields across 72 lessons. DSU was reviewed and needs no change. This is a new editorial pass; the earlier package 3 completion ledger remains historical evidence.

The complete [lesson ledger](contextual-mn-editorial/ledger.json), [before/after fields](contextual-mn-editorial/changes.json) and [individual edits with reasons](contextual-mn-editorial/edits.json) distinguish changed and unchanged lessons. Candidate files retain native document structure and English counterparts. Publication is separately recorded by a receipt; this source review does not itself claim publication or owner acceptance.

## Sources and precedence

All three supplied Library files were materialized through the supported consumer-local transfer, byte-verified and read completely: Pasted text (4), 477 logical lines; (5), 221; (6), 127. Exact filenames, byte lengths and SHA-256 values are in [attachments.json](contextual-mn-editorial/attachments.json). They supplied the general editorial standards and historical Introduction/complexity findings. Each finding was checked against the fresh public bodies, rather than assuming the older criticism still applied.

The user's latest terms take precedence: үл буурах / үл өсөх permit equality; эрс өсөх / эрс буурах exclude it. Strict comparisons use эрс бага / эрс их. Rounding uses тоймлолт / тоймлох, with Доошоо тоймлох and Дээшээ тоймлох for floor and ceil; truncation removes the fractional part toward zero. Approximation remains ойролцоолол. The review distinguishes exponent, power, degree and graph/card uses of зэрэг, and recurrence formulas from recursive algorithms. Familiar algorithm names remain where helpful.

The added C++ `std::round` half-away-from-zero explanation is checked against [Microsoft's C runtime documentation](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/round-roundf-roundl?view=msvc-170). The requested examples are `std::round(2.5) = 3` and `std::round(-2.5) = -3`.

## Examples of contextual corrections

| Lesson | Before | Result and reason |
| --- | --- | --- |
| Introduction | Floor/ceil were only described by inequalities; rounding/truncation distinction was incomplete. | Named floor/ceil directions, truncation toward zero and the two requested round examples, preserving every existing example. |
| Complexity | Descriptions conflated increment operations, arithmetic cost and a Kadane state. | Describe what the actual operations and state mean, with specific practice guidance in both languages. |
| Sorting and binary search | Generic өсөх and “small index” wording could imply the wrong equality or object. | Non-decreasing arrays allow duplicates; comparisons concern element values, with the returned index named explicitly. |
| SCC | IDs “increase along original edges.” | They strictly increase only across different components; within a component the IDs are equal. Both languages now say this. |
| Aho–Corasick | BFS depth “increases”; output traversal was ambiguous after a terminal node. | Depth is non-decreasing; follow output links whether the starting node is terminal or not. |
| Tree DP | Children partition “all vertices except u.” | They partition the vertices of u's subtree, excluding u. |
| Number theory | Euler cancellation sounded like subtraction; exponent reduction was imprecise. | Cancel the coprime factor and reduce the exponent modulo the stated value, with the original conditions and formulas intact. |
| String hashing / lazy segment tree | A normalized residue was described as positive. | It is nonnegative, so zero is included. |
| Lazy segment tree | Padding to the “nearest” power of two. | Use the smallest power of two at least as large as the original size. |
| DP optimizations | A minimizing split index was called the minimum value. | Distinguish the split index from the objective value, including rightmost tie handling. |
| Debugging | Counterexample reduction called an accepted reduction a “repair.” | Call it a simplification; global minimality is still not claimed. |
| Interactive communication | An inline code span contained a literal newline. | Display the intended `\n` escape in MN and EN; executable programs are unchanged. |

## Preservation and validation

The fresh baseline contains 73 public lessons / 74 stored rows, 8 private drafts, 1,010 problems and 285 tutorial history entries. A second prepublication read confirms all 72 target bodies and revisions still match the reviewed baseline.

Recursive comparison preserves object keys, array lengths, section/block order, IDs, priorities, practice identities/stages, native rich-span marks and all unedited fields. It confirms byte-for-byte preservation of **2,498 executable code blocks**, **362 display-formula blocks**, **770 diagrams** and the numerical data in **410 tables**. Byte equality also proves executable token and operator equality. All 241 unique complete C++17 programs match the exact source hashes of the prior successful compilation; this pass does not claim to have newly compiled them.

[15 explicit math/numeric exceptions](contextual-mn-editorial/math-numeric-exceptions.json) cover the requested round examples, English spelling of index bases, explicit `x` operands and removal of a misleading prose `m` variable. Existing equations, constraints, worked answers, example values and executable comparisons are preserved. The only changed code-marked inline spans are the two displayed newline escapes; neither is an executable block. Diagram labels were separately reviewed and kept intact.

Native model/publication-adapter checks cover all 73 bodies and preserve supplemental relationship metadata. Existing mathematical-prose scanner exceptions are compared with the baseline; no new scanner warning is accepted. Existing English problem titles using Roman `I`, search aliases, legitimate recursive descriptions, graph degree, card rank, polynomial degree and powers are retained contextually.

The local browser checks cover all 73 lessons in both languages at 375 px/light and 1200 px/dark: **292 reader cases** with MathJax, TOC navigation, practice controls and overflow checks, plus **146 actual native editor input/save/reload/reader round trips**. A final narrow wording correction in lazy segment tree receives four additional reader cases and two editor round trips. These are local current-runtime fixtures, not authenticated live-user acceptance. The known live Chromium certificate limitation is not bypassed.

The SQL regression runs all 72 candidates in **24 batches of three** through the existing publication validators. It checks atomic rollback after an injected late failure, stale catalog/draft guards, replay rejection, exact reviewed hashes and preservation of synthetic private drafts, the unchanged DSU/Mongolia rows, learner records and problems. The wrapper retains the existing 1–3-target limit and adds the exact reviewed ledger plus whole-catalog/all-draft guards.

Publication must use fresh body/revision, draft, function/ACL and trigger guards before each transaction, with scoped recovery and one-time intent/result files. Only changed published lessons are targeted. A later receipt records actual revisions, history IDs, exact anonymous public-body verification and protected-state/deployment checks. No migration is required. The three deferred UI/progress items remain outside this pass.

The complete Node suite passes: **365 tests, zero failures**. See [verification.json](contextual-mn-editorial/verification.json) for the bounded validation receipt.
