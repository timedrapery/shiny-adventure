#!/usr/bin/env python3
"""Extract review candidates from Pali source texts without creating term entries."""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path

try:
    from scripts.text_utils import normalize_term
    from scripts.term_store import iter_term_files
except ModuleNotFoundError:
    from text_utils import normalize_term
    from term_store import iter_term_files


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
CANDIDATES_DIR = REPO_ROOT / "candidates"
MAX_SNIPPETS_PER_CANDIDATE = 3
MAX_PATHS_PER_CANDIDATE = 8
NGRAM_SIZES = (1, 2, 3)
DOCTRINAL_TAGS = {
    "core-doctrine",
    "core-practice",
    "context-sensitive",
    "translation-sensitive",
    "dependent-origination",
    "four-noble-truths",
    "liberation",
}
STOPWORDS = {
    "a",
    "atha",
    "api",
    "ayaṃ",
    "ayam",
    "ca",
    "ce",
    "eva",
    "hi",
    "idaṃ",
    "idam",
    "ime",
    "iti",
    "kho",
    "ma",
    "me",
    "na",
    "no",
    "nu",
    "pana",
    "pi",
    "so",
    "taṃ",
    "tam",
    "te",
    "ti",
    "tu",
    "va",
    "vā",
    "ya",
    "yaṃ",
    "yam",
    "ye",
    "yo",
}


@dataclass(frozen=True)
class SourceDocument:
    path: Path
    relative_path: str
    tokens: list[str]
    line_tokens: list[tuple[int, str]]


def is_word_char(char: str) -> bool:
    category = unicodedata.category(char)
    return category.startswith(("L", "M")) or char in {"-", "’", "'"}


def tokenize(text: str) -> list[str]:
    cleaned: list[str] = []
    for char in text:
        cleaned.append(char if is_word_char(char) else " ")
    tokens = []
    for raw_token in "".join(cleaned).split():
        token = raw_token.strip("-'’").casefold()
        if token:
            tokens.append(token)
    return tokens


def candidate_key(value: str) -> str:
    return normalize_term(value).replace("_", "").replace("-", "")


def is_edit_distance_at_most_one(left: str, right: str) -> bool:
    if left == right:
        return True
    if abs(len(left) - len(right)) > 1:
        return False
    if len(left) > len(right):
        left, right = right, left
    index_left = 0
    index_right = 0
    found_difference = False
    while index_left < len(left) and index_right < len(right):
        if left[index_left] == right[index_right]:
            index_left += 1
            index_right += 1
            continue
        if found_difference:
            return False
        found_difference = True
        if len(left) == len(right):
            index_left += 1
        index_right += 1
    return True


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_lexicon_index() -> dict[str, object]:
    exact_terms: dict[str, list[str]] = defaultdict(list)
    canonical_terms: dict[str, list[str]] = defaultdict(list)
    doctrinal_terms: set[str] = set()
    major_terms: set[str] = set()

    for path in iter_term_files(TERMS_DIR):
        data = load_json(path)
        if not isinstance(data, dict):
            continue
        stem = path.stem
        exact_terms[stem].append(stem)
        canonical_terms[candidate_key(stem)].append(stem)
        term = data.get("term")
        if isinstance(term, str):
            canonical_terms[candidate_key(term)].append(stem)
        if data.get("entry_type") == "major":
            major_terms.add(stem)
        tags = data.get("tags")
        if isinstance(tags, list) and DOCTRINAL_TAGS.intersection(tag for tag in tags if isinstance(tag, str)):
            doctrinal_terms.add(stem)

    return {
        "exact_terms": {key: sorted(set(value)) for key, value in exact_terms.items()},
        "canonical_terms": {key: sorted(set(value)) for key, value in canonical_terms.items()},
        "canonical_keys": sorted(canonical_terms),
        "doctrinal_terms": doctrinal_terms,
        "major_terms": major_terms,
    }


def gather_source_paths(inputs: list[str]) -> list[Path]:
    paths: list[Path] = []
    for raw_input in inputs:
        path = Path(raw_input)
        if path.is_dir():
            for extension in ("*.txt", "*.md"):
                paths.extend(sorted(path.rglob(extension)))
        elif path.is_file():
            paths.append(path)
        else:
            raise FileNotFoundError(f"Input path not found: {path}")
    return sorted(set(path.resolve() for path in paths))


def load_documents(paths: list[Path]) -> list[SourceDocument]:
    documents: list[SourceDocument] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        line_tokens: list[tuple[int, str]] = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            for token in tokenize(line):
                line_tokens.append((line_number, token))
        documents.append(
            SourceDocument(
                path=path,
                relative_path=str(path.relative_to(REPO_ROOT)) if path.is_relative_to(REPO_ROOT) else str(path),
                tokens=[token for _, token in line_tokens],
                line_tokens=line_tokens,
            )
        )
    return documents


def is_noise_token(token: str) -> bool:
    return len(candidate_key(token)) < 3 or token in STOPWORDS


def build_snippet(document: SourceDocument, start_index: int, size: int) -> dict[str, object]:
    window_start = max(0, start_index - 3)
    window_end = min(len(document.tokens), start_index + size + 3)
    snippet = " ".join(document.tokens[window_start:window_end])
    return {
        "path": document.relative_path,
        "line": document.line_tokens[start_index][0] if start_index < len(document.line_tokens) else 1,
        "snippet": snippet,
    }


def determine_priority(
    *,
    total_count: int,
    document_count: int,
    token_count: int,
    status: str,
    formula_signal: bool,
    doctrinal_signal: bool,
    variant_signal: bool,
    token_is_noise: bool,
) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if token_is_noise:
        return "ignore", ["common particle/pronoun or fragment"]
    if status == "covered":
        return "ignore", ["already covered in lexicon"]
    if variant_signal:
        reasons.append("possible spelling or normalization variant of an existing term")
    if formula_signal:
        reasons.append("appears in repeated multi-word expression")
    if doctrinal_signal:
        reasons.append("touches doctrinal or major-term vocabulary")
    if total_count >= 4:
        reasons.append("recurs frequently")
    if document_count >= 2:
        reasons.append("appears across multiple source files")
    if token_count > 1:
        reasons.append("compound or formula candidate")

    if variant_signal or (formula_signal and doctrinal_signal) or (doctrinal_signal and total_count >= 4):
        return "create_now", reasons or ["high doctrinal drift risk"]
    if doctrinal_signal or formula_signal or total_count >= 3 or document_count >= 2:
        return "review_soon", reasons or ["recurs enough to justify review"]
    return "low_priority", reasons or ["currently low-frequency unresolved vocabulary"]


def collect_candidates(documents: list[SourceDocument], lexicon_index: dict[str, object]) -> dict[str, object]:
    candidates: dict[str, dict[str, object]] = {}
    exact_terms: dict[str, list[str]] = lexicon_index["exact_terms"]  # type: ignore[assignment]
    canonical_terms: dict[str, list[str]] = lexicon_index["canonical_terms"]  # type: ignore[assignment]
    canonical_keys: list[str] = lexicon_index["canonical_keys"]  # type: ignore[assignment]
    doctrinal_terms: set[str] = lexicon_index["doctrinal_terms"]  # type: ignore[assignment]
    major_terms: set[str] = lexicon_index["major_terms"]  # type: ignore[assignment]

    for document in documents:
        seen_in_document: set[tuple[str, int]] = set()
        for size in NGRAM_SIZES:
            if len(document.tokens) < size:
                continue
            for start_index in range(0, len(document.tokens) - size + 1):
                terms = document.tokens[start_index : start_index + size]
                text = " ".join(terms)
                normalized = candidate_key(text)
                if not normalized:
                    continue

                token_is_noise = size == 1 and is_noise_token(text)
                matched_exact = exact_terms.get(normalized, [])
                matched_canonical = canonical_terms.get(normalized, [])
                matched_variant_terms: list[str] = []
                if not matched_canonical and size == 1 and len(normalized) >= 5:
                    for existing_key in canonical_keys:
                        if is_edit_distance_at_most_one(normalized, existing_key):
                            matched_variant_terms.extend(canonical_terms[existing_key])
                matched_major_terms = sorted(set(matched_canonical) & major_terms)
                doctrinal_signal = bool(set(matched_canonical) & doctrinal_terms) or any(
                    candidate_key(part) in canonical_terms and set(canonical_terms[candidate_key(part)]) & doctrinal_terms
                    for part in terms
                )
                formula_signal = size > 1 and (
                    len(matched_major_terms) > 0
                    or any(candidate_key(part) in canonical_terms for part in terms)
                )

                if matched_exact:
                    status = "covered"
                elif matched_canonical:
                    status = "variant_of_existing"
                elif matched_variant_terms:
                    status = "variant_of_existing"
                else:
                    status = "unresolved"

                record = candidates.setdefault(
                    normalized,
                    {
                        "text": text,
                        "normalized": normalized,
                        "token_count": size,
                        "total_count": 0,
                        "document_paths": set(),
                        "matched_terms": set(),
                        "matched_major_terms": set(),
                        "status": status,
                        "formula_signal": False,
                        "doctrinal_signal": False,
                        "noise": token_is_noise,
                        "snippets": [],
                    },
                )

                record["total_count"] += 1
                record["document_paths"].add(document.relative_path)
                record["matched_terms"].update(matched_canonical)
                record["matched_terms"].update(matched_variant_terms)
                record["matched_major_terms"].update(matched_major_terms)
                record["formula_signal"] = bool(record["formula_signal"] or formula_signal)
                record["doctrinal_signal"] = bool(record["doctrinal_signal"] or doctrinal_signal)
                record["noise"] = bool(record["noise"] and token_is_noise) if record["total_count"] > 1 else token_is_noise
                if status == "variant_of_existing" and record["status"] == "unresolved":
                    record["status"] = status

                doc_key = (normalized, start_index)
                if doc_key not in seen_in_document and len(record["snippets"]) < MAX_SNIPPETS_PER_CANDIDATE:
                    record["snippets"].append(build_snippet(document, start_index, size))
                    seen_in_document.add(doc_key)

    resolved_candidates: list[dict[str, object]] = []
    priority_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()

    for normalized, record in candidates.items():
        document_paths = sorted(record["document_paths"])[:MAX_PATHS_PER_CANDIDATE]
        matched_terms = sorted(record["matched_terms"])
        status = str(record["status"])
        priority, reasons = determine_priority(
            total_count=int(record["total_count"]),
            document_count=len(record["document_paths"]),
            token_count=int(record["token_count"]),
            status=status,
            formula_signal=bool(record["formula_signal"]),
            doctrinal_signal=bool(record["doctrinal_signal"]),
            variant_signal=status == "variant_of_existing",
            token_is_noise=bool(record["noise"]),
        )
        resolved = {
            "text": record["text"],
            "normalized": normalized,
            "token_count": record["token_count"],
            "total_count": record["total_count"],
            "document_count": len(record["document_paths"]),
            "document_paths": document_paths,
            "status": status,
            "matched_terms": matched_terms,
            "matched_major_terms": sorted(record["matched_major_terms"]),
            "formula_signal": record["formula_signal"],
            "doctrinal_signal": record["doctrinal_signal"],
            "priority": priority,
            "reasons": reasons,
            "snippets": record["snippets"],
        }
        resolved_candidates.append(resolved)
        priority_counts[priority] += 1
        status_counts[status] += 1

    resolved_candidates.sort(
        key=lambda item: (
            {"create_now": 0, "review_soon": 1, "low_priority": 2, "ignore": 3}[str(item["priority"])],
            -int(item["total_count"]),
            -int(item["document_count"]),
            -int(item["token_count"]),
            str(item["text"]),
        )
    )

    return {
        "source_documents": [document.relative_path for document in documents],
        "summary": {
            "documents": len(documents),
            "total_candidates": len(resolved_candidates),
            "priority_counts": dict(priority_counts),
            "status_counts": dict(status_counts),
        },
        "candidates": resolved_candidates,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "inputs",
        nargs="+",
        help="One or more source text files or directories.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=CANDIDATES_DIR / "candidate_terms.json",
        help="Where to write the JSON candidate report.",
    )
    args = parser.parse_args()

    try:
        input_paths = gather_source_paths(args.inputs)
        if not input_paths:
            print("ERROR: No source text files found.")
            return 1
        documents = load_documents(input_paths)
        report = collect_candidates(documents, load_lexicon_index())
    except (FileNotFoundError, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote candidate extraction report to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
