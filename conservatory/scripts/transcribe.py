#!/usr/bin/env python3
"""Transcribe a recorded take and measure it.

  python3 scripts/transcribe.py days/day-12/audio/take1.m4a --lang es
  python3 scripts/transcribe.py take1.txt --lang es --duration 168      # text fallback, no transcriber needed

Writes <input>.transcript.md and <input>.metrics.json next to the input.
Transcriber: pip install faster-whisper   (or: pip install openai-whisper, plus ffmpeg)
"""
import argparse
import json
import os
import re
import sys

FILLERS = {
    "en": ["um", "uh", "er", "like", "you know", "so", "basically", "actually", "i mean", "kind of", "sort of", "right", "okay so"],
    "es": ["eh", "este", "o sea", "bueno", "pues", "no?", "como que", "digamos", "en realidad", "la verdad", "a ver", "tipo", "sabes?"],
    "it": ["cioè", "allora", "ecco", "diciamo", "insomma", "tipo", "praticamente", "niente", "ehm", "no?", "capito"],
    "da": ["øh", "øhm", "altså", "ligesom", "sådan", "jo", "ik'", "ikke?", "bare", "faktisk", "på en måde"],
    "fr": ["euh", "ben", "en fait", "genre", "du coup", "voilà", "bon", "quoi", "tu vois", "enfin", "bah"],
    "zh": ["那个", "这个", "就是", "然后", "嗯", "啊", "对", "就是说", "怎么说", "那种"],
}
PAUSE = 1.5


def transcribe(path, lang):
    try:
        from faster_whisper import WhisperModel  # type: ignore
        model = WhisperModel("small", compute_type="int8")
        segments, _ = model.transcribe(path, language=lang, word_timestamps=True)
        words = []
        for seg in segments:
            for w in seg.words or []:
                words.append({"w": w.word.strip(), "s": float(w.start), "e": float(w.end)})
        return words
    except ImportError:
        pass
    try:
        import whisper  # type: ignore
        model = whisper.load_model("small")
        r = model.transcribe(path, language=lang, word_timestamps=True)
        words = []
        for seg in r["segments"]:
            for w in seg.get("words", []):
                words.append({"w": w["word"].strip(), "s": float(w["start"]), "e": float(w["end"])})
        return words
    except ImportError:
        pass
    sys.exit("No transcriber installed. pip install faster-whisper (or openai-whisper + ffmpeg), or pass a .txt transcript with --duration SECONDS.")


def from_text(path, duration):
    with open(path, encoding="utf-8") as f:
        toks = f.read().split()
    if not toks:
        sys.exit("empty transcript")
    step = duration / len(toks)
    return [{"w": t, "s": i * step, "e": (i + 1) * step} for i, t in enumerate(toks)]


def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--lang", required=True, choices=sorted(FILLERS))
    ap.add_argument("--duration", type=float, help="seconds; required with a text input")
    a = ap.parse_args()

    text_input = a.input.lower().endswith((".txt", ".md"))
    if text_input:
        if not a.duration:
            sys.exit("--duration SECONDS is required with a text input")
        words = from_text(a.input, a.duration)
    else:
        words = transcribe(a.input, a.lang)
    if not words:
        sys.exit("nothing transcribed")

    duration = a.duration or words[-1]["e"]
    text = " ".join(w["w"] for w in words)
    low = text.lower()
    if a.lang == "zh":
        n_words = len(re.findall(r"[一-鿿]", text))
    else:
        n_words = len(re.findall(r"[\w'’]+", text, re.UNICODE))
    wpm = round(n_words / duration * 60) if duration else 0

    fillers = {}
    for f in FILLERS[a.lang]:
        if a.lang == "zh":
            c = low.count(f)
        else:
            c = len(re.findall(r"(?<![\w'’])" + re.escape(f) + r"(?![\w'’])", low))
        if c:
            fillers[f] = c
    n_fillers = sum(fillers.values())

    false_starts = len(re.findall(r"\b((?:[\w'’]+\s+){0,2}[\w'’]{2,})\b[\s,…\-–]+\1\b", low)) + len(re.findall(r"[\w'’]+-(?:\s|$)", text))

    pauses = []
    for i in range(1, len(words)):
        gap = words[i]["s"] - words[i - 1]["e"]
        if gap >= PAUSE:
            pauses.append({"at": mmss(words[i - 1]["e"]), "seconds": round(gap, 1), "before": " ".join(x["w"] for x in words[max(0, i - 6):i])})
    longest = max(pauses, key=lambda p: p["seconds"]) if pauses else None

    lines = []
    cur = []
    for i, w in enumerate(words):
        if i and words[i]["s"] - words[i - 1]["e"] >= PAUSE:
            cur.append(f"[pause {words[i]['s'] - words[i - 1]['e']:.1f}s]")
        if i % 30 == 0:
            if cur:
                lines.append(" ".join(cur))
                cur = []
            cur.append(f"[{mmss(w['s'])}]")
        cur.append(w["w"])
    if cur:
        lines.append(" ".join(cur))

    base = os.path.splitext(a.input)[0]
    metrics = {
        "input": os.path.basename(a.input),
        "lang": a.lang,
        "duration": round(duration, 1),
        "duration_mmss": mmss(duration),
        "words": n_words,
        "wpm": wpm,
        "fillers": n_fillers,
        "fillers_by_type": dict(sorted(fillers.items(), key=lambda kv: -kv[1])),
        "false_starts": false_starts,
        "pauses_over_1_5s": len(pauses),
        "longest_pause": longest,
        "claim_time": None,
        "note": "claim_time is filled by the coach in /speech; the machine cannot hear a claim.",
    }
    with open(base + ".transcript.md", "w", encoding="utf-8") as f:
        f.write(f"# Transcript · {os.path.basename(a.input)} · {a.lang}\n\n")
        f.write("\n".join(lines) + "\n\n")
        f.write(f"duration {mmss(duration)} · {n_words} words · {wpm} wpm · fillers {n_fillers} · false starts {false_starts}")
        if longest:
            f.write(f" · longest pause {longest['seconds']}s at {longest['at']}")
        f.write("\n")
    with open(base + ".metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    print(f"\nwrote {base}.transcript.md and {base}.metrics.json")


if __name__ == "__main__":
    main()
