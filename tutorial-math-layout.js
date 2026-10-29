// MathJax SVG widths can be fractional; do not turn a subpixel overhang into a scrollbar.
const observed=new Set();
function fit(box){
 if(!box.isConnected)return;
 const svg=box.querySelector('svg');if(!svg)return;
 let parent=box.parentElement;
 while(parent&&getComputedStyle(parent).display==='inline')parent=parent.parentElement;
 if(!parent)return;
 const style=getComputedStyle(parent),available=parent.getBoundingClientRect().width-parseFloat(style.paddingLeft)-parseFloat(style.paddingRight)-parseFloat(style.borderLeftWidth)-parseFloat(style.borderRightWidth);
 box.classList.toggle('inline-math-scroll',svg.getBoundingClientRect().width>available+0.01);
}
const observer=typeof ResizeObserver==='function'?new ResizeObserver(entries=>entries.forEach(e=>fit(e.target))):null;
export function refreshInlineMath(elements){
 for(const box of observed)if(!box.isConnected){observer?.unobserve(box);observed.delete(box);}
 for(const root of elements){for(const box of root.querySelectorAll('mjx-container:not([display="true"])')){fit(box);if(!observed.has(box)){observed.add(box);observer?.observe(box);}}}
}
