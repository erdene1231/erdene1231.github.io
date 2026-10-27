"""Controlled dependency gates compare pre-fix/current startup, no external services."""
import functools,http.server,json,threading,subprocess,time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
old=subprocess.check_output(['git','show','a53ccf0:app.js'],cwd=ROOT,text=True);pool=json.loads((ROOT/'problems.json').read_text())['problems'][:125];results=[]
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for version in['before','after']:
   page=browser.new_page(viewport={'width':1200,'height':950});held=[];seed=[];errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.add_init_script('window.assetStartCatalogCalls=[];const originalFetch=window.fetch;window.fetch=function(url,...args){if(["curriculum.json","study-plan.json","tutorial-editions.json","learning-problems.json","tutorials.json"].some(name=>String(url).includes(name)))assetStartCatalogCalls.push(window.catalogCalls);return originalFetch.call(this,url,...args)};window.catalogCalls=0;window.testClient={auth:{onAuthStateChange:()=>{},getSession:async()=>({data:{session:null}})},rpc:async(name)=>{if(name==="get_catalog"){catalogCalls++;return{data:'+json.dumps({'problems':pool,'knownIds':[p['id']for p in pool]})+'}}return{data:name==="is_admin"?false:[]}}};')
   def route(r):
    url=r.request.url
    if 'cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm'in url:r.fulfill(status=200,content_type='text/javascript',body='export function createClient(){return window.testClient;}')
    elif not url.startswith(base):r.abort()
    elif '/config.js'in url:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={supabaseUrl:"https://fixture.invalid",supabaseKey:"public-test-fixture"};')
    elif '/app.js?'in url and version=='before':r.fulfill(status=200,content_type='text/javascript',body=old)
    elif any('/'+f+'?'in url for f in['curriculum.json','study-plan.json','tutorial-editions.json','learning-problems.json']):held.append(r)
    elif '/problems.json?'in url:seed.append(url);r.fulfill(status=200,content_type='application/json',body=json.dumps({'problems':pool}))
    else:r.continue_()
   page.route('**/*',route);page.goto(base+'/index.html#library',wait_until='domcontentloaded');page.wait_for_function('document.querySelector("#problems")!==null');page.wait_for_timeout(700)
   called=page.evaluate('catalogCalls');usable=page.locator('#problems .open:not(:disabled)').count()
   if version=='before':assert called==0 and usable==0 and len(seed)==1 and held
   else:assert called==1 and usable==100 and not seed and held;assert page.locator('#problem-next').is_enabled()
   results.append({'version':version,'learning_requests_deliberately_unresolved':len(held),'catalog_calls_before_release':called,'usable_rows_before_release':usable,'seed_requests':len(seed),'study_asset_start_catalog_call_counts':page.evaluate('assetStartCatalogCalls')})
   recorded=None
   if version=='after':
    assert all(n>=1 for n in page.evaluate('assetStartCatalogCalls'));page.get_by_role('button',name=pool[0]['title'],exact=False).first.click();page.locator('#problem-status').select_option('solved');recorded=page.evaluate("JSON.parse(localStorage.getItem('erdene:learning:v1:guest')).dates")[pool[0]['id']]['first_solved_at'];assert recorded;page.locator('#problem-status').select_option('new');page.locator('#problem-back').click()
   for r in held:
    name=r.request.url.split('/')[-1].split('?')[0];r.fulfill(status=200,content_type='application/json',body=(ROOT/name).read_text())
   page.wait_for_function('document.querySelectorAll("#problems .open:not(:disabled)").length===100');page.get_by_role('button',name=pool[0]['title'],exact=False).first.click();page.wait_for_function('location.hash.startsWith("#problem/")');assert page.locator('#detail-tags').inner_text()==''
   if recorded:assert page.evaluate("JSON.parse(localStorage.getItem('erdene:learning:v1:guest')).dates")[pool[0]['id']]['first_solved_at']==recorded
   assert not errors,errors;page.close()
  browser.close()
finally:server.shutdown()
report={'status':'passed','kind':'Controlled local browser comparison, not live user timing','cases':results,'preserved':'authoritative catalog waits for RPC, no online seed resurrection, hidden unsolved tags, study bodies defer until catalog; explicit early progress dates survive independent learning initialization'}
(ROOT/'audit/PART04-CATALOG-STARTUP.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
