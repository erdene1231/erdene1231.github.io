// IDs are stable title slugs. Existing IDs are never rewritten on title edits.
export function tutorialSlug(title){
 const mn={'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'yo','ж':'j','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n','о':'o','ө':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ү':'u','ф':'f','х':'kh','ц':'ts','ч':'ch','ш':'sh','щ':'sh','ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya'};
 const slug=[...title.toLowerCase()].map(c=>mn[c]??c).join('').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'').slice(0,80).replace(/-+$/,'');
 return /[a-z]/.test(slug)?slug:'';
}
