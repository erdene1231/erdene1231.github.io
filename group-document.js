import {validDate, weekday} from './group-export.js?v=52';

function text(value) {
    return String(value ?? '').replace(/\r\n?/g, '\n').replace(/\t/g, '    ')
        .replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\ufffe\uffff]/g, '');
}
function name(row) {
    return [row.last_name, row.first_name].filter(Boolean).join(' ') || row.full_name || 'Нэр бөглөөгүй';
}
export function reportFields(row) {
    return [
        ['Бодсон бодлогууд', row.solved_problems || '-'],
        ['Нийт бодлогын тоо', row.problem_count ?? 'Бөглөөгүй'],
        ['Бодлогын хүндрэл', row.difficulty || '-'],
        ['Судалсан сэдвүүд', row.topics || '-'],
        ['Нэмэлт тэмдэглэл', row.notes || '-'],
        ['Багшийн тэмдэглэл', row.teacher_note || '-']
    ];
}
function documentDays(data) {
    const dates = [...new Set(data.dates)].sort();
    if (!dates.length || dates.length > 62 || dates.some(date => !validDate(date))) throw new Error('Export хийх 1–62 зөв өдөр сонгоно уу.');
    return dates.map(date => ({date, rows: data.rows.filter(row => row.report_date === date)}));
}
function summary(rows) {
    const counts = rows.filter(row => Number.isInteger(row.problem_count));
    return `${rows.length} гишүүн. Нийт ${counts.reduce((sum, row) => sum + row.problem_count, 0)} бодлого (${counts.length} гишүүн тоо бөглөсөн). Хоосон тоо нь 0 гэсэн утгагүй.`;
}
const TEX_ESCAPE = {'\\': '\\textbackslash{}', '{': '\\{', '}': '\\}', '$': '\\$', '&': '\\&', '%': '\\%', '#': '\\#', '_': '\\_', '^': '\\textasciicircum{}', '~': '\\textasciitilde{}'};
export function escapeLatex(value) {
    return text(value).split('\n').map(line => line.split(/(\s+)/u).map(token => {
        const chars = Array.from(token);
        return chars.map((char, i) => (TEX_ESCAPE[char] || char) + (chars.length > 32 && (i + 1) % 16 === 0 ? '\\allowbreak{}' : '')).join('');
    }).join('')).join('\\par\n\\noindent ');
}
export function createReportLatex(data) {
    const days = documentDays(data);
    const parts = [String.raw`% Compile with XeLaTeX (UTF-8). User text is escaped; shell escape is unnecessary.
\documentclass[11pt,a4paper]{article}
\usepackage[a4paper,margin=16mm]{geometry}
\usepackage{fontspec}
\setmainfont{DejaVu Sans}
\usepackage{xcolor}
\usepackage{needspace}
\definecolor{clubgreen}{HTML}{194D38}
\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt}
\emergencystretch=3em
\newcommand{\ReportField}[2]{\par\noindent\textbf{#1}\par\nopagebreak[2]\noindent #2\par\vspace{3pt}}
\begin{document}
`];
    days.forEach(({date, rows}, index) => {
        if (index) parts.push('\\clearpage\n');
        parts.push(`{\\Large\\bfseries\\color{clubgreen} ${escapeLatex(data.group.name)}}\\par\n`);
        parts.push(`\\section*{${date} - ${weekday(date)}}\n{\\small ${escapeLatex(summary(rows))}}\\par\\medskip\n`);
        if (!rows.length) parts.push('Энэ өдрийн тайланд гишүүн байхгүй.\\par\n');
        rows.forEach((row, i) => {
            parts.push(`\\Needspace{7\\baselineskip}\n\\subsection*{${i + 1}. ${escapeLatex(name(row))}}\n`);
            for (const [label, value] of reportFields(row)) parts.push(`\\ReportField{${escapeLatex(label)}}{${escapeLatex(value)}}\n`);
            parts.push('\\medskip\\hrule\\medskip\n');
        });
    });
    parts.push('\\end{document}\n');
    return parts.join('');
}

let assetsPromise;
const scripts = new Map();
function loadScript(path, globalName) {
    if (globalThis[globalName]) return Promise.resolve(globalThis[globalName]);
    if (!scripts.has(path)) scripts.set(path, new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = new URL(path, import.meta.url).href;
        script.onload = () => globalThis[globalName] ? resolve(globalThis[globalName]) : reject(new Error('PDF бэлтгэх сан ачаалагдсангүй.'));
        script.onerror = () => {scripts.delete(path); script.remove(); reject(new Error('PDF-ийн файлууд ачаалагдсангүй. Холболтоо шалгаад дахин оролдоорой.'));};
        document.head.append(script);
    }));
    return scripts.get(path);
}
async function fontBytes(path) {
    const response = await fetch(new URL(path, import.meta.url));
    if (!response.ok) throw new Error('PDF-ийн Монгол үсгийн font ачаалагдсангүй.');
    return new Uint8Array(await response.arrayBuffer());
}
async function loadAssets() {
    if (!assetsPromise) assetsPromise = Promise.all([
        loadScript('vendor/pdf/pdf-lib.min.js', 'PDFLib'),
        loadScript('vendor/pdf/fontkit.umd.min.js', 'fontkit'),
        fontBytes('vendor/fonts/DejaVuSans.ttf'), fontBytes('vendor/fonts/DejaVuSans-Bold.ttf')
    ]).then(([pdfLib, fontkit, regular, bold]) => ({pdfLib, fontkit, regular, bold})).catch(error => {assetsPromise = null; throw error;});
    return assetsPromise;
}
export function wrapPdfText(value, font, size, width, firstWidth = width) {
    const lines = [];
    const availableWidth = () => lines.length ? width : firstWidth;
    for (const paragraph of text(value).split('\n')) {
        let line = '';
        for (const word of paragraph.split(/\s+/u).filter(Boolean)) {
            const candidate = line ? line + ' ' + word : word;
            if (font.widthOfTextAtSize(candidate, size) <= availableWidth()) {line = candidate; continue;}
            if (line) {lines.push(line); line = '';}
            for (const char of word) {
                if (line && font.widthOfTextAtSize(line + char, size) > availableWidth()) {lines.push(line); line = '';}
                line += char;
            }
        }
        lines.push(line || ' ');
    }
    return lines;
}
export async function createReportPdf(data, providedAssets) {
    const days = documentDays(data);
    const {pdfLib, fontkit, regular, bold} = providedAssets || await loadAssets();
    const {PDFDocument, PageSizes, rgb} = pdfLib;
    const pdf = await PDFDocument.create();
    pdf.registerFontkit(fontkit);
    const regularFont = await pdf.embedFont(regular, {subset: true});
    const boldFont = await pdf.embedFont(bold, {subset: true});
    const charsets = new Map([[regularFont, new Set(regularFont.getCharacterSet())], [boldFont, new Set(boldFont.getCharacterSet())]]);
    const safe = (value, font) => Array.from(text(value)).map(char => char === '\n' || charsets.get(font).has(char.codePointAt(0)) ? char : `[U+${char.codePointAt(0).toString(16).toUpperCase()}]`).join('');
    const ink = rgb(.10, .16, .13), green = rgb(.10, .30, .22), muted = rgb(.36, .42, .38), lineColor = rgb(.85, .88, .85);
    const pageSize = [PageSizes.A4[1], PageSizes.A4[0]];
    const margin = 26, bottom = 30, gap = 10, padding = 8;
    const width = pageSize[0] - 2 * margin;
    const cardWidth = (width - 2 * gap) / 3, textWidth = cardWidth - 2 * padding;
    const bodySize = 9, labelSize = 8.5, leading = 11.5, nameLeading = 13;
    let page, y, day;
    function drawLines(lines, x, start, font, size, color, step) {
        lines.forEach((line, i) => page.drawText(line, {x, y: start - i * step, font, size, color}));
    }
    function startPage() {
        if (pdf.getPageCount() >= 500) throw new Error('PDF хэт олон хуудастай байна. Цөөн өдөр сонгоод дахин export хийнэ үү.');
        page = pdf.addPage(pageSize); y = pageSize[1] - margin - 14;
        const title = wrapPdfText(safe(data.group.name, boldFont), boldFont, 14, width);
        drawLines(title, margin, y, boldFont, 14, green, 17); y -= title.length * 17 + 2;
        page.drawText(day.date + ' - ' + weekday(day.date), {x: margin, y, font: boldFont, size: 10, color: ink}); y -= 15;
        const info = wrapPdfText(safe(summary(day.rows), regularFont), regularFont, 8, width);
        drawLines(info, margin, y, regularFont, 8, muted, 10); y -= info.length * 10 + 12;
        page.drawLine({start: {x: margin, y: y + 5}, end: {x: margin + width, y: y + 5}, color: lineColor, thickness: .7});
    }
    function cardLines(row) {
        const optional = [
            ['Бодлогын хүндрэл', row.difficulty],
            ['Бодсон бодлогууд', row.solved_problems],
            ['Судалсан сэдвүүд', row.topics],
            ['Нэмэлт тэмдэглэл', row.notes],
            ['Багшийн тэмдэглэл', row.teacher_note]
        ].filter(([, value]) => text(value).trim());
        if (!optional.length && row.problem_count == null) return [{value: 'Тэмдэглэл бөглөөгүй.', before: 0}];
        const fields = [['Нийт бодлого', row.problem_count ?? 'Бөглөөгүй'], ...optional];
        return fields.flatMap(([label, value], fieldIndex) => {
            const prefix = label + ': ';
            const prefixWidth = boldFont.widthOfTextAtSize(prefix, labelSize);
            return wrapPdfText(safe(text(value).trim(), regularFont), regularFont, bodySize, textWidth, textWidth - prefixWidth)
                .map((value, index) => ({value, label, prefix: index ? '' : prefix, prefixWidth: index ? 0 : prefixWidth, before: !index && fieldIndex ? 3 : 0}));
        });
    }
    function splitCard(row, index, maxHeight) {
        const lines = cardLines(row), cards = [];
        let offset = 0;
        while (offset < lines.length) {
            const heading = `${index + 1}. ${name(row)}${offset ? ' (үргэлжлэл)' : ''}`;
            const names = wrapPdfText(safe(heading, boldFont), boldFont, 10, textWidth);
            const headerHeight = padding + names.length * nameLeading + 5;
            const body = [];
            let height = headerHeight + padding;
            // A field that spans cards retains its label; no part of its value is cut.
            if (offset && !lines[offset].prefix && lines[offset].label) {
                body.push({continuation: lines[offset].label + ' (үргэлжлэл)', before: 0});
                height += leading;
            }
            const start = offset;
            while (offset < lines.length) {
                const next = {...lines[offset], before: offset === start ? 0 : lines[offset].before};
                if (height + next.before + leading > maxHeight) break;
                body.push(next); height += next.before + leading; offset++;
            }
            if (offset === start) throw new Error('PDF-ийн гарчиг эсвэл сурагчийн нэр хэт урт байна. Нэрийг богиносгоод дахин оролдоно уу.');
            cards.push({names, headerHeight, body, height});
        }
        return cards;
    }
    function drawCard(card, x, top, height) {
        page.drawRectangle({x, y: top - height, width: cardWidth, height, borderColor: lineColor, borderWidth: .6});
        page.drawRectangle({x: x + .4, y: top - card.headerHeight, width: cardWidth - .8, height: card.headerHeight - .4, color: rgb(.95, .97, .95)});
        drawLines(card.names, x + padding, top - padding - 10, boldFont, 10, green, nameLeading);
        let cursor = top - card.headerHeight;
        for (const line of card.body) {
            cursor -= line.before;
            if (line.label === 'Багшийн тэмдэглэл') page.drawRectangle({x: x + 4, y: cursor - leading, width: cardWidth - 8, height: leading, color: rgb(.96, .98, .96)});
            if (line.continuation) page.drawText(line.continuation, {x: x + padding, y: cursor - bodySize, font: boldFont, size: labelSize, color: green});
            else {
                if (line.prefix) page.drawText(line.prefix, {x: x + padding, y: cursor - bodySize, font: boldFont, size: labelSize, color: green});
                page.drawText(line.value, {x: x + padding + (line.prefixWidth || 0), y: cursor - bodySize, font: regularFont, size: bodySize, color: ink});
            }
            cursor -= leading;
        }
    }
    for (day of days) {
        startPage();
        if (!day.rows.length) page.drawText('Энэ өдрийн тайланд гишүүн байхгүй.', {x: margin, y, font: regularFont, size: 10});
        const maxHeight = y - bottom;
        const cards = day.rows.flatMap((row, index) => splitCard(row, index, maxHeight));
        let columns = [y, y, y];
        for (const card of cards) {
            // Short cards can fill the space below another card without waiting
            // for the longest column. Student numbers preserve the reading order.
            let column = -1;
            for (let i = 0; i < 3; i++) {
                if (columns[i] - card.height >= bottom - .01 && (column < 0 || columns[i] > columns[column])) column = i;
            }
            if (column < 0) {startPage(); columns = [y, y, y]; column = 0;}
            drawCard(card, margin + column * (cardWidth + gap), columns[column], card.height);
            columns[column] -= card.height + gap;
        }
    }
    const pages = pdf.getPages();
    pages.forEach((page, index) => page.drawText(`${index + 1} / ${pages.length}`, {x: pageSize[0] / 2 - 18, y: 14, font: regularFont, size: 8, color: muted}));
    pdf.setTitle(text(data.group.name) + ' - Өдрийн тайлан');
    pdf.setCreator('Erdene Club');
    return pdf.save();
}
