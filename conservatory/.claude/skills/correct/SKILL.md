---
name: correct
description: Corrects the seeker's writing in Italian, Danish, French or Chinese in the fixed shape, tags interference, gives one labeled native model, and writes cards from the errors through scripts/deck.py.
---
Input: the seeker's paragraph in the language's section of `06-languages.md`.

Output under `### Correction`:
1. Table: You wrote | The fix | Why. One row per error. Tag interference: "(ES leaking)", "(EN leaking)". Mark correct sentences ✓ and name the pattern that held.
2. **Native model, read aloud three times, then close:** one paragraph. The only prose you write here.
3. Pattern: one line for `log/errors.md` if this error type has appeared before (check the file). Say which days.
4. Cards: for each interference or register error, one card from the seeker's own sentence: `python3 scripts/deck.py add --front "..." --back "..." --tags lang,interference`. Front is the context, never a bare word. At most six a day across languages.

Language notes:
- Chinese: register (spoken one-syllable word where the written two-character form belongs), 了/在/着, measure words, word order, 把/被. Fifteen characters a day: run `/palace` for them.
- Danish: V2 word order, en/et, the definite suffix, der/som, adverb placement. Pronunciation only when the seeker asks after shadowing.
- Italian: prepositions, possessive overuse, diphthong stems, congiuntivo, partitive ne, future for conjecture.
- French (Wednesday): input first. Six sentences. Light.

Explanations in English until the seeker asks for them in the target language.
