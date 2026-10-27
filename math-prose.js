// Advisory prose lint, not a TeX parser or a substitute for semantic review.
// Whole words avoid ordinary language/identifiers; code, links and delimited math
// are excluded. Existing documents are never rewritten by this module.
const mathOrCode=/\$\$[\s\S]*?\$\$|(?<!\\)\$(?:\\.|[^$\\])*\$|\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]|`[^`]*`|https?:\/\/\S+/g;
const bare=/(?<![A-Za-z0-9_])(?:[nNmMLRrkKxXyYiIjJuUvVwWfFdD]|[LRnm]_[A-Za-z0-9{}]+)(?![A-Za-z0-9_])/g;
export function mathProseWarnings(document){
 const found=[];const check=(text,path)=>{for(const m of String(text||'').replace(mathOrCode,' ').matchAll(bare))found.push({path,variable:m[0]});};
 for(const [lang,body]of[['mn',document],['en',document.translations?.en]]){if(!body)continue;
  for(const [si,section]of(body.sections||[]).entries())for(const [bi,b]of(section.blocks||[]).entries()){
   const path=lang+'.sections['+si+'].blocks['+bi+']';if(['p','note','quote','callout'].includes(b.type))check(b.text,path);
   if(b.content){let run='';for(const r of b.content){if(r.marks?.includes('code')||r.href){check(run,path);run='';}else run+=r.text||'';}check(run,path);}
   if(['list','ordered','checklist'].includes(b.type))for(const item of b.items||[])check(typeof item==='string'?item:item.text,path);
   if(b.type==='table'){for(const text of b.headers||[])check(text,path);for(const row of b.rows||[])for(const text of row)check(text,path);}
  }
 }
 return found;
}
