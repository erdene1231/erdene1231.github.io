# Coordinate compression and difference arrays

Two existing stable originals, not new tutorials. Publication receipt is separate.

## Source and coverage

Read the supplied Competitive Programmer’s Handbook, chapter 9, “Additional techniques”, printed pages 93–94 (PDF pages 103–104). Inspected the actual page-93 layout and complete extracted passage through the end of page 94. Source credit remains centralized on the Tutorials page.

| Source teaching step | Candidate location |
| --- | --- |
| Large array indices and advance knowledge | hash-compression / need |
| Order-preserving mapping c(a)<c(b) | preservation, trace |
| Original 555, 10^9, 8 example and ranks | need |
| Range addition vs point retrieval | difference-array / need, limits |
| Original eight values and their differences | need, definition |
| Recover position 6 by 3−2+4−3=2 | need |
| Add 5 to positions 1–4, adjust differences at 1 and 5 | update |
| Updated difference row and cancellation reasoning | update |
| Point changes + prefix queries on a Fenwick/segment tree | limits; links to the separately taught structures |
| Both range updates and range queries require an extension | limits, without duplicating the later advanced lesson |

Added implementation explanations rather than omitting code: five compression fragments and six difference-array fragments precede their exact complete C++17 programs in both languages. Compression returns zero-based dictionary positions internally and one-based displayed ranks. Duplicate and negative-value traces are retained from the standalone lessons. Rank gaps are explicitly not distances; absent query endpoints are not missing stored values. Exact membership requires an equality check after lower_bound.

Difference-array code uses full initial differences with an n+1st cancellation boundary, not a delta-only array. The signed example keeps its initial terminal −3 and final terminal −1; reconstructing the first n entries produces [4,1,10,1,1]. Empty internal ranges cancel. External inclusive one-based endpoints convert to [l−1,r). Documented arithmetic bounds keep intermediate differences and running sums in ll. A dynamic tree is discussed as the next technique, not falsely claimed to be supplied by the offline program.

## Editorial and preservation review

Read both narratives in context. Definitions precede formulas; each update is explained through its effect on a prefix. Mongolian uses “эрэмбэлэгдсэн”, “ялгавар”, “хуримтлагдсан нийлбэр”, and “хоёр үзүүр орсон”; no repeated book/edition narration. English follows the same steps. Program fragments match complete sources byte for byte. Existing IDs, priorities, prerequisites, practice keys/flags, variants and next links remain unchanged. Practice distinguishes core from independent extensions and warns when additional data structures are needed.

No runtime/editor/schema/security changes. Chapter 9 remains attached to segment-tree; these focused supplements retain their existing placements. Local native reader checks include both languages, themes and responsive widths, editor reload with every untouched block preserved, and actual listing order. Live publication and counts must be read from the final receipt, not inferred from this review.
