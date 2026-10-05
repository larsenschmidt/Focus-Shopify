# The Conservatory

A running coach for one seeker: writer, speaker, thinker, in English and Spanish, with Italian, Danish, Chinese and French underneath. The design is on the page; this folder is the engine that runs it.

The coach is Claude Code, governed by `CLAUDE.md` (the law) and the skills in `.claude/skills/`. The coach never writes a sentence that enters your work. It interrogates, points, measures, compares you with the masters, and sets one target for tomorrow.

## Start

```
cd conservatory
claude
```

Then, in order:

1. **Day 0, before anything.** Open `days/day-00/README.md` and do the sealed tasks. Nothing is critiqued. Commit it. This is the control for every diff you will ever run.
2. **Set the start.** In `config.json`, put the date of your first real day in `start_date` and the master you are reading in `current_master`.
3. **Every morning:** `/today`. It creates `days/day-NN/` from the templates and prints the plan: languages, exercise, speaking drill, rotation language, the piece, and yesterday's one target.
4. **Then the day, block by block.** Each block has a file. The coach's skills are run when the file says so:

| Block | File | Skill |
|---|---|---|
| Morning pages | `00-morning-pages.md` | none, ever |
| Reading the master | `01-reading.md` | `/compare` on Sundays |
| Reps | `02-reps.md` | `/reps` |
| The essay | `03-essay.md` | `/interrogate`, then `/critique` |
| Speaking | `04-speaking.md` | `scripts/transcribe.py`, then `/speech` |
| Recitation & shadowing | `05-recitation.md` | `/palace` when a piece or talk needs one |
| Languages | `06-languages.md` | `/correct`, `/palace` for characters |
| Noticing | `07-noticing.md` | none |
| Evening reading | `08-evening.md` | none |
| Review | `09-review.md` | `/review` |

5. **Commit every night** with the line `/review` gives you.
6. **Weekly:** `/dissent` on Sunday. **Monthly:** `/baseline`.

## Scripts

- `scripts/newday.py [YYYY-MM-DD]` · opens a day.
- `scripts/transcribe.py AUDIO --lang es` · transcript with pauses, plus `metrics.json`: duration, words, wpm, fillers by type, false starts, longest pause. Needs `pip install faster-whisper` (or `openai-whisper` and ffmpeg). Without a transcriber, pass a `.txt` transcript and `--duration SECONDS`.
- `scripts/deck.py add --front "..." --back "..." --tags it,interference` · a card from your own error. `deck.py export` prints Anki import steps.
- `scripts/progress.py` · the numbers: days, streak, essays, words, filler trend, gap mean, deck, pieces.

## The bad day

Ninety minutes: the essay, one impromptu, `/review`. It counts.

## Moving this to its own repository

It is self-contained. From the repo root: `git subtree split -P conservatory -b conservatory` and push that branch wherever you like.
