// Independent document bases share the existing problem CAS, without rebasing
// a different panel after an external reload or discarding its unsaved text.
export function problemMetadata(problem){
 if(!problem)return null;
 const copy=structuredClone(problem),hasStatement=Object.hasOwn(copy,'statement')?!!copy.statement:copy.hasStatement===true,hasEditorial=Object.hasOwn(copy,'editorial')?!!copy.editorial:copy.hasEditorial===true;
 delete copy.statement;delete copy.statementProvenance;delete copy.editorial;
 return{...copy,hasStatement,hasEditorial};
}
export function documentSavePayload(base,kind,document,provenance){
 if(!['statement','editorial'].includes(kind)||!base?.id)throw Error('Хадгалсан бодлого сонгоно уу.');
 const payload={...problemMetadata(base),[kind]:structuredClone(document)};
 if(kind==='statement'&&document)payload.statementProvenance=structuredClone(provenance);
 return payload;
}
export function createProblemDocumentBases(){
 let metadata=null,documents={statement:null,editorial:null};
 function reset(problem){metadata=problemMetadata(problem);documents={statement:problemMetadata(problem),editorial:problemMetadata(problem)};}
 function reload(kind,problem){if(!['statement','editorial'].includes(kind)||problem?.id!==metadata?.id)throw Error('Document target changed');documents[kind]=problemMetadata(problem);}
 function saved(kind,problem){
  const next=problemMetadata(problem);if(!metadata){reset(next);return next;}
  const previous=kind==='metadata'?metadata:documents[kind];if(!previous||previous.id!==next.id)throw Error('Document target changed');
  const sameBase=p=>p?.id===previous.id&&p.revision===previous.revision;
  if(sameBase(metadata))metadata=next;
  for(const key of['statement','editorial'])if(sameBase(documents[key]))documents[key]=next;
  if(kind!=='metadata')documents[kind]=next;
  return metadata;
 }
 return{reset,reload,saved,metadata:()=>metadata,document:kind=>documents[kind]};
}
