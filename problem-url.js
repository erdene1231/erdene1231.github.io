// Only ordinary Codeforces task paths participate; Gym and other URLs stay intact.
export function canonicalProblemUrl(value) {
 if(typeof value!=='string')return value;
 try {
  const u=new URL(value);
  if(u.protocol!=='https:'||u.username||u.password||!['codeforces.com','www.codeforces.com'].includes(u.hostname)||u.port)return value;
  const match=u.pathname.match(/^\/(?:problemset\/problem\/(\d+)\/([A-Za-z][A-Za-z0-9]*)|contest\/(\d+)\/problem\/([A-Za-z][A-Za-z0-9]*))\/?$/);
  if(!match)return value;
  u.hostname='codeforces.com';u.pathname=`/contest/${match[1]||match[3]}/problem/${match[2]||match[4]}`;
  return u.href;
 }catch{return value;}
}
export function problemUrlIdentity(value) {
 const canonical=canonicalProblemUrl(value);
 try{const u=new URL(canonical);if(u.hostname==='codeforces.com'&&/^\/contest\/\d+\/problem\/[A-Za-z][A-Za-z0-9]*$/.test(u.pathname)){u.search='';u.hash='';return u.href;}}catch{}
 return canonical;
}
