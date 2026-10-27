// Public deployment capability declaration, not an authorization source.
// Missing/unknown declarations fall back to31. Capability32 is provided by036;
// it does not imply the complete032 migration or optional033/034 are installed.
export function problemBackend(config=globalThis.window?.THINK_CP_CONFIG||{}) {
 const version=[31,32,33,34].includes(config.problemBackendVersion)?config.problemBackendVersion:31;
 return Object.freeze({version,priority:version>=32,editorial:version>=33,statement:version>=34,bulkImport:version>=34});
}
export function prepareProblemSave(payload,existing,capabilities=problemBackend()) {
 const p=structuredClone(payload);
 if(!capabilities.priority){
  if(!existing)throw Error('Шинэ бодлого нэмэх backend шинэчлэл хараахан идэвхжээгүй.');
  if(['priorityLevel','priorityReason','ratingSource','ratingVerifiedAt'].some(k=>Object.hasOwn(existing,k)))throw Error('Энэ бодлогын metadata-г алдахгүйн тулд backend шинэчлэл шаардлагатай.');
  p.priority=existing.priority===true;
  for(const field of ['priorityLevel','priorityReason','ratingSource','ratingVerifiedAt'])delete p[field];
 }
 if(!capabilities.editorial&&(p.editorial!=null||existing?.hasEditorial))throw Error('Editorial backend шинэчлэл шаардлагатай.');
 if(!capabilities.statement&&(p.statement!=null||existing?.hasStatement))throw Error('Statement backend шинэчлэл шаардлагатай.');
 return p;
}
// Existing authenticated dry-run RPC, deliberately invalid tier.036 rejects it
// before any catalog/source write;031 accepts/ignores it,so a rollback fails closed.
export async function requireProblemMetadataBackend(client,payload){
 try{const{error}=await client.rpc('admin_import_learning_problems',{p_problems:[{...payload,priorityLevel:'__part04_capability_probe__'}],p_dry_run:true});if(error?.code==='22023'&&error.message?.includes('Priority must be low, medium or high.'))return;}catch{}
 throw Error('Priority/rating backend дэмжлэг баталгаажаагүй. Засвар хадгалагдаагүй.');
}
