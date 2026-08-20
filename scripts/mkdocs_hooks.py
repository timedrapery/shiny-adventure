#!/usr/bin/env python3
"""MkDocs build hooks for the reader's edition.

Currently one job: make Pali searchable without a Pali keyboard.

The search index built by the Material search plugin contains only the
diacritic forms the translations actually use (`nibbāna`, `anattā`,
`saḷāyatana`). Neither the indexer nor the client-side query pipeline folds
diacritics, so a reader typing `nibbana` gets no results at all, even though
twelve pages discuss it. That directly undercuts the point of the reader's
edition, which exists to make this material reachable by ordinary readers.

The fix runs entirely at build time and changes nothing a reader sees on the
page: after the search plugin writes `search_index.json`, this hook adds the
ASCII-folded form of any accented word alongside the original, so both
spellings match the same page.
"""

from __future__ import annotations

import json
import os
import re
import unicodedata


# A word containing at least one letter. Kept deliberately broad: the point is
# to catch Pali as it appears in running prose, headings, and glossary lines.
WORD = re.compile(r"\w+", re.UNICODE)


def fold(word: str) -> str:
    """The ASCII-ish form of a word, with diacritics removed.

    Uses the same NFKD + combining-mark strip that `scripts/text_utils.py`
    applies to `normalized_term`, but preserves case and does not mangle word
    boundaries, since this text is fed to a search tokenizer rather than used
    as a filename.
    """
    decomposed = unicodedata.normalize("NFKD", word)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def add_aliases(text: str) -> tuple[str, int]:
    """Insert each accented word's ASCII spelling after its first occurrence.

    Placement matters for more than tidiness. Material builds search result
    previews from this same text, so collecting the aliases into one block at
    the end makes an ASCII match preview as a run of context-free words. Put
    inline instead, the alias sits inside a real sentence, and the preview
    reads normally.

    Only the first occurrence of each distinct word is given an alias: that is
    enough for lunr to match the page, and repeating it at every occurrence
    would bloat the index and double words throughout the preview text.
    """
    seen: set[str] = set()
    out: list[str] = []
    last = 0
    added = 0

    for match in WORD.finditer(text or ""):
        word = match.group(0)
        folded = fold(word)
        if folded == word or not folded or folded in seen:
            continue
        seen.add(folded)
        out.append(text[last:match.end()])
        out.append(f" {folded}")
        last = match.end()
        added += 1

    out.append(text[last:])
    return "".join(out), added


def on_post_build(config, **kwargs) -> None:
    path = os.path.join(config["site_dir"], "search", "search_index.json")
    if not os.path.exists(path):
        # Search is disabled, or the plugin has not run. Nothing to do, and
        # nothing worth failing the build over.
        return

    with open(path, encoding="utf-8") as handle:
        index = json.load(handle)

    docs = index.get("docs")
    if not isinstance(docs, list):
        return

    added = 0
    for doc in docs:
        text, count = add_aliases(doc.get("text", ""))
        doc["text"] = text
        added += count

        # A page whose accented word appears only in its title still has to be
        # findable, so fold those in too. The title itself is left alone: it is
        # displayed verbatim as the search result heading.
        title_aliases = []
        for match in WORD.finditer(doc.get("title", "")):
            word = match.group(0)
            folded = fold(word)
            if folded != word and folded and folded not in text:
                title_aliases.append(folded)
        if title_aliases:
            doc["text"] = f"{text} {' '.join(dict.fromkeys(title_aliases))}".strip()
            added += len(set(title_aliases))

    with open(path, "w", encoding="utf-8") as handle:
        json.dump(index, handle, ensure_ascii=False, separators=(",", ":"))

    print(f"INFO    -  Search: added {added} ASCII aliases for accented words")
