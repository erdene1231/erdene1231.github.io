# International olympiad URL audit — source access gap

The current 1064-row catalog contains161 olympiad-source rows. No URL was changed.
Normal executor HTTPS access returned403 for all eight oj.uz source-list roots,
without Retry-After. These denials do not establish that any task is absent.
No identity/proxy/host workaround or guessed individual identifier was used.

| Source | Total | Existing individual oj.uz retained | Other URL retained, access inconclusive |
|---|---:|---:|---:|
| IOI |54|46|8|
| APIO |27|20|7|
| JOI |24|4|20|
| EGOI |45|36|9|
| USACO |6|0|6|
| CEOI |2|2|0|
| COCI |2|2|0|
| BOI |1|1|0|
| Total |161|111|50|

The36 EGOI matches retain the earlier same-day source/year traversal and
individual-page evidence in [the prior manifest](../egoi-ojuz/manifest.json).
The other existing oj.uz links are retained as preferred-platform URLs; this
phase does not claim fresh individual verification for them.

Before the executor denials, the standard web tool returned cached public
JOI/IOI/APIO root listings with a four-day crawl age. Those roots reveal
subcategories/years/aliases but do not prove complete pagination or individual
page identity. APIO's listing indicates possible preferred replacements for
existing QOJ links; no change is made without individual-page verification.

The normal public web route independently confirmed the title and APIO year of
all six existing QOJ pages: [Mars](https://qoj.ac/problem/4250),
[Magic Show](https://qoj.ac/problem/8726), [Hack!](https://qoj.ac/problem/9205),
[Permutation Game](https://qoj.ac/problem/9206),
[Navigation](https://qoj.ac/problem/17644), and
[Scallion Pancake Party](https://qoj.ac/problem/17645). These are cached public
pages with two-to-three-day crawl ages. Their existence does not establish
absence on oj.uz and authorizes no fallback/downgrade.

The empty allowlist records zero changed-to-oj.uz, zero changed-to-QOJ, zero
conclusive no-match findings, and50 nonpreferred access-inconclusive rows.
All161 URLs remain unchanged; fresh oj.uz individual/pagination coverage is
unavailable. No SQL, catalog mutation, replay or migration was performed.
The source snapshot follows publication of all51 native editorials, preserving
those documents and all statement/I/O/provenance/metadata values.

See [manifest.json](manifest.json) for every category, target, before/after URL,
revision/body hash, denial and evidence limit. Continue the six independent UI
items; revisit URL resolution only through normally available source access.
