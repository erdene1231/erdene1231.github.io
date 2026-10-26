# Catalog visibility, hint badges and two-pane selection

Branch codex/catalog-selection-panels, parent main PR14 merge6104484. Frontendv37.

The catalog no longer forces tags visible for solved problems. Solved detail
reflection tags follow the same setting. Explicit per-detail tag reveal remains
available, and switching the global toggle clears that override. Removed the
All/01/02/rating/source pack tabs and their hidden pack filter state; pagination
scrolls to the library instead. Source/tag/min-max/status/sort filters remain.

Every row shows Hint0/3..3/3 immediately before its status in a bordered badge.
Colors progress green/olive/amber/orange; text and accessible labels carry meaning
independent of color. Hint counts use stored progress without changing it. Both
badges remain alongside each other on mobile. Catalog spacing, filter layout and
row hover presentation were refined for light/dark themes.

The shared problem dialog has two panes: filtered unselected rows on the left and
all chosen rows on the right. Chosen rows remain visible regardless of filters.
Left checkboxes move rows to the right; select-all-filtered adds the entire current
result. Reset-filters preserves chosen rows. Right checkboxes mark chosen rows for
removal; its Select all marks all chosen rows, Remove marked returns them to the
left, and Clear all removes all choices. The right explanatory caption distinguishes
marking from the saved selection. Empty multi-selections can be applied; single
admin edit selection still requires one row. Incomplete embedded references are
kept as private placeholders until selected, never silently linked to another task.
Actor/lock guards, max30 practice limit, section splitting, exact-number search and
numeric/legacy key compatibility remain. Cancel makes no parent edit.

Verification: npm test passes16 files. Actual app.js catalog Chromium test uses
local synthetic progress and eight fixture tasks, no service configuration; checks
solved/unsolved tags, reflection tags, reveal/reset, hint0..3 position, removed pack
DOM and light/dark375/1200 widths. Popup test uses748 synthetic tasks and covers
both panes, reset, mark/remove, empty apply, selection across filters, limits,
actor/cancel, bulk insertion/Undo and overflow. Editor regression checks also pass.
Total39 browser groups:7 catalog,16 popup,16 editor. Screenshots and JSON evidence
are committed. Auth/RPC are mocked; deployed authenticated UI remains unverified.

No production calls, migrations, real content or progress writes.029 remains
applied20261026100333; do not replay021-025/028/029. Pending026/027 remain separate.
Review/merge PR and deploy fullv37 graph. NEXT-STEPS/Start skill and downloadable ZIP
record continuation and verified remote commit; merge/deploy are separate actions.
