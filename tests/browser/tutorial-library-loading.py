"""Actual Supabase SDK and captured anonymous public RPC bytes, no Auth bypass.
Usage: python tests/browser/tutorial-library-loading.py --payload-dir DIR [--root DIR]
DIR contains fresh get_tutorials.json/get_catalog.json fetched through normal HTTPS.
No production mutation, credentials or synthetic successful catalog payloads.
"""
import argparse,functools,http.server,json,pathlib,threading,urllib.request,hashlib
from playwright.sync_api import sync_playwright
ap=argparse.ArgumentParser();ap.add_argument('--payload-dir',required=True);ap.add_argument('--root',default=str(pathlib.Path(__file__).resolve().parents[2]));ap.add_argument('--expect-blocked',action='store_true');args=ap.parse_args();R=pathlib.Path(args.root);W=pathlib.Path(args.payload_dir)
raw={n:(W/(n+'.json')).read_bytes()for n in ['get_catalog','get_tutorials']};rows=json.loads(raw['get_tutorials']);assert len(rows)==76
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}';results=[];sdk_cache={}
try:
 with sync_playwright()as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for mode in (['blocked-course']if args.expect_blocked else['normal','blocked-course','rpc-error']):
   page=b.new_page(viewport={'width':1200,'height':900});errors=[];held=[];requests=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   def route(r):
    u=r.request.url;requests.append(u)
    if mode=='blocked-course'and('study-plan.json'in u or'tutorials.json'in u):held.append(r);return
    if u.startswith(base):return r.continue_()
    if 'cdn.jsdelivr.net/'in u and r.request.method=='GET':
     if u not in sdk_cache:sdk_cache[u]=urllib.request.urlopen(u,timeout=30).read()
     return r.fulfill(status=200,content_type='text/javascript',body=sdk_cache[u])
    for n in raw:
     if u.endswith('/rpc/'+n):return r.fulfill(status=503 if mode=='rpc-error'and n=='get_tutorials'else 200,content_type='application/json',body=b'{"message":"temporary read failure"}'if mode=='rpc-error'and n=='get_tutorials'else raw[n])
    # Non-library leaderboard read is irrelevant and cannot write data.
    if u.endswith('/rpc/get_leaderboard'):return r.fulfill(status=503,content_type='application/json',body=b'{"message":"not part of library read"}')
    raise AssertionError('Unexpected external operation: '+r.request.method+' '+u)
   page.route('**/*',route);page.goto(base+'/index.html#tutorials',wait_until='domcontentloaded')
   if args.expect_blocked:
    page.wait_for_timeout(6000);assert page.locator('.tutorial-card').count()==0;results.append({'mode':mode,'baseline_zero_cards':True});[r.abort()for r in held];page.wait_for_timeout(100);page.close();continue
   if mode=='rpc-error':
    page.wait_for_function('document.querySelector("#tutorial-message").textContent.includes("баталгаажуулж чадсангүй")');assert page.locator('.tutorial-card').count()==0
   else:
    page.wait_for_selector('.tutorial-card',timeout=15000);assert page.locator('.tutorial-card').count()==76;assert page.locator('#tutorial-message').inner_text()==''
    for id in ['complexity','cpp-windows-vscode']:
     page.evaluate('(id)=>location.hash="#tutorial/"+id',id);page.wait_for_selector('#tutorial-content section');page.wait_for_function('document.querySelector("#tutorial-content").getAttribute("aria-busy")==="false"');assert page.locator('#tutorial-content mjx-merror').count()==0
    for width in [375,1200]:
     page.set_viewport_size({'width':width,'height':900});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    assert not errors,errors
    if mode=='blocked-course':assert not any('/tutorials.json?'in u for u in requests),'authoritative library unnecessarily fetched legacy seed'
   results.append({'mode':mode,'cards':page.locator('.tutorial-card').count(),'message':page.locator('#tutorial-message').inner_text(),'runtime_errors':errors});[r.abort()for r in held];page.wait_for_timeout(100);page.close()
  b.close()
finally:s.shutdown()
report={'status':'passed','results':results,'public_payloads':{n:{'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest()}for n,v in raw.items()},'limits':'Actual SDK, anonymous captured public RPC bytes, local native routes. Live site browser certificate blocked; no authenticated production save/read claim.'};(W/('baseline-test.json'if args.expect_blocked else'fixed-test.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
