# Package 4 UI refresh checkpoint

The latest user instructions allow a fresh overall design while preserving routes, features, data and accessibility. The visual direction uses neutral light surfaces, a dark-green accent, clearer spacing and restrained borders. Dark tokens remain coherent. Wide screens receive a persistent side navigation; tablets and phones use a wrapping primary menu. Shared forms, focus indicators, cards and dialogs receive consistent treatment. No new animation, gradient or external font dependency.

Problems has three functional densities. Minimalist uses larger titles, smaller ratings/tags and hides only the hint-use indicator. Hint data, detail hints, solved/trying state and normal-mode indicators persist. Compact now has visibly denser rows. Mobile search/filter controls collapse using a native details element. Profile problem links wrap long unbroken titles rather than expanding the page.

Friends/Following leave the primary menu. Both routes and Users tabs remain, and Users stays marked current for either deep link.

Validation: problem-modes.py passes 24 width/theme/mode combinations, persistence, pagination, empty/loading/error, stored notes/progress, eight public routes and Users subtabs/deep links. Catalog UI8, priority UI7, problem dialog17, publication workflow5 and editor regression checks pass. The full rating matrix remains correct in light/dark and all three surfaces; contrast minima4.537/7.253. Screenshots inspected locally at1440/375 using bundled offline data. Interaction timings are Playwright round trips on125 synthetic records, not production network/render benchmarks.

Production/live authenticated behavior, exhaustive accessibility audit and remaining package4 data/research requirements are still open. No migrations, imports, merge or deployment performed.
