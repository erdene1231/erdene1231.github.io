"""Source-edge contracts and independent oracles for six graph/construction programs."""
import json,subprocess,random,time,hashlib,collections,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];out=Path('/workspace/native-problem-editorials/batch04-code');out.mkdir(parents=True,exist_ok=True);refs=['typical90_l','typical90_m','typical90_u','typical90_af','typical90_ag','typical90_ah'];samples=json.loads((ROOT/'audit/PART04-STATEMENT-REFERENCE-SAMPLES.json').read_text())['records'];rng=random.Random(394);report=[]
for ref in refs:
 src=ROOT/'audit/native-problem-editorials/code'/f'{ref}.cpp';exe=out/ref;subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=undefined','-Wall','-Wextra','-Werror',str(src),'-o',str(exe)],check=True);runs=0;naive=0;edge_checks=[]
 def run(text):
  global runs
  p=subprocess.run([str(exe)],input=text,text=True,capture_output=True,timeout=30);assert p.returncode==0 and not p.stderr,(ref,p.stderr);runs+=1;return p.stdout.split()
 record=next(p for p in samples if p['ref']==ref)
 for s in record['samples']:assert run(s['input'])==s['output'].split(),(ref,'source sample')
 start=time.monotonic()
 if ref=='typical90_l':
  for _ in range(200):
   h,w=rng.randint(1,6),rng.randint(1,6);q=rng.randint(1,80);white=list(range(h*w));active=set();ops=[];expected=[]
   for __ in range(q):
    if white and rng.random()<.45:
     idx=rng.randrange(len(white));u=white.pop(idx);active.add(u);ops.append(f'1 {u//w+1} {u%w+1}')
    else:
     u=rng.randrange(h*w);v=u if rng.random()<.3 else rng.randrange(h*w);ops.append(f'2 {u//w+1} {u%w+1} {v//w+1} {v%w+1}');seen=set();queue=collections.deque()
     if u in active:seen.add(u);queue.append(u)
     while queue:
      cell=queue.popleft();r,c=divmod(cell,w)
      for nr,nc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
       nxt=nr*w+nc
       if 0<=nr<h and 0<=nc<w and nxt in active and nxt not in seen:seen.add(nxt);queue.append(nxt)
     expected.append('Yes'if v in seen else'No')
   assert run(f'{h} {w}\n{q}\n'+'\n'.join(ops)+'\n')==expected;naive+=1
  assert run('1 1\n3\n2 1 1 1 1\n1 1 1\n2 1 1 1 1\n')==['No','Yes'];edge_checks.append('same white cell No; same painted cell Yes')
  paint=[f'1 {u//2000+1} {u%2000+1}'for u in range(99999)];assert run('2000 2000\n100000\n'+'\n'.join(paint)+'\n2 1 1 50 1999\n')==['Yes']
 elif ref=='typical90_m':
  for _ in range(180):
   n=rng.randint(2,8);pairs={tuple(sorted((rng.randrange(v),v)))for v in range(1,n)}
   for a in range(n):
    for b in range(a+1,n):
     if rng.random()<.2:pairs.add((a,b))
   edges=[(a,b,rng.randint(1,10000))for a,b in pairs];arcs=edges+[(b,a,c)for a,b,c in edges];expected=[]
   for via in range(n):
    inf=10**15;d=[[inf]*n for __ in range(2)];d[int(via==0)][0]=0
    for __ in range(2*n-1):
     for seen in range(2):
      for a,b,c in arcs:d[int(seen or b==via)][b]=min(d[int(seen or b==via)][b],d[seen][a]+c)
    expected.append(str(d[1][n-1]))
   text=f'{n} {len(edges)}\n'+'\n'.join(f'{a+1} {b+1} {c}'for a,b,c in edges)+'\n';assert run(text)==expected;naive+=1
  assert run('4 3\n1 2 314\n1 3 159\n1 4 265\n')==['265','893','583','265'];edge_checks.append('source star requires repeated road/vertex: via leaf2 is1->2->1->4')
  n=100000;assert run(f'{n} {n-1}\n'+'\n'.join(f'{i} {i+1} 10000'for i in range(1,n))+'\n')==[str((n-1)*10000)]*n
 elif ref=='typical90_u':
  for _ in range(250):
   n=rng.randint(2,10);edges=[(a,b)for a in range(n)for b in range(n)if a!=b and rng.random()<.15]
   if not edges:edges=[(0,1)]
   if rng.random()<.6:edges.append(rng.choice(edges))
   reach=[[i==j for j in range(n)]for i in range(n)]
   for a,b in edges:reach[a][b]=True
   for k in range(n):
    for i in range(n):
     for j in range(n):reach[i][j]|=reach[i][k]and reach[k][j]
   expected=sum(reach[i][j]and reach[j][i]for i in range(n)for j in range(i+1,n));assert run(f'{n} {len(edges)}\n'+'\n'.join(f'{a+1} {b+1}'for a,b in edges)+'\n')==[str(expected)];naive+=1
  n=100000;cycle='\n'.join(f'{i} {i+1}'for i in range(1,n))+'\n100000 1\n';assert run(f'{n} {2*n}\n'+cycle*2)==[str(n*(n-1)//2)];assert run(f'{n} {n-1}\n'+'\n'.join(f'{i} {i+1}'for i in range(1,n))+'\n')==['0'];edge_checks.append('parallel edges/disconnected random graphs; ll pair product4999950000; iterative100000-depth traversal')
 elif ref=='typical90_af':
  for _ in range(150):
   n=rng.randint(1,8);a=[[rng.randint(1,1000)for __ in range(n)]for ___ in range(n)];bad={(i,j)for i in range(n)for j in range(i+1,n)if rng.random()<.35};inf=10**9;dp=[[inf]*n for __ in range(1<<n)]
   for i in range(n):dp[1<<i][i]=a[i][0]
   for mask in range(1,1<<n):
    leg=mask.bit_count()
    if leg==n:continue
    for last in range(n):
     if dp[mask][last]==inf:continue
     for nxt in range(n):
      if mask>>nxt&1 or tuple(sorted((last,nxt)))in bad:continue
      dp[mask|1<<nxt][nxt]=min(dp[mask|1<<nxt][nxt],dp[mask][last]+a[nxt][leg])
   expected=min(dp[-1]);expected=-1 if expected==inf else expected;text=f'{n}\n'+'\n'.join(' '.join(map(str,row))for row in a)+f'\n{len(bad)}\n'+'\n'.join(f'{i+1} {j+1}'for i,j in bad)+'\n';assert run(text)==[str(expected)];naive+=1
  matrix='\n'.join([' '.join(['1000']*10)]*10);assert run('10\n'+matrix+'\n0\n')==['10000'];bad=list(itertools.combinations(range(1,11),2));assert run('10\n'+matrix+f'\n{len(bad)}\n'+'\n'.join(f'{a} {b}'for a,b in bad)+'\n')==['-1'];edge_checks.append('N1, directed runner/leg matrix indexing, forbidden pairs symmetric; first and last legs not adjacent')
 elif ref=='typical90_ag':
  for h in range(1,5):
   for w in range(1,5):
    best=0
    for mask in range(1<<(h*w)):
     if mask.bit_count()<=best:continue
     ok=True
     for r in range(h-1):
      for c in range(w-1):
       if sum(mask>>(rr*w+cc)&1 for rr in [r,r+1]for cc in[c,c+1])>1:ok=False;break
      if not ok:break
     if ok:best=mask.bit_count()
    assert run(f'{h} {w}\n')==[str(best)];naive+=1
  for h,w,best in [(1,100,100),(100,1,100),(100,100,2500),(99,99,2500),(2,100,50),(100,2,50)]:assert run(f'{h} {w}\n')==[str(best)]
  edge_checks.append('H1 or W1 has no contained2x2; every such cell may be lit')
 else:
  for _ in range(250):
   n=rng.randint(1,40);k=rng.randint(1,n);a=[rng.choice([1,10**9,rng.randint(1,12)])for __ in range(n)];best=0
   for l in range(n):
    seen=set()
    for r in range(l,n):
     seen.add(a[r])
     if len(seen)<=k:best=max(best,r-l+1)
   assert run(f'{n} {k}\n'+' '.join(map(str,a))+'\n')==[str(best)];naive+=1
  n=100000
  for k,a,expected in [(1,list(range(1,n+1)),1),(1,[10**9]*n,n),(n,list(range(1,n+1)),n)]:assert run(f'{n} {k}\n'+' '.join(map(str,a))+'\n')==[str(expected)]
  edge_checks.append('frequency zero erasure, K1, KN, repeated and extreme values')
 report.append({'ref':ref,'program_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'official_samples':len(record['samples']),'independent_naive_cases':naive,'source_edge_contract_checks':edge_checks,'limit_stress_passed':True,'oracle_and_stress_wall_seconds':round(time.monotonic()-start,3),'ubsan_warnings_as_errors':True,'program_runs':runs})
result={'status':'passed','records':report,'total_program_runs':sum(r['program_runs']for r in report),'limits':'Code correctness evidence only. Passing uses independent expanded-state Bellman-Ford; SCC uses transitive closure, painting BFS, relay subsetDP, lighting full masks, and sliding-window exhaustive subarrays. Bilingual/native content needs separate review.'};(ROOT/'audit/native-problem-editorials/batch04-code-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
