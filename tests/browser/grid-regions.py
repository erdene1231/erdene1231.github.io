"""Actual native block editor interactions and reader layouts; synthetic local data only."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}';results=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for width,theme in [(1280,'light'),(1280,'dark'),(390,'light'),(390,'dark')]:
   page=browser.new_page(viewport={'width':width,'height':900},has_touch=width<600);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   page.route('**/*',lambda r:r.abort() if not r.request.url.startswith(base) else r.fulfill(status=200,content_type='text/javascript',body='') if '/app.js?' in r.request.url or '/navigation.js?' in r.request.url else r.continue_());page.goto(base+'/index.html',wait_until='networkidle')
   page.evaluate('''async theme=>{document.documentElement.dataset.theme=theme;const{mountBlockEditor}=await import('/tutorial-block-editor.js?v=61');window.mount=mountBlockEditor;window.sections=[{key:'s',title:'Grid',blocks:[{key:'b',type:'diagram',kind:'dp',rows:[['A','A','B'],['C','D','B']],highlights:[],caption:'Domino'}]}];document.body.innerHTML='<main style="max-width:900px;margin:auto;padding:12px;min-width:0"><div id="fixture"></div><div id="reader"></div></main>';window.messages=[];window.editor=mount(document.querySelector('#fixture'),sections,{message:s=>messages.push(s),changed:()=>{}});}''',theme)
   def cell(r,c):return page.locator(f'.grid-controls td[data-grid-row="{r}"][data-grid-col="{c}"] button')
   cell(0,0).click();cell(0,1).click(modifiers=['Shift']);page.get_by_role('button',name='Нүд нэгтгэх',exact=True).click();assert page.locator('.grid-controls td[colspan="2"]').count()==1
   page.get_by_role('button',name='Хөх өнгө өгөх',exact=True).click();assert page.evaluate('sections[0].blocks[0].gridPresentation.colors.length')==2
   page.locator('[data-undo]').click();assert page.evaluate('sections[0].blocks[0].gridPresentation.colors===undefined');page.locator('[data-redo]').click()
   cell(0,0).click();page.get_by_role('button',name='Нэгтгэл салгах',exact=True).click();assert page.locator('.grid-controls td').count()==6
   cell(0,2).click();cell(1,2).click(modifiers=['Shift']);page.get_by_role('button',name='Нүд нэгтгэх',exact=True).click();assert page.locator('.grid-controls td[rowspan="2"]').count()==1
   # Custom color applies to the whole region, with contrasting text.
   cell(0,2).click();page.get_by_label('Нүдний өнгө',exact=True).fill('#000000');page.get_by_role('button',name='Өнгө өгөх',exact=True).click();assert cell(0,2).evaluate('(e)=>getComputedStyle(e).color')=='rgb(255, 255, 255)'
   # Existing merged region cannot be overlapped. No source strings are removed.
   cell(0,1).click();cell(0,2).click(modifiers=['Control']);cell(1,1).click(modifiers=['Control']);page.get_by_role('button',name='Нүд нэгтгэх',exact=True).click();assert 'давхцаж' in page.locator('.grid-selection-status').inner_text()
   page.get_by_role('button',name='Сонголт цэвэрлэх',exact=True).click();cell(0,0).click();page.get_by_role('button',name='Олон нүд',exact=True).click();cell(1,1).click();page.get_by_role('button',name='Олон нүд',exact=True).click();page.get_by_role('button',name='Нүд нэгтгэх',exact=True).click();assert 'тэгш өнцөгт' in page.locator('.grid-selection-status').inner_text()
   # Keyboard rectangular selection and mixed text visible.
   cell(1,0).click();cell(1,0).press('Shift+ArrowRight');page.get_by_role('button',name='Нүд нэгтгэх',exact=True).click();assert 'C · D' in page.locator('.grid-controls').inner_text()
   # Download and import are the actual editor controls.
   with page.expect_download() as info:page.get_by_role('button',name='Хүснэгтийн JSON татах',exact=True).click()
   downloaded=Path(info.value.path()).read_bytes();original=json.loads(downloaded);assert original['rows']==[['A','A','B'],['C','D','B']]
   page.get_by_label('Нүдтэй хүснэгтийн JSON оруулах',exact=True).set_input_files({'name':'grid.json','mimeType':'application/json','buffer':downloaded});page.wait_for_timeout(100)
   assert page.evaluate('JSON.stringify(sections[0].blocks[0].rows)')==json.dumps(original['rows'],separators=(',',':'))
   malformed={**original,'gridPresentation':{'colors':[{'row':0,'col':0,'color':'url(bad)'}]}}
   page.get_by_label('Нүдтэй хүснэгтийн JSON оруулах',exact=True).set_input_files({'name':'bad.json','mimeType':'application/json','buffer':json.dumps(malformed).encode()});page.wait_for_timeout(100);assert 'өнгө' in page.locator('.grid-selection-status').inner_text();assert page.evaluate('JSON.stringify(sections[0].blocks[0].gridPresentation)')==json.dumps(original['gridPresentation'],separators=(',',':'))
   # Serialize/reload and use the actual extended reader, retaining foreign content.
   outcome=page.evaluate('''async()=>{const{validateExtendedBlock}=await import('/tutorial-blocks.js?v=61'),{renderExtendedBlock}=await import('/tutorial-block-renderer.js?v=61');const b=JSON.parse(JSON.stringify(sections[0].blocks[0]));validateExtendedBlock(b);editor.destroy();sections[0].blocks[0]=b;editor=mount(document.querySelector('#fixture'),sections,{});const root=document.querySelector('#reader');root.className='tutorial-content';renderExtendedBlock(b,root);return {rows:b.rows,spans:root.querySelectorAll('td[rowspan="2"]').length,text:root.textContent};}''');assert outcome['spans']==1 and 'C · D' in outcome['text']
   # Native raw text edits cannot truncate a merge or silently replace saved rows.
   raw=page.get_by_label('Мөр бүр нэг row; нүдүүдийг | тэмдэгтээр тусгаарла',exact=True)
   raw.fill('A | A | B');assert not raw.evaluate('(e)=>e.checkValidity()');assert page.get_by_role('button',name='Хүснэгтийн JSON татах',exact=True).is_disabled()
   assert page.evaluate('sections[0].blocks[0].rows.length')==2
   raw.fill('A | A | B\nC | D | B');assert raw.evaluate('(e)=>e.checkValidity()')
   # Plain table has the same controls and native reader, header remains outside merges.
   extra=page.evaluate('''async()=>{const{renderBlock}=await import('/tutorials.js?v=61');editor.destroy();sections[0].blocks=[{key:'table',type:'table',headers:['X','Y'],rows:[['one','two'],['three','four']],custom:{keep:true}}];editor=mount(document.querySelector('#fixture'),sections,{});return true;}''')
   cell(0,0).click();cell(1,0).click(modifiers=['Shift']);page.get_by_role('button',name='Нүд нэгтгэх',exact=True).click()
   page.get_by_role('button',name='Шар өнгө өгөх',exact=True).click()
   plain=page.evaluate('''async()=>{const{renderBlock}=await import('/tutorials.js?v=61');const b=JSON.parse(JSON.stringify(sections[0].blocks[0]));const root=document.querySelector('#reader');root.replaceChildren();renderBlock(b,root);return {headers:[...root.querySelectorAll('th')].map(x=>x.textContent),text:root.textContent,span:root.querySelector('td').rowSpan,foreign:b.custom.keep,colors:b.gridPresentation.colors.length};}''');assert plain['span']==2 and plain['headers']==['X','Y'] and plain['foreign'] and plain['colors']==2 and 'one · three' in plain['text']
   page.screenshot(path=f'/tmp/grid-{width}-{theme}.png',full_page=True)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,theme,'page overflow')
   assert not errors,errors;results.append({'width':width,'theme':theme,'native_edit_merge_color_undo_import_reload_reader':True});page.close()
  browser.close()
finally:server.shutdown()
out={'status':'passed','cases':results,'scope':'Actual native components, local synthetic fixture; no live user changes'};(ROOT/'audit/GRID-BROWSER-RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
