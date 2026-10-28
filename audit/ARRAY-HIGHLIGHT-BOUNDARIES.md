# Native array highlight boundaries

Reproduced the owner's actual screenshot using the existing renderer: `border-collapse: collapse`, adjacent unselected right border rgb(229,231,235), selected left border rgb(25,77,56), both1pxsolid. The preceding cell wins the collapsed-border tie, so a selected group's left boundary appears grey.

The renderer now marks a cell's shared side when its neighbour is highlighted; diagram-only CSS gives that side the same existing theme highlight-border color. The shared edge remains a single collapsed1px line. No border-width increase, outline overlap, new data field, table/graph selector change or stored content mutation.

24 Chromium cases cover one highlighted cell, interior/first/last contiguous groups, separated groups, two-row DP groups, light/dark,375px/1000px and actual native authoring→JSONsave→reload→reader. Assertions verify all required sides, one-pixel widths and rasterized boundary pixels. No clipping/page overflow or selection changes. Report: ARRAY-HIGHLIGHT-BOUNDARIES.json. Existing graph/table software tests are retained.

Cache54 loads the revised reader renderer and diagram stylesheet; editor controls/schema and database contracts are unchanged. No migration/publication SQL is required. This UI correction does not establish acceptance of complexity revision9's pedagogy; its separate content correction remains pending.
