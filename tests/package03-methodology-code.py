import collections,itertools,json,math,random,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];rng=random.Random(41872)
with tempfile.TemporaryDirectory()as root:
 t=Path(root);names=['missing','piles','debug-solve','debug-stress','subset-brute','subset-meet']
 for name in names:subprocess.run(['g++','-std=c++17','-O1','-g','-Wall','-Wextra','-Wshadow','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/methodology-{name}.cpp'),'-o',str(t/name)],check=True)
 def run(name,s):
  p=subprocess.run([str(t/name)],input=s,text=True,capture_output=True,timeout=40);assert p.returncode==0,(name,p.stderr);assert not p.stderr,(name,p.stderr);return p.stdout
 # Batch harness calls the actual supplied missing-sum function unchanged.
 src=(R/'audit/package03-work/methodology-missing.cpp').read_text().split('int main() {')[0]+'''int main(){int q;cin>>q;while(q--){int n;cin>>n;vector<ll>a(n);for(ll &x:a)cin>>x;cout<<missing(a)<<'\\n';}}''';(t/'h.cpp').write_text(src);subprocess.run(['g++','-std=c++17','-O1','-fsanitize=undefined','-fno-sanitize-recover=all',str(t/'h.cpp'),'-o',str(t/'h')],check=True)
 arrays=[a for n in range(8)for a in itertools.product(range(1,5),repeat=n)];inp=str(len(arrays))+'\n'+''.join(str(len(a))+'\n'+' '.join(map(str,a))+'\n'for a in arrays);p=subprocess.run([str(t/'h')],input=inp,text=True,capture_output=True,check=True);assert not p.stderr;lines=p.stdout.splitlines();assert len(lines)==len(arrays)
 for a,l in zip(arrays,lines):
  sums={0}
  for x in a:sums|={s+x for s in sums}
  want=next(x for x in range(1,sum(a)+2)if x not in sums);assert int(l)==want
 assert run('missing','4\n1 1 3 7\n').strip()=='6';assert run('missing','4\n1 1 3 6\n').strip()=='12';assert run('missing','2\n2 1\n').strip()=='4';assert run('missing','0\n').strip()=='1'
 a=[1<<i for i in range(30)]+[10**9]*199970;want=sum(a)+1;assert int(run('missing','200000\n'+' '.join(map(str,a))+'\n'))==want
 reachable={(0,0)};q=collections.deque([(0,0)])
 while q:
  a,b=q.popleft()
  for da,db in [(2,1),(1,2)]:
   x,y=a+da,b+db
   if x<=30 and y<=30 and(x,y)not in reachable:reachable.add((x,y));q.append((x,y))
 pairs=list(itertools.product(range(31),repeat=2));pairs+= [(10**9,500000000),(999999999,999999999),(10**9,10**9)];lines=run('piles',str(len(pairs))+'\n'+''.join(f'{a} {b}\n'for a,b in pairs)).splitlines();assert len(lines)==len(pairs)
 for (a,b),line in zip(pairs,lines):
  want=(a,b)in reachable if a<=30 and b<=30 else ((2*a-b)>=0 and (2*b-a)>=0 and(2*a-b)%3==0 and(2*b-a)%3==0);assert(line=='YES')==want
 out=run('debug-stress','41872 500\n');assert '1\n0 \nexpected 1 actual 0\n'in out;assert out.endswith('checked 20030\n');assert out==run('debug-stress','41872 500\n')
 for a in [[0],[-1,1],[2,1,0],[-10**9,10**9],*[ [rng.randrange(-10**9,10**9+1)for _ in range(rng.randrange(1,16))]for _ in range(100)]]:
  n=len(a);want=sum(sum(a[l:r])%n==0 for l in range(n)for r in range(l+1,n+1));assert int(run('debug-solve',str(n)+'\n'+' '.join(map(str,a))+'\n'))==want
 assert int(run('debug-solve','200000\n'+'0 '*200000+'\n'))==200000*200001//2
 # Deliberate bug is educational; assert its reduced case is truly failing.
 asan={'compiled':False,'smoke_passed':False};b=t/'asan'
 subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=address,undefined','-fno-sanitize-recover=all',str(R/'audit/package03-work/methodology-debug-solve.cpp'),'-o',str(b)],check=True);asan['compiled']=True
 p=subprocess.run([str(b)],input='2\n-1 1\n',text=True,capture_output=True);asan['smoke_passed']=p.returncode==0 and p.stdout.strip()=='1' and not p.stderr
 if not asan['smoke_passed']:asan['runtime_failure_excerpt']=p.stderr[:300]
 subsetcases=[([],0),([],1),([0,0],0),([1,2,2,3],4),([2,4,5,9],15),([2,4,5,9],10),([-1,1,0],0)]+[([rng.randrange(-8,9)for _ in range(rng.randrange(0,15))],rng.randrange(-20,21))for _ in range(140)]
 for a,target in subsetcases:
  n=len(a);want=sum(sum(a[i]for i in range(n)if mask>>i&1)==target for mask in range(1<<n));inp=f'{n} {target}\n'+' '.join(map(str,a))+'\n';assert int(run('subset-brute',inp))==want;assert int(run('subset-meet',inp))==want
 assert int(run('subset-brute','22 0\n'+'0 '*22+'\n'))==2**22
 for a,target,want in [([0]*40,0,2**40),([1]*40,20,math.comb(40,20)),([1,-1]*20,0,math.comb(40,20)),([10**9]*40,4*10**10,1),([-10**9]*40,-4*10**10,1)]:assert int(run('subset-meet',f'40 {target}\n'+' '.join(map(str,a))+'\n'))==want
 data={'status':'passed','CXX17_UBSan_programs':6,'compiler_warnings_flags':['-Wall','-Wextra','-Wshadow'],'missing_exhaustive_arrays':len(arrays),'missing_independent_actual_sum_set':True,'piles_cases':len(pairs),'piles_independent_reachability_BFS':True,'debug_exhaustive_arrays':19530,'debug_seeded_random_arrays':500,'reproducible_seed_and_real_shrunk_counterexample':True,'debug_solution_external_cases':104,'max_n_missing_and_debug':200000,'ASan':asan,'subset_exhaustive_oracle_cases':len(subsetcases),'brute_max_n':22,'meet_max_n':40,'duplicates_empty_signed_and_64bit_counts':True};(R/'audit/PACKAGE03-METHODOLOGY-CODE.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data))
