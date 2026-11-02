# MathJax saved-menu dependency repair

PR268 remains insufficient for returning readers. The actual provided Android screenshots were viewed from the verified private Library materializations. Introduction shows raw inline/display TeX in its sum/set sections. Neither screenshot identifies the user's saved menu state, so this report does not assert access to that device's settings.

Fresh production reads on 2026-11-02 confirmed main b6ed6d9 and exact deployed loader/core/safe bytes. The three requested optional paths output/chtml.js, input/mml.js and a11y/sre.js return404. The vendored installation contained only tex-svg.js and ui/safe.js.

A local actual-runtime reproduction with the current public Introduction revision4, actual Supabase SDK, Pixel7 emulation and persisted MathJax-Menu-Settings proves another concrete failure: CHTML, Explorer or Collapsible settings produce0 math containers. MathJax startup.document exists, but the menu's loading counter remains1 after a missing component fails. The post-startup checkLoading retry promise never completes. The previous startup-only deadline and tests with fresh storage missed this. See baseline.json (0 containers versus209 with empty settings).

The repair includes the official MathJax3.2.2 component dependency closure for CHTML/fonts, MathML, accessibility and its locale maps. All47 files are byte-identical to the pinned npm distribution,5,368,256bytes in total; vendor.json records hashes/source/integrity and the retained Apache2.0 license. The existing core and safe files remain unchanged. Accessibility components are prepared during the bounded startup; CHTML/fonts are loaded only when selected. This adds about1.2MB of first-load accessibility dependencies to the2.1MB core. The maps for other languages remain demand-loaded. No math CDN, external font or speech-map request is needed.

The bounded loader includes the saved CHTML renderer and menu accessibility dependencies in startup, where errors and stalled loads reach the existing retry path. A second real-engine test found that activating Explorer after startup can throw MathJax retry from the menu’s synchronous rerender and leave empty formula blocks. Preloading the accessibility tools also removes that late initialization path. The initial output renderer matches the saved supported choice so changing renderer during document construction cannot start a competing rerender. Preferences are read, never rewritten/deleted. Screen-reader assistive MathML, Explorer, locale choice, zoom/scale and safe filtering remain enabled as before. No stored content, SQL, schema, permissions or learner records change. Introduction revision4/history409 is not replayed.

Runtime reverse imports and the entry use100, the loader uses2. Native plain Input/Output remains literal. Tests use real SVG/CHTML and actual accessibility components; network failures/delays are injected, never successful typesetter stubs. The browser matrix includes persisted choices, combined French/scale preferences, temporary component503/retry, delayed component/retry, in-page menu changes, reload, MN/EN and lesson navigation, light/dark and Android viewport/touch emulation. It checks209 actual math containers without duplicates, unchanged saved preferences, assistive MathML and no external math requests.

The live-browser certificate restriction is not bypassed. Local actual-runtime checks plus public deployed-byte/readback verification cannot establish success on the user's physical Android device; that remains for user confirmation.

Official references read for this diagnosis:
- https://docs.mathjax.org/en/v3.2/options/menu.html (persistent settings and post-startup checkLoading)
- https://docs.mathjax.org/en/v3.2/web/hosting.html (serve the component distribution, not only the combined entry)
- https://docs.mathjax.org/en/v3.2/options/accessibility.html (extension dependencies and stored preferences)

Final verification:473/473 aggregate Node tests pass. Eight persisted/menu scenarios and six startup failure/delay scenarios each render209 Introduction math containers. Native100-day/quiz/editor and76-card regression suites pass. Fresh anonymous public tutorial and catalog responses match the prior release exactly; Introduction is still revision4. No production writes were executed.
