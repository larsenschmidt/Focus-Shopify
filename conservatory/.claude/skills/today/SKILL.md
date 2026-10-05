---
name: today
description: Open the day. Runs scripts/newday.py, reads yesterday's target from log/targets.md, and states the plan in one screen. Use at the start of every day.
---
1. Run `python3 scripts/newday.py` from the conservatory directory. It creates `days/day-NN/` from the templates and prints the plan: essay language and exercise, speaking language and drill with its prompt, rotation language, the piece, the master, and whether this is a light week.
2. Read the last line of `log/targets.md`. That is today's one target. Put it at the top of your reply, verbatim.
3. Read `log/errors.md`. Do not list it. Hold it for the day.
4. Reply in one screen: the target, the plan, and the first instruction: "Morning pages. Close the coach."

Never open `00-morning-pages.md`, today or any day.
