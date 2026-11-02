"""Real3.2.2 runtime/public Introduction: SVG output, startup failures and retry.
No fake ready promise or successful typesetter; only network failures/delays are injected.
"""
import argparse,functools,http.server,json,pathlib,threading,urllib.request
from playwright.sync_api import sync_playwright
ap=argparse.ArgumentParser();ap.add_argument('--payload-dir',required=True);a=ap.parse_args();R=pathlib.Path(__file__).resolve().parents[2];W=pathlib.Path(a.payload_dir);raw={n:(W/(n+'.json')).read_bytes()for n in ['get_catalog','get_tutorials']}
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}';results=[];cache={}
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for mode in ['normal','safe-failure','core-failure','safe-delay-retry','safe-delay-late','core-delay-retry']:
   page=b.new_page(viewport={'width':980,'height':950});page.clock.install();counts={'core':0,'safe':0};held=[];released=False;errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   def route(r):
    u=r.request.url
    if '/vendor/mathjax/tex-svg.js'in u:
     counts['core']+=1
     if mode=='core-failure'and counts['core']==1:return r.fulfill(status=503,body='temporary injected failure')
     if mode=='core-delay-retry'and not released:held.append(r);return
    if '/vendor/mathjax/ui/safe.js'in u:
     counts['safe']+=1
     if mode=='safe-failure'and counts['safe']==1:return r.fulfill(status=404,body='injected failed dependency')
     if mode in ['safe-delay-retry','safe-delay-late']and not released:held.append(r);return
    if u.startswith(base):return r.continue_()
    if 'cdn.jsdelivr.net/'in u and r.request.method=='GET':
     if u not in cache:cache[u]=urllib.request.urlopen(u,timeout=30).read()
     return r.fulfill(status=200,content_type='text/javascript',body=cache[u])
    for n in raw:
     if u.endswith('/rpc/'+n):return r.fulfill(status=200,content_type='application/json',body=raw[n])
    if u.endswith('/rpc/get_leaderboard'):return r.fulfill(status=503,content_type='application/json',body=b'{"message":"unrelated read"}')
    raise AssertionError('Unexpected operation '+r.request.method+' '+u)
   page.route('**/*',route);page.goto(base+'/index.html#tutorial/introduction',wait_until='domcontentloaded');page.wait_for_selector('#tutorial-content section');assert page.locator('#tutorial-content').inner_text()
   if mode.endswith('retry')or mode=='safe-delay-late':
    for _ in range(100):
     if held:break
     page.wait_for_timeout(30)
    assert held
    page.clock.fast_forward(31000);page.locator('#tutorial-math-retry').wait_for(state='visible');assert page.locator('#tutorial-content mjx-container').count()==0
    if mode.endswith('retry'):
     page.locator('#tutorial-math-retry').click();assert counts['core']==1,'pending timeout must not bootstrap again'
    released=True
    for r in held:
     path='vendor/mathjax/ui/safe.js'if'ui/safe.js'in r.request.url else'vendor/mathjax/tex-svg.js';r.fulfill(status=200,content_type='text/javascript',body=(R/path).read_bytes())
   elif mode in ['core-failure','safe-failure']:
    page.locator('#tutorial-math-retry').wait_for(state='visible');assert page.locator('#tutorial-content mjx-container').count()==0
    page.wait_for_timeout(150);assert counts['core']==1,'failed queued calls must not auto-bootstrap repeatedly';page.locator('#tutorial-math-retry').click()
   page.wait_for_function('document.querySelectorAll("#tutorial-content mjx-container").length===209',timeout=15000);assert page.locator('#tutorial-content mjx-merror').count()==0;assert page.locator('#tutorial-content .tutorial-math').evaluate_all('(xs)=>xs.every(x=>x.querySelector("mjx-container svg"))');page.wait_for_function('document.querySelector("#tutorial-math-message").textContent===""');assert page.locator('#tutorial-math-retry').is_hidden()
   assert page.locator('script[src*="vendor/mathjax/tex-svg.js"]').count()==1
   page.locator('#tutorial-language').select_option('en');page.wait_for_function('document.querySelectorAll("#tutorial-content mjx-container").length>100');assert page.locator('#tutorial-content mjx-merror').count()==0
   page.evaluate('location.hash="#tutorial/complexity"');page.wait_for_function('document.querySelectorAll("#tutorial-content mjx-container").length>20');page.wait_for_function('document.querySelector("#tutorial-content").getAttribute("aria-busy")==="false"')
   page.evaluate('''async()=>{const {renderBlock,typeset}=await import('./tutorials.js?v=100');const e=document.createElement('div');e.id='literal-sample-test';document.body.append(e);for(const language of ['Input','Output'])renderBlock({type:'code',language,text:'$n$\\n1  2\\n'},e,'mn');await typeset([e]);}''');assert page.locator('#literal-sample-test mjx-container').count()==0;assert page.locator('#literal-sample-test code').all_text_contents()==['$n$\n1  2\n']*2
   results.append({'mode':mode,'introduction_svg':209,'single_script':True,'core_requests':counts['core'],'safe_requests':counts['safe'],'literal_samples_preserved':True,'page_errors':errors});assert not errors,errors;page.close()
  b.close()
finally:s.shutdown()
report={'status':'passed','cases':results,'limits':'Actual vendored MathJax/Supabase SDK with anonymous captured public payloads; local browser, no authenticated live mobile/TLS bypass.'};(W/'mathjax-readiness.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
