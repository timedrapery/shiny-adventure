#!/usr/bin/env python3
"""Validate spoken-voice source provenance for every registered surface."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    from scripts.surface_registry import TRANSLATION_SURFACES, TranslationSurface
except ModuleNotFoundError:
    from surface_registry import TRANSLATION_SURFACES, TranslationSurface


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_RELPATH = Path(
    "candidates/source-manifests/osf-spoken-translation-sources.json"
)
PROFILE = "osf-spoken-v1-pilot"
BODY_MARKER = "## Translation"

SOURCE_ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
KINDS = {
    "repo-document",
    "web-corpus",
    "web-transcript",
    "youtube-playlist",
    "youtube-video",
}
ROLES = {
    "governance",
    "primary-calibration",
    "surface-calibration",
    "editor-calibration",
}
TRANSCRIPT_STATUSES = {
    "not-applicable",
    "collection-index-checked",
    "playlist-index-checked",
    "page-checked",
    "automatic-captions-only",
    "speaker-turns-checked",
    "audio-checked",
}
RIGHTS_STATUSES = {
    "repo-owned",
    "public-reference",
    "user-authorized-calibration",
}
REVIEW_STATUSES = {"pilot", "approved"}
CALIBRATION_ROLES = ROLES - {"governance"}
FORBIDDEN_TEXT_FIELDS = {"transcript", "caption_text", "verbatim_text"}


def load_manifest(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("manifest root must be a JSON object")
    return data


def is_iso_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def normalized_translation_body(text: str) -> str:
    if BODY_MARKER not in text:
        raise ValueError(f"surface has no `{BODY_MARKER}` section")
    body = text.split(BODY_MARKER, 1)[1]
    return body.replace("\r\n", "\n").replace("\r", "\n").strip() + "\n"


def translation_body_sha256(path: Path) -> str:
    body = normalized_translation_body(path.read_text(encoding="utf-8"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def manifest_failures(
    manifest: dict[str, object], repo_root: Path
) -> tuple[list[str], dict[str, dict[str, object]]]:
    failures: list[str] = []
    if manifest.get("manifest_version") != "1.0":
        failures.append("manifest_version must be `1.0`")
    if manifest.get("profile") != PROFILE:
        failures.append(f"manifest profile must be `{PROFILE}`")
    if not is_iso_date(manifest.get("updated_on")):
        failures.append("manifest updated_on must be an ISO date")
    if not isinstance(manifest.get("storage_policy"), str):
        failures.append("manifest storage_policy must be a string")

    raw_sources = manifest.get("sources")
    if not isinstance(raw_sources, list) or not raw_sources:
        return failures + ["manifest sources must be a non-empty list"], {}

    sources: dict[str, dict[str, object]] = {}
    root = repo_root.resolve()
    required_strings = (
        "id",
        "kind",
        "role",
        "title",
        "speaker_scope",
        "transcript_status",
        "rights_status",
        "redistribution",
        "notes",
    )

    for index, raw_source in enumerate(raw_sources, start=1):
        prefix = f"sources[{index}]"
        if not isinstance(raw_source, dict):
            failures.append(f"{prefix} must be an object")
            continue
        source = raw_source
        source_id = source.get("id")
        if not isinstance(source_id, str) or not SOURCE_ID_RE.fullmatch(source_id):
            failures.append(f"{prefix}.id must use uppercase hyphenated source ID form")
            continue
        if source_id in sources:
            failures.append(f"duplicate source id `{source_id}`")
            continue
        sources[source_id] = source

        for field in required_strings:
            if not isinstance(source.get(field), str) or not str(source[field]).strip():
                failures.append(f"{source_id}: {field} must be a non-empty string")
        if source.get("kind") not in KINDS:
            failures.append(f"{source_id}: unknown kind `{source.get('kind')}`")
        if source.get("role") not in ROLES:
            failures.append(f"{source_id}: unknown role `{source.get('role')}`")
        if source.get("transcript_status") not in TRANSCRIPT_STATUSES:
            failures.append(
                f"{source_id}: unknown transcript_status "
                f"`{source.get('transcript_status')}`"
            )
        if source.get("rights_status") not in RIGHTS_STATUSES:
            failures.append(
                f"{source_id}: unknown rights_status `{source.get('rights_status')}`"
            )
        if source.get("redistribution") != "metadata-only":
            failures.append(f"{source_id}: pilot sources must be metadata-only")
        if not is_iso_date(source.get("checked_on")):
            failures.append(f"{source_id}: checked_on must be an ISO date")
        for forbidden in FORBIDDEN_TEXT_FIELDS:
            if forbidden in source:
                failures.append(
                    f"{source_id}: `{forbidden}` is forbidden; store metadata only"
                )

        url = source.get("url")
        transcript_url = source.get("transcript_url")
        repo_relpath = source.get("repo_relpath")
        if (isinstance(url, str)) == (isinstance(repo_relpath, str)):
            failures.append(
                f"{source_id}: provide exactly one of url or repo_relpath"
            )
        elif isinstance(url, str) and not url.startswith("https://"):
            failures.append(f"{source_id}: web source URL must use HTTPS")
        elif isinstance(repo_relpath, str):
            resolved = (repo_root / repo_relpath).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                failures.append(f"{source_id}: repo_relpath escapes the repository")
            else:
                if not resolved.is_file():
                    failures.append(
                        f"{source_id}: repo source does not exist: {repo_relpath}"
                    )
        if transcript_url is not None and (
            not isinstance(transcript_url, str)
            or not transcript_url.startswith("https://")
        ):
            failures.append(f"{source_id}: transcript_url must use HTTPS")

    return failures, sources


def review_failures(
    surfaces: tuple[TranslationSurface, ...],
    sources: dict[str, dict[str, object]],
    repo_root: Path,
) -> list[str]:
    failures: list[str] = []
    for surface in surfaces:
        review = surface.spoken_voice_review
        if review is None:
            failures.append(f"{surface.label}: missing spoken_voice_review")
            continue
        prefix = surface.label
        if review.profile != PROFILE:
            failures.append(f"{prefix}: spoken profile must be `{PROFILE}`")
        if review.status not in REVIEW_STATUSES:
            failures.append(f"{prefix}: unknown spoken review status `{review.status}`")
        if not is_iso_date(review.recorded_on):
            failures.append(f"{prefix}: recorded_on must be an ISO date")
        if not review.source_ids:
            failures.append(f"{prefix}: spoken review must cite sources")
            continue

        missing = [source_id for source_id in review.source_ids if source_id not in sources]
        for source_id in missing:
            failures.append(f"{prefix}: unknown spoken source id `{source_id}`")
        roles = {
            str(sources[source_id].get("role"))
            for source_id in review.source_ids
            if source_id in sources
        }
        if "governance" not in roles:
            failures.append(f"{prefix}: spoken review needs a governance source")
        if not roles.intersection(CALIBRATION_ROLES):
            failures.append(f"{prefix}: spoken review needs a calibration source")

        main_path = repo_root / surface.main_relpath
        notes_path = repo_root / surface.notes_relpath
        if not main_path.is_file():
            failures.append(f"{prefix}: translation surface is missing")
            continue
        if not SHA256_RE.fullmatch(review.body_sha256):
            failures.append(f"{prefix}: body_sha256 must be lowercase SHA-256")
        else:
            actual_hash = translation_body_sha256(main_path)
            if actual_hash != review.body_sha256:
                failures.append(
                    f"{prefix}: reviewed body hash is stale; expected {actual_hash}"
                )

        if not notes_path.is_file():
            failures.append(f"{prefix}: companion notes are missing")
            continue
        notes = notes_path.read_text(encoding="utf-8")
        if "## Spoken-Voice Review" not in notes:
            failures.append(f"{prefix}: notes need `## Spoken-Voice Review`")
        for source_id in review.source_ids:
            if source_id not in notes:
                failures.append(f"{prefix}: notes do not mention source `{source_id}`")
        if review.status == "approved":
            if "read-aloud review: complete" not in notes.casefold():
                failures.append(f"{prefix}: approval needs a complete read-aloud review")
            if "newcomer comprehension review: complete" not in notes.casefold():
                failures.append(
                    f"{prefix}: approval needs a complete newcomer comprehension review"
                )
    return failures


def collect_failures(
    repo_root: Path = REPO_ROOT,
    surfaces: tuple[TranslationSurface, ...] = TRANSLATION_SURFACES,
) -> list[str]:
    manifest_path = repo_root / MANIFEST_RELPATH
    if not manifest_path.is_file():
        return [f"missing source manifest: {MANIFEST_RELPATH.as_posix()}"]
    try:
        manifest = load_manifest(manifest_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [f"could not read source manifest: {error}"]
    failures, sources = manifest_failures(manifest, repo_root)
    failures.extend(review_failures(surfaces, sources, repo_root))
    return failures


def main() -> int:
    failures = collect_failures()
    if failures:
        print("Spoken-voice source check failed:\n")
        for failure in failures:
            print(f"- {failure}")
        return 1
    reviewed = sum(
        1 for surface in TRANSLATION_SURFACES if surface.spoken_voice_review is not None
    )
    print(f"Spoken-voice source check passed ({reviewed} reviewed surface(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
