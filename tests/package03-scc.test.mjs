import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {foundationDatabase,localOwnerGuard} from './package03-introduction-fixture.mjs';
import {sccPublicationSql} from '../tools/package03_scc_publication.mjs';
import {validateTutorial} from '../tutorial-model.js';import{publicationBody}from'../tutorial-publication.js';import{bodyHash,proposalProblems}from'../tools/package02_tutorial_proposals.mjs';import{mathProseWarnings}from'../math-prose.js';
const candidate=JSON.parse(fs.readFileSync('audit/package03-lessons/scc.json'));
test('chapter17 complete source partition/times,2SAT examples and explained reusable structs',()=>{
 const b=candidate.body;validateTutorial(b);assert.equal(bodyHash(b),candidate.reviewed_body_sha256);assert.deepEqual(mathProseWarnings(b),[]);assert.deepEqual(publicationBody(b,[b,...JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials.map(r=>r.body)],proposalProblems()),b);assert.deepEqual(b.sections.map(s=>s.key),['strong','kosaraju','2sat','application','practice']);assert.deepEqual(b.learningRelations.practice.map(p=>p.key),['383','382','384','385','761','802']);assert.deepEqual(b.learningRelations.practice.filter(p=>p.priority).map(p=>p.key),['383','384']);
 const parts=JSON.parse(fs.readFileSync('audit/package03-work/scc-code-parts.json'));
 for(const doc of[b,b.translations.en]){const all=doc.sections.flatMap(s=>s.blocks),codes=all.filter(x=>x.type==='code');let prev=-1;for(const name of['scc','2sat','coins']){const src=fs.readFileSync(`audit/package03-work/scc-${name}.cpp`,'utf8'),i=codes.findIndex(c=>c.text===src);assert(i>prev);assert.deepEqual(codes.slice(i-parts[name].length,i).map(c=>c.text),parts[name].map(p=>p.trim()));assert.equal(parts[name].join(''),src);prev=i;}const graphs=all.filter(b=>b.type==='diagram'&&b.kind==='graph');assert.equal(graphs.length,13);assert.deepEqual(graphs[2].edges,[['1','2'],['1','4'],['2','1'],['2','5'],['3','2'],['3','7'],['5','4'],['6','5'],['6','3'],['7','6']]);assert.deepEqual(graphs[4].edges,[['B','A'],['B','D'],['A','C'],['A','D'],['D','C']]);assert.deepEqual(graphs[5].nodes.map(n=>n.annotation),['1/8','2/7','9/14','4/5','3/6','11/12','10/13']);assert.deepEqual(graphs[12].edges,[['A','B'],['B','C'],['C','D']]);assert(!/the book|the source says|Номын|Номд /i.test(JSON.stringify(doc)));}
 const c=JSON.parse(fs.readFileSync('curriculum.json'));assert(c.order.indexOf('scc')>c.order.indexOf('topological-sort'));assert.deepEqual(c.lessons.scc.practice,b.learningRelations.practice);
});
test('SCC publication generator cannot expand the single new-ID scope',()=>{const bad=structuredClone(candidate);bad.id=bad.body.id='unexpected';bad.reviewed_body_sha256=bad.proposed_body_sha256=bodyHash(bad.body);assert.throws(()=>sccPublicationSql(bad,{}),/Exact reviewed/);});
async function guard(db){const g=await localOwnerGuard(db);return{...g,...(await db.query(`select (select count(*)::int from tutorial_catalog) catalog_count,(select md5(jsonb_agg(to_jsonb(t) order by id)::text)from tutorial_catalog t)catalog_fingerprint,(select md5(coalesce(jsonb_agg(to_jsonb(d)order by tutorial_id,editor_id)::text,'[]'))from tutorial_drafts d)all_drafts_fingerprint`)).rows[0]};}
async function snapshot(db){const x={};for(const t of['tutorial_catalog','tutorial_drafts','tutorial_changes','progress','learning_records','problem_catalog'])x[t]=(await db.query(`select * from ${t} order by to_jsonb(${t})::text`)).rows;return x;}
test('new SCC publication is atomic, rejects replay/drift, and preserves existing lessons, drafts and progress',async()=>{
 const{db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision)select 'complexity','00000000-0000-0000-0000-000000000002',body,10,revision from tutorial_catalog where id='complexity'");
  const before=await snapshot(db),g=await guard(db),sql=sccPublicationSql(candidate,g);
  await assert.rejects(db.exec(sql.replace('-- Atomic boundary: catalog and initial history exist together.',"RAISE EXCEPTION 'Injected insertion failure';")),/Injected insertion/);assert.deepEqual(await snapshot(db),before);
  const stale=sccPublicationSql(candidate,{...g,catalog_fingerprint:'0'.repeat(32)});await assert.rejects(db.exec(stale),/Catalog drift/);assert.deepEqual(await snapshot(db),before);
  await db.exec(sql);const after=await snapshot(db);for(const t of ['tutorial_drafts','progress','learning_records','problem_catalog'])assert.deepEqual(after[t],before[t]);assert.deepEqual(after.tutorial_catalog.filter(t=>t.id!=='scc'),before.tutorial_catalog);assert.equal(after.tutorial_changes.length,before.tutorial_changes.length+1);assert.deepEqual(after.tutorial_catalog.find(t=>t.id==='scc').body,candidate.body);
  await assert.rejects(db.exec(sql),/identity already used/);
 }finally{await db.close();}
});
test('new SCC cannot resurrect a tombstone or bypass publication validation',async()=>{
 const{db}=await foundationDatabase();try{
  await db.query("insert into tutorial_deleted_ids values('scc')");await assert.rejects(db.exec(sccPublicationSql(candidate,await guard(db))),/identity already used/);await db.query("delete from tutorial_deleted_ids where id='scc'");
  const bad=structuredClone(candidate);bad.body.sections[4].blocks.push({type:'problem',problemKey:'99999999'});bad.reviewed_body_sha256=bad.proposed_body_sha256=bodyHash(bad.body);await assert.rejects(db.exec(sccPublicationSql(bad,await guard(db))),/Unknown embedded problem/);assert.equal((await db.query("select count(*)::int n from tutorial_catalog where id='scc'")).rows[0].n,0);
 }finally{await db.close();}
});
