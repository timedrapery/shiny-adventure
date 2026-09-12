"""Server-side validation of a feedback submission.

The reader script is one client, but nothing here trusts it. Every field is
checked for type, shape, and length; text is kept verbatim apart from control
characters, and is escaped only at render time.
"""

from __future__ import annotations

import re
from typing import Any

TARGETS = ("translation", "glossary", "introduction", "comprehension")
CATEGORIES = ("word", "sentence", "background", "awkward", "other")
RATINGS = ("yes", "partly", "no")
BASES = ("explicit", "glossary")
MAPPINGS = ("mapped", "unmapped")
INTRO_KINDS = ("guide", "intro", "default")
FAMILIARITY = ("new", "some", "very", "undisclosed")
EDITORIAL_STATUSES = ("draft", "approved")

CLIENT_ID_RE = re.compile(r"^[A-Za-z0-9._:-]{8,64}$")
SURFACE_KEY_RE = re.compile(r"^[a-z0-9_]{1,32}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SHORT_HASH_RE = re.compile(r"^[0-9a-f]{8,16}$")
PASSAGE_ID_RE = re.compile(r"^p\d{3,}$")
TERM_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}$")
QUESTION_ID_RE = re.compile(r"^[a-z][a-z0-9-]{0,39}$")
SESSION_CODE_RE = re.compile(r"^[A-Za-z0-9-]{4,32}$")
PARTICIPANT_RE = re.compile(r"^[A-Za-z0-9-]{1,32}$")
EMAIL_RE = re.compile(r"^[^\s@]{1,120}@[^\s@]{1,80}$")
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

LIMITS = {
    "passage_text": 4000,
    "comment": 2000,
    "glossary_comment": 1000,
    "answer": 2000,
    "glossary_term": 120,
    "page_path": 200,
    "surface_label": 40,
    "section": 200,
    "max_terms": 40,
    "max_answers": 10,
    "max_glossary_versions": 60,
}


class ValidationError(ValueError):
    def __init__(self, field: str, message: str) -> None:
        super().__init__(f"{field}: {message}")
        self.field = field
        self.message = message


def clean_text(value: Any, field: str, limit: int, required: bool = False) -> str:
    if value is None:
        value = ""
    if not isinstance(value, str):
        raise ValidationError(field, "must be text")
    text = CONTROL_RE.sub("", value).replace("\r\n", "\n").strip()
    if required and not text:
        raise ValidationError(field, "is required")
    if len(text) > limit:
        raise ValidationError(field, f"must be at most {limit} characters")
    return text


def _choice(value: Any, field: str, choices: tuple[str, ...], required: bool = True) -> str | None:
    if value is None or value == "":
        if required:
            raise ValidationError(field, "is required")
        return None
    if not isinstance(value, str) or value not in choices:
        raise ValidationError(field, f"must be one of {', '.join(choices)}")
    return value


def _pattern(value: Any, field: str, pattern: re.Pattern[str], required: bool = True) -> str | None:
    if value is None or value == "":
        if required:
            raise ValidationError(field, "is required")
        return None
    if not isinstance(value, str) or not pattern.match(value):
        raise ValidationError(field, "has an unexpected format")
    return value


def _terms(value: Any) -> list[dict[str, str]]:
    if value is None:
        return []
    if not isinstance(value, list) or len(value) > LIMITS["max_terms"]:
        raise ValidationError("terms", "must be a short list")
    terms: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, dict):
            raise ValidationError("terms", "entries must be objects")
        ident = _pattern(item.get("id"), "terms.id", TERM_ID_RE)
        basis = _choice(item.get("basis"), "terms.basis", BASES)
        if ident in seen:
            continue
        seen.add(ident)
        terms.append({"id": ident, "basis": basis})
    return terms


def _glossary_versions(value: Any) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict) or len(value) > LIMITS["max_glossary_versions"]:
        raise ValidationError("glossary_versions", "must be a small object")
    cleaned: dict[str, str] = {}
    for term, version in value.items():
        if not isinstance(term, str) or len(term) > LIMITS["glossary_term"]:
            raise ValidationError("glossary_versions", "term names must be short text")
        cleaned[term] = _pattern(version, "glossary_versions", SHORT_HASH_RE)
    return cleaned


def validate_submission(payload: Any, *, contact_enabled: bool = False) -> dict[str, Any]:
    """Return a normalized submission, or raise ValidationError.

    The result has three parts: `record` (columns for the submissions table
    except session resolution), `terms`, `session` (code and participant or
    None), `contact` (or None), and `honeypot` (True when the hidden field was
    filled, in which case the caller pretends to accept and stores nothing).
    """
    if not isinstance(payload, dict):
        raise ValidationError("payload", "must be a JSON object")
    if payload.get("manifest_format") != 1:
        raise ValidationError("manifest_format", "is not supported")
    target = _choice(payload.get("target"), "target", TARGETS)
    record: dict[str, Any] = {
        "client_submission_id": _pattern(payload.get("client_submission_id"), "client_submission_id", CLIENT_ID_RE),
        "target": target,
        "surface_key": _pattern(payload.get("surface_key"), "surface_key", SURFACE_KEY_RE),
        "surface_label": clean_text(payload.get("surface_label"), "surface_label", LIMITS["surface_label"]),
        "page_path": clean_text(payload.get("page_path"), "page_path", LIMITS["page_path"]),
        "body_sha256": _pattern(payload.get("body_sha256"), "body_sha256", SHA256_RE),
        "introduction_version": _pattern(payload.get("introduction_version"), "introduction_version", SHORT_HASH_RE, required=False),
        "comment": "",
    }
    terms: list[dict[str, str]] = []

    if target == "translation":
        record.update({
            "passage_id": _pattern(payload.get("passage_id"), "passage_id", PASSAGE_ID_RE),
            "passage_fingerprint": _pattern(payload.get("passage_fingerprint"), "passage_fingerprint", SHORT_HASH_RE),
            "passage_section": clean_text(payload.get("passage_section"), "passage_section", LIMITS["section"]),
            "passage_text": clean_text(payload.get("passage_text"), "passage_text", LIMITS["passage_text"], required=True),
            "category": _choice(payload.get("category"), "category", CATEGORIES),
            "comment": clean_text(payload.get("comment"), "comment", LIMITS["comment"]),
            "mapping": _choice(payload.get("mapping"), "mapping", MAPPINGS, required=False) or "unmapped",
        })
        terms = _terms(payload.get("terms"))
        record["glossary_versions_json"] = _json(_glossary_versions(payload.get("glossary_versions")))
    elif target == "introduction":
        record.update({
            "introduction_kind": _choice(payload.get("introduction_kind"), "introduction_kind", INTRO_KINDS, required=False),
            "passage_text": clean_text(payload.get("passage_text"), "passage_text", LIMITS["passage_text"]),
            "category": _choice(payload.get("category"), "category", CATEGORIES),
            "comment": clean_text(payload.get("comment"), "comment", LIMITS["comment"]),
            "mapping": "unmapped",
        })
    elif target == "glossary":
        record.update({
            "glossary_term": clean_text(payload.get("glossary_term"), "glossary_term", LIMITS["glossary_term"], required=True),
            "glossary_version": _pattern(payload.get("glossary_version"), "glossary_version", SHORT_HASH_RE),
            "passage_text": clean_text(payload.get("passage_text"), "passage_text", LIMITS["passage_text"]),
            "rating": _choice(payload.get("rating"), "rating", RATINGS),
            "comment": clean_text(payload.get("comment"), "comment", LIMITS["glossary_comment"]),
            "mapping": _choice(payload.get("mapping"), "mapping", MAPPINGS, required=False) or "unmapped",
        })
        terms = _terms(payload.get("terms"))
    else:  # comprehension
        version = payload.get("question_version")
        if not isinstance(version, int) or isinstance(version, bool) or version < 1:
            raise ValidationError("question_version", "must be a positive integer")
        answers = payload.get("answers")
        if not isinstance(answers, dict) or not answers or len(answers) > LIMITS["max_answers"]:
            raise ValidationError("answers", "must be an object with one to ten answers")
        cleaned: dict[str, str] = {}
        for key, value in answers.items():
            _pattern(key, "answers", QUESTION_ID_RE)
            cleaned[key] = clean_text(value, f"answers.{key}", LIMITS["answer"])
        if not any(cleaned.values()):
            raise ValidationError("answers", "at least one answer is required")
        record.update({
            "question_version": version,
            "question_set_sha256": _pattern(payload.get("question_set_sha256"), "question_set_sha256", SHA256_RE),
            "question_editorial_status": _choice(payload.get("question_editorial_status"), "question_editorial_status", EDITORIAL_STATUSES),
            "answers_json": _json(cleaned),
            "familiarity": _choice(payload.get("familiarity"), "familiarity", FAMILIARITY, required=False),
        })

    session = None
    raw_session = payload.get("session")
    if raw_session is not None:
        if not isinstance(raw_session, dict):
            raise ValidationError("session", "must be an object")
        session = {
            "code": _pattern(raw_session.get("code"), "session.code", SESSION_CODE_RE),
            "participant": _pattern(raw_session.get("participant"), "session.participant", PARTICIPANT_RE),
        }

    contact = None
    raw_contact = payload.get("contact")
    if raw_contact is not None and raw_contact != {}:
        if not contact_enabled:
            raise ValidationError("contact", "is not accepted by this service")
        if not isinstance(raw_contact, dict):
            raise ValidationError("contact", "must be an object")
        email = clean_text(raw_contact.get("email"), "contact.email", 200)
        if email:
            if not EMAIL_RE.match(email):
                raise ValidationError("contact.email", "does not look like an email address")
            if raw_contact.get("consent") is not True:
                raise ValidationError("contact.consent", "is required to store an email address")
            contact = {"email": email}

    honeypot = bool(clean_text(payload.get("website"), "website", 500))
    return {"record": record, "terms": terms, "session": session, "contact": contact, "honeypot": honeypot}


def _json(value: Any) -> str:
    import json

    return json.dumps(value, ensure_ascii=False, sort_keys=True)
