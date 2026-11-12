#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the verbal knowing cluster."""

from __future__ import annotations

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

HEADWORD_TERMS = ["janati", "abhijanati", "pajanati", "sanjanati", "mannati", "anna"]
SUPPORTING_TERMS = [
    "nana",
    "vijja",
    "panna",
    "parinna",
    "sanna",
    "sampajanna",
    "sati",
    "avijja",
    "ditthi",
    "abhinna",
    "asmimana",
    "upadana",
    "vitakka",
    "papanca",
    "yathabhuta-nanadassana",
    "vimutti-nanadassana",
]
FORMULA_TERMS = [
    "yathabhutam-pajanati",
    "naparam-itthattayati-pajanati",
    "yam-vedeti-tam-sanjanati",
    "yam-sanjanati-tam-vitakketi",
    "yam-vitakketi-tam-papanceti",
    "yam-papanceti-tato-nidanam-purisam-papanca-sanna-sankha-samudacaranti",
    "pathavim-pathavito-sannatva-pathavim-mannati",
    "pathavim-pathavito-abhinnaya-pathavim-ma-manni",
    "pathavim-pathavito-abhinnaya-pathavim-na-mannati",
    "nandi-dukkhassa-mulan",
    "bhava-jati-bhutassa-jaramaranam",
]


def render_mismatch_warnings(terms: dict[str, dict[str, object]]) -> list[str]:
    warnings: list[str] = []
    expected = {
        "janati": "knows",
        "abhijanati": "directly knows",
        "pajanati": "discerns",
        "sanjanati": "recognizes",
        "mannati": "thinks of",
        "anna": "final knowledge",
        "yathabhutam-pajanati": "discerns it as it has come to be",
        "naparam-itthattayati-pajanati": "one discerns: there is no more of this state of being",
        "yam-vedeti-tam-sanjanati": "what one feels, one recognizes",
        "yam-sanjanati-tam-vitakketi": "what one recognizes, one thinks about",
        "yam-vitakketi-tam-papanceti": "what one thinks about, one proliferates about",
        "yam-papanceti-tato-nidanam-purisam-papanca-sanna-sankha-samudacaranti": (
            "from what one proliferates about as the source, the recognitions and notions of proliferation sweep over a person"
        ),
        "pathavim-pathavito-sannatva-pathavim-mannati": (
            "having recognized earth as earth, one thinks of oneself as earth"
        ),
        "pathavim-pathavito-abhinnaya-pathavim-ma-manni": (
            "having directly known earth as earth, one should not think of oneself as earth"
        ),
        "pathavim-pathavito-abhinnaya-pathavim-na-mannati": (
            "having directly known earth as earth, one does not think of oneself as earth"
        ),
        "nandi-dukkhassa-mulan": "delight is the root of dissatisfaction",
        "bhava-jati-bhutassa-jaramaranam": (
            "with becoming there is birth, and for whatever has come to be there are aging and death"
        ),
    }
    for stem, expected_rendering in expected.items():
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        if data.get("preferred_translation") != expected_rendering:
            warnings.append(stem)
    return warnings


def build_report(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    all_priority = HEADWORD_TERMS + SUPPORTING_TERMS + FORMULA_TERMS
    return {
        "summary": {
            "headwords_present": len(HEADWORD_TERMS) - len(missing_terms(terms, HEADWORD_TERMS)),
            "headwords_expected": len(HEADWORD_TERMS),
            "supporting_terms_present": len(SUPPORTING_TERMS) - len(missing_terms(terms, SUPPORTING_TERMS)),
            "supporting_terms_expected": len(SUPPORTING_TERMS),
            "formula_records_present": len(FORMULA_TERMS) - len(missing_terms(terms, FORMULA_TERMS)),
            "formula_records_expected": len(FORMULA_TERMS),
        },
        "errors": {
            "missing_headwords": missing_terms(terms, HEADWORD_TERMS),
            "missing_supporting_terms": missing_terms(terms, SUPPORTING_TERMS),
            "missing_formula_records": missing_terms(terms, FORMULA_TERMS),
            "cluster_example_source_gaps": example_source_gaps(terms, all_priority),
        },
        "warnings": {
            "headwords_with_thin_authority_basis": weak_authority_terms(terms, HEADWORD_TERMS),
            "preferred_rendering_mismatches": render_mismatch_warnings(terms),
        },
    }


def render_glossary(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Verbal Knowing / Recognition / Selfing Glossary",
        "",
        "| Pali | Default | Allowed alternates | Discouraged |",
        "| --- | --- | --- | --- |",
    ]
    for stem in HEADWORD_TERMS + SUPPORTING_TERMS:
        data = terms[stem]
        alts = ", ".join(data.get("alternative_translations", []))
        discouraged = ", ".join(data.get("discouraged_translations", []))
        lines.append(
            f"| {data.get('term')} | {data.get('preferred_translation')} | {alts or '-'} | {discouraged or '-'} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_contrast_sheet(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Verbal Knowing / Recognition / Selfing Contrast Sheet",
        "",
        f"- `{terms['janati']['term']}`: `{terms['janati']['preferred_translation']}`",
        f"- `{terms['abhijanati']['term']}`: `{terms['abhijanati']['preferred_translation']}`",
        f"- `{terms['pajanati']['term']}`: `{terms['pajanati']['preferred_translation']}`",
        f"- `{terms['sanjanati']['term']}`: `{terms['sanjanati']['preferred_translation']}`",
        f"- `{terms['mannati']['term']}`: `{terms['mannati']['preferred_translation']}`",
        f"- `{terms['anna']['term']}`: `{terms['anna']['preferred_translation']}`",
        "",
        "## Keep Distinct",
        "",
        "- `janati` is plain knowing-language, not discernment, direct-knowing, or accomplishment-talk.",
        "- `abhijanati` is strengthened direct-knowing language, not mere recognition or generic realization-talk.",
        "- `pajanati` is a sharper discerning verb, but not completed `parinna`.",
        "- `sanjanati` is recognition-language in the `sanna` family, not generic knowledge or liberating insight.",
        "- `mannati` is selfing and taking-as language, not bland thought-language.",
        "- `anna` is accomplishment-side final knowledge, not just another way of saying `nana` or vague realization.",
        "- `sati` remains remembering, and `sampajanna` remains practice-side clear knowing.",
        "",
        "## Verb / Noun Guardrails",
        "",
        "- `janati` <-> `nana`: keep the broad knowing family coherent without inflating the verb.",
        "- `abhijanati` <-> `abhinna`: keep direct-knowing language and higher-knowledge language related without flattening them together.",
        "- `pajanati` <-> `panna` / `parinna`: keep the verb sharper than plain knowing but short of completed full understanding.",
        "- `sanjanati` -> `mannati`: preserve the MN 1 movement from recognition into selfing.",
        "- `mannati` <-> `asmimana` / `upadana` / `papanca`: keep the selfing verb tied to I-making, appropriation, and proliferation.",
        "- `anna` <-> `vijja`: keep accomplishment-side knowledge distinct from broader clear knowledge.",
        "",
        "## Formula Guardrails",
        "",
        f"- `{terms['yathabhutam-pajanati']['term']}` -> `{terms['yathabhutam-pajanati']['preferred_translation']}`",
        (
            f"- `{terms['naparam-itthattayati-pajanati']['term']}` -> "
            f"`{terms['naparam-itthattayati-pajanati']['preferred_translation']}`"
        ),
        f"- `{terms['yam-vedeti-tam-sanjanati']['term']}` -> `{terms['yam-vedeti-tam-sanjanati']['preferred_translation']}`",
        (
            f"- `{terms['yam-sanjanati-tam-vitakketi']['term']}` -> "
            f"`{terms['yam-sanjanati-tam-vitakketi']['preferred_translation']}`"
        ),
        (
            f"- `{terms['yam-vitakketi-tam-papanceti']['term']}` -> "
            f"`{terms['yam-vitakketi-tam-papanceti']['preferred_translation']}`"
        ),
        (
            f"- `{terms['yam-papanceti-tato-nidanam-purisam-papanca-sanna-sankha-samudacaranti']['term']}` -> "
            f"`{terms['yam-papanceti-tato-nidanam-purisam-papanca-sanna-sankha-samudacaranti']['preferred_translation']}`"
        ),
        (
            f"- `{terms['pathavim-pathavito-sannatva-pathavim-mannati']['term']}` -> "
            f"`{terms['pathavim-pathavito-sannatva-pathavim-mannati']['preferred_translation']}`"
        ),
        (
            f"- `{terms['pathavim-pathavito-abhinnaya-pathavim-ma-manni']['term']}` -> "
            f"`{terms['pathavim-pathavito-abhinnaya-pathavim-ma-manni']['preferred_translation']}`"
        ),
        (
            f"- `{terms['pathavim-pathavito-abhinnaya-pathavim-na-mannati']['term']}` -> "
            f"`{terms['pathavim-pathavito-abhinnaya-pathavim-na-mannati']['preferred_translation']}`"
        ),
        f"- `{terms['nandi-dukkhassa-mulan']['term']}` -> `{terms['nandi-dukkhassa-mulan']['preferred_translation']}`",
        (
            f"- `{terms['bhava-jati-bhutassa-jaramaranam']['term']}` -> "
            f"`{terms['bhava-jati-bhutassa-jaramaranam']['preferred_translation']}`"
        ),
        "",
        "## Source-Facing Guardrails",
        "",
        "- Preserve the practical anti-mystification pressure in the knowing verbs: do not inflate them into imported realization-language.",
        "- Preserve the MN 1 sequence from recognition into selfing, and from direct knowing into non-selfing.",
        "- Preserve the MN 18 sequence from feeling into recognition, from recognition into thinking, and from thinking into proliferation.",
        "- Preserve the closing pressure in MN 1: delight feeds dissatisfaction, and becoming keeps the birth-and-death sequence live.",
        "- Preserve MN 18 compatibility: what is recognized can become the footing for thought and proliferation if the family is flattened.",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "verbal-knowing-cluster-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "verbal-knowing-cluster-contrast-sheet.md": render_contrast_sheet(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    common.print_text_report("Verbal Knowing / Recognition / Selfing Cluster Report", report)


def main() -> int:
    return common.run_cli(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main())
