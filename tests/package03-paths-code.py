"""Independent exhaustive/reference checks; source figure walks are verified as well."""
import collections,hashlib,itertools,json,pathlib,random,subprocess,tempfile
R=pathlib.Path(__file__).resolve().parents[1];rng=random.Random(191029);runs=collections.Counter()
NAMES=['euler','backtrack','hamilton','debruijn','knight']
def execute(name,data):
 p=subprocess.run([str(tmp/name)],input=data,text=True,capture_output=True,timeout=15)
 assert p.returncode==0 and not p.stderr,(name,p.returncode,p.stderr)
 runs[name]+=1;return p.stdout.strip()
def euler_exists(n,edges,d):
 adj=[[]for _ in range(n)]
 for i,(a,b)in enumerate(edges):
  adj[a].append((b,i))
  if not d:adj[b].append((a,i))
 def dfs(u,mask):
  if mask==(1<<len(edges))-1:return True
  return any(not(mask>>i&1)and dfs(v,mask|1<<i)for v,i in adj[u])
 return any(dfs(s,0)for s in range(n))
def valid_euler(seq,edges,d):
 left=collections.Counter((a,b)if d else tuple(sorted((a,b)))for a,b in edges)
 for a,b in zip(seq,seq[1:]):
  k=(a,b)if d else tuple(sorted((a,b)));assert left[k]>0,(seq,edges);left[k]-=1
 assert len(seq)==len(edges)+1 and not any(left.values())
def hamilton_exists(n,edges,d,c):
 if c and n<3:return False
 ed=set(edges)
 if not d:ed|={(b,a)for a,b in edges}
 for perm in itertools.permutations(range(1,n)if c else range(n)):
  p=(0,)+perm if c else perm
  if all(e in ed for e in zip(p,p[1:]))and(not c or(p[-1],p[0])in ed):return True
 return False
def valid_hamilton(seq,n,edges,d,c):
 assert len(seq)==n+c and len(set(seq[:n]))==n and set(seq[:n])==set(range(n))
 if c:assert seq[-1]==seq[0]
 ed=set(edges)
 if not d:ed|={(b,a)for a,b in edges}
 assert all(e in ed for e in zip(seq,seq[1:]))
def knight_valid(board,start):
 n=len(board);pos={v:(x,y)for x,row in enumerate(board)for y,v in enumerate(row)}
 assert set(pos)==set(range(1,n*n+1))and pos[1]==start
 for k in range(1,n*n):assert sorted(abs(a-b)for a,b in zip(pos[k],pos[k+1]))==[1,2]
with tempfile.TemporaryDirectory(prefix='paths-code-')as directory:
 tmp=pathlib.Path(directory)
 for name in NAMES:subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=all','-Wall','-Wextra',str(R/f'audit/package03-work/paths-{name}.cpp'),'-o',str(tmp/name)],check=True)
 for d in [0,1]:
  cases=[(1,[]),(1,[(0,0)]*4),(4,[(0,0),(2,2)]),(4,[(0,1),(0,1),(2,3),(2,3)])]
  cases +=[(rng.randrange(1,6),[])for _ in range(2)]
  for _ in range(160):
   n=rng.randrange(1,6);cases.append((n,[(rng.randrange(n),rng.randrange(n))for _ in range(rng.randrange(9))]))
  for n,edges in cases:
   result=execute('euler',f'{n} {len(edges)} {d}\n'+''.join(f'{a+1} {b+1}\n'for a,b in edges));possible=euler_exists(n,edges,d)
   assert(result!='IMPOSSIBLE')==possible,(n,edges,d,result)
   if possible:valid_euler([int(x)-1 for x in result.split()],edges,d)
 for n in range(1,8):
  for d,c in itertools.product([0,1],repeat=2):
   for _ in range(9):
    edges=[(a,b)for a in range(n)for b in range(n)if a!=b and(d or a<b)and rng.random()<0.4]
    expected=hamilton_exists(n,edges,d,c)
    data=f'{n} {len(edges)} {d} {c}\n'+''.join(f'{a+1} {b+1}\n'for a,b in edges)
    for name in ['backtrack','hamilton']:
     result=execute(name,data);assert(result!='IMPOSSIBLE')==expected,(name,n,d,c,edges,result)
     if expected:valid_hamilton([int(x)-1 for x in result.split()],n,edges,d,c)
 for n in range(1,6):
  for k in range(1,5):
   seq=execute('debruijn',f'{n} {k}\n');words=[seq[i:i+n]for i in range(len(seq)-n+1)]
   expected={''.join(x)for x in itertools.product('0123456789'[:k],repeat=n)}
   assert len(seq)==k**n+n-1 and len(words)==len(set(words))==len(expected) and set(words)==expected
 assert execute('debruijn','3 2\n')=='0001011100'
 # Output validation is independent of Warnsdorff's ordering; all 64 starts on the 8x8 board.
 for n,starts in [(1,[(0,0)]),(2,[(0,0)]),(3,[(0,0),(1,1)]),(4,[(0,0)]),(5,[(0,0)]),(6,[(0,0)]),(8,list(itertools.product(range(8),repeat=2)))]:
  for start in starts:
   result=execute('knight',f'{n} {start[0]+1} {start[1]+1}\n')
   if n in [2,3,4]:assert result=='IMPOSSIBLE'
   else:knight_valid([list(map(int,row.split()))for row in result.splitlines()],start)
 # Exact supplied figure walks, not just existence.
 E=[(1,2),(1,4),(4,5),(5,2),(2,3),(3,5)]
 valid_euler([2,1,4,5,2,3,5],E,0)
 valid_euler([2,3,5,4,1,2,5],[(1,2),(2,3),(3,5),(5,4),(4,1),(2,5)],1)
 E7=[(1,2),(2,3),(3,1),(2,5),(5,6),(6,2),(6,3),(3,4),(4,7),(7,6)]
 valid_euler([1,2,5,6,3,4,7,6,2,3,1],E7,0)
 knight_valid([[1,4,11,16,25],[12,17,2,5,10],[3,20,7,24,15],[18,13,22,9,6],[21,8,19,14,23]],(0,0))
 # Linear Euler and bounded exponential DP stress; edge multiplicity and loops retain IDs.
 n=200000;edges=[(i,i+1)for i in range(n-1)];result=execute('euler',f'{n} {n-1} 0\n'+''.join(f'{a+1} {b+1}\n'for a,b in edges));valid_euler([int(x)-1 for x in result.split()],edges,0)
 result=execute('hamilton','20 19 1 0\n'+''.join(f'{i} {i+1}\n'for i in range(1,20)));assert list(map(int,result.split()))==list(range(1,21))
 seq=execute('debruijn','20 2\n');assert len(seq)==2**20+19 and len({seq[i:i+20]for i in range(2**20)})==2**20
report={'status':'passed','seed':191029,'programs':5,'runs':dict(runs),'totalRuns':sum(runs.values()),'sanitizer':'undefined','maxEulerN':200000,'maxHamiltonDPn':20,'deBruijnMaxEdges':2**20,'knight8x8Starts':64,'oracle':'exhaustive edge-ID trails/permutations; independent word coverage and tour legality; exact source walks','sha256':{name:hashlib.sha256((R/f'audit/package03-work/paths-{name}.cpp').read_bytes()).hexdigest()for name in NAMES}}
(R/'audit/PACKAGE03-PATHS-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
