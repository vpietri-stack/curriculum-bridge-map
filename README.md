# Curriculum Atlas

[Open the public teaching map](https://vpietri-stack.github.io/curriculum-bridge-map/).

The current edition compares **Power Up 1**, **iShow Act 3**, and **iShow Play 1** with the revised PEP public-school English textbooks. It is a standalone static site with no login or backend.

## How to use it

Choose a book and unit, then read each lesson topic from left to right:

- **The source lesson** lists vocabulary, sentence patterns, and phonics from the Power Up Teacher's Book or the iShow TLS workbook. Words used in a taught pattern, even when absent from its separate vocabulary list, appear as “Words also used in patterns.”
- **Already aligned with PEP** includes explicit vocabulary, words used in taught patterns, and sentence frames already taught. Expand the green section to inspect the PEP evidence.
- **Consider adding from PEP** holds new vocabulary and sentence patterns. A “Related form” badge marks a similar expression that is still worth teaching explicitly.
- PEP rows link to the textbook page and identify a **target** or **main reading/dialogue**. Extra dialogue examples are collapsed inside each topic and can be revealed or filtered.

The search box finds units, topics, words, patterns, and PEP entries. Clicking a source item shows its PEP evidence. Clicking a PEP entry shows matching Power Up and iShow topics.

## Scope and comparison rules

| Source book | PEP ceiling | Prior learning counted |
| --- | --- | --- |
| iShow Act 3 | Grade 4 | Earlier Act 3 topics |
| Power Up 1 | Grade 4 | Earlier PU1 units, including the separate welcome Unit 0 |
| iShow Play 1 | Grade 4 | Act 3 and earlier Play 1 topics |

Each topic card compares only its subject with relevant PEP items, rather than adding every word from a loosely related PEP unit. Explicit words and words spoken in sentence patterns taught earlier in the same source path count as prior learning. Related expressions stay in the additions column. Core lessons, cross-curricular sections, literature, review, and phonics appear as source topics. The PEP target and main-dialogue inventory currently covers Grades 3 and 4. PEP phonics targets are not indexed yet, so phonics cards show the source curriculum only.

The full previously collected catalog remains in [`catalog.json`](catalog.json) for later expansion to Power Up 2–4, iShow Play 2–4, and the higher PEP grades. The focused site reads [`focus.json`](focus.json).

## Sources and data notes

- [PEP textbook library](https://www.ai2book.com/diandu/)
- Power Up 1 Teacher's Book scans in the local `PU - Think` Google Drive folder. The welcome Unit 0 is drawn from Teacher Book scan pages 18–21; Unit 1 includes the cross-curricular language on scan pages 35–36.
- iShow Act 3 and Play 1 TLS workbooks in the local `curriculum maps` Google Drive folder. A3 means Act 3 and P1 means Play 1.

The site publishes short teaching items and page references, not scans, images, audio, or complete readings. Some source pages are OCR scans; the scripts include manual corrections for joined or misspelled words. The map is a planning aid, so check the cited page before using a suggestion in an assessment.

## Run and rebuild locally

Run `python -m http.server 8000` in this directory and open `http://localhost:8000`.

For the focused data, run `python build_focused.py` followed by `python focus_alignment.py`. The first script creates an intermediate `focus_sources.json` from the local source inventories. The second creates the published `focus.json`. The original full-catalog generation scripts remain available; their OCR and source files stay local under ignored `sources/`.
