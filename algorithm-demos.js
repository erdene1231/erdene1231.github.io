// Small deterministic traces, with no background animation or external dependency.
export function algorithmDemo(id,lang='mn',typeset) {
  if (!['binary-search','greedy','dynamic-programming'].includes(id)) return null;
  const en=lang==='en', el=(tag,text)=>{const x=document.createElement(tag);if(text!==undefined)x.textContent=text;return x;};
  const box=el('aside');box.className='algorithm-demo';box.append(el('h4',en?'Trace one step at a time':'Алхам бүрийг өөрөө дагах'));
  const output=el('div'),controls=el('div');controls.className='learning-nav';let step=0,states=[];
  if(id==='binary-search') {
    const a=[2,4,4,7,9];let l=0,r=a.length;states.push({l,r,text:en?'Find the first value $\\ge 4$.':'$4$-өөс бага биш эхний утгыг хайна.'});
    while(l<r){const mid=l+Math.floor((r-l)/2),text=`$l=${l},\\ r=${r},\\ mid=${mid},\\ a[mid]=${a[mid]}$ → `+(a[mid]>=4?'$r=mid$':'$l=mid+1$');if(a[mid]>=4)r=mid;else l=mid+1;states.push({l,r,text});}
    states.push({l,r,text:(en?'Answer index: ':'Хариу index: ')+'$'+l+'$'});
    states=states.map(s=>({...s,cells:a.map((value,i)=>({value,mark:i>=s.l&&i<s.r?'active':i===s.l&&s.l===s.r?'answer':'muted'}))}));
  } else if(id==='greedy') {
    const movies=[[2,3],[1,4],[3,5],[5,7]];let finish=-Infinity,count=0;
    states.push({text:en?'Sorted by finish time.':'Дуусах цагаар эрэмбэлсэн.',cells:movies.map(a=>({value:'['+a.join(',')+')',mark:'active'}))});
    movies.forEach(([l,r],i)=>{const take=l>=finish;if(take){finish=r;count++;}states.push({text:`$[${l},${r})$ → `+(take?(en?'take':'авна'):(en?'skip':'алгасана'))+' · $count='+count+'$',cells:movies.map((a,j)=>({value:'['+a.join(',')+')',mark:j===i?'answer':j<i?'muted':'active'}))});});
  } else {
    const dp=[1];states.push({text:'$\\mathrm{dp}[0]=1$',cells:[{value:1,mark:'answer'}]});for(let i=1;i<=6;i++){dp[i]=dp[i-1]+(i>=2?dp[i-2]:0);states.push({text:`$\\mathrm{dp}[${i}]=\\mathrm{dp}[${i-1}]`+(i>=2?`+\\mathrm{dp}[${i-2}]=${dp[i-1]}+${dp[i-2]}`:'')+'='+dp[i]+'$',cells:dp.map((value,j)=>({value,mark:j===i?'answer':'active'}))});}
  }
  const previous=el('button',en?'← Back':'← Өмнөх'),next=el('button',en?'Next →':'Дараах →'),reset=el('button',en?'Reset':'Дахин эхлэх');for(const b of [previous,next,reset])b.type='button';
  function paint(){const state=states[step];output.replaceChildren(el('p',state.text));const cells=el('div');cells.className='algorithm-cells';state.cells.forEach((cell,i)=>{const x=el('span','$'+cell.value+'$');x.className=cell.mark;x.title='index '+i;cells.append(x);});output.append(cells,el('small',(en?'Step ':'Алхам ')+(step+1)+'/'+states.length));previous.disabled=step===0;next.disabled=step===states.length-1;}
  function update(){if(typeset)void typeset([output],paint).catch(()=>{});else paint();}
  previous.onclick=()=>{step=Math.max(0,step-1);update();};next.onclick=()=>{step=Math.min(states.length-1,step+1);update();};reset.onclick=()=>{step=0;update();};controls.append(previous,reset,next);box.append(output,controls);paint();return box;
}
