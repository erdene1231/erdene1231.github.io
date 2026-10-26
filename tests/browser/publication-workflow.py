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
    const {setupTutorials}=await import('/tutorials.js?v=39');
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
     if(name==='admin_reset_tutorial_draft'){const c=catalog.get(args.p_id),d=drafts.get(args.p_id);if(!c?.published||c.revision!==args.p_current_revision||(d?.revision||0)!==args.p_draft_revision)return {error:Error('REVISION_CONFLICT')};drafts.delete(args.p_id);return {data:{...structuredClone(c),draft:null}};}
     if(name==='admin_publish_tutorial_draft'){publishCalls.push(structuredClone(args));const c=catalog.get(args.p_id),d=drafts.get(args.p_id);if((c?.revision||0)!==args.p_base_revision||d.revision!==args.p_draft_revision)throw Error('Bad publish CAS');const result={body:structuredClone(args.p_body),revision:(c?.revision||0)+1,published:true};catalog.set(args.p_id,result);drafts.delete(args.p_id);return {data:{...result,draft:null}};}
     throw Error('Unexpected RPC '+name);
    }};
    window.tutorialUI=setupTutorials({client:()=>client,user:()=>actor?{id:actor}:null,learning:()=>null});await tutorialUI.connected();
    document.querySelector('#admin-tutorials').hidden=false;location.hash='#tutorial/complexity';
   }''')
   page.wait_for_function("document.querySelector('#tutorial-admin-id').value==='complexity'&&!document.querySelector('#tutorial-admin-title').disabled")
   page.wait_for_function("document.querySelector('#tutorial-title').textContent==='Public lifecycle lesson'")
   return page, errors
  page,errors=fresh()
  assert page.locator('#tutorial-admin-add-en').count()==0
  assert page.locator('#tutorial-reset').is_visible()
  assert page.locator('#tutorial-delete-review').is_hidden()
  page.locator('#tutorial-admin-title').fill('Volatile edit')
  page.wait_for_timeout(1900)
  assert page.evaluate('saveCalls.length')==0
  page.evaluate('async()=>{await tutorialUI.connected()}')
  page.wait_for_function("document.querySelector('#tutorial-admin-title').value==='Public lifecycle lesson'")
  report['unsaved_published_edits_disappear_on_reload']='PASS'
  page.locator('#tutorial-admin-title').fill('Temporary private')
  page.locator('#tutorial-admin-save').click();page.wait_for_function('saveCalls.length===1')
  assert page.evaluate('catalog.get(lesson.id).body.title')=='Public lifecycle lesson'
  page.evaluate('async()=>{await tutorialUI.connected()}')
  page.wait_for_function("document.querySelector('#tutorial-admin-title').value==='Temporary private'")
  report['explicit_temporary_save_survives_reload_without_public_change']='PASS'
  page.locator('#tutorial-reset').click();page.wait_for_selector('[data-reset-confirm]');page.locator('[data-reset-confirm]').click()
  page.wait_for_function("document.querySelector('#tutorial-admin-title').value==='Public lifecycle lesson'&&document.querySelector('#tutorial-reset').disabled")
  assert page.evaluate('drafts.has(lesson.id)') is False
  report['reset_restores_public_and_removes_owner_draft']='PASS'
  page.locator('#tutorial-admin-language').select_option('en')
  assert page.locator('#tutorial-admin-title').input_value()==''
  page.locator('#tutorial-admin-summary').fill('English summary')
  page.locator('#tutorial-admin-language').select_option('mn')
  assert page.locator('#tutorial-admin-title').input_value()=='Public lifecycle lesson'
  page.locator('#tutorial-admin-language').select_option('en');assert page.locator('#tutorial-admin-summary').input_value()=='English summary'
  page.locator('#tutorial-admin-language').select_option('mn')
  page.locator('#tutorial-publish-review').click();page.wait_for_function('publishCalls.length===1')
  assert page.locator('[data-publish-confirm]').count()==0
  report['language_selector_and_immediate_published_update']='PASS'
  page.locator('#tutorial-admin-new').click();page.locator('#tutorial-new-id').fill('Empty lesson')
  page.locator('#tutorial-new-form').get_by_role('button',name='Ноорог үүсгэх',exact=True).click()
  page.wait_for_function("document.querySelector('#tutorial-admin-id').value==='empty-lesson'")
  assert page.locator('#tutorial-admin-sections .editor-section').count()==0
  assert page.locator('#tutorial-reset').is_hidden()
  assert page.locator('#tutorial-visibility-review').is_hidden()
  page.locator('#tutorial-publish-review').click();page.wait_for_selector('[data-publish-confirm]');page.locator('[data-publish-confirm]').click()
  page.wait_for_function("catalog.has('empty-lesson')&&catalog.get('empty-lesson').published")
  assert page.evaluate("catalog.get('empty-lesson').body.sections.length")==0
  assert page.locator('#tutorial-delete-review').is_hidden()
  assert page.locator('#tutorial-visibility-review').is_visible()
  page.evaluate("location.hash='#tutorial/empty-lesson'");page.wait_for_function("document.querySelector('#tutorial-title').textContent==='Empty lesson'")
  assert page.locator('#tutorial-summary').is_hidden();assert page.locator('#tutorial-prerequisites').is_hidden();assert page.locator('#tutorial-content > section').count()==0
  report['named_empty_tutorial_publishes_and_switches_footer']='PASS'
  assert not errors,errors
  for width in [375,1200]:
   page.set_viewport_size({'width':width,'height':950});page.locator('#admin-tutorials').screenshot(path=str(ROOT/f'audit/browser/workflow-{width}.png'))
  browser.close()
finally:server.shutdown()
(ROOT/'audit/PUBLICATION-WORKFLOW-BROWSER.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
