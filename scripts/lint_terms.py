#!/usr/bin/env python3
"""Run editorial lint checks against term JSON files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    from scripts.repair_guidance import (
        RepairDiagnostic,
        diagnostics_as_json,
        field_examples,
        field_snippet,
        print_diagnostics,
        CLUSTER_DOC_EXAMPLES,
        MAJOR_POLICY_EXAMPLES,
        RELATIONSHIP_EXAMPLES,
        STATUS_EXAMPLES,
    )
    from scripts.text_utils import normalize_term, safe_text
    from scripts.term_store import iter_term_files
except ModuleNotFoundError:
    from repair_guidance import (
        RepairDiagnostic,
        diagnostics_as_json,
        field_examples,
        field_snippet,
        print_diagnostics,
        CLUSTER_DOC_EXAMPLES,
        MAJOR_POLICY_EXAMPLES,
        RELATIONSHIP_EXAMPLES,
        STATUS_EXAMPLES,
    )
    from text_utils import normalize_term, safe_text
    from term_store import iter_term_files


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
GENERIC_AUTHORITY_SOURCES = {"Repository editorial record"}
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
STABILIZED_RULE_TERMS = {
    "anatta",
    "anusaya",
    "asava",
    "ayatana",
    "bhava",
    "dhamma",
    "ditthi",
    "ditthupadana",
    "dukkha",
    "jati",
    "jhana",
    "khandha",
    "mano",
    "mana",
    "namarupa",
    "nibbana",
    "nirodha",
    "paccaya",
    "panna",
    "paticcasamuppada",
    "rupa",
    "samadhi",
    "samyojana",
    "sankhara",
    "sakkaya",
    "sati",
    "tanha",
    "upadana",
    "upakkilesa",
    "attavadupadana",
    "asmimana",
    "vedana",
    "vicara",
    "vinnana",
    "vitakka",
    "kilesa",
}
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
HIGH_LOAD_MINOR_LINT_THRESHOLD = 9

MISSING_RELATED_RE = re.compile(
    r"^(?P<file>[^:]+): related term '(?P<related>[^']+)' does not resolve to a local entry$"
)
RECIPROCAL_RE = re.compile(
    r"^(?P<src>[^ ]+) -> (?P<dst>[^ ]+): related_terms link is not reciprocal$"
)
MISSING_SUTTA_RE = re.compile(
    r"^(?P<file>[^:]+): major (?P<status>reviewed|stable) entry is missing sutta_references$"
)
EXAMPLE_SOURCE_RE = re.compile(
    r"^(?P<file>[^:]+): major (?P<status>reviewed|stable) entry has example_phrases missing source on item\(s\) (?P<indexes>.+)$"
)
THIN_GOVERNANCE_RE = re.compile(
    r"^(?P<file>[^:]+): major (?P<status>reviewed|stable) entry has a thin governance surface "
    r"\(context_rules=(?P<context>\d+), example_phrases=(?P<examples>\d+), note_words=(?P<words>\d+)\); "
    r"expand the note or add another rule/example$"
)
SHORT_NOTES_RE = re.compile(
    r"^(?P<file>[^:]+): major entry notes are too short to function as a rule-bearing policy surface$"
)
POLICY_NOTES_RE = re.compile(
    r"^(?P<file>[^:]+): major entry notes do not read as explicit policy; make the rule and drift guard visible$"
)
STABLE_GATE_RE = re.compile(
    r"^(?P<file>[^:]+): stable major entry does not yet meet the stable-floor maturity gate "
    r"\(context_rules=(?P<context>\d+), example_phrases=(?P<examples>\d+), authority_basis=(?P<authority>\d+), note_words=(?P<words>\d+)\); "
    r"demote to reviewed or deepen the rule surface$"
)
HIGH_LOAD_MINOR_POLICY_RE = re.compile(
    r"^(?P<file>[^:]+): high-load minor entry is missing translation_policy "
    r"\(score=(?P<score>\d+)\); add a compact rule summary before further reuse$"
)


def is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def has_rule_language(text: str) -> bool:
    lowered = text.casefold()
    return any(marker in lowered for marker in RULE_LANGUAGE_MARKERS)


def high_load_minor_score(data: dict[str, object]) -> int:
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


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_terms(terms_dir: Path = TERMS_DIR) -> dict[str, dict[str, object]]:
    terms: dict[str, dict[str, object]] = {}
    for path in iter_term_files(terms_dir):
        data = load_json(path)
        if not isinstance(data, dict):
            continue
        terms[normalize_term(path.stem)] = data
    return terms


def check_missing_related_terms(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        related_terms = data.get("related_terms", [])
        if not isinstance(related_terms, list):
            continue
        for related in related_terms:
            if not isinstance(related, str):
                continue
            target = normalize_term(related)
            if target not in terms:
                issues.append(
                    f"{stem}.json: related term '{safe_text(related)}' does not resolve to a local entry"
                )
    return issues


def check_one_way_related_terms(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        if data.get("entry_type") == "minor" and data.get("part_of_speech") in {"phrase", "expression"}:
            continue
        related_terms = data.get("related_terms", [])
        if not isinstance(related_terms, list):
            continue
        for related in related_terms:
            if not isinstance(related, str):
                continue
            target = normalize_term(related)
            if target not in terms:
                continue
            reverse_related = terms[target].get("related_terms", [])
            if not isinstance(reverse_related, list):
                reverse_related = []
            reverse_stems = {normalize_term(item) for item in reverse_related if isinstance(item, str)}
            if stem not in reverse_stems:
                issues.append(
                    f"{stem}.json -> {target}.json: related_terms link is not reciprocal"
                )
    return issues


def check_missing_sutta_references(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        entry_type = data.get("entry_type")
        status = data.get("status")
        references = data.get("sutta_references", [])
        if (
            entry_type == "major"
            and status in {"reviewed", "stable"}
            and (not isinstance(references, list) or len(references) == 0)
        ):
            issues.append(
                f"{stem}.json: major {status} entry is missing sutta_references"
            )
    return issues


def check_missing_example_sources(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        entry_type = data.get("entry_type")
        status = data.get("status")
        examples = data.get("example_phrases", [])
        if entry_type != "major" or status not in {"reviewed", "stable"}:
            continue
        if not isinstance(examples, list) or len(examples) == 0:
            continue

        missing_indexes = [
            index
            for index, example in enumerate(examples, start=1)
            if isinstance(example, dict) and not is_non_empty_string(example.get("source"))
        ]
        if missing_indexes:
            joined = ", ".join(str(index) for index in missing_indexes)
            issues.append(
                f"{stem}.json: major {status} entry has example_phrases missing source on item(s) {joined}"
            )
    return issues


def check_thin_governance_surfaces(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        if data.get("entry_type") != "major" or data.get("status") not in {"reviewed", "stable"}:
            continue

        notes = data.get("notes")
        context_rules = data.get("context_rules")
        examples = data.get("example_phrases")

        note_words = len(notes.split()) if isinstance(notes, str) else 0
        context_count = len(context_rules) if isinstance(context_rules, list) else 0
        example_count = len(examples) if isinstance(examples, list) else 0

        if note_words < 90 and context_count < 3 and example_count < 2:
            issues.append(
                f"{stem}.json: major {data.get('status')} entry has a thin governance surface "
                f"(context_rules={context_count}, example_phrases={example_count}, note_words={note_words}); "
                "expand the note or add another rule/example"
            )
    return issues


def check_major_rule_note_quality(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        if data.get("entry_type") != "major":
            continue

        notes = data.get("notes")
        if not isinstance(notes, str) or not notes.strip():
            continue

        note_words = len(notes.split())
        if note_words < 40:
            issues.append(
                f"{stem}.json: major entry notes are too short to function as a rule-bearing policy surface"
            )
            continue

        if not has_rule_language(notes):
            issues.append(
                f"{stem}.json: major entry notes do not read as explicit policy; make the rule and drift guard visible"
            )
    return issues


def check_stable_status_discipline(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        if data.get("entry_type") != "major" or data.get("status") != "stable":
            continue

        notes = data.get("notes")
        context_rules = data.get("context_rules")
        examples = data.get("example_phrases")
        authority_basis = data.get("authority_basis")

        note_words = len(notes.split()) if isinstance(notes, str) else 0
        context_count = len(context_rules) if isinstance(context_rules, list) else 0
        example_count = len(examples) if isinstance(examples, list) else 0
        authority_count = len(authority_basis) if isinstance(authority_basis, list) else 0

        if (
            note_words < 70
            and context_count < 3
            and example_count < 2
            and authority_count < 2
        ):
            issues.append(
                f"{stem}.json: stable major entry does not yet meet the stable-floor maturity gate "
                f"(context_rules={context_count}, example_phrases={example_count}, "
                f"authority_basis={authority_count}, note_words={note_words}); demote to reviewed or deepen the rule surface"
            )
    return issues


def check_untranslated_preferences(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        untranslated = data.get("untranslated_preferred")
        gloss = data.get("gloss_on_first_occurrence")
        if untranslated is True and not isinstance(gloss, str):
            issues.append(
                f"{stem}.json: untranslated_preferred is true but gloss_on_first_occurrence is missing"
            )
    return issues


def check_suspicious_placeholders(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    text_fields = (
        "term",
        "preferred_translation",
        "literal_meaning",
        "definition",
        "gloss_on_first_occurrence",
    )
    for stem, data in sorted(terms.items()):
        for field in text_fields:
            value = data.get(field)
            if isinstance(value, str) and "?" in value:
                issues.append(
                    f"{stem}.json: field '{field}' contains '?' placeholder text; check for encoding loss"
                )
    return issues


def check_mojibake_patterns(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    suspicious = (
        "Ã",
        "Ä",
        "Å",
        "â€™",
        "â€œ",
        "â€",
        "á¹",
        "�",
    )

    def walk(value: object, path: str) -> None:
        if isinstance(value, str):
            for needle in suspicious:
                if needle in value:
                    issues.append(
                        f"{path}: contains suspicious mojibake sequence '{safe_text(needle)}'"
                    )
                    break
            return
        if isinstance(value, list):
            for index, item in enumerate(value):
                walk(item, f"{path}[{index}]")
            return
        if isinstance(value, dict):
            for key, item in value.items():
                walk(item, f"{path}.{key}")

    for stem, data in sorted(terms.items()):
        walk(data, f"{stem}.json")
    return issues


def check_stabilized_term_policy(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    required_list_fields = ("context_rules", "related_terms", "example_phrases", "sutta_references")

    for stem in sorted(STABILIZED_RULE_TERMS):
        data = terms.get(stem)
        if data is None:
            issues.append(f"{stem}.json: stabilized drift-danger term is missing")
            continue

        if data.get("entry_type") != "major":
            issues.append(f"{stem}.json: stabilized drift-danger term must be a major entry")

        status = data.get("status")
        if status not in {"reviewed", "stable"}:
            issues.append(
                f"{stem}.json: stabilized drift-danger term must be reviewed or stable"
            )

        notes = data.get("notes")
        if not isinstance(notes, str) or not notes.strip():
            issues.append(
                f"{stem}.json: stabilized drift-danger term must include rule-bearing notes"
            )

        for field in required_list_fields:
            value = data.get(field)
            if not isinstance(value, list) or len(value) == 0:
                issues.append(
                    f"{stem}.json: stabilized drift-danger term must include non-empty {field}"
                )

        context_rules = data.get("context_rules")
        if isinstance(context_rules, list) and len(context_rules) < 2:
            issues.append(
                f"{stem}.json: stabilized drift-danger term must include at least two context_rules"
            )

    return issues


def check_translation_policy_consistency(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        policy = data.get("translation_policy")
        if not isinstance(policy, dict):
            continue

        untranslated = data.get("untranslated_preferred") is True
        leave_untranslated_when = policy.get("leave_untranslated_when")
        default_scope = policy.get("default_scope")
        drift_risk = policy.get("drift_risk")
        inheritance = policy.get("compound_inheritance")

        if untranslated and not isinstance(leave_untranslated_when, str):
            issues.append(
                f"{stem}.json: untranslated-preferred policy should explain leave_untranslated_when in translation_policy"
            )

        if data.get("entry_type") == "major":
            if not isinstance(default_scope, str):
                issues.append(
                    f"{stem}.json: major entry with translation_policy should include default_scope"
                )
            if not isinstance(drift_risk, str):
                issues.append(
                    f"{stem}.json: major entry with translation_policy should include drift_risk"
                )
            if inheritance == "inherit":
                notes = data.get("notes")
                context_rules = data.get("context_rules")
                notes_text = notes.lower() if isinstance(notes, str) else ""
                context_mentions_compounds = False
                if isinstance(context_rules, list):
                    context_mentions_compounds = any(
                        isinstance(rule, dict)
                        and isinstance(rule.get("context"), str)
                        and "compound" in rule["context"].lower()
                        for rule in context_rules
                    )
                if "compound" not in notes_text and not context_mentions_compounds:
                    issues.append(
                        f"{stem}.json: translation_policy sets compound_inheritance to inherit but notes/context_rules do not mention compounds"
                    )

    return issues


def check_high_load_minor_translation_policy(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        if data.get("entry_type") != "minor" or data.get("status") not in {"reviewed", "stable"}:
            continue

        score = high_load_minor_score(data)
        if score < HIGH_LOAD_MINOR_LINT_THRESHOLD:
            continue

        policy = data.get("translation_policy")
        if not isinstance(policy, dict) or len(policy) == 0:
            issues.append(
                f"{stem}.json: high-load minor entry is missing translation_policy (score={score}); add a compact rule summary before further reuse"
            )
    return issues


def check_authority_basis_consistency(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        authority_basis = data.get("authority_basis")
        if authority_basis is None:
            continue
        if not isinstance(authority_basis, list) or len(authority_basis) == 0:
            issues.append(
                f"{stem}.json: authority_basis is present but empty"
            )
            continue

        notes = data.get("notes")
        notes_text = notes.lower() if isinstance(notes, str) else ""
        for index, item in enumerate(authority_basis, start=1):
            if not isinstance(item, dict):
                continue
            source = item.get("source")
            if isinstance(source, str):
                if source in GENERIC_AUTHORITY_SOURCES:
                    continue
                source_token = source.lower().split()[0]
                if source_token not in notes_text:
                    issues.append(
                        f"{stem}.json: authority_basis[{index}] source '{safe_text(source)}' is not reflected in notes"
                    )

    return issues


def check_generic_authority_basis_refinement(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        if data.get("entry_type") != "major":
            continue
        if data.get("status") not in {"reviewed", "stable"}:
            continue
        authority_basis = data.get("authority_basis")
        if not isinstance(authority_basis, list):
            continue
        if any(
            isinstance(item, dict) and item.get("source") in GENERIC_AUTHORITY_SOURCES
            for item in authority_basis
        ):
            issues.append(
                f"{stem}.json: reviewed/stable major entry still uses generic authority_basis source 'Repository editorial record'; refine provenance before merge"
            )
    return issues


def print_group(title: str, issues: list[str]) -> None:
    if not issues:
        return
    print(f"{title}:")
    for issue in issues:
        print(f"- {safe_text(issue)}")
    print()


def issue_file(issue: str) -> str | None:
    return issue.split(":", 1)[0] if ".json:" in issue else None


def build_lint_diagnostic(category: str, issue: str) -> RepairDiagnostic:
    match = MISSING_RELATED_RE.match(issue)
    if match:
        return RepairDiagnostic(
            severity="error",
            category=category,
            code="missing_related_term",
            rule="`related_terms` must resolve to live local entries",
            file=match.group("file"),
            summary=f"Missing local related term `{match.group('related')}`",
            why="Broken related-term links orphan the record from family review and make cross-term governance incomplete.",
            fix="Either add the missing local term record in the same pass or replace/remove the broken link with a real local headword.",
            examples=RELATIONSHIP_EXAMPLES,
        )

    match = RECIPROCAL_RE.match(issue)
    if match:
        src_stem = match.group("src").removesuffix(".json")
        return RepairDiagnostic(
            severity="warning",
            category=category,
            code="one_way_related_term",
            rule="Governed semantic relationships should be reciprocal",
            file=match.group("src"),
            summary=f"`{match.group('src')}` links to `{match.group('dst')}` but not back again",
            why="One-way links hide family coupling and make same-pass doctrinal review easier to miss.",
            fix=f"Add `{src_stem}` to `{match.group('dst')}` `related_terms` if the relationship is governing, or remove the forward-only link if it should not propagate policy.",
            examples=RELATIONSHIP_EXAMPLES,
        )

    match = MISSING_SUTTA_RE.match(issue)
    if match:
        return RepairDiagnostic(
            severity="warning",
            category=category,
            code="missing_sutta_references",
            rule="Reviewed or stable major entries need canonical anchors",
            file=match.group("file"),
            summary=f"Major {match.group('status')} entry is missing `sutta_references`",
            why="Without citations, contributors cannot tell which canonical contexts the live policy is meant to govern.",
            fix=f"Add one or more relevant `sutta_references`. Minimal compliant shape: {field_snippet('sutta_references')}",
            examples=field_examples("sutta_references"),
        )

    match = EXAMPLE_SOURCE_RE.match(issue)
    if match:
        return RepairDiagnostic(
            severity="warning",
            category=category,
            code="missing_example_sources",
            rule="Policy examples need sources",
            file=match.group("file"),
            summary=f"`example_phrases` item(s) {match.group('indexes')} are missing `source`",
            why="Unsourced examples cannot teach contributors where the governed rendering actually applies.",
            fix=f"Add a `source` to each listed example or remove examples that are not ready to act as policy evidence. Minimal compliant shape: {field_snippet('example_phrases')}",
            examples=field_examples("example_phrases"),
        )

    match = THIN_GOVERNANCE_RE.match(issue)
    if match:
        return RepairDiagnostic(
            severity="warning",
            category=category,
            code="thin_governance_surface",
            rule="Reviewed and stable majors need more than a definitional shell",
            file=match.group("file"),
            summary=(
                f"The record is still thin at context_rules={match.group('context')}, "
                f"example_phrases={match.group('examples')}, note_words={match.group('words')}"
            ),
            why="A thin governance surface leaves too much guesswork for later contributors and makes drift more likely in reuse.",
            fix="Strengthen either the note, the context rules, or the examples in the same pass so the entry teaches a future translator what to do without guessing.",
            examples=MAJOR_POLICY_EXAMPLES,
        )

    match = SHORT_NOTES_RE.match(issue)
    if match:
        return RepairDiagnostic(
            severity="error",
            category=category,
            code="major_notes_too_short",
            rule="Major entry notes must function as policy, not filler",
            file=match.group("file"),
            summary="Major-entry notes are too short to act as a rule surface",
            why="The note is where the repo explains the governing default, the drift risk, and the main contrast the entry protects.",
            fix="Replace short definitional prose with one compact policy paragraph that states the default, the drift risk, and at least one concrete contrast or scope limit.",
            examples=field_examples("notes"),
        )

    match = POLICY_NOTES_RE.match(issue)
    if match:
        return RepairDiagnostic(
            severity="error",
            category=category,
            code="major_notes_not_policy_bearing",
            rule="Major entry notes must state an explicit rule",
            file=match.group("file"),
            summary="The note reads as description rather than policy",
            why="If the note does not surface the rule, later contributors cannot tell what the record is protecting.",
            fix="Rewrite the note so it names the governed default, the main drift risk, and the conditions where the default should or should not apply.",
            examples=field_examples("notes"),
        )

    match = STABLE_GATE_RE.match(issue)
    if match:
        return RepairDiagnostic(
            severity="error",
            category=category,
            code="stable_status_too_strong",
            rule="`stable` is a reuse commitment, not praise",
            file=match.group("file"),
            summary=(
                f"The record is marked `stable` with context_rules={match.group('context')}, "
                f"example_phrases={match.group('examples')}, authority_basis={match.group('authority')}, "
                f"note_words={match.group('words')}"
            ),
            why="A stable entry should already be strong enough for downstream work to follow it without caveat.",
            fix="Either deepen the record in the same pass or demote the status to `reviewed` until the rule surface is mature enough to anchor reuse.",
            examples=STATUS_EXAMPLES,
        )

    match = HIGH_LOAD_MINOR_POLICY_RE.match(issue)
    if match:
        return RepairDiagnostic(
            severity="warning",
            category=category,
            code="high_load_minor_missing_translation_policy",
            rule="High-load minor records need a compact rule summary",
            file=match.group("file"),
            summary=f"The minor record carries high governance load at score={match.group('score')} but has no `translation_policy`",
            why="A high-load minor may still be a minor record, but repeated doctrinal reuse becomes fragile if tools cannot see its default scope and drift guard.",
            fix=f"Add a compact `translation_policy` block describing default scope, non-application, inheritance, and drift risk. Minimal compliant shape: {field_snippet('translation_policy')}",
            examples=field_examples("translation_policy"),
        )

    file = issue_file(issue)
    if "untranslated_preferred is true but gloss_on_first_occurrence is missing" in issue:
        return RepairDiagnostic(
            severity="warning",
            category=category,
            code="missing_untranslated_gloss",
            rule="Untranslated-preferred terms need a first-occurrence gloss",
            file=file,
            summary="`untranslated_preferred` is set without `gloss_on_first_occurrence`",
            why="Without a controlled first gloss, translators are left to invent their own onboarding language for the Pāli term.",
            fix="Add `gloss_on_first_occurrence` with the smallest helpful gloss for first mention.",
            examples=("terms/major/nibbana.json", "terms/major/sugata.json"),
        )

    if "stabilized drift-danger term must be a major entry" in issue:
        return RepairDiagnostic(
            severity="error",
            category=category,
            code="stabilized_term_not_major",
            rule="Stabilized drift-danger terms must remain major entries",
            file=file,
            summary="A stabilized high-risk term is not classified as `major`",
            why="Core drift-danger terms need a full rule-bearing surface, not a lightweight minor record.",
            fix="Promote the record back to `major` and keep its policy fields complete before merge.",
            examples=MAJOR_POLICY_EXAMPLES,
        )

    if "stabilized drift-danger term must be reviewed or stable" in issue:
        return RepairDiagnostic(
            severity="error",
            category=category,
            code="stabilized_term_status_too_low",
            rule="Stabilized drift-danger terms cannot drop below reviewed",
            file=file,
            summary="A stabilized high-risk term is below `reviewed` status",
            why="These headwords anchor doctrinal reuse and should not be treated as open-ended drafts without an explicit governance decision.",
            fix="Restore the status to `reviewed` or `stable`, or remove the term from the stabilized set only through an intentional governance change.",
            examples=STATUS_EXAMPLES,
        )

    if "stabilized drift-danger term must include rule-bearing notes" in issue:
        return RepairDiagnostic(
            severity="error",
            category=category,
            code="stabilized_term_missing_notes",
            rule="Stabilized drift-danger terms need policy-bearing notes",
            file=file,
            summary="A stabilized high-risk term is missing rule-bearing notes",
            why="These terms need explicit prose explaining the default and the drift risk they protect against.",
            fix="Add a policy-bearing `notes` block that explains the house default, the main contrast, and the drift risk.",
            examples=field_examples("notes"),
        )

    if "stabilized drift-danger term must include non-empty" in issue:
        field = issue.rsplit(" ", 1)[-1]
        snippet = field_snippet(field)
        fix = f"Populate `{field}` with a non-empty value."
        if snippet:
            fix += f" Minimal compliant shape: {snippet}"
        return RepairDiagnostic(
            severity="error",
            category=category,
            code="stabilized_term_missing_field",
            rule="Stabilized drift-danger terms need the full rule surface",
            file=file,
            summary=f"A stabilized high-risk term is missing non-empty `{field}`",
            why="Core drift-danger terms are not safe to reuse unless the full governing surface is present.",
            fix=fix,
            examples=field_examples(field),
        )

    if "stabilized drift-danger term must include at least two context_rules" in issue:
        return RepairDiagnostic(
            severity="error",
            category=category,
            code="stabilized_term_context_rules_too_thin",
            rule="Stabilized drift-danger terms need more than one recorded context",
            file=file,
            summary="The record has fewer than two `context_rules`",
            why="High-risk doctrinal terms need explicit coverage of the default plus at least one governed contrast or exception.",
            fix="Add another controlled context rule or demote the term until the family review is complete.",
            examples=field_examples("context_rules"),
        )

    if "untranslated-preferred policy should explain leave_untranslated_when" in issue:
        return RepairDiagnostic(
            severity="error",
            category=category,
            code="missing_leave_untranslated_when",
            rule="Untranslated-preferred major terms need an explicit untranslated scope",
            file=file,
            summary="`translation_policy` is missing `leave_untranslated_when`",
            why="Without that scope note, contributors cannot tell when the Pāli should remain visible instead of being translated.",
            fix="Add `leave_untranslated_when` describing the specific contexts where leaving the term in Pāli is still preferred.",
            examples=("terms/major/nibbana.json", "terms/major/sugata.json"),
        )

    if "major entry with translation_policy should include default_scope" in issue:
        return RepairDiagnostic(
            severity="error",
            category=category,
            code="missing_default_scope",
            rule="Major-entry `translation_policy` needs `default_scope`",
            file=file,
            summary="`translation_policy.default_scope` is missing",
            why="Without a default scope, the repo cannot tell contributors where the preferred rendering is meant to govern.",
            fix=f"Add `default_scope` as a non-empty string. Minimal compliant shape: {field_snippet('translation_policy')}",
            examples=field_examples("translation_policy"),
        )

    if "major entry with translation_policy should include drift_risk" in issue:
        return RepairDiagnostic(
            severity="error",
            category=category,
            code="missing_drift_risk",
            rule="Major-entry `translation_policy` needs `drift_risk`",
            file=file,
            summary="`translation_policy.drift_risk` is missing",
            why="The drift-risk sentence tells later contributors what the record is protecting against.",
            fix=f"Add `drift_risk` as a non-empty string. Minimal compliant shape: {field_snippet('translation_policy')}",
            examples=field_examples("translation_policy"),
        )

    if "translation_policy sets compound_inheritance to inherit but notes/context_rules do not mention compounds" in issue:
        return RepairDiagnostic(
            severity="error",
            category=category,
            code="compound_inheritance_missing_note",
            rule="`compound_inheritance: inherit` must be explained explicitly",
            file=file,
            summary="The record claims compounds inherit the headword policy without explaining that inheritance",
            why="Compound inheritance is a governance decision, not a silent default.",
            fix="Either mention compounds directly in `notes` or `context_rules`, or change `compound_inheritance` to `case-by-case` if the family is not yet closed.",
            examples=("terms/major/sati.json", "docs/headword-compound-formula-policy.md"),
        )

    if "authority_basis is present but empty" in issue:
        return RepairDiagnostic(
            severity="error",
            category=category,
            code="empty_authority_basis",
            rule="`authority_basis` must contain real provenance",
            file=file,
            summary="`authority_basis` is present but empty",
            why="An empty provenance block claims support without actually recording any source or scope.",
            fix=f"Add at least one non-empty authority item. Minimal compliant shape: {field_snippet('authority_basis')}",
            examples=field_examples("authority_basis"),
        )

    if "authority_basis[" in issue and "is not reflected in notes" in issue:
        return RepairDiagnostic(
            severity="error",
            category=category,
            code="authority_basis_not_reflected_in_notes",
            file=file,
            rule="Authority claims must be visible in the note",
            summary="An `authority_basis` source is not named or reflected in `notes`",
            why="If the note does not surface the provenance, later editors cannot audit why the current policy exists.",
            fix="Revise the note so it reflects the cited source and the specific part of the policy that source supports.",
            examples=field_examples("authority_basis"),
        )

    if "generic authority_basis source 'Repository editorial record'" in issue:
        return RepairDiagnostic(
            severity="error",
            category=category,
            code="generic_authority_basis",
            file=file,
            rule="Reviewed and stable majors cannot keep placeholder provenance",
            summary="The record still uses generic placeholder authority",
            why="Placeholder provenance is not strong enough for a reusable governed default.",
            fix="Replace the placeholder with specific source entries describing what authority supports the preferred translation, context rules, or rationale.",
            examples=field_examples("authority_basis"),
        )

    return RepairDiagnostic(
        severity="error",
        category=category,
        code="lint_issue",
        file=file,
        rule=f"{category} rule failed",
        summary=issue,
        why="This lint rule blocks merge because the live record is not explicit enough for governed reuse.",
        fix="Repair the record in the smallest safe way that satisfies the rule above, then rerun `python scripts/lint_terms.py --strict`.",
        examples=MAJOR_POLICY_EXAMPLES if category != "Reciprocal Links" else RELATIONSHIP_EXAMPLES,
    )


def collect_lint_diagnostics(
    terms: dict[str, dict[str, object]],
    *,
    enforce_stabilized_terms: bool = True,
) -> tuple[list[RepairDiagnostic], list[RepairDiagnostic]]:
    errors, warnings = collect_lint_results(
        terms,
        enforce_stabilized_terms=enforce_stabilized_terms,
    )
    error_diagnostics: list[RepairDiagnostic] = []
    warning_diagnostics: list[RepairDiagnostic] = []

    for category, issues in errors.items():
        for issue in issues:
            error_diagnostics.append(build_lint_diagnostic(category, issue))
    for category, issues in warnings.items():
        for issue in issues:
            warning_diagnostics.append(build_lint_diagnostic(category, issue))

    return error_diagnostics, warning_diagnostics


def collect_lint_results(
    terms: dict[str, dict[str, object]],
    *,
    enforce_stabilized_terms: bool = True,
) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    errors = defaultdict(list)
    warnings = defaultdict(list)

    resolution_issues = check_missing_related_terms(terms)
    reciprocal_issues = check_one_way_related_terms(terms)
    reference_issues = check_missing_sutta_references(terms)
    example_source_issues = check_missing_example_sources(terms)
    gloss_issues = check_untranslated_preferences(terms)
    thin_governance_issues = check_thin_governance_surfaces(terms)
    major_rule_note_issues = check_major_rule_note_quality(terms)
    placeholder_issues = check_suspicious_placeholders(terms)
    mojibake_issues = check_mojibake_patterns(terms)
    stabilized_term_issues = (
        check_stabilized_term_policy(terms) if enforce_stabilized_terms else []
    )
    translation_policy_issues = check_translation_policy_consistency(terms)
    high_load_minor_policy_issues = check_high_load_minor_translation_policy(terms)
    authority_basis_issues = check_authority_basis_consistency(terms)
    generic_authority_issues = check_generic_authority_basis_refinement(terms)
    status_discipline_issues = check_stable_status_discipline(terms)

    if resolution_issues:
        errors["Resolution"].extend(resolution_issues)
    if major_rule_note_issues:
        errors["Rule Coverage"].extend(major_rule_note_issues)
    if placeholder_issues:
        errors["Encoding"].extend(placeholder_issues)
    if mojibake_issues:
        errors["Encoding"].extend(mojibake_issues)
    if stabilized_term_issues:
        errors["Stabilized Terms"].extend(stabilized_term_issues)
    if translation_policy_issues:
        errors["Translation Policy"].extend(translation_policy_issues)
    if authority_basis_issues:
        errors["Authority Basis"].extend(authority_basis_issues)
    if generic_authority_issues:
        errors["Authority Basis"].extend(generic_authority_issues)
    if status_discipline_issues:
        errors["Status Discipline"].extend(status_discipline_issues)
    if reciprocal_issues:
        warnings["Reciprocal Links"].extend(reciprocal_issues)
    if reference_issues:
        warnings["References"].extend(reference_issues)
    if example_source_issues:
        warnings["Example Sources"].extend(example_source_issues)
    if thin_governance_issues:
        warnings["Governance Surface"].extend(thin_governance_issues)
    if high_load_minor_policy_issues:
        warnings["Minor Governance"].extend(high_load_minor_policy_issues)
    if gloss_issues:
        warnings["Glossing"].extend(gloss_issues)

    return dict(errors), dict(warnings)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a JSON report with actionable repair guidance.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on warnings as well as errors.",
    )
    args = parser.parse_args()

    if not TERMS_DIR.exists():
        print(f"ERROR: Terms directory not found: {TERMS_DIR}")
        return 1

    terms = load_terms()
    if not terms:
        print("WARNING: No term files found in terms/")
        return 0

    errors, warnings = collect_lint_diagnostics(terms)

    if args.json:
        payload = {
            "term_files": len(terms),
            "errors": diagnostics_as_json(errors),
            "warnings": diagnostics_as_json(warnings),
        }
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        if errors:
            print("Editorial lint failed:\n")
            print_diagnostics("Errors", errors)
        if warnings:
            print("Editorial lint warnings:\n")
            print_diagnostics("Warnings", warnings)
        if not errors and not warnings:
            print(f"Editorial lint passed for {len(terms)} term file(s).")

    if errors:
        return 1

    if warnings:
        if args.strict:
            return 1
        print(f"Completed with {len(warnings)} warning(s).")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
