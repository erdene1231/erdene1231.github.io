import json,subprocess,tempfile,itertools,random,functools,bisect
from pathlib import Path
R=Path(__file__).resolve().parents[1];rng=random.Random(701718)
@functools.lru_cache(None)
def merge_cost(a):
 if len(a)<2:return 0
 return min(a[i]+a[i+1]+merge_cost(a[:i]+(a[i]+a[i+1],)+a[i+2:])for i in range(len(a)-1))
def subseq(a,strict):
 best=0
 for mask in range(1<<len(a)):
  s=[x for i,x in enumerate(a)if mask>>i&1]
  if all((x<y if strict else x<=y)for x,y in zip(s,s[1:])):best=max(best,len(s))
 return best
names=['lis-quadratic','lis-fast','lnds-fast','interval-merge'];nc=mc=0
with tempfile.TemporaryDirectory()as td:
 p=Path(td)
 for k in names:subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/lis-interval-{k}.cpp'),'-o',str(p/k)],check=True)
 def run(k,a):return subprocess.check_output([str(p/k)],input=str(len(a))+'\n'+' '.join(map(str,a))+'\n',text=True,timeout=20).splitlines()
 def check(a):
  global nc
  for k in names[:3]:
   strict=k!='lnds-fast';out=run(k,a);ids=[int(v)-1 for v in out[1].split()];assert int(out[0])==len(ids)==subseq(a,strict)
   assert all(0<=i<len(a)for i in ids)and all(i<j for i,j in zip(ids,ids[1:]))
   assert all((a[i]<a[j]if strict else a[i]<=a[j])for i,j in zip(ids,ids[1:]))
  nc+=1
 for n in range(6):
  for a in itertools.product([-1,0,1,2],repeat=n):check(a)
 for _ in range(200):check([rng.randint(-8,8)for _ in range(rng.randrange(11))])
 for a in [[6,2,5,1,7,4,8,3],[-10**18,10**18,-10**18,0,10**18],[2,2,2]]:check(a)
 for a,want in [([7]*200000,1),(list(range(200000)),200000),(list(range(200000,0,-1)),1)]:assert int(run('lis-fast',a)[0])==want
 assert int(run('lnds-fast',[7]*200000)[0])==200000
 assert int(run('lis-quadratic',list(range(2000)))[0])==2000
 def check_merge(a):
  global mc
  out=run('interval-merge',a);want=merge_cost(tuple(a));assert int(out[0])==want
  blocks=[(i,i,x)for i,x in enumerate(a)];total=0
  for line in out[1:]:
   l,k,r=[int(x)-1 for x in line.split()];i=next(i for i,v in enumerate(blocks)if v[:2]==(l,k));assert i+1<len(blocks)and blocks[i+1][:2]==(k+1,r)
   val=blocks[i][2]+blocks[i+1][2];total+=val;blocks[i:i+2]=[(l,r,val)]
  assert len(out)-1==max(0,len(a)-1) and total==want
  assert blocks==([(0,len(a)-1,sum(a))]if a else[])
  mc+=1
 for n in range(6):
  for a in itertools.product(range(4),repeat=n):check_merge(a)
 for _ in range(100):check_merge([rng.randint(0,20)for _ in range(rng.randrange(8))])
 for a in [[10,20,30,40],[6,4,4,6],[1,100,1],[10**9]*7]:check_merge(a)
 assert merge_cost((10,20,30,40))==190 and merge_cost((6,4,4,6))==40
 stress=run('interval-merge',[10**9]*400);assert int(stress[0])>2**31
 a=[6,2,5,1,7,4,8,3];dp=[];tails=[];trace=[]
 for i,x in enumerate(a):
  dp.append(1+max([dp[j]for j in range(i)if a[j]<x]or[0]));j=bisect.bisect_left(tails,x)
  if j==len(tails):tails.append(x)
  else:tails[j]=x
  trace.append(tails[:])
 rows=[]
 for length in range(1,5):
  for l in range(5-length):
   r=l+length-1;rows.append([l,r,sum([10,20,30,40][l:r+1]),merge_cost(tuple([10,20,30,40][l:r+1]))])
 e={'LIS_source_array':a,'LIS_source_end_lengths':dp,'LIS_source_length':4,'LIS_source_indices_one_based':[2,3,5,7],'LIS_tail_trace':trace,'tails_not_a_subsequence':[1,3,7,8],'duplicate_example':{'a':[2,2,2],'strict':1,'nondecreasing':3},'merge_source_array':[10,20,30,40],'merge_interval_rows':rows,'merge_source_cost':190,'greedy_adjacent_counterexample':{'a':[6,4,4,6],'greedy':42,'optimum':40},'nonadjacent_not_allowed':[1,100,1]}
 (R/'audit/PACKAGE03-LIS-INTERVAL-EXAMPLES.json').write_text(json.dumps(e,indent=2)+'\n')
 report={'status':'passed','programs':4,'Cpp17':True,'UBSan':True,'array_cases_all_three_programs':nc,'exhaustive_array_lengths':'0..5 over -1,0,1,2','array_oracle':'enumerated index subsets; validates reconstructed original indices and strict/nondecreasing values','merge_cases':mc,'exhaustive_merge_lengths':'0..5 over0,1,2,3','merge_oracle':'enumerate every first adjacent merge recursively, independent of last-split DP','merge_reconstruction':'every printed original interval must join two actually adjacent current blocks; verify cost and operation count','fast_stress_n':200000,'quadratic_stress_n':2000,'interval_stress_n':400,'ll_comparison_extremes_and_merge_costs':True,'lesson_complete':False,'production_writes':0}
 (R/'audit/PACKAGE03-LIS-INTERVAL-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
