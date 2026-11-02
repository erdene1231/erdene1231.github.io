// A single bootstrap, with readiness covering dependencies as well as the core file.
// A timeout does not remove a still-loading script or start a competing bootstrap.
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
            win.MathJax = {
                loader: {paths: {mathjax: new URL('./vendor/mathjax', doc.baseURI).href}, load: ['ui/safe'], failed: fail},
                options: {safeOptions: {allow: {URLs: 'none', classes: 'none', cssIDs: 'none', styles: 'none'}}},
                tex: {packages: ['base', 'ams', 'newcommand', 'noundefined', 'configmacros'], inlineMath: [['\\(', '\\)'], ['$', '$']], displayMath: [['\\[', '\\]'], ['$$', '$$']], processEscapes: true, maxBuffer: 20000},
                svg: {fontCache: 'local'}, startup: {typeset: false}
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
