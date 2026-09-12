#!/usr/bin/env python3
"""Reader feedback inputs: site config, term maps, comprehension questions.

The reader generator embeds a feedback manifest on each enabled sutta page.
Everything the manifest carries comes from authoritative inputs under
`includes/feedback/`:

  config.json                  which surfaces are enabled, the submission
                               endpoint, and the reader-facing note
  paragraph-ids/<surface>.json stable passage ids (scripts/paragraph_ids.py)
  term-maps/<surface>.json     editor-written passage -> governed term ids
  comprehension/<surface>.json versioned comprehension question sets

This module loads and validates those inputs and builds the manifest. It
never touches the submission service; the service stores what a page sends
and the maintainer queue reads the version fields recorded here.

    python scripts/reader_feedback.py --check
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

try:
    from scripts import paragraph_ids
    from scripts.surface_registry import REPO_ROOT, TRANSLATION_SURFACES
except ModuleNotFoundError:  # invoked as a script from the repo root
    import paragraph_ids  # type: ignore[no-redef]
    from surface_registry import REPO_ROOT, TRANSLATION_SURFACES  # type: ignore[no-redef]


FEEDBACK_DIR = REPO_ROOT / "includes" / "feedback"
CONFIG_PATH = FEEDBACK_DIR / "config.json"
TERM_MAP_DIR = FEEDBACK_DIR / "term-maps"
QUESTION_DIR = FEEDBACK_DIR / "comprehension"
TERMS_DIR = REPO_ROOT / "terms"

MANIFEST_FORMAT = 1
MANIFEST_ELEMENT_ID = "reader-feedback-manifest"

# The category codes a passage-feedback submission may carry. The service
# validates against the same list; the labels live in the reader script.
FEEDBACK_CATEGORIES = ("word", "sentence", "background", "awkward", "other")
FEEDBACK_TARGETS = ("translation", "glossary", "introduction", "comprehension")
GLOSSARY_RATINGS = ("yes", "partly", "no")
QUESTION_ROLES = ("paraphrase", "specific", "reread")
EDITORIAL_STATUSES = ("draft", "approved")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

DEFAULT_READER_NOTE = (
    "Feedback goes to the editors of this translation. It is used to find "
    "wording that is hard to follow and to decide what to revise. It is not "
    "published, it is not linked to you, and it never changes a translation "
    "by itself."
)


def short_hash(text: str, length: int = 12) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def _canonical(data: Any) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


# --------------------------------------------------------------------------
# config
# --------------------------------------------------------------------------

def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    if not path.is_file():
        return {"endpoint": None, "enabled_surfaces": [], "contact_optin": False,
                "reader_note": DEFAULT_READER_NOTE}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("feedback config must be a JSON object")
    data.setdefault("endpoint", None)
    data.setdefault("enabled_surfaces", [])
    data.setdefault("contact_optin", False)
    data.setdefault("reader_note", DEFAULT_READER_NOTE)
    return data


def config_problems(data: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    keys = {surface.key for surface in TRANSLATION_SURFACES}
    endpoint = data.get("endpoint")
    if endpoint is not None:
        if not isinstance(endpoint, str) or not re.match(r"^https?://[^\s/]+", endpoint):
            problems.append("config: endpoint must be null or an http(s) origin")
        elif endpoint.endswith("/"):
            problems.append("config: endpoint must not end with a slash")
    enabled = data.get("enabled_surfaces")
    if not isinstance(enabled, list) or any(not isinstance(k, str) for k in enabled):
        problems.append("config: enabled_surfaces must be a list of surface keys")
    else:
        for key in enabled:
            if key not in keys:
                problems.append(f"config: enabled surface {key!r} is not registered")
        if len(set(enabled)) != len(enabled):
            problems.append("config: enabled_surfaces contains duplicates")
    if not isinstance(data.get("contact_optin"), bool):
        problems.append("config: contact_optin must be true or false")
    note = data.get("reader_note")
    if not isinstance(note, str) or not note.strip():
        problems.append("config: reader_note must be a nonempty string")
    return problems


def enabled_surfaces(config: dict[str, Any] | None = None) -> list[str]:
    config = config if config is not None else load_config()
    return [key for key in config.get("enabled_surfaces", []) if isinstance(key, str)]


# --------------------------------------------------------------------------
# governed term ids
# --------------------------------------------------------------------------

def known_term_ids(terms_dir: Path = TERMS_DIR) -> set[str]:
    if not terms_dir.is_dir():
        return set()
    return {path.stem for path in terms_dir.rglob("*.json")}


# --------------------------------------------------------------------------
# term maps
# --------------------------------------------------------------------------

def term_map_path(key: str, term_map_dir: Path = TERM_MAP_DIR) -> Path:
    return term_map_dir / f"{key}.json"


def load_term_map(key: str, term_map_dir: Path = TERM_MAP_DIR) -> dict[str, Any] | None:
    path = term_map_path(key, term_map_dir)
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: term map must be a JSON object")
    return data


def term_map_problems(
    key: str,
    data: dict[str, Any],
    passage_ids: set[str],
    term_ids: set[str],
) -> list[str]:
    label = f"{key} term map"
    problems: list[str] = []
    if data.get("surface_key") != key:
        problems.append(f"{label}: surface_key must be {key!r}")
    if not isinstance(data.get("basis"), str) or not str(data.get("basis")).strip():
        problems.append(f"{label}: basis must explain where the mappings come from")
    mappings = data.get("mappings")
    if not isinstance(mappings, dict):
        return problems + [f"{label}: mappings must be an object keyed by passage id"]
    for passage_id, terms in mappings.items():
        if passage_id not in passage_ids:
            problems.append(f"{label}: {passage_id} is not a current passage id")
        if not isinstance(terms, list) or not terms or any(not isinstance(t, str) for t in terms):
            problems.append(f"{label}: {passage_id} must list one or more term ids")
            continue
        if len(set(terms)) != len(terms):
            problems.append(f"{label}: {passage_id} lists a term twice")
        for term in terms:
            if term not in term_ids:
                problems.append(f"{label}: {passage_id} names unknown term {term!r}")
    return problems


# --------------------------------------------------------------------------
# comprehension question sets
# --------------------------------------------------------------------------

def question_set_path(key: str, question_dir: Path = QUESTION_DIR) -> Path:
    return question_dir / f"{key}.json"


def load_question_set(key: str, question_dir: Path = QUESTION_DIR) -> dict[str, Any] | None:
    path = question_set_path(key, question_dir)
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: question set must be a JSON object")
    return data


def question_set_sha256(data: dict[str, Any]) -> str:
    """A content version of what a reader is actually shown."""
    shown = {
        "intro": data.get("intro"),
        "questions": data.get("questions"),
        "familiarity": data.get("familiarity"),
    }
    return hashlib.sha256(_canonical(shown).encode("utf-8")).hexdigest()


def question_set_problems(key: str, data: dict[str, Any]) -> list[str]:
    label = f"{key} comprehension questions"
    problems: list[str] = []
    if data.get("surface_key") != key:
        problems.append(f"{label}: surface_key must be {key!r}")
    version = data.get("version")
    if not isinstance(version, int) or version < 1:
        problems.append(f"{label}: version must be a positive integer")
    status = data.get("editorial_status")
    if status not in EDITORIAL_STATUSES:
        problems.append(f"{label}: editorial_status must be draft or approved")
    drafted = data.get("drafted_on")
    if not isinstance(drafted, str) or not DATE_RE.match(drafted):
        problems.append(f"{label}: drafted_on must be YYYY-MM-DD")
    approved_on = data.get("approved_on")
    evidence = data.get("approval_evidence")
    if status == "approved":
        if not isinstance(approved_on, str) or not DATE_RE.match(approved_on):
            problems.append(f"{label}: approved questions need approved_on")
        if not isinstance(evidence, str) or not evidence.strip():
            problems.append(f"{label}: approved questions need approval_evidence")
        elif not (REPO_ROOT / evidence).is_file():
            problems.append(f"{label}: approval_evidence must name a repository file")
    else:
        if approved_on is not None or evidence is not None:
            problems.append(f"{label}: draft questions must not carry approval fields")
    if not isinstance(data.get("intro"), str) or not str(data.get("intro")).strip():
        problems.append(f"{label}: intro must be a nonempty string")
    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        return problems + [f"{label}: questions must be a nonempty list"]
    roles: list[str] = []
    ids: list[str] = []
    for item in questions:
        if not isinstance(item, dict):
            problems.append(f"{label}: each question must be an object")
            continue
        ident = item.get("id")
        if not isinstance(ident, str) or not re.match(r"^[a-z][a-z0-9-]*$", ident):
            problems.append(f"{label}: question id {ident!r} must be lowercase-kebab")
        else:
            ids.append(ident)
        role = item.get("role")
        if role not in QUESTION_ROLES:
            problems.append(f"{label}: question role {role!r} is not one of {QUESTION_ROLES}")
        else:
            roles.append(role)
        if not isinstance(item.get("prompt"), str) or not str(item.get("prompt")).strip():
            problems.append(f"{label}: question {ident!r} needs a prompt")
    if len(set(ids)) != len(ids):
        problems.append(f"{label}: question ids must be unique")
    for role in QUESTION_ROLES:
        if roles.count(role) != 1:
            problems.append(f"{label}: exactly one question must have role {role!r}")
    familiarity = data.get("familiarity")
    if not isinstance(familiarity, dict) or not isinstance(familiarity.get("ask"), bool):
        problems.append(f"{label}: familiarity.ask must be true or false")
    elif familiarity["ask"]:
        options = familiarity.get("options")
        if (not isinstance(options, list) or len(options) < 2 or any(
                not isinstance(o, dict) or not isinstance(o.get("value"), str)
                or not isinstance(o.get("label"), str) for o in options)):
            problems.append(f"{label}: familiarity options need value and label")
        if not isinstance(familiarity.get("prompt"), str):
            problems.append(f"{label}: familiarity prompt is required when asked")
    guidance = data.get("assessment_guidance")
    if not isinstance(guidance, dict):
        problems.append(f"{label}: assessment_guidance must be an object")
    else:
        for field in ("paraphrase", "reread"):
            if not isinstance(guidance.get(field), str) or not str(guidance.get(field)).strip():
                problems.append(f"{label}: assessment_guidance.{field} is required")
        specific = guidance.get("specific")
        if not isinstance(specific, dict) or not isinstance(specific.get("accept"), list) \
                or not specific.get("accept"):
            problems.append(f"{label}: assessment_guidance.specific.accept must list accepted answers")
        elif not isinstance(specific.get("not_required"), str):
            problems.append(f"{label}: assessment_guidance.specific.not_required must say what is not needed")
    return problems


# --------------------------------------------------------------------------
# manifest
# --------------------------------------------------------------------------

def build_manifest(
    *,
    surface,
    reader_title: str,
    body_sha256: str,
    page_path: str,
    passages: list[paragraph_ids.Passage],
    passage_map: dict[str, Any],
    explicit_terms: dict[str, list[str]],
    derived_terms: dict[str, list[str]],
    glossary_entries: list[tuple[str, str]],
    glossary_term_ids: dict[str, str],
    introduction_kind: str,
    introduction_text: str,
    question_set: dict[str, Any] | None,
    config: dict[str, Any],
) -> dict[str, Any]:
    """Assemble the manifest embedded on an enabled sutta page.

    `explicit_terms` come from the editor-written term map and `derived_terms`
    from the page's words-used panel (a glossary rendering that occurs in the
    passage as a whole phrase and equals a governed preferred rendering). The
    two are kept apart on every passage so a maintainer can see the basis.
    """
    ids = [entry["id"] for entry in passage_map["passages"]]
    if len(ids) != len(passages) or any(
        entry["fingerprint"] != passage.fingerprint
        for entry, passage in zip(passage_map["passages"], passages)
    ):
        raise ValueError(
            f"{surface.key}: paragraph map is stale; run "
            "`python scripts/paragraph_ids.py --write`"
        )
    passage_items = []
    for entry, passage in zip(passage_map["passages"], passages):
        terms = [{"id": t, "basis": "explicit"} for t in explicit_terms.get(entry["id"], [])]
        seen = {t["id"] for t in terms}
        for term_id in derived_terms.get(entry["id"], []):
            if term_id not in seen:
                terms.append({"id": term_id, "basis": "glossary"})
                seen.add(term_id)
        passage_items.append({
            "id": entry["id"],
            "fingerprint": passage.fingerprint,
            "prefix": passage.normalized[:40],
            "section": passage.section,
            "terms": terms,
            "mapping": "mapped" if terms else "unmapped",
        })
    glossary = {
        term: {
            "version": short_hash(gloss),
            "term_id": glossary_term_ids.get(term),
        }
        for term, gloss in glossary_entries
    }
    comprehension = None
    if question_set is not None:
        comprehension = {
            "version": question_set["version"],
            "sha256": question_set_sha256(question_set),
            "editorial_status": question_set["editorial_status"],
            "intro": question_set["intro"],
            "questions": [
                {"id": q["id"], "role": q["role"], "prompt": q["prompt"]}
                for q in question_set["questions"]
            ],
            "familiarity": question_set["familiarity"] if question_set["familiarity"].get("ask") else None,
        }
    return {
        "format": MANIFEST_FORMAT,
        "surface_key": surface.key,
        "surface_label": surface.label,
        "reader_title": reader_title,
        "page_path": page_path,
        "body_sha256": body_sha256,
        "endpoint": config.get("endpoint"),
        "contact_optin": bool(config.get("contact_optin", False)),
        "reader_note": config.get("reader_note", DEFAULT_READER_NOTE),
        "categories": list(FEEDBACK_CATEGORIES),
        "passages": passage_items,
        "glossary": glossary,
        "introduction": {
            "kind": introduction_kind,
            "version": short_hash(introduction_text),
        },
        "comprehension": comprehension,
    }


def manifest_script(manifest: dict[str, Any]) -> str:
    """The manifest as a raw HTML block safe to embed in Markdown."""
    text = json.dumps(manifest, ensure_ascii=False, sort_keys=True)
    # `</script>` inside a JSON string would end the element early; `<` is
    # never needed literally in JSON, so escape every instance.
    text = text.replace("<", "\\u003c")
    return f'<script type="application/json" id="{MANIFEST_ELEMENT_ID}">{text}</script>'


# --------------------------------------------------------------------------
# check
# --------------------------------------------------------------------------

def check(
    config_path: Path = CONFIG_PATH,
    term_map_dir: Path = TERM_MAP_DIR,
    question_dir: Path = QUESTION_DIR,
    map_dir: Path = paragraph_ids.MAP_DIR,
) -> list[str]:
    problems: list[str] = []
    try:
        config = load_config(config_path)
    except (json.JSONDecodeError, ValueError) as error:
        return [f"config: {error}"]
    problems.extend(config_problems(config))
    by_key = {surface.key: surface for surface in TRANSLATION_SURFACES}
    term_ids = known_term_ids()

    mapped = {path.stem for path in term_map_dir.glob("*.json")} if term_map_dir.is_dir() else set()
    questioned = {path.stem for path in question_dir.glob("*.json")} if question_dir.is_dir() else set()
    for key in sorted(mapped | questioned | set(enabled_surfaces(config))):
        if key not in by_key:
            problems.append(f"{key}: feedback input names an unregistered surface")
            continue
        passage_ids: set[str] = set()
        map_file = paragraph_ids.map_path(key, map_dir)
        if map_file.is_file():
            try:
                passage_ids = {e["id"] for e in paragraph_ids.load_map(map_file)["passages"]}
            except (json.JSONDecodeError, ValueError, KeyError, TypeError):
                problems.append(f"{key}: paragraph map is unreadable")
        elif key in mapped or key in enabled_surfaces(config):
            problems.append(f"{key}: needs a paragraph map before feedback inputs can be checked")
        if key in mapped:
            try:
                data = load_term_map(key, term_map_dir)
            except (json.JSONDecodeError, ValueError) as error:
                problems.append(f"{key} term map: {error}")
            else:
                problems.extend(term_map_problems(key, data or {}, passage_ids, term_ids))
        if key in questioned:
            try:
                data = load_question_set(key, question_dir)
            except (json.JSONDecodeError, ValueError) as error:
                problems.append(f"{key} comprehension questions: {error}")
            else:
                problems.extend(question_set_problems(key, data or {}))
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="Validate the feedback inputs.")
    parser.parse_args()
    problems = check()
    if problems:
        print("Reader feedback input check failed:\n")
        for problem in problems:
            print(f"- {problem}")
        return 1
    config = load_config()
    enabled = ", ".join(enabled_surfaces(config)) or "none"
    print(f"Reader feedback inputs are valid (enabled: {enabled}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
