#!/usr/bin/env python3
"""Report editorial health signals: coverage, drift, review latency, and check failures.

This is a reporting surface, not a gate. Every number here is derived from
repository content so the same commit always produces the same dashboard.

The four sections answer four standing questions:

- Coverage: how much of the Pali actually quoted in the corpus is governed?
- Drift: where do translation surfaces fight the term records?
- Review latency: what is waiting for an editorial decision, and since when?
- Check failures: how often did schema and lint break, week by week?

Live day counts (how many days something has waited) belong to the CLI and the
JSON snapshot, not to the committed Markdown. The Markdown records absolute
dates instead, so `scripts/check_generated_docs.py` can compare it byte for
byte without the file going stale every midnight.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from functools import lru_cache
from datetime import date, datetime
from pathlib import Path

try:
    from scripts.repo_health import (
        collect_governed_rendering_drift,
        load_translation_declarations,
    )
    from scripts.term_store import iter_term_files
    from scripts.text_utils import normalize_term, safe_text
except ModuleNotFoundError:
    from repo_health import (
        collect_governed_rendering_drift,
        load_translation_declarations,
    )
    from term_store import iter_term_files
    from text_utils import normalize_term, safe_text


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
TRANSLATIONS_DIR = REPO_ROOT / "docs" / "translations"
CANDIDATES_DIR = REPO_ROOT / "candidates"
REVIEWS_DIR = REPO_ROOT / "reviews"
HISTORY_PATH = REPO_ROOT / "reviews" / "check-history.jsonl"
OUTPUT_DIR = REPO_ROOT / "docs" / "generated"

# Backticked spans in translation notes hold both Pali and English. A span is
# read as Pali only when it carries at least one Pali diacritic, and then every
# token inside it counts. That keeps `pariyuṭṭhitena cetasā viharati` whole —
# including the undiacriticked `viharati` — without letting a bare English
# `heart` in backticks enter the corpus. The cost is that a lone ASCII Pali
# word in backticks is missed; the alternative, treating any backticked token
# as Pali when it happens to match a term record, would make the coverage
# number circular.
BACKTICK_SPAN = re.compile(r"`([^`]+)`")
# Uppercase forms matter: a sentence-initial `Āsava` or a headword written
# `Ṭhiti` carries the same diacritic evidence as its lowercase twin, and
# leaving them out dropped those spans from the corpus entirely.
PALI_DIACRITIC = re.compile(r"[āīūṁṃṅñṭḍṇḷṛś]", re.IGNORECASE)
TOKEN_SPLIT = re.compile(r"[^\wÀ-ỿ]+")

# The same declaration shape `repo_health` reads. The left side of a rendering
# declaration is Pali by construction, so it seeds the corpus even when the
# headword carries no diacritics.
RENDERING_DECLARATION = re.compile(r"`([^`]+)`\s*(?:is rendered|→)\s*`([^`]+)`")

# Pali function words and quotation scaffolding that should never count as
# corpus vocabulary. Deliberately short: this is a measurement filter, not a
# lexicon. `scripts/extract_candidate_terms.py` keeps the larger list used for
# candidate discovery; the two serve different jobs and drifting them apart is
# fine.
CORPUS_STOPWORDS = frozenset(
    {
        "atha", "api", "assa", "ayam", "bhante", "bhikkhave", "bhikkhu",
        "ca", "ce", "cha", "eva", "evam", "hi", "hoti", "idam", "idha",
        "ime", "imasmim", "iti", "kho", "na", "nama", "netam", "no",
        "pana", "pi", "puna", "so", "sace", "tam", "tatha", "tassa",
        "tatra", "te", "tena", "ti", "va", "vuccati", "yam", "yatha",
        "ye", "yo", "avuso", "cattaro", "dutiyam", "etam", "etassa",
        "katamo", "katamam", "katame", "seyyathidam", "vuttam",
    }
)

# A coarse inflection fold, not a morphological analyser. It exists so that
# `cittaṃ`, `cittena`, and `cittassa` are all measured against the `citta`
# record instead of being reported as three ungoverned surfaces. Ordered
# longest first so `ānaṃ` is tried before `aṃ`.
INFLECTION_SUFFIXES = (
    "smim", "anam", "assa", "ssa", "ehi", "esu", "aya", "ena", "ani",
    "ayo", "iyo", "mhi", "nam", "smi",
    "am", "na", "ya", "hi", "su", "no", "vo", "ti",
    "a", "e", "i", "o", "u", "m",
)
MIN_FOLD_STEM = 4
# One listed ending may always be removed whole, however long it is, because
# the table only holds real endings -- `-smiṃ`, `-ānaṃ`, `-assa`. The cap
# applies to what a *second* round may remove on top of the first, where the
# fold stops describing an inflection and starts finding a different word:
# `veramaṇī` reaches `vera` only by taking `ani` and then `m`, and `vera`
# governs enmity.
MAX_FOLD_STRIP = 3

# Anything shorter is noise once diacritics are stripped.
MIN_CORPUS_TOKEN = 4

# The newcomer-review ledger's terminal surface status, kept in step with
# ALLOWED_STATUS in `scripts/check_newcomer_reviews.py`.
LEDGER_TERMINAL_STATUS = "validated"

STALE_BUCKETS = ((7, "0-7 days"), (30, "8-30 days"), (90, "31-90 days"))
STALE_OVERFLOW = "over 90 days"


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_terms(terms_dir: Path = TERMS_DIR) -> dict[str, dict[str, object]]:
    terms: dict[str, dict[str, object]] = {}
    for path in iter_term_files(terms_dir):
        data = load_json(path)
        if isinstance(data, dict):
            normalized = str(data.get("normalized_term") or path.stem)
            terms[normalized] = data
    return terms


def headword_index(terms: dict[str, dict[str, object]]) -> dict[str, str]:
    """Map every normalized headword to the record key that governs it.

    Compound slugs are indexed twice. `normalize_term` turns `sammā-diṭṭhi`
    into `samma_ditthi`, but the same compound quoted in a translation comes
    through as `sammaditthi` with nothing to mark the seam, so the separator
    is stripped to give the run-together form a key of its own.
    """
    index: dict[str, str] = {}

    def add(candidate: str, key: str) -> None:
        if candidate:
            index.setdefault(candidate, key)
            index.setdefault(candidate.replace("_", ""), key)

    for key, data in terms.items():
        add(key, key)
        term = data.get("term")
        if isinstance(term, str) and term:
            add(normalize_term(term), key)
    return index


def fold_candidates(token: str) -> list[str]:
    """Return the token plus the coarse stems worth testing against records.

    Every applicable suffix is tried at each step rather than only the first
    that fits. `cittaṃ` normalizes to `cittam`, which matches both `am` and
    `m`; stopping at the first would leave `citt`, and the `citta` record that
    actually governs the word would be reported as a coverage gap.
    """
    forms = [token]
    frontier = {token}
    for round_number in range(2):
        nextfrontier: set[str] = set()
        for stem in frontier:
            for suffix in INFLECTION_SUFFIXES:
                if stem.endswith(suffix) and len(stem) - len(suffix) >= MIN_FOLD_STEM:
                    folded = stem[: -len(suffix)]
                    # The first round may take one whole listed ending. Only
                    # the second round is capped, so a compound ending like
                    # `-smiṃ` folds while a two-step slide into a different
                    # word does not.
                    if round_number and len(token) - len(folded) > MAX_FOLD_STRIP:
                        continue
                    if folded not in forms and folded not in nextfrontier:
                        nextfrontier.add(folded)
        if not nextfrontier:
            break
        # Most Pali nominal stems end in -a, and stripping a case ending takes
        # that stem vowel with it: `dhamme` folds to `dhamm`, `phasso` to
        # `phass`. Restoring the vowel is what connects those back to the
        # `dhamma` and `phassa` records.
        restored = {stem + "a" for stem in nextfrontier if not stem.endswith("a")}
        for form in sorted(nextfrontier | restored):
            if form not in forms:
                forms.append(form)
        frontier = nextfrontier
    return forms


def resolve_token(token: str, index: dict[str, str]) -> tuple[str | None, str]:
    """Match one corpus token to a governing record.

    Returns the record key and how it was reached: `exact` for a headword hit,
    `inflected` for a hit after folding, `compound` when the token is two
    governed headwords run together (`kāyasaṅkhāra`), and `none` when nothing
    governs it. Compound members are folded too, since the tail of a compound
    carries the case ending for the whole word.
    """
    forms = fold_candidates(token)
    for position, form in enumerate(forms):
        if form in index:
            return index[form], "exact" if position == 0 else "inflected"

    for form in forms:
        for split in range(MIN_FOLD_STEM, len(form) - MIN_FOLD_STEM + 1):
            head, tail = form[:split], form[split:]
            if head not in index:
                continue
            if any(candidate in index for candidate in fold_candidates(tail)):
                return index[head], "compound"

    return None, "none"


def pali_tokens(text: str) -> list[str]:
    """Normalized Pali tokens from one document's backticked spans."""
    tokens: list[str] = []
    for span in BACKTICK_SPAN.findall(text):
        if not PALI_DIACRITIC.search(span):
            continue
        for raw in TOKEN_SPLIT.split(span):
            normalized = normalize_term(raw)
            if len(normalized) < MIN_CORPUS_TOKEN or normalized in CORPUS_STOPWORDS:
                continue
            if normalized.isdigit():
                continue
            tokens.append(normalized)
    for headword, _rendering in RENDERING_DECLARATION.findall(text):
        # Only headwords the backtick scan could not see. A declaration is
        # itself a backticked span, so a diacriticked headword has already
        # been counted above, and adding it again inflated every occurrence
        # figure the coverage section reports.
        if PALI_DIACRITIC.search(headword):
            continue
        # Tokenized like any other span: a declaration headword can be a
        # phrase or carry an ellipsis, and taking it whole turned
        # `āraddhosmi ... āraddhacittosmi` into one junk surface.
        for raw in TOKEN_SPLIT.split(headword):
            normalized = normalize_term(raw)
            if len(normalized) < MIN_CORPUS_TOKEN or normalized in CORPUS_STOPWORDS:
                continue
            if normalized.isdigit():
                continue
            tokens.append(normalized)
    return tokens


def example_phrase_tokens(terms: dict[str, dict[str, object]]) -> list[str]:
    """Normalized Pali tokens from the example phrases the records carry."""
    tokens: list[str] = []
    for data in terms.values():
        phrases = data.get("example_phrases")
        if not isinstance(phrases, list):
            continue
        for phrase in phrases:
            if not isinstance(phrase, dict):
                continue
            pali = phrase.get("pali")
            if not isinstance(pali, str):
                continue
            for raw in TOKEN_SPLIT.split(pali):
                normalized = normalize_term(raw)
                if len(normalized) < MIN_CORPUS_TOKEN or normalized in CORPUS_STOPWORDS:
                    continue
                tokens.append(normalized)
    return tokens


def collect_coverage(
    terms: dict[str, dict[str, object]],
    translations_dir: Path = TRANSLATIONS_DIR,
) -> dict[str, object]:
    """Governed versus ungoverned share of the Pali the corpus actually quotes."""
    index = headword_index(terms)
    counts: Counter[str] = Counter()
    sources: dict[str, set[str]] = {}

    def record(token: str, source: str) -> None:
        counts[token] += 1
        sources.setdefault(token, set()).add(source)

    if translations_dir.exists():
        for path in sorted(translations_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            for token in pali_tokens(text):
                record(token, path.name)
    for token in example_phrase_tokens(terms):
        record(token, "terms/")

    governed_types = 0
    governed_tokens = 0
    by_route: Counter[str] = Counter()
    ungoverned: list[dict[str, object]] = []

    for token, count in counts.items():
        key, route = resolve_token(token, index)
        by_route[route] += 1
        if key is None:
            ungoverned.append(
                {
                    "surface": token,
                    "occurrences": count,
                    "documents": sorted(sources.get(token, set()))[:5],
                }
            )
            continue
        governed_types += 1
        governed_tokens += count

    ungoverned.sort(key=lambda row: (-int(row["occurrences"]), str(row["surface"])))
    distinct = len(counts)
    total = sum(counts.values())

    return {
        "distinct_surfaces": distinct,
        "total_occurrences": total,
        "governed_surfaces": governed_types,
        "ungoverned_surfaces": distinct - governed_types,
        "governed_occurrences": governed_tokens,
        "surface_coverage_pct": round(100 * governed_types / distinct, 1) if distinct else 0.0,
        "occurrence_coverage_pct": round(100 * governed_tokens / total, 1) if total else 0.0,
        "match_routes": dict(sorted(by_route.items())),
        # The full list, not a preview. Truncation happens in the renderers,
        # so the JSON a drill-down view reads never needs a second pass over
        # the corpus to see the tail.
        "top_ungoverned": ungoverned,
        "ungoverned_total": len(ungoverned),
    }


def collect_drift(
    terms: dict[str, dict[str, object]],
    translations_dir: Path = TRANSLATIONS_DIR,
) -> dict[str, object]:
    """Declared renderings that fight the records that govern them.

    This wraps `repo_health.collect_governed_rendering_drift` rather than
    re-deriving it. Scanning translation prose for discouraged renderings is
    deliberately not attempted: that experiment is recorded in
    `repo_health.collect_governed_rendering_drift` as abandoned, because a
    phrase cannot be attributed to a headword without alignment this
    repository does not have.
    """
    declarations = load_translation_declarations(translations_dir, terms)
    findings = collect_governed_rendering_drift(terms, declarations)

    by_kind: Counter[str] = Counter()
    by_document: Counter[str] = Counter()
    for finding in findings:
        by_kind[str(finding["kind"])] += 1
        by_document[str(finding["document"])] += 1

    declared_total = sum(len(items) for items in declarations.values())
    return {
        "documents_with_declarations": len(declarations),
        "declared_renderings": declared_total,
        "findings_total": len(findings),
        "by_kind": dict(sorted(by_kind.items())),
        "worst_documents": [
            {"document": document, "findings": count}
            for document, count in by_document.most_common(10)
        ],
        "findings": findings,
    }


def git_output(args: list[str], repo_root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    return result.stdout if result.returncode == 0 else None


@lru_cache(maxsize=None)
def shallow_boundary_date(repo_root: Path = REPO_ROOT) -> str | None:
    """The date of the oldest commit a shallow clone can see, if it is shallow.

    A shallow clone does not fail on `git log` — it answers from its graft
    boundary. Anything genuinely added before that boundary is reported as
    having been added *on* it, which is a wrong date wearing the costume of a
    right one. Knowing the boundary lets `git_first_seen` withhold exactly
    those answers and keep the rest, which matters because this repository is
    routinely worked on from shallow clones while CI checks out full history.

    Returns None for a complete clone, where every date is trustworthy.
    """
    shallow = git_output(["rev-parse", "--is-shallow-repository"], repo_root)
    if shallow is None or shallow.strip() != "true":
        return None
    # Not `--reverse --max-count=1`: git applies the count before reversing,
    # so that pair returns the newest commit, which would mark every date in
    # the repository as untrustworthy.
    log = git_output(["log", "--format=%ad", "--date=short"], repo_root)
    if not log:
        return None
    dates = [line.strip() for line in log.splitlines() if line.strip()]
    return dates[-1] if dates else None


def git_first_seen(path: Path, repo_root: Path = REPO_ROOT) -> str | None:
    """The author date of the commit that added `path`, as an ISO date.

    Returns None when git cannot answer: an untracked file, no git at all, or
    a date that sits on a shallow clone's graft boundary and therefore cannot
    be distinguished from an older one. Callers render that as `unknown`
    rather than guessing, and both workflows check out full history so CI
    reports the real dates.
    """
    try:
        result = subprocess.run(
            [
                "git",
                "log",
                "--diff-filter=A",
                "--follow",
                "--format=%ad",
                "--date=short",
                "--",
                str(path),
            ],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not lines:
        return None
    first_seen = lines[-1]
    boundary = shallow_boundary_date(repo_root)
    if boundary is not None and first_seen <= boundary:
        # Indistinguishable from an older date that was truncated away.
        return None
    return first_seen


def collect_review_queue(
    terms: dict[str, dict[str, object]],
    *,
    candidates_dir: Path = CANDIDATES_DIR,
    reviews_dir: Path = REVIEWS_DIR,
    repo_root: Path = REPO_ROOT,
) -> dict[str, object]:
    """Everything waiting on an editorial decision, with the date it started waiting.

    Three queues feed this, because the repository holds review work in three
    shapes: staged candidate files, term records still marked `draft`, and
    translation surfaces whose newcomer review is unfinished.
    """
    items: list[dict[str, object]] = []

    if candidates_dir.exists():
        for path in sorted(candidates_dir.rglob("*")):
            if not path.is_file() or path.name in {"README.md", ".gitkeep"}:
                continue
            items.append(
                {
                    "kind": "candidate",
                    "id": path.relative_to(repo_root).as_posix(),
                    "waiting_since": git_first_seen(path, repo_root),
                }
            )

    for key, data in sorted(terms.items()):
        if data.get("status") != "draft":
            continue
        entry_type = str(data.get("entry_type", "unknown"))
        path = TERMS_DIR / entry_type / f"{key}.json"
        items.append(
            {
                "kind": "draft_entry",
                "id": key,
                "waiting_since": git_first_seen(path, repo_root) if path.exists() else None,
            }
        )

    ledger_path = reviews_dir / "newcomer-review-ledger.json"
    if ledger_path.exists():
        ledger = load_json(ledger_path)
        surfaces = ledger.get("surfaces") if isinstance(ledger, dict) else None
        ledger_opened = git_first_seen(ledger_path, repo_root)
        if isinstance(surfaces, dict):
            for surface_key, surface in sorted(surfaces.items()):
                if not isinstance(surface, dict):
                    continue
                # `validated` is the terminal state in the ledger's own
                # vocabulary (`scripts/check_newcomer_reviews.py` allows
                # recruiting, in-review, ready, validated). `complete` belongs
                # to the sub-steps, not the surface, so testing for it here
                # excluded nothing and left finished surfaces in the queue.
                if surface.get("status") == LEDGER_TERMINAL_STATUS:
                    continue
                # The ledger records when source fidelity was signed off but
                # not when the surface entered the queue, so the fidelity date
                # is the closest honest "waiting since" it carries.
                fidelity = surface.get("source_fidelity")
                since = None
                if isinstance(fidelity, dict):
                    completed = fidelity.get("completed_on")
                    if isinstance(completed, str) and completed:
                        since = completed
                items.append(
                    {
                        "kind": "newcomer_review",
                        "id": surface_key,
                        "waiting_since": since or ledger_opened,
                        "state": str(surface.get("status", "unknown")),
                    }
                )

    items.sort(key=lambda row: (row["waiting_since"] or "9999-99-99", str(row["id"])))
    by_kind: Counter[str] = Counter(str(row["kind"]) for row in items)
    return {
        "total": len(items),
        "by_kind": dict(sorted(by_kind.items())),
        "undated": sum(1 for row in items if not row["waiting_since"]),
        "oldest_waiting_since": items[0]["waiting_since"] if items else None,
        "items": items,
    }


def bucket_review_queue(queue: dict[str, object], as_of: date) -> dict[str, object]:
    """Age the review queue against a reference date.

    Kept out of `collect_review_queue` on purpose: day counts move every
    midnight, and the committed Markdown has to stay byte-stable. Only the CLI
    and the JSON snapshot call this.
    """
    buckets: Counter[str] = Counter()
    aged: list[dict[str, object]] = []
    for row in queue.get("items", []):
        since = row.get("waiting_since")
        if not isinstance(since, str):
            buckets["unknown"] += 1
            aged.append({**row, "waiting_days": None})
            continue
        try:
            started = date.fromisoformat(since)
        except ValueError:
            buckets["unknown"] += 1
            aged.append({**row, "waiting_days": None})
            continue
        days = (as_of - started).days
        label = STALE_OVERFLOW
        for limit, name in STALE_BUCKETS:
            if days <= limit:
                label = name
                break
        buckets[label] += 1
        aged.append({**row, "waiting_days": days})
    aged.sort(key=lambda row: -(row["waiting_days"] or -1))
    return {"as_of": as_of.isoformat(), "buckets": dict(buckets), "items": aged}


def load_check_history(path: Path = HISTORY_PATH) -> list[dict[str, object]]:
    """Weekly schema and lint failure counts, oldest first.

    The file is produced by `scripts/backfill_check_history.py`, which replays
    git history. A missing file is normal on a fresh checkout and reported as
    an empty series rather than an error.
    """
    if not path.exists():
        return []
    rows: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict) and "week" in row:
            rows.append(row)
    rows.sort(key=lambda row: str(row.get("week", "")))
    return rows


def collect_check_failures(path: Path = HISTORY_PATH) -> dict[str, object]:
    series = load_check_history(path)
    schema_total = sum(int(row.get("schema_failures", 0) or 0) for row in series)
    lint_total = sum(int(row.get("lint_failures", 0) or 0) for row in series)
    failing_weeks = sum(
        1
        for row in series
        if int(row.get("schema_failures", 0) or 0) or int(row.get("lint_failures", 0) or 0)
    )
    return {
        "weeks_recorded": len(series),
        "first_week": series[0]["week"] if series else None,
        "last_week": series[-1]["week"] if series else None,
        "schema_failures_total": schema_total,
        "lint_failures_total": lint_total,
        "failing_weeks": failing_weeks,
        "series": series,
    }


def collect_formula_agreement(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    """Shared Pali formulas whose English differs across the records quoting them.

    A different question from declared-rendering drift, and kept as a
    separate number on purpose: the drift figure can be an honest zero while
    dozens of formulas still disagree, and one reassuring score would hide
    the second behind the first.
    """
    try:
        from scripts import check_formula_agreement as cfa
    except ModuleNotFoundError:
        import check_formula_agreement as cfa

    exceptions = cfa.load_exceptions()
    unexplained, waived = cfa.collect_disagreements(terms, exceptions)
    regressions, stale = cfa.compare_to_baseline(unexplained, cfa.load_baseline())
    return {
        "unexplained": len(unexplained),
        "waived": len(waived),
        "regressions": len(regressions),
        "stale_baseline": len(stale),
        "groups": [
            {"pali": str(f["pali"]), "records": f["records"], "renderings": f["renderings"]}
            for f in unexplained
        ],
    }


def collect_human_evidence(reviews_dir: Path = REVIEWS_DIR) -> dict[str, object]:
    """What human review has actually been recorded, from the newcomer ledger.

    Structural checks can all pass with this at zero. It is reported on its
    own so that state is visible rather than inferred from silence.
    """
    ledger_path = reviews_dir / "newcomer-review-ledger.json"
    empty = {
        "surfaces": 0,
        "source_fidelity_complete": 0,
        "read_aloud_complete": 0,
        "newcomer_reviews_recorded": 0,
        "surfaces_validated": 0,
    }
    if not ledger_path.exists():
        return empty
    ledger = load_json(ledger_path)
    surfaces = ledger.get("surfaces") if isinstance(ledger, dict) else None
    if not isinstance(surfaces, dict):
        return empty
    rows = [s for s in surfaces.values() if isinstance(s, dict)]

    def sub_complete(row: dict[str, object], key: str) -> bool:
        sub = row.get(key)
        return isinstance(sub, dict) and sub.get("status") == "complete"

    return {
        "surfaces": len(rows),
        "source_fidelity_complete": sum(sub_complete(r, "source_fidelity") for r in rows),
        "read_aloud_complete": sum(sub_complete(r, "human_read_aloud") for r in rows),
        "newcomer_reviews_recorded": sum(
            len(r["newcomer_reviews"]) for r in rows if isinstance(r.get("newcomer_reviews"), list)
        ),
        "surfaces_validated": sum(r.get("status") == LEDGER_TERMINAL_STATUS for r in rows),
    }


def build_report(
    terms: dict[str, dict[str, object]],
    *,
    translations_dir: Path = TRANSLATIONS_DIR,
    history_path: Path = HISTORY_PATH,
) -> dict[str, object]:
    """The whole dashboard as data.

    Every renderer — the Markdown below, the CLI text mode, and any later HTML
    view — reads this dict and nothing else. Full detail lists stay in here
    even where the Markdown truncates, so a drill-down view never needs a
    second pass over the corpus.
    """
    return {
        "coverage": collect_coverage(terms, translations_dir),
        "drift": collect_drift(terms, translations_dir),
        "review_queue": collect_review_queue(terms),
        "check_failures": collect_check_failures(history_path),
        "formula_agreement": collect_formula_agreement(terms),
        "human_evidence": collect_human_evidence(),
    }


def md_escape(value: object) -> str:
    """Make a value safe inside a Markdown table cell."""
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_dashboard(report: dict[str, object], *, top: int = 25) -> str:
    coverage = report["coverage"]
    drift = report["drift"]
    queue = report["review_queue"]
    failures = report["check_failures"]

    lines: list[str] = [
        "# Editorial Health Dashboard",
        "",
        "Generated by `scripts/health_dashboard.py`. Do not edit by hand.",
        "",
        "This is a reporting surface, not a gate. Nothing here blocks a merge;",
        "the gates live in `scripts/run_checks.py` and the CI workflow.",
        "",
        "Waiting times are recorded as dates rather than day counts so this file",
        "stays byte-stable between runs. For live ages run the script directly:",
        "",
        "```bash",
        "python scripts/health_dashboard.py --top 20",
        "```",
        "",
        "## Coverage",
        "",
        "How much of the Pali the repository actually quotes is governed by a term",
        "record. The corpus is the backticked Pali in `docs/translations/` plus the",
        "example phrases carried by the records themselves.",
        "",
        "| Measure | Value |",
        "| --- | --- |",
        f"| Distinct surfaces | {coverage['distinct_surfaces']} |",
        f"| Governed surfaces | {coverage['governed_surfaces']} |",
        f"| Ungoverned surfaces | {coverage['ungoverned_surfaces']} |",
        f"| Coverage by surface | {coverage['surface_coverage_pct']}% |",
        f"| Coverage by occurrence | {coverage['occurrence_coverage_pct']}% |",
        "",
        "Surfaces reach a record by one of three routes. `exact` is a headword hit,",
        "`inflected` is a hit after a coarse case-ending fold, and `compound` is two",
        "governed headwords run together. The two folded routes are heuristic: they",
        "buy a usable number at the cost of the occasional wrong lemma, so treat a",
        "single row as a lead rather than a fact.",
        "",
        "| Route | Surfaces |",
        "| --- | --- |",
    ]
    for route, count in coverage["match_routes"].items():
        lines.append(f"| `{md_escape(route)}` | {count} |")

    lines += [
        "",
        f"### Ungoverned surfaces by frequency ({coverage['ungoverned_total']} total)",
        "",
        "| Surface | Occurrences | Documents |",
        "| --- | --- | --- |",
    ]
    for row in coverage["top_ungoverned"][:top]:
        documents = ", ".join(md_escape(name) for name in row["documents"]) or "—"
        lines.append(f"| `{md_escape(row['surface'])}` | {row['occurrences']} | {documents} |")

    lines += [
        "",
        "## Drift",
        "",
        "Renderings a translation document declares against the record that governs",
        "the headword. `self_contradiction` is one document declaring two renderings",
        "for the same headword, `discouraged` is a rendering the record rejects, and",
        "`unlisted` is a rendering the record neither prefers nor allows.",
        "",
        "Translation prose is deliberately not scanned for discouraged renderings.",
        "That was measured and abandoned — see the note in",
        "`repo_health.collect_governed_rendering_drift`.",
        "",
        "| Measure | Value |",
        "| --- | --- |",
        f"| Documents declaring renderings | {drift['documents_with_declarations']} |",
        f"| Declared renderings | {drift['declared_renderings']} |",
        f"| Findings | {drift['findings_total']} |",
        "",
    ]
    if drift["findings"]:
        lines += [
            "| Document | Headword | Kind | Declared | Preferred |",
            "| --- | --- | --- | --- | --- |",
        ]
        for finding in drift["findings"][:top]:
            declared = ", ".join(md_escape(item) for item in finding["declared"])
            lines.append(
                f"| {md_escape(finding['document'])} | `{md_escape(finding['headword'])}` "
                f"| {md_escape(finding['kind'])} | {declared} "
                f"| {md_escape(finding['preferred']) or '—'} |"
            )
        lines.append("")
    else:
        lines += ["No declared rendering fights its record.", ""]

    lines += [
        "## Review queue",
        "",
        "Work waiting on an editorial decision: staged candidate files, term records",
        "still marked `draft`, and translation surfaces whose newcomer review is",
        "unfinished. Oldest first.",
        "",
        "| Measure | Value |",
        "| --- | --- |",
        f"| Waiting | {queue['total']} |",
        f"| Oldest waiting since | {queue['oldest_waiting_since'] or '—'} |",
        f"| Without a recorded date | {queue['undated']} |",
        "",
    ]
    if queue["items"]:
        lines += [
            "| Kind | Item | Waiting since |",
            "| --- | --- | --- |",
        ]
        for row in queue["items"][:top]:
            since = row["waiting_since"] or "unknown"
            lines.append(
                f"| {md_escape(row['kind'])} | `{md_escape(row['id'])}` | {md_escape(since)} |"
            )
        lines.append("")
    else:
        lines += ["Nothing is waiting for review.", ""]

    formulas = report["formula_agreement"]
    lines += [
        "## Formula agreement",
        "",
        "Pali phrases quoted by more than one term record whose English differs",
        "between those records. This is a different question from declared-rendering",
        "drift above, and it is reported separately so a zero there cannot stand in",
        "for a zero here. The acknowledged backlog lives in",
        "`reviews/formula-baseline.json`; anything outside it fails the check.",
        "",
        "| Measure | Value |",
        "| --- | --- |",
        f"| Unexplained disagreements | {formulas['unexplained']} |",
        f"| Waived by scoped exception | {formulas['waived']} |",
        f"| Outside the acknowledged baseline | {formulas['regressions']} |",
        f"| Stale baseline entries | {formulas['stale_baseline']} |",
        "",
    ]
    if formulas["groups"]:
        lines += [
            "| Formula | Records | Renderings |",
            "| --- | --- | --- |",
        ]
        for group in formulas["groups"][:top]:
            renderings = "; ".join(f"`{md_escape(k)}`: {md_escape(t)}" for k, t in group["renderings"])
            lines.append(f"| `{md_escape(group['pali'])}` | {len(group['records'])} | {renderings} |")
        lines.append("")
    else:
        lines += ["Every shared formula is rendered the same way wherever it is quoted.", ""]

    evidence = report["human_evidence"]
    lines += [
        "## Human review evidence",
        "",
        "What human review the newcomer ledger actually records. Every structural",
        "check on this page can pass with these at zero; they are listed so that",
        "state is visible rather than inferred from silence.",
        "",
        "| Measure | Value |",
        "| --- | --- |",
        f"| Surfaces in the cohort | {evidence['surfaces']} |",
        f"| Source fidelity signed off | {evidence['source_fidelity_complete']} |",
        f"| Human read-aloud complete | {evidence['read_aloud_complete']} |",
        f"| Newcomer reviews recorded | {evidence['newcomer_reviews_recorded']} |",
        f"| Surfaces validated | {evidence['surfaces_validated']} |",
        "",
        "Source verification (`scripts/verify_example_sources.py`) is not reported",
        "here: its results depend on a network cache outside the repository, so the",
        "same commit would not produce the same page. Run it directly.",
        "",
        "## Schema and lint failures per week",
        "",
        "Replayed from git history by `scripts/backfill_check_history.py`, which runs",
        "`validate_terms.py --strict` and `lint_terms.py --strict` against every",
        "commit and groups the result by ISO week. Counts are findings, and a week",
        "reports its worst commit rather than the sum, so a failure that survives",
        "several commits is counted once.",
        "",
    ]
    if failures["weeks_recorded"]:
        lines += [
            "| Measure | Value |",
            "| --- | --- |",
            f"| Weeks recorded | {failures['weeks_recorded']} |",
            f"| Range | {failures['first_week']} to {failures['last_week']} |",
            f"| Weeks with a failure | {failures['failing_weeks']} |",
            "",
            "| Week | Commits | Failing commits | Schema findings | Lint findings |",
            "| --- | --- | --- | --- | --- |",
        ]
        for row in failures["series"]:
            lines.append(
                f"| {md_escape(row.get('week', '—'))} | {row.get('commits_checked', '—')} "
                f"| {row.get('commits_failing', '—')} "
                f"| {row.get('schema_failures', '—')} | {row.get('lint_failures', '—')} |"
            )
        lines.append("")
    else:
        lines += [
            "No history recorded yet. Run:",
            "",
            "```bash",
            "python scripts/backfill_check_history.py",
            "```",
            "",
        ]

    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    """Render the dashboard into OUTPUT_DIR.

    `scripts/check_generated_docs.py` calls this with OUTPUT_DIR pointed at a
    temporary directory and compares the result against the committed file, so
    everything written here has to be a pure function of repository content.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report(terms)
    outputs = {OUTPUT_DIR / "health-dashboard.md": render_dashboard(report)}
    for path, content in outputs.items():
        path.write_text(content + ("" if content.endswith("\n") else "\n"), encoding="utf-8")
    return sorted(outputs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("text", "json", "html"),
        default="text",
        help="Output format. `html` is a self-contained page with charts, written to stdout.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=15,
        help="Number of rows to show for long sections.",
    )
    parser.add_argument(
        "--as-of",
        default=None,
        help="Reference date (YYYY-MM-DD) for review-queue ages. Defaults to today.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the generated dashboard under docs/generated/ instead of reporting.",
    )
    args = parser.parse_args()

    if not TERMS_DIR.exists():
        print(f"ERROR: Terms directory not found: {TERMS_DIR}")
        return 1

    terms = load_terms()
    if not terms:
        print("WARNING: No term files found in terms/")
        return 0

    try:
        as_of = date.fromisoformat(args.as_of) if args.as_of else datetime.now().date()
    except ValueError:
        print(f"ERROR: --as-of must be an ISO date, got {args.as_of!r}")
        return 1

    if args.write:
        for path in write_outputs(terms):
            print(f"Wrote {path.relative_to(REPO_ROOT).as_posix()}")
        return 0

    report = build_report(terms)
    report["review_queue_aged"] = bucket_review_queue(report["review_queue"], as_of)

    if args.format == "json":
        # ensure_ascii for the same reason `repo_health` does it: this report
        # carries Pali headwords and CI writes it through a redirect.
        json.dump(report, sys.stdout, ensure_ascii=True, indent=2)
        sys.stdout.write("\n")
    elif args.format == "html":
        try:
            from scripts.health_dashboard_html import render_html
        except ModuleNotFoundError:
            from health_dashboard_html import render_html
        head = git_output(["rev-parse", "--short", "HEAD"], REPO_ROOT)
        page = render_html(
            report,
            generated_on=as_of.isoformat(),
            head_commit=head.strip() if head else None,
            top=args.top,
        )
        # The page is UTF-8 by declaration and carries Pali; a redirected
        # stdout on Windows would otherwise pick cp1252 and fail on the first
        # diacritic, so the bytes are written directly.
        sys.stdout.buffer.write(page.encode("utf-8"))
    else:
        print_text_report(report, top=args.top)
    return 0


def print_text_report(report: dict[str, object], *, top: int) -> None:
    coverage = report["coverage"]
    drift = report["drift"]
    aged = report["review_queue_aged"]
    failures = report["check_failures"]

    print("Health Dashboard")
    print()
    print("Coverage")
    print(
        f"- Governed surfaces: {coverage['governed_surfaces']} / "
        f"{coverage['distinct_surfaces']} ({coverage['surface_coverage_pct']}%)"
    )
    print(f"- Governed occurrences: {coverage['occurrence_coverage_pct']}%")
    print(f"- Match routes: {coverage['match_routes']}")
    print(f"- Top ungoverned ({coverage['ungoverned_total']} total):")
    for row in coverage["top_ungoverned"][:top]:
        print(f"    {safe_text(str(row['surface']))} ({row['occurrences']}x)")
    print()

    print("Drift")
    print(
        f"- Declared renderings: {drift['declared_renderings']} across "
        f"{drift['documents_with_declarations']} document(s)"
    )
    print(f"- Findings: {drift['findings_total']} {drift['by_kind']}")
    for row in drift["worst_documents"][:top]:
        print(f"    {safe_text(str(row['document']))}: {row['findings']}")
    print()

    print(f"Review queue (as of {aged['as_of']})")
    print(f"- Waiting: {report['review_queue']['total']} {aged['buckets']}")
    for row in aged["items"][:top]:
        days = row["waiting_days"]
        age = f"{days}d" if days is not None else "unknown"
        print(f"    [{safe_text(str(row['kind']))}] {safe_text(str(row['id']))} — {age}")
    print()

    formulas = report["formula_agreement"]
    print("Formula agreement")
    print(
        f"- Unexplained: {formulas['unexplained']} | waived: {formulas['waived']} "
        f"| outside baseline: {formulas['regressions']} | stale baseline: {formulas['stale_baseline']}"
    )
    for group in formulas["groups"][:top]:
        print(f"    {safe_text(str(group['pali']))} ({len(group['records'])} records)")
    print()

    evidence = report["human_evidence"]
    print("Human review evidence")
    print(
        f"- Cohort {evidence['surfaces']} | fidelity {evidence['source_fidelity_complete']} "
        f"| read-aloud {evidence['read_aloud_complete']} | newcomer reviews "
        f"{evidence['newcomer_reviews_recorded']} | validated {evidence['surfaces_validated']}"
    )
    print()

    print("Check failures")
    if not failures["weeks_recorded"]:
        print("- No history recorded. Run scripts/backfill_check_history.py.")
        return
    print(
        f"- Weeks recorded: {failures['weeks_recorded']} "
        f"({failures['first_week']} to {failures['last_week']})"
    )
    print(
        f"- Failing weeks: {failures['failing_weeks']} "
        f"(schema {failures['schema_failures_total']}, lint {failures['lint_failures_total']})"
    )


if __name__ == "__main__":
    sys.exit(main())
