#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the jhana core cluster."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from scripts import cluster_report_common as common
    from scripts.cluster_report_common import load_terms, missing_terms, example_source_gaps, weak_authority_terms
except ModuleNotFoundError:
    import cluster_report_common as common
    from cluster_report_common import load_terms, missing_terms, example_source_gaps, weak_authority_terms


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
OUTPUT_DIR = REPO_ROOT / "docs" / "generated"

HEADWORD_TERMS = [
    "jhana",
    "jhayati",
    "samadhi",
    "samma-samadhi",
    "vitakka",
    "vicara",
    "ekaggata",
    "piti",
    "sukha",
    "nivarana",
    "bhavana",
]

SEQUENCE_TERMS = [
    "pathama-jhana",
    "dutiya-jhana",
    "tatiya-jhana",
    "catuttha-jhana",
]

FORMULA_TERMS = [
    "vivekaja-piti-sukha",
    "avitakka-avicara",
    "cetaso-ekodibhava",
    "ajjhatta-sampasadana",
    "samadhija-piti-sukha",
    "upekkha-sukha",
    "upekkha-satiparisuddha",
    "upekkha-satiparisuddhi",
]

EXPECTED_PREFERRED_TRANSLATIONS = {
    "jhana": "mental theme",
    "jhayati": "think like this",
    "ekaggata": "directness",
    "samadhi": "unification of mind",
    "samma-samadhi": "right unification of mind",
    "pathama-jhana": "first mental theme",
    "dutiya-jhana": "second mental theme",
    "tatiya-jhana": "third mental theme",
    "catuttha-jhana": "fourth mental theme",
}


def thin_terms(terms: dict[str, dict[str, object]], stems: list[str]) -> list[str]:
    thin: list[str] = []
    for stem in stems:
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        examples = data.get("example_phrases")
        policy = data.get("translation_policy")
        related = data.get("related_terms")
        if not isinstance(examples, list) or not examples or not isinstance(policy, dict) or not isinstance(related, list):
            thin.append(stem)
    return thin


def preferred_rendering_mismatches(terms: dict[str, dict[str, object]]) -> list[str]:
    mismatches: list[str] = []
    for stem, expected in EXPECTED_PREFERRED_TRANSLATIONS.items():
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        actual = data.get("preferred_translation")
        if actual != expected:
            mismatches.append(f"{stem}: expected '{expected}', found '{actual}'")
    return mismatches


def samma_samadhi_identity_missing(terms: dict[str, dict[str, object]]) -> list[str]:
    data = terms.get("samma-samadhi")
    if not isinstance(data, dict):
        return []
    blob = json.dumps(data, ensure_ascii=False).casefold()
    if ("jhāna" not in blob and "jhana" not in blob) or any(
        token not in blob for token in ("first", "second", "third", "fourth")
    ):
        return ["samma-samadhi"]
    return []


def build_report(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    all_priority = HEADWORD_TERMS + SEQUENCE_TERMS + FORMULA_TERMS
    return {
        "summary": {
            "headwords_present": len(HEADWORD_TERMS) - len(missing_terms(terms, HEADWORD_TERMS)),
            "headwords_expected": len(HEADWORD_TERMS),
            "sequence_terms_present": len(SEQUENCE_TERMS) - len(missing_terms(terms, SEQUENCE_TERMS)),
            "sequence_terms_expected": len(SEQUENCE_TERMS),
            "formula_terms_present": len(FORMULA_TERMS) - len(missing_terms(terms, FORMULA_TERMS)),
            "formula_terms_expected": len(FORMULA_TERMS),
        },
        "errors": {
            "missing_headwords": missing_terms(terms, HEADWORD_TERMS),
            "missing_sequence_terms": missing_terms(terms, SEQUENCE_TERMS),
            "missing_formula_terms": missing_terms(terms, FORMULA_TERMS),
            "cluster_example_source_gaps": example_source_gaps(terms, all_priority),
        },
        "warnings": {
            "headwords_with_thin_authority_basis": weak_authority_terms(terms, HEADWORD_TERMS),
            "sequence_terms_still_thin": thin_terms(terms, SEQUENCE_TERMS),
            "formula_terms_still_thin": thin_terms(terms, FORMULA_TERMS),
            "preferred_rendering_mismatches": preferred_rendering_mismatches(terms),
            "samma_samadhi_identity_missing": samma_samadhi_identity_missing(terms),
        },
    }


def render_glossary(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Jhana Cluster Glossary",
        "",
        "| Pali | Default | Allowed alternates | Discouraged |",
        "| --- | --- | --- | --- |",
    ]
    for stem in HEADWORD_TERMS:
        data = terms[stem]
        alts = ", ".join(data.get("alternative_translations", []))
        discouraged = ", ".join(data.get("discouraged_translations", []))
        lines.append(
            f"| {data.get('term')} | {data.get('preferred_translation')} | {alts or '-'} | {discouraged or '-'} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_sequence_sheet(terms: dict[str, dict[str, object]]) -> str:
    linked_formulas = {
        "pathama-jhana": ["vivekaja-piti-sukha"],
        "dutiya-jhana": ["avitakka-avicara", "ajjhatta-sampasadana", "cetaso-ekodibhava", "samadhija-piti-sukha"],
        "tatiya-jhana": ["upekkha-sukha"],
        "catuttha-jhana": ["upekkha-satiparisuddha", "upekkha-satiparisuddhi"],
    }
    lines = [
        "# Jhana Sequence Sheet",
        "",
        f"- `{terms['samma-samadhi']['term']}` is governed in this repository as the first, second, third, and fourth `{terms['jhana']['term']}`.",
        f"- Keep `{terms['jhana']['term']}` as `{terms['jhana']['preferred_translation']}` across the fourfold sequence unless a controlled technical reason requires the Pali.",
        "",
    ]
    for stem in SEQUENCE_TERMS:
        data = terms[stem]
        lines.append(f"## {data.get('term')}")
        lines.append("")
        lines.append(f"- Default: `{data.get('preferred_translation')}`")
        lines.append(f"- Notes: {data.get('definition')}")
        formulas = linked_formulas.get(stem, [])
        if formulas:
            formula_text = ", ".join(
                f"`{terms[item].get('term')}` -> {terms[item].get('preferred_translation')}"
                for item in formulas
            )
            lines.append(f"- Linked formulas: {formula_text}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_path_brief(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Jhana Path Brief",
        "",
        "## Path Rule",
        "",
        f"- `{terms['samma-samadhi']['term']}` is the first, second, third, and fourth `{terms['jhana']['term']}`.",
        f"- Keep `{terms['samma-samadhi']['preferred_translation']}` as the default rendering for the path factor while making that fourfold identity explicit in notes and explanations.",
        "",
        "## Core Defaults",
        "",
        f"- `{terms['jhana']['term']}` -> `{terms['jhana']['preferred_translation']}`",
        f"- `{terms['jhayati']['term']}` -> `{terms['jhayati']['preferred_translation']}`",
        f"- `{terms['ekaggata']['term']}` -> `{terms['ekaggata']['preferred_translation']}`",
        f"- `{terms['samadhi']['term']}` -> `{terms['samadhi']['preferred_translation']}`",
        f"- `{terms['vitakka']['term']}` and `{terms['vicara']['term']}` stay coordinated as the practical pair in the first mental theme.",
        "- The first mental theme is not treated as separate from ānāpānasati; the same training clears hindrances, brings up wholesome dhammas, and keeps the line of practice direct.",
        "",
        "## Drift Guards",
        "",
        "- Do not widen ariya samma samadhi into a vague concentration category.",
        "- Do not let jhana drift into trance, absorption, or ecstasy language.",
        "- Keep the hindrance-clearing and practical-development frame visible across the cluster.",
        "- Keep the fourfold sequence stable unless a controlled technical reason requires untranslated Pali.",
    ]
    return "\n".join(lines)


def render_formula_sheet(terms: dict[str, dict[str, object]]) -> str:
    by_stage = {
        "First mental theme": ["vivekaja-piti-sukha"],
        "Second mental theme": [
            "avitakka-avicara",
            "ajjhatta-sampasadana",
            "cetaso-ekodibhava",
            "samadhija-piti-sukha",
        ],
        "Third mental theme": ["upekkha-sukha"],
        "Fourth mental theme": ["upekkha-satiparisuddha", "upekkha-satiparisuddhi"],
    }
    lines = [
        "# Jhana Formula Sheet",
        "",
    ]
    for title, stems in by_stage.items():
        lines.append(f"## {title}")
        lines.append("")
        for stem in stems:
            data = terms[stem]
            lines.append(f"- `{data.get('term')}` -> {data.get('preferred_translation')}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "jhana-cluster-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "jhana-sequence-sheet.md": render_sequence_sheet(terms),
        OUTPUT_DIR / "jhana-path-brief.md": render_path_brief(terms),
        OUTPUT_DIR / "jhana-formula-sheet.md": render_formula_sheet(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + ("" if content.endswith("\n") else "\n"), encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    common.print_text_report("Jhana Cluster Report", report)


def main() -> int:
    return common.run_cli(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main())
