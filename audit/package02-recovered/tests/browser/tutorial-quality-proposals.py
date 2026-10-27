"""Render guarded local tutorial proposals in the actual editor/reader/MathJax."""
import functools,http.server,json,os,subprocess,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
data=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import fs from'node:fs';import{proposedTutorialRows}from'./tools/part04_tutorial_proposals.mjs';const ids=new Set(JSON.parse(fs.readFileSync('audit/PART04-TUTORIAL-QUALITY-PATCH01.json')).patches.map(p=>p.id));process.stdout.write(JSON.stringify(proposedTutorialRows(JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials).filter(p=>ids.has(p.body.id)).map(p=>p.body)));"],cwd=ROOT,text=True))
if os.environ.get('TUTORIAL_REVIEW_IDS'):
 selected=set(os.environ['TUTORIAL_REVIEW_IDS'].split(','));data=[d for d in data if d['id']in selected];assert {d['id']for d in data}==selected
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}';checks=[]
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   if not r.request.url.startswith(base):r.abort()
   elif '/app.js?'in r.request.url or '/navigation.js?'in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='')
   else:r.continue_()
  page.route('**/*',route);page.goto(base+'/index.html',wait_until='networkidle');page.evaluate("for(const e of document.body.children)e.hidden=true;window.fixture=document.createElement('div');fixture.style.cssText='max-width:1100px;margin:auto;padding:16px';document.body.append(fixture)")
  for doc in data:
   for lang in ['mn','en']:
    for width,theme in [(375,'light'),(1200,'dark')]:
     page.set_viewport_size({'width':width,'height':950});page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
     result=page.evaluate('''async({doc,lang})=>{
      const{validateTutorial,view}=await import('./tutorial-model.js?v=48'),{mountBlockEditor}=await import('./tutorial-block-editor.js?v=48'),{drawArticle,typeset}=await import('./tutorials.js?v=48');validateTutorial(doc);const before=JSON.stringify(doc),editorRoot=document.createElement('div'),article=document.createElement('article');article.className='tutorial-content';fixture.replaceChildren(editorRoot,article);const editor=mountBlockEditor(editorRoot,view(doc,lang).sections,{changed:()=>{}});editor.destroy();editorRoot.remove();if(JSON.stringify(doc)!==before)throw Error('Editor modified untouched source');
      await typeset([article],()=>drawArticle(doc,article,lang));const expected=view(doc,lang).sections.flatMap(s=>s.blocks.filter(b=>b.type==='code'&&b.language==='C++17').map(b=>b.text));const actual=[...article.querySelectorAll('pre code.language-cpp')].map(e=>e.textContent);return{codeExact:JSON.stringify(expected)===JSON.stringify(actual),inlineMath:article.querySelectorAll('p mjx-container').length,mathErrors:article.querySelectorAll('mjx-merror,[data-mjx-error]').length,inlineCodeMath:article.querySelectorAll('p code mjx-container').length,sections:article.querySelectorAll(':scope>section').length};
     }''',{'doc':doc,'lang':lang})
     assert result['codeExact']and result['inlineMath']>0 and result['mathErrors']==0 and result['inlineCodeMath']==0,result
     assert result['sections']==len((doc if lang=='mn'else doc['translations']['en'])['sections'])
     assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(doc['id'],lang,width)
     checks.append({'id':doc['id'],'lang':lang,'width':width,'theme':theme,'status':'passed','code_preserved':True,'inline_math_nodes':result['inlineMath']})
  assert not errors,errors;browser.close()
finally:s.shutdown()
report={'status':'passed','local_proposals_only':True,'tutorials':len(data),'render_combinations':len(checks),'checks':checks,'limits':'No production edit/publication, actual bundled MathJax/editor/renderer with no external services.'};(ROOT/'audit'/os.environ.get('TUTORIAL_REVIEW_REPORT','PART04-TUTORIAL-QUALITY-BROWSER.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='checks'}))
