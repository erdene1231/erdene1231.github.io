# Browser PDF dependencies

- `pdf-lib.min.js`: pdf-lib 1.17.1, npm package `pdf-lib`, MIT. See LICENSE-pdf-lib.md.
- `fontkit.umd.min.js`: @pdf-lib/fontkit 1.1.1, npm package `@pdf-lib/fontkit`, MIT as declared by the package. The package's upstream README, including its license declaration and project links, is preserved as NOTICE-fontkit.md.
- Fonts in `../fonts`: unchanged DejaVu Sans regular/bold TTFs, with their distributed notices in LICENSE-DejaVu.txt.

These files are loaded from the site itself when PDF export is requested.
No third-party PDF service receives the report data.
