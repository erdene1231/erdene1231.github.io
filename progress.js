export const EMPTY = {status:'new', hints:0, notes:''};
export function cleanEntry(value) {
  if (!value || !['new','trying','solved'].includes(value.status) || !Number.isInteger(value.hints) || value.hints < 0 || value.hints > 3 || typeof value.notes !== 'string' || value.notes.length > 5000) throw new Error('Progress-ийн бүтэц буруу байна.');
  return {status:value.status,hints:value.hints,notes:value.notes};
}
export function parseBackup(value, ids) {
  if (value?.version !== 1 || !value.progress || Array.isArray(value.progress) || typeof value.progress !== 'object') throw new Error('Think CP-ийн progress файл сонгоно уу.');
  const result = {};
  for (const [id, entry] of Object.entries(value.progress)) {
    if (!ids.has(id)) throw new Error('Танихгүй бодлогын ID: '+id);
    result[id] = cleanEntry(entry);
  }
  return result;
}

// Current progress excludes hint history. Legacy parsers above remain available
// only for compatibility; the application reads/writes this projection instead.
export const CURRENT_EMPTY = {status:'new',notes:''};
export function cleanProgress(value) {
  if(!value||!['new','trying','solved'].includes(value.status)||typeof value.notes!=='string'||value.notes.length>5000)throw new Error('Progress-ийн бүтэц буруу байна.');
  return {status:value.status,notes:value.notes};
}
export function parseCurrentBackup(value,ids) {
  if(![1,2].includes(value?.version)||!value.progress||typeof value.progress!=='object'||Array.isArray(value.progress))throw new Error('Think CP-ийн progress файл сонгоно уу.');
  const out={};for(const[id,e]of Object.entries(value.progress)){if(!ids.has(id)||!/^[a-zA-Z0-9][a-zA-Z0-9_-]{0,99}$/.test(id)||['constructor','prototype'].includes(id))throw new Error('Танихгүй бодлогын ID: '+id);out[id]=cleanProgress(e);}return out;
}
export function progressRows(userId,progress,activity={}) {
  return Object.entries(progress).map(([problem_id,e])=>({user_id:userId,problem_id,...cleanProgress(e),record_activity:Boolean(activity[problem_id])}));
}
