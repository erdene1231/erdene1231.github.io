import {normalizeUsername}from'./community.js?v=6';
import {AVATAR_BUCKET,resizeAvatar,validateAvatar,avatarUrl,rpc}from'./accounts.js?v=48';
const reserved=new Set(['admin','administrator','root','system','support','moderator','erdeneclub','api','auth','null','undefined','constructor','prototype']);
export function validateAdminProfileChanges(values,existing){
 if(!values||typeof values!=='object'||Object.keys(values).some(k=>!['first_name','last_name','username'].includes(k)))throw Error('Зөвхөн овог, нэр, username засна.');
 const first_name=String(values.first_name??'').trim(),last_name=String(values.last_name??'').trim(),username=normalizeUsername(values.username??'');
 if(first_name.length>100||last_name.length>100||[last_name,first_name].filter(Boolean).join(' ').length>100||/[\u0000-\u001f\u007f]/.test(first_name+last_name))throw Error('Овог нэр нийлээд 100 тэмдэгт хүртэл байна.');
 if(reserved.has(username)&&username!==existing?.username)throw Error('Энэ username нөөцлөгдсөн байна.');
 return{first_name,last_name,username};
}
export async function saveAdminProfile(client,profile,values,file,current=()=>true){
 if(!/^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$/i.test(profile?.user_id||'')||!/^[0-9a-f]{32}$/.test(profile?.snapshot||''))throw Error('Хэрэглэгчийн мэдээллийг дахин ачаална уу.');
 const changes=validateAdminProfileChanges(values,profile);let uploaded=null,committed=false;
 const requireCurrent=()=>{if(!current())throw Error('ACCOUNT_CHANGED');};requireCurrent();
 try{
  if(file){const blob=await resizeAvatar(file);requireCurrent();if(blob.type!=='image/webp'||!blob.size||blob.size>2097152)throw Error('Зургийг WebP болгон бэлтгэж чадсангүй.');
   const path=await rpc(client,'admin_prepare_profile_avatar',{p_target:profile.user_id,p_expected:profile.snapshot});requireCurrent();
   if(typeof path!=='string'||!path.startsWith(profile.user_id+'/admin_')||!/^[-a-zA-Z0-9_/]+\.webp$/.test(path))throw Error('Зургийн target зам буруу байна.');
   const result=await client.storage.from(AVATAR_BUCKET).upload(path,blob,{contentType:'image/webp',upsert:false});if(result.error)throw result.error;uploaded=path;requireCurrent();changes.avatar_path=path;
  }
  requireCurrent();const result=await rpc(client,'admin_save_profile',{p_target:profile.user_id,p_expected:profile.snapshot,p_changes:changes});committed=true;return result;
 }catch(error){if(uploaded&&!committed)await client.storage.from(AVATAR_BUCKET).remove([uploaded]).catch(()=>{});throw error;}
}
export function setupAdminProfiles(root,ctx){
 let allowed=false,busy=false,request=0,profile=null,dirty=false,preview=null,accountId=ctx.user()?.id||null;
 const node=(tag,text)=>{const e=document.createElement(tag);if(text!==undefined)e.textContent=text;return e;};
 root.classList.add('admin-profile-editor');const title=node('h1','Хэрэглэгчийн мэдээлэл засах'),intro=node('p','Овог, нэр, username болон profile picture-ийг засна.'),status=node('p'),search=node('form'),searchLabel=node('label','Username эсвэл user ID'),query=node('input'),find=node('button','Хэрэглэгч хайх'),form=node('form'),heading=node('h2'),photo=node('img'),reload=node('button','Дахин ачаалах'),save=node('button','Өөрчлөлт хадгалах');search.setAttribute('aria-label','Хэрэглэгч хайх');form.setAttribute('aria-label','Хэрэглэгчийн засвар');status.setAttribute('role','status');status.setAttribute('aria-live','polite');searchLabel.append(query);query.required=true;query.minLength=3;query.maxLength=36;query.autocomplete='off';find.type='submit';search.append(searchLabel,find);form.append(heading);const fields={};
 for(const[key,label]of[['last_name','Овог'],['first_name','Нэр'],['username','Username']]){const l=node('label',label),input=node('input');input.name=key;input.maxLength=key==='username'?24:100;input.required=key==='username';input.autocomplete='off';l.append(input);form.append(l);fields[key]=input;input.oninput=()=>{dirty=true;};}
 const fileLabel=node('label','Шинэ profile picture'),file=node('input');file.type='file';file.accept='image/png,image/jpeg,image/webp';fileLabel.append(file);const imageHelp=node('small','PNG, JPG эсвэл WebP · 2 MB хүртэл.');imageHelp.id='admin-profile-image-help';file.setAttribute('aria-describedby',imageHelp.id);fileLabel.append(imageHelp);photo.alt='Одоогийн profile picture';photo.width=photo.height=96;photo.hidden=true;form.append(photo,fileLabel);const actions=node('div');actions.className='auth-actions';reload.type='button';save.type='submit';actions.append(reload,save);form.append(actions);root.replaceChildren(title,intro,search,status,form);const enabled=ctx.enabled===true;
 function permitted(){return enabled&&allowed&&!!ctx.user()?.id;}
 function lock(){search.hidden=!permitted();form.hidden=!permitted()||!profile;for(const control of root.querySelectorAll('input,button'))control.disabled=busy||!permitted();}
 function clearPreview(){if(preview){URL.revokeObjectURL(preview);preview=null;}photo.removeAttribute('src');photo.hidden=true;}
 function fill(value){profile=value;dirty=false;file.value='';clearPreview();for(const key of Object.keys(fields))fields[key].value=profile[key]||'';heading.textContent='@'+profile.username;const url=avatarUrl(ctx.client(),profile);if(url){photo.src=url;photo.hidden=false;}lock();}
 function errorMessage(e){return e?.code==='40001'?'Мэдээлэл өөрчлөгдсөн байна. Дахин ачаалаад засна уу.':e?.code==='23505'?'Энэ username ашиглагдаж байна.':e?.code==='PGRST202'?'Админ profile backend хараахан идэвхжээгүй байна.':e?.code==='42501'?'Админ эрх хүрэлцэхгүй байна.':'Хадгалж чадсангүй. Дахин ачаалаад оролдоно уу.';}
 function handleError(e){const text=errorMessage(e);if(e?.code==='42501'){allowed=false;invalidate();ctx.navigation?.(false);}status.textContent=text;}
 async function load(args){if(!permitted()||busy)return;if(dirty&&!confirm('Хадгалаагүй өөрчлөлтийг орхих уу?'))return;const turn=++request,actor=ctx.user()?.id;busy=true;lock();status.textContent='Ачаалж байна…';try{const result=await rpc(ctx.client(),'admin_profile_for_edit',args);if(turn!==request||actor!==ctx.user()?.id||!permitted())return;fill(result);status.textContent='Засвар хадгалах хүртэл мэдээлэл өөрчлөгдөхгүй.';}catch(e){if(turn===request)handleError(e);}finally{if(turn===request){busy=false;lock();}}}
 search.onsubmit=e=>{e.preventDefault();if(!search.reportValidity())return;const value=query.value.trim();if(/^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$/i.test(value))void load({p_target:value});else{try{void load({p_username:normalizeUsername(value)});}catch{status.textContent='Username эсвэл user ID буруу байна.';}}};reload.onclick=()=>{if(profile)void load({p_target:profile.user_id});};file.onchange=()=>{dirty=true;};
 form.onsubmit=async e=>{e.preventDefault();if(!permitted()||busy||!profile||!form.reportValidity())return;const values=Object.fromEntries(Object.entries(fields).map(([k,input])=>[k,input.value]));try{validateAdminProfileChanges(values,profile);if(file.files[0])validateAvatar(file.files[0]);}catch(e){status.textContent=e.message;return;}const turn=++request,actor=ctx.user()?.id,target=profile.user_id;busy=true;lock();status.textContent='Хадгалж байна…';try{const saved=await saveAdminProfile(ctx.client(),profile,values,file.files[0],()=>turn===request&&permitted()&&actor===ctx.user()?.id&&profile?.user_id===target);if(turn!==request||actor!==ctx.user()?.id)return;fill(saved);ctx.saved?.(saved);query.value=saved.username;status.textContent='Хадгалагдлаа.';}catch(e){if(turn===request)handleError(e);}finally{if(turn===request){busy=false;lock();}}};
 function invalidate(){request++;busy=false;profile=null;dirty=false;query.value='';form.reset();clearPreview();status.textContent=!enabled?'Энэ боломж backend-ийн зөвшөөрөгдсөн шинэчлэлийн дараа идэвхжинэ.':'';lock();}
 window.addEventListener('erdene-admin',e=>{allowed=e.detail===true;invalidate();ctx.navigation?.(permitted());});window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue='';}});invalidate();return{accountChanged(){const id=ctx.user()?.id||null;if(id===accountId)return;accountId=id;allowed=false;invalidate();ctx.navigation?.(false);}};
}
