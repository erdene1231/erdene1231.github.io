import json,math,random,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];rng=random.Random(45397);L=2**63-1
with tempfile.TemporaryDirectory()as root:
 t=Path(root)
 for name in ['gcd','sieve','power']:subprocess.run(['g++','-std=c++17','-O1','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/arithmetic-{name}.cpp'),'-o',str(t/name)],check=True)
 def run(name,s):
  p=subprocess.run([str(t/name)],input=s,text=True,capture_output=True,check=True,timeout=30);assert not p.stderr;return p.stdout.splitlines()
 pairs=[(a,b)for a in range(-35,36)for b in range(-35,36)]+[(48,18),(24,36),(13,8),(10**18,10**18-1),(-10**18,0),(0,0),(49,L//49),(49,L//49+2)]+[(rng.randrange(-10**18,10**18+1),rng.randrange(-10**18,10**18+1))for _ in range(1000)]
 lines=run('gcd',str(len(pairs))+'\n'+''.join(f'{a} {b}\n'for a,b in pairs))
 assert len(lines)==len(pairs)
 for (a,b),line in zip(pairs,lines):
  g=math.gcd(a,b);c=abs(a//g*b)if g else 0;assert line==f'{g} '+(str(c)if c<=L else'OVERFLOW')
 def trial(x):
  f=[];p=2
  while p*p<=x:
   e=0
   while x%p==0:x//=p;e+=1
   if e:f.append((p,e))
   p+=1
  if x>1:f.append((x,1))
  return f
 xs=list(range(1,2001))+[1,2,4,49,999983,1000000]+[rng.randrange(1,1000001)for _ in range(1000)]
 lines=run('sieve',f'1000000 {len(xs)}\n'+'\n'.join(map(str,xs))+'\n')
 assert len(lines)==len(xs)
 for x,l in zip(xs,lines):
  f=trial(x);prime=len(f)==1 and f[0]==(x,1);d=math.prod(e+1 for p,e in f);assert list(map(int,l.split()))==[int(prime),d]
 assert run('sieve','1 2\n1\n1\n')==['0 1','0 1'];assert not run('sieve','1 0\n')
 # Inspect SPF and factor methods rather than only the displayed count.
 src=(R/'audit/package03-work/arithmetic-sieve.cpp').read_text().split('int main() {')[0]+'''int main(){Sieve s(2000);for(int x=1;x<=2000;x++){cout<<s.spf[x];for(auto [p,e]:s.factor(x))cout<<' '<<p<<' '<<e;cout<<'\\n';}}''';(t/'h.cpp').write_text(src);subprocess.run(['g++','-std=c++17','-O1','-fsanitize=undefined','-fno-sanitize-recover=all',str(t/'h.cpp'),'-o',str(t/'h')],check=True);p=subprocess.run([str(t/'h')],text=True,capture_output=True,check=True);assert not p.stderr
 for x,l in enumerate(p.stdout.splitlines(),1):
  f=trial(x);vals=list(map(int,l.split()));assert vals[0]==(f[0][0]if f else 0);assert vals[1:]==[v for pair in f for v in pair]
 powers=[(a,e,m)for a in range(-12,13)for e in range(15)for m in [1,2,3,17,1000,1000000007]]+[(3,13,17),(0,0,7),(8,0,1),(2,10,1000),(-10**18,10**18,1000000007)]+[(rng.randrange(-10**18,10**18+1),rng.randrange(10**18+1),rng.randrange(1,1000000008))for _ in range(1000)]
 lines=run('power',str(len(powers))+'\n'+''.join(f'{a} {e} {m}\n'for a,e,m in powers))
 assert len(lines)==len(powers)
 for (a,e,m),l in zip(powers,lines):assert int(l)==(a**e % m if e<=14 else pow(a,e,m))
 for name in ['gcd','power']:assert not run(name,'0\n')
 out={'status':'passed','CXX17_UBSan_programs':3,'gcd_cases':len(pairs),'python_exact_gcd_lcm_oracle':True,'sieve_queries':len(xs),'trial_division_and_every_SPF_factor_through':2000,'power_cases':len(powers),'python_exact_integer_power_oracle':True,'zero_sign_modulus1_and_overflow_status':True,'sieve_max_n':1000000,'base_exponent_max_magnitude':10**18,'max_modulus':1000000007};(R/'audit/PACKAGE03-ARITHMETIC-CODE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
