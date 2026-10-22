import {validDate, weekday} from './group-export.js?v=18';

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
export function wrapPdfText(value, font, size, width) {
    const lines = [];
    for (const paragraph of text(value).split('\n')) {
        let line = '';
        for (const word of paragraph.split(/\s+/u).filter(Boolean)) {
            const candidate = line ? line + ' ' + word : word;
            if (font.widthOfTextAtSize(candidate, size) <= width) {line = candidate; continue;}
            if (line) {lines.push(line); line = '';}
            for (const char of word) {
                if (line && font.widthOfTextAtSize(line + char, size) > width) {lines.push(line); line = '';}
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
    const left = 44, bottom = 43, labelWidth = 140, leading = 14.5;
    const width = PageSizes.A4[0] - 2 * left;
    let page, y, day, activeName = '';
    function drawLines(lines, x, start, font, size, color = ink, step = leading) {
        lines.forEach((line, i) => page.drawText(line, {x, y: start - i * step, font, size, color}));
    }
    function drawName(continuation = false) {
        const lines = wrapPdfText(safe(activeName + (continuation ? ' (үргэлжлэл)' : ''), boldFont), boldFont, 12, width);
        drawLines(lines, left, y - 13, boldFont, 12, green, 17);
        y -= lines.length * 17 + 12;
    }
    function startPage(continuation = false) {
        if (pdf.getPageCount() >= 500) throw new Error('PDF хэт олон хуудастай байна. Цөөн өдөр сонгоод дахин export хийнэ үү.');
        page = pdf.addPage(PageSizes.A4); y = PageSizes.A4[1] - 46;
        const title = wrapPdfText(safe(data.group.name, boldFont), boldFont, 16, width);
        drawLines(title, left, y, boldFont, 16, green, 21); y -= title.length * 21 + 8;
        page.drawText(day.date + ' - ' + weekday(day.date), {x: left, y, font: boldFont, size: 11, color: ink}); y -= 20;
        const info = wrapPdfText(safe(summary(day.rows), regularFont), regularFont, 9, width);
        drawLines(info, left, y, regularFont, 9, muted, 12); y -= info.length * 12 + 16;
        page.drawLine({start: {x: left, y: y + 7}, end: {x: left + width, y: y + 7}, color: lineColor, thickness: .7});
        if (continuation) drawName(true);
    }
    function drawField(label, value) {
        const lines = wrapPdfText(safe(value, regularFont), regularFont, 10.5, width - labelWidth - 15);
        let offset = 0;
        while (offset < lines.length) {
            if (y - bottom < 55) startPage(true);
            const maxLines = Math.max(1, Math.floor((y - bottom - 12) / leading));
            const count = Math.min(maxLines, lines.length - offset);
            const labels = wrapPdfText(safe(label + (offset ? ' (үргэлжлэл)' : ''), boldFont), boldFont, 9.5, labelWidth - 10);
            const height = Math.max(labels.length, count) * leading + 12;
            if (height > y - bottom) {startPage(true); continue;}
            if (label === 'Багшийн тэмдэглэл') page.drawRectangle({x: left, y: y - height, width, height, color: rgb(.94, .97, .94)});
            drawLines(labels, left + 5, y - 13, boldFont, 9.5, green);
            drawLines(lines.slice(offset, offset + count), left + labelWidth, y - 13, regularFont, 10.5);
            y -= height;
            page.drawLine({start: {x: left, y}, end: {x: left + width, y}, color: lineColor, thickness: .4});
            offset += count;
            if (offset < lines.length) startPage(true);
        }
    }
    for (day of days) {
        startPage();
        if (!day.rows.length) page.drawText('Энэ өдрийн тайланд гишүүн байхгүй.', {x: left, y, font: regularFont, size: 11});
        for (const [i, row] of day.rows.entries()) {
            activeName = `${i + 1}. ${name(row)}`;
            const headingHeight = wrapPdfText(safe(activeName, boldFont), boldFont, 12, width).length * 17 + 70;
            if (y - bottom < headingHeight) startPage();
            drawName();
            for (const [label, value] of reportFields(row)) drawField(label, value);
            y -= 18;
        }
    }
    const pages = pdf.getPages();
    pages.forEach((page, index) => page.drawText(`${index + 1} / ${pages.length}`, {x: PageSizes.A4[0] / 2 - 18, y: 23, font: regularFont, size: 8, color: muted}));
    pdf.setTitle(text(data.group.name) + ' - Өдрийн тайлан');
    pdf.setCreator('Erdene Club');
    return pdf.save();
}
