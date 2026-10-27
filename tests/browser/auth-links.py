"""Email-link UI uses mocked Auth only: never sends emails or creates accounts."""
import functools,http.server,json,re,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}'
html=re.sub(r'<script\b[^>]*>.*?</script>','',(ROOT/'index.html').read_text(),flags=re.S)
checks=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for width,theme in [(375,'light'),(1200,'dark')]:
   page=browser.new_page(viewport={'width':width,'height':900});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   def route(r):
    if not r.request.url.startswith(base):r.abort()
    elif '/index.html' in r.request.url:r.fulfill(status=200,content_type='text/html',body=html)
    else:r.continue_()
   page.route('**/*',route);page.goto(base+'/index.html#home')
   page.evaluate('''async(theme)=>{document.documentElement.dataset.theme=theme;window.calls=[];window.actor='user-a';window.clock=Date.now();Date.now=()=>clock;window.client={auth:{resetPasswordForEmail:async(email,options)=>{calls.push({email,options});return {};},getUser:async()=>({data:{user:{id:actor}}}),updateUser:async()=>{calls.push({updated:true});return {};}}};const {setupSocial}=await import('./social.js?v=44');window.social=setupSocial({client:()=>client,user:()=>null,problems:()=>[],notice:()=>{}});}''',theme)
   page.evaluate("document.querySelector('#forgot-password').hidden=false;document.querySelector('#auth').showModal()")
   page.locator('#forgot-password').click();page.locator('#recovery-email').fill('local-test@example.invalid');page.locator('#send-recovery-link').click()
   assert page.locator('#recovery-link-panel').is_visible();assert page.locator('#recovery-code').count()==0;assert page.locator('#recovery-password-form').is_hidden()
   assert 'холбоос' in page.locator('#recovery-message').inner_text();assert page.evaluate('calls.length')==1
   page.locator('#resend-recovery-link').click();assert page.evaluate('calls.length')==1;assert 'минут' in page.locator('#recovery-message').inner_text()
   page.evaluate('clock+=61000');page.locator('#resend-recovery-link').click();assert page.evaluate('calls.length')==2
   assert page.evaluate('calls[0].options.redirectTo')==base+'/index.html'
   page.locator('#change-recovery-email').click();assert page.locator('#recovery-email-form').is_visible()
   page.evaluate("social.authEvent('SIGNED_IN',{user:{id:'user-a'}})");assert page.locator('#recovery-password-form').is_hidden()
   page.evaluate("social.authEvent('PASSWORD_RECOVERY',{user:{id:'user-a'}})");assert page.locator('#recovery-password-form').is_visible()
   page.locator('#recovery-password').fill('test-only-password');page.locator('#recovery-confirm').fill('different-password');page.locator('#save-recovery-password').click();assert 'ижил' in page.locator('#recovery-message').inner_text();assert page.evaluate('calls.length')==2
   page.locator('#recovery-confirm').fill('test-only-password');page.evaluate("actor='user-b'");page.locator('#save-recovery-password').click();assert 'солигдсон' in page.locator('#recovery-message').inner_text();assert page.evaluate('calls.length')==2
   page.evaluate("actor='user-a'");page.locator('#save-recovery-password').click();assert 'шинэчлэгдлээ' in page.locator('#recovery-message').inner_text();assert page.evaluate('calls.length')==3
   assert page.locator('#recovery-password').input_value()==''
   page.locator('[data-close=recovery]').evaluate('e=>e.closest("dialog").close()')
   page.evaluate("document.querySelector('#forgot-password').click()");page.evaluate("social.authEvent('PASSWORD_RECOVERY',{user:{id:'user-a'}})");page.locator('#recovery-password').fill('test-only-password');page.evaluate("document.querySelector('#recovery').close()");page.wait_for_timeout(50);assert page.locator('#recovery-password').input_value()==''
   assert not errors,errors;checks.append(f'{width}/{theme}: request/resend/wait/back/callback/mismatch/account-switch/save/close');page.close()
  page=browser.new_page();page.route('**/*',route);page.goto(base+'/index.html#error=access_denied&error_code=otp_expired&error_description=untrusted-text')
  page.evaluate("async()=>{const {setupSocial}=await import('./social.js?v=44');setupSocial({client:()=>null,user:()=>null,notice:()=>{}})}")
  assert page.locator('#auth').is_visible();assert 'хугацаа' in page.locator('#auth-feedback').inner_text();assert 'untrusted-text' not in page.locator('#auth-feedback').inner_text();assert 'error' not in page.url
  checks.append('invalid/expired callback shows generic instruction and removes provider error parameters')
  page=browser.new_page();page.add_init_script("""window.signupCalls=[];window.testClient={auth:{onAuthStateChange:(cb)=>window.authCallback=cb,getSession:async()=>({data:{session:null}}),signUp:async(body)=>{signupCalls.push({email:body.email,redirect:body.options.emailRedirectTo});return {data:{user:{id:'signup-fixture'},session:null}};}},rpc:async(name)=>({data:name==='get_catalog'?{problems:[],knownIds:[]}:name==='is_admin'?false:[]}),from:()=>({select:()=>({eq:async()=>({data:[]})})})};""")
  def app_route(r):
   if 'cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm' in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='export function createClient(){return window.testClient;}')
   elif not r.request.url.startswith(base):r.abort()
   elif '/config.js' in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={supabaseUrl:"https://fixture.invalid",supabaseKey:"public-test-fixture"};')
   else:r.continue_()
  page.route('**/*',app_route);page.goto(base+'/index.html#home',wait_until='networkidle');page.wait_for_function('typeof authCallback==="function"')
  page.locator('#account').click();page.locator('#email').fill('local-signup@example.invalid');page.locator('#password').fill('test-only-password');page.locator('#signup').click()
  page.wait_for_function('signupCalls.length===1');assert 'холбоос дээр дарна уу' in page.locator('#auth-feedback').inner_text();assert page.locator('#password').input_value()==''
  assert page.evaluate('signupCalls[0].redirect')==base+'/index.html'
  page.evaluate("authCallback('SIGNED_IN',{user:{id:'signup-fixture',email:'local-signup@example.invalid'}})");page.wait_for_timeout(100);assert page.locator('#recovery-password-form').is_hidden()
  checks.append('actual app signup uses email link instruction/redirect; mocked confirmation sign-in does not open recovery password form');browser.close()
finally:s.shutdown()
report={'status':'passed','mock_auth_only':True,'checks':checks,'source':'https://supabase.com/docs/reference/javascript/auth-resetpasswordforemail','limitation':'No real email delivery/provider settings or production session exercised.'}
(ROOT/'audit/PART04-AUTH-LINKS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
