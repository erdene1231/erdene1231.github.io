"""Editor bug regressions in Chromium. RPC/Auth/Storage are mocked; no production writes."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
report={};failures=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  def fresh():
   page=browser.new_page(viewport={'width':1200,'height':900})
   def route(r):
    if not r.request.url.startswith(base):r.abort();return
    if '/app.js?' in r.request.url or '/navigation.js?' in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='');return
    r.continue_()
   page.route('**/*',route);page.goto(base+'/index.html',wait_until='networkidle')
   page.evaluate('''async()=>{
    window.MathJax={startup:{promise:Promise.resolve()},typesetPromise:async()=>{},typesetClear:()=>{}};
    const {setupTutorialEditor}=await import('/tutorial-editor.js?v=36');
    window.actor='00000000-0000-0000-0000-000000000001';window.docCalls=0;window.failLoad=false;window.saveCalls=[];window.rev=0;window.drafts=new Map();window.published=null;
    window.lesson=structuredClone((await (await fetch('/tutorials.json')).json()).tutorials[0]);
    lesson.sections=[{title:'First',blocks:[{type:'rich',content:[{text:'Editable text',marks:[]}]}]},{title:'Second',blocks:[{type:'code',language:'C++17',text:'int x = 1;'}]}];
    lesson.translations={en:{title:'English title',summary:'English summary',prerequisites:'None',sections:structuredClone(lesson.sections)}};
    window.client={rpc:async(name,args)=>{
     if(name==='is_admin')return {data:true};
     if(name==='admin_tutorial_workspace')return {data:{catalog:[{id:lesson.id,title:lesson.title}],drafts:[...drafts].map(([tutorial_id,d])=>({tutorial_id,title:d.body.title}))}};
     if(name==='admin_tutorial_document'){docCalls++;if(failLoad)return {error:Error('Load failed')};return {data:{current:args.p_id===lesson.id?{body:lesson,revision:7}:null,draft:drafts.get(args.p_id)||null}};}
     if(name==='admin_save_tutorial_draft'){saveCalls.push(structuredClone(args));const row={body:structuredClone(args.p_body),revision:++rev,base_revision:args.p_base_revision};drafts.set(args.p_id,row);return {data:row};}if(name==='admin_publish_tutorial_draft'){window.published=args;drafts.delete(args.p_id);return {data:{body:args.p_body,revision:1,draft:null}};}
     throw Error('Unexpected RPC '+name);
    }};
    window.editor=setupTutorialEditor({client:()=>client,user:()=>actor?{id:actor}:null,topics:()=>[lesson],problems:()=>[{number:1,id:'p-one',title:'One task',source:'Judge',ref:'one',tags:['dp'],rating:1200}],progress:()=>({'p-one':{status:'solved'}}),learning:()=>null,ready:()=>true,saved:()=>{}});
    await editor.accountChanged();document.querySelector('#admin-tutorials').hidden=false;
   }''')
   return page
  def case(name,fn):
   page=fresh()
   try:fn(page);report[name]='PASS'
   except Exception as e:report[name]='FAIL';failures.append(name+': '+str(e))
   finally:page.close()
  def failure_freezes(page):
   page.evaluate('window.failLoad=true');page.locator('#tutorial-admin-reload').click()
   page.wait_for_function("document.querySelector('#tutorial-admin-message').textContent.includes('Load failed')")
   assert page.locator('#tutorial-admin-title').is_disabled(),'stale title still editable'
   assert page.locator('#tutorial-admin-sections .editor-block').count()==0,'stale blocks still visible'
   assert page.locator('#tutorial-admin-reload').is_enabled()
   assert page.locator('#tutorial-admin-choose').is_enabled()
   page.evaluate('window.failLoad=false');page.locator('#tutorial-admin-reload').click()
   page.wait_for_function("!document.querySelector('#tutorial-admin-title').disabled")
   assert page.locator('#tutorial-admin-title').input_value()==page.evaluate('lesson.title')
  case('failed_document_load_clears_stale_editor_and_allows_retry',failure_freezes)
  def refresh_preserves(page):
   page.locator('#tutorial-admin-language').select_option('en');page.locator('#tutorial-admin-title').fill('My English draft')
   page.locator('#tutorial-admin-save').click();page.wait_for_function('saveCalls.length>0')
   page.evaluate("window.oldField=document.querySelector('#tutorial-admin-sections .block-rich-input');window.oldCalls=docCalls")
   page.evaluate('async()=>{await editor.refresh();}')
   assert page.locator('#tutorial-admin-language').input_value()=='en','refresh reset language'
   assert page.locator('#tutorial-admin-title').input_value()=='My English draft','refresh lost saved draft'
   assert page.evaluate('oldField===document.querySelector("#tutorial-admin-sections .block-rich-input")'),'refresh rebuilt editor'
   assert page.evaluate('docCalls===oldCalls'),'refresh reloaded document unnecessarily'
  case('catalog_refresh_keeps_draft_language_dom_and_history',refresh_preserves)
  def delete_last(page):
   page.locator('#tutorial-admin-sections .editor-block').first.get_by_role('button',name='Хасах',exact=True).click()
   assert page.locator('#tutorial-admin-sections > details').first.locator('.editor-block').count()==0,'last block could not be removed'
   page.locator('[data-undo]').click()
   assert page.locator('#tutorial-admin-sections > details').first.locator('.editor-block').count()==1
  case('remove_last_block_and_undo',delete_last)
  def preview_guard(page):
   page.locator('#tutorial-admin-preview').click();page.wait_for_function("document.querySelector('#tutorial-preview').open")
   assert page.locator('#tutorial-preview-content').text_content()
   # Native dialog close is bound by app.js in production; isolated test closes directly.
   page.evaluate("document.querySelector('#tutorial-preview').close()")
  case('preview_valid_draft',preview_guard)
  def unfinished_preview(page):
   page.locator('#tutorial-admin-new').click();page.locator('#tutorial-new-id').fill('Fresh Draft Preview')
   page.locator('#tutorial-new-form').get_by_role('button',name='Ноорог үүсгэх',exact=True).click()
   page.wait_for_function("document.querySelector('#tutorial-admin-id').value==='fresh-draft-preview'")
   assert page.locator('#tutorial-admin-title').input_value()=='Fresh Draft Preview'
   page.locator('#tutorial-admin-preview').click();page.wait_for_function("document.querySelector('#tutorial-preview').open")
   assert 'Fresh Draft Preview' in page.locator('#tutorial-preview-content').inner_text()
   assert page.evaluate('published') is None
   page.evaluate("document.querySelector('#tutorial-preview').close()")
   page.locator('#tutorial-admin-sections').get_by_role('button',name='+ Шинэ хэсэг',exact=True).click()
   assert page.evaluate("document.querySelectorAll('#tutorial-admin-sections > details').length")==2
   page.locator('[data-undo]').click();assert page.evaluate("document.querySelectorAll('#tutorial-admin-sections > details').length")==1
   page.locator('[data-redo]').click();assert page.evaluate("document.querySelectorAll('#tutorial-admin-sections > details').length")==2
   for width in [375,1200]:
    page.set_viewport_size({'width':width,'height':950});assert page.locator('#admin-tutorials').evaluate('e=>e.scrollWidth<=e.clientWidth');page.locator('#admin-tutorials').screenshot(path=str(ROOT/f'audit/browser/numeric-editor-workspace-{width}.png'))
  case('name_slug_unfinished_preview_and_section_buttons',unfinished_preview)
  def practice_picker(page):
   page.evaluate("document.querySelector('#tutorial-admin-relations').value=JSON.stringify({practice:[{key:'judge|one',stage:'Standard',priority:true,reason:'Keep this reason'}],variants:[],next:null})")
   page.get_by_role('button',name='Practice бодлого сонгох…').click()
   page.locator('dialog[open] [data-filter=status]').select_option('solved')
   assert page.locator('dialog[open] input[type=checkbox]').count()==1
   page.locator('dialog[open] [data-select-filtered]').click();page.locator('dialog[open] [data-selection-apply]').click()
   assert page.evaluate("JSON.parse(document.querySelector('#tutorial-admin-relations').value).practice[0].key")=='1'
   assert page.evaluate("JSON.parse(document.querySelector('#tutorial-admin-relations').value).practice[0].reason")=='Keep this reason'
   page.locator('#tutorial-admin-save').click();page.wait_for_function('saveCalls.length>0')
   page.locator('#tutorial-admin-preview').click();page.wait_for_function("document.querySelector('#tutorial-preview').open")
   page.evaluate("document.querySelector('#tutorial-preview').close()")
  case('practice_popup_uses_catalog_progress_without_learning_dependency',practice_picker)
  def boundary_buttons(page):
   assert page.locator('#tutorial-admin-sections').get_by_role('button',name='↑ Хэсэг',exact=True).first.is_disabled()
   assert page.locator('#tutorial-admin-sections').get_by_role('button',name='↑',exact=True).first.is_disabled()
   assert page.locator('#tutorial-admin-sections').get_by_role('button',name='↓',exact=True).first.is_disabled()
  case('boundary_move_buttons_are_disabled_instead_of_silent_noops',boundary_buttons)
  def preview_logout(page):
   page.locator('#tutorial-admin-preview').click();page.wait_for_function("document.querySelector('#tutorial-preview').open")
   page.evaluate('async()=>{actor=null;await editor.accountChanged();}')
   assert page.locator('#tutorial-preview').evaluate('e=>!e.open')
   assert page.locator('#tutorial-preview-content').inner_text()==''
  case('logout_closes_preview_and_clears_private_preview_content',preview_logout)
  def formatting(page):
   text=page.locator('.block-rich-input').first;text.click();text.press('Control+a')
   form=page.locator('#tutorial-admin-form');form.get_by_role('button',name='Bold',exact=True).click()
   assert text.locator('b,strong').count()>0
   assert text.evaluate('e=>getComputedStyle(e.querySelector("b,strong")).fontWeight') in ['700','bold']
   form.get_by_role('button',name='Bold',exact=True).click()
   assert text.locator('b,strong').count()==0,'bold did not toggle off'
   text.press('Control+End');form.get_by_role('button',name='Italic',exact=True).click();text.press_sequentially(' italic')
   assert text.locator('i,em').count()>0,'italic before typing did not work'
   form.get_by_role('button',name='Italic',exact=True).click();text.press_sequentially(' normal')
   text.press('Control+a');text.press('Control+b')
   form.get_by_role('button',name='Underline',exact=True).click();form.get_by_role('button',name='Strike',exact=True).click()
   page.locator('#tutorial-admin-save').click();page.wait_for_function("saveCalls.at(-1)?.p_body.sections[0].blocks[0].content?.every(x=>['bold','underline','strike'].every(m=>x.marks.includes(m)))")
   for width in [375,1200]:
    page.set_viewport_size({'width':width,'height':900})
    assert form.evaluate('e=>e.scrollWidth<=e.clientWidth')
    page.locator('#admin-tutorials').screenshot(path=str(ROOT/f'audit/browser/numeric-editor-formatting-{width}.png'))
  case('bold_toggle_italic_before_typing_keyboard_and_autosave',formatting)
  def new_document(page):
   page.locator('#tutorial-admin-new').click();page.locator('#tutorial-new-id').fill('new-recovery-regressionture')
   page.locator('#tutorial-new-form').get_by_role('button',name='Ноорог үүсгэх',exact=True).click()
   page.wait_for_function("document.querySelector('#tutorial-admin-id').value==='new-recovery-regressionture'")
   assert page.locator('#tutorial-admin-title').is_enabled()
   page.locator('#tutorial-admin-title').fill('A new tutorial');page.locator('#tutorial-admin-summary').fill('A complete new summary')
   page.locator('#tutorial-admin-category').fill('Basics');page.locator('.tutorial-editor-settings > summary').click();page.locator('#tutorial-admin-aliases').fill('new tutorial fixture')
   page.locator('#tutorial-admin-save').click();page.wait_for_function("saveCalls.at(-1)?.p_body.title==='A new tutorial'")
   saved=page.evaluate('saveCalls.at(-1)');assert saved['p_base_revision']==0;assert saved['p_body']['aliases']=='new tutorial fixture'
   assert saved['p_body']['related']==[]
   # Preview accepts a new lesson with no practice relationships yet.
   page.locator('#tutorial-admin-preview').click();page.wait_for_function("document.querySelector('#tutorial-preview').open")
   page.evaluate("document.querySelector('#tutorial-preview').close()")
   page.locator('#tutorial-publish-review').click();page.wait_for_selector('[data-publish-confirm]');assert page.evaluate('published') is None
   page.locator('[data-publish-confirm]').click();page.wait_for_function("published?.p_id==='new-recovery-regressionture'")
   assert page.evaluate('published.p_body._draftRelationsText') is None
  case('new_tutorial_fields_private_save_preview_and_explicit_publication',new_document)
  def translation(page):
   page.evaluate('''async()=>{delete lesson.translations;await editor.accountChanged(true);}''')
   mn=page.locator('#tutorial-admin-title').input_value();page.locator('#tutorial-admin-add-en').click()
   assert page.locator('#tutorial-admin-language').input_value()=='en'
   page.locator('#tutorial-admin-title').fill('Brand new English translation');page.locator('#tutorial-admin-save').click()
   page.wait_for_function("saveCalls.at(-1)?.p_body.translations?.en.title==='Brand new English translation'")
   assert page.evaluate('saveCalls.at(-1).p_body.title')==mn
   page.locator('#tutorial-admin-language').select_option('mn');assert page.locator('#tutorial-admin-title').input_value()==mn
  case('create_english_translation_without_overwriting_mongolian',translation)
  def complexity(page):
   # Exercise the real current published document when present; future runs use seed.
   live=Path('/tmp/editor-complexity-body.json')
   if live.exists():body=json.loads(live.read_text())['result'][0]['body']
   else:body=next(t for t in json.loads((ROOT/'tutorials.json').read_text())['tutorials'] if t['id']=='complexity')
   page.evaluate('''async body=>{window.lesson=body;await editor.accountChanged(true);}''',body)
   assert page.locator('#tutorial-admin-id').input_value()=='complexity'
   assert page.locator('#tutorial-admin-title').is_enabled()
   assert page.locator('#tutorial-admin-sections > details').count()==len(body['sections'])
   for detail in page.locator('#tutorial-admin-sections > details').all():detail.evaluate('e=>e.open=true')
   assert page.locator('#tutorial-admin-sections .editor-block').count()==sum(len(s['blocks']) for s in body['sections'])
  case('time_complexity_all_sections_open_and_edit',complexity)
  def local_conflict(page):
   page.evaluate('''async()=>{
    const value={actor,id:lesson.id,body:{...lesson,title:'Recover my local work'},baseRevision:1,draftRevision:0,unsynced:true};
    // Switch away first so the existing clean session cannot overwrite the fixture backup.
    actor=null;await editor.accountChanged();actor=value.actor;
    localStorage.setItem('erdene:tutorial-draft:v3:'+actor+':'+lesson.id,JSON.stringify(value));await editor.accountChanged();
   }''')
   page.wait_for_selector('[data-rebase-choice="local"]',state='attached')
   assert 'Recover my local work' in page.locator('[data-version=local]').text_content()
   assert page.locator('#tutorial-admin-title').is_disabled()
   assert page.evaluate('saveCalls.length')==0,'conflict overwrote online draft'
  case('first_tutorial_local_conflict_opens_recovery_instead_of_dead_editor',local_conflict)
  def private_draft(page):
   page.evaluate('''async()=>{
    const body={...structuredClone(lesson),id:'private-only',title:'Private unfinished lesson'};
    drafts.set(body.id,{body,base_revision:0,revision:1});await editor.accountChanged(true);
   }''')
   assert page.locator('#tutorial-admin-choose option[value="private-only"]').count()==1
   page.locator('#tutorial-admin-choose').select_option('private-only')
   page.wait_for_function("document.querySelector('#tutorial-admin-id').value==='private-only'")
   assert page.locator('#tutorial-admin-title').input_value()=='Private unfinished lesson'
  case('private_only_draft_can_be_reopened_from_workspace',private_draft)
  def duplicate_id(page):
   page.locator('#tutorial-admin-new').click();page.locator('#tutorial-new-id').fill(page.evaluate('lesson.id'))
   page.locator('#tutorial-new-form').get_by_role('button',name='Ноорог үүсгэх',exact=True).click()
   page.wait_for_function("document.querySelector('#tutorial-admin-message').textContent.includes('Энэ ID')")
   assert page.evaluate('saveCalls.length')==0
  case('duplicate_tutorial_id_does_not_overwrite_existing_content',duplicate_id)
  def new_reader(page):
   # A fresh complete tutorial UI exercises the actual saved callback and public list.
   page.reload(wait_until='networkidle')
   page.evaluate('''async()=>{
    window.MathJax={startup:{promise:Promise.resolve()},typesetPromise:async()=>{},typesetClear:()=>{}};
    const {setupTutorials}=await import('/tutorials.js?v=36');
    window.lesson=structuredClone((await (await fetch('/tutorials.json')).json()).tutorials[0]);window.saveCalls=[];window.published=null;window.drafts=new Map();window.rev=0;
    const client={rpc:async(name,args)=>{
     if(name==='get_tutorials')return {data:[{body:lesson,revision:7}]};
     if(name==='is_admin')return {data:true};if(name==='admin_tutorial_workspace')return {data:{catalog:[{id:lesson.id,title:lesson.title}],drafts:[]}};
     if(name==='admin_tutorial_document')return {data:{current:args.p_id===lesson.id?{body:lesson,revision:7}:null,draft:null}};
     if(name==='admin_save_tutorial_draft'){saveCalls.push(args);return {data:{revision:args.p_draft_revision+1}};}
     if(name==='admin_publish_tutorial_draft'){window.published=args;return {data:{body:args.p_body,revision:1,draft:null}};}throw Error(name);
    }};
    window.tutorialUI=setupTutorials({client:()=>client,user:()=>({id:'00000000-0000-0000-0000-000000000001'}),learning:()=>null});await tutorialUI.connected();document.querySelector('#admin-tutorials').hidden=false;
   }''')
   page.wait_for_function("document.querySelector('#tutorial-admin-id').value==='complexity'")
   new_document(page)
   page.wait_for_function("document.querySelector('#tutorial-admin-choose option[value=\"new-recovery-regressionture\"]')!==null")
   page.evaluate("location.hash='#tutorial/new-recovery-regressionture'")
   page.wait_for_function("document.querySelector('#tutorial-title').textContent==='A new tutorial'")
  case('new_publication_appears_in_actual_tutorial_library',new_reader)
  browser.close()
finally:server.shutdown()
(ROOT/'audit/NUMERIC-EDITOR-REGRESSIONS.json').write_text(json.dumps({'checks':report,'failures':failures},indent=2)+'\n')
print(json.dumps({'checks':report,'failures':failures}))
assert not failures,failures
