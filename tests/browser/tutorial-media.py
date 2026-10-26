"""Real browser codecs/editor with mocked Storage/Auth. No live upload or user data."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'
report={}
preview_bytes=b''
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1200,'height':900});errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   if r.request.url in ['https://example.invalid/preview.webp','https://example.invalid/test.webp']:
    r.fulfill(status=200,content_type='image/webp',body=preview_bytes);return
   if not r.request.url.startswith(base):r.abort();return
   if '/app.js?' in r.request.url or '/navigation.js?' in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='');return
   r.continue_()
  page.route('**/*',route);page.goto(base+'/index.html',wait_until='networkidle')
  report.update(page.evaluate('''async()=>{
   const m=await import('/tutorial-media.js?v=31');window.media=m;
   const check=(v,s)=>{if(!v)throw Error(s);};const rejects=async(fn)=>{try{await fn();}catch{return;}throw Error('Expected rejection');};
   window.check=check;window.rejects=rejects;
   const canvas=document.createElement('canvas');canvas.width=3000;canvas.height=1500;canvas.getContext('2d').fillRect(0,0,3000,1500);
   for(const type of ['image/png','image/jpeg','image/webp']){
    const blob=await new Promise(r=>canvas.toBlob(r,type));const file=new File([blob],'fixture',{type});
    const prepared=await m.prepareTutorialImage(file);check(prepared.blob.type==='image/webp'&&prepared.width===2400&&prepared.height===1200,'codec dimensions');
    const decoded=await createImageBitmap(prepared.blob);check(decoded.width===2400,'decode output');decoded.close();window.file=file;
   }
   await rejects(()=>m.prepareTutorialImage(new File(['<svg onload=alert(1)>'],'x.svg',{type:'image/svg+xml'})));
   await rejects(()=>m.prepareTutorialImage(new File(['forged image/png'],'x.png',{type:'image/png'})));
   await rejects(()=>m.prepareTutorialImage(new File([new Uint8Array([137,80,78,71,13,10,26,10,0,0,0,0])],'broken.png',{type:'image/png'})));
   const realBitmap=window.createImageBitmap;let closed=false;
   window.createImageBitmap=async()=>({width:10000,height:10000,close(){closed=true;}});await rejects(()=>m.prepareTutorialImage(file));check(closed,'bitmap closed on oversize');window.createImageBitmap=realBitmap;
   window.actor='00000000-0000-0000-0000-000000000001';window.uploads=[];
   window.storage={from(bucket){check(bucket==='tutorial-media','bucket');return {
    async upload(path,blob,options){uploads.push({path,blob,options});return {error:null};},
    async createSignedUrl(path,seconds){check(seconds===60||seconds===600,'ttl');return {data:{signedUrl:'https://example.invalid/image.webp'},error:null};}
   };}};
   const uploaded=await m.uploadTutorialImage({storage},'test-lesson',file,actor);check(uploaded.path.startsWith('test-lesson/'+actor+'/')&&uploaded.pixelWidth===2400,'path/metadata');check(uploads[0].options.upsert===false&&uploads[0].blob.type==='image/webp','immutable webp');
   // Account changes while decoding must prevent dispatch, not merely discard a response.
   let finish;window.createImageBitmap=()=>new Promise(r=>finish=r);const pending=m.uploadTutorialImage({storage},'test-lesson',file,actor);
   while(!finish)await new Promise(r=>setTimeout(r,0));m.clearMediaCache();finish(await realBitmap(file));await rejects(()=>pending);check(uploads.length===1,'late decode sent no bytes');window.createImageBitmap=realBitmap;
   let end;const lateClient={storage:{from:()=>({upload:()=>new Promise(r=>end=r)})}};
   const inFlight=m.uploadTutorialImage(lateClient,'test-lesson',file,actor);while(!end)await new Promise(r=>setTimeout(r,0));m.clearMediaCache();end({error:null});await rejects(()=>inFlight);
   await rejects(()=>m.uploadTutorialImage({storage:{from:()=>({upload:async()=>({error:Error('Storage rejected')})})}},'test-lesson',file,actor));
   return {real_png_jpeg_webp_decode_resize_reencode:'PASS',forged_svg_corrupt_oversize_rejected:'PASS',late_decode_and_upload_after_account_change:'PASS',storage_error_does_not_return_path:'PASS'};
  }'''))
  preview_bytes=bytes(page.evaluate('async()=>Array.from(new Uint8Array(await file.arrayBuffer()))'))
  page.evaluate('''async()=>{
   for(const e of document.body.children)e.hidden=true;
   const {mountBlockEditor}=await import('/tutorial-block-editor.js?v=31');const root=document.createElement('section');root.id='media-editor';root.style.cssText='max-width:850px;margin:auto;padding:12px';document.body.append(root);
   window.sections=[{title:'Image authoring',blocks:[{type:'rich',content:[{text:'Paste image here',marks:[]}]}]}];window.pending=[];window.messages=[];
   window.blockEditor=mountBlockEditor(root,sections,{changed:()=>window.changes=(window.changes||0)+1,message:t=>messages.push(t),uploadImage:(file,current)=>{check(current(),'current block');return new Promise(r=>pending.push(r));},imageUrl:async()=> 'https://example.invalid/preview.webp'});
  }''')
  root=page.locator('#media-editor')
  root.get_by_label('Нэмэх block төрөл').select_option('image');root.get_by_role('button',name='+ Block нэмэх',exact=True).click()
  fake={'name':'test.png','mimeType':'image/png','buffer':b'fake bytes intercepted by mocked upload'}
  root.get_by_label('Tutorial зураг upload').set_input_files(fake)
  root.get_by_label('Tutorial зураг upload').set_input_files(fake)
  page.evaluate("()=>pending[1]({path:'test-lesson/'+actor+'/22222222-2222-2222-2222-222222222222.webp',pixelWidth:100,pixelHeight:50})")
  page.wait_for_function('sections[0].blocks[1].path.includes("22222222")')
  page.evaluate("()=>pending[0]({path:'old-response.webp'})")
  assert page.evaluate('sections[0].blocks[1].path.includes("22222222")')
  root.get_by_label('Alt text',exact=False).fill('Algorithm diagram');root.get_by_label('Caption',exact=True).fill('Figure 1')
  root.get_by_label('Байрлал',exact=False).select_option('right');root.get_by_label('Өргөн (%)',exact=True).fill('60')
  assert page.evaluate("sections[0].blocks[1].alt==='Algorithm diagram'&&sections[0].blocks[1].width===60&&sections[0].blocks[1].align==='right'")
  root.get_by_label('Tutorial зураг upload').set_input_files(fake)
  root.locator('.editor-block').last.get_by_role('button',name='Хасах',exact=True).click()
  page.evaluate("()=>pending[2]({path:'deleted-response.webp'})")
  assert page.evaluate('sections[0].blocks.length')==1
  root.locator('.block-rich-input').evaluate("e=>{const d=new DataTransfer();d.items.add(new File(['x'],'paste.png',{type:'image/png'}));e.dispatchEvent(new ClipboardEvent('paste',{clipboardData:d,cancelable:true,bubbles:true}));}")
  assert page.evaluate('sections[0].blocks[1].type')=='image'
  page.evaluate("()=>pending[3]({path:'test-lesson/'+actor+'/33333333-3333-3333-3333-333333333333.webp',pixelWidth:300,pixelHeight:200})")
  page.wait_for_function('sections[0].blocks[1].path.includes("33333333")')
  root.locator('.editor-image-drop').evaluate("e=>{const d=new DataTransfer();d.items.add(new File(['x'],'drop.png',{type:'image/png'}));e.dispatchEvent(new DragEvent('drop',{dataTransfer:d,cancelable:true,bubbles:true}));}")
  assert page.evaluate('pending.length')==5
  page.evaluate("()=>pending[4]({path:'test-lesson/'+actor+'/44444444-4444-4444-4444-444444444444.webp',pixelWidth:300,pixelHeight:200})")
  page.wait_for_function('sections[0].blocks[1].path.includes("44444444")')
  assert root.locator('img.editor-image-preview').count()==1
  page.wait_for_function("document.querySelector('#media-editor img').naturalWidth>0")
  for width,theme in [(375,'light'),(1200,'dark')]:
   page.set_viewport_size({'width':width,'height':900});page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
   assert root.evaluate('e=>e.scrollWidth<=e.clientWidth')
   root.screenshot(path=str(ROOT/f'audit/browser/editor-fix-media-{width}.png'))
  report['picker_paste_drop_metadata_preview_and_stale_block_responses']='PASS'
  # Use the actual editor adapter and draft autosave with real image conversion.
  page.reload(wait_until='networkidle')
  page.evaluate('''async()=>{
   window.MathJax={startup:{promise:Promise.resolve()},typesetPromise:async()=>{},typesetClear:()=>{}};
   const {setupTutorialEditor}=await import('/tutorial-editor.js?v=31');window.actor='00000000-0000-0000-0000-000000000001';
   window.lesson=structuredClone((await (await fetch('/tutorials.json')).json()).tutorials[0]);delete lesson.translations;lesson.sections=[{title:'Upload fixture',blocks:[{type:'p',text:'Example'}]}];window.savedBody=null;window.didUpload=false;
   const client={storage:{from:()=>({upload:async(path,blob,options)=>{if(blob.type!=='image/webp'||options.upsert!==false)throw Error('bad upload');window.didUpload=true;return {error:null};},createSignedUrl:async()=>({data:{signedUrl:'https://example.invalid/test.webp'}})})},rpc:async(name,args)=>{
    if(name==='is_admin')return {data:true};if(name==='admin_tutorial_document')return {data:{current:{body:lesson,revision:7},draft:null}};
    if(name==='admin_save_tutorial_draft'){window.savedBody=structuredClone(args.p_body);return {data:{body:args.p_body,revision:args.p_draft_revision+1,base_revision:7}};}throw Error('Unexpected RPC '+name);
   }};
   window.editor=setupTutorialEditor({client:()=>client,user:()=>actor?{id:actor}:null,topics:()=>[lesson],learning:()=>null,ready:()=>true,saved:()=>{}});await editor.accountChanged();
  }''')
  # Existing enclosing sections can be hidden by the app shell; reveal only ancestors.
  page.locator('#tutorial-admin-form').evaluate("e=>{for(let p=e;p;p=p.parentElement){p.hidden=false;if(p.tagName==='DETAILS')p.open=true;} }")
  form=page.locator('#tutorial-admin-form')
  form.get_by_label('Нэмэх block төрөл').select_option('image');form.get_by_role('button',name='+ Block нэмэх',exact=True).click()
  png=page.evaluate("async()=>{const c=document.createElement('canvas');c.width=20;c.height=10;return Array.from(new Uint8Array(await (await new Promise(r=>c.toBlob(r,'image/png'))).arrayBuffer()));}")
  form.get_by_label('Tutorial зураг upload').set_input_files({'name':'real.png','mimeType':'image/png','buffer':bytes(png)})
  page.wait_for_function('window.didUpload===true')
  page.wait_for_function("document.querySelector('#tutorial-admin-message').textContent.includes('Зураг upload хийгдлээ')")
  form.get_by_label('Alt text',exact=False).fill('Real upload fixture')
  page.wait_for_function("savedBody?.sections[0].blocks[1]?.path?.endsWith('.webp')&&savedBody.sections[0].blocks[1].alt==='Real upload fixture'")
  assert page.evaluate('savedBody.sections[0].blocks[1].pixelWidth')==20
  page.evaluate('async()=>{window.actor=null;await editor.accountChanged();}')
  assert form.is_hidden()
  report['actual_editor_upload_to_private_autosave_and_logout']='PASS'
  assert not errors,errors
  report['page_errors']=[];browser.close()
finally:server.shutdown()
(ROOT/'audit/EDITOR-FIX-REGRESSION-MEDIA-BROWSER.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
