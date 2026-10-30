import itertools,json,random,subprocess,tempfile,hashlib,io
from pathlib import Path
R=Path(__file__).resolve().parents[1];src=(R/'audit/package03-work/aho-corasick.cpp').read_text();work=Path(tempfile.mkdtemp(prefix='aho-code-'));base=src[:src.index('int main()')]
flags=['g++','-std=c++17','-O2','-Wall','-Wextra','-Wconversion','-Werror','-fsanitize=undefined','-fno-sanitize-recover=all']
(R/'audit/package03-work/aho-corasick.cpp').resolve()
subprocess.run(flags+[str(R/'audit/package03-work/aho-corasick.cpp'),'-o',str(work/'full')],check=True)
harness=base+'''int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int cases; cin >> cases;
    while (cases--) {
        int k; string text; cin >> k >> text;
        if (text == "-") text.clear();
        vector<string> p(k); int m = 0;
        for (auto& x : p) { cin >> x; m += (int)x.size(); }
        Aho ac(m); for (auto& x : p) ac.add(x); ac.build();
        auto a = ac.count(text); auto again = ac.count(text);
        if (a != again) return 10;
        for (int x : a) cout << x << ' ';
        cout << '\\n';
        ac.report(text); cout << "END\\n";
        for (int v = 1; v < (int)ac.t.size(); v++) {
            int f = ac.t[v].link, o = ac.t[v].out;
            if (f == v || (o && ac.t[o].ids.empty())) return 11;
        }
    }
}
''';(work/'h.cpp').write_text(harness);subprocess.run(flags+[str(work/'h.cpp'),'-o',str(work/'h')],check=True)
def oracle(s,p):
 pairs=sorted((i+len(x),j+1)for j,x in enumerate(p)for i in range(len(s)-len(x)+1)if s.startswith(x,i));return [sum(j==id+1 for _,j in pairs)for id in range(len(p))],pairs
words=[''.join(s)for n in range(1,4)for s in itertools.product('ab',repeat=n)];texts=['']+[''.join(s)for n in range(1,6)for s in itertools.product('ab',repeat=n)];cases=[(s,p)for s in texts for p in itertools.product(words[:6],repeat=2)]
rng=random.Random(90210)
for _ in range(500):cases.append((''.join(rng.choice('abcxyz')for _ in range(rng.randrange(75))),[''.join(rng.choice('abcxyz')for _ in range(rng.randrange(1,10)))for _ in range(rng.randrange(1,20))]))
cases += [('ushershe',['he','she','his','hers','he']),('aaaaa',['a','aa','aaa','aa']),('',[]),('abc',[]),('z',['z','zz','x']),('aybabtu',['bab','abc','a'])]
raw=str(len(cases))+'\n'+''.join(str(len(p))+' '+(s or '-')+'\n'+'\n'.join(p)+'\n'for s,p in cases);run=subprocess.run([str(work/'h')],input=raw,text=True,capture_output=True,check=True);out=io.StringIO(run.stdout);pairs_checked=0
for s,p in cases:
 ans,pairs=oracle(s,p);got=list(map(int,out.readline().split()));assert got==ans,(s,p,got,ans);actual=[]
 while (line:=out.readline().strip())!='END':
  assert line;actual.append(tuple(map(int,line.split())))
 assert sorted(actual)==pairs,(s,p,actual,pairs);pairs_checked+=len(pairs)
assert out.read()==''
for s,p in cases[::43]:
 if not s or not p:continue
 run=subprocess.run([str(work/'full')],input=s+'\n'+str(len(p))+'\n'+'\n'.join(p)+'\n',text=True,capture_output=True,check=True);assert list(map(int,run.stdout.split()))==oracle(s,p)[0]
# Adversarial shared suffixes: count only, so the large output set is never enumerated.
stress=base+'''int main() {
    int n = 100000, k = 1000; Aho ac(k * (k + 1) / 2);
    for (int len = 1; len <= k; len++) ac.add(string(len, 'a'));
    ac.build(); auto ans = ac.count(string(n, 'a'));
    for (int i = 0; i < k; i++) if (ans[i] != n - i) return 1;
    Aho chain(500000); chain.add(string(500000, 'z')); chain.add("z");
    chain.build(); auto b = chain.count(string(500000, 'z'));
    if (b[0] != 1 || b[1] != 500000) return 2;
}
''';(work/'stress.cpp').write_text(stress);subprocess.run(flags+[str(work/'stress.cpp'),'-o',str(work/'stress')],check=True);subprocess.run([str(work/'stress')],check=True,timeout=30)
example=base+'''int main() { Aho ac(20); for (string s : {"he","she","his","hers","he"}) ac.add(s); ac.build(); for (int i=0;i<(int)ac.t.size();i++) cout<<i<<' '<<ac.t[i].link<<' '<<ac.t[i].out<<'\\n'; }'''
(work/'example.cpp').write_text(example);subprocess.run(flags+[str(work/'example.cpp'),'-o',str(work/'example')],check=True)
snapshot=[list(map(int,line.split()))for line in subprocess.check_output([str(work/'example')],text=True).splitlines()]
assert snapshot==[[0,0,0],[1,0,0],[2,0,0],[3,0,0],[4,1,0],[5,2,2],[6,0,0],[7,3,0],[8,0,0],[9,3,0]]
report={'status':'passed','Cpp17_UBSan_programs':1,'compiled_source_sha256':hashlib.sha256(src.encode()).hexdigest(),'naive_count_and_position_cases':len(cases),'individual_matches_verified':pairs_checked,'exhaustive_binary_texts_through5_and_duplicate_dictionaries':True,'random_cases':500,'suffixes_overlaps_duplicates_empty_text_empty_dictionary':True,'repeated_count_calls_reset':True,'official_counting_sample':True,'full_program_runs':sum(bool(s and p)for s,p in cases[::43]),'chain_states':500001,'count_without_enumerating_99500500_matches':True,'no_deep_recursion':True,'worked_trie_link_output_snapshot':snapshot};(R/'audit/PACKAGE03-AHO-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
