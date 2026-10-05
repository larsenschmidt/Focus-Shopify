---
name: review
description: End of day. Reads everything the seeker wrote today except morning pages, updates the error log by pattern, checks the cards, sets one target for tomorrow, runs progress.py, and writes the commit line.
---
1. Read today's folder. Never `00-morning-pages.md`.
2. `log/errors.md`: for every finding today, find its pattern row or add one: where | pattern | days seen | status. Statuses: first instance, forming, pattern, tomorrow's rule, retired. A pattern absent from critique five days running is retired; say so.
3. Gap: record today's score in `09-review.md` and the running mean of the last seven days.
4. Cards: `python3 scripts/deck.py count`. At most ten a day across languages.
5. Tomorrow's target: ONE. The pattern with the most days seen that is not already a rule. Write it as a rule obeyable at the desk ("The first sentence is a thing you saw"), never a wish ("be more concrete"). Append to `log/targets.md`: `day-NN | lang | the rule`.
6. Numbers: run `python3 scripts/progress.py` and paste the table into `09-review.md`.
7. Commit line, one line: `day-NN: essay xx vN published (Aw→Bw); speech xx F1→F2 fillers; piece status; cards n; tomorrow: rule`. The seeker commits.
8. Sunday: read `phases.md`. For each gate condition, say met or not, with the evidence from the logs.
9. Last line, always: "22:00. The piece from the cue. Then sleep."
