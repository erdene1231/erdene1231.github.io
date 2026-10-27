import itertools,json,math,random,subprocess,tempfile,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1];rows=json.load(open(root/'audit/PART04-REVIEWED-NEW-TASKS.json'));rng=random.Random(281001);results=[]
with tempfile.TemporaryDirectory()as tmp:
 for ref in ['977/C','455/A','189/A','431/C','698/A']:
  row=next(p for p in rows if p['ref']==ref);code=next(b['text']for s in row['editorial']['sections']for b in s['blocks']if b['type']=='code');src=Path(tmp)/'main.cpp';exe=Path(tmp)/'main';src.write_text(code);built=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wshadow',str(src),'-o',str(exe)],capture_output=True,text=True);assert built.returncode==0 and not built.stderr,built.stderr
  cases=[]
  for _ in range(25):
   if ref=='977/C':
    n=rng.randint(1,12);a=[rng.randint(1,10)for i in range(n)];k=rng.randint(0,n);possible=any(sum(v<=x for v in a)==k for x in range(1,12));inp=f'{n} {k}\n'+' '.join(map(str,a))+'\n';expected=possible
   elif ref=='455/A':
    a=[rng.randint(1,8)for i in range(rng.randint(1,12))];unique=sorted(set(a));expected=max(sum(v*a.count(v)for v in chosen)for mask in range(1<<len(unique))for chosen in[[v for i,v in enumerate(unique)if mask>>i&1]]if all(b-a!=1 for a,b in zip(chosen,chosen[1:])));inp=str(len(a))+'\n'+' '.join(map(str,a))+'\n'
   elif ref=='189/A':
    n=rng.randint(1,35);cuts=[1,rng.randint(1,20),rng.randint(1,20)];rng.shuffle(cuts);expected=max(i+j+(n-i*cuts[0]-j*cuts[1])//cuts[2]for i in range(n//cuts[0]+1)for j in range(n//cuts[1]+1)if n-i*cuts[0]-j*cuts[1]>=0 and(n-i*cuts[0]-j*cuts[1])%cuts[2]==0);inp=f'{n} '+' '.join(map(str,cuts))+'\n'
   elif ref=='431/C':
    n=rng.randint(1,10);k=rng.randint(1,5);d=rng.randint(1,k)
    def count(left,path):
     if left==0:return int(any(x>=d for x in path))
     return sum(count(left-x,path+[x])for x in range(1,min(left,k)+1))
    expected=count(n,[]);inp=f'{n} {k} {d}\n'
   else:
    a=[rng.randrange(4)for i in range(rng.randint(1,8))];expected=len(a)
    for schedule in itertools.product(range(3),repeat=len(a)):
     if all(activity==0 or(a[i]&(1<<(activity-1))and(i==0 or activity!=schedule[i-1]))for i,activity in enumerate(schedule)):expected=min(expected,schedule.count(0))
    inp=str(len(a))+'\n'+' '.join(map(str,a))+'\n'
   cases.append((inp,expected))
  if ref=='977/C':boundaries=[('1 0\n1\n',False),('3 2\n2 2 2\n',False),('1 1\n1000000000\n',True)]
  elif ref=='455/A':boundaries=[('100000\n'+'100000 '*100000+'\n',10000000000),('1\n1\n',1),('4\n1 3 3 5\n',12)]
  elif ref=='189/A':boundaries=[('4000 1 1 1\n',4000),('7 3 4 5\n',2),('5 5 5 5\n',1)]
  elif ref=='431/C':boundaries=[('1 100 100\n',0),('100 1 1\n',1),('100 100 1\n',pow(2,99,1000000007))]
  else:boundaries=[('100\n'+'0 '*100+'\n',100),('100\n'+'3 '*100+'\n',0),('3\n1 1 1\n',1)]
  for inp,expected in cases+boundaries:
   run=subprocess.run([str(exe)],input=inp,capture_output=True,text=True,timeout=5);assert run.returncode==0;tokens=run.stdout.split();assert len(tokens)==1;answer=int(tokens[0])
   if ref=='977/C':
    parsed=list(map(int,inp.split()));n,k=parsed[:2];a=parsed[2:];assert(answer==-1)==(not expected);assert answer==-1 or(1<=answer<=10**9 and sum(v<=answer for v in a)==k)
   else:assert answer==expected,(ref,inp,answer,expected)
  results.append({'source':'Codeforces','ref':ref,'code_sha256':hashlib.sha256(code.encode()).hexdigest(),'independent_oracles':25,'boundary_cases':3,'compiler_warnings':0,'status':'passed'})
(root/'audit/PART04-PROBLEM-CPP01.json').write_text(json.dumps({'status':'passed','seed':281001,'programs':results,'official_samples':0,'limits':'Retained reviewed contracts and original analysis;synthetic independent/boundary tests,not judge submissions. Statements remain unready.','oracle_methods':['threshold existence/direct counts','all nonadjacent value subsets','all feasible cut-count triples','all ordered weight sequences','all activity schedules']},indent=2)+'\n');print(results)
