const el=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;};
export function mountTutorialReset(root,ctx){
 let generation=0,active=false;const valid=(turn,actor)=>turn===generation&&ctx.allowed()&&ctx.user()?.id===actor;
 function close(){generation++;active=false;root.hidden=true;root.replaceChildren();ctx.session.resume();ctx.lock(false);}
 async function open(){if(active||!ctx.allowed()||!ctx.session.snapshot())return;active=true;const turn=++generation,actor=ctx.user()?.id;ctx.lock(true);root.hidden=false;root.replaceChildren(el('p','Нийтлэгдсэн хувилбарыг шалгаж байна…'));root.scrollIntoView({block:'nearest'});
  try{await ctx.session.pause();if(!valid(turn,actor))return;const snapshot=ctx.session.snapshot(),{data,error}=await ctx.client().rpc('admin_tutorial_document',{p_id:snapshot.id});if(error)throw error;if(!valid(turn,actor))return;
   if(!data.current?.published)throw Error('Хичээлийн төлөв өөрчлөгджээ. Дахин ачаална уу.');
   if(snapshot.draftRevision!==(data.draft?.revision||0))throw Error('Ноорог өөр tab-д өөрчлөгджээ. Дахин ачаалж шалгана уу.');
   root.replaceChildren(el('h3','Нийтлэгдсэн хувилбарт буцаах'),el('p',data.current.body.title+' · revision '+data.current.revision),el('p','Түр хадгалсан болон хадгалаагүй засваруудыг арилгана. Хамгийн сүүлд нийтлэгдсэн агуулга editor-т ачаална. Нийтлэл өөрчлөгдөхгүй.'));
   const status=el('p');status.setAttribute('role','status');const confirm=el('button','Reset баталгаажуулах'),cancel=el('button','Болих');confirm.type=cancel.type='button';confirm.dataset.resetConfirm='true';cancel.dataset.resetCancel='true';cancel.onclick=close;
   confirm.onclick=async()=>{if(confirm.disabled||!valid(turn,actor))return;confirm.disabled=cancel.disabled=true;try{const {data:result,error}=await ctx.client().rpc('admin_reset_tutorial_draft',{p_id:snapshot.id,p_current_revision:data.current.revision,p_draft_revision:data.draft?.revision||0,p_actor:actor});if(error)throw error;if(!valid(turn,actor))return;ctx.accept(result,actor,snapshot.id);close();ctx.message('Нийтлэгдсэн хувилбарт буцлаа. Түр засварууд цэвэрлэгдсэн.');}catch(e){if(valid(turn,actor)){status.textContent=e.message;cancel.disabled=false;}}};root.append(status,confirm,cancel);cancel.focus();
  }catch(e){if(valid(turn,actor)){root.replaceChildren(el('p',e.message));const cancel=el('button','Буцах');cancel.type='button';cancel.dataset.resetCancel='true';cancel.onclick=close;root.append(cancel);}}
 }
 root.hidden=true;return {open,invalidate:close};
}
