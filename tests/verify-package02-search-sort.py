"""Current exhaustive-search and bottom-up merge-sort programs; independent local oracles."""
import hashlib,json,random,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];rng=random.Random(20261028);reports=[]
with tempfile.TemporaryDirectory()as tmp:
 for id in ['brute-force','sorting']:
  body=json.loads((ROOT/'audit/package02-lessons'/f'{id}.json').read_text())['body'];blocks=body['sections'][7]['blocks'];pieces=[b['text']for b in blocks if b.get('language')=='C++17'];assert len(pieces)==5 and ''.join(pieces[:4])==pieces[-1]
  assert pieces==[b['text']for b in body['translations']['en']['sections'][7]['blocks']if b.get('language')=='C++17'];code=pieces[-1]
  src=Path(tmp)/(id+'.cpp');exe=Path(tmp)/id;src.write_text(code)
  result=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic',str(src),'-o',str(exe)],capture_output=True,text=True,check=True);assert not result.stderr,result.stderr
  def run(values,path=exe):return subprocess.run([str(path)],input=str(len(values))+'\n'+' '.join(map(str,values))+'\n',capture_output=True,text=True,timeout=5,check=True).stdout.split()
  if id=='brute-force':
   cases=[[],[0],[10**9],[2,3,4],[8,7,6,5,4],[10**9]*19,[10**9]*20,[0]*20,[1,10**9]*10]+[[rng.randrange(21)for _ in range(rng.randrange(15))]for _ in range(90)]
   for values in cases:
    possible={0}
    for weight in values:possible|={s+weight for s in possible}
    total=sum(values);expected=min(abs(total-2*s)for s in possible)
    assert run(values)==[str(expected)],values
   oracle='Reachable-sum set (merges equal subproblems), independent of recursive branch enumeration'
  else:
   harness=Path(tmp)/'sort-harness.cpp';sort_exe=Path(tmp)/'sort-harness'
   harness.write_text('#define main lesson_main\n'+code+'\n#undef main\nint main() { int n; cin >> n; vector<long long> values(n); for (auto& x : values) cin >> x; sort_values(values); for (auto x : values) cout << x << " "; cout << "\\n"; return 0; }\n')
   built=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic',str(harness),'-o',str(sort_exe)],capture_output=True,text=True,check=True);assert not built.stderr,built.stderr
   cases=[[],[0],[-2**63,2**63-1,0,-2**63],list(range(200000)),list(range(199999,-1,-1)),[7]*200000,[5,2,5,1,2,-1,5]]+[[rng.randrange(-40,41)for _ in range(rng.randrange(250))]for _ in range(90)]
   for values in cases:
    assert run(values)==[str(len(set(values)))],values[:30]
    assert run(values,sort_exe)==list(map(str,sorted(values))),values[:30]
   oracle='Python independent sorted sequence and set cardinality, including full maximum-size sorted/reverse/equal inputs'
  sample_in=next(b['text']for b in blocks if b.get('language')=='Input');sample_out=next(b['text']for b in blocks if b.get('language')=='Output');sample_result=subprocess.run([str(exe)],input=sample_in,capture_output=True,text=True,timeout=5,check=True).stdout.split();assert sample_result==sample_out.split()
  reports.append({'lesson':id,'program_sha256':hashlib.sha256(code.encode()).hexdigest(),'compile_warnings':0,'cases':len(cases),'sample_passed':True,'oracle':oracle,'full_sorted_sequence_checked':id=='sorting'})
report={'status':'passed','programs':reports,'scope':'Local complete C++ programs, fragments and declared numeric/size contracts only; semantic/editor/publication gates remain separate'}
(ROOT/'audit/PACKAGE02-SEARCH-SORT-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
