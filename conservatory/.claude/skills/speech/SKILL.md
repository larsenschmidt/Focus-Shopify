---
name: speech
description: Reads the transcript and metrics from scripts/transcribe.py for a take, gives the fixed-shape speech critique and one target, then reviews take two. Covers impromptu, three audiences, hostile question, prepared talk.
---
Precondition: the seeker ran `python3 scripts/transcribe.py days/day-NN/audio/take1.m4a --lang xx`, read the transcript aloud cold, watched the take muted, and wrote two lines under `### Self-critique` plus one line under `Body:`. If any is missing, ask for it and stop.

Take 1, fixed shape from `CLAUDE.md`:
- The clearest sentence, quoted, with its timestamp. Say whether the seeker noticed it.
- When the claim arrived.
- A promise broken ("there are several reasons", then two). An edit out loud ("no, wait"). The longest pause and the words before it.
- One target for take two. One. Usually: the claim is the first sentence; stop when done.

Take 2:
- Numbers side by side: duration, words, wpm, fillers, false starts, claim time.
- The line of the day, quoted. Append it to `log/lines.md` as `day-NN | lang | "..."`.
- Whether the target held. Check `log/targets.md`; if a speaking target held five consecutive days, say it retires and the next pattern takes its place.

Drills by weekday:
- Three audiences (Tue): same idea, ninety seconds each, to a child, a skeptic, an expert. After: which one the seeker believed, with the words that show it.
- Hostile question (Wed): you ask the hardest question about yesterday's essay, in the speaking language. Sixty seconds. Critique: did they answer the question asked, quoted.
- Prepared talk (Fri): seven minutes. The transcript must read as prose. If a paragraph does not, name it; deliver again.

You cannot see the body. Do not coach it from a transcript. Record the seeker's one noted thing and compare it with last week's.
