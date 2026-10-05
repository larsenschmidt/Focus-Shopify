#!/usr/bin/env python3
"""The numbers. Writes progress.md and prints the table."""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def section(text, heading):
    m = re.search(r"^" + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def metrics(day, take):
    for p in glob.glob(os.path.join(day, "audio", f"{take}*.metrics.json")):
        try:
            return json.load(open(p, encoding="utf-8"))
        except Exception:
            pass
    return None


def main():
    days = [d for d in sorted(glob.glob(os.path.join(ROOT, "days", "day-[0-9]*"))) if not d.endswith("day-00")]
    rows = []
    for d in days:
        essay = read(os.path.join(d, "03-essay.md"))
        pub = re.search(r"^Published:[ \t]*(\S.*)$", essay, re.M)
        published = bool(pub and pub.group(1).strip().lower() not in ("no", "none", "-", "(url)"))
        words2 = len(section(essay, "## Draft 2").split())
        words1 = len(section(essay, "## Draft 1").split())
        review = read(os.path.join(d, "09-review.md"))
        done = bool(re.search(r"^Tomorrow:[ \t]*\S", review, re.M))
        gap = re.search(r"score\s*[:=]?\s*([01](?:\.\d+)?)", review, re.I)
        t1, t2 = metrics(d, "take1"), metrics(d, "take2")
        rows.append({
            "day": os.path.basename(d), "done": done, "published": published,
            "w1": words1, "w2": words2, "gap": float(gap.group(1)) if gap else None,
            "f1": t1["fillers"] if t1 else None, "f2": t2["fillers"] if t2 else None,
        })

    streak = 0
    for r in reversed(rows):
        if r["done"]:
            streak += 1
        else:
            break
    deck = read(os.path.join(ROOT, "deck", "cards.tsv")).count("\n") - 1
    pieces = read(os.path.join(ROOT, "pieces", "README.md"))
    known = len(re.findall(r"^\s*-.*\bknown\b", pieces, re.M))
    inprog = len(re.findall(r"^\s*-.*\bin progress\b", pieces, re.M))
    gaps = [r["gap"] for r in rows if r["gap"] is not None][-7:]
    f1s = [r["f1"] for r in rows if r["f1"] is not None]
    published = [r for r in rows if r["published"]]

    table = [
        ("Days opened", len(rows)),
        ("Days done (review written)", sum(1 for r in rows if r["done"])),
        ("Streak", streak),
        ("Essays published", len(published)),
        ("Words published (draft 2)", sum(r["w2"] for r in published)),
        ("Take-one fillers, first → latest", f"{f1s[0]} → {f1s[-1]}" if f1s else "no recordings measured"),
        ("Prediction gap, 7-day mean", f"{sum(gaps) / len(gaps):.2f}" if gaps else "no scores yet"),
        ("Cards in the deck", max(deck, 0)),
        ("Pieces known / in progress", f"{known} / {inprog}"),
    ]
    out = "| | |\n|---|---|\n" + "\n".join(f"| {k} | {v} |" for k, v in table) + "\n"
    with open(os.path.join(ROOT, "progress.md"), "w", encoding="utf-8") as f:
        f.write("# Progress\n\n" + out)
    print(out)


if __name__ == "__main__":
    main()
