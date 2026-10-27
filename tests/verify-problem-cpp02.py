import itertools,json,random,subprocess,tempfile,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1];rows=json.load(open(root/'audit/PART04-REVIEWED-NEW-TASKS.json'));rng=random.Random(281002);reports=[]
def reverse_optimum(start,target):
 steps=0
 while target>start:
  target=target+1 if target%2 else target//2;steps+=1
 return steps+start-target
with tempfile.TemporaryDirectory()as tmp:
 for ref in ['580/B','115/A','520/B','977/E','706/C']:
  row=next(p for p in rows if p['ref']==ref);code=next(b['text']for s in row['editorial']['sections']for b in s['blocks']if b['type']=='code');src=Path(tmp)/'main.cpp';exe=Path(tmp)/'main';src.write_text(code);built=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wshadow',str(src),'-o',str(exe)],capture_output=True,text=True);assert built.returncode==0 and not built.stderr,built.stderr;cases=[]
  for _ in range(30):
   if ref=='580/B':
    n=rng.randint(1,10);limit=rng.randint(1,8);friends=[(rng.randrange(11),rng.randrange(21))for i in range(n)];expected=0
    for mask in range(1,1<<n):
     chosen=[p for i,p in enumerate(friends)if mask>>i&1]
     if max(m for m,f in chosen)-min(m for m,f in chosen)<limit:expected=max(expected,sum(f for m,f in chosen))
    inp=f'{n} {limit}\n'+'\n'.join(f'{m} {f}'for m,f in friends)+'\n'
   elif ref=='115/A':
    n=rng.randint(1,25);labels=rng.sample(range(n),n);parent=[-1]*n
    for i in range(1,n):
     if rng.randrange(3):parent[labels[i]]=labels[rng.randrange(i)]
    expected=0
    for v in range(n):
     length=0
     while v!=-1:length+=1;v=parent[v]
     expected=max(expected,length)
    inp=str(n)+'\n'+'\n'.join(str(p+1)if p!=-1 else'-1'for p in parent)+'\n'
   elif ref=='520/B':
    start=rng.randint(1,30);target=rng.randint(1,30);expected=reverse_optimum(start,target);inp=f'{start} {target}\n'
   elif ref=='977/E':
    n=rng.randint(1,7);edges={e for e in itertools.combinations(range(n),2)if rng.randrange(3)==0};labels=list(range(n))
    for a,b in edges:
     old,new=labels[b],labels[a];labels=[new if x==old else x for x in labels]
    expected=0
    for label in set(labels):
     group=[i for i in range(n)if labels[i]==label];actual={e for e in edges if e[0]in group}
     if len(group)<3:continue
     for order in itertools.permutations(group):
      cycle={tuple(sorted((order[i],order[(i+1)%len(order)])))for i in range(len(order))}
      if cycle==actual:expected+=1;break
    inp=f'{n} {len(edges)}\n'+'\n'.join(f'{a+1} {b+1}'for a,b in edges)+'\n'
   else:
    n=rng.randint(1,8);strings=[''.join(rng.choice('abc')for j in range(rng.randint(1,4)))for i in range(n)];cost=[rng.randint(0,10**9)for i in range(n)];expected=None
    for flags in itertools.product(range(2),repeat=n):
     chosen=[s[::-1]if flag else s for s,flag in zip(strings,flags)]
     if all(a<=b for a,b in zip(chosen,chosen[1:])):expected=min(expected if expected is not None else 10**30,sum(c*f for c,f in zip(cost,flags)))
    expected=-1 if expected is None else expected;inp=str(n)+'\n'+' '.join(map(str,cost))+'\n'+'\n'.join(strings)+'\n'
   cases.append((inp,expected))
  if ref=='580/B':boundary=[('2 5\n0 10\n5 20\n',20),('100000 1\n'+'1 1000000000\n'*100000,100000000000000),('1 1\n0 0\n',0)]
  elif ref=='115/A':boundary=[('1\n-1\n',1),('2000\n-1\n'+'\n'.join(map(str,range(1,2000)))+'\n',2000),('3\n-1\n-1\n-1\n',1)]
  elif ref=='520/B':boundary=[('10000 1\n',9999),('1 1\n',0),('1 10000\n',reverse_optimum(1,10000))]
  elif ref=='977/E':boundary=[('4 4\n1 2\n2 3\n3 1\n3 4\n',0),('6 6\n1 2\n2 3\n3 1\n4 5\n5 6\n6 4\n',2),('200000 199999\n'+'\n'.join(f'{i} {i+1}'for i in range(1,200000))+'\n',0)]
  else:boundary=[('2\n0 0\nb\na\n',-1),('3\n0 0 0\naa\naa\naa\n',0),('6\n'+'1000000000 '*6+'\nba\nac\nda\nae\nfa\nag\n',3000000000)]
  for inp,expected in cases+boundary:
   p=subprocess.run([str(exe)],input=inp,capture_output=True,text=True,timeout=5);assert p.returncode==0 and p.stdout.split()==[str(expected)],(ref,inp[:200],p.stdout,expected)
  reports.append({'source':'Codeforces','ref':ref,'code_sha256':hashlib.sha256(code.encode()).hexdigest(),'independent_oracles':30,'boundary_cases':3,'compiler_warnings':0,'status':'passed'})
(root/'audit/PART04-PROBLEM-CPP02.json').write_text(json.dumps({'status':'passed','seed':281002,'programs':reports,'official_samples':0,'oracle_methods':['all friend subsets','independent manager-chain walks','reverse-operation parity optimum','exact component-cycle edge sets over all permutations','all string orientations'],'limits':'Retained reviewed functional contracts;synthetic tests only,no fresh source/sample/judge-submission claim. Statements separately unready.'},indent=2)+'\n');print(reports)
