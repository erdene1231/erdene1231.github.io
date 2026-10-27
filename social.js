import {avatarUrl,rpc,accountError,requestRecovery,setRecoveredPassword} from './accounts.js?v=44';
export function setupSocial(ctx) {
 const $=id=>document.getElementById(id),node=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;};
 let tab='leaderboard',page=0,friendPage=0,followPage=0,leaderToken=0,friendToken=0,followToken=0,profileToken=0,viewedId=null,relation='guest',accountId=null,searchTimer;
 let recoveryEmail='',verifiedId=null,sentAt=0,recoveryBusy=false,recoveryTurn=0;
 function avatar(profile){const n=node('span','avatar',((profile.full_name||profile.username||'?').trim()[0]||'?').toUpperCase()),url=avatarUrl(ctx.client(),profile);if(url){const img=node('img');img.src=url;img.alt='';img.loading='lazy';img.onerror=()=>img.remove();n.append(img);}return n;}
 function person(profile,rank){const b=node('button','person');b.type='button';b.append(avatar(profile));const info=node('span','person-info');info.append(node('strong','',profile.full_name||profile.username||'Нэрээ тохируулаагүй'),node('small','',profile.username?'@'+profile.username:'Username тохируулаагүй'),node('small','',profile.school||'Сургууль оруулаагүй'));b.append(info);if(rank)b.append(node('span','community-rank','#'+rank));b.append(node('span','person-score',profile.solved_count+' бодсон'));b.onclick=()=>ctx.viewProfile?ctx.viewProfile(profile.user_id):void openProfile(profile.user_id);return b;}
 function online(){if(ctx.client())return true;$('community-message').textContent='Онлайн account холболт шаардлагатай.';return false;}
 async function loadLeaderboard(){
  if(tab!=='leaderboard'||!online())return;const token=++leaderToken;$('community-message').textContent='Хэрэглэгчдийг ачаалж байна…';$('leaderboard-list').replaceChildren();$('leader-next').disabled=true;$('leader-prev').disabled=true;
  try{const rows=await rpc(ctx.client(),'get_leaderboard',{p_offset:page*50,p_limit:50,p_search:$('people-search').value.trim()});if(token!==leaderToken)return;
   for(const p of rows||[]){const li=node('li');li.append(person(p,p.rank));$('leaderboard-list').append(li);}
   const total=Number(rows?.[0]?.total_count||0);$('people-count').textContent=total+' хэрэглэгч';$('leader-page').textContent=(page+1)+'-р хуудас';$('leader-prev').disabled=page===0;$('leader-next').disabled=(page+1)*50>=total;
   $('community-message').textContent=rows?.length?'':'Тохирох хэрэглэгч олдсонгүй.';
  }catch(e){if(token===leaderToken)$('community-message').textContent=accountError(e);}
 }
 async function loadFriends(){
  if(tab!=='friends')return;const token=++friendToken,uid=ctx.user()?.id;$('friends-list').replaceChildren();$('friend-next').disabled=true;$('friend-prev').disabled=true;
  if(!uid){$('community-message').textContent='Friends хэсгийг ашиглахын тулд нэвтэрнэ үү.';$('friends-count').textContent='';return;}if(!online())return;
  $('community-message').textContent='Friends жагсаалтыг ачаалж байна…';
  try{const rows=await rpc(ctx.client(),'get_friends',{p_kind:$('friend-kind').value,p_offset:friendPage*50,p_limit:50});if(token!==friendToken||uid!==ctx.user()?.id)return;
   for(const p of rows||[]){const li=node('li');li.append(person(p));const actions=node('div','friend-actions');addActions(actions,p.relationship,p.user_id);li.append(actions);$('friends-list').append(li);}
   const total=Number(rows?.[0]?.total_count||0);$('friends-count').textContent=total+' хэрэглэгч';$('friend-page').textContent=(friendPage+1)+'-р хуудас';$('friend-prev').disabled=friendPage===0;$('friend-next').disabled=(friendPage+1)*50>=total;$('community-message').textContent=rows?.length?'':'Энэ жагсаалт одоогоор хоосон байна.';
  }catch(e){if(token===friendToken&&uid===ctx.user()?.id)$('community-message').textContent=accountError(e);}
 }
 async function loadFollowing(){
  if(tab!=='following')return;const token=++followToken,uid=ctx.user()?.id;$('following-list').replaceChildren();$('follow-prev').disabled=true;$('follow-next').disabled=true;
  if(!uid){$('community-message').textContent='Following хэсгийг ашиглахын тулд нэвтэрнэ үү.';$('following-count').textContent='';return;}if(!online())return;$('community-message').textContent='Following ачаалж байна…';
  try{const rows=await rpc(ctx.client(),'get_following',{p_offset:followPage*50,p_limit:50});if(token!==followToken||uid!==ctx.user()?.id)return;
   for(const p of rows||[]){const li=node('li');li.append(person(p));const actions=node('div','friend-actions');addFollow(actions,p.user_id,true);li.append(actions);$('following-list').append(li);}
   const total=Number(rows?.[0]?.total_count||0);$('following-count').textContent=total+' хэрэглэгч';$('follow-page').textContent=(followPage+1)+'-р хуудас';$('follow-prev').disabled=followPage===0;$('follow-next').disabled=(followPage+1)*50>=total;$('community-message').textContent=rows?.length?'':'Following жагсаалт одоогоор хоосон байна.';
  }catch(e){if(token===followToken&&uid===ctx.user()?.id)$('community-message').textContent=accountError(e);}
 }
 function addFollow(container,id,following){if(!ctx.user()||ctx.user().id===id)return;const b=node('button','',following?'Follow болих':'Follow хийх');b.type='button';b.onclick=async()=>{const uid=ctx.user()?.id;b.disabled=true;const msg=$('public-profile').open&&viewedId===id?$('public-profile-message'):$('community-message');
  try{await rpc(ctx.client(),'follow_action',{p_user_id:id,p_follow:!following});if(uid!==ctx.user()?.id)return;if(viewedId===id&&$('public-profile').open)await openProfile(id);if(tab==='following')await loadFollowing();msg.textContent=following?'Follow больсон.':'Following-д нэмэгдлээ.';}
  catch(e){if(uid===ctx.user()?.id)msg.textContent=accountError(e);}finally{b.disabled=false;}};container.append(b);}
 function addActions(container,status,id){
  const actions=status==='incoming'?[['accept','Зөвшөөрөх'],['decline','Татгалзах']]:status==='outgoing'?[['cancel','Хүсэлт цуцлах']]:status==='friend'?[['remove','Найзаас хасах']]:status==='none'?[['request','Найзын хүсэлт илгээх']]:[];
  for(const [action,label] of actions){const b=node('button',action==='accept'||action==='request'?'primary':'',label);b.type='button';b.onclick=()=>void act(id,action,b);container.append(b);}
 }
 async function act(id,action,button){const uid=ctx.user()?.id;if(!uid)return;button.disabled=true;const msg=viewedId===id&&$('public-profile').open?$('public-profile-message'):$('community-message');msg.textContent='Хадгалж байна…';
  try{await rpc(ctx.client(),'friend_action',{p_user_id:id,p_action:action});if(uid!==ctx.user()?.id)return;msg.textContent='Хадгалагдлаа.';if(viewedId===id&&$('public-profile').open)await openProfile(id);if(tab==='friends')await loadFriends();else if(tab==='following')await loadFollowing();}
  catch(e){if(uid===ctx.user()?.id)msg.textContent=accountError(e);}finally{button.disabled=false;}
 }
 async function openProfile(id){
  const token=++profileToken,uid=ctx.user()?.id;viewedId=id;$('auth').close();$('public-profile-name').textContent='Profile';$('public-profile-body').replaceChildren();$('public-profile-actions').replaceChildren();$('public-solved').replaceChildren();$('public-trying').replaceChildren();$('public-profile-message').textContent='Profile ачаалж байна…';if(!$('public-profile').open)$('public-profile').showModal();
  try{const [rows,progress,status,following]=await Promise.all([rpc(ctx.client(),'get_public_profile',{p_user_id:id}),rpc(ctx.client(),'get_public_progress',{p_user_id:id}),uid?rpc(ctx.client(),'get_friend_status',{p_user_id:id}):Promise.resolve('guest'),uid&&uid!==id?rpc(ctx.client(),'is_following',{p_user_id:id}):Promise.resolve(false)]);
   if(token!==profileToken||uid!==ctx.user()?.id||!$('public-profile').open)return;const p=rows?.[0];if(!p)throw new Error('Profile олдсонгүй.');relation=status;
   $('public-profile-name').textContent=p.full_name||p.username||'Нэрээ тохируулаагүй';const head=node('div','profile-heading');head.append(avatar(p));const info=node('div');info.append(node('p','profile-username',p.username?'@'+p.username:'Username тохируулаагүй'),node('p','muted',p.school||'Сургууль оруулаагүй'));head.append(info);$('public-profile-body').append(head);
   const known=new Map(ctx.problems().map(p=>[p.id,p])),solved=(progress||[]).filter(x=>x.status==='solved'&&known.has(x.problem_id)),trying=(progress||[]).filter(x=>x.status==='trying'&&known.has(x.problem_id)),percent=ctx.problems().length?Math.round(solved.length/ctx.problems().length*100):0;
   const stats=node('div','profile-stats');stats.append(node('strong','',solved.length+' бодсон'),node('strong','',trying.length+' бодож байгаа'),node('strong','',percent+'%'),node('strong','','#'+p.rank));$('public-profile-body').append(stats);const bar=node('progress');bar.max=100;bar.value=percent;bar.setAttribute('aria-label','Бодсон хувь');$('public-profile-body').append(bar);
   for(const [items,target] of [[solved,'public-solved'],[trying,'public-trying']]){for(const x of items){const task=known.get(x.problem_id),li=node('li'),b=node('button','','#'+task.number+' · '+task.title+' · '+task.ref);b.onclick=()=>{$('public-profile').close();ctx.openProblem(task);};li.append(b);$(target).append(li);}if(!items.length)$(target).append(node('li','muted','Одоогоор байхгүй.'));}
   addActions($('public-profile-actions'),relation,id);addFollow($('public-profile-actions'),id,following);
   if(relation==='self'){const b=node('button','','Profile засах');b.onclick=()=>{$('public-profile').close();ctx.openAccount();};$('public-profile-actions').append(b);}
   if(relation==='guest')$('public-profile-actions').append(node('p','muted','Найзын хүсэлт илгээхийн тулд нэвтэрнэ үү.'));
   $('public-profile-message').textContent='Онлайнаар хадгалсан progress. “Бодсон” төлөвийг хэрэглэгч өөрөө тэмдэглэдэг.';
  }catch(e){if(token===profileToken&&uid===ctx.user()?.id)$('public-profile-message').textContent=accountError(e);}
 }
 async function byUsername(name){if(!online())return;const token=++profileToken;try{const id=await rpc(ctx.client(),'get_profile_id',{p_username:name});if(token!==profileToken)return;if(id){$('auth').close();if(ctx.viewProfile)ctx.viewProfile(id);else await openProfile(id);}else ctx.notice('Profile олдсонгүй.');}catch(e){ctx.notice(accountError(e));}}
 function chooseTab(next){leaderToken++;friendToken++;followToken++;tab=next;$('leaderboard-panel').hidden=tab!=='leaderboard';$('friends-panel').hidden=tab!=='friends';$('following-panel').hidden=tab!=='following';$('leaderboard-tab').setAttribute('aria-selected',String(tab==='leaderboard'));$('friends-tab').setAttribute('aria-selected',String(tab==='friends'));$('following-tab').setAttribute('aria-selected',String(tab==='following'));if(tab==='leaderboard')void loadLeaderboard();else if(tab==='friends')void loadFriends();else void loadFollowing();}
 const communityRoute=()=>{const h=location.hash;if(['#community','#friends','#following'].includes(h))chooseTab(h==='#friends'?'friends':h==='#following'?'following':'leaderboard');};
 window.addEventListener('hashchange',communityRoute);communityRoute();
 $('following-tab').onclick=()=>{location.hash='#following';};$('leaderboard-tab').onclick=()=>{location.hash='#community';};$('friends-tab').onclick=()=>{location.hash='#friends';};$('refresh-community').onclick=()=>{if(tab==='leaderboard')void loadLeaderboard();else if(tab==='friends')void loadFriends();else void loadFollowing();};
 $('people-search').addEventListener('input',()=>{clearTimeout(searchTimer);searchTimer=setTimeout(()=>{page=0;void loadLeaderboard();},300);});
 $('leader-prev').onclick=()=>{if(page>0){page--;void loadLeaderboard();}};$('leader-next').onclick=()=>{page++;void loadLeaderboard();};
 $('friend-kind').onchange=()=>{friendPage=0;void loadFriends();};$('friend-prev').onclick=()=>{if(friendPage>0){friendPage--;void loadFriends();}};$('friend-next').onclick=()=>{friendPage++;void loadFriends();};
 $('follow-prev').onclick=()=>{if(followPage>0){followPage--;void loadFollowing();}};$('follow-next').onclick=()=>{followPage++;void loadFollowing();};
 $('my-profile').onclick=()=>{if(ctx.user()){$('auth').close();if(ctx.viewProfile)ctx.viewProfile(ctx.user().id);else void openProfile(ctx.user().id);}};$('refresh-public-profile').onclick=()=>{if(viewedId)void openProfile(viewedId);};$('public-profile').addEventListener('close',()=>{profileToken++;});
 // The email link authenticates recovery; only PASSWORD_RECOVERY opens the new-password form.
 function recoveryStage(stage){for(const id of ['recovery-email-form','recovery-link-panel','recovery-password-form'])$(id).hidden=id!==stage;}
 function resetRecovery(){recoveryTurn++;verifiedId=null;recoveryEmail='';$('recovery-password').value='';$('recovery-confirm').value='';recoveryStage('recovery-email-form');}
 function startRecovery(){resetRecovery();$('recovery-email').value=$('email').value.trim()||ctx.user()?.email||'';$('recovery-message').textContent='Email дээрх баталгаажуулах холбоосоор нууц үгээ шинэчилнэ.';$('auth').close();if(!$('recovery').open)$('recovery').showModal();}
 async function sendLink(event,resend=false){event?.preventDefault();if(recoveryBusy||!ctx.client())return;if(!resend&&!$('recovery-email-form').reportValidity())return;
  const email=resend?recoveryEmail:$('recovery-email').value.trim();if(email===recoveryEmail&&Date.now()-sentAt<60000){$('recovery-message').textContent='Дахин холбоос авахын өмнө нэг минут хүлээнэ үү.';return;}
  const turn=recoveryTurn;recoveryBusy=true;$('send-recovery-link').disabled=true;$('resend-recovery-link').disabled=true;$('recovery-message').textContent='Холбоос илгээж байна…';
  try{await requestRecovery(ctx.client(),email,location.origin+location.pathname);if(turn!==recoveryTurn)return;recoveryEmail=email;sentAt=Date.now();verifiedId=null;recoveryStage('recovery-link-panel');$('recovery-destination').textContent=email;$('recovery-message').textContent='Энэ email-д бүртгэл байгаа бол баталгаажуулах холбоос илгээгдэнэ. Email дээрх холбоос дээр дарна уу. Inbox болон spam хавтсаа шалгаарай.';}
  catch(e){if(turn===recoveryTurn)$('recovery-message').textContent=accountError(e);}finally{recoveryBusy=false;$('send-recovery-link').disabled=false;$('resend-recovery-link').disabled=false;}
 }
 $('forgot-password').onclick=startRecovery;$('recovery-email-form').onsubmit=e=>void sendLink(e);$('resend-recovery-link').onclick=()=>void sendLink(null,true);$('change-recovery-email').onclick=()=>{if(recoveryBusy)return;resetRecovery();$('recovery-message').textContent='Email хаягаа оруулна уу.';};
 // Never display provider error descriptions or tokens from callback URLs.
 const callbackURL=new URL(location.href),callbackHash=new URLSearchParams(callbackURL.hash.slice(1));
 if(callbackURL.searchParams.has('error')||callbackURL.searchParams.has('error_code')||callbackHash.has('error')||callbackHash.has('error_code')){
  $('auth-feedback').textContent='Баталгаажуулах холбоос хүчингүй эсвэл хугацаа нь дууссан байна. Шинэ холбоос аваад дахин оролдоно уу.';
  for(const key of ['error','error_code','error_description']){callbackURL.searchParams.delete(key);callbackHash.delete(key);}
  callbackURL.hash=callbackHash.toString();history.replaceState(null,'',callbackURL.pathname+callbackURL.search+callbackURL.hash);
  if(!$('auth').open)$('auth').showModal();
 }
 $('recovery-password-form').onsubmit=async e=>{e.preventDefault();if(recoveryBusy||!$('recovery-password-form').reportValidity())return;recoveryBusy=true;$('save-recovery-password').disabled=true;
  try{await setRecoveredPassword(ctx.client(),verifiedId,$('recovery-password').value,$('recovery-confirm').value);resetRecovery();recoveryStage('done');$('recovery-message').textContent='Нууц үг шинэчлэгдлээ. Account руугаа нэвтэрсэн байна.';}
  catch(error){$('recovery-message').textContent=accountError(error);}finally{recoveryBusy=false;$('save-recovery-password').disabled=false;}
 };
 $('recovery').addEventListener('close',()=>{if(!$('recovery').open)resetRecovery();});
 return {
  connected(){if(tab==='leaderboard')void loadLeaderboard();else if(tab==='friends')void loadFriends();else void loadFollowing();},
  accountChanged(){const id=ctx.user()?.id||null;$('my-profile').hidden=!id;$('forgot-password').hidden=!ctx.client();if(id===accountId)return;accountId=id;friendToken++;followToken++;profileToken++;$('friends-list').replaceChildren();$('following-list').replaceChildren();if($('public-profile').open)void openProfile(viewedId);if(tab==='friends')void loadFriends();else if(tab==='following')void loadFollowing();},
  authEvent(event,session){if(event==='PASSWORD_RECOVERY'&&session?.user){recoveryTurn++;verifiedId=session.user.id;$('recovery-password').value='';$('recovery-confirm').value='';recoveryStage('recovery-password-form');$('recovery-message').textContent='Email баталгаажлаа. Шинэ нууц үгээ оруулна уу.';$('auth').close();if(!$('recovery').open)$('recovery').showModal();}},
  byUsername,openProfile,
 };
}
