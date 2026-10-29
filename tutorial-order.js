// Handbook chapter order, with existing focused lessons beside their containing chapter.
// These are lesson positions, not new chapter numbers; no IDs or progress are changed.
export const handbookTutorialOrder = [
 'introduction','complexity','sorting','binary-search','lower-bound','upper-bound','hash-compression',
 'set-map','stack-queue','priority-queue',
 'brute-force','recursion','greedy','binary-search-answer',
 'dynamic-programming','grid-dp','knapsack','lis','interval-dp',
 'two-pointers','sliding-window','monotonic-stack',
 'prefix-sums','prefix-sums-2d','difference-array','sparse-table','fenwick-tree','segment-tree',
 'bit-operations','bitmask-dp',
 'graph-basics','bfs','dfs','flood-fill','connected-components','bipartite',
 'dijkstra','bellman-ford','floyd-warshall','tree-basics','tree-dp','kruskal','dsu',
 'topological-sort','scc','lca','paths-circuits','flows-cuts',
 'number-theory','gcd','sieve','fast-power','combinatorics','kmp','string-hashing','lazy-segment-tree',
 'invariant','debugging','subtask-strategy'
];
export function orderTutorials(input, fallbackOrder=[]) {
 const rank=new Map([...handbookTutorialOrder,...fallbackOrder.filter(id=>!handbookTutorialOrder.includes(id))].map((id,i)=>[id,i]));
 return [...input].sort((a,b)=>(rank.get(a.id)??Infinity)-(rank.get(b.id)??Infinity)||(a.order??Infinity)-(b.order??Infinity)||a.id.localeCompare(b.id));
}
// Only containing topics receive the source chapter number. Focused extras have
// an explicit supplementary label, rather than shifting later chapter numbers.
export const handbookChapterNumbers = Object.freeze({
 introduction:1,complexity:2,sorting:3,'set-map':4,'brute-force':5,greedy:6,
 'dynamic-programming':7,'two-pointers':8,'prefix-sums':9,'bit-operations':10,
 'graph-basics':11,bfs:12,dijkstra:13,'tree-basics':14,kruskal:15,
 'topological-sort':16,scc:17,lca:18,'paths-circuits':19,'flows-cuts':20,
 'number-theory':21,combinatorics:22,kmp:26,'lazy-segment-tree':28
});
