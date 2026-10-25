// Per-user private learning records; problem status/notes stay in the original app.
export function createLearningStore(ctx, changed) {
  let uid = null, generation = 0, records = {}, localDates = {}, dirty = new Set(), syncing = false, again = false;
  const storageKey = () => 'erdene:learning:v1:' + (uid || 'guest');
  const notify = text => { ctx.message?.(text); changed?.(); };
  function persist() {
    try { localStorage.setItem(storageKey(), JSON.stringify({records, dirty:[...dirty], dates:localDates})); return true; }
    catch { ctx.message?.('Төхөөрөмжид хадгалж чадсангүй. Хуудсаа хаахаас өмнө progress-оо татаж аваарай.'); return false; }
  }
  function read() {
    records = {}; localDates = {}; dirty = new Set();
    try { const value = JSON.parse(localStorage.getItem(storageKey()) || '{}'); if (value.records && typeof value.records === 'object' && !Array.isArray(value.records)) records = value.records; if (value.dates && typeof value.dates === 'object') localDates = value.dates; dirty = new Set((value.dirty || []).filter(k => records[k])); } catch {}
  }
  async function flush() {
    if (!uid || !ctx.client() || !dirty.size) return;
    if (syncing) { again = true; return; }
    syncing = true; const turn = generation, user = uid, batch = [...dirty].map(k => [k, records[k]]);
    try {
      const rows = batch.map(([key,value]) => { const cut = key.indexOf(':'); return {user_id:user, kind:key.slice(0,cut), key:key.slice(cut+1), value, updated_at:new Date().toISOString()}; });
      const {error} = await ctx.client().from('learning_records').upsert(rows,{onConflict:'user_id,kind,key'}); if (error) throw error;
      if (turn !== generation) return;
      for (const [key,value] of batch) if (records[key] === value) dirty.delete(key);
      persist(); notify('Сургалтын ахиц хадгалагдлаа.');
    } catch { if (turn === generation) notify('Сургалтын ахиц энэ төхөөрөмжид байна. Онлайн хадгалалтыг дахин оролдоорой.'); }
    finally { syncing = false; if (again) { again = false; void flush(); } }
  }
  async function accountChanged() {
    const next = ctx.user()?.id || null; if (next === uid && generation) return;
    uid = next; const turn = ++generation; read(); changed?.(); if (!uid || !ctx.client()) return;
    try {
      const {data,error} = await ctx.client().from('learning_records').select('kind,key,value').eq('user_id',uid); if (error) throw error;
      if (turn !== generation) return;
      const remote = {}; for (const r of data || []) remote[r.kind + ':' + r.key] = r.value;
      for (const key of dirty) remote[key] = records[key]; records = remote; persist(); changed?.(); void flush();
    } catch { if (turn === generation) notify('Сургалтын ахицыг төхөөрөмжийн хуулбараас харуулж байна.'); }
  }
  window.addEventListener('online', () => void flush());
  return {accountChanged, flush, get:(kind,key) => records[kind + ':' + key] || {}, all:kind => Object.fromEntries(Object.entries(records).filter(([k]) => k.startsWith(kind + ':')).map(([k,v]) => [k.slice(kind.length+1),v])), dates:() => localDates,
    set(kind,key,value) { if (!['tutorial','plan','bookmark'].includes(kind) || !/^[a-zA-Z0-9_-]{1,100}$/.test(key) || JSON.stringify(value).length > 15000) throw new Error('Сургалтын тэмдэглэл буруу байна.'); const k = kind + ':' + key; records[k] = structuredClone(value); dirty.add(k); const saved = persist(); notify(saved ? (uid ? 'Сургалтын ахицыг хадгалж байна…' : 'Сургалтын ахиц энэ төхөөрөмжид хадгалагдлаа.') : 'Хадгалалт амжилтгүй.'); void flush(); },
    recordTransition(id,before,after) { if (before === after) return; const dates = localDates[id] || {}; if (['trying','solved'].includes(after) && !dates.first_attempted_at) dates.first_attempted_at = new Date().toISOString(); if (after === 'solved' && !dates.first_solved_at) dates.first_solved_at = new Date().toISOString(); localDates[id] = dates; persist(); }
  };
}
