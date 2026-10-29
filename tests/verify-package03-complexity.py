import hashlib,itertools,json,random,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];doc=json.loads((ROOT/'audit/package03-lessons/complexity.json').read_text())['body'];code=(ROOT/'audit/package03-work/complexity.cpp').read_text();rng=random.Random(20261028)
with tempfile.TemporaryDirectory()as tmp:
 src=Path(tmp)/'complexity.cpp';exe=Path(tmp)/'fast';src.write_text(code)
 def compile(src,path,extra=[]):
  p=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic',*extra,str(src),'-o',str(path)],capture_output=True,text=True);assert p.returncode==0 and not p.stderr,p.stderr
 compile(src,exe)
 harness=Path(tmp)/'harness.cpp';check=Path(tmp)/'check';harness.write_text('#define main lesson_main\n'+code+'\n#undef main\nint main() { int n; while (cin >> n) { vector<int> a(n); for (int& x : a) cin >> x; cout << cubic(a) << " " << quadratic(a) << " " << max_sum(a) << "\\n"; } return 0; }\n');compile(harness,check)
 cases=[list(a)for n in range(8)for a in itertools.product([-2,0,3],repeat=n)];cases += [[-1,2,4,-3,5,2,-5,2]];cases += [[rng.randrange(-10**9,10**9+1)for _ in range(rng.randrange(25))]for _ in range(200)]
 def oracle(a):
  pref=[0]
  for x in a:pref.append(pref[-1]+x)
  return max([0]+[pref[r]-pref[l]for l in range(len(a))for r in range(l+1,len(a)+1)])
 payload=''.join(str(len(a))+'\n'+' '.join(map(str,a))+'\n'for a in cases);out=subprocess.run([str(check)],input=payload,capture_output=True,text=True,timeout=30,check=True).stdout.splitlines();assert len(out)==len(cases)
 for a,line in zip(cases,out):assert list(map(int,line.split()))==[oracle(a)]*3,a
 samples=[(next(b['text']for b in doc['sections'][3]['blocks']if b.get('language')=='Input'),'10')]
 stress=[([10**9]*10**6,10**15),([-10**9]*10**6,0),([-10**9,10**9]*500000,10**9),([],0),([-5],0),([0],0)]
 for a,expected in stress:
  payload=str(len(a))+'\n'+' '.join(map(str,a))+'\n';actual=subprocess.run([str(exe)],input=payload,capture_output=True,text=True,timeout=15,check=True).stdout.strip();assert actual==str(expected)
 for inp,expected in samples:assert subprocess.run([str(exe)],input=inp,capture_output=True,text=True,check=True).stdout.strip()==expected
 sanitized=Path(tmp)/'ubsan';compile(src,sanitized,['-fsanitize=undefined','-fno-sanitize-recover=all']);assert subprocess.run([str(sanitized)],input=samples[0][0],capture_output=True,text=True,check=True).stdout.strip()=='10'
 counts=[]
 for n in range(21):
  cubic_count=sum(r-l+1 for l in range(n)for r in range(l,n));quad_count=sum(1 for l in range(n)for r in range(l,n));assert cubic_count==n*(n+1)*(n+2)//6 and quad_count==n*(n+1)//2;counts.append({'n':n,'cubic_additions':cubic_count,'quadratic_additions':quad_count,'linear_iterations':n})
 report={'status':'passed','program_sha256':hashlib.sha256(code.encode()).hexdigest(),'algorithms_implemented_and_checked':['cubic enumeration','quadratic incremental sums','linear best-ending scan'],'independent_reference':'Python prefix-sum enumeration of all endpoint pairs; exhaustive and seeded signed arrays','small_cases':len(cases),'algorithm_answers_checked':len(cases)*3,'stress_cases':len(stress),'maximum_n':1000000,'maximum_sum_checked':10**15,'exact_operation_counts':counts,'compile_warnings':0,'sample_passed':True,'sample_UBSan':True,'production_writes':0}
(ROOT/'audit/PACKAGE03-COMPLEXITY-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='exact_operation_counts'}))
