# v39 publication workflow / optional content / delivery plan

Draft footer: Preview | Save | Publish | Delete draft.
Published footer: Preview | Temporary save | Publish | Reset | Temporary remove.
English-add button removed; language selector initializes independent blank EN.
New named tutorials start with zero sections/blocks. Root name remains required;
summary/category/aliases/prerequisites/relations/translation are optional. Empty
content can publish with a nonblocking draft-review warning. Published Publish
saves immediately; unknown references, malformed URLs, images and invalid structure
remain rejected. Reading hides absent metadata and empty section navigation.

Published edits are volatile until explicit Temporary save. Refresh drops volatile
edits but reloads a saved private draft. No implicit published-mode server/local
unsaved autosave. Draft-mode autosave remains. Reset confirms against a fresh
published revision and removes only the actor's saved draft, returning latest public
body; other editors/progress/publication/history remain untouched. Publication and
reset CAS reject races. Semantic comparison ignores empty translation/metadata so
Reset/Publish reflect meaningful changes. Backups/import remain private.

031_optional_tutorial_content_and_reset applied20261026121014 after full metadata
matched030. It installs optional text validation and owner reset, relaxes only
metadata/empty-section/inline requirements and retains021 prerequisite safeguards,
029 numeric lookup, media/deleted-ID/actor/CAS guards. Actual counts/hashes unchanged
by installation:748 problems/56 tutorials; no real publish/reset/delete was invoked.
Fresh after031 schema matches repository reconstruction with zero differences.
Node19 files pass; new workflow Chromium5 groups and tags8 groups pass. Browser
uses synthetic RPC/catalog; deployed authenticated UI remains unverified.

Latest user tag rule supersedes prior hide-all rule: solved tags remain visible;
unsolved tags are hidden using reserved fixed-height space. Tests verify no row
height changes on toggle, both themes and mobile.

Original requirements: audit/DELIVERY-PLAN.md and JSON retain1467 source rows and
319 topic traceability rows with phases, tests and dependencies. Their classification
is planning, not completion evidence. P1 first audit executed: public prerequisites
resolve, no embedded problem refs currently stored. Pending026 requires adaptation;
027 remains pending. Current editor feature scope is frozen except verified bugs.
The larger source backlog is NOT complete. Next work follows P1→P8 gates.
Review/merge and deploy completev39. Do not replay021-025/028/029/030/031.
