"""Maintainer pages: server-rendered HTML, no scripts, everything escaped.

The queue exists to connect a reader's difficulty to the exact passage and
the governed term it concerns, and to record what the editors decided. It
never edits a translation, a glossary entry, or a term record; a disposition
points at the change made elsewhere.
"""

from __future__ import annotations

import html
import json
from typing import TYPE_CHECKING, Any
from urllib.parse import urlencode

from . import auth, export
from .storage import ASSESSMENTS, FIX_LAYERS, STATUSES

if TYPE_CHECKING:  # pragma: no cover
    from .app import FeedbackApp, Request, Response

STATUS_LABELS = {
    "received": "Received",
    "examined": "Examined",
    "proposed": "Proposed change",
    "revised": "Revised",
    "checked": "Checked with readers",
}
FIX_LAYER_LABELS = {
    "": "Not decided",
    "translation": "Translation",
    "glossary": "Glossary",
    "introduction": "Introduction",
    "lexicon": "Shared lexicon",
    "none": "No change",
}
CATEGORY_LABELS = {
    "word": "Word or phrase",
    "sentence": "Sentence",
    "background": "Background",
    "awkward": "Awkward wording",
    "other": "Something else",
}
FILTER_FIELDS = ("surface", "passage", "term", "category", "version", "status", "channel", "target", "session")

STYLE = """
body { font: 15px/1.5 system-ui, sans-serif; margin: 0; padding: 1rem; color: #1b1b1b; background: #fbfaf7; }
main { max-width: 72rem; margin: 0 auto; }
nav a { margin-right: 1rem; }
table { border-collapse: collapse; width: 100%; font-size: 0.92em; }
th, td { text-align: left; vertical-align: top; padding: 0.35rem 0.5rem; border-bottom: 1px solid #ddd; }
th { background: #efece4; }
form.filters label { display: inline-block; margin: 0 0.8rem 0.5rem 0; }
form.filters input, form.filters select { font: inherit; }
fieldset { border: 1px solid #ccc; margin: 1rem 0; padding: 0.6rem 1rem; }
label.block { display: block; margin: 0.5rem 0; font-weight: 600; }
label.block input, label.block select, label.block textarea { display: block; width: 100%; max-width: 40rem; font: inherit; font-weight: normal; box-sizing: border-box; }
blockquote { margin: 0.5rem 0; padding: 0.5rem 0.8rem; border-left: 4px solid #b9b2a2; background: #f3f0e8; white-space: pre-wrap; }
.original { white-space: pre-wrap; border: 1px solid #ddd; background: #fff; padding: 0.6rem; }
.muted { color: #555; }
.tag { display: inline-block; padding: 0 0.4em; border: 1px solid #999; border-radius: 0.3em; font-size: 0.85em; margin-right: 0.3em; }
.notice { border-left: 4px solid #2a6f4e; background: #e7f3ec; padding: 0.5rem 0.8rem; }
.warn { border-left: 4px solid #a55; background: #f7e9e9; padding: 0.5rem 0.8rem; }
button { font: inherit; padding: 0.35rem 0.8rem; }
code { background: #eee; padding: 0 0.2em; }
"""


def h(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def page(title: str, body: str, notice: str = "") -> str:
    banner = f'<p class="notice">{h(notice)}</p>' if notice else ""
    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>{h(title)} · Reader feedback</title>"
        f"<style>{STYLE}</style></head><body><main>"
        "<nav><a href=\"/admin/\">Queue</a><a href=\"/admin/terms\">By term</a>"
        "<a href=\"/admin/sessions\">Sessions</a><a href=\"/admin/export.json\">Export queue (JSON)</a></nav>"
        f"<h1>{h(title)}</h1>{banner}{body}</main></body></html>"
    )


def options(choices: list[tuple[str, str]], selected: str) -> str:
    return "".join(
        f'<option value="{h(value)}"{" selected" if value == selected else ""}>{h(label)}</option>'
        for value, label in choices
    )


def excerpt(row) -> str:
    if row["target"] == "comprehension":
        answers = json.loads(row["answers_json"] or "{}")
        text = " / ".join(f"{k}: {v}" for k, v in answers.items() if v)
    else:
        text = row["comment"] or ""
    text = " ".join(text.split())
    return text if len(text) <= 140 else text[:139] + "…"


def what(row) -> str:
    if row["target"] == "glossary":
        return f"{row['glossary_term']} · rated {row['rating']}"
    if row["target"] == "comprehension":
        return f"review v{row['question_version']} ({row['question_editorial_status']})"
    return CATEGORY_LABELS.get(row["category"] or "", row["category"] or "")


# ---------------------------------------------------------------------------
# GET
# ---------------------------------------------------------------------------

def handle_get(app: "FeedbackApp", request: "Request", user: str) -> "Response":
    from .app import Response

    storage = app.storage
    path = request.path.rstrip("/") or "/admin"
    notice = request.param("notice")
    if path == "/admin":
        return Response.html(queue_page(app, request, notice))
    if path == "/admin/terms":
        return Response.html(terms_page(app))
    if path == "/admin/sessions":
        return Response.html(sessions_page(app, user, notice))
    if path == "/admin/export.json":
        filters = {field: request.param(field) for field in FILTER_FIELDS}
        return Response.json(export.queue_export(storage, filters))
    parts = path.split("/")
    if len(parts) == 4 and parts[2] == "submissions":
        row = storage.submission(parts[3])
        if row is None:
            return Response.text("No such submission.\n", "404 Not Found")
        return Response.html(detail_page(app, user, row, notice))
    if len(parts) >= 4 and parts[2] == "sessions":
        code = parts[3]
        if len(parts) == 5 and parts[4] == "export.json":
            data = export.session_export(storage, code)
            if data is None:
                return Response.text("No such session.\n", "404 Not Found")
            return Response.json(data)
        session = storage.session_by_code(code)
        if session is None:
            return Response.text("No such session.\n", "404 Not Found")
        return Response.html(session_page(app, user, session, notice))
    return Response.text("Not found.\n", "404 Not Found")


def queue_page(app: "FeedbackApp", request: "Request", notice: str) -> str:
    storage = app.storage
    filters = {field: request.param(field) for field in FILTER_FIELDS}
    try:
        offset = max(0, int(request.param("offset") or 0))
    except ValueError:
        offset = 0
    limit = 100
    rows = storage.query(filters, limit=limit + 1, offset=offset)
    more = len(rows) > limit
    rows = rows[:limit]

    def select(name: str, values: list[str], labels: dict[str, str] | None = None) -> str:
        choices = [("", "Any")] + [(v, (labels or {}).get(v, v)) for v in values]
        return f'<label>{h(name.capitalize())} <select name="{name}">{options(choices, filters[name])}</select></label>'

    form = [
        '<form class="filters" method="get" action="/admin/">',
        select("surface", storage.distinct("surface_key")),
        f'<label>Passage <input name="passage" size="6" value="{h(filters["passage"])}"></label>',
        f'<label>Term <input name="term" size="18" value="{h(filters["term"])}"></label>',
        select("category", storage.distinct("category") + storage.distinct("rating"), CATEGORY_LABELS),
        f'<label>Version <input name="version" size="10" value="{h(filters["version"])}" placeholder="body hash prefix"></label>',
        select("status", list(STATUSES), STATUS_LABELS),
        select("channel", ["public", "formal"]),
        select("target", ["translation", "glossary", "introduction", "comprehension"]),
        f'<label>Session <input name="session" size="10" value="{h(filters["session"])}"></label>',
        '<button type="submit">Filter</button> <a href="/admin/">Clear</a>',
        "</form>",
    ]
    head = (
        "<tr><th>Received</th><th>Channel</th><th>Target</th><th>Sutta</th><th>Passage</th>"
        "<th>What</th><th>Terms</th><th>Version</th><th>Status</th><th>Excerpt</th></tr>"
    )
    body_rows = []
    for row in rows:
        terms = storage.terms_for(row["id"])
        term_links = " ".join(
            f'<a class="tag" href="/admin/?{urlencode({"term": t["term_id"]})}" title="{h(t["basis"])}">{h(t["term_id"])}</a>'
            for t in terms
        ) or '<span class="muted">unmapped</span>'
        body_rows.append(
            "<tr>"
            f'<td><a href="/admin/submissions/{h(row["public_id"])}">{h(row["received_at"][:16].replace("T", " "))}</a></td>'
            f"<td>{h(row['channel'])}</td><td>{h(row['target'])}</td>"
            f"<td>{h(row['surface_label'] or row['surface_key'])}</td>"
            f"<td>{h(row['passage_id'] or '')}</td><td>{h(what(row))}</td><td>{term_links}</td>"
            f"<td><code>{h(row['body_sha256'][:8])}</code></td>"
            f"<td>{h(STATUS_LABELS.get(row['status'], row['status']))}</td><td>{h(excerpt(row))}</td></tr>"
        )
    paging = ""
    if offset or more:
        params = {k: v for k, v in filters.items() if v}
        links = []
        if offset:
            links.append(f'<a href="/admin/?{urlencode(dict(params, offset=max(0, offset - limit)))}">Newer</a>')
        if more:
            links.append(f'<a href="/admin/?{urlencode(dict(params, offset=offset + limit))}">Older</a>')
        paging = "<p>" + " · ".join(links) + "</p>"
    export_link = f'<p><a href="/admin/export.json?{urlencode({k: v for k, v in filters.items() if v})}">Export this view as JSON</a></p>'
    table = f"<table>{head}{''.join(body_rows)}</table>" if rows else "<p>No submissions match.</p>"
    return page("Feedback queue", "".join(form) + f"<p class=\"muted\">{len(rows)} shown.</p>" + table + paging + export_link, notice)


def terms_page(app: "FeedbackApp") -> str:
    rows = app.storage.term_groups()
    if not rows:
        return page("Feedback by term", "<p>No submission carries a term mapping yet.</p>")
    body = ["<p>Submissions grouped by governed term across all texts. Repeated confusion about one term in several suttas is a lexicon question, not a local wording question.</p>",
            "<table><tr><th>Term</th><th>Submissions</th><th>Texts</th><th>Unexamined</th><th>Explicit mappings</th></tr>"]
    for row in rows:
        body.append(
            f'<tr><td><a href="/admin/?{urlencode({"term": row["term_id"]})}">{h(row["term_id"])}</a></td>'
            f"<td>{row['submissions']}</td><td>{h(row['surface_keys'])}</td><td>{row['unexamined']}</td>"
            f"<td>{row['explicit_count']}</td></tr>"
        )
    body.append("</table>")
    return page("Feedback by term", "".join(body))


def detail_page(app: "FeedbackApp", user: str, row, notice: str) -> str:
    storage = app.storage
    token = auth.csrf_token(app.settings.secret_key, user)
    doc = export.submission_document(storage, row)
    parts = [f"<p><a href=\"/admin/\">← Queue</a></p>"]
    parts.append("<h2>What the reader saw</h2>")
    meta = [
        ("Received", doc["received_at"]),
        ("Channel", doc["channel"] + (f" · session {doc['session']['code']} · participant {doc['session']['participant']} ({doc['session']['participant_kind']})" if doc["session"] else "")),
        ("Target", doc["target"]),
        ("Sutta", f"{doc['surface_label']} ({doc['surface_key']}) · {doc['page_path']}"),
        ("Translation body version", doc["body_sha256"]),
        ("Introduction version", f"{doc['introduction_kind'] or ''} {doc['introduction_version'] or ''}".strip() or "not recorded"),
    ]
    if doc["target"] == "translation":
        meta += [("Passage", f"{doc['passage_id']} · section “{doc['passage_section']}” · fingerprint {doc['passage_fingerprint']}")]
    if doc["target"] == "glossary":
        meta += [("Glossary explanation", f"“{doc['glossary_term']}” · version {doc['glossary_version']}")]
    if doc["target"] == "comprehension":
        meta += [("Question set", f"version {doc['question_version']} · {doc['question_editorial_status']} · {doc['question_set_sha256']}"),
                 ("Familiarity", doc["familiarity"] or "not given")]
    parts.append("<table>" + "".join(f"<tr><th>{h(k)}</th><td>{h(v)}</td></tr>" for k, v in meta) + "</table>")
    if doc["passage_text"]:
        parts.append(f"<h3>Passage as shown</h3><blockquote>{h(doc['passage_text'])}</blockquote>")
    if doc["glossary_versions"]:
        parts.append("<p class=\"muted\">Glossary explanations relevant to this passage at the time: " + ", ".join(
            f"{h(t)} ({h(v)})" for t, v in doc["glossary_versions"].items()) + "</p>")
    parts.append("<h2>Original response</h2>")
    if doc["target"] == "comprehension":
        for key, value in (doc["answers"] or {}).items():
            parts.append(f"<h3>{h(key)}</h3><div class=\"original\">{h(value) or '<span class=muted>no answer</span>'}</div>")
    else:
        parts.append(f"<p><strong>{h(what(row))}</strong></p>")
        parts.append(f"<div class=\"original\">{h(doc['comment']) or '<span class=muted>no comment</span>'}</div>")
    parts.append("<h2>Governed terms</h2>")
    if doc["terms"]:
        parts.append("<ul>" + "".join(
            f'<li><a href="/admin/?{urlencode({"term": t["term_id"]})}">{h(t["term_id"])}</a> <span class="muted">({h(t["basis"])} mapping)</span></li>'
            for t in doc["terms"]) + "</ul>")
    else:
        parts.append("<p class=\"muted\">Unmapped: no explicit or glossary-backed term mapping for this passage. Record the term below if you identify one.</p>")

    parts.append("<h2>Editorial record</h2>")
    if doc["dispositions"]:
        parts.append("<table><tr><th>When</th><th>By</th><th>Status</th><th>Problem</th><th>Fix belongs in</th><th>Rationale</th><th>Change</th><th>Follow-up evidence</th><th>Confirmed terms</th></tr>")
        for d in doc["dispositions"]:
            parts.append("<tr>" + "".join(f"<td>{h(v)}</td>" for v in (
                d["recorded_at"], d["recorded_by"], STATUS_LABELS.get(d["status"], d["status"]), d["problem"],
                FIX_LAYER_LABELS.get(d["fix_layer"], d["fix_layer"]), d["rationale"], d["change_reference"],
                d["follow_up_evidence"], d["confirmed_terms"])) + "</tr>")
        parts.append("</table>")
    else:
        parts.append("<p class=\"muted\">No disposition recorded yet. Current status: Received.</p>")
    status_choices = [(s, STATUS_LABELS[s]) for s in STATUSES]
    layer_choices = [(l, FIX_LAYER_LABELS[l]) for l in FIX_LAYERS]
    parts.append(
        f'<form method="post" action="/admin/submissions/{h(doc["public_id"])}/disposition">'
        f'<input type="hidden" name="csrf" value="{h(token)}">'
        f'<label class="block">Lifecycle step <select name="status">{options(status_choices, row["status"])}</select></label>'
        '<label class="block">Observed readability problem <textarea name="problem" rows="3" maxlength="2000"></textarea></label>'
        f'<label class="block">Where the fix belongs <select name="fix_layer">{options(layer_choices, "")}</select></label>'
        '<label class="block">Editorial rationale <textarea name="rationale" rows="3" maxlength="4000"></textarea></label>'
        '<label class="block">Reference to the resulting change (commit, PR, or notes file) <input name="change_reference" maxlength="300"></label>'
        '<label class="block">Follow-up evidence, only if actually collected (session code, export file, or later submission ids) <input name="follow_up_evidence" maxlength="500"></label>'
        '<label class="block">Confirmed or corrected term ids (comma-separated) <input name="confirmed_terms" maxlength="300"></label>'
        '<p><button type="submit">Record disposition</button></p>'
        '<p class="muted">Recording a disposition appends to the history above; nothing here changes a translation, a glossary entry, a term record, or a readability status.</p>'
        "</form>"
    )
    if doc["target"] == "comprehension":
        parts.append("<h2>Assessment</h2>")
        if doc["channel"] != "formal":
            parts.append("<p class=\"warn\">Public submission. It can be read and assessed for insight, but it never counts toward the newcomer threshold and is never exported as formal evidence.</p>")
        elif not row["counts_for_session"]:
            parts.append("<p class=\"warn\">A counted response already exists for this participant and body version; this one is kept as history and will not be exported.</p>")
        current = row["assessment"] or ""
        parts.append(
            f'<form method="post" action="/admin/submissions/{h(doc["public_id"])}/assessment">'
            f'<input type="hidden" name="csrf" value="{h(token)}">'
            f'<label class="block">Assessment against the question set\'s guidance <select name="assessment">{options([("", "Not assessed")] + [(a, a) for a in ASSESSMENTS], current)}</select></label>'
            f'<label class="block">Assessment note <textarea name="note" rows="3" maxlength="2000">{h(row["assessment_note"])}</textarea></label>'
            '<p><button type="submit">Record assessment</button></p>'
            "<p class=\"muted\">Accept reasonable paraphrases; house terminology is not required. The assessment guidance lives with the question set in the repository.</p>"
            "</form>"
        )
    return page(f"Submission {doc['public_id']}", "".join(parts), notice)


def sessions_page(app: "FeedbackApp", user: str, notice: str) -> str:
    storage = app.storage
    token = auth.csrf_token(app.settings.secret_key, user)
    rows = storage.sessions()
    body = ["<p>Formal review sessions run by a facilitator. Participants use a link carrying the session code and their anonymous label, so their responses are counted for this session and version only. Public feedback never appears here.</p>"]
    if rows:
        body.append("<table><tr><th>Code</th><th>Text</th><th>Title</th><th>Created</th><th>State</th></tr>")
        for row in rows:
            body.append(
                f'<tr><td><a href="/admin/sessions/{h(row["code"])}">{h(row["code"])}</a></td><td>{h(row["surface_key"])}</td>'
                f"<td>{h(row['title'])}</td><td>{h(row['created_at'][:10])}</td>"
                f"<td>{'closed ' + h(row['closed_at'][:10]) if row['closed_at'] else 'open'}</td></tr>"
            )
        body.append("</table>")
    body.append(
        '<h2>Create a session</h2><form method="post" action="/admin/sessions">'
        f'<input type="hidden" name="csrf" value="{h(token)}">'
        '<label class="block">Surface key (for example sn36_6) <input name="surface_key" required maxlength="32" pattern="[a-z0-9_]+"></label>'
        '<label class="block">Title (internal, no participant details) <input name="title" maxlength="120"></label>'
        '<label class="block">Facilitator note (internal) <textarea name="note" rows="2" maxlength="1000"></textarea></label>'
        '<p><button type="submit">Create session</button></p></form>'
    )
    return page("Formal sessions", "".join(body), notice)


def session_page(app: "FeedbackApp", user: str, session, notice: str) -> str:
    storage = app.storage
    token = auth.csrf_token(app.settings.secret_key, user)
    participants = storage.participants(session["id"])
    code = session["code"]
    body = [
        f"<p><a href=\"/admin/sessions\">← Sessions</a></p>",
        f"<p>Text <code>{h(session['surface_key'])}</code> · created {h(session['created_at'][:10])} · "
        f"{'closed ' + h(session['closed_at'][:10]) if session['closed_at'] else 'open'}</p>",
        f"<p>{h(session['title'])}</p>",
        f"<p class=\"muted\">{h(session['facilitator_note'])}</p>",
        "<h2>Participants</h2>",
    ]
    if participants:
        body.append("<table><tr><th>Label</th><th>Kind</th><th>Returning from</th><th>Independent</th><th>Participant link</th><th></th></tr>")
        for p in participants:
            earlier = ""
            if p["returning_from_participant_id"]:
                origin = storage.participant_by_id(p["returning_from_participant_id"])
                if origin:
                    origin_session = storage.connection.execute("SELECT code FROM sessions WHERE id = ?", (origin["session_id"],)).fetchone()
                    earlier = f"{origin_session['code'] if origin_session else '?'} / {origin['label']}"
            independent = {None: "not recorded", 0: "no", 1: "yes"}[p["independent"]]
            link = f"?{urlencode({'session': code, 'participant': p['label']})}"
            body.append(
                f"<tr><td>{h(p['label'])}</td><td>{h(p['kind'])}</td><td>{h(earlier)}</td><td>{h(independent)}</td>"
                f"<td><code>&lt;reader page URL&gt;{h(link)}</code></td>"
                f'<td><form method="post" action="/admin/sessions/{h(code)}/participants/{h(p["label"])}/independent">'
                f'<input type="hidden" name="csrf" value="{h(token)}">'
                '<select name="independent"><option value="">not recorded</option><option value="1">yes, unprompted</option><option value="0">no, prompted</option></select> '
                '<button type="submit">Save</button></form></td></tr>'
            )
        body.append("</table>")
    else:
        body.append("<p class=\"muted\">No participants yet.</p>")
    body.append(
        f'<h3>Add a participant</h3><form method="post" action="/admin/sessions/{h(code)}/participants">'
        f'<input type="hidden" name="csrf" value="{h(token)}">'
        '<label class="block">Anonymous label (for example R1) <input name="label" required maxlength="32" pattern="[A-Za-z0-9-]+"></label>'
        '<label class="block">Kind <select name="kind"><option value="fresh">Fresh newcomer</option><option value="returning">Returning reader</option></select></label>'
        '<label class="block">If returning: earlier session code / label (for example abcd1234/R1) <input name="returning_from" maxlength="70"></label>'
        '<p><button type="submit">Add participant</button></p></form>'
    )
    body.append("<h2>Responses</h2>")
    rows = storage.query({"session": code}, limit=500)
    if rows:
        body.append("<table><tr><th>Received</th><th>Participant</th><th>Target</th><th>Passage / term</th><th>Counts</th><th>Assessment</th></tr>")
        for row in rows:
            p = storage.participant_by_id(row["participant_id"]) if row["participant_id"] else None
            counts = "yes" if row["counts_for_session"] else ("—" if row["target"] != "comprehension" else "no (duplicate)")
            body.append(
                f'<tr><td><a href="/admin/submissions/{h(row["public_id"])}">{h(row["received_at"][:16].replace("T", " "))}</a></td>'
                f"<td>{h(p['label'] if p else '')}</td><td>{h(row['target'])}</td>"
                f"<td>{h(row['passage_id'] or row['glossary_term'] or '')}</td><td>{h(counts)}</td>"
                f"<td>{h(row['assessment'] or '')}</td></tr>"
            )
        body.append("</table>")
    else:
        body.append("<p class=\"muted\">No responses yet.</p>")
    toggle = "reopen" if session["closed_at"] else "close"
    body.append(
        f'<h2>Export</h2><p><a href="/admin/sessions/{h(code)}/export.json">Reviewed export (JSON)</a> — includes only assessed, counted comprehension responses from participants whose independence is recorded. '
        'Feed it to <code>python scripts/stage_feedback_evidence.py</code> in the repository.</p>'
        f'<form method="post" action="/admin/sessions/{h(code)}/{toggle}"><input type="hidden" name="csrf" value="{h(token)}">'
        f'<button type="submit">{toggle.capitalize()} session</button></form>'
    )
    return page(f"Session {code}", "".join(body), notice)


# ---------------------------------------------------------------------------
# POST
# ---------------------------------------------------------------------------

def _redirect(location: str, notice: str) -> "Response":
    from .app import Response

    return Response.redirect(f"{location}?{urlencode({'notice': notice})}")


def handle_post(app: "FeedbackApp", request: "Request", user: str, form: dict[str, str]) -> "Response":
    from .app import Response

    storage = app.storage
    parts = request.path.rstrip("/").split("/")
    clean = {k: " ".join(v.split()) if k != "problem" and k != "rationale" and k != "note" else v.strip()
             for k, v in form.items()}
    if len(parts) == 5 and parts[2] == "submissions":
        row = storage.submission(parts[3])
        if row is None:
            return Response.text("No such submission.\n", "404 Not Found")
        if parts[4] == "disposition":
            try:
                storage.record_disposition(
                    row["id"], user, clean.get("status", row["status"]),
                    problem=clean.get("problem", "")[:2000], fix_layer=clean.get("fix_layer", ""),
                    rationale=clean.get("rationale", "")[:4000],
                    change_reference=clean.get("change_reference", "")[:300],
                    follow_up_evidence=clean.get("follow_up_evidence", "")[:500],
                    confirmed_terms=clean.get("confirmed_terms", "")[:300],
                )
            except ValueError as error:
                return Response.text(f"{error}\n", "400 Bad Request")
            return _redirect(f"/admin/submissions/{row['public_id']}", "Disposition recorded.")
        if parts[4] == "assessment":
            assessment = clean.get("assessment", "")
            if not assessment:
                storage.connection.execute(
                    "UPDATE submissions SET assessment = NULL, assessment_note = ?, assessed_at = NULL WHERE id = ?",
                    (clean.get("note", "")[:2000], row["id"]),
                )
                return _redirect(f"/admin/submissions/{row['public_id']}", "Assessment cleared.")
            try:
                storage.record_assessment(row["id"], assessment, clean.get("note", "")[:2000])
            except ValueError as error:
                return Response.text(f"{error}\n", "400 Bad Request")
            return _redirect(f"/admin/submissions/{row['public_id']}", "Assessment recorded.")
    if parts == ["", "admin", "sessions"]:
        surface_key = clean.get("surface_key", "")
        if not surface_key or not surface_key.replace("_", "").isalnum():
            return Response.text("A surface key is required.\n", "400 Bad Request")
        session = storage.create_session(surface_key, clean.get("title", "")[:120], clean.get("note", "")[:1000])
        return _redirect(f"/admin/sessions/{session['code']}", "Session created.")
    if len(parts) >= 5 and parts[2] == "sessions":
        session = storage.session_by_code(parts[3])
        if session is None:
            return Response.text("No such session.\n", "404 Not Found")
        action = parts[4]
        if action == "participants" and len(parts) == 5:
            label = clean.get("label", "")
            if not label or not label.replace("-", "").isalnum():
                return Response.text("A label is required.\n", "400 Bad Request")
            kind = clean.get("kind", "fresh")
            returning_id = None
            origin = clean.get("returning_from", "")
            if kind == "returning":
                if "/" not in origin:
                    return Response.text("A returning participant needs an earlier session code and label.\n", "400 Bad Request")
                earlier_code, earlier_label = origin.split("/", 1)
                earlier_session = storage.session_by_code(earlier_code.strip())
                earlier = storage.participant(earlier_session["id"], earlier_label.strip()) if earlier_session else None
                if earlier is None:
                    return Response.text("The earlier session or participant does not exist.\n", "400 Bad Request")
                returning_id = earlier["id"]
            if storage.participant(session["id"], label) is not None:
                return Response.text("That label already exists in this session.\n", "400 Bad Request")
            storage.add_participant(session["id"], label, kind if kind in {"fresh", "returning"} else "fresh", returning_id)
            return _redirect(f"/admin/sessions/{session['code']}", f"Participant {label} added.")
        if action == "participants" and len(parts) == 7 and parts[6] == "independent":
            participant = storage.participant(session["id"], parts[5])
            if participant is None:
                return Response.text("No such participant.\n", "404 Not Found")
            value = clean.get("independent", "")
            storage.set_participant_independent(participant["id"], None if value == "" else value == "1")
            return _redirect(f"/admin/sessions/{session['code']}", "Independence recorded.")
        if action in {"close", "reopen"} and len(parts) == 5:
            storage.close_session(session["code"], action == "close")
            return _redirect(f"/admin/sessions/{session['code']}", f"Session {action}d.")
    return Response.text("Not found.\n", "404 Not Found")
