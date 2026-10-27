import {priorityLevel,priorityRank,isHighPriority} from './priority.js?v=42';
export function ratingLabel(problem) {
  return problem.ratingKind==='unrated'||!Number.isFinite(problem.rating)?'Unrated':(problem.ratingKind==='estimated'?'≈ ':'')+problem.rating;
}
export function difficultyLabel(problem,lang='mn') {
  if(!Number.isFinite(problem.rating))return lang==='en'?'Unrated':'Түвшин тогтоогоогүй';
  const key=problem.difficultyCategory|| (problem.rating<=1100?'foundation':problem.rating<=1500?'standard':problem.rating<=1800?'observation':problem.rating<=2200?'challenge':'olympiad');
  const names={foundation:['Суурь','Foundation'],standard:['Стандарт','Standard'],observation:['Дунд шат','Intermediate'],challenge:['Ахисан шат','Advanced'],olympiad:['Олимпиадын түвшин','Olympiad']};
  return (names[key]||[key,key])[lang==='en'?1:0];
}
export function getTags(problems) {
  return [...new Set(problems.flatMap(p=>p.tags))].sort((a,b)=>a.localeCompare(b));
}
export function filterProblems(problems, progress, filters) {
  const words=(filters.query||'').trim().toLowerCase().split(/\s+/).filter(Boolean);
  const band=filters.ratingBand?filters.ratingBand.split('-').map(Number):null;
  const min=filters.minRating==null||filters.minRating===''?null:Number(filters.minRating),max=filters.maxRating==null||filters.maxRating===''?null:Number(filters.maxRating);
  if((min!==null&&(!Number.isInteger(min)||min<0||min>4000))||(max!==null&&(!Number.isInteger(max)||max<0||max>4000))||(min!==null&&max!==null&&min>max))return [];
  const result=problems.filter(p=>{
    const e=progress[p.id]||{status:'new',hints:0};
    const haystack=[p.title,p.ref,p.id,p.number,'#'+p.number,String(p.number).padStart(3,'0'),'#'+String(p.number).padStart(3,'0'),...p.tags].join(' ').toLowerCase();
    return (!filters.pack||p.pack===filters.pack)
      &&(!filters.source||p.source.toLowerCase()===filters.source.toLowerCase())
      &&(!filters.tag||p.tags.includes(filters.tag))
      &&(!filters.priorityLevel||priorityLevel(p)===filters.priorityLevel)
      &&(!filters.priorityOnly||isHighPriority(p))
      &&(!band||(Number.isFinite(p.rating)&&p.rating>=band[0]&&p.rating<=band[1]))
      &&(min===null||(Number.isFinite(p.rating)&&p.rating>=min))&&(max===null||(Number.isFinite(p.rating)&&p.rating<=max))
      &&(!filters.status||(filters.status==='hinted'?e.hints>0:e.status===filters.status))
      &&words.every(word=>/^#[0-9]+$/.test(word)?Number(p.number)===Number(word.slice(1)):haystack.includes(word));
  });
  return result.sort((a,b)=>{
    if(filters.sort==='number-asc')return a.number-b.number;
    if(filters.sort==='title')return a.title.localeCompare(b.title)||a.id.localeCompare(b.id);
    if(filters.sort==='priority'&&priorityRank(a)!==priorityRank(b))return priorityRank(b)-priorityRank(a);
    return (filters.sort==='rating-desc'?(b.rating??-1)-(a.rating??-1):(a.rating??Infinity)-(b.rating??Infinity))||a.title.localeCompare(b.title)||a.id.localeCompare(b.id);
  });
}
