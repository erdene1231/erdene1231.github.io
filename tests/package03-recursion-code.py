import json,math,subprocess,tempfile,itertools,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory()as td:
 p=Path(td)
 for name in ['factorial','hanoi','parentheses']:subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/recursion-{name}.cpp'),'-o',str(p/name)],check=True)
 for n in range(21):assert int(subprocess.check_output([str(p/'factorial')],input=str(n)+'\n',text=True))==math.factorial(n)
 bfs=[]
 for n in range(6):
  start=(0,)*n;goal=(2,)*n;q=collections.deque([start]);d={start:0}
  while q:
   s=q.popleft()
   if s==goal:break
   tops=[next((i for i,x in enumerate(s)if x==peg),n)for peg in range(3)]
   for a in range(3):
    for b in range(3):
     if a!=b and tops[a]<tops[b]:
      t=list(s);t[tops[a]]=b;t=tuple(t)
      if t not in d:d[t]=d[s]+1;q.append(t)
  bfs.append(d[goal])
 totalmoves=0;source=None
 for n in list(range(11))+[20]:
  file=p/f'hanoi-{n}.out'
  with file.open('w')as f:subprocess.run([str(p/'hanoi')],input=str(n)+'\n',text=True,stdout=f,check=True,timeout=30)
  pegs=[list(range(n,0,-1)),[],[]];cnt=0;sample=[]
  with file.open()as f:
   printed=int(next(f))
   for line in f:
    a,b=map(int,line.split());assert 1<=a<=3 and 1<=b<=3 and a!=b
    x=pegs[a-1].pop();assert not pegs[b-1]or x<pegs[b-1][-1];pegs[b-1].append(x);cnt+=1
    if n==3:sample.append([a,b])
  assert cnt==printed==2**n-1 and pegs==[[],[],list(range(n,0,-1))]
  if n<=5:assert cnt==bfs[n]
  if n==3:source=sample
  totalmoves+=cnt
 totalstrings=0
 for n in range(11):
  out=subprocess.check_output([str(p/'parentheses')],input=str(n)+'\n',text=True).splitlines();want=math.comb(2*n,n)//(n+1);assert len(out)==want and len(set(out))==want
  for s in out:
   depth=0;assert len(s)==2*n
   for c in s:depth+=1 if c=='('else-1;assert depth>=0
   assert depth==0
  if n<=7:
   brute=set()
   for chars in itertools.product('()',repeat=2*n):
    depth=0;ok=True
    for c in chars:
     depth+=1 if c=='('else-1
     if depth<0:ok=False;break
    if ok and depth==0:brute.add(''.join(chars))
   assert set(out)==brute
  totalstrings+=len(out)
 # Verify the actual shared-reference generator restores its caller's string.
 h='#define main lessonMain\n#include "'+str(R/'audit/package03-work/recursion-parentheses.cpp')+'"\n#undef main\nint main(){for(int n=0;n<=10;n++){string s;ostringstream out;auto old=cout.rdbuf(out.rdbuf());generate(0,0,n,s);cout.rdbuf(old);assert(s.empty());}{string s="(";ostringstream out;auto old=cout.rdbuf(out.rdbuf());generate(1,0,2,s);cout.rdbuf(old);assert(s=="(");assert(out.str()=="(())\\n()()\\n");}{string s="((";ostringstream out;auto old=cout.rdbuf(out.rdbuf());generate(2,0,2,s);cout.rdbuf(old);assert(s=="((");assert(out.str()=="(())\\n");}cout<<"restored";}';(p/'restore.cpp').write_text(h);subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',str(p/'restore.cpp'),'-o',str(p/'restore')],check=True,capture_output=True);assert subprocess.check_output([str(p/'restore')],text=True)=='restored'
 examples={'factorial_call_n':[4,3,2,1,0],'factorial_return_values':[1,1,2,6,24],'hanoi_three_moves':source,'hanoi_two_peg_states':[['2 1','–','–'],['2','1','–'],['–','1','2'],['–','–','2 1']],'balanced_n2':['(())','()()'],'hanoi_small_BFS_optima':bfs}
 (R/'audit/PACKAGE03-RECURSION-EXAMPLES.json').write_text(json.dumps(examples,ensure_ascii=False,indent=2)+'\n')
 report={'status':'passed','Cpp17_programs':3,'UBSan':True,'factorial_cases':21,'factorial_max_n':20,'hanoi_cases':12,'hanoi_max_n':20,'legal_hanoi_moves_checked':totalmoves,'independent_BFS_optima':bfs,'balanced_n_cases':11,'balanced_strings_verified':totalstrings,'exhaustive_binary_word_oracle_through_n':7,'actual_shared_string_restoration_cases':13,'largest_int_move_count':2**20-1,'ll_factorial20':math.factorial(20),'no_unbounded_recursion_test':True}
 (R/'audit/PACKAGE03-RECURSION-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
