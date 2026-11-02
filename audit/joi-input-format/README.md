# JOI format/sample presentation — approved, not yet published

User's revised direction (2026-11-02): native Input/Output boxes remain literal
plain text, including samples. Remove the uncomfortable green text background.
Put mathematical input-format templates outside those boxes, as ordinary native
math content within their existing Input sections. No math-in-code feature.

Both original screenshots and the clarified screenshot were materialized and
visually inspected. They show Unique Cities / task-899. The green rectangle is
not the sample panel background: the dark-theme `.tutorial-content code` rule
outranks the sample code's transparent rule. The scoped selector fix in
`tutorial-samples.css` removes that inherited inline-code fill; existing neutral
panel/header colors and all other code/table/graph styling stay intact. Only
this stylesheet's entry cache changes (42 →43). No MathJax/runtime imports change.

Fresh anonymous reads of all24 current JOI rows were compared to the published
plans. Only6 statements contain non-sample Input code templates:

| Problem ID | Problem | Current revision | Native blocks changed |
|---|---|---:|---:|
| task-721 | Coin Collecting |2|2 (MN/EN)|
| task-723 | Growing Vegetables is Fun4 |2|2|
| task-896 | Bitaro the Brave |3|2|
| task-897 | Exhibition |3|2|
| task-898 | Growing Vegetables is Fun3 |3|2|
| task-899 | Unique Cities |3|2|

`proposals.json` stores the exact reviewable6-statement allowlist with fresh
revision/body hashes and each old/new block. Each format becomes one native
`math` block using an array with preserved row/token order; ordinary separators
become math spacing. For example Unique Cities preserves N M, A_1 B_1, vertical
dots, A_{N-1} B_{N-1}, and C_1 … C_N as five consecutive rows. It remains in the
Input section immediately after its explanation; no Input panel/copy button is
used for this mathematical template.

All80 official sample pairs and their literal spaces/newlines remain exactly
unchanged in both languages. Across all24 statements,332 code blocks would
become320:160 Input and160 Output, all samples. The other18 statement documents,
all prose, constraints, examples, sources/license/provenance, metadata, URLs,
editorials and priorities remain unchanged. No schema or access change.

Local evidence:

- `node --test tests/joi-input-format.test.mjs tests/mathjax-module-instance.test.mjs`:
  2/2 pass. All6 documents validate; reversing the12 typed block changes exactly
  restores their original native documents, with no other content differences.
- `python tests/browser/joi-input-format.py`:48 actual app-route cases
  (6×MN/EN×mobile/desktop×light/dark),6 native bilingual editor collect/save/reload
  roundtrips. Format MathJax is outside panels; all sample code stays literal,
  transparent and safe. Explicit `$x$` / `\(y\)` / markup / tabs / blank lines
  remain text and copy exactly. One renderer module, one MathJax bootstrap and
  no page errors. Navigation among the6 actual problem IDs is exercised.
- `python tests/joi-statement-samples.py`:80 official pairs and446 bounded
  independent oracle/edge checks pass, unchanged.
- Actual local screenshots were viewed in both responsive themes. Internal
  screenshots are not published or saved to Library.

Browser uses real app/native editor/renderer and MathJax with synthetic read-only
SDK/Auth transport and the local prepared proposals. This is not a production
save or live visual verification. `browser.json` records the exact tested scope.

Owner explicitly approved this exact version at2026-11-02 03:49:01 UTC.
Publication is in progress; not yet counted live. Fresh guards were captured,
and a full1064-row local rehearsal verifies6 statement-only changes,1058 exact
unrelated rows, midway rollback, replay rejection and protected/access equality.
Before the production submission obtain fresh guards again; never execute the earlier JOI import/URL SQL or
reuse old statement jobs. Only these6 statement-body fields may change; ordinary
samples and all unrelated fields must read back exactly.
