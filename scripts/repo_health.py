#!/usr/bin/env python3
"""Report repository health signals for editorial scalability and automation."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    from scripts.text_utils import normalize_term
    from scripts.text_utils import safe_text
    from scripts.term_store import iter_term_files
except ModuleNotFoundError:
    from text_utils import normalize_term
    from text_utils import safe_text
    from term_store import iter_term_files


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
RULE_LANGUAGE_MARKERS = (
    "default",
    "context",
    "render",
    "translation",
    "untranslated",
    "compound",
    "drift",
    "avoid",
    "prefer",
)
HIGH_LOAD_MINOR_PRIORITY_TAGS = {
    "core-doctrine",
    "dependent-origination",
    "four-noble-truths",
    "aggregates",
    "translation-sensitive",
    "liberation",
    "self-view",
    "formula",
    "path-family",
}
HIGH_LOAD_MINOR_SCORE_THRESHOLD = 7


def stem_key(value: str) -> str:
    return value.replace("-", "_").casefold()


def related_term_keys(data: dict[str, object]) -> set[str]:
    related = data.get("related_terms")
    if not isinstance(related, list):
        return set()
    return {normalize_term(item) for item in related if isinstance(item, str)}


def has_explicit_preferred_disambiguation(
    grouped: list[tuple[str, dict[str, object]]],
) -> bool:
    if len(grouped) < 2:
        return False

    keys = {stem_key(stem): related_term_keys(data) for stem, data in grouped}
    stems = set(keys)
    return all(any(other in keys[stem] for other in stems - {stem}) for stem in stems)


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_terms(terms_dir: Path = TERMS_DIR) -> dict[str, dict[str, object]]:
    terms: dict[str, dict[str, object]] = {}
    for path in iter_term_files(terms_dir):
        data = load_json(path)
        if isinstance(data, dict):
            terms[path.stem] = data
    return terms


def is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def has_rule_language(text: str) -> bool:
    lowered = text.casefold()
    return any(marker in lowered for marker in RULE_LANGUAGE_MARKERS)


def minor_policy_score(data: dict[str, object]) -> int:
    tags = data.get("tags", [])
    tag_set = {tag for tag in tags if isinstance(tag, str)} if isinstance(tags, list) else set()
    references = data.get("sutta_references", [])
    reference_count = len(references) if isinstance(references, list) else 0

    score = 2 * len(tag_set & HIGH_LOAD_MINOR_PRIORITY_TAGS)
    score += min(reference_count, 4)
    if data.get("part_of_speech") in {"phrase", "expression"}:
        score += 1
    preferred = data.get("preferred_translation")
    term = data.get("term")
    if isinstance(preferred, str) and preferred == term:
        score += 1
    return score


def missing_minor_policy_fields(data: dict[str, object]) -> list[str]:
    missing: list[str] = []

    notes = data.get("notes")
    if not is_non_empty_string(notes):
        missing.append("notes")

    examples = data.get("example_phrases")
    if not isinstance(examples, list) or len(examples) == 0:
        missing.append("example_phrases")

    translation_policy = data.get("translation_policy")
    if not isinstance(translation_policy, dict) or len(translation_policy) == 0:
        missing.append("translation_policy")

    return missing


def compute_summary(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    entry_types = Counter(str(data.get("entry_type", "<missing>")) for data in terms.values())
    statuses = Counter(str(data.get("status", "<missing>")) for data in terms.values())
    major_terms = {stem: data for stem, data in terms.items() if data.get("entry_type") == "major"}

    return {
        "term_files": len(terms),
        "major_terms": len(major_terms),
        "minor_terms": entry_types.get("minor", 0),
        "stable_terms": statuses.get("stable", 0),
        "reviewed_terms": statuses.get("reviewed", 0),
        "draft_terms": statuses.get("draft", 0),
        "untranslated_preferred_terms": sum(
            1 for data in terms.values() if data.get("untranslated_preferred") is True
        ),
    }


def collect_major_missing_advanced_fields(
    terms: dict[str, dict[str, object]],
) -> dict[str, list[str]]:
    missing = {
        "authority_basis": [],
        "translation_policy": [],
    }
    for stem, data in sorted(terms.items()):
        if data.get("entry_type") != "major":
            continue
        if not data.get("authority_basis"):
            missing["authority_basis"].append(stem)
        if not data.get("translation_policy"):
            missing["translation_policy"].append(stem)
    return missing


def collect_generic_authority_basis_terms(
    terms: dict[str, dict[str, object]]
) -> list[dict[str, object]]:
    generic_terms: list[dict[str, object]] = []
    for stem, data in sorted(terms.items()):
        authority_basis = data.get("authority_basis")
        if not isinstance(authority_basis, list):
            continue
        for item in authority_basis:
            if isinstance(item, dict) and item.get("source") == "Repository editorial record":
                tags = data.get("tags", [])
                generic_terms.append(
                    {
                        "term": stem,
                        "status": str(data.get("status", "")),
                        "tags": [tag for tag in tags if isinstance(tag, str)] if isinstance(tags, list) else [],
                    }
                )
                break
    return generic_terms


def collect_example_source_gaps(terms: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    gaps: list[dict[str, object]] = []
    for stem, data in sorted(terms.items()):
        if data.get("entry_type") != "major":
            continue
        examples = data.get("example_phrases", [])
        if not isinstance(examples, list) or not examples:
            continue
        missing = [
            index + 1
            for index, example in enumerate(examples)
            if isinstance(example, dict) and not example.get("source")
        ]
        if missing:
            gaps.append(
                {
                    "term": stem,
                    "missing_example_indexes": missing,
                    "total_examples": len(examples),
                }
            )
    return gaps


def collect_example_source_gap_tags(
    terms: dict[str, dict[str, object]],
    gaps: list[dict[str, object]],
) -> list[dict[str, object]]:
    counts: defaultdict[str, int] = defaultdict(int)
    for gap in gaps:
        data = terms.get(gap["term"], {})
        tags = data.get("tags", [])
        if isinstance(tags, list):
            for tag in tags:
                if isinstance(tag, str):
                    counts[tag] += 1
    ranked = [
        {"tag": tag, "terms_with_source_gaps": count}
        for tag, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]
    return ranked


def collect_preferred_translation_collisions(
    terms: dict[str, dict[str, object]]
) -> list[dict[str, object]]:
    collisions: defaultdict[str, list[tuple[str, dict[str, object]]]] = defaultdict(list)
    for stem, data in sorted(terms.items()):
        if data.get("entry_type") != "major":
            continue
        preferred = data.get("preferred_translation")
        if isinstance(preferred, str) and preferred.strip():
            collisions[preferred].append((stem, data))

    results = []
    for preferred, grouped in sorted(collisions.items()):
        if len(grouped) > 1 and not has_explicit_preferred_disambiguation(grouped):
            results.append(
                {
                    "preferred_translation": preferred,
                    "terms": sorted(stem for stem, _data in grouped),
                }
            )
    results.sort(key=lambda item: (-len(item["terms"]), item["preferred_translation"]))
    return results


def collect_weak_major_rule_entries(
    terms: dict[str, dict[str, object]]
) -> list[dict[str, object]]:
    weak_entries: list[dict[str, object]] = []
    for stem, data in sorted(terms.items()):
        if data.get("entry_type") != "major" or data.get("status") not in {"reviewed", "stable"}:
            continue

        reasons: list[str] = []
        notes = data.get("notes")
        context_rules = data.get("context_rules")
        authority_basis = data.get("authority_basis")
        translation_policy = data.get("translation_policy")
        preferred = data.get("preferred_translation")

        if not is_non_empty_string(notes) or len(notes.strip()) < 120 or not has_rule_language(notes):
            reasons.append("thin_notes")
        if not isinstance(context_rules, list) or len(context_rules) < 2:
            reasons.append("thin_context_rules")
        if not isinstance(authority_basis, list) or len(authority_basis) == 0:
            reasons.append("missing_authority_basis")
        if not isinstance(translation_policy, dict):
            reasons.append("missing_translation_policy")
        else:
            if not is_non_empty_string(translation_policy.get("default_scope")):
                reasons.append("missing_default_scope")
            if not is_non_empty_string(translation_policy.get("when_not_to_apply")):
                reasons.append("missing_when_not_to_apply")
            if translation_policy.get("compound_inheritance") not in {"inherit", "case-by-case", "blocked"}:
                reasons.append("missing_compound_inheritance")
            if not is_non_empty_string(translation_policy.get("drift_risk")):
                reasons.append("missing_drift_risk")

        if isinstance(context_rules, list):
            renderings = {
                stem_key(rendering)
                for rendering in (
                    rule.get("rendering")
                    for rule in context_rules
                    if isinstance(rule, dict)
                )
                if isinstance(rendering, str)
            }
            if len(renderings) < 2 and isinstance(data.get("tags"), list) and "context-sensitive" in data["tags"]:
                reasons.append("indistinct_context_renderings")
            if is_non_empty_string(preferred) and stem_key(preferred) not in renderings:
                reasons.append("preferred_not_in_context_rules")

        if reasons:
            weak_entries.append(
                {
                    "term": stem,
                    "status": str(data.get("status", "")),
                    "reasons": reasons,
                }
            )
    return weak_entries


def collect_high_load_minor_entries(
    terms: dict[str, dict[str, object]]
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []

    for stem, data in sorted(terms.items()):
        if data.get("entry_type") != "minor" or data.get("status") not in {"reviewed", "stable"}:
            continue

        score = minor_policy_score(data)
        if score < HIGH_LOAD_MINOR_SCORE_THRESHOLD:
            continue

        missing_fields = missing_minor_policy_fields(data)
        if not missing_fields:
            continue

        tags = data.get("tags", [])
        references = data.get("sutta_references", [])
        results.append(
            {
                "term": stem,
                "status": str(data.get("status", "")),
                "score": score,
                "missing_fields": missing_fields,
                "sutta_reference_count": len(references) if isinstance(references, list) else 0,
                "tags": [tag for tag in tags if isinstance(tag, str)] if isinstance(tags, list) else [],
            }
        )

    results.sort(
        key=lambda item: (
            -item["score"],
            -item["sutta_reference_count"],
            item["term"],
        )
    )
    return results


def build_report(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    summary = compute_summary(terms)
    missing_advanced = collect_major_missing_advanced_fields(terms)
    generic_authority_terms = collect_generic_authority_basis_terms(terms)
    example_source_gaps = collect_example_source_gaps(terms)
    example_source_gap_tags = collect_example_source_gap_tags(terms, example_source_gaps)
    translation_collisions = collect_preferred_translation_collisions(terms)
    weak_major_rule_entries = collect_weak_major_rule_entries(terms)
    high_load_minor_entries = collect_high_load_minor_entries(terms)

    return {
        "summary": summary,
        "major_policy_coverage": {
            "authority_basis_missing": missing_advanced["authority_basis"],
            "translation_policy_missing": missing_advanced["translation_policy"],
            "generic_authority_basis": generic_authority_terms,
        },
        "rule_strength": {
            "weak_major_entries": weak_major_rule_entries,
        },
        "minor_governance": {
            "high_load_minors": high_load_minor_entries,
        },
        "example_source_gaps": example_source_gaps,
        "example_source_gap_tags": example_source_gap_tags,
        "preferred_translation_collisions": translation_collisions,
    }


def print_text_report(report: dict[str, object], *, top: int) -> None:
    summary = report["summary"]
    policy = report["major_policy_coverage"]
    rule_strength = report["rule_strength"]
    minor_governance = report["minor_governance"]
    example_source_gaps = report["example_source_gaps"]
    example_source_gap_tags = report["example_source_gap_tags"]
    collisions = report["preferred_translation_collisions"]

    print("Repository Health")
    print(f"- Term files: {summary['term_files']}")
    print(f"- Major terms: {summary['major_terms']}")
    print(f"- Minor terms: {summary['minor_terms']}")
    print(f"- Stable terms: {summary['stable_terms']}")
    print(f"- Reviewed terms: {summary['reviewed_terms']}")
    print(f"- Draft terms: {summary['draft_terms']}")
    print(f"- Terms preferring Pali untranslated: {summary['untranslated_preferred_terms']}")
    print()

    print("Major Policy Coverage")
    print(f"- Missing authority_basis: {len(policy['authority_basis_missing'])}")
    print(f"- Missing translation_policy: {len(policy['translation_policy_missing'])}")
    print(f"- Generic authority_basis needing refinement: {len(policy['generic_authority_basis'])}")
    print()

    print("Authority Basis Refinement Queue")
    if not policy["generic_authority_basis"]:
        print("- None")
    else:
        for item in policy["generic_authority_basis"][:top]:
            tags = ", ".join(item["tags"]) if item["tags"] else "-"
            print(
                f"- {safe_text(item['term'])}: status {item['status']}; tags {safe_text(tags)}"
            )
        if len(policy["generic_authority_basis"]) > top:
            remaining = len(policy["generic_authority_basis"]) - top
            print(f"- ... {remaining} more term(s)")
    print()

    print("Weak Major Rule Entries")
    if not rule_strength["weak_major_entries"]:
        print("- None")
    else:
        for item in rule_strength["weak_major_entries"][:top]:
            reasons = ", ".join(item["reasons"])
            print(
                f"- {safe_text(item['term'])}: status {item['status']}; reasons {safe_text(reasons)}"
            )
        if len(rule_strength["weak_major_entries"]) > top:
            remaining = len(rule_strength["weak_major_entries"]) - top
            print(f"- ... {remaining} more term(s)")
    print()

    print("High-Load Minor Queue")
    if not minor_governance["high_load_minors"]:
        print("- None")
    else:
        for item in minor_governance["high_load_minors"][:top]:
            missing = ", ".join(item["missing_fields"])
            tags = ", ".join(item["tags"]) if item["tags"] else "-"
            print(
                f"- {safe_text(item['term'])}: status {item['status']}; "
                f"score {item['score']}; missing {safe_text(missing)}; tags {safe_text(tags)}"
            )
        if len(minor_governance["high_load_minors"]) > top:
            remaining = len(minor_governance["high_load_minors"]) - top
            print(f"- ... {remaining} more term(s)")
    print()

    print("Example Source Gaps")
    if not example_source_gaps:
        print("- None")
    else:
        for gap in example_source_gaps[:top]:
            indexes = ", ".join(str(index) for index in gap["missing_example_indexes"])
            print(
                f"- {safe_text(gap['term'])}: missing source on example(s) {indexes} of {gap['total_examples']}"
            )
        if len(example_source_gaps) > top:
            remaining = len(example_source_gaps) - top
            print(f"- ... {remaining} more term(s)")
    print()

    print("Example Source Gap Families")
    if not example_source_gap_tags:
        print("- None")
    else:
        for item in example_source_gap_tags[:top]:
            print(f"- {safe_text(item['tag'])}: {item['terms_with_source_gaps']} term(s)")
        if len(example_source_gap_tags) > top:
            remaining = len(example_source_gap_tags) - top
            print(f"- ... {remaining} more tag group(s)")
    print()

    print("Preferred Translation Collisions")
    if not collisions:
        print("- None")
    else:
        for collision in collisions[:top]:
            terms = ", ".join(safe_text(term) for term in collision["terms"])
            print(f"- {safe_text(collision['preferred_translation'])}: {terms}")
        if len(collisions) > top:
            remaining = len(collisions) - top
            print(f"- ... {remaining} more collision group(s)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=15,
        help="Number of rows to show for long sections in text mode.",
    )
    args = parser.parse_args()

    if not TERMS_DIR.exists():
        print(f"ERROR: Terms directory not found: {TERMS_DIR}")
        return 1

    terms = load_terms()
    if not terms:
        print("WARNING: No term files found in terms/")
        return 0

    report = build_report(terms)
    if args.format == "json":
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print_text_report(report, top=args.top)
    return 0


if __name__ == "__main__":
    sys.exit(main())
