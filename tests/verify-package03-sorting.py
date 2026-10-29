import json,math,random,subprocess,tempfile,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];rng=random.Random(20261029);checks=0
codes={k:(ROOT/f'audit/package03-work/{k}.cpp').read_text()for k in ['sorting-chapter3','sorting-std','sorting-search','sorting-monotone']}
with tempfile.TemporaryDirectory()as tmp:
 def compile(name,source):
  path=Path(tmp)/f'{name}.cpp';path.write_text(source);exe=path.with_suffix('');r=subprocess.run(['g++','-std=c++17','-O1','-Wall','-Wextra','-pedantic','-fsanitize=undefined','-fno-sanitize-recover=all',str(path),'-o',str(exe)],capture_output=True,text=True);assert r.returncode==0 and not r.stderr,r.stderr;return exe
 def run(exe,data):
  r=subprocess.run([str(exe)],input=data,capture_output=True,text=True,check=True,timeout=30);assert not r.stderr,r.stderr;return r.stdout
 exe={k:compile(k,c)for k,c in codes.items()}
 # Exercise the actual functions from the lesson, not duplicate implementations.
 sort_h=compile('sort-harness','#define main lesson_main\n'+codes['sorting-chapter3']+'\n#undef main\nint main(){int n;while(cin>>n){vector<int>a(n),b,c,tmp(n);for(int&x:a)cin>>x;b=c=a;merge_sort(a,tmp,0,n-1);bubble_sort(b);if(a!=b)return 1;bool nonneg=all_of(c.begin(),c.end(),[](int x){return 0<=x&&x<=100;});if(nonneg){count_sort(c,100);if(a!=c)return 2;}for(int x:a)cout<<x<<" ";cout<<"|"<<distinct_count(a)<<"\\n";}return 0;}')
 cases=[list(a)for n in range(7)for a in itertools.product([0,1,2],repeat=n)]+[[1,3,8,2,9,2,5,6],[1,3,6,2,8,2,5,9],[1,3,6,9,9,3,5,9],[5,2,5,1,2,-1,5],[-2**31,2**31-1,0,-2**31]]+[[rng.randrange(-100,101)for _ in range(rng.randrange(30))]for _ in range(100)]
 data=''.join(str(len(a))+'\n'+' '.join(map(str,a))+'\n'for a in cases);lines=run(sort_h,data).splitlines();assert len(lines)==len(cases)
 for a,line in zip(cases,lines):
  vals,cnt=line.split('|');assert list(map(int,vals.split()))==sorted(a)and int(cnt)==len(set(a));checks+=1
 for a in [[],[5,2,5,1,2,-1,5],[1,3,8,2,9,2,5,6],list(range(200000,0,-1)),[7]*200000]:assert int(run(exe['sorting-chapter3'],f'{len(a)}\n'+ ' '.join(map(str,a))+'\n'))==len(set(a));checks+=1
 expected=['2 3 3 4 5 5 8','8 5 5 4 3 3 2','2 3 3 4 5 5 8','ekmnoy','1,2 1,5 2,3','1,5,3 2,1,3 2,1,4','1,2 1,5 2,3','a cat dog book','1,90 2,80 3,80'];assert[line.strip()for line in run(exe['sorting-std'],'').splitlines()]==expected;checks+=9
 # Both search methods may return different valid occurrences of duplicates.
 searchcases=[sorted(a)for a in cases[:1093]]+[[],[-2**31,2**31-1],[3]*17]
 queries=0
 for a in searchcases:
  qs=[-2**31,-1,0,1,2,3,100,2**31-1];inp=f'{len(a)} {len(qs)}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,qs))+'\n';lines=run(exe['sorting-search'],inp).splitlines();assert len(lines)==len(qs)
  for q,line in zip(qs,lines):
   i,j,cnt=map(int,line.split());assert cnt==a.count(q)
   for pos in [i,j]:assert(pos==-1 and q not in a)or(0<=pos<len(a)and a[pos]==q)
   checks+=1;queries+=1
 # Exhaust all thresholds for bounded (including non-power-of-two) jump limits.
 monotone_h=compile('monotone-harness','#define main lesson_main\n'+codes['sorting-monotone']+'\n#undef main\nint main(){for(int z=0;z<=100;z++)for(int k=0;k<=z;k++)if(first_true(z,[&](int x){return x>=k;})!=k)return 1;cout<<5151<<"\\n";}')
 assert run(monotone_h,'')=='5151\n';checks+=5151
 peakcases=[[]]+[[sum(range(i+1))if i<=p else sum(range(p+1))-sum(range(1,i-p+1))for i in range(n)]for n in range(1,16)for p in range(n)]
 for _ in range(100):
  n=rng.randrange(1,100);p=rng.randrange(n);a=[rng.randrange(-10**9,10**9)]
  for i in range(1,n):a.append(a[-1]+rng.randrange(1,1000)*(1 if i<=p else -1))
  peakcases.append(a)
 for t,a in zip([0,1,2,15,16,10**18]+[rng.randrange(10**18+1)for _ in range(len(peakcases))],peakcases):
  inp=f'{t} {len(a)}\n'+' '.join(map(str,a))+'\n';got=list(map(int,run(exe['sorting-monotone'],inp).split()));r=math.isqrt(t);ceil=r+(r*r<t);peak=max(range(len(a)),key=a.__getitem__)if a else-1;assert got==[ceil,peak],(inp,got,ceil,peak);checks+=1
 # Strict weak ordering on representative ties, copied from the actual article functions.
 comp_h=compile('comparator-harness','#define main lesson_main\n'+codes['sorting-std']+'\n#undef main\nint main(){vector<string>v={"","a","b","aa","ab","bb","cat","dog"};for(auto&a:v)for(auto&b:v)for(auto&c:v){if(comp(a,a))return 1;if(comp(a,b)&&comp(b,a))return 2;if(comp(a,b)&&comp(b,c)&&!comp(a,c))return 3;}vector<P>p={{0,0},{1,0},{1,1},{1,1},{-1,2}};for(auto&a:p)for(auto&b:p)for(auto&c:p){if(a<a)return 4;if(a<b&&b<a)return 5;if(a<b&&b<c&&!(a<c))return 6;}cout<<"ok\\n";}');assert run(comp_h,'')=='ok\n'
 # Every full program is actually embedded in both native documents.
 doc=json.loads((ROOT/'audit/package03-lessons/sorting.json').read_text())['body']
 for d in [doc,doc['translations']['en']]:
  for source in codes.values():assert any(b.get('text')==source for s in d['sections']for b in s['blocks']if b['type']=='code')
 report={'status':'passed','compiled_programs_and_harnesses':7,'UBSan':True,'checks':checks,'sort_oracle_cases':len(cases),'search_queries':queries,'all_threshold_boundaries':5151,'unimodal_cases':len(peakcases),'maximum_sort_n':200000,'source_samples_and_old_distinct_example':True,'std_examples':9,'warnings':0,'production_writes':0}
 (ROOT/'audit/PACKAGE03-SORTING-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
