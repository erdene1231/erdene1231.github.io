import test from'node:test';import assert from'node:assert/strict';import{mathProseWarnings}from'../math-prose.js';
test('prose lint finds variables, preserves code/URLs/identifiers and recognizes inline/display delimiters',()=>{
 const doc={sections:[{blocks:[{type:'p',text:'Use L and R for n elements.'},{type:'p',text:'$L$ and \\(n\\), $$m$$, \\[R\\], https://example.com/n/ and `m`.'},{type:'rich',content:[{text:'n',marks:['code']},{text:'R',href:'https://example.com'},{text:' $m$ and ordinary names, minimum, normal.'}]},{type:'code',text:'int n,m; cout << n;'}]}]};
 assert.deepEqual(mathProseWarnings(doc).map(w=>w.variable),['L','R','n']);
});

test('Unicode proper names are whole words while real standalone variables remain flagged',()=>{const doc={sections:[{blocks:[{type:'p',text:'Kőnig, König, Монгол and $n$; n, L and R.'}]}]};assert.deepEqual(mathProseWarnings(doc).map(w=>w.variable),['n','L','R']);});
