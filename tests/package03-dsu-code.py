import json,random,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];rng=random.Random(8732)
with tempfile.TemporaryDirectory()as t:
 t=Path(t);src=(R/'audit/package03-work/dsu.cpp').read_text();h=src.split('int main() {')[0]+'''int main(){int n,m;cin>>n>>m;DSU d(n);for(int i=0,a,b;i<m;i++){cin>>a>>b;bool merged=d.unite(a,b);cout<<merged<<' '<<d.cnt<<' '<<d.mx;for(int v=1;v<=n;v++){cout<<' '<<d.size(v);for(int u=1;u<=n;u++)cout<<' '<<d.same(u,v);}cout<<'\\n';}}''';(t/'h.cpp').write_text(h)
 for name,s in [('program',src),('harness',h)]:
  f=t/(name+'.cpp');f.write_text(s);subprocess.run(['g++','-std=c++17','-O1','-fsanitize=undefined','-fno-sanitize-recover=all',str(f),'-o',str(t/name)],check=True)
 cases=[(5,[(1,2),(3,4),(2,3),(1,4),(5,4)]),(1,[(1,1)]*5)]
 for _ in range(150):
  n=rng.randrange(1,25);cases.append((n,[(rng.randrange(1,n+1),rng.randrange(1,n+1))for _ in range(50)]))
 ops=0
 for n,e in cases:
  inp=f'{n} {len(e)}\n'+''.join(f'{a} {b}\n'for a,b in e);p=subprocess.run([str(t/'harness')],input=inp,text=True,capture_output=True,check=True);assert not p.stderr;rows=[list(map(int,l.split()))for l in p.stdout.splitlines()];labels=list(range(n+1));expected=[]
  for (a,b),row in zip(e,rows):
   old,new=labels[b],labels[a];merged=old!=new;labels=[new if x==old else x for x in labels];sizes={x:labels[1:].count(x)for x in set(labels[1:])};out=[int(merged),len(sizes),max(sizes.values())]
   for v in range(1,n+1):out+=[sizes[labels[v]]]+[int(labels[v]==labels[u])for u in range(1,n+1)]
   assert row==out;expected.append(out[1:3]);ops+=1
  p=subprocess.run([str(t/'program')],input=inp,text=True,capture_output=True,check=True);assert not p.stderr;assert [list(map(int,l.split()))for l in p.stdout.splitlines()]==expected
 n=200000;e=[(i,i+1)for i in range(1,n)]+[(1,n),(n,n)];inp=f'{n} {len(e)}\n'+''.join(f'{a} {b}\n'for a,b in e);p=subprocess.run([str(t/'program')],input=inp,text=True,capture_output=True,check=True);assert not p.stderr
 for i,l in enumerate(p.stdout.splitlines()):assert list(map(int,l.split()))==[max(1,n-i-1),min(n,i+2)]
 out={'status':'passed','CXX17_UBSan':True,'independent_relabeling_model':True,'sequences':len(cases),'operations':ops,'all_sizes_and_pair_queries_checked':True,'max_n':n,'repeated_and_self_unions':True};(R/'audit/PACKAGE03-DSU-CODE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
