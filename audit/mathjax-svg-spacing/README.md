# SVG subscript overlap correction — 2026-11-10

Status: prepared for review; not merged or deployed. No database/content writes.

## Reproduction and cause

Both supplied screenshots were materialized and visually inspected. Geometry §29.3
shows inline vertex indices touching prose, and `x_{i+1}y_i` overlapping in the
shoelace and trapezoid identities. Fresh anonymous public payloads contain 76
lessons; Geometry is revision 2. The actual app route, native renderer and pinned
MathJax runtime reproduce the SVG failure. CHTML does not have this displacement.
Changing `box-sizing` did not fix it; no CSS or formula spacing was changed.

MathJax 3.2.2's `CommonMactionMixin.getParameters()` stores the tooltip's default
horizontal offset (0.2em) in `dx` for every action. `SVGWrapper.place()` adds that
same property to its horizontal placement. Collapsible expressions create nested
`maction` toggle wrappers, which consequently move right without increasing their
bounding-box advance. Their last glyphs overlap the next term or following prose.
The CHTML layout does not use this SVG placement method.

Verified upstream implementation:
- https://github.com/mathjax/MathJax-src/blob/3.2.2/ts/output/common/Wrappers/maction.ts
- https://github.com/mathjax/MathJax-src/blob/3.2.2/ts/output/svg/Wrapper.ts
- https://github.com/mathjax/MathJax-src/blob/3.2.2/ts/output/svg/Wrappers/maction.ts

## Change

A version-pinned, idempotent startup compatibility hook resets `dx` only for SVG
`toggle` actions, before any wrappers are constructed. Tooltip/statusline behavior,
CHTML, collapsible interactions, accessibility and saved menu preferences remain
intact. Official vendor bytes and license remain unchanged. The hook deliberately
does not apply to a future MathJax version; retain the real-layout regression test
when upgrading. This uses MathJax's internal wrapper API and is intentionally
limited to the exact vendored version.

The renderer's reverse import chain advances to v101 and loader to v3 so all
consumers share a single corrected bootstrap. No stylesheet, mathematical content,
code sample, tutorial metadata, database, permissions or learner data changed.

## Verification

Run:

```sh
npm test
python tests/browser/mathjax-svg-spacing.py --payload-dir PUBLIC_RPC_DIR --output-dir RESULTS_DIR
python tests/browser/mathjax-saved-settings.py --payload-dir PUBLIC_RPC_DIR
python tests/browser/mathjax-readiness.py --payload-dir PUBLIC_RPC_DIR
```

The layout test disables only the compatibility call in its control case and
requires negative glyph separation in both reported identities. Corrected cases
measure non-overlapping glyphs and inline ink containment, using fresh published
Geometry in the real app. Coverage includes default settings, SVG/CHTML,
393px/1400px, light/dark, saved scale, native preview rendering, literal Input/Output,
MN/EN, navigation, collapse/expand, CHTML→SVG switching and narrow-screen scrolling.
Screenshots and numeric measurements are recorded alongside this report.

The browser transport serves captured public RPC responses locally and fetches the
real Supabase SDK; it does not fake MathJax or use a signed-in account. Mobile is
Chromium emulation, not a physical Android device. No live authenticated editor or
production deployment success is claimed. Publication awaits approval for this
specific correction.

Observed desktop glyph separation: **−1.784px before**, **+2.834px after** in
both supplied identities. The inline formula's ink is contained with 1px remaining
inside its existing container padding. CHTML boxes retain their natural touching
(non-overlapping) layout. All 10 layout cases (one failing-control reproduction plus
nine corrected configurations), 8 saved-settings cases and 6 startup/recovery cases
passed. Screenshots were visually inspected, including a scrolled mobile dark view.

A normal live Chromium navigation to `https://erdeneclub.com/#tutorial/geometry`
was blocked by `net::ERR_CERT_AUTHORITY_INVALID`. No TLS bypass was attempted.
Fresh public RPC reads used normal certificate validation. Main remained
`f65d8673905699b82363daa2e85c6badfb4bb936` during preparation.

Full repository suite: **474/474 passed**, no failures/skips (330.634s).
`git diff --check` passed. No compiler/content/database tests were altered to
accept changed lesson data; only loader/cache assertions and browser import
versions were updated for the corrected runtime.
