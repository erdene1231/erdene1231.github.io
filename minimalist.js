export function columnPreference(value){const n=Number(value);return[1,2,3].includes(n)?n:1;}
export function effectiveColumns(preference,width){return Math.min(columnPreference(preference),3,Math.max(1,Math.floor((Math.max(0,Number(width)||0)+16)/316)));}
export function statusPresentation(status){return status==='solved'?{icon:'✓',label:'Бодсон',color:'green'}:status==='trying'?{icon:'◷',label:'Оролдож байгаа',color:'yellow'}:{icon:'○',label:'Эхлээгүй',color:'red'};}
