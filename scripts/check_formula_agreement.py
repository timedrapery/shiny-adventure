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
BASELINE_PATH = REPO_ROOT / "reviews" / "formula-baseline.json"

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

    An exception is a pinned editorial decision, not a mute button. Each
    entry must name the phrase, a rationale, and `renderings`: the exact
    English each named record is approved to use. That scope is what makes
    the waiver mean something — a record the entry does not name, or a
    named record whose English later drifts from what was approved, is
    reported again rather than riding the old waiver. Two entries for the
    same phrase are rejected instead of one silently winning.
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
        renderings = entry.get("renderings")
        if not isinstance(pali, str) or not isinstance(rationale, str) or not rationale.strip():
            raise ValueError(f"formula exception needs `pali` and a non-empty `rationale`: {entry!r}")
        if (
            not isinstance(renderings, dict)
            or not renderings
            or not all(isinstance(k, str) and isinstance(v, str) and v.strip() for k, v in renderings.items())
        ):
            raise ValueError(
                "formula exception needs `renderings`: a non-empty map of record key to the "
                f"exact English that record is approved to use: {pali!r}"
            )
        key = normalize_pali(pali)
        if key in result:
            raise ValueError(f"duplicate formula exception for {pali!r}; merge the two entries")
        result[key] = entry
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
            approved = {k: canonical_rendering(v) for k, v in exception["renderings"].items()}
            # A record the exception does not name has no approved English,
            # and a named record whose English no longer matches what was
            # approved has drifted since the decision was made. Either way
            # the waiver does not cover what is actually on disk.
            uncovered = sorted(
                key
                for key, _pali, translation in quotes
                if key not in approved or canonical_rendering(translation) != approved[key]
            )
            if uncovered:
                finding["exception_gap"] = sorted(set(uncovered))
                unexplained.append(finding)
                continue
            finding["rationale"] = exception["rationale"]
            waived.append(finding)
        else:
            unexplained.append(finding)
    return unexplained, waived


def variant_key(finding: dict[str, object]) -> list[str]:
    """The exact set of (record, English) pairs a disagreement consists of."""
    return sorted(f"{key}\t{canonical_rendering(translation)}" for key, translation in finding["renderings"])


def load_baseline(path: Path = BASELINE_PATH) -> dict[str, list[str]]:
    """Known, not-yet-reconciled disagreements, keyed by normalized Pali.

    The baseline is the acknowledged backlog. It lets the check block a
    *new* disagreement, or a change to a known one, without first demanding
    that all of the backlog be resolved. Gating on the total count would let
    one fixed group pay for one freshly broken group; the variants are
    recorded so that trade is visible instead.
    """
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    groups = data.get("groups") if isinstance(data, dict) else None
    if not isinstance(groups, dict):
        return {}
    return {normalize_pali(pali): sorted(str(v) for v in variants) for pali, variants in groups.items()}


def compare_to_baseline(
    unexplained: list[dict[str, object]],
    baseline: dict[str, list[str]],
) -> tuple[list[dict[str, object]], list[str]]:
    """Return (regressions, stale) against the baseline.

    A regression is an unexplained disagreement the baseline does not list,
    or lists with a different set of variants. A stale entry is a baseline
    group no longer in disagreement: it has been resolved, and should be
    removed so the file keeps describing the real backlog.
    """
    current = {normalize_pali(str(f["pali"])): f for f in unexplained}
    regressions = [
        f for key, f in current.items()
        if key not in baseline or baseline[key] != variant_key(f)
    ]
    stale = sorted(key for key in baseline if key not in current)
    return regressions, stale


def write_baseline(unexplained: list[dict[str, object]], path: Path = BASELINE_PATH) -> None:
    payload = {
        "_comment": (
            "Acknowledged formula disagreements, written by "
            "`scripts/check_formula_agreement.py --update-baseline`. The check fails on any "
            "disagreement not listed here or whose variants have changed, and on entries that "
            "are no longer in disagreement. Resolve groups by editing the records, then rerun "
            "with --update-baseline to drop them; never add to this file by hand to silence a finding."
        ),
        "groups": {str(f["pali"]): variant_key(f) for f in unexplained},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


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
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on every unexplained disagreement, baseline or not.",
    )
    parser.add_argument(
        "--update-baseline",
        action="store_true",
        help="Rewrite reviews/formula-baseline.json to the current unexplained set.",
    )
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

    if args.update_baseline:
        write_baseline(unexplained)
        print(f"Wrote {len(unexplained)} acknowledged group(s) to {BASELINE_PATH.relative_to(REPO_ROOT).as_posix()}.")
        return 0

    regressions, stale = compare_to_baseline(unexplained, load_baseline())

    if args.json:
        json.dump(
            {"unexplained": unexplained, "waived": waived, "regressions": regressions, "stale_baseline": stale},
            sys.stdout,
            ensure_ascii=True,
            indent=2,
        )
        sys.stdout.write("\n")
    elif not unexplained:
        print(f"Formula agreement check passed ({len(waived)} waived by exception).")
    else:
        print_findings(unexplained, waived)

    # The backlog is advisory; a change to it is not. A new disagreement, a
    # changed one, or a resolved one still listed in the baseline all fail,
    # so the repairs already made stay made.
    if regressions:
        print(f"\nNew or changed disagreements not in the baseline ({len(regressions)}):")
        for finding in regressions:
            print(f"- {safe_text(finding['pali'])}")
        print("Reconcile the records, add a scoped exception, or acknowledge with --update-baseline.")
    if stale:
        print(f"\nBaseline entries no longer in disagreement ({len(stale)}); run --update-baseline to drop them:")
        for key in stale:
            print(f"- {safe_text(key)}")

    if regressions or stale:
        return 1
    if unexplained and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
