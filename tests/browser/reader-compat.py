"""Isolated real-Chromium checks. App/Auth/Storage writes are mocked, never live."""
import functools
import http.server
import json
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}'
report = {}
try:
 with sync_playwright() as p:
  browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
  page = browser.new_page(viewport={'width':1440,'height':1000})
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   url=r.request.url
   if not url.startswith(base):r.abort();return
   if '/app.js?' in url or '/navigation.js?' in url:r.fulfill(status=200,content_type='text/javascript',body='');return
   r.continue_()
  page.route('**/*',route)
  page.goto(base+'/index.html',wait_until='networkidle')
  page.evaluate('''async()=>{
   window.MathJax={startup:{promise:Promise.resolve()},typesetPromise:async()=>{},typesetClear:()=>{}};
   const {renderBlock,drawArticle}=await import('/tutorials.js?v=30');
   window.renderBlock=renderBlock;window.drawArticle=drawArticle;
   const lessons=(await (await fetch('/tutorials.json')).json()).tutorials;
   window.original=structuredClone(lessons[0]);window.fixture=structuredClone(original);
   delete fixture.translations;
   fixture.sections=[{title:'Reader compatibility',blocks:[
    {type:'rich',content:[{text:'<img src=x onerror="window.injected=1"> $n$',marks:['bold','code']},{text:' Safe link',href:'https://example.com'}]},
    {type:'heading',level:1,text:'A content heading'},
    {type:'callout',tone:'proof',text:'Proof with $n$ preserved.'},
    {type:'quote',text:'Text only'},
    {type:'checklist',items:[{text:'Explain the invariant',checked:false}]},
    {type:'diagram',kind:'graph',nodes:[{id:'a',label:'A',x:20,y:20},{id:'b',label:'B',x:80,y:80}],edges:[['a','b']]},
    {type:'diagram',kind:'dp',rows:[Array(30).fill('12345')]},
    {type:'image',path:'test-lesson/00000000-0000-0000-0000-000000000001/11111111-1111-1111-1111-111111111111.webp',alt:'An unavailable image',width:80,align:'center'},
    {type:'tutorial',tutorialId:'binary-search',label:'Binary search'},
    {type:'problem',problemKey:'cses|1071'},
    {type:'code',language:'C++17',text:'int main() { return 0; }'},
    {type:'p',text:'An editable legacy paragraph.'}
   ]}];
   const target=document.createElement('article');target.id='compat-reader';target.className='tutorial-content';target.style.cssText='width:100%;max-width:900px;min-width:0;margin:auto;padding:16px';
   for(const child of document.body.children)child.hidden=true;
   document.body.append(target);drawArticle(fixture,target,'en');
   renderBlock(null,target,'en');renderBlock({type:'unknown'},target,'en');
   renderBlock({type:'rich',content:[{text:'bad',href:'javascript:alert(1)'}]},target,'en');
   window.lessons=lessons;window.richBefore=JSON.stringify(fixture.sections[0].blocks[0]);
  }''')
  page.wait_for_function("document.querySelector('.tutorial-image button') !== null")
  assert page.locator('#compat-reader .rich-text img').count()==0
  assert page.evaluate('window.injected') is None
  assert page.locator('#compat-reader h1').count()==0
  assert page.locator('#compat-reader .diagram-graph line').count()==1
  assert page.locator('#compat-reader .tutorial-note').count()>=3
  assert page.locator('#compat-reader .rich-text a').get_attribute('rel')=='noopener noreferrer'
  assert page.locator('#compat-reader .content-checklist input').is_disabled()
  assert page.locator('#compat-reader .language-cpp').count()==1
  # Clipboard behavior and real MathJax network typesetting are outside this check.
  report['safe_typed_dom']='PASS'
  for width,theme in [(1440,'light'),(375,'light'),(1440,'dark'),(375,'dark')]:
   page.set_viewport_size({'width':width,'height':1000})
   page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
   assert page.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth'),(width,theme)
   # Line coordinates must align with percentage-positioned HTML nodes at both sizes.
   assert page.evaluate('''()=>{
    const svg=document.querySelector('.diagram-graph svg'),line=svg.querySelector('line');
    const point=new DOMPoint(line.x1.baseVal.value,line.y1.baseVal.value).matrixTransform(svg.getScreenCTM());
    const box=document.querySelector('.diagram-node').getBoundingClientRect();
    return Math.abs(point.x-(box.x+box.width/2))<1&&Math.abs(point.y-(box.y+box.height/2))<1;
   }''')
   out=ROOT/'audit/browser';out.mkdir(parents=True,exist_ok=True)
   page.screenshot(path=str(out/f'step-009-{width}-{theme}.png'),full_page=True)
  report['desktop_mobile_light_dark_overflow']='PASS'
  page.evaluate('''async()=>{
   const {setupLearning}=await import('/learning.js?v=30');
   const catalog=(await (await fetch('/problems.json')).json()).problems;
   window.learningProgress={};window.openedProblem=null;
   window.learning=await setupLearning({client:()=>null,user:()=>null,profile:()=>null,
    problems:()=>catalog,progress:()=>learningProgress,openProblem:p=>{window.openedProblem=p.id;}});
   const topics=structuredClone(lessons),current=topics.find(t=>t.id==='complexity'),target=topics.find(t=>t.id==='brute-force');
   delete target.translations;window.mnVariantTitle=target.title;learning.setTopics(topics);
   const extras=document.getElementById('tutorial-learning-extras'),article=document.getElementById('tutorial-content');
   extras.replaceChildren();article.replaceChildren();extras.hidden=false;article.hidden=false;
   document.body.append(article,extras);learning.renderTutorial(current,'en',extras);
   window.embeddedProblem=catalog.find(p=>p.source==='CSES'&&p.ref==='1071');
   renderBlock({type:'problem',problemKey:'cses|1071'},article,'en',{learning});
  }''')
  assert page.locator('#tutorial-learning-extras .learning-variant a[href="#tutorial/brute-force"]').inner_text()==page.evaluate('mnVariantTitle')
  assert page.locator('#tutorial-content .learning-problem strong').inner_text()==page.evaluate('embeddedProblem.title')
  page.locator('#tutorial-content .learning-problem-open').click()
  assert page.evaluate('openedProblem===embeddedProblem.id')
  page.evaluate("()=>{learningProgress[embeddedProblem.id]={status:'solved'};learning.progressChanged(embeddedProblem.id,'new','solved');}")
  page.wait_for_function("document.querySelector('#tutorial-content .learning-problem .badge').textContent.includes('Solved')")
  page.evaluate("()=>{learning.store.set('bookmark',embeddedProblem.id,{saved:true});}")
  page.wait_for_function("document.querySelector('#tutorial-content [data-bookmark]').textContent==='Saved ✓'")
  report['learning_mn_variant_and_embedded_problem_refresh']='PASS'
  page.evaluate("()=>{document.getElementById('tutorial-content').hidden=true;document.getElementById('tutorial-learning-extras').hidden=true;}")
  page.evaluate('''async()=>{
   document.querySelector('#compat-reader').hidden=true;
   // Reuse the real form; mount it directly to remove routing dependencies.
   const form=document.getElementById('tutorial-admin-form');document.body.append(form);
   const {setupTutorialEditor}=await import('/tutorial-editor.js?v=30');
   const topics=lessons.map(t=>({...structuredClone(t),revision:9}));topics[0]={...structuredClone(fixture),revision:9};
   window.fixtureActor='fixture-admin';window.savedPayload=null;window.draftCalls=[];window.draftOffline=false;
   const client={rpc:async(name,args)=>{
    if(name==='is_admin')return {data:true,error:null};
    if(name==='admin_tutorial_document')return {data:window.comparisonDocument||{current:{body:fixture,revision:9},draft:null},error:null};
    if(name==='admin_publish_tutorial_draft'){window.publishArgs=structuredClone(args);if(window.rejectPublish)return {error:Error('REVISION_CONFLICT')};return {data:{body:args.p_body,revision:13,draft:null}};}
    if(name==='admin_rebase_tutorial_draft'){window.rebaseArgs=structuredClone(args);if(window.deferRebase)return new Promise(resolve=>window.finishRebase=()=>resolve({data:{body:args.p_body,revision:9,base_revision:12}}));if(window.rejectRebase)return {error:Error('REVISION_CONFLICT')};return {data:{body:args.p_body,revision:8,base_revision:args.p_current_revision}};}
    if(name==='admin_save_tutorial_draft'){draftCalls.push(name);if(draftOffline)return {error:Error('offline')};window.savedPayload=structuredClone(args.p_body);return {data:{body:args.p_body,revision:1},error:null};}
    throw new Error('Unexpected RPC '+name);
   }};
   window.editor=setupTutorialEditor({topics:()=>topics,learning:()=>null,ready:()=>true,client:()=>client,user:()=>fixtureActor?({id:fixtureActor}):null,reload:()=>{},saved:()=>{}});
   await editor.accountChanged(true);
  }''')
  page.locator('#tutorial-admin-language').select_option('en')
  assert page.locator('#tutorial-admin-language').input_value()=='mn'
  assert 'Англи хувилбар' in page.locator('#tutorial-admin-message').inner_text()
  assert page.locator('#tutorial-admin-sections .block-rich-input').count()==2
  assert page.locator('#tutorial-admin-sections .block-code-input').count()==1
  page.locator('#tutorial-admin-title').fill('Preserved MN title edit')
  # Input autosaves without pressing the save button.
  page.wait_for_function('window.savedPayload !== null')
  assert page.evaluate('JSON.stringify(savedPayload.sections[0].blocks[0])===richBefore')
  assert page.evaluate('savedPayload.translations===undefined')
  assert page.evaluate('savedPayload.title')=='Preserved MN title edit'
  assert page.evaluate('savedPayload.id===fixture.id')
  report['legacy_editor_preserves_rich_and_mn_only']='PASS'
  page.locator('#tutorial-admin-sections .block-rich-input').last.fill('Rich edit through the real draft form')
  page.wait_for_function("savedPayload.sections[0].blocks.at(-1).content?.[0].text==='Rich edit through the real draft form'")
  assert page.evaluate("savedPayload.sections[0].blocks.at(-1).type")=='rich'
  report['rich_form_autosave']='PASS'
  page.evaluate('window.draftOffline=true')
  page.locator('#tutorial-admin-title').fill('Offline recoverable title')
  page.wait_for_function("document.querySelector('#tutorial-admin-message').textContent.includes('Онлайн хадгалалт амжилтгүй')")
  assert page.evaluate("JSON.parse(localStorage.getItem('erdene:tutorial-draft:v3:fixture-admin:'+fixture.id)).body.title")=='Offline recoverable title'
  page.evaluate('window.draftOffline=false')
  page.locator('#tutorial-admin-save').click()
  page.wait_for_function("savedPayload.title==='Offline recoverable title'")
  assert page.evaluate("draftCalls.every(name=>name==='admin_save_tutorial_draft')")
  report['autosave_offline_retry_private_rpc']='PASS'
  page.evaluate("()=>{window.comparisonDocument={current:{body:{...fixture,title:'Published latest'},revision:12},draft:{body:{...fixture,title:'Other tab draft'},revision:7,base_revision:9}};}")
  page.locator('#tutorial-compare-drafts').click()
  page.wait_for_selector('[data-rebase-choice="local"]',state='attached')
  assert page.locator('[data-rebase-save]').is_disabled()
  assert 'Other tab draft' in page.locator('[data-version="draft"]').text_content()
  page.locator('[data-version="local"] summary').click()
  for width,theme in [(375,'dark'),(1440,'light')]:
   page.set_viewport_size({'width':width,'height':1000})
   page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
   assert page.locator('#tutorial-draft-comparison').evaluate('(e)=>e.scrollWidth<=e.clientWidth')
   page.locator('#tutorial-draft-comparison').screenshot(path=str(ROOT/f'audit/browser/step-009-comparison-{width}.png'))
  page.locator('[data-rebase-choice="local"]').click()
  page.evaluate('window.rejectRebase=true')
  page.locator('[data-rebase-save]').click()
  page.wait_for_function("document.querySelector('#tutorial-draft-comparison [role=status]').textContent.includes('Харьцуулснаас хойш')")
  assert page.locator('[data-rebase-save]').is_disabled()
  page.locator('#tutorial-draft-comparison').get_by_role('button',name='Буцах',exact=True).click()
  page.evaluate('window.rejectRebase=false')
  page.locator('#tutorial-compare-drafts').click()
  page.locator('[data-version="draft"] summary').click()
  page.locator('[data-rebase-choice="draft"]').click()
  page.locator('[data-rebase-save]').click()
  page.wait_for_function("document.querySelector('#tutorial-admin-title').value==='Other tab draft'")
  assert page.evaluate('rebaseArgs.p_current_revision')==12
  assert page.evaluate('rebaseArgs.p_draft_revision')==7
  assert page.evaluate('rebaseArgs.p_actor')=='fixture-admin'
  assert page.evaluate("JSON.parse(localStorage.getItem('erdene:tutorial-draft:v3:fixture-admin:'+fixture.id+':before-rebase')).body.title")=='Offline recoverable title'
  assert page.evaluate("JSON.parse(localStorage.getItem('erdene:tutorial-draft:v3:fixture-admin:'+fixture.id)).draftRevision")==8
  assert page.locator('#tutorial-admin-title').is_enabled()
  report['explicit_rebase_stale_conflict_and_backup']='PASS'
  page.locator('#tutorial-publish-review').click()
  page.wait_for_selector('[data-publish-confirm]')
  assert page.evaluate('window.publishArgs') is None
  for width in [375,1440]:
   page.set_viewport_size({'width':width,'height':1000})
   assert page.locator('#tutorial-publication').evaluate('(e)=>e.scrollWidth<=e.clientWidth')
   page.locator('#tutorial-publication').screenshot(path=str(ROOT/f'audit/browser/step-009-publication-{width}.png'))

  page.evaluate('window.rejectPublish=true')
  page.locator('[data-publish-confirm]').click()
  page.wait_for_function("document.querySelector('#tutorial-publication [role=status]').textContent.includes('Хувилбар өөрчлөгджээ')")
  assert page.locator('[data-publish-confirm]').is_disabled()
  page.locator('#tutorial-publication').get_by_role('button',name='Буцах',exact=True).click()
  page.evaluate('window.rejectPublish=false')
  page.locator('#tutorial-publish-review').click()
  page.locator('[data-publish-confirm]').click()
  page.wait_for_function("document.querySelector('#tutorial-admin-message').textContent==='Хичээл нийтлэгдлээ.'")
  assert page.evaluate('publishArgs.p_body._draftRelationsText') is None
  assert page.evaluate('publishArgs.p_actor')=='fixture-admin'
  assert page.evaluate("JSON.parse(localStorage.getItem('erdene:tutorial-draft:v3:fixture-admin:'+fixture.id)).baseRevision")==13
  report['explicit_publish_confirmation_private_metadata_and_conflict']='PASS'

  page.evaluate('window.deferRebase=true')
  page.locator('#tutorial-compare-drafts').click()
  page.locator('[data-version="published"] summary').click()
  page.locator('[data-rebase-choice="published"]').click()
  page.locator('[data-rebase-save]').click()
  page.wait_for_function('typeof finishRebase === "function"')
  page.evaluate('async()=>{window.fixtureActor=null;await editor.accountChanged();finishRebase();}')
  assert page.locator('#tutorial-admin-form').is_hidden()
  assert page.locator('#tutorial-draft-comparison').is_hidden()
  assert page.locator('#tutorial-admin-title').input_value()=='Other tab draft'
  report['late_rebase_response_after_logout']='PASS'



  page.evaluate("""async()=>{
   const {mountBlockEditor}=await import('/tutorial-block-editor.js?v=30');
   const root=document.createElement('section');root.id='authoring-test';root.style.cssText='max-width:900px;margin:auto;padding:16px';document.body.append(root);
   window.authored=[{title:'Authoring fixture',blocks:[{type:'rich',key:'stable-key',metadata:{keep:true},content:[{text:'Select me',marks:[]}]}]}];
   window.authoring=mountBlockEditor(root,authored,{changed:()=>{window.authoringChanges=(window.authoringChanges||0)+1;}});
  }""")
  editable=page.locator('#authoring-test .block-rich-input').first
  editable.evaluate("e=>{const r=document.createRange();r.selectNodeContents(e);const s=getSelection();s.removeAllRanges();s.addRange(r);e.dispatchEvent(new MouseEvent('mouseup'));}")
  page.locator('#authoring-test').get_by_role('button',name='Bold',exact=True).click()
  assert page.evaluate("authored[0].blocks[0].content[0].marks.includes('bold')")
  assert page.evaluate('authored[0].blocks[0].metadata.keep')
  editable.evaluate("e=>{const d=new DataTransfer();d.setData('text/html','<img src=x onerror=window.pasteInjected=1>');d.setData('text/plain','<img src=x> plain text');e.dispatchEvent(new ClipboardEvent('paste',{clipboardData:d,bubbles:true,cancelable:true}));}")
  assert editable.locator('img').count()==0
  assert page.evaluate('window.pasteInjected') is None
  page.locator('#authoring-test').get_by_label('Нэмэх block төрөл').select_option('code')
  page.locator('#authoring-test').get_by_role('button',name='+ Block нэмэх',exact=True).click()
  assert page.evaluate('authored[0].blocks.length')==2
  page.locator('#authoring-test').get_by_role('button',name='↶ Undo',exact=True).click()
  assert page.evaluate('authored[0].blocks.length')==1
  page.locator('#authoring-test').get_by_role('button',name='↷ Redo',exact=True).click()
  assert page.evaluate('authored[0].blocks.length')==2
  page.locator('#authoring-test').get_by_role('button',name='Хэсэг хувилах',exact=True).click()
  assert page.evaluate('authored.length')==2
  page.locator('#authoring-test').get_by_role('button',name='↓ Хэсэг',exact=True).first.click()
  assert page.evaluate('authored.length')==2
  page.evaluate("async()=>{const {validateTutorial}=await import('/tutorial-model.js?v=30');validateTutorial({...original,sections:authored});}")
  assert page.locator('#authoring-test option[value=image]').count()==0
  page.locator('#authoring-test > details').first.evaluate('(e)=>e.open=true')
  page.wait_for_selector('#authoring-test .block-rich-input',state='visible')
  for width,theme in [(375,'light'),(1440,'dark')]:
   page.set_viewport_size({'width':width,'height':1000})
   page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
   assert page.locator('#authoring-test').evaluate('(e)=>e.scrollWidth<=e.clientWidth')
   page.locator('#authoring-test').screenshot(path=str(ROOT/f'audit/browser/step-009-authoring-{width}.png'))
  report['rich_authoring_paste_sections_undo_redo']='PASS'
  # Fresh real tutorial setup checks routine same-account notifications do not
  # rebuild the article or reset the reader's position.
  page.reload(wait_until='networkidle')
  page.evaluate('''async()=>{
   window.MathJax={startup:{promise:Promise.resolve()},typesetPromise:async()=>{},typesetClear:()=>{}};
   location.hash='#tutorial/complexity';
   const {setupTutorials}=await import('/tutorials.js?v=30');
   window.tutorialUI=setupTutorials({client:()=>null,user:()=>null,learning:()=>null});
  }''')
  page.wait_for_function("document.querySelector('#tutorial-content > section')!==null && document.querySelector('#tutorial-content').getAttribute('aria-busy')==='false'")
  page.evaluate('''()=>{
   window.beforeArticle=document.querySelector('#tutorial-content > section');
   window.scrollTo({top:250,behavior:'instant'});window.beforeScroll=window.scrollY;
   tutorialUI.accountChanged();tutorialUI.accountChanged();
  }''')
  page.evaluate('()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))')
  assert page.evaluate("beforeArticle===document.querySelector('#tutorial-content > section')")
  assert page.evaluate('window.scrollY===beforeScroll')
  report['same_account_preserves_reader_dom_and_scroll']='PASS'
  page.reload(wait_until='networkidle')
  page.evaluate("""async()=>{
   window.MathJax={startup:{promise:Promise.resolve()},typesetPromise:async()=>{},typesetClear:()=>{}};
   const {setupTutorials}=await import('/tutorials.js?v=30');
   window.serverReader=setupTutorials({client:()=>({rpc:async()=>({data:[],error:null})}),user:()=>null,learning:()=>null});
   await serverReader.connected();
  }""")
  page.wait_for_function("document.querySelector('#tutorial-count').textContent.startsWith('0 / 0')")
  assert page.locator('#tutorial-grid .tutorial-card').count()==0
  report['empty_online_catalog_does_not_restore_seed']='PASS'

  assert not errors,errors
  report['page_errors']=[]
  browser.close()
finally:server.shutdown()
(ROOT/'audit/STEP-009-BROWSER.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
