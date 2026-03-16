#!/usr/bin/env python3
"""Report doctrinal coverage gaps in the term dataset."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from scripts.text_utils import normalize_term, safe_text
    from scripts.term_store import iter_term_files
except ModuleNotFoundError:
    from text_utils import normalize_term, safe_text
    from term_store import iter_term_files


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"


@dataclass(frozen=True)
class CoverageFamily:
    name: str
    weight: int
    terms: tuple[str, ...]


COVERAGE_FAMILIES: tuple[CoverageFamily, ...] = (
    CoverageFamily(
        "Bases of Spiritual Power",
        10,
        ("iddhipada", "chanda", "viriya", "citta", "vimamsa"),
    ),
    CoverageFamily(
        "Three Characteristics",
        8,
        ("anicca", "dukkha", "anatta"),
    ),
    CoverageFamily(
        "Four Noble Truths",
        10,
        ("ariyasacca", "dukkha", "samudaya", "nirodha", "magga"),
    ),
    CoverageFamily(
        "Noble Eightfold Path",
        10,
        (
            "magga",
            "samma-ditthi",
            "samma-sankappa",
            "samma-vaca",
            "samma-kammanta",
            "samma-ajiva",
            "samma-vayama",
            "samma-sati",
            "samma-samadhi",
        ),
    ),
    CoverageFamily(
        "Four Foundations of Sati",
        9,
        ("satipatthana", "kaya", "vedana", "citta", "dhamma"),
    ),
    CoverageFamily(
        "Seven Awakening Factors",
        9,
        ("bojjhanga", "sati", "dhammavicaya", "viriya", "piti", "passaddhi", "samadhi", "upekkha"),
    ),
    CoverageFamily(
        "Five Hindrances",
        8,
        ("nivarana", "kamacchanda", "byapada", "thina-middha", "uddhacca-kukkucca", "vicikiccha"),
    ),
    CoverageFamily(
        "Five Faculties",
        8,
        ("indriya", "saddha", "viriya", "sati", "samadhi", "panna"),
    ),
    CoverageFamily(
        "Five Powers",
        8,
        ("bala", "saddha", "viriya", "sati", "samadhi", "panna"),
    ),
    CoverageFamily(
        "Wholesome and Unwholesome Roots",
        9,
        ("lobha", "dosa", "moha", "alobha", "adosa", "amoha"),
    ),
    CoverageFamily(
        "Liberation Sequence",
        9,
        ("nibbida", "viraga", "nirodha", "vimutti", "nibbana"),
    ),
    CoverageFamily(
        "Liberation Stages",
        9,
        ("sotapatti", "sotapanna", "sakadagami", "anagami", "arahant"),
    ),
    CoverageFamily(
        "Six Sense Faculties",
        9,
        ("cakkhu", "sota", "ghana", "jivha", "kaya", "mano"),
    ),
    CoverageFamily(
        "Six Sense Objects",
        9,
        ("rupa", "sadda", "gandha", "rasa", "photthabba", "dhamma"),
    ),
    CoverageFamily(
        "Six Consciousnesses",
        9,
        ("cakkhu-vinnana", "sota-vinnana", "ghana-vinnana", "jivha-vinnana", "kaya-vinnana", "mano-vinnana"),
    ),
    CoverageFamily(
        "Action and Ethical Result",
        8,
        ("kamma", "cetana", "phala", "punna", "papa", "kusala", "akusala"),
    ),
    CoverageFamily(
        "Outflows and Fettering",
        8,
        ("asava", "samyojana", "anusaya", "raga"),
    ),
    CoverageFamily(
        "Conditioned and Unconditioned",
        10,
        ("sankhata", "asankhata", "nibbana"),
    ),
    CoverageFamily(
        "Possessiveness and Comparison",
        7,
        ("mana", "issa", "macchariya"),
    ),
    CoverageFamily(
        "Support and Burden",
        7,
        ("upadhi", "upadana", "bhava"),
    ),
    CoverageFamily(
        "Two Release Modes",
        7,
        ("cetovimutti", "pannavimutti", "vimutti"),
    ),
    CoverageFamily(
        "Attention Pair",
        8,
        ("manasikara", "yoniso-manasikara", "ayoniso-manasikara"),
    ),
)


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_terms() -> dict[str, dict[str, object]]:
    terms: dict[str, dict[str, object]] = {}
    for path in iter_term_files(TERMS_DIR):
        data = load_json(path)
        if isinstance(data, dict):
            terms[normalize_term(path.stem)] = data
    return terms


def family_progress(terms: dict[str, dict[str, object]], family: CoverageFamily) -> tuple[list[str], list[str]]:
    present: list[str] = []
    missing: list[str] = []
    for term in family.terms:
        normalized = normalize_term(term)
        if normalized in terms:
            present.append(term)
        else:
            missing.append(term)
    return present, missing


def compute_candidate_scores(terms: dict[str, dict[str, object]]) -> list[tuple[str, int, list[str]]]:
    scores: dict[str, int] = {}
    reasons: dict[str, list[str]] = {}
    for family in COVERAGE_FAMILIES:
        _, missing = family_progress(terms, family)
        if not missing:
            continue
        for term in missing:
            normalized = normalize_term(term)
            scores[normalized] = scores.get(normalized, 0) + family.weight
            reasons.setdefault(normalized, []).append(family.name)
    ranked = sorted(
        ((term, score, sorted(reasons[term])) for term, score in scores.items()),
        key=lambda item: (-item[1], item[0]),
    )
    return ranked


def print_summary(terms: dict[str, dict[str, object]]) -> None:
    reviewed = sum(1 for data in terms.values() if data.get("status") in {"reviewed", "stable"})
    untranslated = sum(1 for data in terms.values() if data.get("untranslated_preferred") is True)
    print("Coverage Summary")
    print(f"- Term files: {len(terms)}")
    print(f"- Reviewed or stable entries: {reviewed}")
    print(f"- Entries with untranslated_preferred: {untranslated}")
    print()


def print_partial_families(terms: dict[str, dict[str, object]]) -> None:
    partials: list[tuple[float, CoverageFamily, list[str], list[str]]] = []
    for family in COVERAGE_FAMILIES:
        present, missing = family_progress(terms, family)
        if present and missing:
            ratio = len(present) / len(family.terms)
            partials.append((ratio, family, present, missing))
    partials.sort(key=lambda item: (-item[0], -item[1].weight, item[1].name))

    print("Partial Families")
    if not partials:
        print("- None")
        print()
        return

    for _, family, present, missing in partials:
        print(
            f"- {family.name}: {len(present)}/{len(family.terms)} present; missing {', '.join(safe_text(term) for term in missing)}"
        )
    print()


def print_missing_families(terms: dict[str, dict[str, object]]) -> None:
    missing_families = [family for family in COVERAGE_FAMILIES if not family_progress(terms, family)[0]]

    print("Missing Families")
    if not missing_families:
        print("- None")
        print()
        return

    for family in sorted(missing_families, key=lambda item: (-item.weight, item.name)):
        print(f"- {family.name}: {', '.join(safe_text(term) for term in family.terms)}")
    print()


def print_ranked_candidates(terms: dict[str, dict[str, object]], top: int) -> None:
    ranked = compute_candidate_scores(terms)
    print("Ranked Missing Candidates")
    if not ranked:
        print("- None")
        print()
        return

    for term, score, reasons in ranked[:top]:
        print(f"- {safe_text(term)}: score {score}; families {', '.join(safe_text(reason) for reason in reasons)}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--top",
        type=int,
        default=20,
        help="Number of ranked missing candidates to show.",
    )
    args = parser.parse_args()

    if not TERMS_DIR.exists():
        print(f"ERROR: Terms directory not found: {TERMS_DIR}")
        return 1

    terms = load_terms()
    if not terms:
        print("WARNING: No term files found in terms/")
        return 0

    print_summary(terms)
    print_partial_families(terms)
    print_missing_families(terms)
    print_ranked_candidates(terms, args.top)
    return 0


if __name__ == "__main__":
    sys.exit(main())
