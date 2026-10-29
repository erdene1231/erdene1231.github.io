import argparse,functools,http.server,json,threading,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser();parser.add_argument('--candidate',type=Path,action='append');parser.add_argument('--report',default='audit/PACKAGE02-REWRITE-BROWSER.json');args=parser.parse_args()
docs=[json.loads(p.read_text())['body']for p in args.candidate]if args.candidate else[json.loads((ROOT/'audit/package02-rewrite'/f'{id}.json').read_text())['body']for id in ['binary-search','greedy','dynamic-programming']]
rows=[r for r in json.loads((ROOT/'audit/PART04-BASELINE.json').read_text())['tutorials'] if r['id']!='mongolia']
for row in rows:
 for doc in docs:
  if row['body']['id']==doc['id']:row['body']=doc
problems=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import{proposalProblems}from'./tools/package02_tutorial_proposals.mjs';console.log(JSON.stringify(proposalProblems()))"],cwd=ROOT,text=True))
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}';cases=[]
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);errors=[]
  for width,mobile,theme in [(375,True,'light'),(393,True,'dark'),(980,True,'light'),(1200,False,'dark')]:
   page=b.new_page(viewport={'width':width,'height':950},is_mobile=mobile,has_touch=mobile);page.on('pageerror',lambda e:errors.append(str(e)))
   page.route('**/*',lambda r:r.abort()if not r.request.url.startswith(base)else r.fulfill(status=200,content_type='text/javascript',body='')if '/app.js?'in r.request.url or'/navigation.js?'in r.request.url else r.continue_())
   page.goto(base+'/index.html#tutorial/'+docs[0]['id'],wait_until='networkidle')
   page.evaluate('''async payload=>{const{setupTutorials}=await import('/tutorials.js?v=56');const{setupLearning}=await import('/learning.js?v=56');const section=document.getElementById('tutorial-reader').closest('section');for(const e of document.querySelectorAll('main>section'))e.hidden=e!==section;section.hidden=false;document.documentElement.dataset.theme=payload.theme;window.p02Learning=await setupLearning({client:()=>null,user:()=>null,isAdmin:()=>false,problems:()=>payload.problems,progress:()=>({}),openProblem:p=>{window.p02LastOpened=p.id}});window.p02TopicIds=new Set(payload.rows.map(r=>r.body.id));const ctx={client:()=>({rpc:async name=>{if(name==='get_tutorials')return{data:payload.rows};throw Error('Unexpected RPC '+name)}}),user:()=>null,learning:()=>p02Learning,isAdmin:()=>false};window.app=setupTutorials(ctx);await app.connected();}''',{'rows':rows,'problems':problems,'theme':theme})
   for doc in docs:
    for lang in ['mn','en']:
     page.evaluate('(id)=>location.hash="#tutorial/"+id',doc['id']);page.select_option('#tutorial-language',lang)
     page.wait_for_function("p=>document.getElementById('tutorial-content').getAttribute('aria-busy')==='false'&&document.getElementById('tutorial-content').lang===p.lang&&document.querySelector('#tutorial-content>section')?.id==='tutorial-'+p.id+'-0'",arg={'lang':lang,'id':doc['id']})
     result=page.evaluate('''()=>{const a=document.getElementById('tutorial-content'),panel=document.getElementById('tutorial-contents-panel'),g=document.querySelector('.tutorial-reading-layout'),cards=[...document.querySelectorAll('#tutorial-learning-extras .learning-problem[data-problem-id]')];let openedAll=true;for(const card of cards){card.querySelector('button')?.click();openedAll&&=p02LastOpened===card.dataset.problemId;}return{sections:a.querySelectorAll(':scope>section').length,math:a.querySelectorAll('mjx-container').length,mathErrors:a.querySelectorAll('mjx-merror,[data-mjx-error],mjx-mtext[data-mjx-error]').length,unknownMath:[...a.querySelectorAll('mjx-mtext')].filter(x=>x.textContent.includes('\\\\le')).length,code:a.querySelectorAll('pre code.language-cpp').length,practice:cards.length,openedAll,overflow:document.documentElement.scrollWidth>innerWidth,articleWidth:a.getBoundingClientRect().width,grid:getComputedStyle(g).gridTemplateColumns,contentsOpen:panel.open,toc:document.querySelectorAll('#tutorial-toc a').length,legacyDemo:a.querySelectorAll('.algorithm-demo').length}}''')
     assert result['sections']==len(doc['sections']) and result['toc']==len(doc['sections']),result
     assert result['math']>0 and result['mathErrors']==0,result
     expected_code=sum(1 for section in doc['sections'] for block in section['blocks'] if block.get('type')=='code' and block.get('language','').lower() in ['c++','c++17','cpp'])
     assert expected_code>=5 and result['code']==expected_code and result['practice']>=6 and result['openedAll'],result
     assert not result['overflow'],result
     if mobile:assert result['articleWidth']>=width-70 and not result['contentsOpen'],result
     cases.append({'lesson':doc['id'],'lang':lang,'width':width,'mobile':mobile,'theme':theme,**result})
     if lang=='mn':
      page.screenshot(path=f'/tmp/p02-rewrite-{doc["id"]}-{width}.png',full_page=False)
      if not page.locator('#tutorial-contents-panel').evaluate('(e)=>e.open'):page.locator('#tutorial-contents-panel summary').click()
      target=min(7,len(doc['sections'])-1)
      page.locator('#tutorial-toc a').nth(target).click()
      page.wait_for_function("p=>location.hash.endsWith('/part/'+p)",arg=target)
      if width in [375,1200]:page.screenshot(path=f'/tmp/p02-rewrite-code-{doc["id"]}-{width}.png')
      if mobile:assert not page.locator('#tutorial-contents-panel').evaluate('(e)=>e.open')
      page.locator('#tutorial-reading-mode').select_option('step')
      assert page.locator('#tutorial-content>section:visible').count()==1
      page.locator('#tutorial-reading-mode').select_option('full')
   if width==393:
    page.evaluate("document.documentElement.style.fontSize='125%'")
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   if width!=1200:page.close()
  page.evaluate("()=>{window.fixture=document.createElement('article');fixture.className='tutorial-content';document.getElementById('tutorial-content').replaceChildren(fixture)}")
  roundtrips=[]
  for doc in docs:
   result=page.evaluate('''async doc=>{const{validateTutorial}=await import('/tutorial-model.js?v=52'),{mountBlockEditor}=await import('/tutorial-block-editor.js?v=52'),{drawArticle,typeset}=await import('/tutorials.js?v=56');const copy=structuredClone(doc);copy.fixtureLegacyMetadata={opaque:'preserve-only',array:[1,2]};copy.sections[0].blocks[0].fixtureLegacyMetadata={keep:true};const image={type:'image',path:doc.id+'/00000000-0000-0000-0000-000000000001/11111111-1111-1111-1111-111111111111.webp',alt:'Round-trip fixture only',width:50,align:'center',detailKey:'fixture-image'};const practice={type:'problem',problemKey:'939',detailKey:'fixture-practice'};copy.sections[copy.sections.length-2].blocks.push(image,practice);validateTutorial(copy);const keep=structuredClone(copy);const editor=document.createElement('div');fixture.replaceChildren(editor);let changed=0;const mounted=mountBlockEditor(editor,copy.sections,{changed:()=>changed++,locked:()=>false,imageUrl:async()=>{throw Error('No live media requested in round-trip fixture')}});const input=editor.querySelector('.block-rich-input');input.textContent+=' Нэмэлт $n$ / extra $n$.';input.dispatchEvent(new Event('input',{bubbles:true}));const saved=JSON.stringify(copy);mounted.destroy();const loaded=JSON.parse(saved);validateTutorial(loaded);const reload=mountBlockEditor(editor,loaded.sections,{changed:()=>{},locked:()=>false,imageUrl:async()=>{throw Error('No live media')}});reload.destroy();const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);if(!same(loaded.fixtureLegacyMetadata,keep.fixtureLegacyMetadata)||!same(loaded.sections[0].blocks[0].fixtureLegacyMetadata,keep.sections[0].blocks[0].fixtureLegacyMetadata))throw Error('Legacy metadata lost');for(const k of['id','aliases','related','prerequisiteIds','prerequisites','learningRelations'])if(!same(loaded[k],keep[k]))throw Error('Identity/relationships lost:'+k);if(!same(loaded.translations,keep.translations))throw Error('Unedited translation lost');if(!same(loaded.sections[loaded.sections.length-2],keep.sections[keep.sections.length-2]))throw Error('Image/practice reference lost');for(const sec of[7,loaded.sections.length-3,loaded.sections.length-1])if(!same(loaded.sections[sec],keep.sections[sec]))throw Error('Code fragment/program changed');const article=document.createElement('article');article.className='tutorial-content';fixture.replaceChildren(article);await typeset([article],()=>drawArticle(loaded,article,'mn',{learning:window.p02Learning}));return{lesson:doc.id,edited:changed>0,roundtrip:true,math:article.querySelectorAll('mjx-container').length,mathErrors:article.querySelectorAll('mjx-merror,[data-mjx-error]').length};}''',doc)
   assert result['edited']and result['roundtrip']and result['math']>0 and result['mathErrors']==0;roundtrips.append(result)
  assert not errors,errors
  b.close()
finally:server.shutdown()
report={'status':'passed','full_reader_cases':cases,'native_editor_roundtrips':roundtrips,'production_writes':0,'scope':'Actual setupTutorials reader/TOC/learning and native block editor; local candidate bodies and read-only RPC fixtures. Not live publication or user acceptance.'}
(ROOT/args.report).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'cases':len(cases),'roundtrips':len(roundtrips),'status':'passed'}))
