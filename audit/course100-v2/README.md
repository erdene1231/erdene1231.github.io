# 100-day course rebuild and native practice quizzes

Full newly authored day1–100 curriculum, not a patch of the previous ordering. Stable plan/day identities and existing learner records remain untouched. A read-only check found two started plan records and no completed days; no assumption was made about their owners and no migration/reset was performed.

## Curriculum decisions

- Beginner environment/I/O/loops/arrays/strings, then complexity and sorting/search; static arrays/containers; complete search/math; DP; graphs/shortest paths/trees; range queries; selected advanced methods; strings; contest/upsolve/reflection.
- 75 distinct core catalog problems. One deliberate core exercise on most days; bounded assessments, repeated tasks revisited using the new method rather than accepting an old solved badge as new learning. Difficult later tasks are identified as extensions.
- Each day points to specific native tutorial sections; day completion requires their reading record, required task status and daily self-checks. Whole-topic mastery semantics are unchanged. Quizzes never auto-complete a day.
- 122 single-answer questions, plus three setup-lesson questions. Stable opaque option identity, equivalent bilingual choices, retrieval/review, feedback after checking and retry. Client-delivered answers are practice, not secure examination.
- Existing authoritative tutorial/problem IDs are verified in the committed inventories. `selection-manifest.json` records daily choices and review rationale. Exact3/7/21 review intervals and pacing are our curricular judgment, not a research guarantee.

## Research and illustrations

`research-sources.json` records primary CP/platform/compiler sources and retrieval/distributed-practice rationale. Setup lessons distinguish editor/shell/terminal/compiler, C++ language mode versus toolchain, CMD/PowerShell/Bash and exact compile/redirection commands. IOI2026 equipment is the official published planned/minimum configuration, not a tested VM.

Microsoft VS Code docs screenshots are CC BY3.0 US. AsbakWiki's Dev-C++5.1.1.0 screenshot is historical CC BY-SA3.0, not Embarcadero6.3 settings. Actual pixels were inspected, version captions retained; images re-encoded only. Sources and image-specific licenses are in `tutorial-assets/cpp-environment/LICENSE.txt` and native lesson links. No fabricated UI or Windows capture claim.

## Implementation and rollout

The existing native tutorial block model/editor/reader gains a bounded `quiz` type; no separate quiz service or access grant. Static lesson images have an exact three-path same-origin allowlist; ordinary authenticated Storage images still use their original path contract. Migration041 changes only the existing validation function with baseline/ACL guards, no RLS/roles/grants.

Staged rollout keeps courseVersion1 and quiz authoring disabled until runtime/assets and041 are installed and three setup tutorials are read back. Final config enables courseVersion2/quizVersion1. The legacy JSON is a temporary release fallback, not a user-history migration. No learner data is rewritten.

## Verification

- Full Node aggregate before final publication helper:462/462 passed. The expanded aggregate includes the atomic three-document publication fixture.
- Native browser fixture: all100 bilingual documents, actual editor authoring/option reorder/delete/copy/serialization, retry/navigation, section reading/day save/reload, responsive375/1200/light/dark and actual three tutorial routes/images. Synthetic read-only SDK/Auth; no claim of production authenticated GUI save.
- C++:five complete programs,24 compile/run cases in C++17/C++20, quoted cwd and Bash stdin/stdout/stderr files, compile-failure stale-binary prevention. Windows shells/GUI and final IOI VM were not executed.
- PGlite uses actual current validation definitions, tests041 and all103 documents, preserved old data/ACL, invalid inputs and replay rejection. Publication fixture checks exact three-ID scope, stale guard, injected atomic rollback, old-row preservation and replay rejection.

Publication receipts and deployed checks are added after completion. No earlier JOI/content transaction or migration is replayed.
