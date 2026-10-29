#!/usr/bin/env python3
"""Independent parent/path/subtree oracles for the six chapter-18 programs."""
import collections, hashlib, json, pathlib, random, subprocess, tempfile
ROOT = pathlib.Path(__file__).resolve().parents[1]
NAMES = ['basic', 'aggregate', 'dynamic', 'rmq', 'merge', 'offline']
rng = random.Random(180029)
counts = collections.Counter()

def run(name, lines, expected):
    out = subprocess.run([str(tmp / name)], input='\n'.join(map(str, lines)) + '\n', text=True, capture_output=True, timeout=20)
    assert out.returncode == 0 and not out.stderr, (name, out.returncode, out.stderr)
    assert out.stdout.splitlines() == list(map(str, expected)), (name, lines[:8], out.stdout[:1000], expected[:30])
    counts[name] += 1

def check(n, edges, root):
    adj = [[] for _ in range(n + 1)]
    weight = {}
    for a, b in edges:
        adj[a].append(b); adj[b].append(a)
        weight[a, b] = weight[b, a] = rng.choice([-10**9, -7, -1, 0, 3, 10**9])
    par = [0] * (n + 1); dep = [0] * (n + 1); order = [root]
    for u in order:
        for v in adj[u]:
            if v != par[u]: par[v] = u; dep[v] = dep[u] + 1; order.append(v)
    def ancestor(u, k):
        if k > dep[u]: return 0
        for _ in range(k): u = par[u]
        return u
    def path(a, b):
        left, right = [], []
        while dep[a] > dep[b]: left.append(a); a = par[a]
        while dep[b] > dep[a]: right.append(b); b = par[b]
        while a != b: left.append(a); right.append(b); a = par[a]; b = par[b]
        return left + [a] + right[::-1], a
    def below(v, u):
        return dep[v] >= dep[u] and ancestor(v, dep[v] - dep[u]) == u
    pairs = [(root, root), (root, n), (n, n)] + [(rng.randint(1,n), rng.randint(1,n)) for _ in range(65)]
    if n < 10: pairs += [(a,b) for a in range(1,n+1) for b in range(1,n+1)]
    head = [f'{n} {len(pairs)} {root}'] + [f'{a} {b}' for a,b in edges]
    expected = [f'{path(a,b)[1]} {len(path(a,b)[0])-1}' for a,b in pairs]
    run('rmq', head + [f'{a} {b}' for a,b in pairs], expected)
    run('offline', head + [f'{a} {b}' for a,b in pairs], [path(a,b)[1] for a,b in pairs])
    ks = [(u,k) for u in [root,n,rng.randint(1,n)] for k in [0,1,dep[u],dep[u]+1,10**18]]
    run('basic', [f'{n} {len(pairs)+len(ks)} {root}'] + head[1:] + [f'C {a} {b}' for a,b in pairs] + [f'K {u} {k}' for u,k in ks], expected + [ancestor(u,k) for u,k in ks])
    vals = [0] + [rng.choice([-10**9, -3, 0, 2, 10**9]) for _ in range(n)]
    for mode in ['E','V']:
        lines = [f'{n} {2*len(pairs)} {root} {mode}']
        if mode == 'V': lines.append(' '.join(map(str, vals[1:])))
        lines += [f'{a} {b}' + (f' {weight[a,b]}' if mode == 'E' else '') for a,b in edges]
        ans = []
        for a,b in pairs:
            nodes,c = path(a,b)
            values = [vals[u] for u in nodes] if mode == 'V' else [weight[x,y] for x,y in zip(nodes,nodes[1:])]
            lines += [f'P {a} {b}', f'S {a} {b}']
            ans += [f'{c} {min(values)} {max(values)} {sum(values)}' if values else f'{c} EMPTY 0', str(sum(values))]
        run('aggregate', lines, ans)
    commands, ans = [], []
    current = vals[:]
    for i in range(100):
        u = rng.randint(1,n)
        if i % 3 == 0:
            x = rng.choice([-10**9, 0, 10**9]); commands.append(f'U {u} {x}'); current[u] = x
        elif i % 3 == 1:
            commands.append(f'T {u}'); ans.append(sum(current[v] for v in range(1,n+1) if below(v,u)))
        else:
            commands.append(f'R {u}'); ans.append(sum(current[v] for v in path(root,u)[0]))
    run('dynamic', [f'{n} {len(commands)} {root}', ' '.join(map(str, vals[1:]))] + head[1:] + commands, ans)
    for labels in [[0]+[1]*n, [0]+list(range(1,n+1)), [0]+[rng.randrange(5) for _ in range(n)]]:
        qs = [(rng.randint(1,n),rng.choice([0,1,2,n,n+100])) for _ in range(65)]
        run('merge', [f'{n} {len(qs)} {root}', ' '.join(map(str,labels[1:]))] + head[1:] + [f'{u} {x}' for u,x in qs], [sum(labels[v]==x and below(v,u) for v in range(1,n+1)) for u,x in qs])

with tempfile.TemporaryDirectory(prefix='tree-queries-') as directory:
    tmp = pathlib.Path(directory)
    for name in NAMES:
        subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=all','-Wall','-Wextra','-Wshadow',str(ROOT/f'audit/package03-work/tree-query-{name}.cpp'),'-o',str(tmp/name)], check=True)
    for n in [1,2,3,8,9,25,70,200]:
        for kind in ['chain','star','random']:
            edges = [(v, v-1 if kind=='chain' else 1 if kind=='star' else rng.randrange(1,v)) for v in range(2,n+1)]
            for root in sorted({1,n,rng.randint(1,n)}): check(n,edges,root)
    # Empty query batches must emit nothing, including singleton trees.
    for name in ['basic','rmq','offline']: run(name,['1 0 1'],[])
    run('dynamic',['1 0 1','-1000000000'],[])
    run('merge',['1 0 1','7'],[])
    run('aggregate',['1 0 1 V','-1000000000'],[])
    # Deep trees exercise explicit traversal stacks and 64-bit sums without recursive DFS.
    n = 200000
    edges = [f'{u-1} {u}' for u in range(2,n+1)]
    run('basic',[f'{n} 3 1']+edges+[f'K {n} {n-1}',f'K {n} {n}',f'C {n} 1'],[1,0,f'1 {n-1}'])
    run('rmq',[f'{n} 2 1']+edges+[f'{n} 1',f'{n} {n}'],[f'1 {n-1}',f'{n} 0'])
    run('offline',[f'{n} 2 1']+edges+[f'{n} 1',f'{n} {n}'],[1,n])
    values = ' '.join(['1000000000']*n)
    run('dynamic',[f'{n} 3 1',values]+edges+['T 1',f'R {n}',f'T {n}'],[n*10**9,n*10**9,10**9])
    run('merge',[f'{n} 2 1',' '.join(['1']*n)]+edges+['1 1',f'{n} 1'],[n,1])
    run('aggregate',[f'{n} 2 1 E']+[e+' 1000000000' for e in edges]+[f'P 1 {n}',f'S 1 {n}'],[f'1 1000000000 1000000000 {(n-1)*10**9}',(n-1)*10**9])
report = {'status':'passed','seed':180029,'runs':dict(counts),'totalRuns':sum(counts.values()),'maxN':200000,'sanitizer':'undefined','programSha256':{name:hashlib.sha256((ROOT/f'audit/package03-work/tree-query-{name}.cpp').read_bytes()).hexdigest() for name in NAMES},'oracle':'independent parent walks, collected paths, direct descendant enumeration and mutable values'}
(ROOT/'audit/PACKAGE03-TREE-QUERY-CODE.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
