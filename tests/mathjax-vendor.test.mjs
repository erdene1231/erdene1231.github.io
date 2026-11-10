import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
test('optional MathJax components, fonts and speech maps match the pinned official distribution',()=>{
 const m=JSON.parse(fs.readFileSync('audit/mathjax-saved-settings/vendor.json'));
 assert.equal(m.package,'mathjax@3.2.2');assert.equal(m.files.length,47);
 for(const file of m.files){const bytes=fs.readFileSync('vendor/mathjax/'+file.path);assert.equal(bytes.length,file.bytes);assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),file.sha256,file.path);}
 assert(fs.readFileSync('vendor/mathjax/LICENSE','utf8').includes('Apache License'));
});
test('every current reverse importer shares the renderer singleton and fresh loader',()=>{
 const closure=JSON.parse(fs.readFileSync('audit/mathjax-saved-settings/cache-closure.json'));
 for(const file of fs.readdirSync('.').filter(p=>/\.(js|html)$/.test(p))){const text=fs.readFileSync(file,'utf8');for(const match of text.matchAll(/([\w.-]+\.js)\?v=(\d+)/g)){if(closure.includes(match[1]))assert.equal(match[2],'101',file+' -> '+match[1]);if(match[1]==='mathjax-loader.js')assert.equal(match[2],'3');}}
});
