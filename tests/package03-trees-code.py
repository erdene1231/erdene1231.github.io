import json,random,subprocess,tempfile,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1];random.seed(141331);runs=0
root8=[(1,2),(1,3),(1,4),(2,5),(2,6),(4,7),(6,8)];diam7=root8[:-1];all6=[(1,2),(1,3),(1,4),(2,5),(2,6)];binary=[[2,3],[4,5],[0,7],[0,0],[6,0],[0,0],[0,0]]
fixtures={'root8':{'n':8,'edges':root8,'subtree2':[2,5,6,8],'sizes':[8,4,1,2,1,2,1,1],'leaves':[3,5,7,8]},'diam7':{'n':7,'edges':diam7,'diameter':4,'path':[6,2,1,4,7]},'all6':{'n':6,'edges':all6,'ecc':[2,2,3,3,3,3],'down':[2,1,0,0,0,0],'up':[0,2,3,3,3,3]},'binary7':{'n':7,'children':binary,'pre':[1,2,4,5,6,3,7],'in':[4,2,6,5,1,3,7],'post':[4,6,5,2,7,3,1]}}
(R/'audit/package03-work/trees-fixtures.json').write_text(json.dumps(fixtures,indent=2)+'\n')
def distances(n,edges,s):
 a=[[]for _ in range(n+1)]
 for u,v in edges:a[u].append(v);a[v].append(u)
 d=[-1]*(n+1);par=[0]*(n+1);d[s]=0;q=collections.deque([s])
 while q:
  u=q.popleft()
  for v in a[u]:
   if d[v]<0:d[v]=d[u]+1;par[v]=u;q.append(v)
 return d,par
with tempfile.TemporaryDirectory()as tmp:
 exe={}
 for name in['recursive','analysis','binary','rebuild']:
  exe[name]=tmp+'/'+name;subprocess.run(['g++','-std=c++17','-O1','-g','-Wall','-Wextra','-Wconversion','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/trees-{name}.cpp'),'-o',exe[name]],check=True)
 def run(name,inp):
  global runs
  x=subprocess.run([exe[name]],input=inp,text=True,capture_output=True,check=True,timeout=30);assert not x.stderr,x.stderr;runs+=1;return x.stdout.splitlines()
 cases=[(8,root8),(7,diam7),(6,all6),(1,[]),(2,[(1,2)]),(9,[(1,v)for v in range(2,10)])]
 for _ in range(150):
  n=random.randint(1,14);es=[(u,random.randrange(1,u))for u in range(2,n+1)];random.shuffle(es);cases.append((n,es))
 for n,edges in cases:
  for root in set([1,random.randint(1,n)]):
   ds,pa=distances(n,edges,root);sub=[[False]*(n+1)for _ in range(n+1)]
   for v in range(1,n+1):
    u=v
    while u:sub[u][v]=True;u=pa[u]
   sz=[sum(sub[u])for u in range(1,n+1)];down=[max(ds[v]-ds[u]for v in range(1,n+1)if sub[u][v])for u in range(1,n+1)];all_d=[distances(n,edges,u)[0]for u in range(1,n+1)];ecc=[max(d[1:])for d in all_d];D=max(ecc);inp=f'{n} {root}\n'+'\n'.join(f'{a} {b}'for a,b in edges)+'\n';out=run('analysis',inp);assert [list(map(int,l.split()))for l in out[:5]]==[pa[1:],ds[1:],sz,down,ecc];a,d,b,c=map(int,out[5].split());assert a==d==D and all_d[b-1][c]==D
   out=run('recursive',inp);assert [list(map(int,l.split()))for l in out[1:]]==[pa[1:],ds[1:],sz];order=list(map(int,out[0].split()));assert len(set(order))==n and order[0]==root;pos={u:i for i,u in enumerate(order)};assert all(not pa[u]or pos[pa[u]]<pos[u]for u in range(1,n+1))
 # Binary reference traversals and exact structural reconstruction.
 def orders(ch,root):
  pre=[];ino=[];post=[]
  def go(u):
   if not u:return
   pre.append(u);go(ch[u-1][0]);ino.append(u);go(ch[u-1][1]);post.append(u)
  go(root);return[pre,ino,post]
 binarycases=[(7,binary,1),(0,[],0),(2,[[2,0],[0,0]],1),(2,[[0,2],[0,0]],1)]
 for _ in range(130):
  n=random.randint(1,15);ids=list(range(1,n+1));random.shuffle(ids);root=ids[0];ch=[[0,0]for _ in range(n)];slots=[(root,0),(root,1)]
  for u in ids[1:]:
   i=random.randrange(len(slots));p,s=slots.pop(i);ch[p-1][s]=u;slots.extend([(u,0),(u,1)])
  binarycases.append((n,ch,root))
 for n,ch,root in binarycases:
  want=orders(ch,root);out=run('binary',f'{n} {root}\n'+'\n'.join(f'{l} {r}'for l,r in ch)+'\n');assert[list(map(int,l.split()))for l in out]==want
  for mode,seq in[('PRE',want[0]),('POST',want[2])]:
   out=run('rebuild',f'{n} {mode}\n'+' '.join(map(str,seq))+'\n'+' '.join(map(str,want[1]))+'\n');assert int(out[0])==root and[list(map(int,l.split()))for l in out[1:]]==ch
 # Stack-safe deep input and tied branches.
 n=200000;chain='\n'.join(f'{u} {u+1}'for u in range(1,n));out=run('analysis',f'{n} 1\n'+chain+'\n');assert list(map(int,out[2].split()))==list(range(n,0,-1));assert list(map(int,out[4].split()))==[max(u-1,n-u)for u in range(1,n+1)];assert list(map(int,out[5].split()))[:2]==[n-1,n-1]
 star='\n'.join(f'1 {u}'for u in range(2,n+1));out=run('analysis',f'{n} 1\n'+star+'\n');assert list(map(int,out[4].split()))==[1]+[2]*(n-1)
 children='\n'.join(f'0 {u+1}'if u<n else'0 0'for u in range(1,n+1));out=run('binary',f'{n} 1\n'+children+'\n');assert list(map(int,out[0].split()))==list(range(1,n+1));assert list(map(int,out[2].split()))==list(range(n,0,-1))
 for mode,seq in[('PRE',range(1,n+1)),('POST',range(n,0,-1))]:
  out=run('rebuild',f'{n} {mode}\n'+' '.join(map(str,seq))+'\n'+' '.join(map(str,range(1,n+1)))+'\n');assert out[0]=='1'and out[1]=='0 2'and out[-1]=='0 0'and len(out)==n+1
 n=1000;out=run('recursive',f'{n} 1\n'+'\n'.join(f'{u} {u+1}'for u in range(1,n))+'\n');assert int(out[3].split()[0])==n
report={'status':'passed','programs':4,'UBSan_oracle_runs':runs,'oracles':'All-pairs BFS distances, brute ancestor membership/descendant heights, reference recursive binary traversals and exact child-slot reconstruction','stress':'200000-node chain/star analysis,200000-node binary traversal and both reconstruction modes;1000-node recursion fixture only','source_examples':'8-node subtree sizes;7-node diameter4;6-node eccentricities2,2,3,3,3,3; exact three7-node binary orders;two-node left/right ambiguity'};(R/'audit/PACKAGE03-TREES-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
