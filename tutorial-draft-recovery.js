// Explicit comparison/rebase; no version is chosen or published automatically.
const el=(tag,text)=>{const e=document.createElement(tag);if(text!==undefined)e.textContent=text;return e;};
export function mountDraftRecovery(root,ctx){
 let generation=0,active=false;
 const valid=(turn,actor)=>turn===generation&&ctx.allowed()&&ctx.user()?.id===actor;
 function close(){generation++;active=false;root.replaceChildren();root.hidden=true;ctx.session.resume();ctx.lock(false);}
 async function open(){
  if(active||!ctx.allowed())return;
  const actor=ctx.user()?.id,turn=++generation;active=true;root.hidden=false;ctx.lock(true);
  root.replaceChildren(el('p','Хувилбаруудыг ачаалж байна…'));
  try{
   ctx.capture();await ctx.session.pause();if(!valid(turn,actor))return;
   const local=ctx.candidate();if(!local||local.actor!==actor)throw Error('Харьцуулах ноорог сонгоно уу.');
   const id=local.id,{data,error}=await ctx.client().rpc('admin_tutorial_document',{p_id:id});
   if(error)throw error;if(!valid(turn,actor))return;
   root.replaceChildren(el('h3','Хичээлээ үргэлжлүүлэх хувилбарыг сонгоно уу'),el('p','Доорх гурван хувилбарыг шалгаад нэгийг сонгоно уу. Дараа нь сонгосон хувилбараа хувийн ноорогт хадгалж, editor рүү орно.'));
   root.append(el('p','Онлайн ноорог ба нийтлэгдсэн хичээлийн revision нь тусдаа тоолуур. Тоогоор нь шинэ, хуучныг харьцуулахгүй.'));
   const backup=el('button','Төхөөрөмжийн засварыг JSON backup татах');backup.type='button';backup.dataset.recoveryBackup='true';backup.onclick=()=>ctx.backup?.(local.body);root.append(backup);
   const versions=[['local','Төхөөрөмжийн засвар',local.body,local.draftRevision,'Нооргийн revision'],['draft','Онлайн ноорог',data.draft?.body,data.draft?.revision,'Нооргийн revision'],['published','Нийтлэгдсэн хувилбар',data.current?.body,data.current?.revision,'Нийтлэлийн revision']];
   let selected=null;
   const choices=el('div');choices.className='recovery-choices';root.append(choices);
   const status=el('p');status.setAttribute('role','status');
   const save=el('button','Сонгосон хувилбарыг ноорог болгон хадгалах');save.type='button';save.disabled=true;save.dataset.rebaseSave='true';
   const buttons=[];
   for(const [key,label,body,rev,counter] of versions){
    const card=el('article');card.dataset.version=key;card.className='recovery-version';card.append(el('h4',label),el('small',counter+' '+(rev??0)));
    if(body){card.append(el('p',body.title||id),el('p',body.summary||'Тайлбар оруулаагүй.'));
     const choose=el('button',label+' сонгох');choose.type='button';choose.dataset.rebaseChoice=key;choose.setAttribute('aria-pressed','false');buttons.push(choose);
     choose.onclick=()=>{selected=body;for(const b of buttons)b.setAttribute('aria-pressed',String(b===choose));status.textContent=label+' сонгогдлоо. Доорх хадгалах товчоор editor рүү орно.';save.disabled=false;};card.append(choose);
     const detail=el('details');detail.append(el('summary','Агуулгыг дэлгэрэнгүй харах'));const pre=el('pre',JSON.stringify(body,null,2));pre.style.cssText='max-height:320px;overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere';detail.append(pre);card.append(detail);
    }else card.append(el('p','Энэ хувилбар байхгүй.'));choices.append(card);
   }
   const cancel=el('button','Буцах');cancel.type='button';cancel.dataset.recoveryCancel='true';cancel.onclick=close;
   const retry=el('button','Хувилбаруудыг дахин ачаалах');retry.type='button';retry.dataset.recoveryRetry='true';retry.hidden=true;retry.onclick=()=>{active=false;void open();};
   save.onclick=async()=>{
    if(!selected||!valid(turn,actor)||save.disabled)return;
    for(const b of root.querySelectorAll('button'))b.disabled=true;
    try{
     ctx.session.preserve(local);
     const {data:result,error}=await ctx.client().rpc('admin_rebase_tutorial_draft',{p_id:id,p_body:structuredClone(selected),p_current_revision:data.current?.revision??0,p_draft_revision:data.draft?.revision??0,p_actor:actor});
     if(error)throw error;if(!valid(turn,actor))return;
     ctx.accept(result,actor,id);close();ctx.message('Сонгосон хувилбар ноорогт хадгалагдлаа. Засвараа үргэлжлүүлээрэй.');
    }catch(e){if(!valid(turn,actor))return;
     status.textContent=/REVISION_CONFLICT/.test(e.message)?'Харьцуулснаас хойш хувилбар өөрчлөгджээ. Дахин ачаалаад сонгоно уу. Төхөөрөмжийн засвар хадгалагдсан.':e.message;
     cancel.disabled=backup.disabled=retry.disabled=false;retry.hidden=false;
    }
   };
   root.append(status,save,cancel,retry);
  }catch(e){if(valid(turn,actor)){root.replaceChildren(el('p',e.message));const cancel=el('button','Буцах');cancel.type='button';cancel.dataset.recoveryCancel='true';cancel.onclick=close;root.append(cancel);}}
 }
 root.hidden=true;return {open,invalidate:close};
}
