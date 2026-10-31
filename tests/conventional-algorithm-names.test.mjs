import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {ledger,changes,candidate,baseline,editorialPublicationSql} from '../tools/conventional_algorithm_names.mjs';
import {bodyHash,proposalProblems} from '../tools/package02_tutorial_proposals.mjs';
import {validateTutorial} from '../tutorial-model.js';
import {publicationBody} from '../tutorial-publication.js';
import {mathProseWarnings} from '../math-prose.js';
import {foundationDatabase,localOwnerGuard} from './package03-introduction-fixture.mjs';
const read=name=>JSON.parse(fs.readFileSync('audit/conventional-names/'+name));
const entries=ledger().lessons,docs=entries.map(x=>candidate(x.id)),diffs=changes();
const special=new Map();
const math=s=>s.match(/\$[^$]+\$/g)||[],numbers=s=>s.match(/\d+(?:[.,]\d+)*/g)||[];
function inspect(a,b,id,path='',totals={code:0,math:0,diagrams:0,tables:0}){
 assert.equal(typeof a,typeof b,id+':'+path);
 if(Array.isArray(a)){assert.equal(a.length,b.length,path);a.forEach((v,i)=>inspect(v,b[i],id,path+`[${i}]`,totals));}
 else if(a&&typeof a==='object'){
  assert.deepEqual(Object.keys(a),Object.keys(b),path);
  if(a.marks?.includes('code'))assert.deepEqual(a,b,path);
  if(a.type==='code'){assert.deepEqual(a,b,path);totals.code++;}
  if(a.type==='math'){assert.deepEqual(a,b,path);totals.math++;}
  if(['graph','grid','array'].includes(a.kind)){for(const k of Object.keys(a))if(k!=='caption')assert.deepEqual(a[k],b[k],path+'.'+k);totals.diagrams++;}
  if(a.type==='table')totals.tables++;
  for(const k of Object.keys(a))inspect(a[k],b[k],id,path?path+'.'+k:k,totals);
 }else if(a!==b){
  const d=diffs.find(x=>x.id===id&&x.path===path);assert(d,'Unreviewed field '+id+':'+path);assert.equal(d.before,a);assert.equal(d.after,b);
  assert(!/(^|\.)(id|key|type|kind|language|order|priority|priorityLevel|number|problemId|problemKey|stage|next|url|href|detailKey|marks)(\[|$)/.test(path),'Protected metadata '+path);
  if(JSON.stringify(math(a))!==JSON.stringify(math(b))||JSON.stringify(numbers(a))!==JSON.stringify(numbers(b))){const e=special.get(id+':'+path);assert(e,'Unreviewed math/numeric delta');assert.equal(e.before,a);assert.equal(e.after,b);assert(e.review.length>30);}
 }
 return totals;
}
test('all 73 contextual reviews preserve executable bytes, formula blocks, diagrams, numerical examples and native structure',()=>{
 assert.equal(entries.length,73);assert.equal(new Set(entries.map(x=>x.id)).size,73);assert.equal(entries.filter(x=>x.status==='reviewed-changed').length,48);assert.equal(entries.filter(x=>x.status==='reviewed-unchanged').length,25);assert.equal(entries.find(x=>x.id==='hash-compression').status,'reviewed-unchanged');
 const totals={code:0,math:0,diagrams:0,tables:0};
 for(const e of entries){const a=baseline(e.id),b=candidate(e.id);assert.equal(bodyHash(a),e.baseline_body_sha256);assert.equal(bodyHash(b),e.candidate_body_sha256);inspect(a,b,e.id,'',totals);assert.deepEqual(a.translations,b.translations);validateTutorial(b);const expected=structuredClone(b);if(expected.learningRelations&&!Object.hasOwn(expected.learningRelations,'next'))expected.learningRelations.next=null;assert.deepEqual(publicationBody(b,docs,proposalProblems()),expected,e.id);assert.deepEqual(mathProseWarnings(b),mathProseWarnings(a),e.id);assert.deepEqual(a.sections.map(x=>x.key),b.sections.map(x=>x.key));assert.deepEqual(a.learningRelations.practice.map(x=>[x.key,x.stage]),b.learningRelations.practice.map(x=>[x.key,x.stage]));}
 assert.deepEqual(totals,{code:2498,math:362,diagrams:770,tables:410});
 const compiled=JSON.parse(fs.readFileSync('audit/PACKAGE03-FINAL-COMPILE.json'));assert.equal(compiled.status,'passed');const known=new Set(compiled.program_results.filter(x=>x.passed).map(x=>x.sha256)),programs=new Set();
 for(const b of docs)for(const d of[b,b.translations.en])for(const s of d.sections)for(const c of s.blocks)if(c.type==='code'&&/\bint\s+main\s*\(/.test(c.text)&&/#include/.test(c.text)){const h=crypto.createHash('sha256').update(c.text).digest('hex');if(known.has(h))programs.add(h);}
 assert.equal(programs.size,241);
});
test('conventional names and requested math terminology remain contextual and distinct',()=>{
 for(const [id,name]of [['stack-queue','Stack'],['two-pointers','Two Pointers'],['monotonic-stack','Monotonic stack'],['greedy','Greedy'],['knapsack','Knapsack'],['dynamic-programming','DP'],['sliding-window','Sliding Window'],['string-hashing','Rolling Hash'],['kmp','Hash'],['bitmask-dp','Bitmask DP'],['brute-force','Brute Force']])assert(candidate(id).title.includes(name),id);
 assert(candidate('two-pointers').sections[2].title.includes('Monotonic queue'));
 assert(candidate('sliding-window').sections[4].title.includes('Monotonic queue'));
 assert(candidate('binary-search-answer').sections[1].title.includes('монотон'));
 assert.deepEqual(candidate('hash-compression'),baseline('hash-compression'));
 assert.equal(candidate('lca').sections[1].blocks[9].caption,baseline('lca').sections[1].blocks[9].caption);
 assert(candidate('dynamic-programming').sections[0].blocks[0].text.includes('DP (Dynamic Programming)'));
 assert(candidate('bitmask-dp').sections[0].blocks[0].text.includes('битийн маск'));
 assert(candidate('kmp').sections[3].blocks[0].text.includes('тоон хураангуй'));

 const intro=candidate('introduction').sections[4].blocks[28].text;for(const t of['Доошоо тоймлох','Дээшээ тоймлох','Тоймлох (round)','бутархай хэсгийг таслах','std::round(2.5) = 3','std::round(-2.5) = -3'])assert(intro.includes(t));
 for(const b of docs){const mn=structuredClone(b);delete mn.translations;assert(!/томъёо|дугуйруул|рекурс(?:ив)? томьёо/.test(JSON.stringify(mn)),b.id);}
 assert(candidate('sorting').sections[0].blocks[1].text.includes('үл буурах дараалал'));
 assert(candidate('scc').sections[2].blocks[16].content.map(x=>x.text).join('').includes('өөр компонентуудыг холбосон'));
 assert(candidate('aho-corasick').sections[3].blocks[0].content.map(x=>x.text).join('').includes('үл буурах'));
});
async function payload(db,ids){const targets=[];for(const id of ids){const e=entries.find(x=>x.id===id),r=(await db.query('select revision,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];targets.push({id,expected_revision:r.revision,expected_published:true,expected_body_md5:r.body_md5,expected_body_sha256:e.baseline_body_sha256,reviewed_body_sha256:e.candidate_body_sha256,proposed_body_sha256:e.candidate_body_sha256,body:candidate(id)});}const guard={...await localOwnerGuard(db,[...ids].sort()),...(await db.query(`select (select count(*)::int from tutorial_catalog)catalog_count,(select md5(jsonb_agg(to_jsonb(t)order by id)::text)from tutorial_catalog t)catalog_fingerprint,(select md5(coalesce(jsonb_agg(to_jsonb(d)order by tutorial_id,editor_id)::text,'[]'))from tutorial_drafts d)all_drafts_fingerprint`)).rows[0]};return {batch:{targets},guard};}
test('16 bounded name-review batches validate all 48 replacements and preserve drafts, unchanged lessons and learner data',async()=>{
 const{db}=await foundationDatabase();try{
  // Local synthetic database only: seed a mutually linked catalog before enabling publication validation.
  await db.exec('alter table tutorial_catalog disable trigger publication_check');
  for(const e of entries.filter(x=>!['mongolia'].includes(x.id)))await db.query('insert into tutorial_catalog(id,body,revision,published)values($1,$2,$3,false)on conflict(id)do nothing',[e.id,baseline(e.id),e.baseline_revision]);
  for(const e of entries)await db.query('insert into tutorial_catalog(id,body,revision,published)values($1,$2,$3,true)on conflict(id)do update set body=excluded.body,revision=excluded.revision,published=true',[e.id,baseline(e.id),e.baseline_revision]);
  await db.exec('alter table tutorial_catalog enable trigger publication_check');
  for(const e of entries.slice(0,8))await db.query('insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision)values($1,$2,$3,2,$4)',[e.id,'00000000-0000-0000-0000-000000000002',baseline(e.id),e.baseline_revision]);
  const protectedSnap=async()=>{const o={};for(const t of ['tutorial_drafts','progress','learning_records','problem_catalog'])o[t]=(await db.query(`select * from ${t} order by to_jsonb(${t})::text`)).rows;o.unchanged=(await db.query("select * from tutorial_catalog where id not in ('complexity','brute-force','sorting','recursion','stack-queue','set-map','prefix-sums-2d','two-pointers','bit-operations','graph-basics','bfs','dfs','flood-fill','greedy','binary-search-answer','tree-basics','dynamic-programming','probability','game-theory','grid-dp','knapsack','lis','sqrt-algorithms','monotonic-stack','kruskal','priority-queue','bridges-articulation','dijkstra','floyd-warshall','heavy-light-decomposition','centroid-decomposition','topological-sort','digit-dp','combinatorics','kmp','lca','paths-circuits','bitmask-dp','flows-cuts','scc','sliding-window','connected-components','bipartite','interval-dp','tree-dp','bellman-ford','string-hashing','invariant') order by id")).rows;return o;};const before=await protectedSnap();
  const ids=entries.filter(x=>x.status==='reviewed-changed').map(x=>x.id).sort();let batches=0;
  for(let i=0;i<ids.length;i+=3){const{batch,guard}=await payload(db,ids.slice(i,i+3)),sql=editorialPublicationSql(batch,guard);
   if(i===0){const snap=(await db.query('select * from tutorial_catalog order by id')).rows;
    await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"RAISE EXCEPTION 'Injected editorial failure';")),/Injected editorial failure/);assert.deepEqual((await db.query('select * from tutorial_catalog order by id')).rows,snap);
    await assert.rejects(db.exec(editorialPublicationSql(batch,{...guard,all_drafts_fingerprint:'0'.repeat(32)})),/All private draft drift/);
    await assert.rejects(db.exec(editorialPublicationSql(batch,{...guard,catalog_fingerprint:'0'.repeat(32)})),/Catalog drift/);
    const bad=structuredClone(batch);bad.targets[0].body.summary+=' Unreviewed';assert.throws(()=>editorialPublicationSql(bad,guard),/Exact conventional-name/);
    assert.throws(()=>editorialPublicationSql({targets:[...batch.targets,batch.targets[0]]},guard),/allowlist/);
    assert.throws(()=>editorialPublicationSql({targets:[{...batch.targets[0],id:'dsu'}]},guard),/Exact conventional-name/);
   }
   await db.exec(sql);await assert.rejects(db.exec(sql),/Catalog drift|CAS\/body\/status drift/);batches++;
  }
  assert.equal(batches,16);assert.deepEqual(await protectedSnap(),before);assert.equal((await db.query('select count(*)::int n from tutorial_changes')).rows[0].n,48);
  for(const id of ids){const r=(await db.query('select body,revision from tutorial_catalog where id=$1',[id])).rows[0],e=entries.find(x=>x.id===id);assert.deepEqual(r.body,candidate(id));assert.equal(r.revision,e.baseline_revision+1);}
 }finally{await db.close();}
});
