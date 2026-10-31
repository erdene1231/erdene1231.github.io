# Conventional algorithm names — focused follow-up

GPT Astra with high reasoning reviewed the conventional algorithm and data-structure names in all 73 current public lessons. The fresh snapshot matches the completed contextual editorial release exactly. This pass changes 264 Mongolian/shared text fields in 48 lessons; 25 lessons require no naming correction. It does not repeat or overwrite the earlier general editorial review.

The user's latest names control this follow-up: **Stack, Monotonic stack/queue, Greedy, Knapsack, DP, Two Pointers, Sliding Window, Hash/Rolling Hash and Bitmask DP**. The already fully read general editorial attachment also calls for familiar names such as Brute Force, Prefix Sum, Kadane, Big-O and NP-hard. Existing suitable names are retained; this is not a request to translate all Mongolian vocabulary into English.

The [all-73 ledger](conventional-names/ledger.json) records changed and unchanged lessons, current baseline revisions and exact candidate hashes. The [field-level before/after review](conventional-names/changes.json) gives every changed path. The original [73-lesson editorial ledger](contextual-mn-editorial/ledger.json) and [attachment byte/read evidence](contextual-mn-editorial/attachments.json) remain intact as historical records.

| Before | After and context |
| --- | --- |
| Шуналтай алгоритм — сонголт ба баталгаа | Greedy алгоритм — сонголт ба баталгаа; the first paragraph still explains choosing the locally attractive option and why a proof is needed. |
| Үүргэвчийн DP | Knapsack DP; the first paragraph explains selecting weighted items, while the value-maximization section preserves its capacity constraint. |
| Динамик програмчлал | DP; the first introduction spells out Dynamic Programming and explains retaining repeated subproblem answers. |
| Монотон стек | Monotonic stack; the worked strict-order condition and equality handling remain unchanged. |
| Гулсах цонх | Sliding Window; the introduction still defines a contiguous segment whose boundaries move. |
| Unnamed deque-based minimum-window method | Monotonic queue is named at its first explanation; the existing deque implementation and increasing candidate values are retained. |
| хэш / Rolling hash | Hash / Rolling Hash; the numeric-summary explanation, collision risk, probabilistic assumptions and exact-verification cost are retained. |
| Битийн масктай DP | Bitmask DP; the introduction explains encoding a small set as a bitmask and keeping it in the DP state. |

Ordinary mathematical монотон, weak/strict order, comparison operands and rounding/approximation terms remain intact. Descriptive references to two actual pointers in LCA and Floyd's cycle procedure remain contextual. **Coordinate Compression (`hash-compression`) is unchanged**: it is an order-preserving exact transformation, not hashing. Literal sequence order, recursion, arrays and other established Mongolian mathematical terms are not broadly renamed. Stable aliases remain intact.

The private baseline has 73 public lessons / 74 stored rows, eight private drafts, 1,010 problems and 357 tutorial history entries. A second prepublication snapshot confirms all 48 target revisions and bodies still match the reviewed baseline.

Validation recursively checks all 73 native documents and exact before/after paths. English translations, executable and code-marked inline spans, display/inline math, numeric tokens, diagram data and table data are unchanged. The preserved corpus contains 2,498 executable blocks, 362 display-formula blocks, 770 diagrams and 410 tables. Executable byte equality proves token/operator equality; the 241 complete program hashes match prior successful compilation. No new compilation is claimed. IDs, URLs, ordering, priorities, practice identities/stages and native editor structure remain intact; human-readable metadata changes only replace the reviewed algorithm names.

The focused SQL regression validates every one of the 48 replacements in 16 bounded batches of three, including rollback, stale-body/catalog/draft rejection, replay rejection, exact reviewed hashes, and unchanged non-target rows/drafts/learner/problem fixtures. The wrapper retains the established 1–3 target contract and fresh catalog/all-draft guards. Each live transaction requires fresh authority/function/trigger, body/revision and draft checks, scoped recovery and one-time intent/result evidence.

All 368 Node tests pass, plus three final focused tests after the last seven Two Pointers references were corrected. The 48 changed lessons pass 192 bilingual mobile/desktop reader cases and 96 native editor round trips; the six lessons affected by those final references pass 24 additional reader cases and 12 editor round trips. These results are recorded in [verification.json](conventional-names/verification.json). Browser checks use the real local reader, MathJax, TOC, practice controls and native editor with current candidate bodies; they are not live authenticated acceptance. The known live Chromium certificate limitation is not bypassed.

Publication status is separate from this review. Only the 48 changed published lessons may be republished; a later receipt records committed revisions/history, exact anonymous public bodies, untouched protected state and normal-TLS deployment verification. No migration, credentials, authority change, APPROVE review, private-draft publication or deferred completion/profile/weekly-progress UI work is included. Histories 286–357 from the prior pass are already committed and must never be replayed.
