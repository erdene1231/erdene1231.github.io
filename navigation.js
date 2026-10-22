const byId=id=>document.getElementById(id);
let admin=false;
export function setAdminRoute(allowed){admin=allowed===true;byId('admin-nav').hidden=!admin;byId('admin-tutorial-nav').hidden=!admin;route();}
export function route(){
 const hash=location.hash, tutorial=/^#tutorial(?:s|\/)/.test(hash);
 const community=['#community','#friends','#following'].includes(hash);
 const selected=tutorial?'tutorials':community?'community':/^#groups(?:\/|$)/.test(hash)?'groups':hash==='#admin-section'?'admin-section':hash==='#admin-tutorials'?'admin-tutorials':hash==='#library'?'library':'home';
 document.querySelectorAll('main > section').forEach(el=>{const home=el.classList.contains('hero')||el.classList.contains('method');const stats=el.classList.contains('stats');el.hidden=home?selected!=='home':stats?!['home','library'].includes(selected):el.id!==selected||(['admin-section','admin-tutorials'].includes(el.id)&&!admin);});
 byId('route-message').hidden=!(['admin-section','admin-tutorials'].includes(selected)&&!admin);
 document.querySelectorAll('.site-nav [data-route]').forEach(a=>{const active=a.dataset.route===(community?hash.slice(1):selected);if(active)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
 if(!tutorial)document.title='Erdene Club — Бодлого ба DSA tutorials';
 window.scrollTo({top:0,behavior:'instant'});
}
window.addEventListener('hashchange',route);
route();
