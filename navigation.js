const byId=id=>document.getElementById(id);
let admin=false;
export function setAdminRoute(allowed){admin=allowed===true;byId('admin-nav').hidden=!admin;byId('admin-tutorial-nav').hidden=!admin;byId('learning-admin-nav').hidden=!admin;window.dispatchEvent(new CustomEvent('erdene-admin',{detail:admin}));route({preserveScroll:true});}
export function route({preserveScroll=false}={}){
 const hash=location.hash, tutorial=/^#tutorial(?:s|\/)/.test(hash);
 const community=['#community','#friends','#following'].includes(hash);
 const selected=/^#problem\//.test(hash)?'detail':/^#profile(?:\/|$)/.test(hash)?'profile':/^#plan(?:\/|$)/.test(hash)?'plan':hash==='#admin'?'admin':hash==='#learning-admin'?'learning-admin':tutorial?'tutorials':community?'community':/^#groups(?:\/|$)/.test(hash)?'groups':hash==='#admin-section'?'admin-section':hash==='#admin-tutorials'?'admin-tutorials':hash==='#library'?'library':'home';
 document.querySelectorAll('main > section').forEach(el=>{const home=el.classList.contains('hero')||el.classList.contains('method');const stats=el.classList.contains('stats');el.hidden=home?selected!=='home':stats?!['home','library'].includes(selected):el.id!==selected||(['admin','admin-section','admin-tutorials','learning-admin'].includes(el.id)&&!admin);});
 byId('route-message').hidden=!(['admin','admin-section','admin-tutorials','learning-admin'].includes(selected)&&!admin);
 document.querySelectorAll('.site-nav [data-route]').forEach(a=>{const active=a.dataset.route===(selected==='detail'?'library':['admin-section','admin-tutorials','learning-admin'].includes(selected)?'admin':selected);if(active)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
 if(!tutorial&&selected!=='detail')document.title='Erdene Club — Бодлого ба DSA tutorials';
 if(!preserveScroll)window.scrollTo({top:0,behavior:'instant'});
}
window.addEventListener('hashchange',route);
route();
