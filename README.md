# Curriculum Atlas

An English-language, unit-first comparison of Power Up, iShow 2.0, and the revised PEP public-school English series. The standalone site is published at [Curriculum Atlas](https://vpietri-stack.github.io/curriculum-bridge-map/).

## What the map covers

- **Power Up 1–4:** Nine units per level, indexed from the Teacher's Books in the local `PU - Think` Drive folder. Vocabulary in PU1–3 was checked against the separate word-list workbooks for OCR spelling. The map does not use Power Up TLS files. Grammar targets were edited into readable teaching patterns from the Teacher's Book language-practice panels; the cited scan page accompanies each pattern.
- **iShow 2.0:** Act 3, then Play 1–4, with nine topics per level. Vocabulary and sentence structures come from the TLS workbooks. Session 5 phonics and review material is shown separately.
- **PEP:** Revised three-year-starting-point books from Grade 3 Fall through Grade 6 Fall: 42 units across seven books. Grade 6 Spring is not listed in the revised sequence on the source site as of 12 November 2026. PEP vocabulary and useful expressions come from the unit appendices, linked to their first unit occurrence where found. Main reading and dialogue lines are separately indexed with page links. The site distinguishes PEP target evidence from reading/dialogue evidence.

Choose a unit, then click vocabulary or a structure to see exact and related matches. **Add from PEP** suggests items absent from the selected Power Up or iShow unit, across selected related PEP units. Related forms remain visible and labelled. Filter additions by grade, theme or grammar concept, and optionally include main reading/dialogue lines. Global search accepts unit labels, words, themes, and grammar terms. Choose a PEP unit to look up matches in reverse.

## Sources and limits

- [PEP textbooks on ai2book](https://www.ai2book.com/diandu/)
- [People's Education Press overview of the revised series](https://www.pep.com.cn/xw/zt/hd/12/xjcjs/xx/202409/t20240920_1995564.html)

The map contains page links, short vocabulary items, teaching patterns, and selected short reading/dialogue lines. It does not redistribute PDFs, images, audio, or full textbooks. OCR and automatic theme grouping can still make errors; use the linked PEP page and the cited Teacher's Book scan page when planning lessons. Related matches and suggested PEP units are planning aids, not claims of identical coverage or exam priority.

## Local use and regeneration

Run `python -m http.server 8000` in this directory, then open `http://localhost:8000`.

`catalog.json` is the published dataset. The Python scripts build it from locally held source files. `sources/` and logs stay ignored. Regeneration order after the inputs are present: `fetch_pep.py`, `ocr_teacher.py` for each Power Up Teacher's Book, `extract_teacher_blocks.py`, `read_wordlist.py`, `build_pep_inventory.py`, `build_powerup.py`, `build_ishow.py`, then `build_catalog.py`. The current scripts contain the local source paths used for this edition and are not required to run the site.
