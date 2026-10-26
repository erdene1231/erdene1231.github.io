"""Conflict recovery UX in real Chromium; synthetic documents and mocked RPC/Auth only."""
import functools
import http.server
import json
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}'
report, failures = {}, []
try:
 with sync_playwright() as p:
  browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
  def fresh():
   page = browser.new_page(viewport={'width':1200,'height':950}, accept_downloads=True)
   page_errors = []
   page.on('pageerror', lambda e: page_errors.append(str(e)))
   def route(r):
    if not r.request.url.startswith(base): r.abort(); return
    if '/app.js?' in r.request.url or '/navigation.js?' in r.request.url:
     r.fulfill(status=200, content_type='text/javascript', body=''); return
    r.continue_()
   page.route('**/*', route)
   page.goto(base+'/index.html', wait_until='networkidle')
   page.evaluate('''async()=>{
    window.MathJax={startup:{promise:Promise.resolve()},typesetPromise:async()=>{},typesetClear:()=>{}};
    const {setupTutorialEditor}=await import('/tutorial-editor.js?v=32');
    window.actor='00000000-0000-0000-0000-000000000001';window.rebaseCalls=[];window.saveCalls=[];
    window.rejectRebase=false;window.delayRebase=false;window.publishCalls=[];
    const original=structuredClone((await (await fetch('/tutorials.json')).json()).tutorials[0]);
    window.makeBody=(title,text)=>({...structuredClone(original),id:'complexity',title,translations:undefined,
     sections:[{title:'Recovery fixture',blocks:[{type:'rich',content:[{text,marks:[]}]}]}]});
    window.publishedBody=makeBody('Published title','Published paragraph');
    window.onlineBody=makeBody('Online draft title','Online draft paragraph');
    window.localBody=makeBody('Local edit title','Local paragraph to preserve');
    window.onlineDraft={body:onlineBody,revision:2,base_revision:5};
    window.cacheKey='erdene:tutorial-draft:v3:'+actor+':complexity';
    localStorage.setItem(cacheKey,JSON.stringify({actor,id:'complexity',body:localBody,baseRevision:4,draftRevision:1,unsynced:true}));
    window.client={rpc:async(name,args)=>{
     if(name==='is_admin')return {data:true};
     if(name==='admin_tutorial_workspace')return {data:{catalog:[{id:'complexity',title:publishedBody.title,revision:5}],drafts:[{tutorial_id:'complexity',title:onlineBody.title,revision:2,base_revision:5}]}};
     if(name==='admin_tutorial_document')return {data:{current:{body:publishedBody,revision:5,published:true},draft:onlineDraft}};
     if(name==='admin_rebase_tutorial_draft'){
      rebaseCalls.push(structuredClone(args));
      const result=()=>{if(rejectRebase)return {error:Error('REVISION_CONFLICT: newer draft')};
       if(args.p_current_revision!==5||args.p_draft_revision!==2||args.p_actor!=='00000000-0000-0000-0000-000000000001')throw Error('Wrong rebase/CAS actor');
       onlineDraft={body:structuredClone(args.p_body),revision:3,base_revision:5};return {data:onlineDraft};};
      if(delayRebase)return new Promise(resolve=>window.finishRebase=()=>resolve(result()));return result();
     }
     if(name==='admin_save_tutorial_draft'){saveCalls.push(structuredClone(args));return {data:{body:args.p_body,base_revision:5,revision:args.p_draft_revision+1}};}
     if(name==='admin_publish_tutorial_draft'){publishCalls.push(args);throw Error('Recovery must never publish');}
     throw Error('Unexpected RPC '+name);
    }};
    window.editor=setupTutorialEditor({client:()=>client,user:()=>actor?{id:actor}:null,topics:()=>[publishedBody],learning:()=>null,ready:()=>true,saved:()=>{}});
    await editor.accountChanged();document.querySelector('#admin-tutorials').hidden=false;
   }''')
   page.wait_for_selector('[data-rebase-choice="local"]', state='attached')
   return page, page_errors
  def case(name, fn):
   page, errors = fresh()
   try:
    fn(page)
    assert not errors, errors
    report[name] = 'PASS'
   except Exception as e:
    report[name] = 'FAIL'; failures.append(name+': '+str(e))
   finally: page.close()
  def initial(page):
   assert page.locator('#tutorial-admin-form').is_hidden(), 'empty disabled editor should be hidden'
   for key,title in [('local','Local edit title'),('draft','Online draft title'),('published','Published title')]:
    assert page.locator('[data-rebase-choice="'+key+'"]').is_visible(), key+' choice hidden in collapsed details'
    assert title in page.locator('[data-version="'+key+'"]').inner_text()
   assert page.locator('[data-recovery-backup]:visible').is_visible()
   assert page.locator('[data-rebase-save]').is_disabled()
   assert page.evaluate('rebaseCalls.length===0&&saveCalls.length===0&&publishCalls.length===0')
   for width in [375,1200]:
    page.set_viewport_size({'width':width,'height':950})
    assert page.locator('#admin-tutorials').evaluate('e=>e.scrollWidth<=e.clientWidth'), 'recovery overflows viewport'
    page.locator('#admin-tutorials').screenshot(path=str(ROOT/f'audit/browser/recovery-ux-{width}.png'))
  case('conflict_hides_empty_form_and_shows_immediate_choices', initial)
  def choose(page, key, title, paragraph):
   page.locator('[data-rebase-choice="'+key+'"]').click()
   assert page.evaluate('rebaseCalls.length') == 0, 'selection alone wrote the draft'
   assert page.locator('[data-rebase-save]').is_enabled()
   page.locator('[data-rebase-save]').click()
   page.wait_for_function("!document.querySelector('#tutorial-admin-form').hidden&&!document.querySelector('#tutorial-admin-title').disabled")
   assert page.locator('#tutorial-admin-title').input_value() == title
   assert page.locator('#tutorial-admin-sections .block-rich-input').first.inner_text() == paragraph
   assert page.locator('#tutorial-draft-comparison').is_hidden()
   args = page.evaluate('rebaseCalls[0]')
   assert args['p_current_revision'] == 5 and args['p_draft_revision'] == 2
   assert page.evaluate('JSON.parse(localStorage.getItem(cacheKey+":before-rebase")).body.title') == 'Local edit title'
   assert page.evaluate('JSON.parse(localStorage.getItem(cacheKey)).draftRevision') == 3
   assert page.evaluate('JSON.parse(localStorage.getItem(cacheKey)).baseRevision') == 5
   assert page.evaluate('publishCalls.length') == 0
   page.locator('#tutorial-admin-title').fill(title+' continued')
   page.locator('#tutorial-admin-save').click()
   page.wait_for_function('saveCalls.length===1')
   assert page.evaluate('saveCalls[0].p_draft_revision')==3
   assert page.evaluate('saveCalls[0].p_base_revision')==5
   assert page.evaluate('saveCalls[0].p_body.title')==title+' continued'
  case('online_draft_choice_rebases_and_reopens_actual_editor', lambda page: choose(page,'draft','Online draft title','Online draft paragraph'))
  case('local_choice_rebases_and_preserves_local_content', lambda page: choose(page,'local','Local edit title','Local paragraph to preserve'))
  case('published_choice_preserves_local_backup_before_reopening', lambda page: choose(page,'published','Published title','Published paragraph'))
  def backup(page):
   with page.expect_download() as result: page.locator('[data-recovery-backup]:visible').click()
   download=result.value
   path=download.path()
   body=json.loads(Path(path).read_text())
   # Backup can be a full recovery snapshot or its document; both must retain content.
   assert (body.get('body') or body)['title'] == 'Local edit title'
   assert page.evaluate('rebaseCalls.length===0&&saveCalls.length===0')
  case('backup_is_available_without_unlocking_the_form', backup)
  def postpone(page):
   page.locator('[data-recovery-cancel]').click()
   assert page.locator('#tutorial-admin-form').is_hidden()
   assert page.locator('[data-recovery-resume]').is_visible()
   assert page.locator('#tutorial-admin-new').is_enabled()
   assert page.locator('#tutorial-admin-choose').is_enabled()
   assert page.evaluate('JSON.parse(localStorage.getItem(cacheKey)).body.title') == 'Local edit title'
   page.locator('[data-recovery-resume]').click()
   page.wait_for_selector('[data-rebase-choice="draft"]', state='visible')
   assert page.evaluate('rebaseCalls.length===0&&saveCalls.length===0')
  case('postponing_recovery_keeps_backup_navigation_and_resume', postpone)
  def stale(page):
   page.evaluate('window.rejectRebase=true')
   page.locator('[data-rebase-choice="local"]').click();page.locator('[data-rebase-save]').click()
   page.wait_for_function("document.querySelector('#tutorial-draft-comparison [role=status]').textContent.includes('Харьцуулснаас хойш')")
   assert page.locator('[data-rebase-save]').is_disabled()
   assert page.locator('[data-recovery-cancel]').is_enabled()
   assert page.evaluate('JSON.parse(localStorage.getItem(cacheKey)).body.title') == 'Local edit title'
   assert page.evaluate('JSON.parse(localStorage.getItem(cacheKey+":before-rebase")).body.title') == 'Local edit title'
   assert page.evaluate('saveCalls.length===0&&publishCalls.length===0')
  case('cas_failure_keeps_local_and_before_rebase_backups', stale)
  def backup_failure(page):
   page.evaluate('''()=>{const write=Storage.prototype.setItem;Storage.prototype.setItem=function(key,value){if(key.endsWith(':before-rebase'))throw Error('Backup storage full');return write.call(this,key,value);};}''')
   page.locator('[data-rebase-choice="draft"]').click();page.locator('[data-rebase-save]').click()
   page.wait_for_function("document.querySelector('#tutorial-draft-comparison [role=status]').textContent.includes('Backup storage full')")
   assert page.evaluate('rebaseCalls.length===0&&saveCalls.length===0'), 'backup failure must prevent write'
   assert page.evaluate('JSON.parse(localStorage.getItem(cacheKey)).body.title') == 'Local edit title'
   assert page.locator('[data-recovery-cancel]').is_enabled()
  case('backup_storage_failure_prevents_any_rebase_write', backup_failure)
  def logout(page):
   page.evaluate('window.delayRebase=true')
   page.locator('[data-rebase-choice="draft"]').click();page.locator('[data-rebase-save]').click()
   page.wait_for_function('typeof finishRebase==="function"')
   page.evaluate('async()=>{actor=null;await editor.accountChanged();finishRebase();}')
   page.wait_for_function("document.querySelector('#tutorial-draft-comparison').hidden")
   assert page.locator('#tutorial-admin-form').is_hidden()
   assert page.locator('#tutorial-admin-title').input_value() != 'Online draft title'
   assert page.evaluate('JSON.parse(localStorage.getItem(cacheKey)).body.title') == 'Local edit title'
   assert page.evaluate('saveCalls.length===0&&publishCalls.length===0')
  case('late_rebase_after_logout_cannot_reopen_or_replace_editor', logout)
  browser.close()
finally: server.shutdown()
(ROOT/'audit/RECOVERY-UX-BROWSER.json').write_text(json.dumps({'checks':report,'failures':failures},indent=2)+'\n')
print(json.dumps({'checks':report,'failures':failures}))
assert not failures, failures
