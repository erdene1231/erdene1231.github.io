# User rejection: reopen the three foundation lessons

The user rejected the revision 6 Binary Search, Greedy and DP lessons. They are still live and must not be deleted or unpublished, but **none of the three is accepted or complete**. Stop advancing the other 52 with the rejected template.

## Observed faults

The user screenshot (`libfile_8bb924c8240c8191804deb364f8ac0e8`, viewed as pixels) shows the old 1–10 sequence with sections 11–15 appended. Complexity appears in both 7 and 11; practice appears in both 14 and 15. Code occurs in section 6 before the proof, while the complete program is detached into 13. This is incremental patching, not the requested coherent rewrite.

The Mongolian prose visibly mixes unexplained “scan”, “Boolean”, “Loop-ийн invariant”, “false” and similar terms. The previous article-only browser fixture did not exercise the complete reader with its TOC. In the screenshot, that sidebar occupies roughly half the phone screen and the prose is clipped on the right. The screenshot establishes the symptom, not its cause; reproduce full reader layouts before assigning a cause or assuming zoom.

Prior compilation, schema, transport, MathJax and serialization results remain evidence only for those mechanisms. They did not justify the previous whole-lesson acceptance claim.

## New organization, authored from scratch

Each lesson will have these 15 ordered teaching chapters, with topic-specific titles and transitions:

1. A concrete problem and why it matters.
2. A direct solution and its limitation.
3. Discover the key observation step by step.
4. State the algorithm and the condition it preserves.
5. Work through a complete small example.
6. Prove correctness.
7. Derive time and memory costs and practical limits.
8. Build the C++17 implementation: actual meaningful fragments with explanations first, then the complete program and checked sample.
9. Boundary cases.
10. Common errors with small counterexamples.
11. Prerequisites, variants, related topics and next lesson.
12. Recognizing when to use or avoid this method.
13. Six-stage practice with objectives and prerequisites.
14. Educational importance and which skills/practice to prioritize, independent of task difficulty.
15. A concise synthesis and a mastery self-check.

No duplicate complexity/practice appendices, no old prose pasted into a new numbering scheme. Existing tested algorithm code can be retained where correct; its explanation and placement must be newly authored and understandable.

## Language and preservation

Write natural Mongolian sentences. Use “давталт”, “байрлалын дугаар”, “шалгах нөхцөл”, “хадгалагдах нөхцөл”, “мөрөөр шалгах” and similar clear phrases where appropriate. Explain a necessary foreign technical term once at first use, then use consistent Mongolian wording. Keep C++ identifiers literal and explain them. MN and EN have the same substantive teaching order, not mixed-language Mongolian paragraphs.

Keep stable lesson/problem IDs, references, prerequisite/related/variant/next/practice relationships and all stored learner records. Narrative, titles and layout are replaceable. Do not silently overwrite private drafts. Mongolia is entirely excluded. Current live revision 6 is the fresh guarded base; a replacement publication requires fresh recovery/CAS and the standing operator workflow only after real quality checks.

## Acceptance gates

- Read each complete learner-facing MN/EN lesson against all 15 teaching requirements; headings/tests alone do not pass it.
- Inspect the actual whole reader, TOC, navigation, practice and code at phone and desktop sizes, both themes, and enlarged text; investigate the screenshot symptom.
- Exercise the existing native editor and save/serialize/reload compatibility without flattening structured content.
- Verify explained fragments match the final standard C++17 program and check its sample and meaningful boundary/oracle evidence.
- Publish only a genuinely finished corrected lesson. Until then, accepted completion stays 0/55 and revision 6 stays live.
