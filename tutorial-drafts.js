// Private draft transport. A revision conflict never overwrites the remote draft.
export function createDraftSession(ctx){
 let current=null,version=0,saved=0,generation=0,pending=null,timer,paused=false;
 const storage=ctx.storage||globalThis.localStorage;
 const key=(actor,id)=>`erdene:tutorial-draft:v3:${actor}:${id}`;
 const report=text=>ctx.message?.(text);
 const local=(actor,id)=>{try{return JSON.parse(storage.getItem(key(actor,id))||'null');}catch{return null;}};
 const persist=()=>{if(!current)return;try{storage.setItem(key(current.actor,current.id),JSON.stringify({...current,unsynced:version!==saved}));}catch{report('Төхөөрөмжид хадгалж чадсангүй. JSON backup татна уу.');}};
 async function flush(){
  clearTimeout(timer);if(paused||!current||saved===version||ctx.user()?.id!==current.actor)return;
  if(pending)return pending;
  const turn=generation;
  const run=(async()=>{await Promise.resolve();try{
   // One promise drains all edits, so callers can safely navigate/publish after await.
   while(turn===generation&&!paused&&current&&saved!==version&&ctx.user()?.id===current.actor){
    const batch=structuredClone(current),sent=version;
    const {data,error}=await ctx.client().rpc('admin_save_tutorial_draft',{p_id:batch.id,p_body:batch.body,p_base_revision:batch.baseRevision,p_draft_revision:batch.draftRevision,p_actor:batch.actor});
    if(error)throw error;if(turn!==generation||ctx.user()?.id!==batch.actor)return;
    if(!Number.isInteger(data?.revision)||data.revision<=batch.draftRevision)throw Error('Invalid draft save response.');
    current.draftRevision=data.revision;saved=sent;persist();report(saved===version?'Ноорог хадгалагдлаа.':'Шинэ засварыг хадгалж байна…');
   }
  }catch(e){if(turn===generation){report(/REVISION_CONFLICT/.test(e.message)?'Ноорог өөр tab-д шинэчлэгдсэн. JSON backup татаад хувилбаруудаа харьцуулна уу.':/TUTORIAL_DELETED_REFERENCE/.test(e.message)?'Үүрд устгасан хичээл рүү холбоос байна. Холбоосоо засаад хадгална уу.':/TUTORIAL_DELETED/.test(e.message)?'Энэ хичээл үүрд устгагдсан. Засвараа JSON backup татаад шинэ ID-тай хичээл үүсгэнэ үү.':'Онлайн хадгалалт амжилтгүй. Local ноорог хадгалагдсан; дахин оролдоно уу.');ctx.error?.(e);}}
  finally{if(turn===generation)pending=null;}})();
  pending=run;return run;
 }
 return {local,checkpoint:persist,async pause(){paused=true;clearTimeout(timer);await pending;},resume(){paused=false;if(current&&saved!==version){clearTimeout(timer);timer=setTimeout(()=>void flush(),0);}},preserve(value){storage.setItem(key(value.actor,value.id)+':before-rebase',JSON.stringify(value));},open(value){this.invalidate();current=structuredClone(value);version=value.unsynced?1:0;saved=0;},changed(body){if(!current)return;current.body=structuredClone(body);version++;persist();clearTimeout(timer);timer=setTimeout(()=>void flush(),ctx.delay??1800);report('Хадгалаагүй засвар байна…');},flush,dirty:()=>version!==saved,snapshot:()=>current&&structuredClone(current),invalidate({saveLocal=true}={}){if(saveLocal)persist();clearTimeout(timer);generation++;current=null;pending=null;paused=false;version=saved=0;}};
}
