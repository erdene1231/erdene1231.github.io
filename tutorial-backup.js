import {validateTutorial} from './tutorial-model.js?v=46';
export function parseTutorialBackup(text,id){
 if(new TextEncoder().encode(text).length>1500000)throw Error('JSON backup 1.5 MB-аас их байна.');
 let value;try{value=JSON.parse(text);}catch{throw Error('JSON файл буруу байна.');}
 const body=value?.body??value;if(!body||typeof body!=='object'||Array.isArray(body)||body.id!==id)throw Error('Backup-ийн ID одоогийн хичээлтэй таарахгүй байна. Тохирох хичээлийг нээгээрэй.');
 const check=structuredClone(body);
 for(const v of [check,check.translations?.en].filter(Boolean)){
  for(const k of ['title','summary','prerequisites'])if(v[k]==='')v[k]='Ноорог';
  if(Array.isArray(v.sections))for(const s of v.sections){if(s.title==='')s.title='Шинэ хэсэг';if(Array.isArray(s.blocks)&&!s.blocks.length)s.blocks=[{type:'p',text:'Ноорог'}];
   if(Array.isArray(s.blocks))for(const b of s.blocks){if(['p','code','note'].includes(b?.type)&&b.text==='')b.text='Ноорог';if(b?.type==='problem'&&b.problemKey==='')b.problemKey='1';
    if(b?.type==='image'){if(b.alt==='')b.alt='Ноорог';if(b.path==='')b.path=id+'/00000000-0000-0000-0000-000000000000/00000000-0000-0000-0000-000000000000.webp';}
    if(b?.type==='rich'&&Array.isArray(b.content)){if(!b.content.length)b.content=[{text:'Ноорог',marks:[]}];else for(const span of b.content)if(span?.text==='')span.text='Ноорог';}
   }
  }
 }
 for(const k of ['category','aliases'])if(check[k]==='')check[k]='Ноорог';
 validateTutorial(check);return structuredClone(body);
}
const el=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;};
export function mountBackupImport(root,input,ctx){
 let generation=0;const valid=(turn,actor)=>turn===generation&&ctx.allowed()&&ctx.user()?.id===actor;
 function close(){generation++;root.hidden=true;root.replaceChildren();input.value='';ctx.session.resume();ctx.lock(false);}
 input.onchange=async()=>{const file=input.files?.[0],snapshot=ctx.session.snapshot();if(!file||!snapshot||!ctx.allowed())return;const actor=ctx.user()?.id,turn=++generation;ctx.lock(true);root.hidden=false;root.replaceChildren(el('p','JSON backup шалгаж байна…'));
  try{ctx.capture?.();await ctx.session.pause();if(!valid(turn,actor))return;if(file.size>1500000)throw Error('JSON backup 1.5 MB-аас их байна.');const body=parseTutorialBackup(await file.text(),snapshot.id);if(!valid(turn,actor))return;
   root.replaceChildren(el('h3','JSON backup-ийг хувийн ноорогт оруулах'),el('p',(body.title||body.id)+' · '+body.id),el('p','Одоогийн засварын backup төхөөрөмжид хадгалагдана. Импорт зөвхөн хувийн нооргийг солино; нийтлэгдсэн хичээлийг өөрчлөхгүй.'));
   const status=el('p');status.setAttribute('role','status');const confirm=el('button','Импорт баталгаажуулах'),cancel=el('button','Болих');confirm.type=cancel.type='button';confirm.dataset.importConfirm='true';cancel.dataset.importCancel='true';cancel.onclick=close;
   confirm.onclick=()=>{if(!valid(turn,actor)||confirm.disabled)return;try{const current=ctx.session.snapshot();if(!current||current.id!==snapshot.id)throw Error('Хичээл өөрчлөгджээ. Дахин оролдоно уу.');ctx.session.preserve(current);ctx.accept(body,current);close();ctx.message('JSON backup хувийн ноорогт импортлогдлоо.');}catch(e){status.textContent=e.message;}};
   root.append(status,confirm,cancel);root.scrollIntoView({block:'nearest'});
  }catch(e){if(valid(turn,actor)){root.replaceChildren(el('p',e.message));const cancel=el('button','Буцах');cancel.type='button';cancel.dataset.importCancel='true';cancel.onclick=close;root.append(cancel);}}
 };
 root.hidden=true;return {invalidate:close};
}
