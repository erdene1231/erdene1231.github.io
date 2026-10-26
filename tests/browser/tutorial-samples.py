"""Reader sample layout and exact clipboard behavior in Chromium; no remote access."""
import functools
import http.server
import json
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}'
report = {}
try:
 with sync_playwright() as p:
  browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
  page = browser.new_page(viewport={'width':1200,'height':900})
  errors = []
  page.on('pageerror', lambda e: errors.append(str(e)))
  def route(r):
   if not r.request.url.startswith(base): r.abort(); return
   if '/app.js?' in r.request.url or '/navigation.js?' in r.request.url:
    r.fulfill(status=200, content_type='text/javascript', body=''); return
   r.continue_()
  page.route('**/*', route)
  page.goto(base+'/index.html', wait_until='networkidle')
  page.evaluate('''async()=>{
   const {drawArticle,renderBlock}=await import('/tutorials.js?v=33');
   window.drawArticle=drawArticle;window.renderBlock=renderBlock;
   window.lessons=(await (await fetch('/tutorials.json')).json()).tutorials;
   window.fixture={...structuredClone(lessons[0]),translations:undefined,sections:[{
    title:'13. Бүтэн program ба жишээ input, output',blocks:[
     {type:'p',text:'Input: n, q, array, дараа q ширхэг l, r. Index 0-оос эхэлнэ; хоёр зах орно.'},
     {type:'code',language:'Input',text:'5 3\\n2 -1 4 0 3\\n1 3\\n0 4\\n2 2\\n'},
     {type:'code',language:'Output',text:'3\\n8\\n4\\n'}
   ]}]};
   window.target=document.createElement('article');target.id='sample-preview';target.className='tutorial-content';target.style.cssText='max-width:980px;min-width:0;margin:20px auto;padding:16px';
   for(const child of document.body.children)child.hidden=true;
   document.body.append(target);drawArticle(fixture,target,'mn');
   window.copied=[];window.copyFail=false;
   Object.defineProperty(navigator,'clipboard',{value:{writeText:async text=>{if(copyFail)throw Error('permission denied');copied.push(text);}},configurable:true});
  }''')
  assert page.locator('.tutorial-samples').count() == 1
  assert page.locator('.sample-input pre code').text_content() == '5 3\n2 -1 4 0 3\n1 3\n0 4\n2 2\n'
  assert page.locator('.sample-output pre code').text_content() == '3\n8\n4\n'
  page.get_by_role('button', name='Input хуулах').click()
  page.wait_for_function('copied.length===1')
  assert page.evaluate('copied[0]===fixture.sections[0].blocks[1].text')
  assert page.locator('.sample-input [role=status]').inner_text() == 'Input хуулагдлаа.'
  page.get_by_role('button', name='Output хуулах').click()
  page.wait_for_function('copied.length===2')
  assert page.evaluate('copied[1]===fixture.sections[0].blocks[2].text')
  report['exact_sample_text_and_copy_preserve_trailing_newlines'] = 'PASS'
  page.evaluate('window.copyFail=true')
  page.get_by_role('button', name='Input хуулах').click()
  page.wait_for_function("document.querySelector('.sample-input [role=status]').textContent.includes('Хуулах боломжгүй')")
  assert page.evaluate('copied.length') == 2
  assert page.get_by_role('button', name='Input хуулах').inner_text() == 'Хуулах'
  report['copy_failure_is_visible_and_does_not_report_success'] = 'PASS'
  page.evaluate("drawArticle(fixture,target,'mn')")
  for width,theme in [(1200,'light'),(375,'light'),(1200,'dark'),(375,'dark')]:
   page.set_viewport_size({'width':width,'height':900})
   page.evaluate('(theme)=>document.documentElement.dataset.theme=theme',theme)
   assert page.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth'), (width,theme)
   boxes=page.locator('.tutorial-sample-panel').all()
   first,second=[box.bounding_box() for box in boxes]
   if width>700: assert abs(first['y']-second['y'])<1 and second['x']>first['x'], (width,theme)
   else: assert second['y']>=first['y']+first['height'], (width,theme)
   assert page.locator('.sample-input pre').get_attribute('tabindex') == '0'
   assert page.locator('.sample-input pre').evaluate("e=>parseFloat(getComputedStyle(e).lineHeight)") < 25
   # Dark/light both provide a readable, explicit foreground/background contrast.
   contrast=page.locator('.tutorial-sample-panel').first.evaluate('''e=>{
    const lum=value=>{const rgb=value.match(/[\\d.]+/g).slice(0,3).map(x=>{x=Number(x)/255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4;});return rgb[0]*.2126+rgb[1]*.7152+rgb[2]*.0722;};
    const style=getComputedStyle(e),a=lum(style.backgroundColor),b=lum(style.color);return (Math.max(a,b)+.05)/(Math.min(a,b)+.05);
   }''')
   assert contrast>=4.5, (theme,contrast)
   page.locator('#sample-preview').screenshot(path=str(ROOT/f'audit/browser/tutorial-samples-{width}-{theme}.png'))
  report['responsive_pair_layout_and_both_theme_contrast'] = 'PASS'
  page.evaluate('''()=>{
   window.literal='  <img src=x onerror="window.injected=true">\\t  \\n\\nend\\n';
   target.replaceChildren();renderBlock({type:'code',language:'Input',text:literal},target,'en');
  }''')
  assert page.locator('.tutorial-sample-panel img').count() == 0
  assert page.locator('.tutorial-sample-panel code').text_content() == page.evaluate('literal')
  page.evaluate('window.copyFail=false')
  page.get_by_role('button', name='Copy Input', exact=True).click()
  page.wait_for_function('copied.length===3')
  assert page.evaluate('copied[2]===literal')
  page.evaluate("renderBlock({type:'code',language:'Output',text:'A'.repeat(300)},target,'en')")
  assert page.locator('.sample-output pre').evaluate('e=>e.scrollWidth>e.clientWidth')
  assert page.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth')
  report['standalone_sample_keeps_tabs_spaces_blanklines_and_escapes_markup'] = 'PASS'
  page.evaluate('''()=>{
   const checks=[];
   for(const lesson of lessons){
    const before=JSON.stringify(lesson);
    for(const lang of ['mn','en']){
     const version=lang==='en'&&lesson.translations?.en?lesson.translations.en:lesson;
     drawArticle(lesson,target,lang);
     const expected=version.sections.flatMap(s=>s.blocks).filter(b=>b.type==='code').map(b=>b.text);
     const actual=[...target.querySelectorAll('.tutorial-code pre code,.tutorial-sample-panel pre code')].map(e=>e.textContent);
     checks.push(JSON.stringify(expected)===JSON.stringify(actual));
    }
    checks.push(before===JSON.stringify(lesson));
   }
   window.contentPreserved=checks.every(Boolean);
  }''')
  assert page.evaluate('contentPreserved')
  assert not errors, errors
  report['all_55_tutorials_both_languages_keep_code_order_and_content'] = 'PASS'
  browser.close()
finally: server.shutdown()
(ROOT/'audit/TUTORIAL-SAMPLES-BROWSER.json').write_text(json.dumps({'checks':report},indent=2)+'\n')
print(json.dumps(report))
