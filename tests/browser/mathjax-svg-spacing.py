"""Real published Geometry + real MathJax: measure glyph spacing, not just SVG count.
No private/authenticated transport. --payload-dir contains fresh public RPC responses.
"""
import argparse, functools, http.server, json, pathlib, threading, urllib.request
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument('--payload-dir', required=True)
ap.add_argument('--output-dir', required=True)
a = ap.parse_args()
R = pathlib.Path(__file__).resolve().parents[2]
P, W = pathlib.Path(a.payload_dir), pathlib.Path(a.output_dir)
W.mkdir(parents=True, exist_ok=True)
raw = {n: (P / (n + '.json')).read_bytes() for n in ['get_catalog', 'get_tutorials']}
geometry = next(x['body'] for x in json.loads(raw['get_tutorials']) if x['body']['id'] == 'geometry')
formulas = [x['tex'] for x in geometry['sections'][3]['blocks'] if x['type'] == 'math']
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(R)))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}'
cache, results = {}, []
# Last two subscripts in both reported identities are x_{i+1} and y_i.
# Compare actual glyph extents after all SVG transforms, including nested maction.
measure = '''e => {
 const svg=e.querySelector('mjx-container[jax="SVG"]');
 const subs=[...e.querySelectorAll(svg?'g[data-mml-node="msub"]':'mjx-msub')];
 const [x,y]=subs.slice(-2);
 const right=x.getBoundingClientRect().right;
 const base=y.querySelector(svg?'g[data-mml-node="mi"]':'mjx-mi');
 return {gap:base.getBoundingClientRect().left-right, renderer:svg?'SVG':'CHTML'};
}'''
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        cases = [('unfixed', 'SVG', 1400, 'light', 1), ('default', 'SVG', 1400, 'light', 1)]
        cases += [(f'{renderer}-{width}-{theme}', renderer, width, theme, 1.2 if theme == 'dark' else 1)
                  for renderer in ['SVG', 'CHTML'] for width in [393, 1400] for theme in ['light', 'dark']]
        for name, renderer, width, theme, scale in cases:
            settings = json.dumps({} if name == 'default' else {'renderer': renderer, 'collapsible': True, 'explorer': True, 'scale': scale})
            page = browser.new_page(viewport={'width': width, 'height': 950}, device_scale_factor=2 if width == 393 else 1,
                                    is_mobile=width == 393, has_touch=width == 393)
            page.add_init_script('localStorage.setItem("MathJax-Menu-Settings",' + json.dumps(settings) + ');')
            failures, errors = [], []
            page.on('pageerror', lambda e: errors.append(str(e)))
            def route(r):
                u = r.request.url
                if u.startswith(base):
                    if name == 'unfixed' and '/mathjax-loader.js' in u:
                        return r.fulfill(content_type='text/javascript', body=(R / 'mathjax-loader.js').read_text().replace('fixSvgTogglePlacement(win.MathJax);', '/* reproduce unpatched vendor */'))
                    return r.continue_()
                for n in raw:
                    if u.endswith('/rpc/' + n):
                        return r.fulfill(content_type='application/json', body=raw[n])
                if u.startswith('https://cdn.jsdelivr.net/') and 'mathjax' not in u:
                    if u not in cache: cache[u] = urllib.request.urlopen(u, timeout=30).read()
                    return r.fulfill(content_type='text/javascript', body=cache[u])
                if '/rpc/get_leaderboard' not in u: failures.append(u)
                return r.abort()
            page.route('**/*', route)
            page.goto(base + '/#tutorial/geometry', wait_until='domcontentloaded')
            page.wait_for_function('document.querySelectorAll("#tutorial-content mjx-container").length>20 && document.querySelector("#tutorial-content").getAttribute("aria-busy")==="false"')
            page.evaluate('(theme)=>document.documentElement.dataset.theme=theme', theme)
            page.evaluate('document.fonts.ready')
            section = page.locator('#tutorial-content section').nth(3)
            math = section.locator('.tutorial-math')
            gaps = [math.nth(i).evaluate(measure)['gap'] for i in [0, 2]]
            math.nth(0).screenshot(path=str(W / (name + '-shoelace.png')))
            math.nth(2).screenshot(path=str(W / (name + '-trapezoid.png')))
            section.locator('p').first.screenshot(path=str(W / (name + '-inline.png')))
            if name == 'unfixed':
                assert max(gaps) < -1, gaps
                results.append({'case': name, 'glyphGapsPx': gaps})
                page.close()
                continue
            assert min(gaps) >= (0.01 if renderer == 'SVG' else 0), (name, gaps)
            inline_clearance = section.locator('p').first.locator('mjx-container').first.evaluate('''e=>{
              const ink=e.querySelector('svg>g')||e.querySelector('mjx-math');
              return e.getBoundingClientRect().right-ink.getBoundingClientRect().right;
            }''')
            assert inline_clearance >= 0, (name, inline_clearance)
            assert page.locator('#tutorial-content mjx-merror').count() == 0
            if width == 393:
                display = math.nth(0).locator('mjx-container')
                assert display.evaluate('e=>e.scrollWidth>e.clientWidth')
                display.evaluate('e=>e.scrollLeft=e.scrollWidth')
                assert display.evaluate('e=>e.scrollLeft>0')
                math.nth(0).screenshot(path=str(W / (name + '-scroll-end.png')))
            # Render identical source math through native renderBlock in the preview surface.
            page.evaluate('''async tex=>{const {renderBlock,typeset}=await import('./tutorials.js?v=101');
              const e=document.createElement('div');e.id='spacing-preview';e.className='tutorial-content';document.body.append(e);
              for(const t of tex)renderBlock({type:'math',tex:t},e,'mn');
              for(const language of ['Input','Output'])renderBlock({type:'code',language,text:'$n$\\n1  2\\n'},e,'mn');
              await typeset([e]);}''', [formulas[0], formulas[2]])
            preview_gaps = [e.evaluate(measure)['gap'] for e in page.locator('#spacing-preview .tutorial-math').all()]
            assert min(preview_gaps) >= (0.01 if renderer == 'SVG' else 0), preview_gaps
            assert page.locator('#spacing-preview code').all_text_contents() == ['$n$\n1  2\n'] * 2
            assert page.locator('#spacing-preview pre mjx-container').count() == 0
            # Collapse/expand still works; repeated render and output switches must retain spacing.
            if renderer == 'SVG':
                action = math.nth(0).locator('g[data-mml-node="maction"][data-toggle]').first
                page.evaluate('''e=>e.dispatchEvent(new MouseEvent('click',{bubbles:true}))''', action.element_handle())
                page.wait_for_function('document.querySelector(`#tutorial-content section:nth-of-type(4) g[data-toggle="1"]`)')
                action = math.nth(0).locator('g[data-toggle="1"]').first
                page.evaluate('''e=>e.dispatchEvent(new MouseEvent('click',{bubbles:true}))''', action.element_handle())
                assert math.nth(0).evaluate(measure)['gap'] > 0
            page.locator('#tutorial-language').select_option('en')
            page.wait_for_function('document.querySelector("#tutorial-content").lang==="en" && document.querySelectorAll("#tutorial-content mjx-container").length>20 && document.querySelector("#tutorial-content").getAttribute("aria-busy")==="false"')
            assert page.locator('#tutorial-content section').nth(3).locator('.tutorial-math').first.evaluate(measure)['gap'] >= (0.01 if renderer == 'SVG' else 0)
            page.evaluate('location.hash="#tutorial/complexity"')
            page.wait_for_function('document.querySelector("#tutorial-complexity-0") && document.querySelectorAll("#tutorial-content mjx-container").length>20 && document.querySelector("#tutorial-content").getAttribute("aria-busy")==="false"')
            page.evaluate('location.hash="#tutorial/geometry"')
            page.wait_for_function('document.querySelector("#tutorial-geometry-0") && document.querySelectorAll("#tutorial-content mjx-container").length>20 && document.querySelector("#tutorial-content").getAttribute("aria-busy")==="false"')
            assert page.locator('#tutorial-content section').nth(3).locator('.tutorial-math').first.evaluate(measure)['gap'] >= (0.01 if renderer == 'SVG' else 0)
            assert page.evaluate('localStorage.getItem("MathJax-Menu-Settings")') == settings
            assert page.locator('script[src*="vendor/mathjax/tex-svg.js"]').count() == 1
            if name == 'CHTML-1400-dark':
                page.evaluate('MathJax.startup.document.menu.setRenderer("SVG")')
                page.wait_for_function('document.querySelectorAll("#tutorial-content mjx-container[jax=SVG]").length>20')
                assert page.locator('#tutorial-content section').nth(3).locator('.tutorial-math').first.evaluate(measure)['gap'] >= (0.01 if renderer == 'SVG' else 0)
            assert not failures, failures
            assert not errors, errors
            results.append({'case': name, 'glyphGapsPx': gaps, 'previewGapsPx': preview_gaps, 'inlineClearancePx': inline_clearance,
                            'MN_EN_navigation_plainIO_preferences': True})
            print('passed ' + name, flush=True)
            page.close()
        browser.close()
finally:
    server.shutdown()
(W / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results))
