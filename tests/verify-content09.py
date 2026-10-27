"""Independent min-coin/assignment/tree/subset oracles; semantic choice-string checking."""
import collections,hashlib,itertools,json,random,subprocess,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1];rows=json.load(open(root/'audit/PART04-REVIEWED-NEW-TASKS.json'));records=json.load(open(root/'audit/PART04-CONTENT09-SAMPLES.json'));rng=random.Random(91027);results=[]
def coin_optimum(target,coins):
 dp=[0]+[1000000]*target
 for total in range(1,target+1):dp[total]=min((dp[total-value]+1 for value in coins if value<=total),default=1000000)
 return dp[target]
def relay_optimum(time,pairs):
 n=len(time);forbidden={frozenset(p)for p in pairs};dp={(1<<runner,runner):time[runner][0]for runner in range(n)}
 for count in range(1,n):
  next_dp={}
  for (mask,last),cost in dp.items():
   for runner in range(n):
    if not mask>>runner&1 and frozenset((last,runner))not in forbidden:
     state=(mask|1<<runner,runner);next_dp[state]=min(next_dp.get(state,10**9),cost+time[runner][count])
  dp=next_dp
 return min(dp.values(),default=-1)
def tree_sum(n,edges):
 neighbors=[[]for i in range(n)]
 for a,b in edges:neighbors[a].append(b);neighbors[b].append(a)
 answer=0
 for source in range(n):
  distance=[-1]*n;distance[source]=0;queue=collections.deque([source])
  while queue:
   vertex=queue.popleft()
   for other in neighbors[vertex]:
    if distance[other]<0:distance[other]=distance[vertex]+1;queue.append(other)
  answer+=sum(distance[source+1:])
 return answer
def bitonic_optimum(values):
 best=0
 for mask in range(1,1<<len(values)):
  candidate=[v for i,v in enumerate(values)if mask>>i&1];falling=False;valid=True
  for first,second in zip(candidate,candidate[1:]):
   if first==second or(falling and second>first):valid=False;break
   if second<first:falling=True
  if valid:best=max(best,len(candidate))
 return best
def relay_input(time,pairs):
 return str(len(time))+'\n'+'\n'.join(' '.join(map(str,row))for row in time)+'\n'+str(len(pairs))+'\n'+'\n'.join(f'{a+1} {b+1}'for a,b in pairs)+'\n'
def tree_input(n,edges):return str(n)+'\n'+'\n'.join(f'{a+1} {b+1}'for a,b in edges)+'\n'
def choices_input(pairs,target):return f'{len(pairs)} {target}\n'+'\n'.join(f'{a} {b}'for a,b in pairs)+'\n'
def check_choice_output(inp,output,possible):
 tokens=list(map(int,inp.split()));n,target=tokens[:2];pairs=list(zip(tokens[2::2],tokens[3::2]));out=output.split()
 assert len(out)==1,(inp,output)
 if not possible:assert out[0]=='Impossible',(inp,output);return
 choice=out[0];assert len(choice)==n and set(choice)<=set('AB'),(inp,output)
 assert sum(pair[letter=='B']for pair,letter in zip(pairs,choice))==target,(inp,output)
with tempfile.TemporaryDirectory()as tmp:
 for record in records:
  suffix=record['ref'].split('_')[-1];row=next(p for p in rows if p['ref']==record['ref']);code=next(b['text']for s in row['editorial']['sections']for b in s['blocks']if b['type']=='code');src=Path(tmp)/'main.cpp';exe=Path(tmp)/'main';src.write_text(code)
  built=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wshadow',str(src),'-o',str(exe)],capture_output=True,text=True);assert built.returncode==0 and not built.stderr,built.stderr
  cases=[(s['input'],s['output'])for s in record['samples']]
  for _ in range(40):
   if suffix=='p':
    while True:
     coins=rng.sample(range(1,31),3);target=rng.randint(1,200);expected=coin_optimum(target,coins)
     if expected<1000000:break
    inp=f'{target}\n'+' '.join(map(str,coins))+'\n'
   elif suffix=='af':
    n=rng.randint(1,7);time=[[rng.randint(1,1000)for j in range(n)]for i in range(n)];all_pairs=list(itertools.combinations(range(n),2));pairs=rng.sample(all_pairs,rng.randint(0,len(all_pairs)));expected=relay_optimum(time,pairs);inp=relay_input(time,pairs)
   elif suffix=='am':
    n=rng.randint(2,16);labels=rng.sample(range(n),n);edges=[(labels[i],labels[rng.randrange(i)])for i in range(1,n)];rng.shuffle(edges);inp=tree_input(n,edges);expected=tree_sum(n,edges)
   elif suffix=='bd':
    n=rng.randint(1,10);pairs=[(rng.randint(1,30),rng.randint(1,30))for i in range(n)];target=rng.randint(1,200);possible=any(sum(choice)==target for choice in itertools.product(*pairs));inp=choices_input(pairs,target);expected='possible'if possible else'Impossible'
   else:
    n=rng.randint(1,13);values=[rng.randint(1,n)for i in range(n)];expected=bitonic_optimum(values);inp=str(n)+'\n'+' '.join(map(str,values))+'\n'
   cases.append((inp,str(expected)))
  if suffix=='p':focused=[('6\n1 3 4\n','2'),('12\n9 6 1\n','2'),('9999\n1000000000 999999999 1\n','9999'),('1000000000\n1000000000 999999999 1\n','1')]
  elif suffix=='af':focused=[(relay_input([[1000]],[]),'1000'),(relay_input([[1000]*10 for i in range(10)],[]),'10000'),(relay_input([[1]*10 for i in range(10)],list(itertools.combinations(range(10),2))),'-1'),(relay_input([[1 if i==j else 1000 for j in range(3)]for i in range(3)],[(0,2)]),'3')]
  elif suffix=='am':focused=[(tree_input(100000,[(i-1,i)for i in range(1,100000)]),str((100000**3-100000)//6)),(tree_input(100000,[(0,i)for i in range(1,100000)]),str(99999**2)),('2\n2 1\n','1')]
  elif suffix=='bd':focused=[(choices_input([(1000,2000)]*100,100000),'possible'),(choices_input([(1,1)]*100,1),'Impossible'),('1 1\n100000 1\n','possible'),('2 4\n2 2\n2 2\n','possible')]
  else:focused=[('300000\n'+'1 '*300000+'\n','1'),('300000\n'+' '.join(map(str,range(1,300001)))+'\n','300000'),('300000\n'+' '.join(map(str,range(300000,0,-1)))+'\n','300000'),('300000\n'+' '.join(map(str,[*range(1,150001),*range(150000,0,-1)]))+'\n','299999')]
  cases+=focused
  for inp,out in cases:
   run=subprocess.run([str(exe)],input=inp,capture_output=True,text=True,timeout=10);assert run.returncode==0,(suffix,run.stderr)
   if suffix=='bd':check_choice_output(inp,run.stdout,out.strip()!='Impossible')
   else:assert run.stdout.split()==out.split(),(suffix,inp[:200],run.stdout[:200],out[:200])
  results.append({'ref':record['ref'],'code_sha256':hashlib.sha256(code.encode()).hexdigest(),'official_samples':len(record['samples']),'independent_oracles':40,'focused_boundary_cases':len(focused),'warnings':0,'status':'passed','output_check':'semantic AB plan validity/existence;any valid plan accepted'if suffix=='bd'else'whitespace-normalized exact output'})
(root/'audit/PART04-CONTENT09-CPP.json').write_text(json.dumps({'status':'passed','seed':91027,'programs':results,'oracle_methods':['small target min-coin DP','subset/end-runner assignment DP','all-source BFS unordered distance sums','all per-day binary choices plus semantic returned-plan validation','all subsequences with explicit strict up-then-down predicate'],'limits':'Local executable checks; no judge submission.'},indent=2)+'\n');print(results)
