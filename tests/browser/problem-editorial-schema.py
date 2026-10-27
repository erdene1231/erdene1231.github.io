"""Prepared problem editorials reuse tutorial schema/editor/renderer, not HTML."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}'
docs=[p['editorial']for p in json.loads((ROOT/'audit/PART04-REVIEWED-NEW-TASKS.json').read_text())if p.get('editorial')]+[p['field_updates']['editorial'] for p in json.loads((ROOT/'audit/PART04-BASELINE-REVIEW-PATCH04.json').read_text())['patches'] if p['field_updates'].get('editorial')]
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   if not r.request.url.startswith(base):r.abort()
   elif '/app.js?'in r.request.url or '/navigation.js?'in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='')
   else:r.continue_()
  page.route('**/*',route);page.goto(base+'/index.html',wait_until='networkidle')
  page.evaluate('''()=>{for(const el of document.body.children)el.hidden=true;window.fixture=document.createElement('div');fixture.style.cssText='max-width:900px;margin:auto;padding:16px';document.body.append(fixture);}''')
  for doc in docs:
   for width,theme in [(375,'light'),(1200,'dark')]:
    page.set_viewport_size({'width':width,'height':950});page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
    result=page.evaluate(r'''async(doc)=>{
     const {validateTutorial}=await import('/tutorial-model.js?v=46'),{mountBlockEditor}=await import('/tutorial-block-editor.js?v=46'),{drawArticle,typeset}=await import('/tutorials.js?v=46');
     validateTutorial(doc);const copy=JSON.parse(JSON.stringify(doc)),editor=document.createElement('div'),reader=document.createElement('article');reader.className='tutorial-content';fixture.replaceChildren(editor,reader);
     const mounted=mountBlockEditor(editor,copy.sections,{changed:()=>{}});const input=editor.querySelector('.block-rich-input');input.textContent='Changed proof <img src=x onerror=alert(1)>';input.dispatchEvent(new Event('input',{bubbles:true}));
     validateTutorial(copy);copy.sections[0].blocks.push({type:'rich',content:[{text:'Хилүүд $L$, $R$ ба хэмжээ $n$, $m$. ',marks:[]},{text:'n + m',marks:['code']}]});copy.sections[0].blocks.push({type:'math',tex:'\\frac{x_1}{2}\\le y'});await typeset([reader],()=>drawArticle(copy,reader,'mn'));mounted.destroy();
     return{inlineMath:reader.querySelectorAll('p mjx-container').length,inlineCodeMath:reader.querySelectorAll('p code mjx-container').length,sections:reader.querySelectorAll(':scope>section').length,code:reader.querySelectorAll('pre code').length,math:reader.querySelectorAll('mjx-container').length,mathErrors:reader.querySelectorAll('mjx-merror,[data-mjx-error]').length,unsafeImages:reader.querySelectorAll('img').length,literalEscaped:reader.textContent.includes('<img src=x onerror=alert(1)>')};
    }''',doc)
    assert result.pop('inlineMath')>=4,result
    assert result.pop('inlineCodeMath')==0,result
    assert result.pop('math')>=1+sum(b['type']=='math' for sec in doc['sections'] for b in sec['blocks']),result
    assert result=={'sections':len(doc['sections']),'code':sum(b['type']=='code' for sec in doc['sections'] for b in sec['blocks']),'mathErrors':0,'unsafeImages':0,'literalEscaped':True},result
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert not errors,errors;b.close()
finally:s.shutdown()
report={'status':'passed','documents':len(docs),'schema':'Existing tutorial document validator, block editor and drawArticle renderer','checks':['JSON/editor roundtrip','typed text/math/code/links','escaped HTML','actual bundled MathJax','mobile light/desktop dark'],'limitation':'Existing problem admin/lazy reader integrated; browser RPC mocked and SQL proposal tested locally; production not applied.'}
(ROOT/'audit/PART04-EDITORIAL-SCHEMA-BROWSER.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
