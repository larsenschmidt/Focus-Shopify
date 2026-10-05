#!/usr/bin/env python3
"""Open a day: create days/day-NN from templates/day and print the plan.
Usage: python3 scripts/newday.py [YYYY-MM-DD]
"""
import datetime
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG_PATH = os.path.join(ROOT, "config.json")
TPL = os.path.join(ROOT, "templates", "day")
DAYS = os.path.join(ROOT, "days")

NAMES = {"en": "English", "es": "Spanish", "it": "Italian", "da": "Danish", "fr": "French", "zh": "Chinese"}
ROTATION = {0: "it", 1: "da", 2: "fr", 3: "it", 4: "da", 5: "it", 6: None}  # Mon..Sun
DRILL = {
    0: "impromptu",
    1: "three audiences",
    2: "hostile question",
    3: "impromptu",
    4: "prepared talk (7 min, written last night)",
    5: "read the long essay aloud",
    6: "rest",
}
EXERCISES = ["Fable", "Narrative", "Chreia", "Maxim", "Refutation", "Confirmation"]


def pick_prompt(cfg, lang, seed):
    path = os.path.join(ROOT, "prompts", f"impromptu-{lang}.txt")
    with open(path, encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    used = cfg.setdefault("used_prompts", {}).setdefault(lang, [])
    remaining = [p for p in lines if p not in used] or lines
    if not [p for p in lines if p not in used]:
        used.clear()
    choice = random.Random(seed).choice(remaining)
    used.append(choice)
    return choice


def current_piece():
    path = os.path.join(ROOT, "pieces", "README.md")
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        return "none"
    for status in ("in progress", "queued"):
        for l in lines:
            if l.lstrip().startswith("-") and status in l:
                return l.lstrip("- ").strip()
    return "none: queue one in pieces/README.md"


def main():
    with open(CFG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    start = datetime.date.fromisoformat(cfg["start_date"])
    today = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.date.today()
    n = (today - start).days + 1
    if n < 1:
        sys.exit(f"start_date in config.json is {start}. Before it there is only Day 0: days/day-00/README.md")
    wd = today.weekday()
    essay_lang = "en" if n % 2 == 1 else "es"
    speak_lang = "es" if essay_lang == "en" else "en"
    rot = ROTATION[wd]
    drill = DRILL[wd]
    if wd == 5:
        exercise = "Long essay: grow the week's best short one to 1,500 words in five drafts"
    elif wd == 6:
        exercise = "No essay. Franklin reconstruction in 01-reading.md, then /compare and the weekly review"
    else:
        exercise = EXERCISES[(n - 1) % len(EXERCISES)]
    week = (n - 1) // 7 + 1
    light = week % 7 == 0
    if drill in ("impromptu", "three audiences"):
        prompt = pick_prompt(cfg, speak_lang, n)
    elif drill == "hostile question":
        prompt = "the coach asks, from yesterday's essay"
    elif drill.startswith("prepared"):
        prompt = "your own, written last night"
    else:
        prompt = "none"
    piece = current_piece()
    master = cfg.get("current_master", "set current_master in config.json")
    rotation_name = NAMES[rot] if rot else "Sunday: tutors only (Italian, Danish, Chinese)"

    subs = {
        "DAY": f"{n:02d}",
        "DATE": today.isoformat(),
        "WEEKDAY": today.strftime("%A"),
        "WEEK": str(week),
        "ESSAY_LANG": NAMES[essay_lang],
        "SPEAK_LANG": NAMES[speak_lang],
        "SPEAK_CODE": speak_lang,
        "MP_LANG": NAMES[speak_lang],
        "EXERCISE": exercise,
        "DRILL": drill,
        "PROMPT": prompt,
        "ROTATION": rotation_name,
        "PIECE": piece,
        "MASTER": master,
        "LIGHT": "LIGHT WEEK: no new essays. Reread the corpus, revise the best three, recite everything, read." if light else "",
    }

    folder = os.path.join(DAYS, f"day-{n:02d}")
    if os.path.exists(folder):
        print(f"{folder} exists. Not touched.")
    else:
        os.makedirs(os.path.join(folder, "audio"))
        open(os.path.join(folder, "audio", ".gitkeep"), "w").close()
        for name in sorted(os.listdir(TPL)):
            with open(os.path.join(TPL, name), encoding="utf-8") as f:
                text = f.read()
            for k, v in subs.items():
                text = text.replace("{{" + k + "}}", v)
            with open(os.path.join(folder, name), "w", encoding="utf-8") as f:
                f.write(text)
        with open(CFG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"created {folder}")

    print()
    print(f"Day {n:02d} · {today.strftime('%A')} {today.isoformat()} · week {week}")
    if light:
        print(subs["LIGHT"])
    print(f"  morning pages  {NAMES[speak_lang]}")
    print(f"  reading        {master}")
    print(f"  essay          {NAMES[essay_lang]} · {exercise}")
    print(f"  speaking       {NAMES[speak_lang]} · {drill} · {prompt}")
    print(f"  recitation     {piece}")
    print(f"  languages      Chinese + {rotation_name}")
    print(f"  review         one target: see the last line of log/targets.md")


if __name__ == "__main__":
    main()
