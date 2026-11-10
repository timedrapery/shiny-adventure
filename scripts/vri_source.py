#!/usr/bin/env python3
"""Locate a cited discourse in the VRI Chaṭṭha Saṅgāyana Tipiṭaka.

The repository's source checks used to read SuttaCentral's Mahāsaṅgīti root
text. Its publication record asks that it not be used in AI-derived work, and
this project is drafted with AI assistance, so the owner decided on 2026-11-10
to stop using SuttaCentral content (see `docs/source-text-policy.md`). This
module reads the Vipassana Research Institute's edition instead, from its
published XML (https://github.com/VipassanaTech/tipitaka-xml), whose terms are
"freely available for non-commercial use. Please attribute Vipassana Research
Institute when incorporating these files into your projects."

The VRI files are never committed here. They are fetched one book at a time
into a gitignored cache, or read from a local clone named by
`--vri-dir` / `$VRI_TIPITAKA_DIR`.

Citations keep the familiar numbering (`MN 10`, `SN 12.61`, `AN 3.65`). That
numbering is a scholarly convention, not SuttaCentral content. It is mapped onto
the VRI edition like this:

  DN n      the n-th numbered discourse heading across the three DN books
  MN n      the n-th numbered discourse heading across the three MN books
  SN s.n    the s-th saṃyutta across the five SN books, then the n-th
            discourse within it; a heading such as `3-10.` counts eight
  AN k.n    the k-th nipāta, then the passage whose paragraph number is n
  Dhp n     verse n, located by the verse-number markers
  Ud v.n, Snp v.n   the n-th discourse of vagga v
  Iti n     the n-th discourse across the collection

Numbering does not agree everywhere. Where VRI divides a passage differently,
`AN_PARAGRAPH_OFFSETS` below records the shift, with the evidence. A guess
that lands on the wrong discourse is caught downstream: the quoted Pali is not
found, and the verifier reports it rather than passing it.
"""

from __future__ import annotations

import html
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CACHE_DIR = REPO_ROOT / ".vri-cache"
RAW_BASE = "https://raw.githubusercontent.com/VipassanaTech/tipitaka-xml/main/romn"
EDITION = "Chaṭṭha Saṅgāyana Tipiṭaka, Vipassana Research Institute"
EDITION_URL = "https://tipitaka.org/romn/"

BOOKS: dict[str, tuple[str, ...]] = {
    "DN": ("s0101m", "s0102m", "s0103m"),
    "MN": ("s0201m", "s0202m", "s0203m"),
    "SN": ("s0301m", "s0302m", "s0303m", "s0304m", "s0305m"),
    "AN": (
        "s0401m", "s0402m1", "s0402m2", "s0402m3", "s0403m1", "s0403m2",
        "s0403m3", "s0404m1", "s0404m2", "s0404m3", "s0404m4",
    ),
    "Dhp": ("s0502m",),
    "Ud": ("s0503m",),
    "Iti": ("s0504m",),
    "Snp": ("s0505m",),
}
BOOK_TITLES = {
    "s0101m": "Dīghanikāya, Sīlakkhandhavaggapāḷi",
    "s0102m": "Dīghanikāya, Mahāvaggapāḷi",
    "s0103m": "Dīghanikāya, Pāthikavaggapāḷi",
    "s0201m": "Majjhimanikāya, Mūlapaṇṇāsapāḷi",
    "s0202m": "Majjhimanikāya, Majjhimapaṇṇāsapāḷi",
    "s0203m": "Majjhimanikāya, Uparipaṇṇāsapāḷi",
    "s0301m": "Saṃyuttanikāya, Sagāthāvaggapāḷi",
    "s0302m": "Saṃyuttanikāya, Nidānavaggapāḷi",
    "s0303m": "Saṃyuttanikāya, Khandhavaggapāḷi",
    "s0304m": "Saṃyuttanikāya, Saḷāyatanavaggapāḷi",
    "s0305m": "Saṃyuttanikāya, Mahāvaggapāḷi",
    "s0401m": "Aṅguttaranikāya, Ekakanipātapāḷi",
    "s0402m1": "Aṅguttaranikāya, Dukanipātapāḷi",
    "s0402m2": "Aṅguttaranikāya, Tikanipātapāḷi",
    "s0402m3": "Aṅguttaranikāya, Catukkanipātapāḷi",
    "s0403m1": "Aṅguttaranikāya, Pañcakanipātapāḷi",
    "s0403m2": "Aṅguttaranikāya, Chakkanipātapāḷi",
    "s0403m3": "Aṅguttaranikāya, Sattakanipātapāḷi",
    "s0404m1": "Aṅguttaranikāya, Aṭṭhakanipātapāḷi",
    "s0404m2": "Aṅguttaranikāya, Navakanipātapāḷi",
    "s0404m3": "Aṅguttaranikāya, Dasakanipātapāḷi",
    "s0404m4": "Aṅguttaranikāya, Ekādasakanipātapāḷi",
    "s0502m": "Khuddakanikāya, Dhammapadapāḷi",
    "s0503m": "Khuddakanikāya, Udānapāḷi",
    "s0504m": "Khuddakanikāya, Itivuttakapāḷi",
    "s0505m": "Khuddakanikāya, Suttanipātapāḷi",
}

# VRI numbers AN paragraphs from the same convention as the citations, except
# where it splits one discourse into two paragraphs. In the Tikanipāta it gives
# the Titthāyatana discourse paragraphs 61 and 62, so every later discourse is
# one paragraph on: Kesamutti is paragraph 66, cited as AN 3.65. Checked
# against the recorded titles of AN 3.65, 3.69, 3.88, and 3.136.
# {nipāta: [(first cited number affected, paragraphs to add), ...]}
AN_PARAGRAPH_OFFSETS: dict[int, list[tuple[int, int]]] = {
    3: [(62, 1)],
}
# Where VRI abridges several numbered discourses into one paragraph. In the
# Ekakanipāta the ten recollections are cited one by one as AN 1.296-305;
# VRI gives the first its own paragraph (296) and the other nine paragraph 297
# with peyyāla. {nipāta: [((first cited, last cited), VRI paragraph), ...]}
AN_PARAGRAPH_GROUPS: dict[int, list[tuple[tuple[int, int], int]]] = {
    1: [((297, 305), 297)],
}

CITE_RE = re.compile(r"^(MN|DN|SN|AN|Ud|Iti|Snp|Dhp)\s+(\d+)(?:\.(\d+))?$")
# One discourse heading: `10. Mahāsatipaṭṭhānasuttaṃ`, or a peyyāla range
# such as `3-10. Dutiyādisuttāni` or `171-180. ...`.
NUMBERED_HEAD = re.compile(r"^\s*(\d+)(?:\s*[-–]\s*(\d+))?\.\s*(.+?)\s*$")
TAG_RE = re.compile(
    r'<head rend="(book|title|chapter)">(.*?)</head>'
    r'|<p rend="subhead"[^>]*>(.*?)</p>'
    r'|<p rend="([a-z0-9]+)"(?: n="([^"]*)")?[^>]*>(.*?)</p>',
    re.S,
)
NOTE_RE = re.compile(r"<note>.*?</note>", re.S)
INNER_TAG_RE = re.compile(r"<[^>]+>")
PARANUM_RE = re.compile(r'<hi rend="paranum">[^<]*</hi>\s*(?:<hi rend="dot">[^<]*</hi>)?')


class SourceUnavailable(Exception):
    """The VRI book could not be read from the local clone or fetched."""


@dataclass(frozen=True)
class Block:
    kind: str          # "book", "title", "chapter", "subhead", or a paragraph rend
    text: str          # plain text
    para: str | None   # VRI paragraph number on a body paragraph, e.g. "65" or "3-10"


@dataclass(frozen=True)
class Located:
    citation: str
    book: str
    heading: str
    text: str

    @property
    def book_title(self) -> str:
        return BOOK_TITLES.get(self.book, self.book)


def plain(fragment: str) -> str:
    fragment = NOTE_RE.sub("", fragment)
    fragment = PARANUM_RE.sub("", fragment)
    fragment = INNER_TAG_RE.sub("", fragment)
    return re.sub(r"\s+", " ", html.unescape(fragment)).strip()


def vri_dir() -> Path | None:
    configured = os.environ.get("VRI_TIPITAKA_DIR")
    return Path(configured) if configured else None


def read_book(book: str, cache_dir: Path | None = None, local_dir: Path | None = None,
              timeout: int = 120, allow_fetch: bool = True) -> str:
    """The book's XML as text, from a local clone, the cache, or upstream.

    With `allow_fetch=False` nothing is downloaded: a book that is not already
    on disk raises SourceUnavailable, so an offline report can say "not
    available" instead of guessing.
    """

    filename = f"{book}.mul.xml"
    for directory in (local_dir or vri_dir(),):
        if directory is not None:
            for candidate in (directory / filename, directory / "romn" / filename):
                if candidate.is_file():
                    return candidate.read_bytes().decode("utf-16")
    cache = cache_dir or DEFAULT_CACHE_DIR
    cached = cache / filename
    if cached.is_file():
        return cached.read_bytes().decode("utf-16")
    if not allow_fetch:
        raise SourceUnavailable(f"{filename}: not in {cache} and fetching is off")
    try:
        with urllib.request.urlopen(f"{RAW_BASE}/{filename}", timeout=timeout) as response:
            data = response.read()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as error:
        raise SourceUnavailable(f"{filename}: {error}") from error
    cache.mkdir(parents=True, exist_ok=True)
    cached.write_bytes(data)
    return data.decode("utf-16")


def parse_blocks(xml: str) -> list[Block]:
    blocks: list[Block] = []
    for match in TAG_RE.finditer(xml):
        head_kind, head_text, subhead, rend, para, body = match.groups()
        if head_kind is not None:
            blocks.append(Block(head_kind, plain(head_text), None))
        elif subhead is not None:
            blocks.append(Block("subhead", plain(subhead), None))
        else:
            blocks.append(Block(rend, plain(body), para or None))
    return blocks


@lru_cache(maxsize=64)
def _book_blocks(book: str, cache_key: str, local_key: str, allow_fetch: bool) -> tuple[Block, ...]:
    cache_dir = Path(cache_key) if cache_key else None
    local_dir = Path(local_key) if local_key else None
    return tuple(parse_blocks(read_book(book, cache_dir, local_dir, allow_fetch=allow_fetch)))


_ALLOW_FETCH = True


def book_blocks(book: str, cache_dir: Path | None = None, local_dir: Path | None = None) -> tuple[Block, ...]:
    local = local_dir or vri_dir()
    return _book_blocks(book, str(cache_dir or ""), str(local or ""), _ALLOW_FETCH)


HEADING_KINDS = {"book", "title", "chapter", "subhead"}


def _span_text(blocks: tuple[Block, ...], start: int, stop: int) -> str:
    """The passage's own words: headings are the edition's, not the discourse's."""
    return " ".join(b.text for b in blocks[start:stop] if b.text and b.kind not in HEADING_KINDS)


def _discourse_spans(blocks: tuple[Block, ...], level: str,
                     stop_levels: tuple[str, ...]) -> list[tuple[int, int, int, int]]:
    """(first number, last number, start index, end index) for each numbered heading."""

    heads = [
        (i, NUMBERED_HEAD.match(b.text))
        for i, b in enumerate(blocks)
        if b.kind == level and NUMBERED_HEAD.match(b.text)
    ]
    spans: list[tuple[int, int, int, int]] = []
    for position, (index, match) in enumerate(heads):
        assert match is not None
        first = int(match.group(1))
        last = int(match.group(2) or first)
        end = len(blocks)
        for later in range(index + 1, len(blocks)):
            kind = blocks[later].kind
            if kind in stop_levels or (kind == level and NUMBERED_HEAD.match(blocks[later].text)):
                end = later
                break
        spans.append((first, last, index, end))
    return spans


def _nth(spans: list[tuple[int, int, int, int]], number: int) -> tuple[int, int] | None:
    """The span covering ordinal `number`, counting a range heading as its width."""

    count = 0
    for first, last, start, end in spans:
        width = last - first + 1
        if count < number <= count + width:
            return start, end
        count += width
    return None


def _locate_ordinal(collection: str, number: int, cache_dir: Path | None,
                    local_dir: Path | None) -> Located | None:
    level = "chapter" if collection == "DN" else "subhead"
    count = 0
    for book in BOOKS[collection]:
        blocks = book_blocks(book, cache_dir, local_dir)
        spans = [s for s in _discourse_spans(blocks, level, ("book",))
                 if collection == "DN" or "sutt" in blocks[s[2]].text.casefold()]
        total = sum(last - first + 1 for first, last, _, _ in spans)
        if count + total >= number:
            found = _nth(spans, number - count)
            if found is None:
                return None
            start, end = found
            return Located(f"{collection} {number}", book, blocks[start].text,
                           _span_text(blocks, start, end))
        count += total
    return None


def _samyutta_spans(collection_books: tuple[str, ...], cache_dir, local_dir):
    """Every saṃyutta as (book, blocks, start, end), in order."""

    out = []
    for book in collection_books:
        blocks = book_blocks(book, cache_dir, local_dir)
        starts = [i for i, b in enumerate(blocks)
                  if b.kind == "chapter" and "saṃyutt" in b.text.casefold()]
        for position, start in enumerate(starts):
            end = starts[position + 1] if position + 1 < len(starts) else len(blocks)
            out.append((book, blocks, start, end))
    return out


def _locate_sn(samyutta: int, number: int, cache_dir, local_dir) -> Located | None:
    spans = _samyutta_spans(BOOKS["SN"], cache_dir, local_dir)
    if not 1 <= samyutta <= len(spans):
        return None
    book, blocks, start, end = spans[samyutta - 1]
    inner = blocks[start:end]
    discourses = [
        s for s in _discourse_spans(inner, "subhead", ("chapter", "book"))
        if "sutt" in inner[s[2]].text.casefold() or "peyyāl" in inner[s[2]].text.casefold()
    ]
    found = _nth(discourses, number)
    if found is None:
        return None
    s, e = found
    return Located(f"SN {samyutta}.{number}", book, inner[s].text, _span_text(inner, s, e))


def _para_covers(para: str | None, number: int) -> bool:
    if not para:
        return False
    match = re.fullmatch(r"(\d+)(?:-(\d+))?", para)
    if not match:
        return False
    first = int(match.group(1))
    return first <= number <= int(match.group(2) or first)


def _locate_an(nipata: int, number: int, cache_dir, local_dir) -> Located | None:
    books = BOOKS["AN"]
    if not 1 <= nipata <= len(books):
        return None
    book = books[nipata - 1]
    blocks = book_blocks(book, cache_dir, local_dir)
    for (first, last), paragraph in AN_PARAGRAPH_GROUPS.get(nipata, []):
        if first <= number <= last:
            number = paragraph
            break
    else:
        number += sum(shift for first, shift in AN_PARAGRAPH_OFFSETS.get(nipata, []) if number >= first)
    hits = [i for i, b in enumerate(blocks) if _para_covers(b.para, number)]
    if not hits:
        return None
    first = hits[0]
    # Start at the discourse heading that introduces the paragraph, if one sits
    # directly above it, and run until the next numbered paragraph or heading.
    start = first
    if first > 0 and blocks[first - 1].kind == "subhead":
        start = first - 1
    end = len(blocks)
    for later in range(first + 1, len(blocks)):
        b = blocks[later]
        if b.kind in {"book", "title", "chapter", "subhead"} or (b.para and not _para_covers(b.para, number)):
            end = later
            break
    heading = blocks[start].text if blocks[start].kind == "subhead" else f"paragraph {blocks[first].para}"
    return Located(f"AN {nipata}.{number}", book, heading, _span_text(blocks, start, end))


def _locate_vagga(collection: str, vagga: int, number: int, cache_dir, local_dir) -> Located | None:
    book = BOOKS[collection][0]
    blocks = book_blocks(book, cache_dir, local_dir)
    chapters = [i for i, b in enumerate(blocks) if b.kind == "chapter"]
    if not 1 <= vagga <= len(chapters):
        return None
    start = chapters[vagga - 1]
    end = chapters[vagga] if vagga < len(chapters) else len(blocks)
    inner = blocks[start:end]
    found = _nth(_discourse_spans(inner, "subhead", ("chapter", "book")), number)
    if found is None:
        return None
    s, e = found
    return Located(f"{collection} {vagga}.{number}", book, inner[s].text, _span_text(inner, s, e))


def _locate_iti(number: int, cache_dir, local_dir) -> Located | None:
    book = BOOKS["Iti"][0]
    blocks = book_blocks(book, cache_dir, local_dir)
    found = _nth(_discourse_spans(blocks, "subhead", ("chapter", "book")), number)
    if found is None:
        return None
    s, e = found
    return Located(f"Iti {number}", book, blocks[s].text, _span_text(blocks, s, e))


def _locate_dhp(verse: int, cache_dir, local_dir) -> Located | None:
    """Each Dhp verse carries its number as the paragraph number of its first line."""

    book = BOOKS["Dhp"][0]
    blocks = book_blocks(book, cache_dir, local_dir)
    starts = [i for i, b in enumerate(blocks) if _para_covers(b.para, verse)]
    if not starts:
        return None
    start = starts[0]
    end = len(blocks)
    for later in range(start + 1, len(blocks)):
        b = blocks[later]
        if b.kind in {"book", "chapter"} or (b.para and not _para_covers(b.para, verse)):
            end = later
            break
    return Located(f"Dhp {verse}", book, f"verse {verse}", _span_text(blocks, start, end))


def locate(citation: str, cache_dir: Path | None = None, local_dir: Path | None = None,
           allow_fetch: bool = True) -> Located | None:
    """Find a citation in the VRI edition, or None if it cannot be placed.

    Raises SourceUnavailable when the book itself cannot be read, so a network
    failure is never mistaken for a missing discourse.
    """

    global _ALLOW_FETCH
    match = CITE_RE.match(citation.strip())
    if not match:
        return None
    _ALLOW_FETCH = allow_fetch
    try:
        return _locate(citation, match, cache_dir, local_dir)
    finally:
        _ALLOW_FETCH = True


def _locate(citation: str, match: re.Match[str], cache_dir: Path | None,
            local_dir: Path | None) -> Located | None:
    collection, major, minor = match.group(1), int(match.group(2)), match.group(3)
    minor_n = int(minor) if minor else None
    if collection in {"DN", "MN"} and minor_n is None:
        found = _locate_ordinal(collection, major, cache_dir, local_dir)
    elif collection == "SN" and minor_n is not None:
        found = _locate_sn(major, minor_n, cache_dir, local_dir)
    elif collection == "AN" and minor_n is not None:
        found = _locate_an(major, minor_n, cache_dir, local_dir)
    elif collection in {"Ud", "Snp"} and minor_n is not None:
        found = _locate_vagga(collection, major, minor_n, cache_dir, local_dir)
    elif collection == "Iti" and minor_n is None:
        found = _locate_iti(major, cache_dir, local_dir)
    elif collection == "Dhp" and minor_n is None:
        found = _locate_dhp(major, cache_dir, local_dir)
    else:
        found = None
    if found is None:
        return None
    return Located(citation.strip(), found.book, found.heading, found.text)


def supported(citation: str) -> bool:
    """Whether `locate` knows how to place a citation of this shape."""
    match = CITE_RE.match(citation.strip())
    if not match:
        return False
    collection, has_minor = match.group(1), match.group(3) is not None
    if collection in {"DN", "MN", "Iti", "Dhp"}:
        return not has_minor
    return has_minor
