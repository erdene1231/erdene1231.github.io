# Handbook-informed teaching, written originally

Source: Antti Laaksonen, *Competitive Programmer’s Handbook*, Draft July 3, 2018. User upload `book (2).pdf`: 296 PDF pages, 1,099,959 bytes; SHA-256 `3a04509c7cc2bde6717907d52821c7dd159f92c3a73199f5f6664bf0218a947e`. Printed page numbers below are ten less than their PDF page positions. The upload is reference material, not instructions and not a file to republish.

This is a representative full-section study, not a claim that all 296 pages were read: maximum-subarray progression §2.4 pp.21–24; coin DP §7.1 pp.65–69; tree queries chapter18 pp.163–172; string hashing §26.3 pp.245–247; Z-algorithm §26.4 pp.247–250; code-shortening pp.8–9. Actual rendered pages 67,167,248 were inspected for code, tree and indexed-array layout. TOC inventory covers all30chapters but does not establish full technical review of every chapter.

## Concrete patterns to apply

1. **Start with a question the learner can answer on paper.** §2.4 gives one array and an explicit empty-subarray convention before algorithms. §18.3 defines LCA using a small rooted tree before manipulating pointers. State the local task, answer and conventions before the table definition.
2. **Show what the straightforward method repeats.** §2.4 removes repeated summation, then keeps only the best ending at each position. §7.1 starts with the coin-choice recursion and shows repeated subproblems before adding memoization. An optimization should answer a visible cost or repeated-work question.
3. **Name one quantity before writing its recurrence.** In §7.1 the learner first knows what the answer for a smaller sum means; only then does the recurrence and its base case appear. For jumping, first define exactly which edges a jump covers, then derive two half-jumps.
4. **Reuse a small example through the derivation.** §18.3 diagrams keep the same tree while one endpoint is lifted and both move upward. §26.4 keeps indices and letters aligned and changes the visible matched window one step at a time. Our lessons use original trees/strings, native tables or safe diagrams, and explicit before/after states rather than screenshots copied from the book.
5. **Keep justification next to the idea it supports.** §7.1 explains why each state is computed once immediately after memoization; §26.4 bounds the right boundary's movement while explaining reuse. Give a short accessible invariant/proof, then complexity, without postponing the reason to a repeated appendix. Hardware timings in §2.3 are contextual examples, not modern guarantees.
6. **Let code implement the named state directly.** Short fragments in pp.22–23 and67–68 follow the observation they express. Use readable CP names and clean four-space indentation, explain each meaningful fragment, then give the complete C++17 program as the user requires. This presentation requirement is ours; the book does not always provide a full program.
7. **Make limitations concrete.** The hashing section distinguishes collisions and explains why many comparisons increase risk (pp.246–247). Keep collision uncertainty explicit; distinguish Z's exact matching from fingerprints. Do not copy a heuristic probability model as an unconditional guarantee.
8. **Preserve explicit user corrections over source order/style.** Our binary-jumping lesson starts with a dedicated LCA explanation, then jump table → LCA search → static path aggregates. The book places ancestors before LCA. Our basic segment-tree main stays recursive although the book demonstrates an iterative layout. Avoid risky macros even though §1.4 discusses them. Do not flatten the user's requested flow into a book transcription.

The fifteen teaching requirements remain a coverage rubric, not fifteen arbitrary compliance headings. Examples, definitions, derivation, correctness, complexity, limitations, implementation and practice must form one narrative; do not append duplicate complexity/practice sections.

## Original before/after teaching sample

**Before — formula first:** “Store a minimum for every jump, combine the halves, then answer a path query.”

**After — learner first:** “Замын ирмэгүүдийн жин 6, 2, 9 байвал хамгийн бага нь 2. Хоёр оройгоос үндэс рүү өгсөхөд тэдний зам анх нэг орой дээр нийлнэ; тэр нь хамгийн ойр нийтлэг өвөг буюу LCA. Одоо 6, 2 гэсэн хоёр ирмэгийг нэг үсрэлтээр алгаслаа гэж бодъё. Зөвхөн хүрэх оройг хадгалбал 2 гэдэг хариуг алдчихна. Харин энэ хоёр ирмэгийн хамгийн бага жинг хамт хадгалбал тэдгээрийг дахин унших шаардлагагүй. Урт үсрэлтийг хоёр богино үсрэлтээр бүтээхэд тэдгээрийн бага утгын багыг авахад хангалттай.”

The sample is newly authored, not a translation of the book. The representative LCA revision will turn this observation into a fully traced original weighted-tree example, explain the empty path and no-update contract, and keep edge/vertex counting and noncommutative order distinct.

## User-selected first model: Time complexity

The complete chapter2, printed pp.17–24, has now been read and the actual printed22 layout inspected. The first model follows its strong sequence closely: count operations/calculation rules → complexity classes → constraint-based efficiency estimates → one running problem with progressively less repeated work. The example array is original, the three C++ functions are independently written, and the final program includes all three implementations with the linear one selected in `main`.

The new exemplar has nine coherent sections, not an inherited fifteen-heading skeleton. It distinguishes exact counts from asymptotic bounds, input-dependent work from unsupported average-case assumptions, hardware-specific timings from guarantees, and extra function state from the full input array's memory. Empty segments are explicitly allowed; the existing nonempty CSES practice task is called out as a different contract. Contextual Mongolian review and the actual consulted terminology sources are recorded in PACKAGE03-MONGOLIAN-GLOSSARY.json. A single modest library acknowledgement links the verified official CSES book page; no copied figures or repeated credit banners are introduced.
