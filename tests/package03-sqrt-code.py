import json,random,subprocess,tempfile,itertools
from pathlib import Path
R=Path(__file__).resolve().parents[1];out=Path(tempfile.mkdtemp(prefix='sqrt-tests-'));rng=random.Random(2701);runs=0
for name in ['blocks','cases','batch','knapsack','strings','mo']:
 subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/sqrt-{name}.cpp'),'-o',str(out/name)],check=True)
def run(name,s):
 global runs
 p=subprocess.run([str(out/name)],input=s,text=True,capture_output=True,timeout=12);assert p.returncode==0,(name,p.stderr,s[:200]);runs+=1;return p.stdout.split()
def same(name,s,want):assert run(name,s)==list(map(str,want)),(name,s[:200],want)
a=[5,8,6,3,2,7,2,6,7,1,7,5,6,2,3,2]
same('blocks','16 4\n'+' '.join(map(str,a))+'\n2 0 4\n1 5 5\n2 3 14\n2 0 16\n',[22,46,70])
for t in range(90):
 n=rng.randint(1,45);a=[rng.randint(-10**12,10**12)for _ in range(n)];cur=a[:];ops=[];ans=[]
 for _ in range(60):
  if rng.randrange(2):
   i=rng.randrange(n);x=rng.randint(-10**12,10**12);ops.append(f'1 {i} {x}');cur[i]=x
  else:
   l=rng.randrange(n+1);r=rng.randrange(l,n+1);ops.append(f'2 {l} {r}');ans.append(sum(cur[l:r]))
 same('blocks',f'{n} {len(ops)}\n'+' '.join(map(str,a))+'\n'+'\n'.join(ops)+'\n',ans)
same('cases','4 4\nA F B A\nC E G E\nB D A F\nA C B D\n',[2])
for t in range(80):
 h=rng.randint(1,9);w=rng.randint(1,9);n=h*w;a=[rng.randrange(rng.randint(1,n+1))for _ in range(n)];pairs=[abs(i//w-j//w)+abs(i%w-j%w)for i in range(n)for j in range(i)if a[i]==a[j]]
 same('cases',f'{h} {w}\n'+' '.join(map(str,a))+'\n',[min(pairs,default=-1)])
for h,w in [(1,1),(1,2000),(40,50)]+[(rng.randint(1,9),rng.randint(1,9))for _ in range(70)]:
 order=list(range(h*w));rng.shuffle(order);black=[order[0]];ans=[]
 for v in order[1:]:ans.append(min(abs(v//w-u//w)+abs(v%w-u%w)for u in black));black.append(v)
 same('batch',f'{h} {w} {len(ans)} {order[0]//w} {order[0]%w}\n'+'\n'.join(f'{v//w} {v%w}'for v in order[1:])+'\n',ans)
same('knapsack','3\n1 3 3\n',[0,1,3,4,6,7])
for t in range(90):
 a=[rng.randint(1,20)for _ in range(rng.randint(0,16))];s={0}
 for x in a:s|={v+x for v in list(s)}
 same('knapsack',str(len(a))+'\n'+' '.join(map(str,a))+'\n',sorted(s))
same('knapsack','200000\n'+'1 '*200000+'\n',range(200001))
for t in range(90):
 s=''.join(rng.choices('ABC',k=rng.randrange(25)));words=[''.join(rng.choices('ABC',k=rng.randint(1,8)))for _ in range(rng.randrange(25))];dp=[1]+[0]*len(s)
 for r in range(1,len(s)+1):dp[r]=sum(dp[r-len(w)]for w in set(words)if len(w)<=r and s[r-len(w):r]==w)%1000000007
 for mode in ['HASH','EXACT']:same('strings',mode+'\n'+s+'\n'+str(len(words))+'\n'+'\n'.join(words)+'\n',[dp[-1]])
for mode in ['HASH','EXACT']:same('strings',mode+'\nABAB\n3\nA\nB\nAB\n',[4])
# Forced collision changes only a temporary test copy. 'AD' and 'BA' have the same base3 polynomial.
src=(R/'audit/package03-work/sqrt-strings.cpp').read_text().replace('M1 = 1000000007, M2 = 1000000009, B = 911382323','M1 = 97, M2 = 97, B = 3');(out/'weak.cpp').write_text(src)
subprocess.run(['g++','-std=c++17','-O1','-fsanitize=undefined','-fno-sanitize-recover=all',str(out/'weak.cpp'),'-o',str(out/'weak')],check=True)
same('weak','HASH\nBA\n1\nAD\n',[1]);same('weak','EXACT\nBA\n1\nAD\n',[0])
for t in range(90):
 n=rng.randint(1,70);a=[rng.choice([-2**63,2**63-1,rng.randint(-10,10)])for _ in range(n)];qs=[]
 for _ in range(rng.randrange(80)):
  l=rng.randrange(n+1);r=rng.randrange(l,n+1);qs.append((l,r))
 same('mo',f'{n} {len(qs)}\n'+' '.join(map(str,a))+'\n'+'\n'.join(f'{l} {r}'for l,r in qs)+'\n',[len(set(a[l:r]))for l,r in qs])
same('mo','9 2\n4 2 5 4 2 4 3 3 4\n1 5\n2 7\n',[3,4])
a=list(range(200000));same('mo',f'{len(a)} 3\n'+' '.join(map(str,a))+'\n0 200000\n100000 100000\n199999 200000\n',[200000,0,1])
same('batch','4 4 3 0 0\n2 1\n2 3\n0 2\n',[3,2,2])
for mode in ['HASH','EXACT']:same('strings',mode+'\n'+'A'*20000+'\n1\nA\n',[1])
same('cases','1 200000\n'+'A '*200000+'\n',[1])
same('cases','1 40000\n'+' '.join(map(str,range(40000)))+'\n',[-1])
report={'programs':6,'ubsan_oracle_executions':runs,'source_block_sums':[22,17,20,13],'source_updated_sums':[22,15,20,13],'source_query_3_14':46,'source_mo_ranges':[[1,5],[2,7]],'source_mo_answers':[3,4],'weak_hash_collision':['AD','BA'],'hash_count_collision':1,'verified_count':0,'all_passed':True}
(R/'audit/PACKAGE03-SQRT-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
