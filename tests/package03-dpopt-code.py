import collections,functools,hashlib,itertools,json,random,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];rng=random.Random(20261030);names=['partition-slow','divide','merge-slow','knuth'];sources={n:ROOT/f'audit/package03-work/dpopt-{n}.cpp'for n in names}
def partition(a,k):
 n=len(a);s=[0]
 for x in a:s.append(s[-1]+x)
 prev=[0]+[10**30]*n;rows=[]
 for g in range(1,k+1):
  cur=[10**30]*(n+1);opt=[-1]*(n+1)
  for i in range(g,n+1):
   for j in range(g-1,i):
    v=prev[j]+(s[i]-s[j])**2
    if v<=cur[i]:cur[i]=v;opt[i]=j
  assert all(opt[i]<=opt[i+1]for i in range(g,n))
  rows.append((cur,opt));prev=cur
 return prev[n]
def merge(a):
 n=len(a);s=[0]
 for x in a:s.append(s[-1]+x)
 d=[[0]*n for _ in a];o=[[i for j in a]for i in range(n)]
 for length in range(2,n+1):
  for l in range(n-length+1):
   r=l+length-1;vals=[d[l][j]+d[j+1][r]+s[r+1]-s[l]for j in range(l,r)];d[l][r]=min(vals);o[l][r]=max(j+l for j,v in enumerate(vals)if v==d[l][r]);assert o[l][r-1]<=o[l][r]<=o[l+1][r]
 return d[0][-1]
@functools.lru_cache(None)
def brute_merge(a):
 if len(a)==1:return 0
 return min(a[i]+a[i+1]+brute_merge(a[:i]+(a[i]+a[i+1],)+a[i+2:])for i in range(len(a)-1))
def brute_partition(a,k):
 best=10**30
 for cuts in itertools.combinations(range(1,len(a)),k-1):
  borders=(0,)+cuts+(len(a),);best=min(best,sum(sum(a[l:r])**2 for l,r in zip(borders,borders[1:])))
 return best
part_cases=[];merge_cases=[];exhaustive=0
for n in range(1,7):
 for a in itertools.product(range(3),repeat=n):
  exhaustive+=1;m=merge(a);assert m==brute_merge(a);merge_cases.append((a,m))
  for k in range(1,n+1):v=partition(a,k);assert v==brute_partition(a,k);part_cases.append((a,k,v))
for _ in range(220):
 n=rng.randrange(1,36);a=tuple(rng.randrange(0,100001)for _ in range(n));k=rng.randrange(1,n+1);part_cases.append((a,k,partition(a,k)));merge_cases.append((a,merge(a)))
# Large allowed weights and all-zero ties are included separately from random data.
for a in [(10**5,)*8,(0,)*12,(0,1,0,1,0,1,0,1)]:
 for k in range(1,len(a)+1):part_cases.append((a,k,partition(a,k)))
for a in [(10**9,)*8,(0,)*12,(4,2,3,1)]:merge_cases.append((a,merge(a)))
with tempfile.TemporaryDirectory()as tmp:
 flags=['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=all'];exes={n:Path(tmp)/n for n in names}
 for n,p in sources.items():subprocess.run(flags+[str(p),'-o',str(exes[n])],check=True)
 def run(n,a,k=None,timeout=30):
  text=f'{len(a)}'+(' '+str(k)if k is not None else'')+'\n'+' '.join(map(str,a))+'\n';r=subprocess.run([str(exes[n])],input=text,text=True,capture_output=True,check=True,timeout=timeout);assert not r.stderr;return int(r.stdout)
 full_runs=0
 for a,k,v in part_cases[:20]+part_cases[-30:]+[rng.choice(part_cases)for _ in range(30)]:
  for name in ['partition-slow','divide']:assert run(name,a,k)==v;full_runs+=1
 for a,v in merge_cases[:20]+merge_cases[-20:]+[rng.choice(merge_cases)for _ in range(30)]:
  for name in ['merge-slow','knuth']:assert run(name,a)==v;full_runs+=1
 assert run('divide',[2,3,1,2,2,3,4,1],3)==110;assert run('knuth',[2,7,3,2,5])==43;assert run('knuth',[10,20,30,40])==190
 # Batch through the actual optimized structs; verify every row/interval and rightmost opt.
 divide=sources['divide'].read_text().split('int main() {')[0]+'''int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int t;cin>>t;while(t--){int n,k;cin>>n>>k;DivideDP fast(n);for(int i=1,x;i<=n;i++){cin>>x;fast.s[i]=fast.s[i-1]+x;}vector<ll>pr(n+1,DivideDP::INF),cur(n+1);pr[0]=0;for(int g=1;g<=k;g++){fill(cur.begin(),cur.end(),DivideDP::INF);vector<int>opt(n+1,-1);for(int i=g;i<=n;i++)for(int j=g-1;j<i;j++){if(pr[j]==DivideDP::INF)continue;ll sum=fast.s[i]-fast.s[j],v=pr[j]+sum*sum;if(v<=cur[i]){cur[i]=v;opt[i]=j;}}for(int i=g;i<n;i++)assert(opt[i]<=opt[i+1]);fast.pr=pr;fill(fast.cur.begin(),fast.cur.end(),DivideDP::INF);fast.calc(g,n,g-1,n-1);assert(fast.cur==cur);swap(pr,cur);}assert(fast.run(k)==pr[n]);cout<<pr[n]<<'\\n';}}\n'''
 knuth=sources['knuth'].read_text().split('int main() {')[0]+'''int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int t;cin>>t;while(t--){int n;cin>>n;Knuth fast(n);for(int i=1,x;i<=n;i++){cin>>x;fast.s[i]=fast.s[i-1]+x;}vector<vector<ll>>d(n+1,vector<ll>(n+1));vector<vector<int>>o(n+1,vector<int>(n+1));for(int i=1;i<=n;i++)o[i][i]=i;for(int len=2;len<=n;len++)for(int l=1;l+len-1<=n;l++){int r=l+len-1;d[l][r]=Knuth::INF;for(int j=l;j<r;j++){ll v=d[l][j]+d[j+1][r]+fast.s[r]-fast.s[l-1];if(v<=d[l][r]){d[l][r]=v;o[l][r]=j;}}assert(o[l][r-1]<=o[l][r]&&o[l][r]<=o[l+1][r]);}assert(fast.run()==d[1][n]);for(int l=1;l<=n;l++)for(int r=l;r<=n;r++){assert(fast.dp[l][r]==d[l][r]);assert(fast.opt[l][r]==o[l][r]);}cout<<d[1][n]<<'\\n';}}\n'''
 for name,text,cases in [('divide',divide,part_cases),('knuth',knuth,merge_cases)]:
  p=Path(tmp)/(name+'-batch.cpp');p.write_text(text);out=Path(tmp)/(name+'-batch');subprocess.run(flags+[str(p),'-o',str(out)],check=True)
  data=str(len(cases))+'\n'+''.join((f'{len(a)} {k}\n'if name=='divide'else f'{len(a)}\n')+' '.join(map(str,a))+'\n'for row in cases for a,k in [(row[0],row[1]if name=='divide'else 0)])
  p=subprocess.run([str(out)],input=data,text=True,capture_output=True,check=True,timeout=40);assert not p.stderr;assert list(map(int,p.stdout.split()))==[row[-1]for row in cases]
 # Deliberately invalid signed inputs: record failures rather than pretending assumptions hold.
 assert run('partition-slow',[-3,1,-2,-2],2)==18;assert run('divide',[-3,1,-2,-2],2)==20
 assert run('merge-slow',[-3,-2,-1,-3])==-20;assert run('knuth',[-3,-2,-1,-3])==-18
 # Maximum numeric domains and worst endpoint/tie cases.
 assert run('divide',[100000]*3000,1)==90000000000000000
 assert run('divide',[100000]*3000,3000,timeout=50)==30000000000000
 assert run('divide',[0]*3000,50)==0
 for n in range(1,25):h=(n-1).bit_length();assert merge((1,)*n)==n*(h+1)-(1<<h)
 n=5000;h=(n-1).bit_length();large=(n*(h+1)-(1<<h))*10**9
 assert run('knuth',[10**9]*n,timeout=50)==large;assert run('knuth',[0]*n,timeout=50)==0
report={'status':'passed','Cpp17_UBSan_programs':4,'compiled_source_sha256':{n:hashlib.sha256(p.read_bytes()).hexdigest()for n,p in sources.items()},'exhaustive_nonnegative_arrays_through6':exhaustive,'partition_cases':len(part_cases),'merge_cases':len(merge_cases),'independent_cut_enumeration_and_adjacent_merge_order_oracles':True,'all_divide_rows_and_knuth_intervals_and_rightmost_opts_match_baseline':True,'full_program_comparisons':full_runs,'official_samples_verified':True,'zero_ties_singletons_k1_kn':True,'negative_counterexamples':{'divide':{'baseline':18,'invalid_fast':20},'knuth':{'baseline':-20,'invalid_fast':-18}},'max_partition_n':3000,'max_partition_k':3000,'max_knuth_n':5000,'large_knuth_answer':str(large),'exact_ll_boundary_checks':True}
(ROOT/'audit/PACKAGE03-DPOPT-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
