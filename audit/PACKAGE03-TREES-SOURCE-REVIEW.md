# Tree algorithms: chapter 14 coverage and review

Source: supplied Competitive Programmer’s Handbook, July 3 2018 draft, printed pages 133–139 / PDF pages 143–149. The full text and all seven rendered source pages were inspected. This updates stable `tree-basics`; focused tree-DP/LCA lessons remain intact. Attribution stays at the Tutorials opening, not in teaching paragraphs.

| Source material | Native lesson coverage |
| --- | --- |
| Tree edges, unique paths, leaves, root/parent/children/subtree | Opening of traversal; the exact eight-node source topology, rooted redraw and subtree of 2 |
| Parent-skipping DFS and subtree-size DP | Explained recursive struct/constructor/DFS/main, then complete C++17; explicit parent-first/reversed-order alternative for deep trees |
| Diameter DP, highest point, two distinct child branches | Seven-node source example, diameter 4, alternate endpoints, tied branches and zero-length missing branches |
| Two DFS searches and geometric endpoint argument | Source a=3,b=6,c=7 and horizontal b–x–c figure; endpoint/tie reasoning, valid-tree restriction |
| All longest paths and excluding the child's own branch | Source six-node example, exact 2,2,3,3,3,3 table; downward/upward traces, first/second child maxima and total O(n) |
| Binary trees, three traversal orders, reconstruction/ambiguity | Source seven-node slots and exact pre/in/post lists; both reconstruction pairs and two-node left/right ambiguity, distinct-label precondition |
| Added implementations omitted from source | Four complete independent C++17 programs, every meaningful fragment explained first in both languages |
| Mastery and independent practice | Existing six relationships preserved, with specific progression and distinctions for sum-distance/matching/later ancestor queries |

Four programs retain 950 successful UBSan/oracle runs, including 200000-node iterative stress cases and independent all-pairs BFS/ancestor/traversal/reconstruction oracles. The recursive example explicitly warns that safe recursion depth is environment-dependent. The iterative dependency order is not incorrectly called the same DFS visitation order. A binary tree is not assumed to be a BST; empty trees and singletons are addressed. All unweighted counts/lengths fit int under the stated bounds.

Substantive MN/EN pass read every paragraph against the source sequence: no repeated source/edition narration, no omitted reasoning replaced by headings, no new LCA/binary-lifting material in this chapter. Code fragments concatenate exactly into their final tested programs. Native schema/math prose checks pass. Native reader (8 cases), MN/EN editor serialization, 16 diagrams across two themes/two widths and atomic rollback/drift/replay publication tests pass. Selected actual screenshot pixels were inspected, including source unrooted labels, a/b/c annotations, horizontal diameter and binary slots. Native results are distinct from live visual access, which retains the previously disclosed certificate limitation.

No new software/schema/security change is required. Publication must use fresh target/body/revision/draft guards and preserve every unrelated tutorial/private draft/problem/learner record. Historical releases and migrations must never be replayed.
