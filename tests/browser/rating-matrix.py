"""Actual list/detail/picker rating colors, 100-step boundaries, both themes."""
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
bands = ['newbie']*4 + ['pupil']*2 + ['specialist']*2 + ['expert']*3 + ['candidate-master']*2 + ['master']*3 + ['grandmaster']*6 + ['legendary']*11 + ['unrated']
values = list(range(800, 4001, 100)) + [None]
palette = {
    'light': ['#4b5563','#166534','#075e70','#1e40af','#86198f','#9a4200','#a11b2c','#111827'],
    'dark': ['#d1d5db','#a1edba','#95e8f2','#b6c8ff','#f0b0fa','#ffd1a0','#ffb8c1','#ffffff'],
}
band_names = ['newbie','pupil','specialist','expert','candidate-master','master','grandmaster','legendary']
pool = [dict(id=f'matrix-{i}', number=i+1, title=f'Matrix {i}', source='Codeforces', ref=f'1/A{i}', url=f'https://codeforces.com/contest/1/problem/A{i}', rating=value, ratingKind='unrated' if value is None else 'official' if i%2==0 else 'estimated', tags=['math'], priority=False, hints=[], hintsEn=[]) for i, value in enumerate(values)]
report = {}
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        page = browser.new_page(viewport={'width':1200, 'height':950}); errors=[]
        page.on('pageerror', lambda e: errors.append(str(e)))
        def route(r):
            if not r.request.url.startswith(base): r.abort()
            elif '/config.js' in r.request.url: r.fulfill(status=200, content_type='text/javascript', body='window.THINK_CP_CONFIG={};')
            elif '/problems.json' in r.request.url: r.fulfill(status=200, content_type='application/json', body=json.dumps({'problems':pool}))
            else: r.continue_()
        page.route('**/*', route)
        page.add_init_script('window.MathJax={startup:{promise:Promise.resolve()},typesetClear:()=>{},typesetPromise:async()=>{}};')
        page.goto(base+'/index.html#library', wait_until='networkidle')
        page.wait_for_selector('#problems .rating'); assert page.locator('#problems .problem').count()==34
        for theme in ['light', 'dark']:
            page.evaluate('(t)=>document.documentElement.dataset.theme=t', theme)
            colors = []
            for i, band in enumerate(bands):
                row = page.locator('#problems .problem').filter(has=page.get_by_role('heading', name=f'Matrix {i}', exact=True))
                badge = row.locator('.rating'); assert 'rating-'+band in badge.get_attribute('class')
                label = badge.inner_text()
                assert label=='Unrated' if values[i] is None else ('≈' in label)==(pool[i]['ratingKind']=='estimated')
                color = badge.evaluate('(e)=>{const s=getComputedStyle(e);return [s.color,s.backgroundColor]}'); colors.append(color)
                if band != 'unrated':
                    value = palette[theme][band_names.index(band)]
                    rgb = tuple(int(value[j:j+2], 16) for j in [1,3,5])
                    assert color[0]=='rgb(%d, %d, %d)' % rgb, (theme, band, color)
                if theme=='dark' and band=='legendary': assert color[1]=='rgb(8, 11, 16)'
                row.locator('.open').click()
                detail = page.locator('#detail-note .rating')
                assert detail.inner_text()==label and 'rating-'+band in detail.get_attribute('class')
                assert detail.evaluate('(e)=>{const s=getComputedStyle(e);return [s.color,s.backgroundColor]}')==color
                page.locator('[data-close=detail]').click()
            page.evaluate('''async(pool)=>{const {openProblemSelection}=await import('/problem-selection-dialog.js?v=42');openProblemSelection({problems:()=>pool,onSelect:()=>{}})}''', pool)
            picker = page.locator('[data-selection-available] .rating'); assert picker.count()==34
            for i, band in enumerate(bands):
                badge = picker.nth(i); assert 'rating-'+band in badge.get_attribute('class')
                assert badge.evaluate('(e)=>{const s=getComputedStyle(e);return [s.color,s.backgroundColor]}')==colors[i]
            contrast = picker.evaluate_all(r'''els=>{const lum=c=>{const a=c.match(/[\d.]+/g).slice(0,3).map(Number).map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4});return a[0]*.2126+a[1]*.7152+a[2]*.0722};return els.map(e=>{const s=getComputedStyle(e),a=lum(s.color),b=lum(s.backgroundColor);return (Math.max(a,b)+.05)/(Math.min(a,b)+.05)})}''')
            assert min(contrast)>=4.5, (theme, min(contrast))
            report[theme]={'values_checked':34, 'surfaces':['list','detail','shared picker'], 'minimum_text_contrast':min(contrast), 'status':'passed'}
            page.get_by_role('button', name='Болих', exact=True).click()
        assert not errors, errors
        browser.close()
finally:
    server.shutdown()
(ROOT/'audit/PART04-RATING-MATRIX.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report))
