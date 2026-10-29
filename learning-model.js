// Shared, DOM-free relationships and statistics. Problem IDs remain unchanged.
export const CHECKS = ['purpose', 'correctness', 'complexity', 'implementation', 'mistakes'];
export function canonicalKey(problem) {
  try {
    const url = new URL(problem.url);
    const match = url.pathname.match(/^\/problemset\/task\/(\d+)\/?$/);
    if (url.hostname === 'cses.fi' && match) return 'cses|' + match[1];
  } catch {}
  return String(problem.source).trim().toLowerCase() + '|' + String(problem.ref).trim().toLowerCase();
}
export function problemReferenceKey(problem){return Number.isSafeInteger(problem.number)&&problem.number>0?String(problem.number):canonicalKey(problem);}
export function normalizeProblemReferences(value,problems){const idx=problemIndex(problems),copy=structuredClone(value);const key=k=>idx.has(String(k))?problemReferenceKey(idx.get(String(k))):k;function walk(v){if(!v||typeof v!=='object')return;if(v.type==='problem')v.problemKey=key(v.problemKey);if(v.learningRelations?.practice)for(const p of v.learningRelations.practice)p.key=key(p.key);if(typeof v._draftRelationsText==='string')try{const r=JSON.parse(v._draftRelationsText);for(const p of r.practice||[])p.key=key(p.key);v._draftRelationsText=JSON.stringify(r,null,2);}catch{}for(const x of Object.values(v))if(x&&typeof x==='object')walk(x);}walk(copy);return copy;}
export function problemIndex(problems) {
  const index = new Map();
  for (const p of problems) { index.set(p.id, p);if(Number.isSafeInteger(p.number)&&p.number>0)index.set(String(p.number),p); if (!index.has(canonicalKey(p))) index.set(canonicalKey(p), p); }
  return index;
}
export function resolvePractice(list, problems) {
  const index = problemIndex(problems);
  return list.map(row => ({...row, problem: index.get(row.key) || index.get(row.problemId)}));
}
export function tutorialMastery(id, record, practice, progress) {
  const confirmed = CHECKS.every(key => (record?.checks || []).includes(key));
  const priority = practice.filter(row => row.priority);
  return {read: (record?.readSections || []).length > 0, confirmed,
    mastered: confirmed && priority.length > 0 && priority.every(row => row.problem && progress[row.problem.id]?.status === 'solved')};
}
export function dayCompletion(day, index, records, progress, checks = []) {
  const required = day.required.map(key => index.get(key));
  const missing = required.some(p => !p), solved = required.filter(p => p && progress[p.id]?.status === 'solved').length;
  const understood = day.tutorials.every(id => CHECKS.every(c => (records[id]?.checks || []).includes(c)));
  return {missing, solved, total: required.length,
    complete: !missing && solved === required.length && understood && day.checklist.every((_, i) => checks.includes(i))};
}
export function dateKey(date, timeZone = 'Asia/Ulaanbaatar') {
  const parts = Object.fromEntries(new Intl.DateTimeFormat('en-CA', {timeZone, year:'numeric', month:'2-digit', day:'2-digit'}).formatToParts(new Date(date)).map(p => [p.type, p.value]));
  return `${parts.year}-${parts.month}-${parts.day}`;
}
export function addDays(key, n) { const d = new Date(key + 'T12:00:00Z'); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); }
export function monday(key) { return addDays(key, -(new Date(key + 'T12:00:00Z').getUTCDay() + 6) % 7); }
export function withArchivedProblems(problems, progress) {
  const known=new Set(problems.map(p=>p.id));
  const archived=Object.entries(progress).filter(([id,row])=>!known.has(id)&&['trying','solved'].includes(row.status)).map(([id])=>({id,title:'Идэвхгүй бодлого · '+id,rating:null,ratingKind:'unrated',tags:[],archived:true}));
  return problems.concat(archived);
}
export function buildStatistics(problems, progress, dates = {}, today = dateKey(new Date())) {
  const solved = problems.filter(p => progress[p.id]?.status === 'solved'), trying = problems.filter(p => progress[p.id]?.status === 'trying');
  const activity = new Map(), ratings = new Map(), tags = new Map(); let unknownDate = 0, unrated = 0;
  for (const p of solved) {
    const stamp = dates[p.id]?.first_solved_at;
    if (stamp && !Number.isNaN(Date.parse(stamp))) { const key = dateKey(stamp); activity.set(key, (activity.get(key) || 0) + 1); } else unknownDate++;
    if (Number.isFinite(p.rating) && p.ratingKind !== 'unrated') { const key = p.ratingKind + '|' + p.rating; ratings.set(key, (ratings.get(key) || 0) + 1); } else unrated++;
    for (const tag of new Set(p.tags || [])) tags.set(tag, (tags.get(tag) || 0) + 1);
  }
  const keys = [...activity.keys()].sort(); let longest = 0, run = 0, previous;
  for (const key of keys) { run = previous === addDays(key, -1) ? run + 1 : 1; longest = Math.max(longest, run); previous = key; }
  let current = 0, key = activity.has(today) ? today : addDays(today, -1);
  while (activity.has(key)) { current++; key = addDays(key, -1); }
  const within = n => keys.filter(k => k >= addDays(today, 1-n) && k <= today).reduce((sum,k) => sum + activity.get(k), 0);
  return {solved, trying, activity, ratings, tags, unrated, unknownDate, current, longest, last7: within(7), last30: within(30), last365: within(365)};
}
export function weekStatistics(stats, dates, start) {
  const end = addDays(start, 7), inWeek = s => s && !Number.isNaN(Date.parse(s)) && dateKey(s) >= start && dateKey(s) < end;
  const solved = stats.solved.filter(p => inWeek(dates[p.id]?.first_solved_at));
  const attempted = [...stats.solved, ...stats.trying].filter(p => inWeek(dates[p.id]?.first_attempted_at));
  const rated = solved.filter(p => Number.isFinite(p.rating) && p.ratingKind !== 'unrated');
  return {solved, attempted, highest: rated.length ? Math.max(...rated.map(p => p.rating)) : null,
    average: rated.length ? Math.round(rated.reduce((sum,p) => sum + p.rating, 0) / rated.length) : null};
}
export function validateRelations(value, topicId, topics, problems) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('Relationship object шаардлагатай.');
  const ids = new Set(topics.map(t => t.id)), index = problemIndex(problems), stages = ['Warm-up','Standard','Observation','Application','Challenge','Olympiad extension'];
  const checkId = id => { if (id === topicId || !ids.has(id)) throw new Error('Published tutorial ID-гаа шалгана уу: ' + id); };
  if (!Array.isArray(value.variants) || value.variants.length > 20 || !Array.isArray(value.practice) || value.practice.length > 30) throw new Error('Variants 0–20, practice 0–30 байна.');
  for (const v of value.variants) { checkId(v.tutorialId); for (const field of ['description','descriptionEn']) if (v[field]!==undefined&&(typeof v[field] !== 'string' || v[field].length > 1000)) throw new Error('Variant-ийн хоёр хэлний тайлбар шаардлагатай.'); }
  if (value.next) checkId(value.next);
  const seen = new Set();
  for (const row of value.practice) { if (!index.has(row.key) || seen.has(row.key)) throw new Error('Practice key байхгүй эсвэл давхардсан: ' + row.key); seen.add(row.key); if (!stages.includes(row.stage) || typeof row.priority !== 'boolean') throw new Error('Practice stage / priority буруу.'); if (row.reason!==undefined&&(typeof row.reason !== 'string' || row.reason.length > 1000)) throw new Error('Priority сонголтын үндэслэл шаардлагатай.'); }
  return {variants:value.variants.map(v => ({tutorialId:v.tutorialId,description:(v.description||'').trim(),descriptionEn:(v.descriptionEn||'').trim()})), next:value.next || null,
    practice:value.practice.map(row => ({key:row.key,stage:row.stage,priority:row.priority,reason:row.priority ? (row.reason||'').trim() : ''}))};
}
export function stableStringify(value) { if (Array.isArray(value)) return '[' + value.map(stableStringify).join(',') + ']'; if (value && typeof value === 'object') return '{' + Object.keys(value).sort().map(key => JSON.stringify(key) + ':' + stableStringify(value[key])).join(',') + '}'; return JSON.stringify(value); }
export async function bodyHash(value) { const result = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(stableStringify(value))); return [...new Uint8Array(result)].map(x => x.toString(16).padStart(2,'0')).join(''); }
let contentPromise;
export function loadLearningContent() {
  return contentPromise ??= Promise.all(['curriculum.json','study-plan.json','tutorial-editions.json','learning-problems.json'].map(async name => { const response = await fetch('./' + name + (name==='curriculum.json'?'?v=75':'?v=23')); if (!response.ok) throw new Error('Сургалтын агуулга ачаалсангүй.'); return response.json(); })).then(([curriculum,plan,editions,catalog]) => {if(!Array.isArray(curriculum.order)||!curriculum.lessons||!Array.isArray(plan.days)||plan.days.length!==100||!editions.editions||!Array.isArray(catalog.problems))throw new Error('Сургалтын агуулгын бүтэц буруу байна.');return {curriculum,plan,editions,catalog};});
}
