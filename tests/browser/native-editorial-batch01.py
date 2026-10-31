"""Real app entry, native bilingual renderer/editor and bundled MathJax; synthetic read transport."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
entries=json.loads((ROOT/'audit/native-problem-editorials/batch01.json').read_text());before=json.loads((ROOT/'audit/atcoder-io-format/before-targets.json').read_text());patches=json.loads((ROOT/'audit/atcoder-io-format/patches.json').read_text());records={}
for e in entries:
 p=next(x for x in before if x['body']['id']==e['id']);records[e['id']]={**p['body'],'statement':next(x['after_statement']for x in patches if x['id']==e['id']),'editorial':e['editorial'],'revision':4,'hasStatement':True,'hasEditorial':True}
checks=[];errors=[];cases=0
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(viewport={'width':1200,'height':950});page.on('pageerror',lambda e:errors.append(str(e)))
  page.add_init_script('window.records='+json.dumps(records)+''';window.reads=[];window.testClient={auth:{getSession:async()=>({data:{session:null}}),onAuthStateChange:()=>{}},from:name=>({select:()=>({eq:(field,id)=>({maybeSingle:async()=>{if(name!=='problem_catalog')return{data:null};reads.push(id);return{data:{body:records[id],revision:4}};}})})}),rpc:async(name)=>{if(name==='get_catalog'){const problems=Object.values(records).map(p=>{let q={...p};delete q.statement;delete q.statementProvenance;delete q.editorial;return q;});return{data:{problems,knownIds:problems.map(p=>p.id)}};}return{data:name==='is_admin'?false:[]};}};''')
  def route(r):
   u=r.request.url
   if 'cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm'in u:r.fulfill(status=200,content_type='text/javascript',body='export function createClient(){return window.testClient;}')
   elif not u.startswith(base):r.abort()
   elif '/config.js'in u:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={supabaseUrl:"https://fixture.invalid",supabaseKey:"public-test-fixture",problemBackendVersion:32,problemStatementStorage:"catalog-inline-v1",problemEditorialStorage:"catalog-inline-v1"};')
   else:r.continue_()
  page.route('**/*',route);page.goto(base+'/index.html#library',wait_until='networkidle');page.wait_for_selector('#problems .open');assert page.evaluate('reads.length')==0
  for e in entries:
   page.goto(base+'/index.html#problem/'+e['id'],wait_until='networkidle');page.wait_for_selector('#problem-statement article section');root=page.locator('#problem-editorial');assert root.is_visible();root.locator('summary').click();page.wait_for_selector('#problem-editorial article section')
   for width,theme in [(375,'light'),(1200,'dark')]:
    page.set_viewport_size({'width':width,'height':950});page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
    for lang in ['mn','en']:
     root.locator('select').select_option(lang);page.wait_for_function("document.querySelector('#problem-editorial article').lang==='"+lang+"'&&document.querySelectorAll('#problem-editorial mjx-container').length>0")
     expected=e['editorial']if lang=='mn'else e['editorial']['translations']['en'];codes=[b['text']for s in expected['sections']for b in s['blocks']if b['type']=='code'];assert root.locator('pre code').all_text_contents()==codes
     assert root.locator('mjx-merror,[data-mjx-error]').count()==0;assert root.evaluate('e=>e.scrollWidth<=e.clientWidth');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');cases+=1
  checks.append(f'{cases} actual public problem entry/editorial reader cases: source priority preserved, MN/EN, mobile/light + desktop/dark, MathJax, exact fragments and final full program')
  roundtrips=page.evaluate('''async()=>{const{setupProblemEditorialEditor}=await import('./problem-editorial.js?v=86');const host=document.createElement('div');document.body.append(host);let count=0;for(const p of Object.values(records)){const ui=setupProblemEditorialEditor(host,{locked:()=>false,user:()=>({id:'isolated'}),client:()=>testClient,problems:()=>Object.values(records),progress:()=>({})});await ui.edit({...p,editorial:undefined});const initial=JSON.stringify(ui.collect());if(initial!==JSON.stringify(p.editorial))throw Error('native initial mismatch');host.querySelector('select').value='en';host.querySelector('select').dispatchEvent(new Event('change'));host.querySelector('select').value='mn';host.querySelector('select').dispatchEvent(new Event('change'));if(JSON.stringify(ui.collect())!==initial)throw Error('language roundtrip');const serialized=structuredClone(ui.collect());records[p.id].editorial=serialized;ui.markSaved();await ui.edit({...p,editorial:undefined});if(JSON.stringify(ui.collect())!==JSON.stringify(serialized))throw Error('save reload');ui.invalidate();host.replaceChildren();count++;}host.remove();return count;}''');assert roundtrips==3
  checks.append('3 actual native block-editor language/serialize/save/lazy-reload roundtrips; exact document preservation')
  assert not errors,errors;browser.close()
finally:server.shutdown()
report={'status':'passed','reader_cases':cases,'native_editor_roundtrips':3,'checks':checks,'limitations':'Actual public app/components with synthetic anonymous read transport; live public readback follows guarded publication. Not an authenticated live-user browser claim.'};(ROOT/'audit/native-problem-editorials/batch01-native-browser.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
