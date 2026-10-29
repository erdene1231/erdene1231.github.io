# Directed graphs: full chapter 16 review

All eight supplied source pages were inspected as text and rendered pixels: printed149–156 / PDF159–166. Stable topological-sort contains the complete chapter; focused existing BFS/DP/shortest-path/LCA IDs and relationships remain unchanged. No repeated source/edition prose appears inside the lesson.

| Source coverage | Native adaptation |
| --- | --- |
| DAG and successor classes | Nonempty-cycle definition, weak functional components and unique successors |
| Topological sorting | Exact six-node topology, both valid source orders, three states, all three finishing stages, full finishing list and reversed list; cyclic2→3→5→2 counterexample |
| Path DP | Distinct1→4 direction retained versus4→1 in the preceding graph; all three paths, recurrence, exact1,2,3,1,1,3 vertex counts; extensions to weighted minima/maxima, edge counts and mandatory vertices |
| Dijkstra extension | Exact original weighted graph and retained tight edges, distances0,3,5,7,8 and counts1,1,2,3,3; strictly-positive qualification and explicit zero-weight-cycle limitation |
| State-graph model | All0–6 coin states and13edges for1/3/4coins, topological sum order, minimum2coins and9ordered sequences; graph and complete transition table retain every source edge |
| Successor paths | Exact nine-node mapping/two components,6-step walk, all1/2/4/8-step table values,11=8+2+1 and both4-start query answers |
| Cycle detection | Exact tail1→2→3 and cycle4→5→6→4; visited-array method, Floyd meeting/entry/length stages and divisibility argument; input storage distinguished from auxiliary storage |

Six independent C++17 implementations are explained before full code. Topological DFS is iterative; DAG path statistics, positive-weight shortest-path counts and coin sequences have explicit exact-count bounds (simple graphs n≤60, positive distinct coins and target≤60) keeping ll safe, rather than silent overflow or modular equality for mandatory vertices. Larger counts require an appropriate modulus or arbitrary precision. Successor jumps use60levels for0…1e18, int vertices and ll steps; the later dedicated LCA/static-path lesson is not preempted. All six existing practice relationships/priority remain unchanged.

520 UBSan/oracle runs pass: independent Kahn orders/cycle detection, exhaustive DAG paths and intersections, all simple positive paths, coin-sequence enumeration and recorded functional walks; long iterative chain,2^58exact count,1e18queries, cycles/disconnected/negative DAG weights/singletons/zero steps are covered.

Native diagrams retain the source node identities and directions. Existing SVG markers were hidden behind fixed-size nodes when the SVG scaled; the bounded renderer correction measures endpoint node rectangles in CSS pixels, clips the line and draws an8px triangle outside the target. ResizeObserver handles canvas and node size changes. Six actual native arrow cases verify direction and outside-node placement across themes, resizing and longer labels. Existing color/annotation/editor round-trips pass; no serialized content format or security/schema change. Self-loop drawing enhancements are not claimed by this straight-edge correction. PR119 fixed grid tracks remain unchanged. Cache63 covers only this module/style import closure; unrelated URLs remain intact.

Reader8cases, MN/EN editor round-trips and19native diagrams (14graphs/5arrays) pass both-theme/mobile checks. Source and representative rendered pixels were inspected, including the reversed4/1directions, shortest-path arrows, functional reciprocal arrows and cycle entry. Live visual verification retains the known certificate block, never bypassed; deployed bytes and anonymous public-body retrieval are separate checks. Fresh guarded publication must preserve all other lessons/private drafts/Mongolia/problem/learner/authority state; never replay historical jobs or migration037. Three deferred features remain deferred.

The post-publication read identified one precision issue: the visited-array method's walking phase is O(mu+lambda), but initializing its n-slot array costs O(n). Both language paragraphs now explicitly state O(n) total for that implementation, while Floyd retains O(mu+lambda) function time and O(1) auxiliary space. The first publication (revision7/history227) was independently verified and must not be replayed. This narrow wording correction uses a new revision7 CAS job, not the previous SQL.
