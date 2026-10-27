"""Native MN/EN problem statement viewer/admin; synthetic RPC/Auth, actual MathJax/editor."""
import functools,http.server,json,threading,re
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
entries=[p for p in json.loads((ROOT/'audit/PART04-REVIEWED-NEW-TASKS.json').read_text())if p.get('statement')];pool=[];docs={}
for i,p in enumerate(entries,1):
 pid='statement-'+str(i);docs[pid]={'body':p['statement'],'provenance':p['statementProvenance'],'problemRevision':1,'revision':1};meta={**p,'id':pid,'number':i,'revision':1,'priorityLevel':'low'if i==1 else'high','priority':i!=1,'tags':['secret-tag'],'hasStatement':True,'hasEditorial':False};meta.pop('statement');meta.pop('statementProvenance');meta.pop('editorial',None);pool.append(meta)
checks=[]
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(viewport={'width':1200,'height':950});page.set_default_timeout(20000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.add_init_script('window.pool='+json.dumps(pool)+';window.docs='+json.dumps(docs)+''';window.calls=[];window.statementMode='normal';window.role=false;window.testClient={auth:{onAuthStateChange:cb=>window.authCallback=cb,getSession:async()=>({data:{session:null}})},from:name=>({select:()=>({eq:()=>name==='profiles'?{maybeSingle:async()=>({data:null})}:Promise.resolve({data:[]})}),upsert:async()=>({data:[]})}),rpc:async(name,args)=>{calls.push({name,args});if(name==='get_catalog')return{data:{problems:pool,knownIds:pool.map(p=>p.id)}};if(name==='is_admin')return{data:role};if(name==='get_admin_catalog')return{data:pool};if(name==='get_problem_statement'){if(statementMode==='defer')return await new Promise(resolve=>window.resolveStatement=resolve);if(statementMode==='error')return{error:{message:'private backend error'}};return{data:docs[args.p_problem_id]||null};}if(name==='admin_save_problem'){const index=pool.findIndex(p=>p.number===args.p_number),body=args.p_body;docs[pool[index].id]={body:body.statement,provenance:body.statementProvenance,revision:2,problemRevision:2};pool[index]={...pool[index],title:body.title,revision:2};window.lastSave=body;return{data:{...pool[index],...body,revision:2}};}if(name==='get_problem_editorial')return{data:null};return{data:[]};}};''')
  def route(r):
   url=r.request.url
   if 'cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm'in url:r.fulfill(status=200,content_type='text/javascript',body='export function createClient(){return window.testClient;}')
   elif not url.startswith(base):r.abort()
   elif '/config.js'in url:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={supabaseUrl:"https://fixture.invalid",supabaseKey:"public-test-fixture",problemBackendVersion:34};')
   else:r.continue_()
  page.route('**/*',route);page.goto(base+'/index.html#library',wait_until='networkidle');page.wait_for_function("document.querySelector('#problems .open:not(:disabled)')");assert page.evaluate("calls.filter(c=>c.name==='get_problem_statement').length")==0
  for i,entry in enumerate(entries,1):
   page.goto(base+'/index.html#problem/statement-'+str(i),wait_until='networkidle');page.wait_for_selector('#problem-statement article section');root=page.locator('#problem-statement');assert root.is_visible();assert page.locator('#hint-list .hint').count()==0;assert page.evaluate("calls.filter(c=>c.name==='get_problem_editorial').length")==0
   assert root.locator('a[target=_blank]').first.get_attribute('rel')=='noopener noreferrer';assert 'secret-tag'not in page.locator('#detail').inner_text()
   for width,theme in[(375,'light'),(1200,'dark')]:
    page.set_viewport_size({'width':width,'height':950});page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
    for lang in['mn','en']:
     root.locator('select').select_option(lang);page.wait_for_function("document.querySelectorAll('#problem-statement mjx-container').length>0");assert root.locator('mjx-merror,[data-mjx-error]').count()==0
     expected=entry['statement']if lang=='mn'else entry['statement']['translations']['en'];expected_codes=[b['text']for s in expected['sections']for b in s['blocks']if b['type']=='code'];actual=root.locator('pre code').all_text_contents();assert actual==expected_codes,(entry['ref'],lang,actual,expected_codes)
     assert root.evaluate('e=>e.scrollWidth<=e.clientWidth'),(entry['ref'],lang,width,theme,root.evaluate('e=>({width:e.clientWidth,scroll:e.scrollWidth,overflow:[...e.querySelectorAll("*")].filter(x=>x.getBoundingClientRect().right>e.getBoundingClientRect().right).map(x=>({tag:x.tagName,text:x.textContent.slice(0,160),width:x.getBoundingClientRect().width}))})'))
     assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(entry['ref'],lang,width,theme,'page overflow')
     if entry['ref']=='typical90_bz' and width==375:
      # A real bank constraint is wider than the mobile column. Preserve the
      # full formula and allow local scrolling rather than clipping/shrinking it.
      wide=root.locator('mjx-container').filter(has_text='min').first
      assert wide.evaluate('e=>e.scrollWidth>e.clientWidth'),(lang,'wide fixture lost')
      assert wide.evaluate('e=>getComputedStyle(e).overflowX')=='auto'
      assert wide.evaluate('e=>{e.scrollLeft=e.scrollWidth;const moved=e.scrollLeft>0;e.scrollLeft=0;return moved;}')
   if i==1:assert page.locator('#problem-hints-button').is_hidden()
  checks.append(f'{len(entries)} actual native documents:{len(entries)*4}language/theme/width combinations; exact literal input/sample code, MathJax, attribution; Low statement visible without hints; hidden tags and spoiler actions unaffected')
  page.goto(base+'/index.html#library',wait_until='networkidle');page.evaluate("statementMode='defer'");page.get_by_role('button',name=entries[0]['title'],exact=False).first.click();page.wait_for_function("typeof resolveStatement==='function'");page.locator('#problem-back').click();page.evaluate("statementMode='normal'");page.get_by_role('button',name=entries[1]['title'],exact=False).first.click();page.wait_for_selector('#problem-statement article section');before=page.locator('#problem-statement article').inner_text();page.evaluate("resolveStatement({data:docs['statement-1']})");page.wait_for_timeout(100);assert page.locator('#problem-statement article').inner_text()==before
  page.goto(base+'/index.html#library',wait_until='networkidle');page.evaluate("statementMode='error'");page.get_by_role('button',name=entries[0]['title'],exact=False).first.click();page.wait_for_function("document.querySelector('#problem-statement').textContent.includes('ачаалсангүй')");assert 'private backend error'not in page.locator('#problem-statement').inner_text();page.evaluate("statementMode='normal'");root=page.locator('#problem-statement');root.locator('summary').click();root.locator('summary').click();page.wait_for_selector('#problem-statement article section')
  checks.append('no library body fetch; stale response cannot overwrite another problem; safe error and explicit retry; no editorial body fetched by statement reading')
  page.evaluate("role=true;authCallback('SIGNED_IN',{user:{id:'00000000-0000-0000-0000-000000000001',email:'fixture@example.invalid'}})");page.wait_for_function("!document.querySelector('#admin-nav').hidden");page.evaluate("location.hash='#admin-section'");page.wait_for_selector('#admin-section',state='visible');page.wait_for_function("document.querySelector('#admin-choose option[value=\"1\"]')");page.get_by_role('button',name='Засах бодлого сонгох…',exact=True).click();picker=page.get_by_role('dialog',name='Бодлого сонгох');picker.get_by_role('checkbox',name=re.compile(re.escape(entries[0]['title']))).check();picker.locator('[data-selection-apply]').click();admin=page.locator('#admin-statement-document');admin.locator('summary').first.click();page.wait_for_function("document.querySelector('#admin-statement-document input[maxlength]').value.length>0")
  title=admin.get_by_label('Statement гарчиг',exact=True);title.fill('Reviewed statement title');review=admin.locator('input[type=checkbox]');assert not review.is_checked();review.check();page.locator('#admin-save').click();page.wait_for_function("typeof lastSave==='object'");assert page.evaluate('lastSave.statement.title')=='Reviewed statement title';assert page.evaluate('lastSave.statement.translations.en.title')==entries[0]['statement']['translations']['en']['title'];assert page.evaluate('lastSave.statementProvenance.checks.translation')is True
  page.evaluate("role=false;authCallback('SIGNED_OUT',null)");page.wait_for_timeout(120);assert admin.locator('input[maxlength="200"]').is_hidden();assert page.locator('#admin-nav').is_hidden();assert page.locator('#admin-section').is_hidden()
  checks.append('actual admin native block editor loads lazily with revision; content edit clears review attestation, re-review and atomic payload preserve EN/samples; logout clears private editor and hides admin')
  assert not errors,errors;browser.close()
finally:server.shutdown()
report={'status':'passed','statement_documents':len(entries),'checks':checks,'limits':'Synthetic RPC/Auth only; actual tutorial block editor/renderer and bundled MathJax; no production writes or new permission application.'}
(ROOT/'audit/PART04-STATEMENT-BROWSER.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
