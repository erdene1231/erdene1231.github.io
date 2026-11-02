"""Reproduce76-count/empty-list with real SDK/public payloads and stalled MathJax.
Progress is synthetic guest read state using the actual learning store, never
production authentication or account mutation. Run with --payload-dir DIR.
"""
import argparse,functools,http.server,json,pathlib,re,threading,urllib.request
from playwright.sync_api import sync_playwright
ap=argparse.ArgumentParser();ap.add_argument('--payload-dir',required=True);ap.add_argument('--root',default=str(pathlib.Path(__file__).resolve().parents[2]));ap.add_argument('--expect-mismatch',action='store_true');a=ap.parse_args();R=pathlib.Path(a.root);W=pathlib.Path(a.payload_dir);raw={n:(W/(n+'.json')).read_bytes()for n in ['get_catalog','get_tutorials']};assert len(json.loads(raw['get_tutorials']))==76
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}';held_math=[];held_rpc=[];released=False;checks=[]
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1280,'height':900});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.add_init_script("localStorage.setItem('erdene:learning:v1:guest',JSON.stringify({records:{'tutorial:introduction':{readSections:[0],checks:[],viewedAt:'2026-11-01T00:00:00Z'}},dirty:[]}));")
  def route(r):
   u=r.request.url
   if '/vendor/mathjax/tex-svg.js'in u and not released:held_math.append(r);page.evaluate("document.documentElement.dataset.mathWaiting='1'");return
   if u.startswith(base):return r.continue_()
   if 'cdn.jsdelivr.net/'in u and r.request.method=='GET':return r.fulfill(status=200,content_type='text/javascript',body=urllib.request.urlopen(u,timeout=30).read())
   if u.endswith('/rpc/get_tutorials'):
    if released:return r.fulfill(status=200,content_type='application/json',body=raw['get_tutorials'])
    held_rpc.append(r);page.evaluate("document.documentElement.dataset.rpcWaiting='1'");return
   if u.endswith('/rpc/get_catalog'):return r.fulfill(status=200,content_type='application/json',body=raw['get_catalog'])
   if u.endswith('/rpc/get_leaderboard'):return r.fulfill(status=503,content_type='application/json',body=b'{"message":"unrelated read"}')
   raise AssertionError('Unexpected external operation '+r.request.method+' '+u)
  page.route('**/*',route);page.goto(base+'/index.html#tutorials',wait_until='domcontentloaded');page.wait_for_function("document.querySelector('#tutorial-grid').textContent.includes('Тохирох хичээл олдсонгүй')&&document.documentElement.dataset.mathWaiting&&document.documentElement.dataset.rpcWaiting");assert held_math and held_rpc
  for r in held_rpc:r.fulfill(status=200,content_type='application/json',body=raw['get_tutorials'])
  page.wait_for_function("document.querySelector('#tutorial-count').textContent.startsWith('76 / 76')")
  if a.expect_mismatch:
   assert page.locator('.tutorial-card').count()==0;assert 'Тохирох хичээл олдсонгүй'in page.locator('#tutorial-grid').inner_text();checks.append('baseline reproduces screenshot:76 count,0 cards, stale empty state with MathJax pending')
  else:
   def consistent():
    count=int(re.match(r'\d+',page.locator('#tutorial-count').inner_text())[0]);assert page.locator('.tutorial-card').count()==count
    if count>0:assert not any(text in page.locator('#tutorial-grid').inner_text()for text in ['Тохирох хичээл олдсонгүй','No matching tutorials'])
   consistent();assert page.locator('.tutorial-card').count()==76;checks.append('76 cards immediately while MathJax remains pending, with loaded native progress state')
   assert page.locator('.tutorial-card').first.locator('.tutorial-learning-state').inner_text()=='Уншсан'
   categories=page.locator('#tutorial-category option').evaluate_all('(xs)=>xs.map(x=>x.value)');
   for category in categories:
    page.locator('#tutorial-category').select_option(category);consistent();assert page.locator('.tutorial-card').count()>0
   page.locator('#tutorial-category').select_option('')
   for lang in ['en','mn']:
    page.locator('#tutorial-language').select_option(lang)
    for order in ['priority','']:
     page.locator('#tutorial-priority-sort').select_option(order);consistent();assert page.locator('.tutorial-card').count()==76
   page.locator('#tutorial-search').fill('no-matching-lesson-zzzz');consistent();assert page.locator('.tutorial-card').count()==0;page.locator('#tutorial-search').fill('');consistent()
   for priority in ['high','medium','low','']:
    page.locator('#tutorial-priority-filter').select_option(priority);consistent()
   page.locator('#tutorial-level').select_option('beginner');consistent();page.locator('#tutorial-level').select_option('');consistent();assert page.locator('.tutorial-card').count()==76
   checks.append('all actual groups, MN/EN, default/priority order, search and level/priority changes keep count/cards consistent before math loads')
  if not a.expect_mismatch:
   for id in ['complexity','cpp-windows-vscode']:
    page.evaluate('(id)=>location.hash="#tutorial/"+id+"/part/0"',id);page.wait_for_selector('#tutorial-content section');page.wait_for_function('(id)=>document.querySelector("#tutorial-content>section").id.startsWith("tutorial-"+id+"-")',arg=id);assert page.locator('#tutorial-title').inner_text();assert page.locator('#tutorial-content>section').first.is_visible()
   page.evaluate('location.hash="#tutorials"');page.wait_for_selector('.tutorial-card');consistent();assert page.locator('.tutorial-card').count()==76
   checks.append('old/new lesson text and section navigation render while MathJax is still pending')
  released=True
  for r in held_math:r.fulfill(status=200,content_type='text/javascript',body=(R/'vendor/mathjax/tex-svg.js').read_bytes())
  if not a.expect_mismatch:
   page.wait_for_function('Boolean(window.MathJax?.typesetPromise)')
   for id in ['complexity','cpp-windows-vscode']:
    page.evaluate('(id)=>location.hash="#tutorial/"+id',id);page.wait_for_selector('#tutorial-content section');page.wait_for_function('document.querySelector("#tutorial-content").getAttribute("aria-busy")==="false"');assert page.locator('#tutorial-content mjx-merror').count()==0
   page.evaluate('location.hash="#tutorials"');page.wait_for_selector('.tutorial-card');consistent();assert page.locator('.tutorial-card').count()==76
   for width in [375,1280]:
    page.set_viewport_size({'width':width,'height':900});consistent();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   assert page.locator('script[src*="vendor/mathjax/tex-svg.js"]').count()==1;page.reload(wait_until='domcontentloaded');page.wait_for_function('document.querySelectorAll(".tutorial-card").length===76');consistent();assert not errors,errors;checks.append('math release, old/new lesson navigation, mobile/desktop and singleton loader remain correct')
  b.close()
finally:s.shutdown()
result={'status':'passed','checks':checks,'limits':'Actual SDK/current public response bytes; synthetic guest progress exercises native progress rendering. No live authenticated session or TLS bypass.'};(W/('math-race-baseline.json'if a.expect_mismatch else'math-race-fixed.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
