// Optional presentation over the original cell strings. Merging never rewrites rows.
export const gridKey = (row, col) => row + ':' + col;
export const safeGridColor = value => typeof value === 'string' && /^#[0-9a-f]{6}$/i.test(value);
export const isCellGrid = b => b?.type === 'table' || (b?.type === 'diagram' && ['array', 'dp'].includes(b.kind));

export function gridDimensions(b) {
    if (!isCellGrid(b) || !Array.isArray(b.rows) || !b.rows.length) throw Error('Нүдтэй хүснэгт сонгоно уу.');
    const rows = b.rows.length, cols = b.rows[0]?.length;
    const maxRows = b.type === 'table' ? 100 : 20, maxCols = b.type === 'table' ? 8 : 30;
    if (!Number.isInteger(cols) || cols < 1 || cols > maxCols || rows > maxRows ||
        b.rows.some(row => !Array.isArray(row) || row.length !== cols || row.some(s => typeof s !== 'string'))) {
        throw Error('Мөр бүр ижил тооны нүдтэй, зөв хэмжээтэй байна.');
    }
    return {rows, cols};
}

export function validateGridPresentation(b) {
    if (!isCellGrid(b) || b.gridPresentation === undefined) return true;
    const {rows, cols} = gridDimensions(b), g = b.gridPresentation;
    const object = value => value && typeof value === 'object' && !Array.isArray(value);
    const keys = (value, allowed) => Object.keys(value).every(k => allowed.includes(k));
    if (!object(g) || !keys(g, ['colors', 'merges'])) throw Error('Нүдний өнгө/нэгтгэлийн бүтэц буруу.');
    const colors = g.colors ?? [], merges = g.merges ?? [];
    if ((g.colors !== undefined && !Array.isArray(g.colors)) || (g.merges !== undefined && !Array.isArray(g.merges)) ||
        colors.length > rows * cols || merges.length > Math.floor(rows * cols / 2)) throw Error('Нүдний тохиргооны тоо буруу.');
    const validCell = v => object(v) && Number.isInteger(v.row) && Number.isInteger(v.col) &&
        v.row >= 0 && v.row < rows && v.col >= 0 && v.col < cols;
    const painted = new Set(), occupied = new Set();
    for (const c of colors) {
        const key = gridKey(c?.row, c?.col);
        if (!validCell(c) || !keys(c, ['row', 'col', 'color']) || !safeGridColor(c.color) || painted.has(key)) {
            throw Error('Нүдний өнгө эсвэл байрлал буруу/давхардсан.');
        }
        painted.add(key);
    }
    for (const m of merges) {
        if (!validCell(m) || !keys(m, ['row', 'col', 'rowSpan', 'colSpan']) ||
            !Number.isInteger(m.rowSpan) || !Number.isInteger(m.colSpan) || m.rowSpan < 1 || m.colSpan < 1 ||
            m.rowSpan * m.colSpan < 2 || m.row + m.rowSpan > rows || m.col + m.colSpan > cols) {
            throw Error('Нэгтгэх бүс тэгш өнцөгт бөгөөд хүснэгтийн дотор байна.');
        }
        for (let r = m.row; r < m.row + m.rowSpan; r++) for (let c = m.col; c < m.col + m.colSpan; c++) {
            const key = gridKey(r, c);
            if (occupied.has(key)) throw Error('Нэгтгэсэн бүсүүд давхцаж болохгүй.');
            occupied.add(key);
        }
    }
    return true;
}

export function gridLayout(b) {
    validateGridPresentation(b);
    const colors = new Map((b.gridPresentation?.colors || []).map(c => [gridKey(c.row, c.col), c.color]));
    const regions = new Map();
    for (const m of b.gridPresentation?.merges || []) {
        for (let r = m.row; r < m.row + m.rowSpan; r++) for (let c = m.col; c < m.col + m.colSpan; c++) regions.set(gridKey(r, c), m);
    }
    return {colors, regions};
}

export function regionCells(m) {
    const cells = [];
    for (let row = m.row; row < m.row + m.rowSpan; row++) for (let col = m.col; col < m.col + m.colSpan; col++) cells.push([row, col]);
    return cells;
}

function selectedCells(b, selection) {
    const {rows, cols} = gridDimensions(b), cells = new Map();
    for (const pair of selection) {
        if (!Array.isArray(pair) || pair.length !== 2 || !pair.every(Number.isInteger) || pair[0] < 0 || pair[0] >= rows || pair[1] < 0 || pair[1] >= cols) throw Error('Сонгосон нүд хүснэгтийн гадна байна.');
        cells.set(gridKey(...pair), pair);
    }
    if (!cells.size) throw Error('Эхлээд нүд сонгоно уу.');
    return [...cells.values()];
}

export function mergedSelection(b, selection) {
    const {regions} = gridLayout(b), cells = new Map();
    for (const [r, c] of selectedCells(b, selection)) {
        for (const pair of regionCells(regions.get(gridKey(r, c)) || {row:r, col:c, rowSpan:1, colSpan:1})) cells.set(gridKey(...pair), pair);
    }
    return [...cells.values()];
}

export function mergeGridCells(b, selection) {
    validateGridPresentation(b);
    const cells = selectedCells(b, selection);
    if (cells.length < 2) throw Error('Нэгтгэхийн тулд дор хаяж хоёр нүд сонгоно уу.');
    const rs = cells.map(c => c[0]), cs = cells.map(c => c[1]);
    const row = Math.min(...rs), col = Math.min(...cs), rowSpan = Math.max(...rs) - row + 1, colSpan = Math.max(...cs) - col + 1;
    if (rowSpan * colSpan !== cells.length) throw Error('Нэгтгэх сонголт завсаргүй тэгш өнцөгт байна.');
    const {regions} = gridLayout(b);
    if (cells.some(c => regions.has(gridKey(...c)))) throw Error('Өмнөх нэгтгэлтэй давхцаж байна. Эхлээд салгана уу.');
    const next = structuredClone(b.gridPresentation || {});
    (next.merges ??= []).push({row, col, rowSpan, colSpan});
    validateGridPresentation({...b, gridPresentation:next});
    return next;
}

export function unmergeGridCells(b, selection) {
    validateGridPresentation(b);
    const cells = new Set(selectedCells(b, selection).map(c => gridKey(...c)));
    const next = structuredClone(b.gridPresentation || {});
    next.merges = (next.merges || []).filter(m => !regionCells(m).some(c => cells.has(gridKey(...c))));
    return next;
}

export function colorGridCells(b, selection, color) {
    if (color !== undefined && !safeGridColor(color)) throw Error('Өнгө #RRGGBB хэлбэртэй байна.');
    const cells = mergedSelection(b, selection), next = structuredClone(b.gridPresentation || {});
    const colors = new Map((next.colors || []).map(c => [gridKey(c.row, c.col), c]));
    for (const [row, col] of cells) {
        if (color === undefined) colors.delete(gridKey(row, col));
        else colors.set(gridKey(row, col), {row, col, color});
    }
    next.colors = [...colors.values()].sort((a,b) => a.row-b.row || a.col-b.col);
    validateGridPresentation({...b, gridPresentation:next});
    return next;
}

export function gridTextColor(color) {
    if (!safeGridColor(color)) return '';
    const rgb = [1,3,5].map(i => parseInt(color.slice(i,i+2),16)/255).map(v => v <= 0.04045 ? v/12.92 : ((v+0.055)/1.055)**2.4);
    const lum = rgb[0]*0.2126 + rgb[1]*0.7152 + rgb[2]*0.0722;
    return (lum+0.05)/0.05 >= 1.05/(lum+0.05) ? '#000000' : '#ffffff';
}

export function gridCellText(b, m) {
    const values = regionCells(m).map(([r,c]) => b.rows[r][c]);
    return new Set(values).size === 1 ? values[0] : values.join(' · ');
}

// Both native reader and editor preview use the same spans, colors and cell text.
export function renderGridRows(parent, b, {editor=false, onCell}={}) {
    const {colors, regions} = gridLayout(b), high = new Set(b.highlights || []), buttons = [];
    b.rows.forEach((row,r) => {
        const tr = document.createElement('tr');
        row.forEach((_,c) => {
            const m = regions.get(gridKey(r,c)) || {row:r,col:c,rowSpan:1,colSpan:1};
            if (m.row !== r || m.col !== c) return;
            const td = document.createElement('td'), content = document.createElement(editor ? 'button' : 'span');
            td.rowSpan=m.rowSpan; td.colSpan=m.colSpan; td.dataset.gridRow=r; td.dataset.gridCol=c;
            const cells=regionCells(m), color=colors.get(gridKey(r,c));
            if (color) {td.style.backgroundColor=color;td.style.color=gridTextColor(color);}
            if (cells.some(p=>high.has(gridKey(...p)))) td.classList.add('highlight');
            for (const [side,neighbors] of [['left',Array.from({length:m.rowSpan},(_,i)=>[r+i,c-1])],['right',Array.from({length:m.rowSpan},(_,i)=>[r+i,c+m.colSpan])],['top',Array.from({length:m.colSpan},(_,i)=>[r-1,c+i])],['bottom',Array.from({length:m.colSpan},(_,i)=>[r+m.rowSpan,c+i])]]) {
                if(neighbors.some(p=>high.has(gridKey(...p))))td.classList.add('highlight-border-'+side);
            }
            content.className=editor?'grid-select-cell':'grid-cell-content'; content.textContent=gridCellText(b,m);
            if(b.gridPresentation)content.style.minHeight=(48*m.rowSpan)+'px';
            if(editor){content.type='button';content.setAttribute('aria-pressed','false');content.setAttribute('aria-label','Мөр '+(r+1)+', багана '+(c+1)+': '+content.textContent);content.onclick=e=>onCell?.(m,e);buttons.push({button:content,region:m});}
            if(cells.length>1)td.title=cells.map(([y,x])=>(y+1)+':'+(x+1)+' '+b.rows[y][x]).join('; ');
            td.append(content);tr.append(td);
        });
        parent.append(tr);
    });
    return buttons;
}

export function prepareGridTable(table,b) {
    if(!b.gridPresentation)return;
    table.classList.add('grid-presented');
    if(b.type==='diagram'){const{cols}=gridDimensions(b);table.style.width=(cols*48)+'px';table.style.tableLayout='fixed';}
}

export function validateGridDocument(b) {
    const {cols}=gridDimensions(b);
    const max=b.type==='table'?8000:500;
    if(b.rows.some(row=>row.some(s=>!s.trim()||s.length>max)))throw Error('Нүдний текст хоосон эсвэл хэт урт байна.');
    if(b.type==='table'&&(!Array.isArray(b.headers)||b.headers.length!==cols||b.headers.some(s=>typeof s!=='string'||!s.trim()||s.length>200)))throw Error('Хүснэгтийн гарчгууд буруу байна.');
    validateGridPresentation(b);
    return true;
}
