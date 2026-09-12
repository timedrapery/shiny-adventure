#!/usr/bin/env python3
"""Check that a Pali phrase shared across term records is rendered the same way.

Term records carry `example_phrases`, and many phrases recur: a formula like
`vivekajaṃ pītisukhaṃ` is quoted by `piti`, `sukha`, and the compound record
that governs it. When those copies disagree, the lexicon contradicts itself
in exactly the place a translator looks for the house rendering.

This check groups every example phrase by its normalized Pali and reports
groups whose English differs. Differences are not always errors — a record
may legitimately quote a formula under a context rule that changes one word —
so a disagreement can be waived with a scoped, explained exception in
`reviews/formula-exceptions.json`. What is not allowed is an unexplained one.

The check is advisory until the existing disagreements are reconciled; pass
`--strict` to make it a gate.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

try:
    from scripts.term_store import iter_term_files
    from scripts.text_utils import safe_text
except ModuleNotFoundError:
    from term_store import iter_term_files
    from text_utils import safe_text


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
EXCEPTIONS_PATH = REPO_ROOT / "reviews" / "formula-exceptions.json"

# Records write the anusvāra both ways. Folding them is the difference
# between seeing one shared formula and two unrelated phrases.
ANUSVARA_VARIANTS = {"ṁ": "ṃ"}  # ṁ -> ṃ
STRIP = re.compile(r"[^\w\s]", re.UNICODE)


def normalize_pali(value: str) -> str:
    text = unicodedata.normalize("NFC", value).casefold()
    for variant, canonical in ANUSVARA_VARIANTS.items():
        text = text.replace(variant, canonical)
    return " ".join(STRIP.sub("", text).split())


def canonical_rendering(value: str) -> str:
    return " ".join(value.casefold().split())


def load_terms(terms_dir: Path = TERMS_DIR) -> dict[str, dict[str, object]]:
    terms: dict[str, dict[str, object]] = {}
    for path in iter_term_files(terms_dir):
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, dict):
            terms[str(data.get("normalized_term") or path.stem)] = data
    return terms


def load_exceptions(path: Path = EXCEPTIONS_PATH) -> dict[str, dict[str, object]]:
    """Waived disagreements, keyed by normalized Pali.

    Each entry names the phrase, the records allowed to differ, and why. An
    exception without a rationale is not an exception; it is a suppressed
    finding, and it is rejected here.
    """
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    entries = data.get("exceptions") if isinstance(data, dict) else None
    result: dict[str, dict[str, object]] = {}
    if not isinstance(entries, list):
        return result
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        pali = entry.get("pali")
        rationale = entry.get("rationale")
        if not isinstance(pali, str) or not isinstance(rationale, str) or not rationale.strip():
            raise ValueError(f"formula exception needs `pali` and a non-empty `rationale`: {entry!r}")
        result[normalize_pali(pali)] = entry
    return result


def collect_disagreements(
    terms: dict[str, dict[str, object]],
    exceptions: dict[str, dict[str, object]] | None = None,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Return (unexplained, waived) disagreements.

    Each finding carries the phrase, and every record/translation pair that
    quotes it, so the repair is visible without opening five files.
    """
    exceptions = exceptions or {}
    groups: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for key, data in terms.items():
        phrases = data.get("example_phrases")
        if not isinstance(phrases, list):
            continue
        for phrase in phrases:
            if not isinstance(phrase, dict):
                continue
            pali = phrase.get("pali")
            translation = phrase.get("translation")
            if not isinstance(pali, str) or not isinstance(translation, str):
                continue
            groups[normalize_pali(pali)].append((key, pali, translation.strip()))

    unexplained: list[dict[str, object]] = []
    waived: list[dict[str, object]] = []
    for normalized, quotes in sorted(groups.items()):
        renderings = {canonical_rendering(translation) for _key, _pali, translation in quotes}
        if len(renderings) < 2:
            continue
        finding = {
            "pali": quotes[0][1],
            "records": sorted({key for key, _pali, _translation in quotes}),
            "renderings": sorted(
                {(key, translation) for key, _pali, translation in quotes},
                key=lambda pair: (pair[0], pair[1]),
            ),
        }
        exception = exceptions.get(normalized)
        if exception is not None:
            allowed = exception.get("records")
            if isinstance(allowed, list) and set(finding["records"]) - set(allowed):
                # The exception names fewer records than actually disagree:
                # a new copy of the formula has drifted since it was written.
                finding["exception_gap"] = sorted(set(finding["records"]) - set(allowed))
                unexplained.append(finding)
                continue
            finding["rationale"] = exception["rationale"]
            waived.append(finding)
        else:
            unexplained.append(finding)
    return unexplained, waived


def print_findings(unexplained: list[dict[str, object]], waived: list[dict[str, object]]) -> None:
    if unexplained:
        print(f"Shared example phrases rendered differently ({len(unexplained)}):\n")
        for finding in unexplained:
            print(f"- {safe_text(finding['pali'])}")
            for key, translation in finding["renderings"]:
                print(f"    [{safe_text(key)}] {safe_text(translation)}")
            if "exception_gap" in finding:
                print(
                    "    exception in reviews/formula-exceptions.json does not cover: "
                    + ", ".join(safe_text(k) for k in finding["exception_gap"])
                )
            print()
        print(
            "Repair: make the copies agree, or add a scoped exception with a rationale to "
            "reviews/formula-exceptions.json."
        )
    if waived:
        print(f"Waived by explicit exception: {len(waived)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Fail on unexplained disagreements.")
    parser.add_argument("--json", action="store_true", help="Emit findings as JSON.")
    args = parser.parse_args()

    if not TERMS_DIR.exists():
        print(f"ERROR: Terms directory not found: {TERMS_DIR}")
        return 1

    try:
        exceptions = load_exceptions()
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1

    unexplained, waived = collect_disagreements(load_terms(), exceptions)

    if args.json:
        json.dump({"unexplained": unexplained, "waived": waived}, sys.stdout, ensure_ascii=True, indent=2)
        sys.stdout.write("\n")
    elif not unexplained:
        print(f"Formula agreement check passed ({len(waived)} waived by exception).")
    else:
        print_findings(unexplained, waived)

    if unexplained and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
