import itertools,json,random,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];rng=random.Random(808182)
names=['fixed-sum','positive-count','deque-extrema','neighbors','histogram'];cnt=dict(window=0,positive=0,neighbors=0,histogram=0)
def exact(a,x):return sum(sum(a[l:r])==x for l in range(len(a))for r in range(l+1,len(a)+1))
def nearest(a):
 out=[]
 for right,strict in [(False,True),(False,False),(True,True),(True,False)]:
  row=[]
  for i,v in enumerate(a):
   js=range(i+1,len(a))if right else range(i-1,-1,-1)
   row.append(next((j+1 for j in js if ((a[j]>v if strict else a[j]>=v)if right else(a[j]<v if strict else a[j]<=v))),0))
  out.append(row)
 return out
with tempfile.TemporaryDirectory()as td:
 p=Path(td)
 for k in names:subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/window-stack-{k}.cpp'),'-o',str(p/k)],check=True)
 def run(k,a,extra=None):return subprocess.check_output([str(p/k)],input=str(len(a))+(' '+str(extra)if extra is not None else'')+'\n'+' '.join(map(str,a))+'\n',text=True,timeout=20).splitlines()
 def wins(a,k):
  want=[a[i:i+k]for i in range(len(a)-k+1)]if 1<=k<=len(a)else[]
  assert list(map(int,run('fixed-sum',a,k)[0].split()))==[sum(w)for w in want]
  z=run('deque-extrema',a,k);assert len(z)==2 and list(map(int,z[0].split()))==[min(w)for w in want]and list(map(int,z[1].split()))==[max(w)for w in want]
  cnt['window']+=1
 def near(a):
  assert[list(map(int,s.split()))for s in run('neighbors',a)]==nearest(a);cnt['neighbors']+=1
 for n in range(5):
  for a in itertools.product([-2,0,2],repeat=n):
   near(a)
   for k in range(n+2):wins(a,k)
 for _ in range(200):
  a=[rng.randint(-10,10)for _ in range(rng.randrange(21))];near(a);wins(a,rng.randrange(len(a)+2))
 for n in range(6):
  for a in itertools.product([1,2,3],repeat=n):
   for x in range(sum(a)+2):
    assert int(run('positive-count',a,x)[0])==exact(a,x);cnt['positive']+=1
 assert run('positive-count',[4,-1],3)==['0']and exact([4,-1],3)==1
 assert run('positive-count',[0,0],0)==['2']and exact([0,0],0)==3
 for n in range(6):
  for a in itertools.product(range(4),repeat=n):
   best=max([min(a[l:r])*(r-l)for l in range(n)for r in range(l+1,n+1)]or[0]);assert int(run('histogram',a)[0])==best;cnt['histogram']+=1
 for _ in range(120):
  a=[rng.randint(0,10)for _ in range(rng.randrange(18))];best=max([min(a[l:r])*(r-l)for l in range(len(a))for r in range(l+1,len(a)+1)]or[0]);assert int(run('histogram',a)[0])==best;cnt['histogram']+=1
 wins([10**9]*10,10);wins([-10**9]*10,10);near([-10**18,10**18,10**18,-10**18]);assert run('histogram',[10**9]*200000)==['200000000000000'];assert run('positive-count',[1]*200000,1)==['200000'];assert int(run('fixed-sum',[10**9]*200000,200000)[0])==200000000000000
 for a in [list(range(200000)),list(range(200000,0,-1)),[7]*200000]:
  z=run('neighbors',a);assert len(z)==4 and all(len(row.split())==len(a)for row in z)
 assert run('deque-extrema',[5]*200000,100000)[0].split()==['5']*100001
 sw=[1,3,2,5,1,1,2,3];count=[2,1,3,2,1];m=[2,1,4,5,3,4,1,2];src=[1,3,4,2,5,3,4,2];old=[2,5,1,4,4,3]
 def stacktrace(a):
  st=[];rows=[]
  for i,x in enumerate(a):
   popped=[]
   while st and a[st[-1]]>=x:popped.append(st.pop())
   ans=st[-1]+1 if st else 0;st.append(i);rows.append([i,x,popped,ans,st[:],[a[j]for j in st]])
  return rows
 def deqtrace(a,k):
  q=[];rows=[]
  for i,x in enumerate(a):
   expired=[];popped=[]
   while q and q[0]<=i-k:expired.append(q.pop(0))
   while q and a[q[-1]]>=x:popped.append(q.pop())
   q.append(i)
   if i>=k-1:rows.append([i-k+1,i,expired,popped,q[:],[a[j]for j in q],a[q[0]]])
  return rows
 h=[2,1,5,6,2,3];left=[next((j for j in range(i-1,-1,-1)if h[j]<h[i]),-1)for i in range(len(h))];right=[next((j for j in range(i+1,len(h))if h[j]<h[i]),len(h))for i in range(len(h))]
 e={'source_sum_array':sw,'source_sum_target':8,'source_sum_window':[2,4],'old_count_array':count,'old_count_target':3,'old_count_answer':3,'source_min_array':m,'source_k':4,'source_minima':[min(m[i:i+4])for i in range(5)],'source_maxima':[max(m[i:i+4])for i in range(5)],'source_deque_trace':deqtrace(m,4),'source_stack_array':src,'source_stack_trace':stacktrace(src),'old_stack_array':old,'old_stack_trace':stacktrace(old),'ties':{'a':[2,2,2],'answers':nearest([2,2,2])},'histogram':h,'histogram_boundaries':[[i,h[i],left[i],right[i],right[i]-left[i]-1,h[i]*(right[i]-left[i]-1)]for i in range(len(h))],'histogram_area':10,'negative_counterexample':{'a':[4,-1],'x':3,'positive_only_code':0,'correct':1},'zero_counterexample':{'a':[0,0],'x':0,'positive_only_code':2,'correct':3}}
 assert e['source_minima']==[1,1,3,1,1]and e['source_maxima']==[5,5,5,5,4]and run('positive-count',count,3)==['3']
 (R/'audit/PACKAGE03-WINDOW-STACK-EXAMPLES.json').write_text(json.dumps(e,indent=2)+'\n')
 report={'status':'passed','Cpp17_programs':5,'UBSan':True,'cases':cnt,'window_oracle':'all slices including invalid/full/singleton widths and signed values','positive_oracle':'all subarrays for every positive tuple length0..5 over1,2,3 and every target0..sum+1','neighbors_oracle':'linear nearest scan for strict and weak previous-smaller/next-greater','histogram_oracle':'all intervals and their minimum height','actual_invalid_domain_counterexamples':True,'stress_n':200000,'ll_sums_and_areas':True,'source_and_old_example_traces_verified':True,'production_writes':0}
 (R/'audit/PACKAGE03-WINDOW-STACK-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
