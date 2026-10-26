// Offline reference reconstruction. Never connects to production.
import {PGlite} from '@electric-sql/pglite';
import fs from 'node:fs';
const root=new URL('../',import.meta.url);
const read=p=>fs.readFileSync(new URL(p,root),'utf8');
const db=new PGlite();
await db.exec(`
create role anon; create role authenticated; create role service_role;
create schema auth; create schema storage;
create table auth.users(id uuid primary key,email text,created_at timestamptz default now());
create function auth.uid() returns uuid language sql stable as $$select null::uuid$$;
create table storage.buckets(id text primary key,name text,public boolean,file_size_limit bigint,allowed_mime_types text[]);
create table storage.objects(id uuid,bucket_id text,name text,created_at timestamptz,metadata jsonb);
create function storage.foldername(text) returns text[] language sql immutable as $$select string_to_array($1,'/')$$;
-- Supabase default grants, before the repository's explicit revocations.
alter default privileges in schema public grant all on tables to anon,authenticated,service_role;
alter default privileges in schema public grant all on sequences to anon,authenticated,service_role;
alter default privileges in schema public grant all on functions to anon,authenticated,service_role;
`);
// Split PostgreSQL statements without splitting quoted bodies or strings.
function statements(sql){
 let out=[],start=0,i=0,quote=null;
 while(i<sql.length){
  if(quote){if(sql.startsWith(quote,i)){if(quote==="'"&&sql[i+1]==="'"){i+=2;continue;}i+=quote.length;quote=null;}else i++;continue;}
  if(sql.startsWith('--',i)){const e=sql.indexOf('\n',i);i=e<0?sql.length:e+1;continue;}
  if(sql.startsWith('/*',i)){let depth=1;i+=2;while(depth&&i<sql.length){if(sql.startsWith('/*',i)){depth++;i+=2;}else if(sql.startsWith('*/',i)){depth--;i+=2;}else i++;}continue;}
  if(sql[i]==="'"||sql[i]==='"'){quote=sql[i++];continue;}
  const dollar=sql.slice(i).match(/^\$(?:[a-zA-Z_][a-zA-Z_0-9]*)?\$/);if(dollar){quote=dollar[0];i+=quote.length;continue;}
  if(sql[i]===';'){out.push(sql.slice(start,i+1));start=i+1;}i++;
 }
 return out;
}
const files=['schema.sql',...fs.readdirSync(new URL('supabase/',root)).filter(f=>/^\d+.*\.sql$/.test(f)).sort()];
for(const file of files){
 for(const stmt of statements(read('supabase/'+file))){
  const clean=stmt.replace(/--[^\n]*/g,'').trim();
  // Only DDL/ACL. No seed imports, DO blocks, application RPCs or data updates.
  if(!/^(create|alter|drop|grant|revoke)\b/i.test(clean))continue;
  try{await db.exec(stmt);}catch(e){console.error(file,e.message);process.exit(1);}
 }
}
const expected=(await db.query(read('supabase/audit/catalog.sql'))).rows[0].catalog;
const actual=JSON.parse(read(process.argv[2] || 'supabase/audit/production-after-025.json'));
const differences={};
// ACL ordering is irrelevant; PGlite bootstrap and production owners differ.
function normalize(v){
 if(Array.isArray(v))return v.map(normalize);
 if(v&&typeof v==='object')return Object.fromEntries(Object.entries(v).sort().map(([k,x])=>[k,normalize(x)]));
 if(typeof v==='string')return v.replaceAll('\r\n','\n');
 return v;
}
for(const kind of Object.keys(expected)){
 const changes=[];
 const key=r=>kind==='columns'?r.table_schema+'.'+r.table_name+'.'+r.column_name:
  kind==='constraints'?r.schema+'.'+r.table_name+'.'+r.conname:
  kind==='indexes'?r.schemaname+'.'+r.indexname:
  kind==='policies'?r.schemaname+'.'+r.tablename+'.'+r.policyname:
  kind==='triggers'?r.schema+'.'+r.table_name+'.'+r.tgname:
  kind==='functions'?r.schema+'.'+r.name+'('+r.arguments+')':kind==='views'?r.schemaname+'.'+r.viewname:r.schema+'.'+r.name;
 // PostgreSQL 18 catalogs NOT NULL constraints separately; compare nullability via columns.
 const comparable=rows=>(rows||[]).filter(r=>kind!=='constraints'||r.contype!=='n');
 const wanted=new Map(comparable(expected[kind]).map(r=>[key(r),r])),live=new Map(comparable(actual[kind]).map(r=>[key(r),r]));
 for(const k of new Set([...wanted.keys(),...live.keys()])){
  const a=wanted.get(k),b=live.get(k);
  if(!a||!b){changes.push({object:k,status:a?'missing':'extra'});continue;}
  for(const field of Object.keys(a)){
   let x=a[field],y=b[field];
   if(field==='relacl'||field==='proacl'){
    const acl=s=>(s||'').replace(/[{}]/g,'').split(',').map(x=>x.replace(/(?:postgres|supabase_admin)/g,'OWNER')).sort();x=acl(x);y=acl(y);
   }
   if(JSON.stringify(normalize(x))!==JSON.stringify(normalize(y)))changes.push({object:k,field,expected:x,actual:y});
  }
 }
 differences[kind]=changes;
}
fs.writeFileSync(new URL('supabase/audit/comparison.json',root),JSON.stringify(differences,null,2)+'\n');
console.log(Object.fromEntries(Object.entries(differences).map(([k,v])=>[k,v.length])));
await db.close();

if(Object.values(differences).some(changes=>changes.length))process.exitCode=1;
