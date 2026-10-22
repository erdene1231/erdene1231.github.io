import {normalizeUsername} from './community.js?v=6';
export const AVATAR_BUCKET='think-cp-avatars';
export function cleanProfile(values) {
 const first_name=String(values.first_name||'').trim(),last_name=String(values.last_name||'').trim();
 if(first_name.length>100||last_name.length>100)throw new Error('Овог болон нэр тус бүр 100 тэмдэгтээс урт байж болохгүй.');
 const full_name=[last_name,first_name].filter(Boolean).join(' ')||String(values.full_name||'').trim(),school=String(values.school||'').trim();
 if(full_name.length>100||school.length>160)throw new Error('Овог нэр 100, сургууль 160 тэмдэгтээс урт байж болохгүй.');
 return {username:normalizeUsername(values.username),full_name,first_name,last_name,school,avatar_path:values.avatar_path||null};
}
export function avatarUrl(client,profile) {
 const path=profile?.avatar_path;
 if(!client||!path||!new RegExp('^'+profile.user_id+'/[a-zA-Z0-9_-]+\\.(webp|png|jpg|jpeg)$').test(path))return null;
 return client.storage.from(AVATAR_BUCKET).getPublicUrl(path).data.publicUrl;
}
export async function ownProfile(client,id) {
 const {data,error}=await client.from('profiles').select('user_id,username,full_name,first_name,last_name,school,avatar_path').eq('user_id',id).maybeSingle();
 if(error)throw error;return data||{user_id:id,username:null,full_name:'',first_name:'',last_name:'',school:'',avatar_path:null};
}
export function validateAvatar(file) {
 if(!['image/jpeg','image/png','image/webp'].includes(file.type))throw new Error('JPG, PNG эсвэл WebP зураг сонгоно уу.');
 if(!file.size||file.size>2*1024*1024)throw new Error('Зураг 2 MB-аас бага хэмжээтэй байна.');
}
export async function resizeAvatar(file) {
 validateAvatar(file);
 const bitmap=await createImageBitmap(file);
 try {
  if(!bitmap.width||!bitmap.height)throw new Error('Зургийг уншиж чадсангүй.');
  const canvas=document.createElement('canvas'),size=Math.min(512,bitmap.width,bitmap.height);canvas.width=size;canvas.height=size;
  const crop=Math.min(bitmap.width,bitmap.height);canvas.getContext('2d').drawImage(bitmap,(bitmap.width-crop)/2,(bitmap.height-crop)/2,crop,crop,0,0,size,size);
  const blob=await new Promise(resolve=>canvas.toBlob(resolve,'image/webp',.85));
  if(!blob)throw new Error('Зургийг боловсруулах боломжгүй.');return blob;
 } finally {bitmap.close();}
}
export async function saveOwnProfile(client,id,values,file,previousPath=null) {
 const row={user_id:id,...cleanProfile(values)};let uploaded=null;
 if(file){const blob=await resizeAvatar(file);uploaded=id+'/'+crypto.randomUUID()+'.webp';const {error}=await client.storage.from(AVATAR_BUCKET).upload(uploaded,blob,{contentType:blob.type,upsert:false});if(error)throw error;row.avatar_path=uploaded;}
 try {const {error}=await client.from('profiles').upsert(row,{onConflict:'user_id'});if(error)throw error;}
 catch(error){if(uploaded)await client.storage.from(AVATAR_BUCKET).remove([uploaded]).catch(()=>{});throw error;}
 // Cleanup is best-effort; a saved profile remains successful if cleanup fails.
 if(previousPath&&previousPath!==row.avatar_path)await client.storage.from(AVATAR_BUCKET).remove([previousPath]).catch(()=>{});
 return row;
}
export async function rpc(client,name,args={}) {const {data,error}=await client.rpc(name,args);if(error)throw error;return data;}
export function accountError(error) {
 if(['42P01','PGRST202','PGRST205','PGRST204','42703'].includes(error?.code))return 'Account шинэчлэл идэвхжээгүй байна. Багшдаа мэдэгдээрэй.';
 if(error?.code==='23505')return 'Энэ username ашиглагдаж байна. Өөр нэр сонгоорой.';
 return error?.message||'Холболт амжилтгүй. Дахин оролдоорой.';
}
export async function requestRecovery(client,email,redirectTo) {
 const {error}=await client.auth.resetPasswordForEmail(email,{redirectTo});if(error)throw error;
}
export async function verifyRecovery(client,email,token) {
 const {data,error}=await client.auth.verifyOtp({email,token,type:'recovery'});if(error)throw error;
 if(!data.session?.user?.id)throw new Error('Код баталгаажсангүй. Дахин код аваарай.');return data.session.user.id;
}
export async function setRecoveredPassword(client,verifiedUserId,password,confirm) {
 if(!verifiedUserId)throw new Error('Эхлээд email кодоо баталгаажуулна уу.');
 if(password.length<8)throw new Error('Нууц үг дор хаяж 8 тэмдэгттэй байна.');
 if(password!==confirm)throw new Error('Хоёр нууц үг ижил биш байна.');
 const {data,error}=await client.auth.getUser();if(error)throw error;
 if(data.user?.id!==verifiedUserId)throw new Error('Account солигдсон байна. Email кодоо дахин баталгаажуулна уу.');
 const result=await client.auth.updateUser({password});if(result.error)throw result.error;
}
