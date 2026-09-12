-- Reader feedback service: initial schema.
--
-- Submissions are stored exactly as validated. Text a reader typed is kept
-- verbatim in the *_text / comment / answers columns and is escaped when
-- rendered; it is never trusted as markup. Version columns record what the
-- reader actually saw so a revision can be judged against them later.

CREATE TABLE sessions (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    surface_key TEXT NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    facilitator_note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    closed_at TEXT
);

CREATE TABLE participants (
    id INTEGER PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    label TEXT NOT NULL,
    kind TEXT NOT NULL CHECK (kind IN ('fresh', 'returning')),
    returning_from_participant_id INTEGER REFERENCES participants(id),
    independent INTEGER,                  -- 1 unprompted, 0 prompted, NULL not yet recorded
    created_at TEXT NOT NULL,
    UNIQUE (session_id, label)
);

CREATE TABLE submissions (
    id INTEGER PRIMARY KEY,
    public_id TEXT NOT NULL UNIQUE,
    client_submission_id TEXT NOT NULL UNIQUE,
    received_at TEXT NOT NULL,
    channel TEXT NOT NULL CHECK (channel IN ('public', 'formal')),
    session_id INTEGER REFERENCES sessions(id),
    participant_id INTEGER REFERENCES participants(id),
    target TEXT NOT NULL CHECK (target IN ('translation', 'glossary', 'introduction', 'comprehension')),
    surface_key TEXT NOT NULL,
    surface_label TEXT NOT NULL DEFAULT '',
    page_path TEXT NOT NULL DEFAULT '',
    body_sha256 TEXT NOT NULL,
    passage_id TEXT,
    passage_fingerprint TEXT,
    passage_section TEXT,
    passage_text TEXT,
    introduction_kind TEXT,
    introduction_version TEXT,
    glossary_term TEXT,
    glossary_version TEXT,
    glossary_versions_json TEXT NOT NULL DEFAULT '{}',
    terms_json TEXT NOT NULL DEFAULT '[]',
    mapping TEXT,
    category TEXT,
    rating TEXT,
    comment TEXT NOT NULL DEFAULT '',
    question_version INTEGER,
    question_set_sha256 TEXT,
    question_editorial_status TEXT,
    answers_json TEXT,
    familiarity TEXT,
    counts_for_session INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'received'
        CHECK (status IN ('received', 'examined', 'proposed', 'revised', 'checked')),
    assessment TEXT CHECK (assessment IN ('pass', 'fail', 'unclear')),
    assessment_note TEXT NOT NULL DEFAULT '',
    assessed_at TEXT
);

CREATE INDEX submissions_surface ON submissions (surface_key, passage_id);
CREATE INDEX submissions_status ON submissions (status);
CREATE INDEX submissions_session ON submissions (session_id, participant_id);

CREATE TABLE submission_terms (
    submission_id INTEGER NOT NULL REFERENCES submissions(id) ON DELETE CASCADE,
    term_id TEXT NOT NULL,
    basis TEXT NOT NULL,
    PRIMARY KEY (submission_id, term_id)
);

CREATE INDEX submission_terms_term ON submission_terms (term_id);

CREATE TABLE dispositions (
    id INTEGER PRIMARY KEY,
    submission_id INTEGER NOT NULL REFERENCES submissions(id) ON DELETE CASCADE,
    recorded_at TEXT NOT NULL,
    recorded_by TEXT NOT NULL,
    status TEXT NOT NULL,
    problem TEXT NOT NULL DEFAULT '',
    fix_layer TEXT NOT NULL DEFAULT '',
    rationale TEXT NOT NULL DEFAULT '',
    change_reference TEXT NOT NULL DEFAULT '',
    follow_up_evidence TEXT NOT NULL DEFAULT '',
    confirmed_terms TEXT NOT NULL DEFAULT ''
);

-- Optional follow-up contact, kept apart from the feedback itself so it can
-- be deleted independently and never appears in queue views or exports.
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY,
    submission_id INTEGER NOT NULL UNIQUE REFERENCES submissions(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    consent_text TEXT NOT NULL,
    recorded_at TEXT NOT NULL
);

-- Proportionate spam protection: a sliding window per hashed client.
CREATE TABLE rate_events (
    client_hash TEXT NOT NULL,
    at TEXT NOT NULL
);

CREATE INDEX rate_events_client ON rate_events (client_hash, at);
