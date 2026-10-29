import {gridDimensions,gridKey,gridLayout,regionCells,renderGridRows,prepareGridTable,validateGridPresentation,mergeGridCells,unmergeGridCells,colorGridCells} from './tutorial-grid.js?v=61';

const stateFor=new WeakMap();
const make=(tag,text)=>{const e=document.createElement(tag);if(text!==undefined)e.textContent=text;return e;};
export function gridControls(root,b,change,{locked=()=>false,validate=()=>{}}={}) {
    let state=stateFor.get(b);
    if(!state){state={selected:new Set(),anchor:null,multiple:false,color:'#dbeafe',open:true};stateFor.set(b,state);}
    const group=make('details'),summary=make('summary','Нүдний өнгө ба нэгтгэл');group.className='grid-controls';group.open=state.open;group.ontoggle=()=>state.open=group.open;group.append(summary);root.append(group);
    const message=make('p');message.className='grid-selection-status';message.setAttribute('role','status');
    let dimensions;
    try{dimensions=gridDimensions(b);validateGridPresentation(b);}catch(e){message.textContent=e.message;group.append(message);return;}
    const {rows,cols}=dimensions,layout=gridLayout(b),selection=()=>[...state.selected].map(k=>k.split(':').map(Number));
    // A stale selection is UI state only, never silently applied to resized content.
    for(const key of state.selected){const[r,c]=key.split(':').map(Number);if(r>=rows||c>=cols)state.selected.delete(key);}
    const hint=make('p','Нүд дээр дарж сонгоно. Shift-ээр хүрээ, Ctrl/⌘ эсвэл «Олон нүд» горимоор нэмнэ. Сумтай товчоор шилжинэ. Нэгтгэхэд текст устахгүй; ялгаатай текстүүд хамт харагдана. Нэгтгэсэн бүс зүүн дээд нүдний өнгөөр харагдана.');hint.className='muted';group.append(hint);
    if(b.type==='table')group.append(make('small','Өгөгдлийн нүднүүдийг өөрчилнө; гарчгийн мөр хэвээр үлдэнэ.'));
    const actions=make('div');actions.className='grid-actions';group.append(actions);
    const btn=(label,fn)=>{const e=make('button',label);e.type='button';e.onclick=()=>{if(!locked())fn();};return e;};
    const run=operation=>{try{const next=operation();change(()=>b.gridPresentation=next,b,true);}catch(e){message.textContent=e.message;}};
    const multiple=btn('Олон нүд',()=>{state.multiple=!state.multiple;multiple.setAttribute('aria-pressed',String(state.multiple));});multiple.setAttribute('aria-pressed',String(state.multiple));
    const clear=btn('Сонголт цэвэрлэх',()=>{state.selected.clear();state.anchor=null;update();});
    const merge=btn('Нүд нэгтгэх',()=>run(()=>mergeGridCells(b,selection()))),unmerge=btn('Нэгтгэл салгах',()=>run(()=>unmergeGridCells(b,selection())));
    actions.append(multiple,clear,merge,unmerge);
    const colors=make('div');colors.className='grid-colors';group.append(colors);
    const label=make('label','Нүдний өнгө'),picker=make('input');picker.type='color';picker.value=state.color;picker.setAttribute('aria-label','Нүдний өнгө');picker.oninput=()=>state.color=picker.value;label.append(picker);colors.append(label);
    const apply=btn('Өнгө өгөх',()=>run(()=>colorGridCells(b,selection(),state.color))),reset=btn('Өнгө арилгах',()=>run(()=>colorGridCells(b,selection(),undefined)));colors.append(apply,reset);
    const palette=make('div');palette.className='grid-palette';colors.append(palette);const swatches=[];
    for(const[name,color]of[['Хөх','#dbeafe'],['Ногоон','#dcfce7'],['Шар','#fef3c7'],['Ягаан','#fce7f3'],['Нил','#e0e7ff'],['Саарал','#e5e7eb']]){const e=btn(name,()=>{state.color=color;run(()=>colorGridCells(b,selection(),color));});e.setAttribute('aria-label',name+' өнгө өгөх');e.style.backgroundColor=color;e.style.color='#000000';palette.append(e);swatches.push(e);}
    const wrap=make('div'),table=make('table'),tbody=make('tbody');wrap.className='grid-editor-scroll';table.className='grid-editor-preview';table.style.width=(cols*48)+'px';table.style.tableLayout='fixed';prepareGridTable(table,b);table.append(tbody);wrap.append(table);group.append(wrap,message);
    const buttons=renderGridRows(tbody,b,{editor:true,onCell:select});
    function disabled(e,value){e.disabled=locked()||value;e.dataset.boundaryDisabled=String(value);}
    function update(){
        for(const e of group.querySelectorAll('button,input'))e.disabled=locked();
        for(const{button,region}of buttons){const active=regionCells(region).every(c=>state.selected.has(gridKey(...c)));button.classList.toggle('selected',active);button.setAttribute('aria-pressed',String(active));}
        const count=state.selected.size;message.textContent=count?count+' нүд сонгосон. Нэгтгэх сонголт тэгш өнцөгт байна.':'Өнгө өгөх эсвэл нэгтгэх нүднүүдээ сонгоно уу.';
        for(const e of[clear,apply,reset,...swatches])disabled(e,count===0);disabled(merge,count<2);disabled(unmerge,![...state.selected].some(k=>layout.regions.has(k)));
    }
    function select(m,e){
        if(locked())return;
        const cells=regionCells(m);
        if(e.shiftKey&&state.anchor){const a=state.anchor;const loR=Math.min(a.row,m.row),hiR=Math.max(a.row+a.rowSpan,m.row+m.rowSpan),loC=Math.min(a.col,m.col),hiC=Math.max(a.col+a.colSpan,m.col+m.colSpan);state.selected.clear();for(let r=loR;r<hiR;r++)for(let c=loC;c<hiC;c++){const covered=layout.regions.get(gridKey(r,c))||{row:r,col:c,rowSpan:1,colSpan:1};for(const cell of regionCells(covered))state.selected.add(gridKey(...cell));}}
        else if(state.multiple||e.ctrlKey||e.metaKey){const all=cells.every(c=>state.selected.has(gridKey(...c)));for(const c of cells){if(all)state.selected.delete(gridKey(...c));else state.selected.add(gridKey(...c));}state.anchor=m;}
        else{state.selected=new Set(cells.map(c=>gridKey(...c)));state.anchor=m;}
        update();
    }
    for(const{button,region:m}of buttons)button.onkeydown=e=>{
        if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)||locked())return;e.preventDefault();let r=m.row,c=m.col;
        if(e.key==='ArrowLeft')c--;if(e.key==='ArrowRight')c+=m.colSpan;if(e.key==='ArrowUp')r--;if(e.key==='ArrowDown')r+=m.rowSpan;
        if(r<0||r>=rows||c<0||c>=cols)return;const region=layout.regions.get(gridKey(r,c))||{row:r,col:c,rowSpan:1,colSpan:1};const next=buttons.find(x=>x.region.row===region.row&&x.region.col===region.col);next?.button.focus();if(e.shiftKey)select(region,e);
    };
    const files=make('div');files.className='grid-files';group.append(files);
    const importer=make('input');importer.type='file';importer.accept='.json,application/json';importer.setAttribute('aria-label','Нүдтэй хүснэгтийн JSON оруулах');
    importer.onchange=async()=>{try{const file=importer.files?.[0];if(!file)return;if(file.size>1048576)throw Error('Хүснэгтийн JSON 1MB-ээс ихгүй байна.');const value=JSON.parse(await file.text());if(locked()||!importer.isConnected)return;
        if(value.type!==b.type||(b.type==='diagram'&&!['array','dp'].includes(value.kind)))throw Error('Ижил төрлийн хүснэгт эсвэл array/DP JSON сонгоно уу.');validate(value);gridDimensions(value);validateGridPresentation(value);
        state.selected.clear();state.anchor=null;change(()=>{const key=b.key;for(const k of Object.keys(b))delete b[k];for(const k of Object.keys(value))Object.defineProperty(b,k,{value:value[k],writable:true,enumerable:true,configurable:true});if(key!==undefined)b.key=key;},importer,true);
    }catch(e){message.textContent=e instanceof SyntaxError?'JSON файлын бүтэц буруу.':e.message;}};
    const importLabel=make('label','Хүснэгтийн JSON оруулах');importLabel.append(importer);files.append(importLabel,btn('Хүснэгтийн JSON татах',()=>{try{validate(b);validateGridPresentation(b);const content=JSON.stringify(b,null,2);if(new Blob([content]).size>1048576)throw Error('Хүснэгтийн JSON 1MB-ээс ихгүй байна.');const url=URL.createObjectURL(new Blob([content],{type:'application/json'})),a=make('a');a.href=url;a.download='grid.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}catch(e){message.textContent=e.message;}}));
    update();
}
