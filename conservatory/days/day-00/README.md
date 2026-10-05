# Day 0 · the baseline · sealed

Do these before Day 1. Nothing is corrected. Nothing is critiqued, now or ever. Every thirty days you do them again in `days/day-NN/baseline/`, and the coach lays the two beside each other. This folder is the control for every diff you will ever run.

Forty minutes per essay, no revision, no coach. Three minutes per impromptu, standing, recorded. Read-aloud: two minutes per language, recorded. Six sentences per language, no dictionary.

| file | task |
|---|---|
| `essay-en.md` | "Describe a person you watched for ten minutes, and what you concluded." 40 min. |
| `essay-es.md` | "Describe a una persona que observaste durante diez minutos, y qué concluiste." 40 min. |
| `audio/impromptu-en.m4a` | "Convince someone who hates cooking to learn one dish." 3 min. Then `scripts/transcribe.py` → `impromptu-en.transcript.md`. |
| `audio/impromptu-es.m4a` | "Convence a alguien que odia cocinar de aprender un solo plato." 3 min. Transcribe. |
| `audio/read-{en,es,it,da,zh,fr}.m4a` | Read `pieces/en-bacon-of-studies.md` (en), Machado (es), and one paragraph of anything in each other language. 2 min each. |
| `sentences-it.md`, `sentences-da.md`, `sentences-zh.md`, `sentences-fr.md` | Six sentences each: what you did yesterday, and one opinion. No dictionary. |

When every file is non-empty: `/baseline` checks completeness, then
`git add days/day-00 && git commit -m "day-00: baseline sealed"`.

Then set `start_date` in `config.json` and tomorrow run `/today`.
