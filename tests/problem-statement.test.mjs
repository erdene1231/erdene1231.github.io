import test from'node:test';import assert from'node:assert/strict';import fs from'node:fs';
import{assertProblemStatementReady}from'../problem-statement-policy.js';import{validateProblem}from'../problem-store.js';
const rows=JSON.parse(fs.readFileSync('audit/PART04-REVIEWED-NEW-TASKS.json')).filter(p=>p.statement);
test('native bilingual statements and provenance round-trip without mutating samples or exposing solution fields',()=>{
 assert.equal(rows.length,2);for(const p of rows){const before=JSON.stringify(p);assertProblemStatementReady(p);const normalized=validateProblem({...p,tags:['implementation']});assert.deepEqual(normalized.statement,p.statement);assert.deepEqual(normalized.statementProvenance,p.statementProvenance);assert.equal(JSON.stringify(p),before);assert(!JSON.stringify(p.statement).includes('editorial-cf'));}
});
test('statement completeness, rights, dates, literal bilingual samples and safe native schema fail closed',()=>{
 const base=rows[0];for(const mutate of[p=>delete p.statement,p=>delete p.statement.translations,p=>p.statement.translations.en.sections.pop()&&p.statement.translations.en.sections.pop(),p=>p.statement.translations.en.sections[4].blocks.find(b=>b.type==='code').text+='changed',p=>p.statementProvenance.sourceUrl='javascript:alert(1)',p=>delete p.statementProvenance.sourceSha256,p=>p.statementProvenance.rightsBasis='unknown',p=>p.statementProvenance.rightsBasis='licensed',p=>p.statementProvenance.reviewedAt='2026-02-30',p=>p.statementProvenance.checks.translation=false,p=>p.statement.sections[0].blocks=[{type:'html',text:'<script>bad</script>'}]]){const copy=structuredClone(base);mutate(copy);assert.throws(()=>assertProblemStatementReady(copy));}
 const licensed=structuredClone(base);licensed.statementProvenance.rightsBasis='licensed';licensed.statementProvenance.rightsReference='https://example.com/permission';assert.doesNotThrow(()=>assertProblemStatementReady(licensed));
});
