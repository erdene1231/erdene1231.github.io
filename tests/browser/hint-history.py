"""No persistent hint usage; synthetic Auth/progress only, bundled real frontend."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}'
p=json.loads((ROOT/'problems.json').read_text())['problems'][0]
pool=[{**p,'id':'history-high','number':1,'title':'History High','priorityLevel':'high','hints':['First $n$.','Second','Third'],'hintsEn':['First $n$.','Second','Third']},{**p,'id':'history-low','number':2,'title':'History Low','priorityLevel':'low'}]
legacy=json.dumps({'progress':{'history-high':{'status':'solved','notes':'Guest note','hints':3}},'dirty':[]})
checks=[]
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(viewport={'width':1200,'height':950});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.add_init_script('window.pool='+json.dumps(pool)+';window.legacy='+json.dumps(legacy)+''';if(!localStorage.getItem('think-cp:v1:guest'))localStorage.setItem('think-cp:v1:guest',legacy);window.writes=[];const originalSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){writes.push({k,v});return originalSet.call(this,k,v)};window.calls=[];window.remote={problem_id:'history-high',status:'trying',notes:'Remote note',hints:3};window.testClient={auth:{onAuthStateChange:cb=>window.authCallback=cb,getSession:async()=>({data:{session:null}})},from:name=>({select:columns=>({eq:()=>{calls.push({kind:'select',name,columns});return name==='profiles'?{maybeSingle:async()=>({data:null})}:Promise.resolve({data:name==='progress'?[remote]:[]})}}),upsert:async(rows,options)=>{calls.push({kind:'upsert',name,rows,options});for(const row of rows)if(name==='progress')Object.assign(remote,row);return{data:[]}}}),rpc:async(name,args)=>{calls.push({kind:'rpc',name,args});if(name==='get_catalog')return{data:{problems:pool,knownIds:pool.map(p=>p.id)}};return{data:name==='is_admin'?false:[]}}};''')
  def route(r):
   if 'cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm'in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='export function createClient(){return window.testClient;}')
   elif not r.request.url.startswith(base):r.abort()
   elif '/config.js'in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={supabaseUrl:"https://fixture.invalid",supabaseKey:"public-test-fixture"};')
   elif '/problems.json'in r.request.url:r.fulfill(status=200,content_type='application/json',body=json.dumps({'problems':pool}))
   else:r.continue_()
  page.route('**/*',route);page.goto(base+'/index.html#library',wait_until='networkidle');page.wait_for_function("document.querySelector('#problems .open')&&!document.querySelector('#problems .open').disabled")
  assert page.locator('option[value=hinted]').count()==0
  page.get_by_role('button',name='History High',exact=False).first.click();assert page.locator('#problem-status').input_value()=='solved';assert page.locator('#notes').input_value()=='Guest note'
  page.locator('#problem-hints-button').click();assert page.locator('#hint-list .hint').count()==0
  page.evaluate('writes=[];calls=[]');snapshot=page.evaluate('JSON.stringify({...localStorage})')
  for i in range(3):page.locator('#next-hint').click();assert page.locator('#hint-list .hint').count()==i+1
  page.locator('#hint-language').select_option('en');page.locator('#toggle-hints').click();page.locator('#toggle-hints').click();assert page.locator('#hint-list .hint').count()==3
  assert page.evaluate('writes.length')==0;assert page.evaluate("calls.filter(c=>c.kind==='upsert').length")==0;assert page.evaluate('JSON.stringify({...localStorage})')==snapshot
  assert page.locator('.hint-meter').count()==0;assert not page.locator('#detail').get_by_text('Hint 3/3',exact=True).count();assert page.locator('#problem-status').input_value()=='solved'
  checks.append('legacy hint history ignored; guest status/notes preserved; staged MN/EN reveal/hide has zero Storage writes and zero upserts')
  page.locator('#problem-back').click();page.get_by_role('button',name='History High',exact=False).first.click();page.locator('#problem-hints-button').click();assert page.locator('#hint-list .hint').count()==0
  page.locator('#next-hint').click();page.reload(wait_until='networkidle');page.wait_for_selector('#problem-hints-button');page.locator('#problem-hints-button').click();assert page.locator('#hint-list .hint').count()==0
  checks.append('navigation and reload start with no revealed hints; no persisted language/usage preference')
  page.evaluate("authCallback('SIGNED_IN',{user:{id:'00000000-0000-0000-0000-000000000002',email:'test@example.invalid'}})");page.wait_for_function("document.querySelector('#problem-status').value==='trying'&&!document.querySelector('#problem-status').disabled");assert page.locator('#notes').input_value()=='Remote note'
  assert page.evaluate("calls.filter(c=>c.kind==='select'&&c.name==='progress').every(c=>c.columns==='problem_id,status,notes')")
  page.locator('#problem-hints-button').click();assert page.locator('#hint-list .hint').count()==0;page.evaluate('writes=[];calls=[]');page.locator('#next-hint').click();assert page.locator('#problem-status').input_value()=='trying';assert page.evaluate('writes.length')==0;assert page.evaluate("calls.filter(c=>c.kind==='upsert').length")==0
  page.locator('#notes').fill('Updated note');page.locator('#save-note').click();page.wait_for_function("calls.some(c=>c.kind==='upsert'&&c.name==='progress')")
  assert page.evaluate("calls.filter(c=>c.kind==='upsert'&&c.name==='progress').every(c=>c.options.defaultToNull===false&&c.rows.every(r=>!Object.hasOwn(r,'hints')))")
  assert page.evaluate('remote.hints')==3;assert page.evaluate('remote.notes')=='Updated note';assert page.evaluate("localStorage.getItem('think-cp:v1:guest')") == legacy
  modern=page.evaluate("JSON.parse(localStorage.getItem('think-cp:v2:00000000-0000-0000-0000-000000000002'))")
  assert modern['progress']['history-high']=={'status':'trying','notes':'Updated note'}
  checks.append('account switch resets reveal; remote SELECT omits history; explicit notes save whitelists status/notes without hints, preserving stored historical value and legacy blob')
  page.locator('#problem-back').click()
  with page.expect_download()as download:page.locator('#export').click()
  exported=json.loads(Path(download.value.path()).read_text());assert exported['version']==2;assert exported['progress']['history-high']=={'status':'trying','notes':'Updated note'}
  page.on('dialog',lambda d:d.accept());page.locator('#import').set_input_files({'name':'legacy-progress.json','mimeType':'application/json','buffer':json.dumps({'version':1,'progress':{'history-high':{'status':'solved','notes':'Imported note','hints':2}}}).encode()})
  page.wait_for_function("remote.status==='solved'&&remote.notes==='Imported note'");assert page.evaluate('remote.hints')==3
  assert page.evaluate("localStorage.getItem('think-cp:v1:guest')")==legacy
  checks.append('actual v2 backup export excludes history; legacy v1 import restores status/notes only and preserves old backend/local history')
  page.get_by_role('button',name='History Low',exact=False).first.click();assert page.locator('#problem-hints-button').is_hidden();assert page.locator('#hint-list .hint').count()==0
  assert not errors,errors;browser.close()
finally:s.shutdown()
report={'status':'passed','checks':checks,'limits':'Synthetic Auth/progress only; no production reads/writes or history deletion. Column-limited SQL preservation tested independently.'}
(ROOT/'audit/PART04-HINT-HISTORY.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
