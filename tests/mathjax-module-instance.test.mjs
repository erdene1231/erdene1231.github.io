import test from'node:test';import assert from'node:assert/strict';import fs from'node:fs';
const read=name=>fs.readFileSync(new URL('../'+name,import.meta.url),'utf8');
test('all public/native/tutorial consumers share one MathJax loader/queue module and refreshed cache chain',()=>{
 for(const name of['app.js','learning.js','problem-statement.js','problem-editorial.js','tutorial-editor.js']){const paths=[...read(name).matchAll(/from ['"]\.\/(tutorials\.js\?v=\d+)['"]/g)].map(m=>m[1]);assert.deepEqual(paths,['tutorials.js?v=97'],name);}
 for(const [file,imports]of[['app.js',['learning.js?v=97','problem-statement.js?v=97','problem-editorial.js?v=97','admin.js?v=97']],['admin.js',['problem-statement.js?v=97','problem-editorial.js?v=97']],['tutorials.js',['tutorial-editor.js?v=97']]])for(const path of imports)assert(read(file).includes("'./"+path+"'"),file+' cache '+path);
 assert(read('index.html').includes('src="app.js?v=97"'));
});
