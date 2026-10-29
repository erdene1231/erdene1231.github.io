"""Actual native editor/reader checks of the user's two source tiling grids; no live writes."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2];doc=json.loads((R/'audit/package03-lessons/dynamic-programming.json').read_text())['body']
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}';cases=[]
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for width,theme,lang in [(w,t,l)for w in[390,1200]for t in['light','dark']for l in['mn','en']]:
   page=b.new_page(viewport={'width':width,'height':950});page.route('**/*',lambda r:r.abort()if not r.request.url.startswith(base)else r.fulfill(status=200,content_type='text/javascript',body='')if '/app.js?'in r.request.url or'/navigation.js?'in r.request.url else r.continue_());page.goto(base+'/index.html',wait_until='networkidle')
   page.evaluate('''async p=>{document.documentElement.dataset.theme=p.theme;const{renderBlock}=await import('/tutorials.js?v=61'),{mountBlockEditor}=await import('/tutorial-block-editor.js?v=61');const d=p.lang==='mn'?p.doc:p.doc.translations.en;window.blocks=[d.sections[5].blocks[1],d.sections[5].blocks[3]];document.body.innerHTML='<main style="max-width:850px;margin:auto;padding:12px;min-width:0"><article class="tutorial-content" id="reader"></article><div id="editor"></div></main>';for(const b of blocks)renderBlock(b,document.querySelector('#reader'));window.sections=[{key:'tiling',title:'Domino',blocks:[structuredClone(blocks[0])]}];window.mount=mountBlockEditor;window.editor=mount(document.querySelector('#editor'),sections,{changed:()=>{}});}''',{'theme':theme,'lang':lang,'doc':doc})
   outcome=page.evaluate('''()=>{const grids=[...document.querySelectorAll('#reader .grid-presented')];return{cells:grids.map(g=>g.querySelectorAll('td').length),horizontal:grids[0].querySelectorAll('td[colspan="2"]').length,vertical:grids[0].querySelectorAll('td[rowspan="2"]').length,labels:[...grids[0].querySelectorAll('td')].map(e=>e.textContent).sort().join(''),hasBorders:[...grids[0].querySelectorAll('td')].every(e=>parseFloat(getComputedStyle(e).borderLeftWidth)>0),colors:[...new Set([...grids[0].querySelectorAll('td')].map(e=>getComputedStyle(e).backgroundColor))].length,overflow:document.documentElement.scrollWidth>innerWidth};}''')
   assert outcome['cells']==[14,28]and outcome['horizontal']==8 and outcome['vertical']==6 and outcome['labels']=='ABCDEFGHIJKLMN'and outcome['colors']==14 and outcome['hasBorders']and not outcome['overflow'],outcome
   # Unmerge and undo are actual editor buttons; underlying letters survive.
   page.locator('.grid-controls td[data-grid-row="0"][data-grid-col="0"] button').click();page.get_by_role('button',name='Нэгтгэл салгах',exact=True).click();assert page.locator('.grid-controls td').count()==15;page.locator('[data-undo]').click();assert page.locator('.grid-controls td').count()==14
   with page.expect_download()as download:page.get_by_role('button',name='Хүснэгтийн JSON татах',exact=True).click()
   raw=Path(download.value.path()).read_bytes();assert json.loads(raw)==page.evaluate('blocks[0]');page.get_by_label('Нүдтэй хүснэгтийн JSON оруулах',exact=True).set_input_files({'name':'domino.json','mimeType':'application/json','buffer':raw});page.wait_for_timeout(100)
   assert page.evaluate('JSON.stringify(sections[0].blocks[0])===JSON.stringify(blocks[0])')
   result=page.evaluate('''()=>{const saved=JSON.stringify(sections);editor.destroy();sections=JSON.parse(saved);editor=mount(document.querySelector('#editor'),sections,{changed:()=>{}});return JSON.stringify(sections[0].blocks[0])===JSON.stringify(blocks[0]);}''');assert result
   page.locator('#reader').screenshot(path=f'/tmp/domino-correction-{width}-{theme}-{lang}.png');cases.append({'width':width,'theme':theme,'lang':lang,'actual_editor_unmerge_undo_export_import_reload':True,**outcome});page.close()
  b.close()
finally:server.shutdown()
report={'status':'passed','cases':cases,'scope':'Actual native renderer and editor on exact public-candidate blocks; no live authenticated mutation or certificate bypass'};(R/'audit/PACKAGE03-DOMINO-NATIVE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'cases':len(cases),'status':'passed'}))
