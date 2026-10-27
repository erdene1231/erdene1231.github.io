// Hint text remains plain text. Only backtick code spans become DOM elements;
// MathJax handles its existing safe delimiters outside code elements.
export function appendHintText(parent,text) {
 for(const part of String(text).split(/(`[^`]*`)/g)) {
  if(part.startsWith('`')&&part.endsWith('`')&&part.length>=2){const code=document.createElement('code');code.textContent=part.slice(1,-1);parent.append(code);}
  else parent.append(document.createTextNode(part));
 }
}
