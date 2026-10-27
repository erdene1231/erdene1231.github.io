// Public deployment capability declaration, not an authorization source.
// Keep 31 until separately approved migrations are installed and verified.
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
