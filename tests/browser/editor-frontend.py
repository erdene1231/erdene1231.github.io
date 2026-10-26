"""Real Chromium block editor regressions; synthetic content, no database/network credentials."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}';report={}
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1200,'height':950});errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   if not r.request.url.startswith(base):r.abort();return
   if '/app.js?' in r.request.url or '/navigation.js?' in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='');return
   r.continue_()
  page.route('**/*',route);page.goto(base+'/index.html',wait_until='networkidle')
  page.evaluate('''async()=>{
   const {mountBlockEditor}=await import('/tutorial-block-editor.js?v=40');
   for(const e of document.body.children)e.hidden=true;
   const form=document.createElement('form');form.id='fixture';form.style.cssText='max-width:1000px;margin:auto;padding:16px';document.body.append(form);
   window.submits=0;form.onsubmit=e=>{e.preventDefault();submits++};window.root=document.createElement('div');form.append(root);
   window.mount=(sections)=>{window.editor?.destroy();window.sections=sections;window.locked=false;window.messages=[];window.editor=mountBlockEditor(root,sections,{locked:()=>locked,message:t=>messages.push(t),changed:()=>{}})};
   mount([{title:'Last section',blocks:[]}]);
  }''')
  root=page.locator('#fixture')
  root.get_by_role('button',name='Хэсэг хасах',exact=True).click(timeout=1500)
  assert page.evaluate('sections.length')==0
  root.get_by_role('button',name='↶ Undo',exact=True).click();assert page.evaluate('sections.length')==1
  root.get_by_role('button',name='↷ Redo',exact=True).click();assert page.evaluate('sections.length')==0
  report['last_section_delete_undo_redo']='PASS'
  root.get_by_role('button',name='+ Шинэ хэсэг',exact=True).click()
  assert root.locator('.editor-section[open]').count()==1
  root.get_by_label('Нэмэх block төрөл').select_option('rich');root.get_by_role('button',name='+ Block нэмэх',exact=True).click()
  editable=root.get_by_role('textbox',name='Formatting бүхий тайлбар');editable.fill('Alpha beta')
  page.evaluate('''()=>{const e=document.querySelector('.block-rich-input'),r=document.createRange();r.setStart(e.firstChild,0);r.setEnd(e.firstChild,5);getSelection().removeAllRanges();getSelection().addRange(r);document.dispatchEvent(new Event('selectionchange'));}''')
  root.get_by_role('button',name='Bold',exact=True).click()
  assert page.evaluate("sections[0].blocks[0].content.some(r=>r.text==='Alpha'&&r.marks.includes('bold'))")
  link=root.get_by_role('textbox',name='Текстийн холбоос');link.fill('https://example.com');link.press('Enter')
  assert page.evaluate('submits')==0
  assert page.evaluate("sections[0].blocks[0].content.some(r=>r.href==='https://example.com/')")
  report['formatting_and_link_enter_does_not_submit_form']='PASS'
  for label,mark in [('Italic','italic'),('Underline','underline'),('Strike','strike'),('Inline code','code')]:
   page.evaluate("()=>mount([{title:'Formatting',blocks:[{type:'rich',content:[{text:'Plain selection',marks:[]}]}]}])")
   page.evaluate('''()=>{const e=document.querySelector('.block-rich-input'),r=document.createRange();r.selectNodeContents(e);getSelection().removeAllRanges();getSelection().addRange(r);document.dispatchEvent(new Event('selectionchange'));}''')
   root.get_by_role('button',name=label,exact=True).click()
   assert page.evaluate('(mark)=>sections[0].blocks[0].content.every(r=>r.marks.includes(mark))',mark),(mark,page.evaluate('sections[0].blocks[0].content'),editable.inner_html())
  report['italic_underline_strike_inline_code']='PASS'
  page.evaluate("()=>{mount([{title:'Open',blocks:[]},{title:'Closed',blocks:[{type:'rich',content:[{text:'Locked',marks:[]}]}]}]);locked=true;editor.refreshControls()}")
  root.locator('.editor-section').nth(1).locator('summary').click()
  assert root.locator('.editor-section').nth(1).get_by_label('Хэсгийн гарчиг',exact=True).is_disabled()
  assert root.locator('.editor-section').nth(1).locator('.block-rich-input').get_attribute('contenteditable')=='false'
  report['opening_section_during_lock_cannot_enable_inputs']='PASS'
  page.evaluate("()=>mount(Array.from({length:80},(_,i)=>({title:'Section '+i,blocks:[]})))")
  assert root.get_by_role('button',name='+ Шинэ хэсэг',exact=True).is_disabled()
  assert root.get_by_role('button',name='Хэсэг хувилах',exact=True).first.is_disabled()
  page.evaluate("()=>mount([{title:'Full section',blocks:Array.from({length:100},()=>({type:'divider'}))}])")
  assert root.get_by_role('button',name='+ Block нэмэх',exact=True).is_disabled()
  assert root.get_by_role('button',name='Хувилах',exact=True).first.is_disabled()
  page.evaluate('()=>{locked=true;editor.refreshControls()}')
  assert root.get_by_label('Нэмэх block төрөл').is_disabled()
  page.evaluate('()=>{locked=false;editor.refreshControls()}')
  assert root.get_by_role('button',name='+ Block нэмэх',exact=True).is_disabled()
  report['section_block_limits_and_lock_restore']='PASS'
  page.evaluate("()=>mount([{title:'Table',blocks:[{type:'table',headers:['A'],rows:Array.from({length:100},()=>['value'])}]}])")
  assert root.get_by_role('button',name='+ Мөр',exact=True).is_disabled()
  page.evaluate("()=>mount([{title:'A',blocks:[{type:'rich',content:[{text:'Formatting content',marks:[]}]}]}])")
  for width in [375,1200]:
   page.set_viewport_size({'width':width,'height':950})
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   root.screenshot(path=str(ROOT/f'audit/browser/part01-editor-{width}.png'))
  assert not errors,errors
  report['table_limit_responsive_no_runtime_errors']='PASS';browser.close()
finally:server.shutdown()
(ROOT/'audit/PART01-EDITOR-FRONTEND-BROWSER.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
