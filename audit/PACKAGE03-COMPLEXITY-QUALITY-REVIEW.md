# Complexity revision 9: improved but incomplete against requested source coverage

The published revision9/history204 receipt remains a factual record of execution and exact-body verification. It is not pedagogical acceptance. On the owner's latest feedback this exemplar is reopened; scaling its template and publishing other candidates are paused. No unpublish, SQL replay or private-draft rewrite is required.

## Direct comparison evidence

Re-read the full uploaded chapter2, printed17–24/PDF27–34, and visually inspected all eight rendered pages, including code boxes, the array highlight, recurrence explanation and empirical timing table. Compared the actual current native body and reader screenshot, not only section counts.

- Printed17–19 build calculation rules from concrete short code: a single loop, nested loops, three linear variants, a triangular loop, sequential phases, independent variables, and two recursive functions with a call-count table. Revision9 compresses most of this into one summary table and prose with no corresponding code. A beginner is told the result without seeing the operation being counted.
- Printed20 gives each complexity class room to explain its mechanism, with explicit subsets/permutations. Revision9 merges classes into one-line table entries and omits polynomial/non-polynomial context. The visual compactness has become conceptual compression.
- Printed21 relates several input scales to plausible algorithm classes. Revision9 has one numeric comparison but no multi-scale estimation table. The caution that seconds depend on hardware is useful, but cannot replace the examples.
- Printed21–23 carry the SAME eight numbers `[-1, 2, 4, -3, 5, 2, -5, 2]` and answer10 through three algorithms. Revision9 unnecessarily replaces these with six other values/answer7. The owner's latest clarification requires preserving supplied content/examples, not merely similar style.
- Printed22 places one complete compact algorithm beside its explanation, making the removed loop visually comparable. Revision9 splits each slow function into opening boilerplate, core and closing return blocks, repeats identical setup prose, and postpones the only full program until much later. This is mechanical fragmentation rather than meaningful teaching units.
- Printed23 explicitly chooses between a new one-element segment and extending the previous best ending segment. Revision9 instead uses a zero-clamped state. Both can produce correct empty-allowed answers, but the changed state obscures direct comparison with the book's explanation.
- Printed23–24 distinguish measured performance from asymptotic growth. Revision9 drops the empirical comparison. Retain the book's table as its HISTORICAL reported experiment, not measurements made on this site or a universal one-second promise; independently measured additions must be labelled separately.
- The native mobile screenshot shows several large title/control blocks before the first small conceptual example. The book alternates short narrative, code and explanation promptly. This supports simplifying lesson titles/subheadings and reducing repeated setup; it does not prove a general CSS bug or authorize an untested global reader redesign.

The earlier 185 tests establish software/code behavior, not these teaching requirements. The 10440 result checks do not compensate for missing source examples or shortened explanation.

## Corrected content progression

Retain the book's four main sections and their full substantive examples: calculation rules (including loop/order/phases/multiple variables/recursion), classes, efficiency estimates, and maximum-subarray comparison. Add the requested explanatory code fragments and complete C++17 program without interrupting every brace or return. Keep source numeric examples, including the eight-element array, recursive call counts, constraint scales and explicitly historical timing data. Natural MN/EN wording, native math/code/diagrams, deliberate int/ll types and compatible practice remain required. No fixed15 headings.

Source traceability must distinguish preserved example/data from added explanations and newly written implementation. The actual official project README, reached via the verified CSES page, states CC BY-NC-SA4.0: https://github.com/pllk/cphb/ . Verify and apply attribution, change notice and matching adaptation license to handbook-derived teaching content, without relicensing unrelated app code or the owner's template by accident. Do not invent an unrestricted license. The uploaded book itself is the source for adaptation, not an instruction document.

## Short revised original Mongolian excerpt (draft, not published)

### Баруун төгсгөлийг нэг байрлал ахиулбал

Номын жишээ массивыг хэвээр авъя:

`[-1, 2, 4, -3, 5, 2, -5, 2]`

Зүүн төгсгөлөө хоёр дахь элемент болох $2$ дээр тогтооё. Баруун төгсгөлийг дарааллаар ахиулахад хэсгийн нийлбэр $2$, $6$, $3$, $8$, $10$ болно. Жишээ нь $[2,4,-3]$-ын нийлбэр $3$ байсныг мэдэж байхад дараагийн $5$-ыг нэмээд $8$ гэж олно. $2$ ба $4$-ийг дахин нэмэх шаардлагагүй.

Иймээс нэг зүүн төгсгөлд нийлбэрийг ганц удаа тэглэж, баруун төгсгөл ахих бүрд шинээр орсон утгыг нэмнэ. Дараах нь функцийн гол хэсэг; $a$ нь массив, $n$ нь түүний урт, `best` нь өмнө олдсон хамгийн их нийлбэр юм.

```cpp
for(int l = 0; l < n; l++) {
    ll sum = 0;
    for(int r = l; r < n; r++) {
        sum += a[r];
        best = max(best, sum);
    }
}
```

`sum`-ийг доторх давталтын өмнө эхлүүлсэн нь чухал. Ингэснээр нэг зүүн төгсгөлөөс эхэлсэн нийлбэрүүд өмнөх ажлаа үргэлжлүүлнэ. Харин дараагийн зүүн төгсгөл рүү шилжихэд хуучин нийлбэр хэрэггүй тул дахин тэглэнэ. Боломжит хэсгүүдийг орхиогүй; тэдгээрийн нийлбэрийг олох давтагдсан ажлыг л хассан. Одоо $n+(n-1)+\cdots+1$ удаа шинэ утга нэмэх учраас хугацаа $O(n^2)$ болно.

Next: preserve the book's nonempty ending-segment state `sum = max(a[i], sum + a[i])`, while `best` starts at zero because the final answer allows an empty segment. Trace all eight positions before showing its explained compact implementation and final complete program. Do not claim this short excerpt is the completed replacement lesson or verified renderer output.


## Latest owner clarification (supersedes blanket rejection wording)

The owner explicitly says revision9 is much better than before. Preserve its useful original explanations, correctness details, native code/math, practice and improvements. It remains incomplete against the requested source coverage, not an entirely bad lesson. The FOUR MAIN internal sections must be Calculation rules, Complexity classes, Estimating efficiency and Maximum subarray sum, with detailed examples/code as internal headings. Reuse ordinary existing sections/TOC/anchors. The separate sub-tutorial feature was cancelled; no nested entities, new editor hierarchy, schema/migration or progress semantics are authorized. Other chapter topics likewise retain their substantive internal source subtopics, not an arbitrary4or15section quota.

All five additional full-book TOC PNGs and the two later topic crops were materialized and actual pixels inspected. They cover chapters1–30 and118numbered subtopics, not merely complexity. The coverage ledger records targets, not proof of implementation. Preserve stable focused lesson IDs with crosslinks where a primary containing lesson covers the full chapter; never destructively merge IDs/progress or silently omit advanced source subtopics to enforce the earlier illustrative17count. A final container/crosslink map is still to reconcile before scaling.
