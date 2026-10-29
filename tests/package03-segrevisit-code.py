import json,random,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];out=Path(tempfile.mkdtemp(prefix='seg-revisit-'));rng=random.Random(2801);runs=0
names=['lazy','poly','sparse','persistent','maps','two-d']
def compile(name,src):
 p=out/(name+'.cpp');p.write_text(src);subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=all',str(p),'-o',str(out/name)],check=True)
for name in names:compile(name,(R/f'audit/package03-work/segrevisit-{name}.cpp').read_text())
def same(name,s,want):
 global runs
 p=subprocess.run([str(out/name)],input=s,text=True,capture_output=True,timeout=15);assert p.returncode==0,(name,p.stderr,s[:300]);runs+=1;assert p.stdout.split()==list(map(str,want)),(name,s[:500],p.stdout,want)
a=[5,8,6,3,2,7,2,6,7,1,7,5,6,2,3,2]
same('lazy','16 5\n'+' '.join(map(str,a))+'\n3 5 14\n1 5 14 2\n3 0 16\n3 10 14\n3 5 14\n',[43,90,28,61])
same('lazy','5 8\n2 1 3 4 5\n1 1 4 2\n3 0 5\n2 2 5 1\n3 0 5\n1 0 5 -3\n3 0 5\n2 0 5 0\n3 0 5\n',[21,8,-7,0])
for _ in range(100):
 n=rng.randint(1,50);a=[rng.randint(-10**12,10**12)for i in range(n)];cur=a[:];ops=[];ans=[]
 for j in range(100):
  l=rng.randrange(n+1);r=rng.randrange(l,n+1);t=rng.randint(1,3)
  if t==3:ops.append(f'3 {l} {r}');ans.append(sum(cur[l:r]));continue
  x=rng.choice([0,rng.randint(-10**6,10**6)])if t==1 else rng.choice([0,rng.randint(-10**12,10**12)])
  ops.append(f'{t} {l} {r} {x}')
  for i in range(l,r):cur[i]=x if t==2 else cur[i]+x
 same('lazy',f'{n} {len(ops)}\n'+' '.join(map(str,a))+'\n'+'\n'.join(ops)+'\n',ans)
same('lazy','200000 4\n'+'1000000000000 '*200000+'\n1 0 200000 1000000\n3 0 200000\n2 0 200000 0\n3 0 200000\n',[200000*1000001000000,0])
MOD=1000000007
for _ in range(110):
 n=rng.randint(1,40);k=rng.randrange(6);a=[rng.randint(-10**12,10**12)for i in range(n)];cur=[x%MOD for x in a];ops=[];ans=[]
 for j in range(65):
  l=rng.randrange(n+1);r=rng.randrange(l,n+1)
  if rng.randrange(3)==0:ops.append(f'2 {l} {r}');ans.append(sum(cur[l:r])%MOD)
  else:
   c=[rng.randint(-10**12,10**12)for j in range(k+1)];ops.append(f'1 {l} {r} '+' '.join(map(str,c)))
   for i in range(l,r):cur[i]=(cur[i]+sum(c[j]*(i-l)**j for j in range(k+1)))%MOD
 same('poly',f'{n} {len(ops)} {k}\n'+' '.join(map(str,a))+'\n'+'\n'.join(ops)+'\n',ans)
same('poly','5 3 1\n0 0 0 0 0\n1 1 5 1 1\n2 0 5\n2 3 5\n',[10,7])
for _ in range(90):
 n=rng.choice([1,16,10**12,rng.randint(2,100)]);a={};ops=[];ans=[]
 for j in range(100):
  if rng.randrange(2):i=rng.randrange(n);x=rng.randint(-10**12,10**12);a[i]=x;ops.append(f'1 {i} {x}')
  else:l=rng.randrange(n+1);r=rng.randrange(l,n+1);ops.append(f'2 {l} {r}');ans.append(sum(x for i,x in a.items()if l<=i<r))
 same('sparse',f'{n} {len(ops)}\n'+'\n'.join(ops)+'\n',ans)
for _ in range(100):
 n=rng.randint(1,45);versions=[[0]*n];ops=[];ans=[]
 for j in range(100):
  v=rng.randrange(len(versions))
  if rng.randrange(2):
   i=rng.randrange(n);x=rng.randint(-10**12,10**12);b=versions[v][:];b[i]=x;versions.append(b);ops.append(f'1 {v} {i} {x}');ans.append(len(versions)-1)
  else:l=rng.randrange(n+1);r=rng.randrange(l,n+1);ops.append(f'2 {v} {l} {r}');ans.append(sum(versions[v][l:r]))
 same('persistent',f'{n} {len(ops)}\n'+'\n'.join(ops)+'\n',ans)
for _ in range(100):
 n=rng.randint(1,45);a=[rng.choice([-2**63,2**63-1,rng.randrange(7)])for i in range(n)];cur=a[:];ops=[];ans=[]
 for j in range(100):
  x=rng.choice([-2**63,2**63-1,rng.randrange(10)])
  if rng.randrange(2):i=rng.randrange(n);cur[i]=x;ops.append(f'1 {i} {x}')
  else:l=rng.randrange(n+1);r=rng.randrange(l,n+1);ops.append(f'2 {l} {r} {x}');ans.append(cur[l:r].count(x))
 same('maps',f'{n} {len(ops)}\n'+' '.join(map(str,a))+'\n'+'\n'.join(ops)+'\n',ans)
same('maps','8 1\n3 1 2 3 1 1 1 2\n2 1 6 1\n',[3])
for _ in range(100):
 n=rng.randint(1,9);m=rng.randint(1,10);a=[[rng.randint(-10**9,10**9)for c in range(m)]for r in range(n)];cur=[row[:]for row in a];ops=[];ans=[]
 for j in range(65):
  if rng.randrange(2):r=rng.randrange(n);c=rng.randrange(m);x=rng.randint(-10**9,10**9);cur[r][c]=x;ops.append(f'1 {r} {c} {x}')
  else:
   l=rng.randrange(n+1);r=rng.randrange(l,n+1);cl=rng.randrange(m+1);cr=rng.randrange(cl,m+1);ops.append(f'2 {l} {r} {cl} {cr}');ans.append(sum(sum(row[cl:cr])for row in cur[l:r]))
 same('two-d',f'{n} {m} {len(ops)}\n'+'\n'.join(' '.join(map(str,row))for row in a)+'\n'+'\n'.join(ops)+'\n',ans)
same('two-d','4 4 2\n7 6 1 6\n8 7 5 2\n3 9 7 1\n8 5 3 8\n2 0 4 0 4\n2 0 2 0 2\n',[86,28])
same('two-d','500 500 1\n'+('1000000000 '*500+'\n')*500+'2 0 500 0 500\n',[250000000000000])
# Direct invariants not visible through main: reads allocate no sparse nodes; versions immutable; queries insert no absent map keys.
for name,main in [('sparse',r'''int main(){Sparse st(1000000000000LL);st.update(1,0,st.n,3,5000000000LL);auto n=st.tree.size();for(int i=0;i<1000;i++)assert(st.query(1,0,st.n,0,st.n)==5000000000LL);assert(st.tree.size()==n);cout<<"OK";}'''),('persistent',r'''int main(){Persistent st(16);int a=st.assign(0,3,5000000000LL),b=st.assign(a,10,-7000000000LL),c=st.assign(a,3,9);auto n=st.tree.size();assert(st.query(st.roots[0],0,16,0,16)==0);assert(st.query(st.roots[a],0,16,0,16)==5000000000LL);assert(st.query(st.roots[b],0,16,0,16)==-2000000000LL);assert(st.query(st.roots[c],0,16,0,16)==9);assert(st.tree.size()==n);cout<<"OK";}'''),('maps',r'''int main(){Segtree st(vector<ll>{3,1,2,3,1,1,1,2});auto before=st.tree;assert(st.query(1,0,8,0,8,99)==0);assert(st.tree==before);st.update(1,0,8,0,3);assert(st.tree==before);cout<<"OK";}''')]:
 src=(R/f'audit/package03-work/segrevisit-{name}.cpp').read_text().rsplit('int main()',1)[0];compile(name+'-invariant',src+main);same(name+'-invariant','',['OK'])
report={'programs':6,'ubsan_oracle_executions':runs,'all_passed':True,'source_initial_sum':72,'source_recursive_query_5_14':43,'source_after_add_5_14_by2_sum':90,'source_next_query_10_14':28,'source_map_count_1_in_1_6':3,'source_2d_sum':86,'all_polynomial_degrees_0_to5_tested':True,'modulus':MOD,'sparse_domain':10**12,'old_persistent_versions_and_forks':True,'read_only_queries_allocate_no_nodes_or_map_keys':True,'maximum_2d':[500,500]}
(R/'audit/PACKAGE03-SEGREVISIT-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
