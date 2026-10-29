# Inline MathJax scrollbar correction

Inspected actual pixels of the owner's image(20261029-004052).png: the small scrollbar is directly below inline n/2, rather than below the entire lesson or a code block. Existing tutorial-blocks.css assigned overflow-x:auto to every inline MathJax container.

Default Linux Chromium did not consistently reproduce the screenshot's native scrollbar for that fitting expression (clientWidth equalled scrollWidth). A controlled one-pixel underallocation of the real MathJax inline box reproduces unwanted scrolling under the former unconditional rule. This models a rounding/zoom-sized mismatch; it is not a claim of an actual Windows-native fixture.

The fix compares the SVG's natural fractional width with available width in its containing text block, rather than the rounded width of the tiny inline box. Fitting math uses visible overflow, preserving glyphs. Only truly oversized inline math receives overflow:auto. ResizeObserver reclassifies on layout changes; detached old math nodes are unobserved at subsequent typesets. Display math, code/table/array wrappers and graph scrolling are untouched. All consumers of typeset are cache-invalidated to56, including statement/editorial previews, so older cached renderers cannot miss wide-formula classification.

Four actual MathJax browser cases (light/dark,375/1200px) verify fitting expressions, controlled one-pixel reproduction, genuinely wide formulas, no page overflow and resize reclassification. Eight complete complexity-reader cases plus a native editor roundtrip passed;185Node tests passed. No lesson content, revision11 data, private drafts, progress, schema or permissions changed. Graph work remains isolated and unpublished on codex/tutorial-graph-labels, checkpointdf555ba.
