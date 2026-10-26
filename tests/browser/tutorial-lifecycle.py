"""Tutorial lifecycle through the real editor/reader in Chromium; mock Auth/RPC only."""
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
   page = browser.new_page(viewport={'width':1200,'height':950})
   page.set_default_timeout(8000)
   errors=[]
   page.on('pageerror', lambda e: errors.append(str(e)))
   def route(r):
    if not r.request.url.startswith(base): r.abort(); return
    if '/app.js?' in r.request.url or '/navigation.js?' in r.request.url:
     r.fulfill(status=200, content_type='text/javascript', body=''); return
    r.continue_()
   page.route('**/*', route)
   page.goto(base+'/index.html', wait_until='networkidle')
   page.evaluate('''async()=>{
    window.MathJax={startup:{promise:Promise.resolve()},typesetPromise:async()=>{},typesetClear:()=>{}};
    const {setupTutorials}=await import('/tutorials.js?v=38');
    window.actor='00000000-0000-0000-0000-000000000001';window.admin=true;
    window.visibilityCalls=[];window.deleteCalls=[];window.saveCalls=[];window.publishCalls=[];window.docCalls=[];
    window.failSave=false;window.visibilityError='';window.deleteError='';window.delayVisibility=false;window.delayDelete=false;window.delayDocument=false;
    const original=structuredClone((await (await fetch('/tutorials.json')).json()).tutorials[0]);
    window.lesson={...original,id:'complexity',title:'Public lifecycle lesson',prerequisiteIds:[],related:[],translations:undefined,
      sections:[{title:'Lifecycle fixture',blocks:[{type:'rich',content:[{text:'Published paragraph',marks:[]}]}]}]};
    window.other={...structuredClone(lesson),id:'surviving-lesson',title:'Surviving lesson'};
    window.catalog=new Map([[lesson.id,{body:structuredClone(lesson),revision:7,published:true}],[other.id,{body:structuredClone(other),revision:12,published:true}]]);
    window.drafts=new Map();window.deletedIds=new Set();window.cacheKey='erdene:tutorial-draft:v3:'+actor+':complexity';
    window.progressKey='erdene:test-preserved-progress';localStorage.setItem(progressKey,JSON.stringify({'complexity':{readSections:[0]},'surviving-lesson':{readSections:[0],mastered:true}}));
    window.originalProgress=localStorage.getItem(progressKey);window.originalOther=JSON.stringify(catalog.get(other.id));
    window.client={rpc:async(name,args)=>{
     if(name==='get_tutorials')return {data:[...catalog.values()].filter(t=>t.published).map(t=>structuredClone(t))};
     if(name==='is_admin')return {data:admin};
     if(name==='admin_tutorial_workspace')return {data:{catalog:[...catalog.values()].map(t=>({id:t.body.id,title:t.body.title,revision:t.revision,published:t.published})),drafts:[...drafts].map(([id,d])=>({tutorial_id:id,title:d.body.title,base_revision:d.base_revision,revision:d.revision}))}};
     if(name==='admin_tutorial_document'){
      docCalls.push(args.p_id);const result=()=>({data:{current:structuredClone(catalog.get(args.p_id)||null),draft:structuredClone(drafts.get(args.p_id)||null),deleted:deletedIds.has(args.p_id)}});
      if(delayDocument)return new Promise(resolve=>window.finishDocument=()=>resolve(result()));return result();
     }
     if(name==='admin_save_tutorial_draft'){
      saveCalls.push(structuredClone(args));if(failSave)return {error:Error('SAVE_FAILED: offline')};
      const old=drafts.get(args.p_id);if((old?.revision||0)!==args.p_draft_revision)return {error:Error('REVISION_CONFLICT: draft changed')};
      const d={body:structuredClone(args.p_body),base_revision:args.p_base_revision,revision:args.p_draft_revision+1};drafts.set(args.p_id,d);return {data:structuredClone(d)};
     }
     if(name==='admin_set_tutorial_publication'){
      visibilityCalls.push(structuredClone(args));const result=()=>{
       if(visibilityError)return {error:Error(visibilityError)};const current=catalog.get(args.p_id);
       if(current.revision!==args.p_revision)return {error:Error('REVISION_CONFLICT: catalog changed')};
       const oldRevision=current.revision;current.published=args.p_published;current.revision++;
       const draft=drafts.get(args.p_id);let remaining=null;if(draft?.base_revision===oldRevision){draft.base_revision=current.revision;draft.revision++;remaining=structuredClone(draft);}
       return {data:{...structuredClone(current),draft:remaining}};
      };
      if(delayVisibility)return new Promise(resolve=>window.finishVisibility=()=>resolve(result()));return result();
     }
     if(name==='admin_delete_tutorial'){
      deleteCalls.push(structuredClone(args));const result=()=>{
       if(deleteError)return {error:Error(deleteError)};const current=catalog.get(args.p_id);
       if(current?.revision!==args.p_revision)return {error:Error('REVISION_CONFLICT: catalog changed')};
       if(current.published||args.p_confirmation!==args.p_id)throw Error('Invalid permanent deletion confirmation');
       catalog.delete(args.p_id);drafts.delete(args.p_id);deletedIds.add(args.p_id);return {data:{id:args.p_id,deleted:true}};
      };
      if(delayDelete)return new Promise(resolve=>window.finishDelete=()=>resolve(result()));return result();
     }
     if(name==='admin_delete_tutorial_draft'){deleteCalls.push(structuredClone(args));const d=drafts.get(args.p_id);if(catalog.has(args.p_id)||(d?.revision||0)!==args.p_draft_revision)return {error:Error('REVISION_CONFLICT: changed')};drafts.delete(args.p_id);return {data:{id:args.p_id,deleted:true}};}
     if(name==='admin_publish_tutorial_draft'){publishCalls.push(structuredClone(args));const c=catalog.get(args.p_id),d=drafts.get(args.p_id);if(c.revision!==args.p_base_revision||d.revision!==args.p_draft_revision)throw Error('Bad publish CAS');const result={body:structuredClone(args.p_body),revision:c.revision+1,published:true};catalog.set(args.p_id,result);drafts.delete(args.p_id);return {data:{...result,draft:null}};}
     throw Error('Unexpected RPC '+name);
    }};
    window.tutorialUI=setupTutorials({client:()=>client,user:()=>actor?{id:actor}:null,learning:()=>null});await tutorialUI.connected();
    document.querySelector('#admin-tutorials').hidden=false;location.hash='#tutorial/complexity';
   }''')
   page.wait_for_function("document.querySelector('#tutorial-admin-id').value==='complexity'&&!document.querySelector('#tutorial-admin-title').disabled")
   page.wait_for_function("document.querySelector('#tutorial-title').textContent==='Public lifecycle lesson'")
   return page, errors
  def check_preserved(page):
   assert page.evaluate('localStorage.getItem(progressKey)===originalProgress'), 'progress changed'
   assert page.evaluate('JSON.stringify(catalog.get(other.id))===originalOther'), 'surviving ID/body/revision changed'
   assert page.evaluate('publishCalls.length===0'), 'private content published by lifecycle action'
  def case(name, fn, preserve=True):
   page, errors=fresh()
   try:
    fn(page)
    if preserve:check_preserved(page)
    assert not errors, errors
    report[name]='PASS'
   except Exception as e:report[name]='FAIL';failures.append(name+': '+str(e))
   finally:page.close()
  def review(page, mode):
   page.locator('#tutorial-delete-review' if mode=='delete' else '#tutorial-visibility-review').click()
   page.wait_for_selector('[data-lifecycle-confirm="'+mode+'"]')
  def hide(page):
   review(page,'hide');page.locator('[data-lifecycle-confirm="hide"]').click()
   page.wait_for_function("document.querySelector('#tutorial-visibility-review').hidden&&!document.querySelector('#tutorial-delete-review').hidden&&!document.querySelector('#tutorial-delete-review').disabled")
  def initial_cancel(page):
   assert page.locator('#tutorial-delete-review').is_hidden()
   review(page,'hide')
   assert page.evaluate('visibilityCalls.length===0&&deleteCalls.length===0')
   assert page.locator('#tutorial-admin-title').is_disabled()
   page.locator('[data-lifecycle-cancel]').click()
   assert page.locator('#tutorial-admin-title').is_enabled()
   assert page.evaluate('catalog.get(lesson.id).published===true&&visibilityCalls.length===0')
  case('review_and_cancel_do_not_change_visibility', initial_cancel)
  def hide_publish(page):
   page.locator('#tutorial-admin-title').fill('Private unsent revision');hide(page)
   assert page.evaluate('catalog.get(lesson.id).published') is False
   assert page.evaluate('catalog.get(lesson.id).body.title')=='Public lifecycle lesson'
   assert page.locator('#tutorial-admin-title').input_value()=='Private unsent revision'
   assert page.locator('#tutorial-visibility-review').is_hidden()
   assert page.locator('.tutorial-editor-savebar #tutorial-delete-review').is_visible()
   assert 'ноорог' in page.locator('#tutorial-admin-choose option[value="complexity"]').text_content()
   page.locator('#tutorial-publish-review').click();page.wait_for_selector('[data-publish-confirm]');assert page.evaluate('publishCalls.length')==0
   page.locator('[data-publish-confirm]').click();page.wait_for_function("catalog.get(lesson.id).published&&document.querySelector('#tutorial-visibility-review').hidden===false")
   assert page.evaluate('catalog.get(lesson.id).body.title')=='Private unsent revision'
   assert page.evaluate('publishCalls.length')==1
   assert page.evaluate('localStorage.getItem(progressKey)===originalProgress&&JSON.stringify(catalog.get(other.id))===originalOther')
  case('temporary_remove_is_draft_then_explicit_publish_uses_current_draft',hide_publish,False)
  def failed_save(page):
   page.evaluate('window.failSave=true');page.locator('#tutorial-admin-title').fill('Keep offline edit')
   page.locator('#tutorial-visibility-review').click()
   page.wait_for_function("document.querySelector('#tutorial-lifecycle').textContent.includes('Эхлээд нооргоо')")
   assert page.locator('[data-lifecycle-confirm]').count()==0
   assert page.evaluate('visibilityCalls.length===0')
   assert page.evaluate('JSON.parse(localStorage.getItem(cacheKey)).body.title')=='Keep offline edit'
   page.locator('[data-lifecycle-cancel]').click();assert page.locator('#tutorial-admin-title').input_value()=='Keep offline edit'
  case('failed_private_save_blocks_visibility_change_and_keeps_local_edit', failed_save)
  def stale_catalog(page):
   review(page,'hide');page.evaluate('catalog.get(lesson.id).revision++')
   page.locator('[data-lifecycle-confirm="hide"]').click()
   page.wait_for_function("document.querySelector('#tutorial-lifecycle [role=status]').textContent.includes('Хувилбар өөрчлөгджээ')")
   assert page.locator('[data-lifecycle-confirm="hide"]').is_disabled()
   assert page.locator('[data-lifecycle-cancel]').is_enabled()
   assert page.evaluate('visibilityCalls.length===1&&catalog.get(lesson.id).published')
  case('catalog_revision_conflict_blocks_blind_retry', stale_catalog)
  def stale_private(page):
   page.evaluate('''()=>{catalog.get(lesson.id).revision=9;}''')
   page.locator('#tutorial-visibility-review').click()
   page.wait_for_function("document.querySelector('#tutorial-lifecycle').textContent.includes('Хувилбар өөрчлөгджээ')")
   assert page.evaluate('visibilityCalls.length===0')
   assert page.evaluate('JSON.parse(localStorage.getItem(cacheKey)).baseRevision')==7
   assert page.evaluate('drafts.get(lesson.id).base_revision')==7
  case('stale_private_base_requires_explicit_rebase_before_visibility_change', stale_private)
  def dependency(page):
   page.evaluate("window.visibilityError='A published tutorial still requires this prerequisite.'")
   review(page,'hide');page.locator('[data-lifecycle-confirm="hide"]').click()
   page.wait_for_function("document.querySelector('#tutorial-lifecycle [role=status]').textContent.includes('урьдчилсан хичээл')")
   assert page.evaluate('catalog.get(lesson.id).published')
   page.locator('[data-lifecycle-cancel]').click();assert page.locator('#tutorial-admin-title').is_enabled()
  case('prerequisite_failure_explains_blocker_and_preserves_editor', dependency)
  def twice(page):
   page.evaluate('window.delayVisibility=true');review(page,'hide')
   page.locator('[data-lifecycle-confirm="hide"]').evaluate('e=>{e.click();e.click();}')
   page.wait_for_function('typeof finishVisibility==="function"')
   assert page.evaluate('visibilityCalls.length')==1
   assert page.locator('[data-lifecycle-cancel]').is_disabled()
   page.evaluate('finishVisibility()');page.wait_for_function("document.querySelector('#tutorial-lifecycle').hidden")
  case('repeated_confirmation_sends_one_visibility_request', twice)
  def logout_late(page):
   page.evaluate('window.delayVisibility=true');review(page,'hide');page.locator('[data-lifecycle-confirm="hide"]').click()
   page.wait_for_function('typeof finishVisibility==="function"')
   page.evaluate('()=>{actor=null;tutorialUI.accountChanged();finishVisibility();}')
   page.wait_for_function("document.querySelector('#tutorial-admin-form').hidden&&document.querySelector('#tutorial-lifecycle').hidden")
   assert page.locator('#tutorial-admin-form').is_hidden()
   assert page.evaluate('JSON.parse(localStorage.getItem(cacheKey)).baseRevision')==7, 'late result altered logged-out local session'
  case('late_visibility_response_after_logout_cannot_reopen_editor', logout_late)
  def review_logout(page):
   page.evaluate('window.delayDocument=true');page.locator('#tutorial-visibility-review').click()
   page.wait_for_function('typeof finishDocument==="function"')
   page.evaluate('()=>{actor=null;tutorialUI.accountChanged();finishDocument();}')
   page.wait_for_function("document.querySelector('#tutorial-lifecycle').hidden")
   assert page.locator('[data-lifecycle-confirm]').count()==0
   assert page.evaluate('visibilityCalls.length===0&&deleteCalls.length===0')
  case('late_review_response_after_logout_cannot_show_confirmation', review_logout)
  def permanent(page):
   page.locator('#tutorial-admin-title').fill('Draft to discard only on confirmation');hide(page);review(page,'delete')
   assert page.locator('[data-lifecycle-confirm="delete"]').is_disabled()
   page.locator('[data-delete-id]').fill('other-id')
   assert page.locator('[data-lifecycle-confirm="delete"]').is_disabled()
   page.locator('[data-delete-id]').fill('complexity ')
   assert page.locator('[data-lifecycle-confirm="delete"]').is_disabled(), 'confirmation must be exact'
   page.locator('[data-delete-id]').fill('complexity')
   assert page.locator('[data-lifecycle-confirm="delete"]').is_enabled()
   for width in [375,1200]:
    page.set_viewport_size({'width':width,'height':950})
    assert page.locator('#admin-tutorials').evaluate('e=>e.scrollWidth<=e.clientWidth')
    page.locator('#tutorial-lifecycle').screenshot(path=str(ROOT/f'audit/browser/draft-actions-deletion-{width}.png'))
   assert page.evaluate('deleteCalls.length===0')
   page.locator('[data-lifecycle-confirm="delete"]').click()
   page.wait_for_function("document.querySelector('#tutorial-admin-id').value==='surviving-lesson'")
   assert page.evaluate('deleteCalls[0].p_confirmation')=='complexity'
   assert page.evaluate('deleteCalls[0].p_revision')==8
   assert page.evaluate('!catalog.has("complexity")&&!drafts.has("complexity")')
   assert page.evaluate('localStorage.getItem(cacheKey)') is None
   assert page.locator('#tutorial-admin-choose option[value="complexity"]').count()==0
   assert page.locator('#tutorial-grid a[href="#tutorial/complexity"]').count()==0
   assert page.evaluate('catalog.get("surviving-lesson").body.id')=='surviving-lesson'
  case('permanent_delete_requires_exact_id_and_keeps_surviving_ids_progress', permanent)
  def delete_cancel(page):
   hide(page);review(page,'delete');page.locator('[data-delete-id]').fill('complexity');page.locator('[data-lifecycle-cancel]').click()
   assert page.evaluate('deleteCalls.length===0&&catalog.has("complexity")&&drafts.has("complexity")')
   assert page.locator('#tutorial-admin-title').is_enabled()
  case('permanent_delete_cancel_preserves_archived_content_and_draft', delete_cancel)
  def delete_failure(page):
   hide(page);page.evaluate("window.deleteError='Tutorial is referenced by another draft.'")
   review(page,'delete');page.locator('[data-delete-id]').fill('complexity');page.locator('[data-lifecycle-confirm="delete"]').click()
   page.wait_for_function("document.querySelector('#tutorial-lifecycle [role=status]').textContent.includes('referenced')")
   assert page.evaluate('catalog.has("complexity")&&drafts.has("complexity")')
   assert page.locator('[data-lifecycle-confirm="delete"]').is_disabled()
   page.locator('[data-lifecycle-cancel]').click();assert page.locator('#tutorial-admin-title').is_enabled()
  case('permanent_delete_dependency_failure_keeps_draft_and_requires_new_review', delete_failure)
  def late_delete(page):
   hide(page);page.evaluate('window.delayDelete=true');review(page,'delete');page.locator('[data-delete-id]').fill('complexity');page.locator('[data-lifecycle-confirm="delete"]').click()
   page.wait_for_function('typeof finishDelete==="function"')
   page.evaluate('()=>{actor=null;tutorialUI.accountChanged();finishDelete();}')
   page.wait_for_function("document.querySelector('#tutorial-admin-form').hidden&&document.querySelector('#tutorial-lifecycle').hidden")
   assert page.locator('#tutorial-admin-form').is_hidden()
  case('late_permanent_delete_after_logout_cannot_reopen_another_tutorial', late_delete)
  def private_only(page):
   page.locator('#tutorial-admin-new').click();page.locator('#tutorial-new-id').fill('never-published')
   page.locator('#tutorial-new-form').get_by_role('button',name='Ноорог үүсгэх',exact=True).click()
   page.wait_for_function("document.querySelector('#tutorial-admin-id').value==='never-published'")
   assert page.locator('#tutorial-visibility-review').is_hidden()
   assert page.locator('#tutorial-delete-review').is_visible()
   review(page,'delete');page.locator('[data-delete-id]').fill('never-published');page.locator('[data-lifecycle-confirm="delete"]').click()
   page.wait_for_function("!document.querySelector('#tutorial-admin-choose option[value=never-published]')")
   assert page.evaluate('deleteCalls.at(-1).p_draft_revision')==0
   assert page.evaluate('!drafts.has("never-published")&&visibilityCalls.length===0')
  case('private_only_draft_is_permanently_removed_with_confirmation', private_only)
  def nonadmin(page):
   page.evaluate('async()=>{admin=false;await tutorialUI.connected();}')
   page.wait_for_function("document.querySelector('#tutorial-admin-form').hidden")
   assert page.locator('#tutorial-visibility-review').is_hidden()
   assert page.locator('#tutorial-delete-review').is_hidden()
   assert page.evaluate('deleteCalls.length===0&&visibilityCalls.length===0')
  case('non_admin_cannot_access_lifecycle_controls', nonadmin)
  def logout_private(page):
   page.locator('#tutorial-admin-new').click();page.locator('#tutorial-new-id').fill('private-logout-fixture')
   page.locator('#tutorial-new-form').get_by_role('button',name='Ноорог үүсгэх',exact=True).click()
   page.wait_for_function("document.querySelector('#tutorial-admin-id').value==='private-logout-fixture'")
   page.locator('#tutorial-admin-title').fill('Confidential private title');page.locator('#tutorial-admin-save').click()
   page.wait_for_function("drafts.get('private-logout-fixture')?.body.title==='Confidential private title'")
   assert page.locator('#tutorial-admin-choose option[value="private-logout-fixture"]').count()==1
   page.evaluate('()=>{actor=null;tutorialUI.accountChanged();}')
   assert page.locator('#tutorial-admin-form').is_hidden()
   assert page.locator('#tutorial-admin-title').input_value()==''
   assert page.locator('#tutorial-admin-id').input_value()==''
   assert page.locator('#tutorial-admin-choose option').count()==0
   for control in ['choose','reload','new','title','save','preview','language']:
    assert page.locator('#tutorial-admin-'+control).is_disabled(), control+' enabled after logout'
   assert page.locator('#tutorial-admin-sections .editor-block').count()==0
   assert page.evaluate("JSON.parse(localStorage.getItem('erdene:tutorial-draft:v3:00000000-0000-0000-0000-000000000001:private-logout-fixture')).body.title")=='Confidential private title'
  case('logout_clears_private_options_title_controls_and_preserves_backup', logout_private)
  def tombstone(page):
   page.evaluate("deletedIds.add('permanently-gone')")
   page.locator('#tutorial-admin-new').click();page.locator('#tutorial-new-id').fill('permanently-gone')
   page.locator('#tutorial-new-form').get_by_role('button',name='Ноорог үүсгэх',exact=True).click()
   page.wait_for_function("document.querySelector('#tutorial-admin-message').textContent.includes('үүрд устгагдсан')")
   assert page.locator('#tutorial-admin-id').input_value()=='complexity'
   assert page.locator('#tutorial-admin-title').input_value()=='Public lifecycle lesson'
   assert page.evaluate("!drafts.has('permanently-gone')&&saveCalls.every(x=>x.p_id!=='permanently-gone')")
   assert page.locator('#tutorial-admin-choose option[value="permanently-gone"]').count()==0
  case('server_tombstone_rejects_id_reuse_before_new_draft_creation', tombstone)
  def startup(page, mode):
   page.reload(wait_until='networkidle')
   page.evaluate('''async mode=>{
    window.MathJax={startup:{promise:Promise.resolve()},typesetPromise:async()=>{},typesetClear:()=>{}};
    const {setupTutorials}=await import('/tutorials.js?v=38');window.catalogRequests=0;
    window.startClient=mode==='failed'?{rpc:async name=>{if(name==='get_tutorials'){catalogRequests++;return {error:Error('Offline catalog')};}throw Error('Unexpected RPC '+name);}}:null;
    window.startUI=setupTutorials({...(mode==='pending'?{requiresOnline:true}:{}),client:()=>startClient,user:()=>null,learning:()=>null});
    if(mode==='failed')await startUI.connected();
   }''', mode)
   page.wait_for_load_state('networkidle')
   page.evaluate('()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))')
  def configured_startup(page):
   startup(page,'pending')
   assert page.locator('#tutorial-grid .tutorial-card').count()==0, 'seed appeared before configured client initialized'
   assert page.locator('#tutorial-admin-choose option').count()==0
   assert 'ачаалж байна' in page.locator('#tutorial-message').text_content()
   page.evaluate('''()=>{
    startClient={rpc:async name=>{if(name==='get_tutorials'){catalogRequests++;return new Promise(resolve=>window.finishCatalog=()=>resolve({data:[]}));}throw Error('Unexpected RPC '+name);}};
    window.catalogPending=startUI.connected();
   }''')
   page.wait_for_function('typeof finishCatalog==="function"')
   assert page.locator('#tutorial-grid .tutorial-card').count()==0, 'seed appeared while catalog response pending'
   page.evaluate('async()=>{finishCatalog();await catalogPending;}')
   assert page.locator('#tutorial-grid .tutorial-card').count()==0, 'empty authoritative catalog resurrected seed'
   page.evaluate("location.hash='#tutorial/complexity'")
   page.wait_for_function("document.querySelector('#tutorial-reader').hidden")
   assert page.evaluate('catalogRequests')==1
   startup(page,'failed')
   assert page.locator('#tutorial-grid .tutorial-card').count()==0, 'failed first catalog read fell back to seed'
   assert page.locator('#tutorial-reader').is_hidden()
   assert 'баталгаажуулж чадсангүй' in page.locator('#tutorial-message').text_content()
   assert page.evaluate('catalogRequests')==1
  case('configured_pending_empty_or_failed_catalog_never_resurrects_seed', configured_startup, False)
  def offline_demo(page):
   startup(page,'offline')
   page.wait_for_function("document.querySelectorAll('#tutorial-grid .tutorial-card').length>0")
   page.evaluate("location.hash='#tutorial/complexity'")
   page.wait_for_function("!document.querySelector('#tutorial-reader').hidden&&document.querySelector('#tutorial-title').textContent.length>0")
   assert page.evaluate('catalogRequests')==0
  case('unconfigured_offline_demo_still_displays_seed_lessons', offline_demo, False)
  browser.close()
finally:server.shutdown()
(ROOT/'audit/DRAFT-ACTIONS-LIFECYCLE-BROWSER.json').write_text(json.dumps({'checks':report,'failures':failures},indent=2)+'\n')
print(json.dumps({'checks':report,'failures':failures}))
assert not failures, failures
