"""Compile the actual lesson programs and exercise their supported numeric domains."""
import json, math, random, subprocess, tempfile, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'audit/package03-lessons/introduction.json').read_text())['body'];rng=random.Random(29);checks=0
with tempfile.TemporaryDirectory()as tmp:
 def compile(name,source):
  p=Path(tmp)/f'{name}.cpp';p.write_text(source);exe=p.with_suffix('')
  c=subprocess.run(['g++','-std=c++17','-O1','-Wall','-Wextra','-pedantic','-fsanitize=undefined','-fno-sanitize-recover=all',str(p),'-o',str(exe)],capture_output=True,text=True)
  assert c.returncode==0 and not c.stderr,c.stderr
  return exe
 def run(exe,data,expected):
  global checks
  r=subprocess.run([str(exe)],input=data,capture_output=True,text=True,check=True,timeout=3)
  assert not r.stderr and r.stdout==expected,(data,r.stdout,expected,r.stderr);checks+=1
 exes={}
 for name in ['io','mod','square','sequences','digits']:
  source=(ROOT/f'audit/package03-work/introduction-{name}.cpp').read_text();exes[name]=compile(name,source)
  for doc in [d,d['translations']['en']]:assert any(b.get('text')==source for s in doc['sections']for b in s['blocks']if b['type']=='code')
 for data in ['123 456 monkey\n','123    456\nmonkey\n','\n123\t456\nmonkey\n']:
  run(exes['io'],data,'123 456 monkey\n')
 for n,m in [(0,1),(0,7),(1,1),(5,7),(20,10**9+7)]+[(rng.randrange(200),rng.randrange(1,10**9+8))for _ in range(50)]:
  run(exes['mod'],f'{n} {m}\n',str(math.factorial(n)%m)+'\n')
 for x in [0,1,-1,123456789,3*10**9,-3*10**9]+[rng.randrange(-3*10**9,3*10**9+1)for _ in range(20)]:run(exes['square'],f'{x}\n',str(x*x)+'\n')
 a,b=0,1
 for n in range(91):
  f=str(math.factorial(n))if n<=20 else'OUT OF RANGE';run(exes['sequences'],f'{n}\n',f'{a}\n{f}\n');a,b=b,a+b
 for x,b in [(0,2),(123,2),(2**62,2),(2**63-1,2),(10**18,10)]+[(rng.randrange(2**63),rng.randrange(2,37))for _ in range(50)]:
  v=x;cnt=1
  while v>=b:v//=b;cnt+=1
  run(exes['digits'],f'{x} {b}\n',f'{cnt}\n')
 # Independently compile the book-derived caution examples; never execute signed overflow.
 c=compile('cautions',r'''#include <bits/stdc++.h>
using namespace std;
using ll = long long;
#define SQ_BAD(a) a*a
#define SQ_BOOK(a) (a)*(a)
#define SQ_PAREN(a) ((a)*(a))
int main() {
    int a = 123456789;
    cout << 1LL * a * a << "\n";
    ll x = -3, m = 5;
    x %= m;
    if (x < 0) x += m;
    cout << x << "\n";
    cout << SQ_BAD(3 + 3) << " " << SQ_BOOK(3 + 3) << " " << 100 / SQ_PAREN(3) << "\n";
    double y = 0.3 * 3 + 0.1;
    cout << (abs(y - 1) < 1e-9) << "\n";
    cout << floor(-3.0 / 2) << " " << -3 / 2 << "\n";
    ll u = 123456789, v = 987654321;
    cout << u * v << "\n";
}
''');run(c,'','15241578750190521\n2\n15 36 11\n1\n-2 -1\n121932631112635269\n')
 c=compile('stdio','#include <cstdio>\nint main() { int a, b; if (scanf("%d %d", &a, &b) != 2) return 1; printf("%d %d\\n", a, b); }');run(c,'123 456\n','123 456\n')
 c=compile('getline','#include <bits/stdc++.h>\nusing namespace std;\nint main(){int n;cin>>n;cin.ignore(numeric_limits<streamsize>::max(),\'\\n\');string s;getline(cin,s);cout<<n<<" "<<s<<"\\n";}');run(c,'2\nhello world\n','2 hello world\n')
 c=compile('eof','#include <bits/stdc++.h>\nusing namespace std;\nint main(){int x;while(cin>>x){cout<<x<<"\\n";}}');run(c,'1 -2\n3\n','1\n-2\n3\n');run(c,'','')
 for n in range(1,21):
  assert sum(range(1,n+1))==n*(n+1)//2
  assert sum(x*x for x in range(1,n+1))==n*(n+1)*(2*n+1)//6
  assert sum(2**i for i in range(n))==2**n-1
 report={'status':'passed','compiled_programs':9,'program_runs':checks,'sanitizer':'UBSan on all compiled examples','numeric_limits_checked':{'square_abs_max':3000000000,'fibonacci_max_n':90,'factorial_max_n':20,'digit_max_x':2**63-1},'formula_cases':60,'warnings':0,'production_writes':0}
 (ROOT/'audit/PACKAGE03-INTRODUCTION-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
