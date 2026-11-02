// A single bootstrap, with readiness covering dependencies as well as the core file.
// A timeout does not remove a still-loading script or start a competing bootstrap.
export function mathJaxComponents(storage) {
    let settings = {};
    try { settings = JSON.parse(storage?.getItem('MathJax-Menu-Settings') || '{}') || {}; } catch { /* Storage may be unavailable. */ }
    // The contextual menu may enable these after startup. MathJax 3's synchronous
    // menu rerender cannot recover an asynchronous enrichment retry, so prepare
    // the available accessibility tools before any document can be rendered.
    const components = ['ui/safe', 'a11y/complexity', 'a11y/explorer'];
    if (settings.renderer === 'CHTML') components.push('output/chtml');
    return components;
}

export function createMathJaxLoader({window: win, document: doc, timeoutMs = 30000, setTimer = setTimeout, clearTimer = clearTimeout, onLateReady = () => {}}) {
    let state = 'idle', boot = null, attempt = null, script = null, timedOut = false;
    const failure = () => new Error('MathJax ачаалж чадсангүй. Дахин оролдоно уу. / Could not load MathJax. Try again.');
    function start() {
        state = 'loading'; timedOut = false;
        boot = new Promise((resolve, reject) => {
            let settled = false;
            const fail = () => { if (settled) return; settled = true; state = 'failed'; reject(failure()); };
            const loaded = () => {
                const mj = win.MathJax;
                if (!mj?.startup?.promise) return fail();
                Promise.resolve(mj.startup.promise).then(() => {
                    if (settled) return;
                    if (typeof mj.typesetPromise !== 'function' || !mj.startup.document) return fail();
                    settled = true; state = 'ready'; resolve(mj);
                    if (timedOut) onLateReady();
                }, fail);
            };
            // Adopt an existing runtime only after its startup promise resolves.
            if (win.MathJax?.startup?.promise) { loaded(); return; }
            // Menu preferences survive page reloads. Load their components during
            // startup, so a failed dependency reaches our bounded retry path rather
            // than MathJax 3's post-startup menu-loading promise (which can hang).
            let storage;
            try { storage = win.localStorage; } catch { /* Restricted browser storage. */ }
            const components = mathJaxComponents(storage);
            win.MathJax = {
                loader: {paths: {mathjax: new URL('./vendor/mathjax', doc.baseURI).href, sre: new URL('./vendor/mathjax/sre/mathmaps', doc.baseURI).href}, load: components, failed: fail},
                options: {safeOptions: {allow: {URLs: 'none', classes: 'none', cssIDs: 'none', styles: 'none'}}},
                tex: {packages: ['base', 'ams', 'newcommand', 'noundefined', 'configmacros'], inlineMath: [['\\(', '\\)'], ['$', '$']], displayMath: [['\\[', '\\]'], ['$$', '$$']], processEscapes: true, maxBuffer: 20000},
                svg: {fontCache: 'local'}, startup: {typeset: false, output: components.includes('output/chtml') ? 'chtml' : 'svg'}
            };
            script = doc.createElement('script');
            script.src = new URL('./vendor/mathjax/tex-svg.js', doc.baseURI).href;
            script.async = true; script.onerror = fail; script.onload = loaded;
            doc.head.append(script);
        });
        // Keep a late failure handled even after a timed-out caller has returned.
        void boot.catch(() => {});
    }
    function ready() {
        if (state === 'ready') return boot;
        if (attempt) return attempt;
        if (!boot) start();
        attempt = new Promise((resolve, reject) => {
            const timer = setTimer(() => { timedOut = true; if (state === 'loading') state = 'waiting'; reject(failure()); }, timeoutMs);
            boot.then(value => { clearTimer(timer); resolve(value); }, error => { clearTimer(timer); reject(error); });
        });
        return attempt;
    }
    function retry() {
        if (state === 'failed') {
            script?.remove();
            // Only a definitively failed bootstrap is replaced, never a pending one.
            win.MathJax = undefined;
            boot = null; state = 'idle';
        }
        if (state !== 'loading') attempt = null;
        return ready();
    }
    return {ready, retry, status: () => state};
}
