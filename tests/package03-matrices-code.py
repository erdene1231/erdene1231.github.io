import collections,fractions,hashlib,itertools,json,math,pathlib,random,subprocess,tempfile
R=pathlib.Path(__file__).resolve().parents[1];rng=random.Random(231029);MOD=1000000007;counts=collections.Counter();names=['basic','power','determinant','recurrence','walks','minplus','kirchhoff']
E=[(0,3,4),(1,0,2),(1,4,1),(1,5,2),(2,1,4),(3,1,1),(5,2,3),(5,4,2)]
def lines(a):return '\n'.join(' '.join(map(str,r))for r in a)+'\n'
def mul(a,b):return [[sum(x*y for x,y in zip(r,c))for c in zip(*b)]for r in a]
def identity(n):return [[int(i==j)for j in range(n)]for i in range(n)]
def oracle_power(a,k):
 res=identity(len(a))
 for _ in range(k):res=[[x%MOD for x in r]for r in mul(res,a)]
 return res
def determinant(a):
 n=len(a);res=0
 for perm in itertools.permutations(range(n)):
  inversions=sum(perm[i]>perm[j]for i in range(n)for j in range(i+1,n));res+=(-1)**inversions*math.prod(a[i][perm[i]]for i in range(n))
 return res

def call(name,data):
 p=subprocess.run([str(tmp/name)],input=data,text=True,capture_output=True,timeout=30);assert p.returncode==0 and not p.stderr,(name,data[:200],p.stderr);counts[name]+=1;return p.stdout.splitlines()
def matrix(out):return [list(map(int,s.split()))for s in out]
def trees(n,edges):
 count=0
 for ids in itertools.combinations(range(len(edges)),n-1):
  par=list(range(n))
  def root(u):
   while par[u]!=u:u=par[u]
   return u
  for i in ids:
   a,b=edges[i];a,b=root(a),root(b)
   if a==b:break
   par[a]=b
  else:count+=1
 return count
with tempfile.TemporaryDirectory(prefix='matrices-code-')as folder:
 tmp=pathlib.Path(folder)
 for name in names:subprocess.run(['g++','-std=c++17','-O1','-g','-Wall','-Wextra','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/matrices-{name}.cpp'),'-o',str(tmp/name)],check=True)
 for _ in range(65):
  r,n,c=[rng.randrange(1,6)for _ in range(3)];a=[[rng.randrange(-20,21)for _ in range(n)]for _ in range(r)];b=[[rng.randrange(-20,21)for _ in range(c)]for _ in range(n)];d=[[rng.randrange(-20,21)for _ in range(n)]for _ in range(r)];x=rng.randrange(-10,11);out=call('basic',f'{r} {n} {c} {x}\n'+lines(a)+lines(b)+lines(d));pos=0
  for ans in [[[a[i][j]+d[i][j]for j in range(n)]for i in range(r)],[[x*v for v in row]for row in a],list(map(list,zip(*a))),mul(a,b)]:
   rr,cc=map(int,out[pos].split());pos+=1;assert [rr,cc]==[len(ans),len(ans[0])]and matrix(out[pos:pos+rr])==ans;pos+=rr
 a=[[10**6]*30 for _ in range(30)];out=call('basic','30 30 30 1000000\n'+lines(a)*3);assert matrix(out[-30:])==[[30*10**12]*30 for _ in range(30)]
 for _ in range(70):
  n=rng.randrange(1,5);a=[[rng.randrange(-10,11)for _ in range(n)]for _ in range(n)];k=rng.randrange(9);assert matrix(call('power',f'{n} {k}\n'+lines(a)))==oracle_power(a,k)
 assert matrix(call('power','2 3\n2 5\n1 4\n'))==[[48,165],[33,114]]
 assert matrix(call('power','1 1000000000000000000\n-9223372036854775808\n'))==[[pow(-2**63,10**18,MOD)]]
 cases=[[[3,4],[1,6]],[[2,4,3],[5,1,6],[7,2,4]],[[0]],[[1]],[[2,4],[1,2]],[[0,1],[1,0]],[[20 if i==j else -20 for j in range(6)]for i in range(6)]]
 cases +=[[[rng.randrange(-5,6)for _ in range(n)]for _ in range(n)]for n in [1,2,3,4,5]for _ in range(9)]
 for a in cases:
  n=len(a);out=call('determinant',f'{n}\n'+lines(a));d=determinant(a);assert int(out[0])==d
  if d==0:assert out[1]=='SINGULAR'
  else:
   inv=[[fractions.Fraction(x)for x in row.split()]for row in out[1:]];assert mul(a,inv)==identity(n)and mul(inv,a)==identity(n)
 for _ in range(90):
  k=rng.randrange(1,7);n=rng.randrange(50);f=[rng.randrange(-8,9)for _ in range(k)];c=[rng.randrange(-8,9)for _ in range(k)];seq=f[:]
  while len(seq)<n+k:seq.append(sum(c[j]*seq[-1-j]for j in range(k))%MOD)
  out=matrix(call('recurrence',f'{k} {n}\n'+' '.join(map(str,f))+'\n'+' '.join(map(str,c))+'\n'))[0];assert out==[x%MOD for x in seq[n:n+k]]
 assert call('recurrence','2 6\n0 1\n1 1\n')==['8 13 ']
 assert int(call('recurrence','1 1000000000000000000\n3\n-2\n')[0])==3*pow(-2,10**18,MOD)%MOD
 for _ in range(90):
  n=rng.randrange(1,6);k=rng.randrange(8);edges=[(rng.randrange(n),rng.randrange(n),rng.randrange(-5,6))for _ in range(rng.randrange(13))];data=f'{n} {len(edges)} {k}\n';a=[[0]*n for _ in range(n)]
  for u,v,w in edges:a[u][v]+=1
  assert matrix(call('walks',data+''.join(f'{u+1} {v+1}\n'for u,v,w in edges)))==oracle_power(a,k)
  expected=[[None]*n for _ in range(n)]
  for s in range(n):
   dp=[None]*n;dp[s]=0
   for step in range(k):
    q=[None]*n
    for u,v,w in edges:
     if dp[u]is not None:q[v]=dp[u]+w if q[v]is None else min(q[v],dp[u]+w)
    dp=q
   expected[s]=dp
  got=[[None if x=='INF'else int(x)for x in row.split()]for row in call('minplus',data+''.join(f'{u+1} {v+1} {w}\n'for u,v,w in edges))];assert got==expected
 source_count=matrix(call('walks','6 8 4\n'+''.join(f'{u+1} {v+1}\n'for u,v,w in E)));assert source_count==[[0,0,1,1,1,0],[2,0,0,0,2,2],[0,2,0,0,0,0],[0,2,0,0,0,0],[0,0,0,0,0,0],[0,0,1,1,1,0]]
 source_min=[[None if v=='INF'else int(v)for v in row.split()]for row in call('minplus','6 8 4\n'+''.join(f'{u+1} {v+1} {w}\n'for u,v,w in E))];assert source_min==[[None,None,10,11,9,None],[9,None,None,None,8,9],[None,11,None,None,None,None],[None,8,None,None,None,None],[None]*6,[None,None,12,13,11,None]]
 assert call('minplus','1 1 1000000000000\n1 1 -1000000\n')==['-1000000000000000000 ']
 assert call('minplus','1 0 1\n')==['INF '];assert call('minplus','1 0 0\n')==['0 ']
 graphcases=[(1,[]),(4,[(0,1),(0,2),(0,3),(2,3)]),(2,[(0,1)]*5),(3,[(0,0),(0,1),(1,2),(2,2)])]
 graphcases +=[(n,[(rng.randrange(n),rng.randrange(n))for _ in range(rng.randrange(10))])for n in range(1,7)for _ in range(9)]
 for n,edges in graphcases:
  expected=trees(n,edges)
  for root in range(n):assert int(call('kirchhoff',f'{n} {len(edges)} {root+1}\n'+''.join(f'{u+1} {v+1}\n'for u,v in edges))[0])==expected%MOD
 n=20;edges=list(itertools.combinations(range(n),2));assert int(call('kirchhoff',f'{n} {len(edges)} 7\n'+''.join(f'{u+1} {v+1}\n'for u,v in edges))[0])==pow(n,n-2,MOD)
 n=150;edges=[(i,i+1)for i in range(n-1)];assert int(call('kirchhoff',f'{n} {len(edges)} 80\n'+''.join(f'{u+1} {v+1}\n'for u,v in edges))[0])==1
 n=80;assert matrix(call('power',f'{n} 2\n'+lines([[MOD-1]*n for _ in range(n)])))==[[n]*n for _ in range(n)]
 edges=[(i,j)for i in range(n)for j in range(n)];out=call('minplus',f'{n} {len(edges)} 1000000000000\n'+''.join(f'{u+1} {v+1} -1000000\n'for u,v in edges));assert matrix(out)==[[-10**18]*n for _ in range(n)]
 report={'programs':7,'UBSan_oracle_executions':sum(counts.values()),'cases':dict(counts),'oracles':['exact rectangular arithmetic and transpose','repeated Python matrix multiplication','Leibniz permutation determinant and exact rational inverse identities','direct recurrence DP','fixed-edge-count walk DP including loops/multiedges/negative weights','independent spanning-edge subsets and every principal cofactor'],'source_checks':{'cube_matrix':[[48,165],[33,114]],'det2':14,'det3':81,'Fibonacci6_7':[8,13],'walk_count_2_5_length4':source_count[1][4],'mincost_2_5_length4':source_min[1][4],'spanning_trees':3},'boundaries':{'rect_dim':30,'rect_product_entry':30*10**12,'power_exponent':10**18,'minplus_exponent':10**12,'minplus_weight':-10**6,'negative_and_LL_MIN_input_normalization':True,'determinant_n':6,'Kirchhoff_complete_n':20,'Kirchhoff_dimension':150,'dense_power_minplus_dimension':80},'source_sha256':{name:hashlib.sha256((R/f'audit/package03-work/matrices-{name}.cpp').read_bytes()).hexdigest()for name in names}}
 (R/'audit/PACKAGE03-MATRICES-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
