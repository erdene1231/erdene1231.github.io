(function () {
    'use strict';
    const key = 'erdene-club:theme';
    const system = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
    let chosen = null;
    try {const value = localStorage.getItem(key); if (value === 'dark' || value === 'light') chosen = value;} catch {}
    function apply() {
        const dark = chosen ? chosen === 'dark' : Boolean(system?.matches);
        document.documentElement.dataset.theme = dark ? 'dark' : 'light';
        const button = document.getElementById('theme-toggle');
        if (button) {
            const label = dark ? 'Гэрэлтэй горимд шилжих' : 'Бараан горимд шилжих';
            button.textContent = dark ? '☀' : '☾'; button.title = label;
            button.setAttribute('aria-label', label); button.setAttribute('aria-pressed', String(dark));
        }
    }
    apply(); // Runs before stylesheets to avoid a flash of the wrong theme.
    function bind() {
        const button = document.getElementById('theme-toggle');
        if (button) button.addEventListener('click', function () {
            chosen = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
            try {localStorage.setItem(key, chosen);} catch {}
            apply();
        });
        apply();
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bind, {once: true}); else bind();
    system?.addEventListener?.('change', function () {if (!chosen) apply();});
    window.addEventListener('storage', function (event) {
        if (event.key !== key) return;
        chosen = ['dark', 'light'].includes(event.newValue) ? event.newValue : null; apply();
    });
})();
