#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the sense-fields cluster."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from scripts import cluster_report_common as common
    from scripts.cluster_report_common import load_terms, missing_terms, example_source_gaps, weak_authority_terms, contains_all
except ModuleNotFoundError:
    import cluster_report_common as common
    from cluster_report_common import load_terms, missing_terms, example_source_gaps, weak_authority_terms, contains_all


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
OUTPUT_DIR = REPO_ROOT / "docs" / "generated"

HEADWORD_TERMS = [
    "ayatana",
    "salayatana",
    "phassa",
]

FIELD_TERMS = [
    "cakkhayatana",
    "sotayatana",
    "ghanayatana",
    "jivhayatana",
    "kayayatana",
    "manayatana",
    "rupayatana",
    "saddayatana",
    "gandhayatana",
    "rasayatana",
    "photthabbatana",
    "dhammayatana",
]

CONTACT_TERMS = [
    "cakkhu-samphassa",
    "sota-samphassa",
    "ghana-samphassa",
    "jivha-samphassa",
    "kaya-samphassa",
    "mano-samphassa",
]

FORMULA_TERMS = [
    "namarupapaccaya-salayatanam",
    "salayatanapaccaya-phasso",
    "phassapaccaya-vedana",
]

EXPECTED_PREFERRED_TRANSLATIONS = {
    "ayatana": "field",
    "salayatana": "six fields of experience",
    "phassa": "contact",
    "cakkhayatana": "eye sense field",
    "sotayatana": "ear sense field",
    "ghanayatana": "nose sense field",
    "jivhayatana": "tongue sense field",
    "kayayatana": "body sense field",
    "manayatana": "mind sense field",
    "rupayatana": "form sense field",
    "saddayatana": "sound sense field",
    "gandhayatana": "odor sense field",
    "rasayatana": "taste sense field",
    "photthabbatana": "tangible sense field",
    "dhammayatana": "dhamma sense field",
    "cakkhu-samphassa": "eye-contact",
    "sota-samphassa": "ear-contact",
    "ghana-samphassa": "nose-contact",
    "jivha-samphassa": "tongue-contact",
    "kaya-samphassa": "body-contact",
    "mano-samphassa": "mind-contact",
    "namarupapaccaya-salayatanam": "with name-and-form as condition, the six fields of experience",
    "salayatanapaccaya-phasso": "with the six fields of experience as condition, contact",
    "phassapaccaya-vedana": "with contact as condition, felt experience",
}


def thin_terms(terms: dict[str, dict[str, object]], stems: list[str]) -> list[str]:
    thin: list[str] = []
    for stem in stems:
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        notes = data.get("notes")
        related = data.get("related_terms")
        examples = data.get("example_phrases")
        if (
            not isinstance(notes, str)
            or not notes.strip()
            or not isinstance(related, list)
            or not related
            or not isinstance(examples, list)
            or not examples
        ):
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


def contact_chain_identity_missing(terms: dict[str, dict[str, object]]) -> list[str]:
    missing: list[str] = []
    expectations = {
        "salayatana": ["contact"],
        "phassa": ["sense field", "earliest practical pivot"],
        "namarupapaccaya-salayatanam": ["six fields of experience"],
        "salayatanapaccaya-phasso": ["six fields of experience", "contact"],
        "phassapaccaya-vedana": ["contact", "felt experience"],
    }
    for stem, tokens in expectations.items():
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        blob = json.dumps(data, ensure_ascii=False).casefold()
        if not contains_all(blob, tokens):
            missing.append(stem)
    return missing


def build_report(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    all_priority = HEADWORD_TERMS + FIELD_TERMS + CONTACT_TERMS + FORMULA_TERMS
    return {
        "summary": {
            "headwords_present": len(HEADWORD_TERMS) - len(missing_terms(terms, HEADWORD_TERMS)),
            "headwords_expected": len(HEADWORD_TERMS),
            "field_terms_present": len(FIELD_TERMS) - len(missing_terms(terms, FIELD_TERMS)),
            "field_terms_expected": len(FIELD_TERMS),
            "contact_terms_present": len(CONTACT_TERMS) - len(missing_terms(terms, CONTACT_TERMS)),
            "contact_terms_expected": len(CONTACT_TERMS),
            "formula_terms_present": len(FORMULA_TERMS) - len(missing_terms(terms, FORMULA_TERMS)),
            "formula_terms_expected": len(FORMULA_TERMS),
        },
        "errors": {
            "missing_headwords": missing_terms(terms, HEADWORD_TERMS),
            "missing_field_terms": missing_terms(terms, FIELD_TERMS),
            "missing_contact_terms": missing_terms(terms, CONTACT_TERMS),
            "missing_formula_terms": missing_terms(terms, FORMULA_TERMS),
            "cluster_example_source_gaps": example_source_gaps(terms, all_priority),
        },
        "warnings": {
            "headwords_with_thin_authority_basis": weak_authority_terms(terms, HEADWORD_TERMS),
            "field_terms_still_thin": thin_terms(terms, FIELD_TERMS),
            "contact_terms_still_thin": thin_terms(terms, CONTACT_TERMS),
            "preferred_rendering_mismatches": preferred_rendering_mismatches(terms),
            "contact_chain_identity_missing": contact_chain_identity_missing(terms),
        },
    }


def render_glossary(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Sense-Fields Cluster Glossary",
        "",
        "| Role | Pali | Default | Allowed alternates | Discouraged |",
        "| --- | --- | --- | --- | --- |",
    ]
    grouped_terms = (
        [("Headword", stem) for stem in HEADWORD_TERMS]
        + [("Field", stem) for stem in FIELD_TERMS]
        + [("Contact", stem) for stem in CONTACT_TERMS]
    )
    for role, stem in grouped_terms:
        data = terms[stem]
        alts = ", ".join(data.get("alternative_translations", []))
        discouraged = ", ".join(data.get("discouraged_translations", []))
        lines.append(
            f"| {role} | {data.get('term')} | {data.get('preferred_translation')} | {alts or '-'} | {discouraged or '-'} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_twelve_field_map(terms: dict[str, dict[str, object]]) -> str:
    pairs = [
        ("cakkhayatana", "rupayatana", "cakkhu-samphassa"),
        ("sotayatana", "saddayatana", "sota-samphassa"),
        ("ghanayatana", "gandhayatana", "ghana-samphassa"),
        ("jivhayatana", "rasayatana", "jivha-samphassa"),
        ("kayayatana", "photthabbatana", "kaya-samphassa"),
        ("manayatana", "dhammayatana", "mano-samphassa"),
    ]
    lines = [
        "# Sense-Fields Twelve-Field Map",
        "",
        "| Internal field | Object field | Contact event |",
        "| --- | --- | --- |",
    ]
    for internal, object_field, contact in pairs:
        lines.append(
            f"| {terms[internal].get('preferred_translation')} | {terms[object_field].get('preferred_translation')} | {terms[contact].get('preferred_translation')} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_contact_interface_sheet(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Sense-Fields Contact Sheet",
        "",
        f"- `{terms['ayatana']['term']}` stays `{terms['ayatana']['preferred_translation']}` across the family and blocks silent drift back to `base` or `organ` language.",
        f"- `{terms['salayatana']['term']}` stays `{terms['salayatana']['preferred_translation']}` and should remain readable as the experiential field structure from which contact can arise.",
        f"- `{terms['phassa']['term']}` stays `{terms['phassa']['preferred_translation']}` as the event-term, not the feeling that follows and not mere physical touch.",
        f"- `{terms['salayatanapaccaya-phasso']['term']}` -> `{terms['salayatanapaccaya-phasso']['preferred_translation']}` keeps the family linked at the chain level.",
        f"- `{terms['phassapaccaya-vedana']['term']}` -> `{terms['phassapaccaya-vedana']['preferred_translation']}` keeps contact distinct from felt experience.",
    ]
    return "\n".join(lines)


def render_translator_brief(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Sense-Fields Translator Brief",
        "",
        "## Core Defaults",
        "",
        f"- `{terms['ayatana']['term']}` -> `{terms['ayatana']['preferred_translation']}`",
        f"- `{terms['salayatana']['term']}` -> `{terms['salayatana']['preferred_translation']}`",
        f"- `{terms['phassa']['term']}` -> `{terms['phassa']['preferred_translation']}`",
        "",
        "## Drift Guards",
        "",
        "- Do not reduce the field family to physical sense organs alone.",
        "- Do not let `base` silently replace `field` across the cluster.",
        "- Do not let contact drift into sensation, feeling, or vague encounter-language.",
        "- Keep the twelve-field map readable as lived process rather than faculty-metaphysics.",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "sense-fields-cluster-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "sense-fields-twelve-field-map.md": render_twelve_field_map(terms),
        OUTPUT_DIR / "sense-fields-contact-interface-sheet.md": render_contact_interface_sheet(terms),
        OUTPUT_DIR / "sense-fields-translator-brief.md": render_translator_brief(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + ("" if content.endswith("\n") else "\n"), encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    common.print_text_report("Sense-Fields Cluster Report", report)


def main() -> int:
    return common.run_cli(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main())
