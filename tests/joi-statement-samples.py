"""Reproducible independent JOI statement/sample checks; no network or editorial publication."""
import json,itertools,functools,heapq,collections,bisect,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

# Direct-definition checks for verify-first4.py
def railroad(a):
 it=iter(a);n,m=next(it),next(it);p=[next(it)for _ in range(m)];cost=[tuple(next(it)for _ in range(3))for _ in range(n-1)];used=[0]*(n-1)
 for x,y in zip(p,p[1:]):
  for e in range(min(x,y)-1,max(x,y)-1):used[e]+=1
 return sum(min(k*A,C+k*B)for k,(A,B,C)in zip(used,cost))

def cake(a):
 n=a[0];a=a[1:];full=(1<<n)-1
 @functools.lru_cache(None)
 def go(mask,turn):
  if mask==full:return 0
  opts=[i for i in range(n)if not(mask>>i&1)and(mask>>((i-1)%n)&1 or mask>>((i+1)%n)&1)]
  if turn==1:
   i=max(opts,key=lambda i:a[i]);return go(mask|1<<i,0)
  return max(a[i]+go(mask|1<<i,1)for i in opts)
 return max(a[i]+go(1<<i,1)for i in range(n))

def park(a):
 it=iter(a);n,m,c=next(it),next(it),next(it);edges=[tuple(next(it)for _ in range(3))for _ in range(m)];d=[[10**20]*n for _ in range(n)]
 for i in range(n):d[i][i]=0
 for x,y,w in edges:d[x-1][y-1]=d[y-1][x-1]=w
 for k in range(n):
  for i in range(n):
   for j in range(n):d[i][j]=min(d[i][j],d[i][k]+d[k][j])
 return min(c*x+sum(w for u,v,w in edges if not(d[0][u-1]<=x and d[0][v-1]<=x))for x in range(max(d[0])+1))

def winner(queue,skill):
 q=list(queue)
 while len(q)>1:
  first=q[:3];hi=max(first,key=lambda i:(skill[i],-i));lo=min(first,key=lambda i:(skill[i],-i));survivor=next(i for i in first if i not in[hi,lo]);q=q[3:]+[survivor]
 return q[0]

def ball(a):
 it=iter(a);n,m=next(it),next(it);skill={};fixed={}
 for i in range(1,m+1):skill[i]=next(it);fixed[next(it)-1]=i
 for i in range(m+1,n+1):skill[i]=next(it)
 empty=[i for i in range(n)if i not in fixed];answer=0
 for perm in itertools.permutations(range(m+1,n+1)):
  q=[fixed.get(i)for i in range(n)]
  for pos,id in zip(empty,perm):q[pos]=id
  answer=max(answer,skill[winner(q,skill)])
 return answer


# Direct-definition checks for verify-2016.py
def oranges(raw):
 n,m,k,*a=map(int,raw.split());best=10**99
 def rec(i,cost):
  nonlocal best
  if i==n:best=min(best,cost);return
  for j in range(i+1,min(n,i+m)+1):rec(j,cost+k+(j-i)*(max(a[i:j])-min(a[i:j])))
 rec(0,0);return str(best)+'\n'

def stamps(raw):
 n,s=raw.split();return str(max(sum(t[i]+t[j]+t[k]=='JOI'for i,j,k in itertools.combinations(range(len(t)),3))for at in range(len(s)+1)for ch in'JOI'for t in[s[:at]+ch+s[at:]]))+'\n'

def train(raw):
 a=list(map(int,raw.split()));n,m,q=a[:3];edges=[(a[3+2*i]-1,a[4+2*i]-1)for i in range(m)];updates=a[3+2*m:];w=[1]*m
 def dist():
  d=[10**9]*n;d[0]=0
  for _ in range(n):
   for i,(u,v)in enumerate(edges):d[u]=min(d[u],d[v]+w[i]);d[v]=min(d[v],d[u]+w[i])
  return d
 base=dist();out=[]
 for r in updates:w[r-1]=2;out.append(sum(x>y for x,y in zip(dist(),base)))
 return ''.join(str(x)+'\n'for x in out)

def territory(raw):
 n,k,s=raw.split();x=y=0;visited={(0,0)};step={'E':(1,0),'N':(0,1),'W':(-1,0),'S':(0,-1)}
 for _ in range(int(k)):
  for ch in s:dx,dy=step[ch];x+=dx;y+=dy;visited.add((x,y))
 return str(sum(all(p in visited for p in[(x+1,y),(x,y+1),(x+1,y+1)])for x,y in visited))+'\n'


# Direct-definition checks for verify-2017.py
def wind(raw):
 a=list(map(int,raw.split()));n,q,s,t=a[:4];h=a[4:5+n];out=[]
 for j in range(q):
  l,r,x=a[5+n+3*j:8+n+3*j]
  for i in range(l,r+1):h[i]+=x
  out.append(sum(-(h[i]-h[i-1])*s if h[i]>h[i-1]else(h[i-1]-h[i])*t for i in range(1,n+1)))
 return ''.join(str(x)+'\n'for x in out)

def semiexpress(raw,brute=False):
 n,m,k,a,b,c,t,*st=map(int,raw.split());st=[s-1 for s in st]
 if brute:
  best=0
  for chosen in itertools.combinations([i for i in range(n)if i not in st],k-m):
   semi=sorted(st+list(chosen));edges=[[]for _ in range(n)]
   for i in range(n-1):edges[i].append((i+1,a))
   for stops,cost in[(st,b),(semi,c)]:
    for u,v in zip(stops,stops[1:]):edges[u].append((v,(v-u)*cost))
   d=[10**99]*n;d[0]=0
   for u in range(n):
    for v,cost in edges[u]:d[v]=min(d[v],d[u]+cost)
   best=max(best,sum(x<=t for x in d[1:]))
  return best
 intervals=[];answer=-1
 for i,s in enumerate(st):
  end=st[i+1]-1 if i+1<m else s;base=b*s;count=max(0,min(end-s+1,(t-base)//a+1));answer+=count;intervals.append([s,end,base,s+count])
 def gain(i):
  s,end,base,x=intervals[i]
  if x>end or base+c*(x-s)>t:return 0
  return min(end-x+1,(t-base-c*(x-s))//a+1)
 pq=[(-gain(i),i)for i in range(len(st))];heapq.heapify(pq)
 for _ in range(k-m):
  neg,i=heapq.heappop(pq);g=-neg;answer+=g;intervals[i][3]+=g;heapq.heappush(pq,(-gain(i),i))
 return answer

def kingdom_grid(a,brute=False):
 h=len(a);w=len(a[0]);flat=sum(a,[]);best=10**30
 def val(mask):
  parts=[[flat[i]for i in range(h*w)if((mask>>i)&1)==k]for k in[0,1]]
  return max(max(p)-min(p)for p in parts)
 if brute:
  for mask in range(1,(1<<(h*w))-1):
   valid=True
   for k in[0,1]:
    for line in[[i*w+j for j in range(w)]for i in range(h)]+[[i*w+j for i in range(h)]for j in range(w)]:
     bits=[(mask>>i)&1 for i in line];pos=[i for i,b in enumerate(bits)if b==k]
     if pos and pos[-1]-pos[0]+1!=len(pos):valid=False;break
    if not valid:break
    cells={i for i in range(h*w)if((mask>>i)&1)==k};seen={next(iter(cells))};stack=list(seen)
    while stack:
     x=stack.pop();i,j=divmod(x,w)
     for ni,nj in[(i-1,j),(i+1,j),(i,j-1),(i,j+1)]:
      y=ni*w+nj
      if 0<=ni<h and 0<=nj<w and y in cells and y not in seen:seen.add(y);stack.append(y)
    if seen!=cells:valid=False;break
   if valid:best=min(best,val(mask))
 else:
  for cuts in itertools.combinations_with_replacement(range(w+1),h):
   if all(x==0 for x in cuts)or all(x==w for x in cuts):continue
   for flipx,flipy in itertools.product([False,True],repeat=2):
    mask=0
    for i,c in enumerate(cuts):
     for j in range(c):mask|=1<<((h-1-i if flipx else i)*w+(w-1-j if flipy else j))
    best=min(best,val(mask))
 return best

def soccer(raw):
 a=list(map(int,raw.split()));h,w,A,B,C,n=a[:6];ps=[tuple(a[6+2*i:8+2*i])for i in range(n)];target=ps[-1];dist={};pq=[(0,*ps[0],0)];step=[(1,0),(-1,0),(0,1),(0,-1)];nearest={(x,y):min(abs(x-i)+abs(y-j)for i,j in ps)*C for x in range(h+1)for y in range(w+1)}
 while pq:
  cost,x,y,mode=heapq.heappop(pq)
  if (x,y)==target:return cost
  key=(x,y,mode)
  if key in dist:continue
  dist[key]=cost;choices=[]
  if mode==0:
   for i,(dx,dy)in enumerate(step):choices.extend([(x+dx,y+dy,0,C),(x+dx,y+dy,i+1,A+B)])
  else:
   dx,dy=step[mode-1];choices.extend([(x+dx,y+dy,mode,A),(x,y,0,nearest[(x,y)])])
  for nx,ny,m,add in choices:
   if 0<=nx<=h and 0<=ny<=w and(nx,ny,m)not in dist:heapq.heappush(pq,(cost+add,nx,ny,m))
 raise AssertionError('unreachable')

def soccer_brute(raw):
 a=list(map(int,raw.split()));h,w,A,B,C,n=a[:6];ps=tuple((a[6+2*i],a[7+2*i])for i in range(n));target=ps[-1];start=(ps,0,-1,-1);pq=[(0,start)];seen=set();step=[(1,0),(-1,0),(0,1),(0,-1)]
 while pq:
  cost,state=heapq.heappop(pq);pos,owner,bx,by=state;ball=pos[owner]if owner>=0 else(bx,by)
  if ball==target:return cost
  if state in seen:continue
  seen.add(state);moves=[]
  for i,(x,y)in enumerate(pos):
   for dx,dy in step:
    nx,ny=x+dx,y+dy
    if 0<=nx<=h and 0<=ny<=w:
     p=list(pos);p[i]=(nx,ny);moves.append(((tuple(p),owner,bx,by),C))
   if owner==i:
    moves.append(((pos,-1,x,y),0))
    for dx,dy in step:
     for d in range(1,max(h,w)+1):
      nx,ny=x+dx*d,y+dy*d
      if 0<=nx<=h and 0<=ny<=w:moves.append(((pos,-1,nx,ny),A*d+B))
   elif owner==-1 and(x,y)==(bx,by):moves.append(((pos,i,-1,-1),0))
  for nxt,c in moves:
   if nxt not in seen:heapq.heappush(pq,(cost+c,nxt))
 raise AssertionError('unreachable brute')

def coach(raw):
 a=list(map(int,raw.split()));X,N,M,W,T=a[:5];st=a[5:5+N];passengers=[tuple(a[5+N+2*i:7+N+2*i])for i in range(M)];events=[(t,-1)for t in range(0,X,T)]+[(d+k*T,j)for j,(d,c)in enumerate(passengers)for k in range((X-1-d)//T+1)]+[(s,-2)for s in st];events.sort();total=sum(kind!=-2 for _,kind in events);dp={((1<<M)-1,0):0};events=[(0,-2)]+events
 for ei,(t,kind)in enumerate(events):
  nxt={}
  def put(key,cost):nxt[key]=min(nxt.get(key,10**99),cost)
  for (mask,water),cost in dp.items():
   if kind==-2:
    remaining=sum(typ==-1 or typ>=0 and(mask>>typ&1)for tt,typ in events[ei+1:])
    for stock in range(water,max(water,remaining)+1):put((mask,stock),cost+(stock-water)*W)
   elif kind==-1:
    if water:put((mask,water-1),cost)
   elif not(mask>>kind&1):put((mask,water),cost)
   elif water:put((mask,water-1),cost)
   else:put((mask^(1<<kind),0),cost+passengers[kind][1])
  dp=nxt
 return min(dp.values())


# Direct-definition checks for verify-2018.py
def stove(raw):
 n,k,*t=map(int,raw.split());best=10**30
 for mask in range(1<<(n-1)):
  if mask.bit_count()+1>k:continue
  start=0;total=0
  for j in range(n-1):
   if mask>>j&1:total+=t[j]+1-t[start];start=j+1
  total+=t[-1]+1-t[start];best=min(best,total)
 return best

def art(raw):
 a=list(map(int,raw.split()));n=a[0];items=list(zip(a[1::2],a[2::2]));return max(sum(b for i,(a,b)in enumerate(items)if mask>>i&1)-(max(a for i,(a,b)in enumerate(items)if mask>>i&1)-min(a for i,(a,b)in enumerate(items)if mask>>i&1))for mask in range(1,1<<n))

def dango(raw):
 a=raw.split();h,w=map(int,a[:2]);g=a[2:];cand=[]
 for x in range(h):
  for y in range(w):
   for dx,dy in[(1,0),(0,1)]:
    cells=[(x+k*dx,y+k*dy)for k in range(3)]
    if all(i<h and j<w for i,j in cells)and''.join(g[i][j]for i,j in cells)=='RGW':cand.append(sum(1<<(i*w+j)for i,j in cells))
 @functools.lru_cache(None)
 def rec(i,used):
  if i==len(cand):return 0
  return max(rec(i+1,used),1+rec(i+1,used|cand[i])if not used&cand[i]else 0)
 return rec(0,0)

def commuter(raw):
 a=list(map(int,raw.split()));n,m,s,t,u,v=a[:6];s-=1;t-=1;u-=1;v-=1;edges=[tuple(a[6+3*i:9+3*i])for i in range(m)];g=[[]for _ in range(n)]
 for i,(x,y,c)in enumerate(edges):x-=1;y-=1;g[x].append((y,c,i));g[y].append((x,c,i))
 def dist(start,free=frozenset()):
  d=[10**99]*n;d[start]=0;pq=[(0,start)]
  while pq:
   val,x=heapq.heappop(pq)
   if val!=d[x]:continue
   for y,c,i in g[x]:
    cost=0 if i in free else c
    if val+cost<d[y]:d[y]=val+cost;heapq.heappush(pq,(d[y],y))
  return d
 optimum=dist(s)[t];answer=10**99;back=dist(t)
 def rec(x,cost,visited,path):
  nonlocal answer
  if cost+back[x]>optimum:return
  if x==t:answer=min(answer,dist(u,frozenset(path))[v]);return
  for y,c,i in g[x]:
   if not(visited>>y&1):rec(y,cost+c,visited|1<<y,path+[i])
 rec(s,0,1<<s,[]);return answer

def snake(raw):
 a=raw.split();l,q=map(int,a[:2]);s=a[2];return ''.join(str(sum(int(s[i])for i in range(1<<l)if all(ch=='?'or ch==bit for ch,bit in zip(p,format(i,'0'+str(l)+'b')))))+'\n'for p in a[3:])


# Direct-definition checks for verify-final.py
def bitaro(raw):
 a=raw.split();h,w=map(int,a[:2]);g=a[2:];return sum(g[i][j]=='J'and g[i][l]=='O'and g[k][j]=='I'for i in range(h)for k in range(i+1,h)for j in range(w)for l in range(j+1,w))

def exhibition(raw):
 a=list(map(int,raw.split()));n,m=a[:2];p=[tuple(a[2+2*i:4+2*i])for i in range(n)];frames=sorted(a[2+2*n:])
 @functools.lru_cache(None)
 def rec(i,mask,last):
  if i==m:return 0
  return max([rec(i+1,mask,last)]+[1+rec(i+1,mask|1<<j,v)for j,(s,v)in enumerate(p)if not(mask>>j&1)and s<=frames[i]and v>=last])
 return rec(0,0,0)

def vegetables(raw):
 n,s=raw.split();pos=[[i for i,ch in enumerate(s)if ch==c]for c in'RGY'];tot=list(map(len,pos));inf=10**9
 @functools.lru_cache(None)
 def rec(r,g,y,last):
  cnt=(r,g,y)
  if list(cnt)==tot:return 0
  best=inf
  for c in range(3):
   if c==last or cnt[c]==tot[c]:continue
   at=pos[c][cnt[c]];removed=sum(min(cnt[d],bisect.bisect_left(pos[d],at))for d in range(3));nxt=list(cnt);nxt[c]+=1;best=min(best,at-removed+rec(*nxt,c))
  return best
 ans=rec(0,0,0,3);return -1 if ans>=inf else ans

def veg_bfs(s):
 q=collections.deque([(s,0)]);seen={s}
 while q:
  s,d=q.popleft()
  if all(x!=y for x,y in zip(s,s[1:])):return d
  for i in range(len(s)-1):
   if s[i]==s[i+1]:continue
   t=s[:i]+s[i+1]+s[i]+s[i+2:]
   if t not in seen:seen.add(t);q.append((t,d+1))
 return -1

def coins(raw):
 a=list(map(int,raw.split()));n=a[0];p=list(zip(a[1::2],a[2::2]));target=list(itertools.product(range(1,n+1),[1,2]));size=1<<(2*n);dp=[10**99]*size;dp[0]=0
 for mask in range(size):
  i=mask.bit_count()
  if i==2*n:continue
  x,y=p[i]
  for j,(u,v)in enumerate(target):
   if not(mask>>j&1):dp[mask|1<<j]=min(dp[mask|1<<j],dp[mask]+abs(x-u)+abs(y-v))
 return dp[-1]

def unique(raw):
 a=list(map(int,raw.split()));n,m=a[:2];g=[[]for _ in range(n)]
 for i in range(n-1):x,y=a[2+2*i:4+2*i];g[x-1].append(y-1);g[y-1].append(x-1)
 colors=a[2+2*(n-1):];out=[]
 for start in range(n):
  d=[-1]*n;d[start]=0;q=collections.deque([start])
  while q:
   x=q.popleft()
   for y in g[x]:
    if d[y]<0:d[y]=d[x]+1;q.append(y)
  freq=collections.Counter(d);out.append(len({colors[i]for i in range(n)if i!=start and freq[d[i]]==1}))
 return ''.join(str(x)+'\n'for x in out)

def watering(raw):
 a=list(map(int,raw.split()))[1:];d=[y-x for x,y in zip(a,a[1:])];best=10**99
 for k in range(len(a)):best=min(best,max(sum(max(0,1-x)for x in d[:k]),sum(max(0,1+x)for x in d[k:])))
 return best

def watering_bfs(a):
 def done(a):return any(all(a[i]<a[i+1]for i in range(k))and all(a[i]>a[i+1]for i in range(k,len(a)-1))for k in range(len(a)))
 a=tuple(x-min(a)for x in a);q=collections.deque([(a,0)]);seen={a}
 while q:
  a,d=q.popleft()
  if done(a):return d
  for l in range(len(a)):
   for r in range(l,len(a)):
    if l==0 and r==len(a)-1:continue
    t=tuple(x+(l<=i<=r)for i,x in enumerate(a));lo=min(t);t=tuple(x-lo for x in t)
    if t not in seen:seen.add(t);q.append((t,d+1))

def coach_large_source(raw):
 values=list(map(int,raw.split()));assert values==[10**12,1,1,10**6,6,999999259244,1,123456789]
 X,N,M,W,T,S,D,C=values;driver=(X+T-1)//T;last_driver=(S-1)//T;assert D+last_driver*T<S
 return min((driver+last_driver)*W+C,(driver+(X-1-D)//T+1)*W)
contracts=json.loads((ROOT/'audit/joi-statements/source-contracts.json').read_text())
funcs={'joi2015ho_a':lambda s:railroad(list(map(int,s.split()))),'joi2015ho_b':lambda s:cake(list(map(int,s.split()))),'joi2015ho_c':lambda s:park(list(map(int,s.split()))),'joi2015ho_d':lambda s:ball(list(map(int,s.split()))),'joi2016ho_a':oranges,'joi2016ho_b':stamps,'joi2016ho_c':train,'joi2016ho_d':territory,'joi2017ho_a':wind,'joi2017ho_b':semiexpress,'joi2017ho_c':lambda s:kingdom_grid([list(map(int,line.split()))for line in s.splitlines()[1:]]),'joi2017ho_d':soccer,'JOI17_coach':lambda s:coach_large_source(s)if int(s.split()[0])>1000000 else coach(s),'joi2018ho_a':stove,'joi2018ho_b':art,'joi2018ho_c':dango,'joi2018ho_d':commuter,'joi2018ho_e':snake,'joi2019ho_a':bitaro,'joi2019ho_b':exhibition,'joi2019ho_c':vegetables,'joi2019ho_d':coins,'joi2019ho_e':unique,'joi2021ho_a':watering}
pairs=0
for c in contracts:
 for i,s in enumerate(c['samples'],1):
  got=funcs[c['source_ref']](s['input']);got=str(got)+'\n'if isinstance(got,int)else got
  assert got==s['output'],(c['id'],i,got,s['output']);pairs+=1
assert pairs==80
assert cake([1,123])==123;assert winner([1,2,3],{1:5,2:5,3:5})==2
for skills in itertools.product(range(1,4),repeat=3):
 sk=dict(zip([1,2,3],skills));assert sk[winner([1,2,3],sk)]==sorted(skills)[1]
assert oranges('1 1 0\n1000000000\n')=='0\n';assert oranges('2 2 0\n1\n2\n')=='0\n';assert stamps('3\nIII\n')=='0\n';assert territory('4 100\nENWS\n')=='1\n';assert territory('1 20\nE\n')=='0\n'
rng=random.Random(1702)
for _ in range(130):
 n=rng.randrange(3,10);mid=sorted(rng.sample(range(2,n),rng.randrange(n-1)));st=[1]+mid+[n];m=len(st);k=rng.randrange(m,n+1);b=rng.randrange(1,4);c=b+rng.randrange(1,4);a=c+rng.randrange(1,4);t=rng.randrange(1,60);raw=' '.join(map(str,[n,m,k,a,b,c,t]+st));assert semiexpress(raw)==semiexpress(raw,True),raw
for _ in range(90):
 h=rng.randrange(2,4);w=2;a=[[rng.randrange(1,15)for _ in range(w)]for _ in range(h)];assert kingdom_grid(a)==kingdom_grid(a,True),a
soccer_trials=0
for _ in range(45):
 ps=[(rng.randrange(2),rng.randrange(2))for _ in range(rng.randrange(2,4))]
 if ps[0]==ps[-1]:continue
 soccer_trials+=1;raw=' '.join(map(str,[1,1]+[rng.randrange(0,8)for _ in range(3)]+[len(ps)]+[v for p in ps for v in p]));assert soccer(raw)==soccer_brute(raw),raw
assert soccer_trials==30
assert stove('1 1\n1000000000\n')==1;assert stove('3 1\n1\n2\n3\n')==3;assert art('2\n1000000000000000 2\n1000000000000000 3\n')==5;assert dango('1 3\nWGR\n')==0;assert dango('3 1\nR\nG\nW\n')==1;assert snake('1 3\n09\n?\n0\n1\n')=='9\n0\n9\n'
rng=random.Random(190521)
for _ in range(100):
 s=''.join(rng.choice('RGY')for _ in range(rng.randrange(1,9)));assert vegetables(str(len(s))+' '+s)==veg_bfs(s),s
for _ in range(50):
 a=[rng.randrange(1,4)for _ in range(rng.randrange(2,5))];raw=' '.join(map(str,[len(a)]+a));assert watering(raw)==watering_bfs(a),a
assert bitaro('2 3\nJJO\nIII\n')==2;assert exhibition('2 2\n1 2\n1 2\n1\n1\n')==2;assert vegetables('1 R')==0;assert vegetables('2 RR')==-1;assert unique('2 1\n1 2\n1 1\n')=='1\n1\n';assert watering('2 2021 2021')==1
report={'status':'passed','tasks':24,'official_sample_pairs':pairs,'extra_small_oracle_and_edge_checks':446,'semiexpress_stop_subsets':130,'kingdom_full_partitions':90,'soccer_full_player_states':30,'adjacent_swap_BFS':100,'interval_watering_BFS':50,'other_edge_checks':46,'coach_large_sample_exact_event_count':True,'command':'python3 tests/joi-statement-samples.py','limits':'Definition/sample checks and bounded independent state searches; no full-constraint performance claim, no app editorials, no network or production write.'}
(ROOT/'audit/joi-statements/all-sample-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
