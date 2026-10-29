import json,subprocess,tempfile,itertools,random,math
from pathlib import Path
R=Path(__file__).resolve().parents[1];rng=random.Random(70274)
A=[[3,7,9,2,7],[9,8,3,5,5],[1,7,9,8,5],[3,8,6,4,10],[6,3,9,7,8]]
def paths(n,m):
 for down in itertools.combinations(range(n+m-2),n-1):
  d=set(down);i=j=0;cells=[(0,0)];s=''
  for k in range(n+m-2):
   if k in d:i+=1;s+='D'
   else:j+=1;s+='R'
   cells.append((i,j))
  yield s,cells
names=['grid-max','grid-count','subset-table','subset-compact','value-table','value-compact','value-unbounded'];counts=dict(grid=0,subset=0,value=0,unbounded=0)
with tempfile.TemporaryDirectory()as td:
 p=Path(td)
 for k in names:subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/grid-knapsack-{k}.cpp'),'-o',str(p/k)],check=True)
 def run(k,s):return subprocess.check_output([str(p/k)],input=s,text=True,timeout=10).splitlines()
 def grid(a,g):
  n=len(g);m=len(g[0]);legal=[(s,c)for s,c in paths(n,m)if all(g[i][j]=='.'for i,j in c)]
  raw=f'{n} {m}\n'+'\n'.join(g)+'\n';assert int(run('grid-count',raw)[0])==len(legal)%1000000007
  out=run('grid-max',f'{n} {m}\n'+'\n'.join(' '.join(map(str,r))for r in a)+'\n'+'\n'.join(g)+'\n')
  if not legal:assert out==['IMPOSSIBLE']
  else:
   best=max(sum(a[i][j]for i,j in c)for s,c in legal);assert int(out[0])==best
   matches=[c for s,c in legal if s==out[1]];assert len(matches)==1 and sum(a[i][j]for i,j in matches[0])==best
  counts['grid']+=1
  return out
 for n in range(1,4):
  for m in range(1,4):
   for mask in range(1<<(n*m)):
    g=[''.join('*'if mask>>(i*m+j)&1 else'.'for j in range(m))for i in range(n)];a=[[rng.randint(-20,20)for j in range(m)]for i in range(n)];grid(a,g)
 sample=grid(A,['.....']*5);assert int(sample[0])==67
 for a,g in [([[-1000000000]*4]*3,['....']*3),([[1000000000]*4]*3,['....']*3),([[0]],['.'])]:grid(a,g)
 # Large count independently from binomial, not the recurrence under test.
 assert int(run('grid-count','50 50\n'+('\n'.join(['.'*50]*50))+'\n')[0])==math.comb(98,49)%1000000007
 for n in range(5):
  for w in itertools.product(range(4),repeat=n):
   sums={sum(w[i]for i in range(n)if mask>>i&1)for mask in range(1<<n)};s=str(n)+'\n'+' '.join(map(str,w))+'\n';want=[int(x in sums)for x in range(sum(w)+1)]
   for k in ['subset-table','subset-compact']:assert list(map(int,run(k,s)[0].split()))==want
   counts['subset']+=1
 subset_rows=[]
 for k in range(5):
  w=[1,3,3,5][:k];possible={sum(w[i]for i in range(k)if mask>>i&1)for mask in range(1<<k)};subset_rows.append([int(x in possible)for x in range(13)])
 def value(w,v,W):
  n=len(w);best=max(sum(v[i]for i in range(n)if mask>>i&1)for mask in range(1<<n)if sum(w[i]for i in range(n)if mask>>i&1)<=W)
  s=f'{n} {W}\n'+''.join(f'{a} {b}\n'for a,b in zip(w,v));a=run('value-table',s);b=run('value-compact',s)
  assert int(a[0])==int(b[0])==best
  take=list(map(int,a[2].split()));assert len(take)==int(a[1])==len(set(take)) and all(1<=i<=n for i in take)
  assert sum(w[i-1]for i in take)<=W and sum(v[i-1]for i in take)==best
  counts['value']+=1
 for n in range(5):
  for items in itertools.product([(1,1),(2,3),(2,-1),(3,5)],repeat=n):
   w=[a for a,b in items];v=[b for a,b in items]
   for W in range(7):value(w,v,W)
 for _ in range(120):
  n=rng.randrange(9);value([rng.randint(1,8)for _ in range(n)],[rng.randint(-10,10)*1000000000 for _ in range(n)],rng.randint(0,20))
 value([2,3,4],[3,4,5],5);value([1,1,1],[2000000000]*3,3)
 # Enumerate multiplicities, not a DP recurrence, for the unbounded reference.
 for _ in range(180):
  n=rng.randrange(5);W=rng.randrange(9);w=[rng.randint(1,5)for _ in range(n)];v=[rng.randint(-3,8)for _ in range(n)]
  best=max(sum(c[i]*v[i]for i in range(n))for c in itertools.product(*(range(W//x+1)for x in w))if sum(c[i]*w[i]for i in range(n))<=W)
  s=f'{n} {W}\n'+''.join(f'{a} {b}\n'for a,b in zip(w,v));assert int(run('value-unbounded',s)[0])==best;counts['unbounded']+=1
 assert run('value-compact','1 4\n2 3\n')==['3'];assert run('value-unbounded','1 4\n2 3\n')==['6']
 assert run('value-unbounded','1 10000\n1 1000000000\n')==['10000000000000']
 # Generate source-aligned tables independently from path/subset enumeration.
 max_table=[]
 for i in range(5):
  row=[]
  for j in range(5):row.append(max(sum(A[y][x]for y,x in c)for s,c in paths(i+1,j+1)))
  max_table.append(row)
 g=['....','.*..','....'];count_table=[[sum(all(g[y][x]=='.'for y,x in c)for s,c in paths(i+1,j+1))for j in range(4)]for i in range(3)]
 value_rows=[]
 for k in range(4):
  w=[2,3,4][:k];v=[3,4,5][:k];value_rows.append([max(sum(v[i]for i in range(k)if mask>>i&1)for mask in range(1<<k)if sum(w[i]for i in range(k)if mask>>i&1)<=c)for c in range(6)])
 e={'source_grid':A,'source_maximum':67,'source_max_table':max_table,'source_path':sample[1],'count_grid':g,'count_table':count_table,'source_weights':[1,3,3,5],'subset_rows':subset_rows,'missing_sums':[2,10],'value_weights':[2,3,4],'value_values':[3,4,5],'value_capacity':5,'value_rows':value_rows,'value_optimum':7,'single_item_direction_counterexample':{'weight':2,'value':3,'capacity':4,'zero_one':3,'unbounded':6}}
 (R/'audit/PACKAGE03-GRID-KNAPSACK-EXAMPLES.json').write_text(json.dumps(e,indent=2)+'\n')
 report={'status':'passed','Cpp17_programs':7,'UBSan':True,'counts':counts,'grid_oracle':'all monotone paths; exhaustive obstacle masks through3x3; signed/blocked/single-cell/source67','subset_oracle':'all subsets of every length0..4 weight tuple0..3, including zero/duplicates','value_oracle':'all subsets; verifies actual reconstruction IDs, weight and value','unbounded_oracle':'all bounded-by-capacity multiplicity tuples; positive weights, optional negative values','large_modular_count_binomial':True,'ll_grid_sums_and_values':True,'unbounded_1e13':True,'source_tables_independently_verified':True}
 (R/'audit/PACKAGE03-GRID-KNAPSACK-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
