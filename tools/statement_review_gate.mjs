import fs from'node:fs';import{canonicalKey}from'../learning-model.js';import{bodyHash}from'./part04_tutorial_proposals.mjs';
// Package-bank acceptance uses recorded semantic review, not a publication checkbox alone.
// This is a local curation gate, not an extra dependency of live admin publishing.
export function assertReviewedStatement(problem){
 const key=canonicalKey(problem),auditDirectory=new URL('../audit/',import.meta.url);let found;
 for(const file of fs.readdirSync(auditDirectory).filter(f=>/^PART04-STATEMENT-CONTENT[0-9]+-REVIEW[.]json$/.test(f))){const batch=JSON.parse(fs.readFileSync(new URL(file,auditDirectory)));const record=batch.records.find(r=>canonicalKey(r)===key);if(record){if(found)throw Error('Duplicate statement review: '+key);found={...record,verification:batch.verification};}}
 if(!found||!problem.statement||!problem.statementProvenance||(found.document_sha256!==bodyHash(problem.statement)||found.provenance_sha256!==bodyHash(problem.statementProvenance)))throw Error('Statement semantic review fingerprint missing/stale: '+key);
 if(['native_policy','reference_samples','browser','sql'].some(name=>found.verification?.[name]!=='passed'))throw Error('Statement verification pending: '+key);
 return found;
}
