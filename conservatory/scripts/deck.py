#!/usr/bin/env python3
"""Cards from your own errors, never from word lists.

  python3 scripts/deck.py add --front "ES 'en el tren' → IT ___ treno" --back "sul treno · the leak: en → nel" --tags it,interference
  python3 scripts/deck.py count
  python3 scripts/deck.py export
"""
import argparse
import datetime
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = os.path.join(ROOT, "deck", "cards.tsv")


def today_label():
    days = sorted(glob.glob(os.path.join(ROOT, "days", "day-[0-9]*")))
    return os.path.basename(days[-1]) if days else datetime.date.today().isoformat()


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--front", required=True)
    a.add_argument("--back", required=True)
    a.add_argument("--tags", default="")
    sub.add_parser("count")
    sub.add_parser("export")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(DECK), exist_ok=True)
    if not os.path.exists(DECK):
        with open(DECK, "w", encoding="utf-8") as f:
            f.write("front\tback\ttags\tday\n")

    if args.cmd == "add":
        row = [args.front, args.back, args.tags, today_label()]
        row = [c.replace("\t", " ").replace("\n", " ") for c in row]
        with open(DECK, "a", encoding="utf-8") as f:
            f.write("\t".join(row) + "\n")
        print("added:", row[0], "→", row[1])
    elif args.cmd == "count":
        with open(DECK, encoding="utf-8") as f:
            n = sum(1 for _ in f) - 1
        print(f"{n} cards in {os.path.relpath(DECK, ROOT)}")
    elif args.cmd == "export":
        print("Anki: File → Import → choose deck/cards.tsv → fields separated by Tab → "
              "map front, back, tags; allow HTML off; first line is a header. Review daily; the deck is small on purpose.")


if __name__ == "__main__":
    main()
