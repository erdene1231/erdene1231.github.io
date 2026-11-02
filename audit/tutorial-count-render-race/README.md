#76 tutorials counted but no cards rendered

The user's actual screenshot was materialized and visually inspected:all/default filters,76/76 count, stale “No matching tutorials” text, and account progress loaded. The screenshot contains private account details and is deliberately not copied into this repository.

PR266 removed a separate course/seed dependency, but did not fix this mismatch. The count updated synchronously while the card-building callback waited in the global MathJax queue. An initial empty-list callback had already painted the no-results message. If that job waited for math, later76-card callbacks could not replace the old DOM, even though their counters had updated.

The baseline at d67776d was reproduced exactly using the actual current Supabase SDK, captured anonymous76-lesson public payload and native app/store. Hold MathJax, paint initial empty state, then release the tutorial RPC:count76, cards0, same no-results text. This identifies a rendering race independent of category or login permissions. Native synthetic guest reading records exercise the same mastery badge path; no real authenticated session is claimed.

Fix:build the card fragment and replace the list synchronously with the current filter state. MathJax is queued only for optional formatting, guarded by the current render generation. Lesson text/section navigation likewise build independently of math, so clicking a card does not present another blocked empty reader. One MathJax script/queue is retained. Seven reverse imports are refreshed at98.

Browser regression:76 cards while math remains held; all actual categories; MN/EN; default/priority order; search; priority/level changes; loaded read badge; old/new lesson text and section navigation before math is released; math completion, navigation, reload,375/1280 widths and one loader. The all100-day/native quiz/editor suite is rerun too. No content, SQL, migrations, authentication or access changes. Live browser TLS restriction is not bypassed; deployed-byte/public-payload checks are reported after release.
