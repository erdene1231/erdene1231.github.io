"""Recursive merge sort, library alternatives and a two-key lambda example."""
import hashlib,itertools,json,random,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];b=json.loads((ROOT/'audit/package02-revisions/sorting-recursive.json').read_text())['body'];blocks=b['sections'][7]['blocks'];pieces=[x['text']for x in blocks if x.get('language')=='C++17'];assert len(pieces)==10
assert ''.join(pieces[:4])==pieces[4];assert pieces[7]+pieces[8]==pieces[9]
assert pieces==[x['text']for x in b['translations']['en']['sections'][7]['blocks']if x.get('language')=='C++17'];rng=random.Random(20261028)
with tempfile.TemporaryDirectory()as tmp:
 def compile(name,text):
  src=Path(tmp)/(name+'.cpp');exe=Path(tmp)/name;src.write_text(text);r=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic',str(src),'-o',str(exe)],capture_output=True,text=True,check=True);assert not r.stderr,r.stderr;return exe
 def run(exe,text=''):return subprocess.run([str(exe)],input=text,capture_output=True,text=True,check=True,timeout=8).stdout.split()
 program=compile('recursive-sort',pieces[4]);harness=compile('recursive-harness','#define main lesson_main\n'+pieces[4]+'\n#undef main\nint main() { int n; cin >> n; vector<long long> a(n); for (auto& x:a) cin>>x; sort_values(a); for(auto x:a) cout<<x<<" "; return 0; }\n')
 arrays=[[],[1],[2,1],list(range(200000)),list(range(199999,-1,-1)),[7]*200000,[-2**63,2**63-1,0,-2**63],[5,2,5,1,2,-1,5]]+[[rng.randrange(-100,101)for _ in range(rng.randrange(400))]for _ in range(100)]
 for a in arrays:
  text=str(len(a))+'\n'+' '.join(map(str,a))+'\n';assert run(program,text)==[str(len(set(a)))];assert list(map(int,run(harness,text)))==sorted(a)
 sample_in=next(x['text']for x in blocks if x.get('language')=='Input');sample_out=next(x['text']for x in blocks if x.get('language')=='Output');assert run(program,sample_in)==sample_out.split()
 # Compile exactly the published lambda program and compare the explicit secondary-key result.
 custom=compile('two-key-example',pieces[9]);assert run(custom)==['1','95','2','95','3','80','4','80']
 # Reuse the exact extracted comparator on a duplicate-heavy corpus and all triples.
 comparator=pieces[8].split('[](const Student& first, const Student& second)',1)[1].split(');',1)[0]
 custom_harness=compile('comparator-contract',pieces[7]+'int main() { auto comp=[](const Student& first, const Student& second)'+comparator+';\nvector<Student> a={{1,2},{2,2},{1,1},{1,2},{3,-1},{0,2}}; for(auto x:a) { if(comp(x,x)) return 1; for(auto y:a) { if(comp(x,y)&&comp(y,x)) return 2; for(auto z:a) { if(comp(x,y)&&comp(y,z)&&!comp(x,z)) return 3; auto eq=[&](Student p,Student q){return !comp(p,q)&&!comp(q,p);}; if(eq(x,y)&&eq(y,z)&&!eq(x,z)) return 4; } } } sort(a.begin(),a.end(),comp); for(auto x:a)cout<<x.id<<" "<<x.score<<" "; return 0; }')
 records=[(1,2),(2,2),(1,1),(1,2),(3,-1),(0,2)];expected=[str(v)for rec in sorted(records,key=lambda x:(-x[1],x[0]))for v in rec];assert run(custom_harness)==expected
 # Both displayed library snippets compile and match an independent Python ordering.
 for index,snippet in enumerate(pieces[5:7]):
  exe=compile('library-'+str(index),'#include <algorithm>\n#include <iostream>\n#include <vector>\nusing namespace std; int main() { vector<long long> values={3,-1,3,2}; '+snippet+' for(auto x:values)cout<<x<<" "; }');assert list(map(int,run(exe)))==sorted([3,-1,3,2],reverse=index==1)
report={'status':'passed','recursive_cases':len(arrays),'full_sequence_and_count_checked':True,'maximum_size':200000,'sample_passed':True,'compile_warnings':0,'program_sha256':hashlib.sha256(pieces[4].encode()).hexdigest(),'lambda_program_sha256':hashlib.sha256(pieces[9].encode()).hexdigest(),'library_examples':3,'comparator_checks':'Exact comparator: identity, asymmetric, transitive and equivalence-transitive checks over all triples of a duplicate-heavy corpus; independent score-desc/id-asc oracle','scope':'Local compiled programs and comparator examples; publication and native editor checks separate'}
(ROOT/'audit/PACKAGE02-RECURSIVE-SORT-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
