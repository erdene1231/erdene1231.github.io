"""Exact naive string/dictionary oracles plus deliberate collision fault injection."""
import subprocess,tempfile,random,itertools
from pathlib import Path
R=Path(__file__).resolve().parents[1];rng=random.Random(2601);count=0
mods=[1000000007,1000000009];bases=[911382323,97266353]
def h(s,base,mod):
 ans=0
 for c in s:ans=(ans*base+c)%mod
 return ans
def dh(s):return tuple(h(s,a,b)for a,b in zip(bases,mods))
def pi(s):return [max([k for k in range(i+1)if s[:k]==s[i-k+1:i+1]],default=0)for i in range(len(s))]
def za(s):
 out=[0]*len(s)
 for i in range(1,len(s)):
  while i+out[i]<len(s)and s[out[i]]==s[i+out[i]]:out[i]+=1
 return out
def matches(s,p):return [i for i in range(len(s)-len(p)+1)if s[i:i+len(p)]==p]
def vector(line):
 a=list(map(int,line.split()));assert a[0]==len(a)-1;return a[1:]
def sign(x):return(x>0)-(x<0)
with tempfile.TemporaryDirectory()as td:
 bins={}
 for name in ['trie','hash','hash-match','hash-compare','z','kmp','rolling','palindrome']:
  exe=Path(td)/name;src=R/f'audit/package03-work/strings-{name}.cpp';subprocess.run(['g++','-std=c++17','-O1','-fsanitize=undefined','-fno-sanitize-recover=all',str(src),'-o',str(exe)],check=True);bins[name]=exe
 for name in ['hash-match','hash-compare','rolling','palindrome']:
  src=(R/f'audit/package03-work/strings-{name}.cpp').read_text().replace('911382323','3').replace('97266353','3').replace('1000000007','97').replace('1000000009','97');p=Path(td)/(name+'-forced.cpp');p.write_text(src);exe=Path(td)/(name+'-forced');subprocess.run(['g++','-std=c++17','-O1','-fsanitize=undefined','-fno-sanitize-recover=all',str(p),'-o',str(exe)],check=True);bins[name+'-forced']=exe
 def run(name,data):
  global count
  count+=1;p=subprocess.run([bins[name]],input=data,text=True,capture_output=True,timeout=15);assert p.returncode==0,(name,p.stderr,data[:200]);return p.stdout.splitlines()
 for _ in range(75):
  words=[''.join(rng.choices('ABCDEF',k=rng.randrange(12)))for i in range(rng.randrange(30))];words+=words[:3];queries=[(op,''.join(rng.choices('ABCDEF',k=rng.randrange(12))))for op in 'CPL'for i in range(20)];queries +=[(op,s[:rng.randrange(len(s)+1)])for op in 'CPL'for s in words[:5]];data=str(len(words))+'\n'+'\n'.join(words)+ ('\n'if words else'')+str(len(queries))+'\n'+'\n'.join(f'{op} {s}'for op,s in queries)+'\n';out=list(map(int,run('trie',data)));dictionary=set(words);want=[]
  for op,s in queries:
   if op=='C':want.append(int(s in dictionary))
   elif op=='P':want.append(sum(w.startswith(s)for w in dictionary))
   else:want.append(max((len(w)for w in dictionary if s.startswith(w)),default=-1))
  assert out==want
 assert run('trie','4\nCANAL\nCANDY\nTHE\nTHERE\n5\nC THE\nC TH\nP TH\nL THERETO\nL THEN\n')==['1','0','2','5','3']
 s='A'*200000;assert run('trie','1\n'+s+'\n3\nC '+s+'\nP \nL '+s+'B\n')==['1','1','200000']
 for _ in range(80):
  s=''.join(rng.choices('ABCD # xyz',k=rng.randrange(50)));a=s.encode();q=[sorted([rng.randrange(len(a)+1),rng.randrange(len(a)+1)])for j in range(30)];mod=rng.choice([97,1000000007,972663749]);base=3 if mod==97 else 911382323;data=s+f'\n{base} {mod} {len(q)}\n'+'\n'.join(f'{l} {r}'for l,r in q);assert list(map(int,run('hash',data)))==[h(a[l:r],base,mod)for l,r in q]
 assert [h(b'ALLEY'[i:i+3],3,97)for i in range(3)]==[16,11,10]
 assert h(bytes([1,2,1]),31,1000000007)==1024 and h(bytes([2,1,2]),31,1000000007)==1955 and h(bytes([1,2,1,2,1]),31,1000000007)==984127
 assert run('hash','ALLEY\n3 97 3\n0 5\n0 0\n1 4')==['52','0',str(h(b'LLE',3,97))]
 assert run('hash','ADBA\n3 97 2\n0 2\n2 4')==['69','69']
 samples=[('ABABCBABC','ABC'),('HATTIVATTI','ATT'),('ACBACDACBACBACDA','ACB'),('AAAAA','AAA'),('',''),('','A'),('ABC',''),('#A##A#','#A#'),('A B A B',' B'),('ӨӨ #Ө','Ө'),('\0A\0','\0')]
 samples +=[(''.join(rng.choices('ABC #',k=rng.randrange(45))),''.join(rng.choices('ABC #',k=rng.randrange(15))))for _ in range(110)]
 for s,p in samples:
  a,b=s.encode(),p.encode();expected=matches(a,b);out=run('z',s+'\n'+p+'\n');assert vector(out[0])==za(a);joined=[c+1 for c in b]+[0]+[c+1 for c in a];assert vector(out[1])==za(joined);assert vector(out[2])==expected
  out=run('kmp',s+'\n'+p+'\n');assert vector(out[0])==pi(a);assert vector(out[1])==expected;borders=[i for i in range(1,len(a)+1)if a[:i]==a[-i:]];assert vector(out[2])==borders
  partial=next((k for k in range(1,len(a)+1)if all(a[i]==a[i%k]for i in range(len(a)))),0);whole=next((k for k in range(1,len(a)+1)if len(a)%k==0 and a==a[:k]*(len(a)//k)),0);assert list(map(int,out[3].split()))==[partial,whole]
  for name in ['hash-match','rolling']:
   for mode in ['C','V']:
    out=run(name,mode+'\n'+s+'\n'+p+'\n')[0].split();ans=list(map(int,out[2:]));assert int(out[1])==len(ans);assert out[0]==('EXACT'if mode=='V'else'CANDIDATES')
    want=expected if mode=='V'else[i for i in range(len(a)-len(b)+1)if dh(a[i:i+len(b)])==dh(b)];assert ans==want
 for name in ['z','kmp']:
  n=200000;s='A'*n;p='A'*100;out=run(name,s+'\n'+p+'\n');assert vector(out[0])==([0]+list(range(n-1,0,-1))if name=='z'else list(range(n)));assert vector(out[2 if name=='z'else 1])==list(range(n-99))
 assert vector(run('z','ACBACDACBACBACDA\nA\n')[0])==[0,0,0,2,0,0,5,0,0,7,0,0,2,0,0,1]
 out=run('z','HATTIVATTI\nATT\n');assert vector(out[1])==[0,0,0,0,0,3,0,0,0,0,3,0,0,0]and vector(out[2])==[1,6]
 assert vector(run('kmp','ABACABA\nABA\n')[2])==[1,3,7]
 assert run('kmp','ABCABCA\nABC\n')[3]=='3 7'
 for _ in range(80):
  s=''.join(rng.choices('ABCD #',k=rng.randrange(40)));a=s.encode();q=[sum((sorted([rng.randrange(len(a)+1),rng.randrange(len(a)+1)])for j in range(2)),[])for i in range(25)];suffix='\n'+str(len(q))+'\n'+'\n'.join(' '.join(map(str,row))for row in q)
  for mode in ['C','V']:
   out=run('hash-compare',mode+'\n'+s+suffix)
   for line,(l,r,u,v)in zip(out,q):
    x,y=a[l:r],a[u:v];k=next((i for i in range(min(len(x),len(y)))if x[i]!=y[i]),min(len(x),len(y)));label,actual,cmp=line.split();assert label==('EXACT'if mode=='V'else'ESTIMATE')
    collision=any(dh(x[:i])==dh(y[:i])and x[:i]!=y[:i]for i in range(min(len(x),len(y))+1))
    if mode=='V'or not collision:assert(int(actual),int(cmp))==(k,sign((x>y)-(x<y)))
  ranges=[sorted([rng.randrange(len(a)+1),rng.randrange(len(a)+1)])for i in range(25)];suf='\n'+str(len(ranges))+'\n'+'\n'.join(f'{l} {r}'for l,r in ranges)
  for mode in ['C','V']:
   out=run('palindrome',mode+'\n'+s+suf);want=[]
   for l,r in ranges:
    x=a[l:r];same=(x==x[::-1])if mode=='V'else dh(x)==dh(x[::-1]);want.append(('YES'if mode=='V'else'POSSIBLE')if same else'NO')
   assert out==want
 for name in ['hash-match','rolling']:
  assert run(name+'-forced','C\nBA\nAD\n')[0]=='CANDIDATES 1 0';assert run(name+'-forced','V\nBA\nAD\n')[0]=='EXACT 0'
 assert run('hash-compare-forced','C\nADZBAA\n1\n0 3 3 6')[0]=='ESTIMATE 2 1'
 assert run('hash-compare-forced','V\nADZBAA\n1\n0 3 3 6')[0]=='EXACT 0 -1'
 bad=None
 for n in range(2,9):
  for xs in itertools.product(b'ABCD',repeat=n):
   a=bytes(xs)
   if a!=a[::-1]and h(a,3,97)==h(a[::-1],3,97):bad=a.decode();break
  if bad:break
 assert bad
 assert run('palindrome-forced','C\n'+bad+f'\n1\n0 {len(bad)}')[0]=='POSSIBLE'
 assert run('palindrome-forced','V\n'+bad+f'\n1\n0 {len(bad)}')[0]=='NO'
 print(f'Strings: eight C++17 programs; {count} UBSan/oracle executions passed, including deliberate collision faults, empty/overlap/separator/UTF8-byte boundaries and200000-byte cases.')
