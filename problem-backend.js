// Public deployment capability declaration, not an authorization source.
// Missing/unknown declarations fall back to31. Capability32 is provided by036;
// it does not imply the complete032 migration or optional033/034 are installed.
export function problemBackend(config=globalThis.window?.THINK_CP_CONFIG||{}) {
 const version=[31,32,33,34].includes(config.problemBackendVersion)?config.problemBackendVersion:31;
 const inlineStatement=version>=32&&config.problemStatementStorage==='catalog-inline-v1';
 return Object.freeze({version,priority:version>=32,editorial:version>=33,statement:version>=34||inlineStatement,bulkImport:version>=34,...(inlineStatement?{inlineStatement:true}:{})});
}
// Uses the table's existing SELECT privilege and active/admin row policy. No
// new reader RPC, credentials or grants are required by inline storage.
export async function readProblemStatement(client,id,capabilities=problemBackend()) {
 if(!capabilities.inlineStatement){const result=await client.rpc('get_problem_statement',{p_problem_id:id});if(result.error)throw result.error;return result.data;}
 const result=await client.from('problem_catalog').select('body,revision').eq('problem_id',id).maybeSingle();
 if(result.error)throw result.error;const row=result.data;if(!row?.body?.statement)return null;
 return{body:row.body.statement,provenance:row.body.statementProvenance,problemRevision:row.revision,revision:row.revision};
}
export async function requireInlineStatementBackend(client){
 // Both old and new validators reject this before any allocator/source/catalog
 // write. Only the native validator returns this precise capability marker.
 try{const{error}=await client.rpc('admin_save_problem',{p_body:{statement:null,statementProvenance:{capabilityProbe:true}},p_number:null,p_revision:null});if(error?.code==='22023'&&error.message?.includes('NATIVE_STATEMENT_PROVENANCE_WITHOUT_BODY'))return;}catch{}
 throw Error('Native statement backend баталгаажаагүй. Өөрчлөлт хадгалагдаагүй.');
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
