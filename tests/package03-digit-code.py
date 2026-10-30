import json,random,subprocess,tempfile,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];src=ROOT/'audit/package03-work/digit-dp.cpp';rng=random.Random(1618033);MAX=10**18
valid=lambda x:all(a!=b for a,b in zip(str(x),str(x)[1:]))
pref=[];count=0
for x in range(200001):count+=valid(x);pref.append(count)
def rank_count(x):
 if x<0:return 0
 if x==0:return 1
 ds=list(map(int,str(x)));ans=1+sum(9**k for k in range(1,len(ds)));prev=-1
 for i,d in enumerate(ds):
  for c in range(1 if i==0 else 0,d):
   if c!=prev:ans+=9**(len(ds)-i-1)
  if d==prev:return ans
  prev=d
 return ans+1
assert all(rank_count(x)==pref[x]for x in range(10001))
cases=[];expected=[]
def add(a,b,kind):
 assert 0<=a<=b<=MAX
 answer=pref[b]-(pref[a-1]if a else 0)if b<=200000 else sum(valid(x)for x in range(a,b+1))if b-a<=300 else rank_count(b)-rank_count(a-1)
 cases.append((a,b,kind));expected.append(answer)
for b in range(10001):add(0,b,'dense_prefix_bruteforce')
for a in range(41):
 for b in range(a,41):add(a,b,'all_small_ranges')
for _ in range(500):
 a=rng.randrange(200001);b=rng.randrange(a,200001);add(a,b,'random_small_bruteforce')
for k in range(1,19):
 x=10**k;add(max(0,x-12),min(MAX,x+12),'power10_window');add(0,x-1,'closed_all9');add(0,x,'power10_prefix')
for k in range(1,19):
 for d in range(1,10):
  x=int(str(d)*k);add(max(0,x-3),min(MAX,x+3),'repeated_digit_window')
for x in [0,1,9,10,11,99,100,101,1000,1010,101010101010101010,999999999999999999,MAX]:add(x,x,'singleton')
for _ in range(200):
 a=rng.randrange(MAX+1);b=rng.randrange(a,MAX+1);add(a,b,'large_combinatorial_rank_oracle')
# Interleave bounds of different digit lengths to expose stale memo entries.
order=list(range(len(cases)));rng.shuffle(order)
with tempfile.TemporaryDirectory()as tmp:
 exe=Path(tmp)/'digit';flags=['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=all'];subprocess.run(flags+[str(src),'-o',str(exe)],check=True)
 samples=[(0,0),(1,1),(10,25),(123,321),(0,MAX),(MAX,MAX),(0,9),(99,101)]+[(cases[i][0],cases[i][1])for i in order[:40]]
 for a,b in samples:
  p=subprocess.run([str(exe)],input=f'{a} {b}\n',text=True,capture_output=True,check=True,timeout=5);assert not p.stderr;assert int(p.stdout)==rank_count(b)-rank_count(a-1),(a,b,p.stdout)
 text=src.read_text();text=text[:text.index('int main() {')]+'''int main() {
 ios::sync_with_stdio(false);cin.tie(nullptr);
 DigitDP digit;assert(digit.count(-1)==0);assert(digit.count(0)==1);assert(digit.count(25)==24);assert(digit.count(101)==92);
 int t;cin>>t;while(t--){ll a,b;cin>>a>>b;cout<<digit.count(b)-digit.count(a-1)<<'\\n';}
}\n'''
 h=Path(tmp)/'batch.cpp';h.write_text(text);subprocess.run(flags+[str(h),'-o',str(exe)],check=True)
 data=str(len(cases))+'\n'+''.join(f'{cases[i][0]} {cases[i][1]}\n'for i in order);p=subprocess.run([str(exe)],input=data,text=True,capture_output=True,check=True,timeout=20);assert not p.stderr;actual=list(map(int,p.stdout.split()));assert len(actual)==len(order)
 for i,answer in zip(order,actual):assert answer==expected[i],(cases[i],answer,expected[i])
 for k in range(1,19):assert rank_count(10**k-1)==1+sum(9**j for j in range(1,k+1))
 assert rank_count(MAX)==1+sum(9**j for j in range(1,19))==168856464709124011
report={'status':'passed','compiled_source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'Cpp17_UBSan':True,'complete_program_runs':len(samples),'range_cases':len(cases),'dense_prefix_bruteforce_through':10000,'all_ranges_through40':True,'small_bruteforce_prefix_limit':200000,'power10_and_repeated_digits_to_1e18':True,'large_independent_combinatorial_rank_cases':200,'zero_and_negative_prefix_lower_guard':True,'interleaved_digit_lengths_reset_memo':True,'max_bound':str(MAX),'max_prefix_answer':str(rank_count(MAX)),'full_18digit_closed_form_verified':True}
(ROOT/'audit/PACKAGE03-DIGIT-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
