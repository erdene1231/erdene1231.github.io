# Exact problem numbers and simpler rating controls

Shared catalog search treats #1 / #001 as exact problem number1, rather than
matching10/100. Text queries retain existing token search. Popup rows expose #number.
Main and modal Rating-band selectors are removed; Min/Max rating remain.
Frontend graph v35. Regression: tests/number-search.test.mjs; npm test PASS.
No database changes. Existing IDs/progress retained. Deploy after review/merge.
