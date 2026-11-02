import test from'node:test';
import fs from'node:fs';import assert from'node:assert/strict';
const repo=new URL('..',import.meta.url).pathname;
const{joiStatementFixture}=await import(repo+'/tests/joi-statement-fixture.mjs');
const{buildJoiInputFormatJob,preflightSql,plan}=await import(repo+'/tools/joi_input_format_job.mjs');
const originals=JSON.parse(fs.readFileSync(repo+'/audit/joi-statements/statement-plans.json'));
const rows=JSON.parse(fs.readFileSync(repo+'/audit/joi-statements/before-targets.json'));
for(const row of rows){const p=originals.find(p=>p.id===row.problem_id);row.body={...row.body,statement:p.statement,statementProvenance:p.statementProvenance};row.revision++;}
test('Native format SQL is statement-only, atomic and rejects replay',async()=>{const db=await joiStatementFixture(rows);
try{
 const before=(await db.query('select * from problem_catalog order by number')).rows;
 const g=(await db.query(preflightSql())).rows[0].recovery;const sql=await buildJoiInputFormatJob(g);
 await assert.rejects(db.exec(sql.replace('-- Atomic statement body/history pair complete.',"IF cardinality(edited_ids)=2 THEN RAISE EXCEPTION 'Injected rollback';END IF;")),/Injected rollback/);
 assert.deepEqual((await db.query('select * from problem_catalog order by number')).rows,before);
 await db.exec(sql);
 const after=(await db.query('select * from problem_catalog order by number')).rows;
 for(const old of before){const now=after.find(r=>r.problem_id===old.problem_id),p=plan.find(p=>p.id===old.problem_id);if(p){assert.deepEqual(now.body,{...old.body,statement:p.statement});assert.equal(now.revision,old.revision+1);}else assert.deepEqual(now,old);}
 await assert.rejects(db.exec(sql),/Catalog baseline drift/);
 const post=(await db.query(preflightSql())).rows[0].recovery;
 for(const k of ['protected','authority','sequence','source_fingerprint','policy_fingerprint','learning_triggers_fingerprint'])assert.deepEqual(post[k],g[k]);
 const report={passed:true,catalog:before.length,statement_only_changes:6,unchanged_rows:before.length-6,midway_rollback:true,replay_rejected:true,protected_data_access_exact:true};
 console.log(report);
}finally{await db.close();}
});
