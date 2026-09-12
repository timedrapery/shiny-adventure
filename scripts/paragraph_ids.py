#!/usr/bin/env python3
"""Maintain stable passage identifiers for governed translation surfaces.

Reader feedback needs to name the passage a reader was looking at in a way
that still means something after the translation is revised. A position
("the seventh paragraph") breaks the moment a paragraph is added above it,
and a content hash changes the moment the paragraph itself is edited, which is
exactly when we most want to connect old feedback to the revised wording.

So each surface with feedback enabled carries an authoritative map in
`includes/feedback/paragraph-ids/<surface>.json`: an ordered list of passage
ids (`p001`, `p002`, ...) with a fingerprint of each passage's current text.
Ids are allocated once per surface and never reused.

A passage is a blank-line-separated block inside the `## Translation` section
that is not a heading. Headings are not passages, but the section heading a
passage sits under is recorded to help a maintainer find it.

Alignment rules applied by `--write` after the translation changes:

- an unchanged passage keeps its id, wherever it moved;
- an edited passage between the same neighbours keeps its id; the previous
  fingerprint is kept in its history so feedback recorded against the earlier
  wording stays identifiable;
- a split keeps the id on the first part and allocates new ids for the rest,
  recording `split_from`; a merge keeps the first id and retires the others
  with `merged_into`;
- a new passage gets a new id; a removed passage is retired with the body
  hash that removed it.

Usage:

    python scripts/paragraph_ids.py --check
    python scripts/paragraph_ids.py --write [--surface KEY ...]
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from scripts.check_readability_reviews import translation_body_sha256
    from scripts.surface_registry import REPO_ROOT, TRANSLATION_SURFACES
except ModuleNotFoundError:  # invoked as a script from the repo root
    from check_readability_reviews import translation_body_sha256  # type: ignore[no-redef]
    from surface_registry import REPO_ROOT, TRANSLATION_SURFACES  # type: ignore[no-redef]


MAP_DIR = REPO_ROOT / "includes" / "feedback" / "paragraph-ids"
CONFIG_PATH = REPO_ROOT / "includes" / "feedback" / "config.json"
BODY_MARKER = "## Translation"
ID_RE = re.compile(r"^p\d{3,}$")
FINGERPRINT_LENGTH = 16
PREVIEW_LENGTH = 72


@dataclass(frozen=True)
class Passage:
    index: int
    section: str
    markdown: str
    normalized: str
    fingerprint: str

    @property
    def preview(self) -> str:
        if len(self.normalized) <= PREVIEW_LENGTH:
            return self.normalized
        return self.normalized[: PREVIEW_LENGTH - 1].rstrip() + "…"


# --------------------------------------------------------------------------
# passages
# --------------------------------------------------------------------------

def normalize_passage(markdown: str) -> str:
    """The reader-visible wording of a passage, whitespace- and markup-folded.

    This must track what a browser shows as `textContent`, because the reader
    script matches page paragraphs against these fingerprints before it
    attaches a feedback control.
    """
    text = re.sub(r"<!--.*?-->", " ", markdown, flags=re.S)
    text = re.sub(r"!?\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"(\*\*|__)(.+?)\1", r"\2", text, flags=re.S)
    text = re.sub(r"(?<!\w)([*_])(?!\s)(.+?)(?<!\s)\1(?!\w)", r"\2", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", text, flags=re.M)
    text = re.sub(r"^\s*>\s?", "", text, flags=re.M)
    return " ".join(text.split())


def fingerprint(normalized: str) -> str:
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:FINGERPRINT_LENGTH]


def translation_body(text: str) -> str:
    if BODY_MARKER not in text:
        raise ValueError(f"surface has no `{BODY_MARKER}` section")
    return text.split(BODY_MARKER, 1)[1].strip()


def passages_from_body(body: str) -> list[Passage]:
    """Split a governed translation body into its passages, in order."""
    found: list[Passage] = []
    section = ""
    for block in re.split(r"\n[ \t]*\n", body.replace("\r\n", "\n")):
        block = block.strip("\n")
        if not block.strip():
            continue
        heading = re.match(r"^#{1,6}\s+(.+?)\s*$", block.strip())
        if heading and "\n" not in block.strip():
            section = heading.group(1)
            continue
        normalized = normalize_passage(block)
        if not normalized:
            continue
        found.append(
            Passage(
                index=len(found),
                section=section,
                markdown=block,
                normalized=normalized,
                fingerprint=fingerprint(normalized),
            )
        )
    return found


def passages_for_surface(surface) -> list[Passage]:
    return passages_from_body(
        translation_body(surface.main_path.read_text(encoding="utf-8"))
    )


# --------------------------------------------------------------------------
# maps
# --------------------------------------------------------------------------

def map_path(key: str, map_dir: Path = MAP_DIR) -> Path:
    return map_dir / f"{key}.json"


def load_map(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: map must be a JSON object")
    return data


def empty_map(key: str) -> dict:
    return {
        "surface_key": key,
        "body_sha256": "",
        "next_id": 1,
        "passages": [],
        "retired": [],
    }


def _allocate(state: dict) -> str:
    number = int(state["next_id"])
    state["next_id"] = number + 1
    return f"p{number:03d}"


def _entry(passage: Passage, ident: str, history: list[str] | None = None) -> dict:
    return {
        "id": ident,
        "fingerprint": passage.fingerprint,
        "section": passage.section,
        "preview": passage.preview,
        "previous_fingerprints": list(history or []),
    }


def align(previous: dict, passages: list[Passage], body_sha256: str) -> dict:
    """Produce the next map for `passages`, keeping ids stable where possible."""
    state = {
        "surface_key": previous["surface_key"],
        "body_sha256": body_sha256,
        "next_id": int(previous.get("next_id", 1)),
        "passages": [],
        "retired": [dict(item) for item in previous.get("retired", [])],
    }
    old = list(previous.get("passages", []))
    old_prints = [str(item["fingerprint"]) for item in old]
    new_prints = [passage.fingerprint for passage in passages]

    # Anchor on unchanged passages first. Ordered matching (rather than a
    # dictionary lookup) is what keeps two identical paragraphs -- SN 36.6
    # repeats several lines verbatim -- attached to their own ids.
    matcher = difflib.SequenceMatcher(a=old_prints, b=new_prints, autojunk=False)
    anchors: list[tuple[int, int]] = []
    for block in matcher.get_matching_blocks():
        for offset in range(block.size):
            anchors.append((block.a + offset, block.b + offset))

    # An edited passage whose earlier wording is on record is also anchored:
    # the reader saw a version we can name. Only monotonic matches are kept,
    # so the gaps between anchors stay well-defined.
    claimed_old = {i for i, _ in anchors}
    claimed_new = {j for _, j in anchors}
    for j, passage in enumerate(passages):
        if j in claimed_new:
            continue
        for i, entry in enumerate(old):
            if i in claimed_old:
                continue
            if passage.fingerprint in entry.get("previous_fingerprints", []):
                candidate = sorted(anchors + [(i, j)], key=lambda pair: pair[1])
                if all(x[0] < y[0] for x, y in zip(candidate, candidate[1:])):
                    anchors = candidate
                    claimed_old.add(i)
                    claimed_new.add(j)
                break

    result: list[dict | None] = [None] * len(passages)
    for i, j in anchors:
        entry = old[i]
        result[j] = _entry(passages[j], str(entry["id"]), entry.get("previous_fingerprints"))

    # Now walk the gaps between anchors and decide edit / split / merge /
    # add / remove for each unmatched run.
    bounds = [(-1, -1)] + anchors + [(len(old), len(passages))]
    gaps = [
        (prev_i + 1, next_i, prev_j + 1, next_j)
        for (prev_i, prev_j), (next_i, next_j) in zip(bounds, bounds[1:])
        if next_i > prev_i + 1 or next_j > prev_j + 1
    ]

    for a, b, c, d in gaps:
        old_run = old[a:b]
        new_run = list(range(c, d))
        if old_run and new_run:
            paired = min(len(old_run), len(new_run))
            for offset in range(paired):
                entry = old_run[offset]
                history = list(entry.get("previous_fingerprints", []))
                if entry["fingerprint"] not in history:
                    history.append(str(entry["fingerprint"]))
                result[new_run[offset]] = _entry(
                    passages[new_run[offset]], str(entry["id"]), history
                )
            if len(new_run) > paired:
                # More new blocks than old: the surplus is a split when one
                # passage became several, otherwise plain additions.
                split_from = str(old_run[0]["id"]) if len(old_run) == 1 else None
                for j in new_run[paired:]:
                    entry = _entry(passages[j], _allocate(state))
                    if split_from is not None:
                        entry["split_from"] = split_from
                    result[j] = entry
            elif len(old_run) > paired:
                # More old blocks than new: a merge when several became one,
                # otherwise removals.
                merged_into = str(old_run[0]["id"]) if len(new_run) == 1 else None
                for entry in old_run[paired:]:
                    retired = {
                        "id": str(entry["id"]),
                        "fingerprint": str(entry["fingerprint"]),
                        "retired_in": body_sha256,
                        "reason": "merged" if merged_into else "removed",
                    }
                    if merged_into:
                        retired["merged_into"] = merged_into
                    state["retired"].append(retired)
        elif new_run:
            for j in new_run:
                result[j] = _entry(passages[j], _allocate(state))
        else:
            for entry in old_run:
                state["retired"].append({
                    "id": str(entry["id"]),
                    "fingerprint": str(entry["fingerprint"]),
                    "retired_in": body_sha256,
                    "reason": "removed",
                })

    state["passages"] = [entry for entry in result if entry is not None]
    if len(state["passages"]) != len(passages):
        raise RuntimeError("alignment left a passage without an id")
    return state


def build_map(surface, previous: dict | None = None) -> dict:
    previous = previous if previous is not None else empty_map(surface.key)
    passages = passages_for_surface(surface)
    return align(previous, passages, translation_body_sha256(surface.main_path))


# --------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------

def map_problems(surface, data: dict) -> list[str]:
    """Structural and freshness problems with a surface's map."""
    problems: list[str] = []
    label = f"{surface.key} paragraph map"
    if data.get("surface_key") != surface.key:
        problems.append(f"{label}: surface_key must be {surface.key!r}")
    entries = data.get("passages")
    if not isinstance(entries, list):
        return problems + [f"{label}: passages must be a list"]
    seen: set[str] = set()
    numbers: list[int] = []
    for entry in entries + list(data.get("retired", [])):
        ident = entry.get("id") if isinstance(entry, dict) else None
        if not isinstance(ident, str) or not ID_RE.match(ident):
            problems.append(f"{label}: invalid passage id {ident!r}")
            continue
        if ident in seen:
            problems.append(f"{label}: duplicate passage id {ident}")
        seen.add(ident)
        numbers.append(int(ident[1:]))
    next_id = data.get("next_id")
    if not isinstance(next_id, int) or (numbers and next_id <= max(numbers)):
        problems.append(f"{label}: next_id must exceed every allocated id")
    passages = passages_for_surface(surface)
    current = [passage.fingerprint for passage in passages]
    recorded = [str(entry.get("fingerprint")) for entry in entries if isinstance(entry, dict)]
    if current != recorded:
        problems.append(
            f"{label}: stale; the translation has {len(current)} passages and the map "
            f"records {len(recorded)} with different wording. Run "
            "`python scripts/paragraph_ids.py --write`."
        )
    body_hash = translation_body_sha256(surface.main_path)
    if data.get("body_sha256") != body_hash:
        problems.append(f"{label}: body_sha256 is not the current translation body")
    return problems


def enabled_surface_keys(config_path: Path = CONFIG_PATH) -> list[str]:
    if not config_path.is_file():
        return []
    data = json.loads(config_path.read_text(encoding="utf-8"))
    keys = data.get("enabled_surfaces", []) if isinstance(data, dict) else []
    return [key for key in keys if isinstance(key, str)]


def surfaces_with_maps(map_dir: Path = MAP_DIR) -> list[str]:
    if not map_dir.is_dir():
        return []
    return sorted(path.stem for path in map_dir.glob("*.json"))


def check(map_dir: Path = MAP_DIR, config_path: Path = CONFIG_PATH) -> list[str]:
    by_key = {surface.key: surface for surface in TRANSLATION_SURFACES}
    problems: list[str] = []
    wanted = set(surfaces_with_maps(map_dir)) | set(enabled_surface_keys(config_path))
    for key in sorted(wanted):
        surface = by_key.get(key)
        if surface is None:
            problems.append(f"{key}: paragraph map names an unregistered surface")
            continue
        path = map_path(key, map_dir)
        if not path.is_file():
            problems.append(
                f"{key}: feedback is enabled but includes/feedback/paragraph-ids/{key}.json "
                "is missing. Run `python scripts/paragraph_ids.py --write --surface "
                f"{key}`."
            )
            continue
        try:
            data = load_map(path)
        except (json.JSONDecodeError, ValueError) as error:
            problems.append(f"{key}: cannot load paragraph map: {error}")
            continue
        problems.extend(map_problems(surface, data))
    return problems


def write(keys: list[str] | None = None, map_dir: Path = MAP_DIR,
          config_path: Path = CONFIG_PATH) -> list[str]:
    by_key = {surface.key: surface for surface in TRANSLATION_SURFACES}
    wanted = keys or sorted(set(surfaces_with_maps(map_dir)) | set(enabled_surface_keys(config_path)))
    written: list[str] = []
    map_dir.mkdir(parents=True, exist_ok=True)
    for key in wanted:
        surface = by_key.get(key)
        if surface is None:
            raise SystemExit(f"{key}: not a registered translation surface")
        path = map_path(key, map_dir)
        previous = load_map(path) if path.is_file() else None
        data = build_map(surface, previous)
        text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        if path.is_file() and path.read_text(encoding="utf-8") == text:
            continue
        path.write_text(text, encoding="utf-8", newline="\n")
        try:
            written.append(path.relative_to(REPO_ROOT).as_posix())
        except ValueError:
            written.append(path.as_posix())
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="Fail if any map is stale.")
    parser.add_argument("--write", action="store_true", help="Create or realign maps.")
    parser.add_argument("--surface", action="append", default=[],
                        help="Limit --write to this surface key (repeatable).")
    args = parser.parse_args()

    if args.write:
        written = write(args.surface or None)
        for path in written:
            print(f"wrote {path}")
        if not written:
            print("Paragraph maps already current.")
        return 0

    problems = check()
    if problems:
        print("Paragraph identifier check failed:\n")
        for problem in problems:
            print(f"- {problem}")
        return 1
    count = len(surfaces_with_maps())
    print(f"Paragraph identifier check passed ({count} mapped surface(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
