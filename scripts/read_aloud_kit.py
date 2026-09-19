#!/usr/bin/env python3
"""Generate the session kit for a read-aloud review.

The read-aloud gate in `docs/newcomer-review-protocol.md` is the cheapest of
the three human gates and the only one that needs nobody but a reviewer and a
voice. It has still never been run, and the reason is visible in the
materials: the newcomer sessions have a facilitator guide and a printable
sheet, and the read-aloud review has one sentence of protocol and a footnote.

This script produces what the reviewer actually needs at the table:

- the `body_sha256` of the text as it stands right now, computed rather than
  copied, so the evidence cannot end up bound to the wrong words
- the translation split into numbered sentences, so a stumble is recorded as
  "14" rather than as a description of a sentence that has to be found again
- a ledger-ready record with the hash and the sentence numbers already in it

`--facilitator` adds the measured watch points for the surface, taken from the
spoken register profile in `plain_english_audit.py`. That section is printed
separately and marked, because a reviewer who has been told where the awkward
sentences are is no longer a first hearing. Read first, compare afterwards.

Nothing here decides anything. The kit is stationery; the evidence is the
reviewer's.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

try:
    from scripts.check_readability_reviews import (
        normalized_translation_body,
        translation_body_sha256,
    )
    from scripts.plain_english_audit import (
        profile_text,
        split_paragraphs,
        split_sentences,
        strip_apparatus,
        write_output,
    )
    from scripts.surface_registry import TRANSLATION_SURFACES
except ModuleNotFoundError:  # pragma: no cover - exercised by direct invocation
    from check_readability_reviews import (  # type: ignore[no-redef]
        normalized_translation_body,
        translation_body_sha256,
    )
    from plain_english_audit import (  # type: ignore[no-redef]
        profile_text,
        split_paragraphs,
        split_sentences,
        strip_apparatus,
        write_output,
    )
    from surface_registry import TRANSLATION_SURFACES  # type: ignore[no-redef]


REPO_ROOT = Path(__file__).resolve().parent.parent

# The three-text pilot named in docs/newcomer-review-protocol.md. Ordered
# short-to-long: a reviewer doing their first session should meet the method on
# a text that takes a minute, not on the longest one in the cohort.
PILOT = ("an2_9", "sn36_6", "an3_65")

# Words per minute for unhurried reading aloud. Deliberately slower than silent
# reading; the estimate is there so a session can be scheduled, not to be
# precise.
WORDS_PER_MINUTE = 130


def surfaces_by_key() -> dict[str, object]:
    return {surface.key: surface for surface in TRANSLATION_SURFACES}


def numbered_sentences(text: str) -> list[dict[str, object]]:
    """Number every sentence of the translation body, keeping its source line.

    The numbering is what makes a stumble recordable. Sentence 14 stays
    sentence 14 for as long as the body does not change, and the moment it does
    the body hash changes with it, so a stale number can never quietly point at
    different words.
    """
    body = strip_apparatus(text)
    sentences: list[dict[str, object]] = []
    for line_number, paragraph in split_paragraphs(body):
        for sentence in split_sentences(paragraph):
            sentences.append(
                {
                    "number": len(sentences) + 1,
                    "line": line_number,
                    "words": len(sentence.split()),
                    "text": sentence,
                }
            )
    return sentences


def build_kit(surface: object, repo_root: Path = REPO_ROOT) -> dict[str, object]:
    path = repo_root / surface.main_relpath  # type: ignore[attr-defined]
    text = path.read_text(encoding="utf-8")
    body = normalized_translation_body(text)
    sentences = numbered_sentences(text)
    words = len(body.split())
    return {
        "key": surface.key,  # type: ignore[attr-defined]
        "label": surface.label,  # type: ignore[attr-defined]
        "path": surface.main_relpath,  # type: ignore[attr-defined]
        "body_sha256": translation_body_sha256(path),
        "words": words,
        "minutes": max(1, round(words / WORDS_PER_MINUTE)),
        "sentences": sentences,
        "profile": profile_text(text, surface.main_relpath),  # type: ignore[attr-defined]
    }


def render_watch_points(kit: dict[str, object]) -> list[str]:
    """Render the measured pressure points for this surface.

    Kept in its own section, and out of the kit unless asked for, because
    telling a reviewer where to expect trouble is the one thing that can spoil
    a first hearing.
    """
    profile = kit["profile"]
    dialogue = profile["dialogue"]
    vocatives = profile["vocatives"]

    lines = [
        "",
        "---",
        "",
        "## Facilitator notes — do not read before the session",
        "",
        "These are measured pressure points, not defects, and the reviewer's ear",
        "outranks them. Compare them with what actually caught, after the read.",
        "",
        f"- dialogue negation: {dialogue['contractions']} contracted,"
        f" {dialogue['contractible_negations']} not",
        f"- forms of address: {vocatives['initial']} opening,"
        f" {vocatives['medial']} mid-clause, {vocatives['final']} closing",
        f"- sentences over 45 words: {profile['over_breath_limit']}"
        f" (longest {profile['longest_unit']})",
    ]

    if profile["long_units"]:
        lines.extend(["", "Longest sentences:"])
        for unit in profile["long_units"]:
            lines.append(f"- line {unit['line']} ({unit['words']}w) {unit['opening']} ...")

    if profile["repeated_units"]:
        lines.extend(["", "Units this text repeats:"])
        for unit in profile["repeated_units"]:
            lines.append(f"- x{unit['occurrences']}: {unit['text']}")
        lines.append("")
        lines.append(
            "A repeated unit is heard every time. If it caught once, it caught"
        )
        lines.append("every time.")

    return lines


def render_kit(kit: dict[str, object], facilitator: bool = False) -> str:
    today = date.isoformat(date.today())
    sentences = kit["sentences"]
    lines = [
        f"# Read-aloud session kit: {kit['label']}",
        "",
        f"- Surface: `{kit['key']}`",
        f"- Text: `{kit['path']}`",
        f"- Body hash: `{kit['body_sha256']}`",
        f"- Length: {kit['words']} words, about {kit['minutes']} minute"
        f"{'' if kit['minutes'] == 1 else 's'} aloud",
        f"- Generated: {today}",
        "",
        "The body hash above is what binds this session to the words being read.",
        "If the translation is edited before the session happens, regenerate the",
        "kit; the hash will change and the old one no longer describes this text.",
        "",
        "## How to run it",
        "",
        "1. Read the whole translation aloud, at an unhurried speaking pace, to",
        "   the end. Not silently, and not in excerpts: the gate is about",
        "   delivery, and a passage skipped is a passage unreviewed.",
        "2. Do not stop to fix anything. Mark the sentence number and keep going.",
        "3. Mark a sentence when you have to restart it, run out of breath, take a",
        "   breath somewhere the punctuation did not offer, hear a word you would",
        "   not say out loud, or reach the end unsure of who was speaking.",
        "4. A second voice helps but is not required. If someone is listening,",
        "   mark separately what they did not follow on first hearing -- that is",
        "   the thing silent review cannot reach.",
        "",
        "## The reading",
        "",
    ]

    for sentence in sentences:
        lines.append(f"{sentence['number']:>4}.  {sentence['text']}")
        lines.append("")

    lines.extend(
        [
            "## What caught",
            "",
            "One row per sentence that caught. Leave it empty if nothing did;",
            "an empty table is a real result and a fabricated one is not.",
            "",
            "| Sentence | What happened | What it sounded like it needed |",
            "| ---: | --- | --- |",
            "|  |  |  |",
            "|  |  |  |",
            "|  |  |  |",
            "",
            "## Ledger record",
            "",
            "Replace the reviewer label and the observations, then put this in the",
            f"surface's `human_read_aloud` object in",
            "`reviews/newcomer-review-ledger.json`.",
            "",
            "Set `status` to `complete` only if the whole text was read aloud. If",
            "the session stopped early, leave it `pending` and record what was",
            "covered -- a partial read is worth keeping and is not the gate.",
            "",
            "```json",
        ]
    )

    record = {
        "status": "complete",
        "body_sha256": kit["body_sha256"],
        "reviewers": [
            {
                "label": "A1",
                "reviewed_on": today,
                "read_complete": True,
                "observations": [
                    {
                        "sentence": 0,
                        "line": 0,
                        "problem": "What caught, in the reviewer's words.",
                    }
                ],
            }
        ],
    }
    lines.extend(json.dumps(record, indent=2, ensure_ascii=False).splitlines())
    lines.extend(
        [
            "```",
            "",
            "Then run `python scripts/check_newcomer_reviews.py`. It checks that the",
            "record is complete and bound to the current body. It cannot check that",
            "the session happened, which is the part that rests on you.",
        ]
    )

    if facilitator:
        lines.extend(render_watch_points(kit))

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--surface",
        action="append",
        help="Surface key, e.g. sn36_6. Repeatable. Defaults to the three-text pilot.",
    )
    parser.add_argument(
        "--facilitator",
        action="store_true",
        help=(
            "Append the measured watch points for the surface. Withhold this "
            "from the reviewer until after the read."
        ),
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="Directory to write one kit per surface into. Prints to stdout otherwise.",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    registry = surfaces_by_key()
    keys = tuple(args.surface) if args.surface else PILOT

    unknown = [key for key in keys if key not in registry]
    if unknown:
        known = ", ".join(sorted(registry))
        print(f"Unknown surface key(s): {', '.join(unknown)}", file=sys.stderr)
        print(f"Known keys: {known}", file=sys.stderr)
        return 2

    kits = [build_kit(registry[key]) for key in keys]

    if args.format == "json":
        write_output(json.dumps(kits, indent=2, ensure_ascii=False) + "\n")
        return 0

    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        for kit in kits:
            target = args.out / f"read-aloud-{str(kit['key']).replace('_', '-')}.md"
            target.write_text(render_kit(kit, args.facilitator), encoding="utf-8")
            print(f"Wrote {target}")
        return 0

    write_output("\n\n".join(render_kit(kit, args.facilitator) for kit in kits) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
