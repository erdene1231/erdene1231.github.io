"""Edit/serialize/reload each actual English section document, preserving Mongolian and code."""
import argparse,functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];parser=argparse.ArgumentParser();parser.add_argument('candidates',nargs='+',type=Path);parser.add_argument('--report',required=True);args=parser.parse_args();docs=[json.loads(p.read_text())['body']for p in args.candidates]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}';results=[]
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.route('**/*',lambda r:r.abort()if not r.request.url.startswith(base)else r.fulfill(status=200,content_type='text/javascript',body='')if '/app.js?'in r.request.url or'/navigation.js?'in r.request.url else r.continue_());page.goto(base+'/index.html',wait_until='networkidle')
  for doc in docs:
   result=page.evaluate('''async doc=>{const{mountBlockEditor}=await import('/tutorial-block-editor.js?v=52'),{validateTutorial}=await import('/tutorial-model.js?v=52'),{drawArticle,typeset}=await import('/tutorials.js?v=52');const copy=structuredClone(doc),keep=structuredClone(copy),root=document.createElement('div');document.body.replaceChildren(root);let changes=0;const mounted=mountBlockEditor(root,copy.translations.en.sections,{changed:()=>changes++,locked:()=>false});const input=root.querySelector('.block-rich-input');input.textContent+=' Editor round-trip $n$.';input.dispatchEvent(new Event('input',{bubbles:true}));const serialized=JSON.stringify(copy);mounted.destroy();const loaded=JSON.parse(serialized);validateTutorial(loaded);if(JSON.stringify(loaded.sections)!==JSON.stringify(keep.sections))throw Error('Mongolian content changed');for(const k of['id','aliases','related','prerequisiteIds','learningRelations'])if(JSON.stringify(loaded[k])!==JSON.stringify(keep[k]))throw Error('Identity/relationship changed:'+k);for(const s of[7,12,14])if(JSON.stringify(loaded.translations.en.sections[s])!==JSON.stringify(keep.translations.en.sections[s]))throw Error('Unedited English code/practice/checklist changed');const reload=mountBlockEditor(root,loaded.translations.en.sections,{changed:()=>{},locked:()=>false});reload.destroy();const article=document.createElement('article');article.className='tutorial-content';root.replaceChildren(article);await typeset([article],()=>drawArticle(loaded,article,'en'));return{lesson:doc.id,language:'en',changed:changes>0,mongolian_preserved:true,code_and_relationships_preserved:true,math:article.querySelectorAll('mjx-container').length,math_errors:article.querySelectorAll('mjx-merror,[data-mjx-error]').length};}''',doc)
   assert result['changed']and result['math']>0 and result['math_errors']==0;results.append(result)
  assert not errors,errors;b.close()
finally:server.shutdown()
report={'status':'passed','cases':results,'scope':'Actual native English block editor and serializer/reload/renderer, local fixtures; no production or real-account writes'};(ROOT/args.report).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
