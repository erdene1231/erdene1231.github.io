import functools,http.server,threading,json
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2]
class Q(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Q,directory=str(R)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}';cases=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(accept_downloads=True)
 page.route('**/*',lambda x:x.abort()if not x.request.url.startswith(base)or'/app.js?'in x.request.url else x.continue_());page.goto(base+'/index.html',wait_until='networkidle')
 page.evaluate('''async()=>{const{mountBlockEditor}=await import('/tutorial-block-editor.js?v=57');window.block={key:'stable-block',type:'diagram',kind:'graph',nodes:[{id:'a',label:'A',x:25,y:50,color:'#ccddaa',annotation:'size=4',annotationColor:'#112233',annotationDx:14,annotationDy:-40},{id:'b',label:'B',x:75,y:50}],edges:[['a','b']],edgeStyles:[{label:'12',color:'#aa4455',labelDx:4,labelDy:-8}],directed:true,customLegacy:{keep:42}};window.sections=[{key:'g',title:'Graph',blocks:[block]}];const root=document.createElement('div');root.style.maxWidth='calc(100vw - 60px)';root.style.margin='auto';document.body.replaceChildren(root);window.editor=mountBlockEditor(root,sections,{changed:()=>{},locked:()=>false});root.querySelector('.graph-controls').open=true;}''')
 page.get_by_label('Чиглэлтэй',exact=True).uncheck();assert not page.evaluate('block.directed')
 page.get_by_label('Чиглэлтэй',exact=True).check();assert page.evaluate('block.directed')
 for width in [375,1100]:
  page.set_viewport_size({'width':width,'height':900});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');page.screenshot(path=f'/tmp/graph-editor-{width}.png')
 page.screenshot(path='/tmp/graph-editor-desktop.png')
 with page.expect_download()as download:page.get_by_role('button',name='Граф JSON татах').click()
 exported=json.loads(Path(download.value.path()).read_text());assert exported==page.evaluate('block');cases.append('actual native download preserves full structured graph')
 payload={**exported,'key':'foreign-key','kind':'tree'};payload['nodes'][0]['annotation']='distance=9';payload['nodes'][0]['label']='<img src=x onerror=alert(1)>'
 def upload(x):page.get_by_label('Граф JSON оруулах').set_input_files({'name':'graph.json','mimeType':'application/json','buffer':json.dumps(x).encode()})
 upload(payload);page.wait_for_function("block.kind==='tree'&&block.nodes[0].annotation==='distance=9'")
 assert page.evaluate("block.key==='stable-block'&&block.customLegacy.keep===42");cases.append('import edits content but retains block identity and unknown metadata')
 page.locator('.graph-controls').evaluate('(e)=>e.open=true');before=page.evaluate('JSON.stringify(block)');bad=json.loads(json.dumps(payload));bad['nodes'][0]['color']='url(javascript:alert(1))';upload(bad);page.wait_for_function("document.querySelector('.graph-controls [role=status]').textContent.length>0");assert page.evaluate('JSON.stringify(block)')==before;cases.append('unsafe colors rejected without modifying graph')
 page.get_by_label('Граф JSON оруулах').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{invalid'});page.wait_for_timeout(50);assert page.evaluate('JSON.stringify(block)')==before;cases.append('malformed JSON leaves graph intact')
 page.get_by_label('Граф JSON оруулах').set_input_files({'name':'large.json','mimeType':'application/json','buffer':b' '*100001});page.wait_for_function("document.querySelector('.graph-controls [role=status]').textContent.includes('100KB')");assert page.evaluate('JSON.stringify(block)')==before;cases.append('oversized import leaves graph intact')
 # Topology edits keep per-node attributes and edge styles attached by endpoint identity.
 topology=json.loads(json.dumps(payload));topology['nodes'].append({'id':'c','label':'C','x':50,'y':75});topology['edges']=[['a','b'],['b','c']];topology['edgeStyles']=[{'label':'12','color':'#aa4455'},{'label':'34','color':'#2233aa'}];upload(topology);page.wait_for_function("block.nodes.length===3")
 nodes=page.locator('label').filter(has_text='Орой бүр:').locator('textarea');nodes.fill('a | A | 30 | 50\nb | B | 75 | 50\nc | C | 50 | 75');nodes.press('Tab');assert page.evaluate("block.nodes[0].annotation==='distance=9'&&block.nodes[0].x===30&&block.nodes[0].color==='#ccddaa'");cases.append('manual node rows retain annotations, colors and metadata')
 edges=page.locator('label').filter(has_text='Ирмэг бүр:').locator('textarea');edges.fill('b c\na b');edges.press('Tab');assert page.evaluate("block.edgeStyles[0].label==='34'&&block.edgeStyles[1].label==='12'");cases.append('edge reorder preserves styles by endpoint identity')
 page.get_by_role('button',name='↶ Undo',exact=True).click();assert page.evaluate("block===sections[0].blocks[0]")is False
 # Undo replaces the block snapshot; inspect the actual active section rather than an old object reference.
 assert page.evaluate("sections[0].blocks[0].edges[0][0]==='a'&&sections[0].blocks[0].edgeStyles[0].label==='12'");cases.append('topology edit undo restores the complete styled graph')
 # Restore fixture reference after native undo, which deliberately replaces section objects.
 page.evaluate('window.block=sections[0].blocks[0]')
 # Prototype-like unknown JSON keys remain data, never object prototype mutations.
 payload['__proto__']={'polluted':True};upload(payload);page.wait_for_timeout(80);assert page.evaluate("Object.getPrototypeOf(block)===Object.prototype&&!({}).polluted");cases.append('prototype-like metadata cannot alter object prototypes')
 page.locator('.graph-controls').evaluate('(e)=>e.open=true');page.locator('fieldset').filter(has=page.locator('legend').get_by_text('Орой a',exact=True)).locator('.graph-color').first.get_by_role('button').click();assert page.evaluate("!Object.hasOwn(block.nodes[0],'color')&&block.nodes[0].annotation==='distance=9'");cases.append('automatic theme color reset preserves annotation data')
 page.locator('.graph-controls').evaluate('(e)=>e.open=true');page.get_by_label('Чиглэлтэй',exact=True).uncheck();edges=page.locator('label').filter(has_text='Ирмэг бүр:').locator('textarea');edges.fill('b a');edges.press('Tab');assert page.evaluate("block.edgeStyles[0].label==='12'");cases.append('undirected endpoint reversal retains the same edge style')
 page.evaluate('''async()=>{const{renderExtendedBlock}=await import('/tutorial-block-renderer.js?v=57');editor.destroy();const a=document.createElement('article');a.className='tutorial-content';document.body.replaceChildren(a);renderExtendedBlock(JSON.parse(JSON.stringify(block)),a);if(a.querySelector('img,script'))throw Error('Label parsed as HTML');}''');cases.append('HTML-looking labels render as literal text')
 b.close()
s.shutdown();(R/'audit/GRAPH-TRANSFER-BROWSER.json').write_text(json.dumps({'status':'passed','cases':cases,'production_writes':0},indent=2)+'\n');print(json.dumps(cases))
