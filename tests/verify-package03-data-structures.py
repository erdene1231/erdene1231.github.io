import json,subprocess,tempfile,random,collections,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];rng=random.Random(20261029);names=['ds-vector-string','ds-sets','ds-map-demo','ds-frequencies','ds-ranges','ds-nearest','ds-other','ds-pbds','ds-comparison'];codes={n:(ROOT/f'audit/package03-work/{n}.cpp').read_text()for n in names};runs=0
with tempfile.TemporaryDirectory()as tmp:
 def compile(name,source):
  p=Path(tmp)/f'{name}.cpp';p.write_text(source);exe=p.with_suffix('');r=subprocess.run(['g++','-std=c++17','-O1','-Wall','-Wextra','-pedantic','-fsanitize=undefined','-fno-sanitize-recover=all',str(p),'-o',str(exe)],capture_output=True,text=True);assert r.returncode==0 and not r.stderr,(name,r.stderr);return exe
 def run(exe,data=''):
  global runs
  r=subprocess.run([str(exe)],input=data,capture_output=True,text=True,check=True,timeout=30);assert not r.stderr,r.stderr;runs+=1;return [line.strip()for line in r.stdout.splitlines()]
 exes={n:compile(n,c)for n,c in codes.items()}
 assert run(exes['ds-vector-string'])==['3 2 5']*3+['2','5','5 0 5','hattihatti','hattivatti','tiva','5']
 assert run(exes['ds-sets'])==['1 0','0 1','4','2 5 6 8','1','3','2','0']
 assert run(exes['ds-map-demo'])==['3','0','1','0','4','aybabtu 0','banana 3','harpsichord 9','monkey 4']
 assert run(exes['ds-other'])==['1 0','1 0 4','0010010000','1011111110','1001101110','5','5 2','3 2','7','5','6','2']
 assert run(exes['ds-pbds'])==['7','2','2','3']
 for line in run(exes['ds-ranges']):assert sorted(map(int,line.split()))==[3,4,6,8,12,13,14,17]
 freqcases=[[],[7,2,7,5,2,7],[-2**31,2**31-1,-2**31]]+[[rng.randrange(-5,6)for _ in range(rng.randrange(40))]for _ in range(80)]
 query_checks=0
 for a in freqcases:
  qs=[-2**31,2**31-1,2,5,7,9,9]+[rng.randrange(-7,8)for _ in range(8)];freq=collections.Counter(a);data=f'{len(a)} {len(qs)}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,qs))+'\n';expected=[str(freq[x])for x in qs]+[str(len(freq))]+[f'{x} {freq[x]}'for x in sorted(freq)];assert run(exes['ds-frequencies'],data)==expected;query_checks+=len(qs)
 nearcases=[[],[0],[3,4,6,8,12,13,14,17],[-2**31,2**31-1],[-2**31,0,2**31-1]]+[[rng.randrange(-100,101)for _ in range(rng.randrange(30))]for _ in range(100)];nearest_queries=0
 for a in nearcases:
  qs=[-2**31,2**31-1,-1,0,1,5,10]+[rng.randrange(-110,111)for _ in range(8)];expected=[str(min(set(a),key=lambda v:(abs(v-x),-v)))if a else'EMPTY'for x in qs];data=f'{len(a)} {len(qs)}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,qs))+'\n';assert run(exes['ds-nearest'],data)==expected;nearest_queries+=len(qs)
 # Actual article functions against an independent Python distinct intersection.
 harness=compile('ds-comparison-harness','#define main lesson_main\n'+codes['ds-comparison']+'\n#undef main\nint main(){int n,m;while(cin>>n>>m){vector<int>a(n),b(m);for(int&x:a)cin>>x;for(int&x:b)cin>>x;cout<<common_brute(a,b)<<" "<<common_set(a,b)<<" "<<common_hash(a,b)<<" "<<common_sort(a,b)<<"\\n";}return 0;}')
 arrays=[list(a)for n in range(4)for a in itertools.product([0,1,2],repeat=n)];pairs=[(a,b)for a in arrays for b in arrays]+[([5,2,8,9,4],[3,2,9,5]),([-2**31,2**31-1]*3,[2**31-1,-2**31]),([5,5,5],[5,5])]+[([rng.randrange(-20,21)for _ in range(rng.randrange(40))],[rng.randrange(-20,21)for _ in range(rng.randrange(40))])for _ in range(100)]
 payload=''.join(f'{len(a)} {len(b)}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,b))+'\n'for a,b in pairs);actual=run(harness,payload);assert len(actual)==len(pairs)
 for(a,b),line in zip(pairs,actual):assert list(map(int,line.split()))==[len(set(a)&set(b))]*4
 # Main stays practical on its published domain and preserves exact example semantics.
 for a,b in [([5,2,8,9,4],[3,2,9,5]),(list(range(200000)),list(range(100000,300000))),([7]*200000,[7]*200000),([],[])]:
  got=run(exes['ds-comparison'],f'{len(a)} {len(b)}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,b))+'\n');ans=len(set(a)&set(b));assert got==[f'{ans} {ans} {ans}']
 # PBDS boundary and rank operations, not an invented vector substitute.
 pb=compile('ds-pbds-harness','#define main lesson_main\n'+codes['ds-pbds']+'\n#undef main\nint main(){indexed_set s;for(int i=99;i>=0;i--){s.insert(i);s.insert(i);}for(int i=0;i<100;i++){if(*s.find_by_order(i)!=i||s.order_of_key(i)!=(unsigned)i)return 1;}if(s.find_by_order(100)!=s.end())return 2;for(int i=0;i<100;i+=2)s.erase(i);for(int i=-1;i<=101;i++){int cnt=0;for(int x:s)cnt+=x<i;if(s.order_of_key(i)!=(unsigned)cnt)return 3;}cout<<"ok\\n";}');assert run(pb)==['ok']
 d=json.loads((ROOT/'audit/package03-lessons/set-map.json').read_text())['body']
 for doc in [d,d['translations']['en']]:
  for source in codes.values():assert any(b.get('text')==source for s in doc['sections']for b in s['blocks']if b['type']=='code')
 report={'status':'passed','compiled_programs':9,'additional_harnesses':2,'UBSan':True,'program_runs':runs,'exact_source_demo_programs':6,'frequency_queries':query_checks,'nearest_queries':nearest_queries,'intersection_oracle_pairs':len(pairs),'intersection_answers_checked':len(pairs)*4,'duplicate_semantics':'distinct intersection, all four methods agree','maximum_main_n_m':200000,'integer_extremes':True,'PBDS_order_rank_empty_end_and_duplicates':True,'historical_book_benchmark_not_remeasured':True,'warnings':0,'production_writes':0}
 (ROOT/'audit/PACKAGE03-DATA-STRUCTURES-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
