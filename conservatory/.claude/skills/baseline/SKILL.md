---
name: baseline
description: Day 0 sealing and the monthly diff. Checks the sealed tasks for completeness only, never critiques them, and every thirty days lays the new run beside the old in the fixed shape.
---
Day 0 (`days/day-00/`): the tasks are in its README. Check completeness only: every file non-empty, every recording present. Write nothing about quality. Then tell the seeker: `git add days/day-00 && git commit -m "day-00: baseline sealed"`.

Monthly (`days/day-NN/baseline/`, every thirty days): same tasks, same prompts, same durations. Copy the README from day-00. Then the diff, per task:
- Essay (each language): stated in one sentence by a stranger, both runs; throat-clearing opening yes/no; abstractions per hundred words, counted; words; the sentence that worked in each.
- Impromptu (each language): duration, words, wpm, fillers, claim time, side by side.
- Read-aloud (each language): pace, pauses, sounds flagged.
- Six sentences (it, da, zh, fr): corrections per six, interference count, both runs.

End with: what changed, what did not, the one thing to aim the next thirty days at. The sealed run is never edited.
