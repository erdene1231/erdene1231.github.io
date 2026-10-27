"""Final prepared bank in actual browser; synthetic IDs/RPC, no production calls."""
import functools,http.server,json,subprocess,threading,time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
# Real metadata is normalized through the actual import model; IDs are fixtures only.
script="""import fs from'node:fs';import{validateProblem}from'./problem-store.js';const b=JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).problems.map(r=>({...r.body,number:r.number}));const next=Math.max(...b.map(r=>r.number))+1;const added=JSON.parse(fs.readFileSync('audit/PART04-REVIEWED-NEW-TASKS.json')).map((r,i)=>({...validateProblem(r),id:'fixture-p4-'+i,number:next+i,revision:1}));const rows=[...b,...added].map(r=>{const{editorial,statement,statementProvenance,...lean}=r;return{...lean,hasEditorial:!!editorial,hasStatement:!!statement}});process.stdout.write(JSON.stringify(rows));"""
pool=json.loads(subprocess.check_output(['node','--input-type=module','-e',script],cwd=ROOT,text=True));assert len(pool)==993
for i in range(7):pool.append({**pool[0],'id':f'fixture-extra-{i}','number':10000+i,'ref':f'fixture-extra-{i}','title':f'Extra synthetic row {i}'})
payload=json.dumps({'problems':pool,'knownIds':[p['id']for p in pool]},ensure_ascii=False)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}';checks=[]
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for width in [375,1440]:
   for theme in ['light','dark']:
    page=browser.new_page(viewport={'width':width,'height':950});page.set_default_timeout(15000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.add_init_script('window.catalogCalls=0;window.richCalls=0;localStorage.setItem("theme","'+theme+'");window.fixtureCatalog='+payload+''';window.testClient={auth:{onAuthStateChange:()=>{},getSession:async()=>({data:{session:null}})},rpc:async name=>{if(name==='get_catalog'){catalogCalls++;return{data:fixtureCatalog}};if(name==='get_problem_editorial'||name==='get_problem_statement')richCalls++;return{data:name==='is_admin'?false:[]}}};''')
    def route(r):
     url=r.request.url
     if'cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm'in url:r.fulfill(status=200,content_type='text/javascript',body='export function createClient(){return window.testClient;}')
     elif not url.startswith(base):r.abort()
     elif'/config.js'in url:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={supabaseUrl:"https://fixture.invalid",supabaseKey:"public-test-fixture"};')
     elif'/problems.json'in url:raise AssertionError('Configured catalog must not request seed')
     else:r.continue_()
    page.route('**/*',route);start=time.perf_counter();page.goto(base+'/index.html#library',wait_until='domcontentloaded');page.wait_for_function('document.querySelectorAll("#problems .open:not(:disabled)").length===100');first=round((time.perf_counter()-start)*1000,2)
    if page.evaluate('document.documentElement.dataset.theme')!=theme:page.locator('#theme-toggle').click()
    assert page.locator('#results-count').inner_text()=='1000 / 1000 бодлого';assert page.evaluate('catalogCalls')==1;assert page.evaluate('richCalls')==0
    timings={}
    for mode in ['comfortable','compact','minimalist']:
     start=time.perf_counter();page.locator('#problem-density').select_option(mode);timings[mode]=round((time.perf_counter()-start)*1000,2);assert page.locator('#problems .problem').count()==100;assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert page.locator('.hint-meter').count()==0
    if not page.locator('#catalog-filter-panel').evaluate('e=>e.open'):page.locator('#catalog-filter-panel > summary').click()
    page.locator('#source').select_option('Codeforces');assert page.locator('#results-count').inner_text().startswith('378 / 1000');page.locator('#reset-filters').click()
    page.locator('#sort').select_option('number-asc')
    for i in range(9):page.locator('#problem-next').click()
    assert page.locator('#problems .problem').count()==100;assert page.locator('#problem-next').is_disabled();assert page.locator('#problem-prev').is_enabled()
    page.locator('#search').fill('no-matching-final-fixture');assert page.locator('#problems .problem').count()==0;page.locator('#reset-filters').click();assert page.locator('#problems .problem').count()==100
    assert page.evaluate('richCalls')==0;assert not errors,errors
    checks.append({'width':width,'theme':theme,'first_usable_100_rows_ms':first,'mode_switch_ms':timings,'catalog_calls':1,'rich_body_calls':0,'page_size':100,'last_page':100,'filters_pagination_empty_reset':'passed'});page.close()
  browser.close()
finally:server.shutdown()
report={'status':'passed','environment':'Local Chromium with synthetic anonymous RPC/Auth;not live network/production timing','fixture':{'retained_metadata_rows':748,'prepared_metadata_rows':245,'additional_synthetic_rows':7,'total':1000,'new_ids':'fixture-only,not server allocation'},'catalog_json_bytes':len(payload.encode()),'rich_bodies_in_catalog':False,'checks':checks}
(ROOT/'audit/PART04-FINAL-BANK-BROWSER.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
