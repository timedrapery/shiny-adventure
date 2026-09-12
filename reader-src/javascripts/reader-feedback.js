(() => {
  "use strict";

  // Reader feedback is a progressive enhancement over the generated page.
  // The page carries a JSON manifest (surface, body version, passage ids,
  // term mappings, glossary versions, question set). This script attaches a
  // discreet control to each passage and to each glossary explanation, wires
  // the optional comprehension review, and posts to the submission service.
  //
  // Nothing appears unless the service answers a health probe, so a site
  // with no service deployed shows the ordinary page. The governed
  // translation is never modified; controls are appended beside it.

  const MANIFEST_ID = "reader-feedback-manifest";
  const HEALTH_CACHE_KEY = "reader-feedback-health";
  const SESSION_KEY = "reader-feedback-session";
  const HEALTH_TTL_MS = 10 * 60 * 1000;

  const CATEGORY_LABELS = [
    ["word", "I don’t understand a word or phrase."],
    ["sentence", "I understand the words, but not the sentence."],
    ["background", "I’m missing some background."],
    ["awkward", "The wording feels awkward."],
    ["other", "Something else."],
  ];
  const RATING_LABELS = [
    ["yes", "Yes"],
    ["partly", "Partly"],
    ["no", "No"],
  ];

  const MESSAGES = {
    sent: "Thank you. Your feedback was received.",
    sending: "Sending…",
    failed:
      "Your feedback could not be sent. Nothing you wrote has been lost; please try again in a moment.",
    rejected: "The service could not accept this feedback. Please check your answers and try again.",
    needCategory: "Choose one of the options first.",
    needAnswer: "Write an answer to at least one question first.",
  };

  // ---------------------------------------------------------------------
  // helpers
  // ---------------------------------------------------------------------

  function readManifest() {
    const node = document.getElementById(MANIFEST_ID);
    if (!node) return null;
    try {
      return JSON.parse(node.textContent);
    } catch (error) {
      return null;
    }
  }

  function normalize(text) {
    return (text || "").replace(/\s+/g, " ").trim();
  }

  function uuid() {
    if (window.crypto && typeof window.crypto.randomUUID === "function") {
      return window.crypto.randomUUID();
    }
    const bytes = new Uint8Array(16);
    if (window.crypto && window.crypto.getRandomValues) {
      window.crypto.getRandomValues(bytes);
    } else {
      for (let i = 0; i < 16; i += 1) bytes[i] = Math.floor(Math.random() * 256);
    }
    bytes[6] = (bytes[6] & 0x0f) | 0x40;
    bytes[8] = (bytes[8] & 0x3f) | 0x80;
    const hex = Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
    return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
  }

  function el(tag, attributes, children) {
    const node = document.createElement(tag);
    Object.entries(attributes || {}).forEach(([name, value]) => {
      if (value === null || value === undefined || value === false) return;
      if (name === "text") node.textContent = value;
      else if (name === "class") node.className = value;
      else node.setAttribute(name, value === true ? "" : value);
    });
    (children || []).forEach((child) => {
      if (child === null || child === undefined) return;
      node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
    });
    return node;
  }

  function storage(kind) {
    try {
      return window[kind];
    } catch (error) {
      return null;
    }
  }

  function readJSON(kind, key) {
    const store = storage(kind);
    if (!store) return null;
    try {
      const raw = store.getItem(key);
      return raw ? JSON.parse(raw) : null;
    } catch (error) {
      return null;
    }
  }

  function writeJSON(kind, key, value) {
    const store = storage(kind);
    if (!store) return;
    try {
      store.setItem(key, JSON.stringify(value));
    } catch (error) {
      /* storage may be unavailable; feedback still works without it */
    }
  }

  // ---------------------------------------------------------------------
  // endpoint and session
  // ---------------------------------------------------------------------

  function endpointFor(manifest) {
    if (typeof manifest.endpoint === "string" && manifest.endpoint) return manifest.endpoint;
    return ""; // same origin: the local service serves the built site itself
  }

  async function serviceIsHealthy(endpoint) {
    const cached = readJSON("sessionStorage", HEALTH_CACHE_KEY);
    if (cached && cached.endpoint === endpoint && Date.now() - cached.at < HEALTH_TTL_MS) {
      return cached.ok;
    }
    let ok = false;
    try {
      const response = await fetch(`${endpoint}/api/health`, { method: "GET", mode: "cors" });
      ok = response.ok;
    } catch (error) {
      ok = false;
    }
    writeJSON("sessionStorage", HEALTH_CACHE_KEY, { endpoint, ok, at: Date.now() });
    return ok;
  }

  function sessionContext() {
    // A facilitator hands a participant a link carrying the session code and
    // their anonymous label. Kept for the browser session so it follows the
    // reader to the next page; never stored longer.
    const params = new URLSearchParams(window.location.search);
    const code = normalize(params.get("session"));
    const participant = normalize(params.get("participant"));
    if (code && participant) {
      const context = { code, participant };
      writeJSON("sessionStorage", SESSION_KEY, context);
      return context;
    }
    return readJSON("sessionStorage", SESSION_KEY);
  }

  // ---------------------------------------------------------------------
  // submission
  // ---------------------------------------------------------------------

  function basePayload(manifest, session, target) {
    return {
      client_submission_id: uuid(),
      target,
      surface_key: manifest.surface_key,
      surface_label: manifest.surface_label,
      page_path: manifest.page_path,
      body_sha256: manifest.body_sha256,
      introduction_version: manifest.introduction ? manifest.introduction.version : null,
      manifest_format: manifest.format,
      session: session ? { code: session.code, participant: session.participant } : null,
    };
  }

  async function post(endpoint, payload) {
    const response = await fetch(`${endpoint}/api/submissions`, {
      method: "POST",
      mode: "cors",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (response.ok) return { ok: true };
    if (response.status === 400 || response.status === 413 || response.status === 422) {
      return { ok: false, rejected: true };
    }
    return { ok: false };
  }

  function setStatus(node, message, isError) {
    node.textContent = message;
    node.setAttribute("role", isError ? "alert" : "status");
    node.classList.toggle("reader-feedback__status--error", Boolean(isError));
  }

  // ---------------------------------------------------------------------
  // form pieces
  // ---------------------------------------------------------------------

  function honeypot() {
    return el("div", { hidden: true }, [
      el("label", {}, [
        "Leave this field empty ",
        el("input", { type: "text", name: "website", autocomplete: "off", tabindex: "-1" }),
      ]),
    ]);
  }

  function contactFields(manifest, prefix) {
    if (!manifest.contact_optin) return [];
    return [
      el("p", { class: "reader-feedback__field" }, [
        el("label", { for: `${prefix}-contact`, text: "Email address, only if you would like a reply (optional)" }),
        el("input", { id: `${prefix}-contact`, name: "contact", type: "email", autocomplete: "email", maxlength: "200" }),
      ]),
      el("p", { class: "reader-feedback__field" }, [
        el("label", {}, [
          el("input", { type: "checkbox", name: "contact_consent", value: "yes" }),
          " I agree that the editors may contact me once about this feedback. The address is stored separately from the feedback and deleted when the reply is sent.",
        ]),
      ]),
    ];
  }

  function noteLine(manifest) {
    return el("p", { class: "reader-feedback__note", text: manifest.reader_note });
  }

  // ---------------------------------------------------------------------
  // passage and introduction feedback
  // ---------------------------------------------------------------------

  function buildFeedbackForm(context) {
    const { manifest, session, endpoint, target, prefix, quote, extra, onDone } = context;
    const form = el("form", { class: "reader-feedback__form", id: `${prefix}-form`, novalidate: true });
    let submissionId = uuid();

    const legend = el("legend", { text: "What happened while you were reading this?" });
    const fieldset = el("fieldset", { class: "reader-feedback__choices" }, [legend]);
    CATEGORY_LABELS.forEach(([value, label], index) => {
      const input = el("input", { type: "radio", name: "category", value, id: `${prefix}-category-${index}` });
      fieldset.appendChild(el("label", { for: `${prefix}-category-${index}` }, [input, ` ${label}`]));
    });

    const commentId = `${prefix}-comment`;
    const comment = el("textarea", { id: commentId, name: "comment", rows: "3", maxlength: "2000" });
    const status = el("p", { class: "reader-feedback__status", role: "status", "aria-live": "polite" });

    const cancel = el("button", { type: "button", class: "reader-feedback__cancel", text: "Cancel" });
    const send = el("button", { type: "submit", class: "reader-feedback__submit", text: "Send feedback" });

    form.appendChild(el("blockquote", { class: "reader-feedback__passage" }, [quote]));
    form.appendChild(fieldset);
    form.appendChild(
      el("p", { class: "reader-feedback__field" }, [
        el("label", { for: commentId, text: "What did you think this meant, or where did you get stuck? (optional)" }),
        comment,
      ])
    );
    contactFields(manifest, prefix).forEach((node) => form.appendChild(node));
    form.appendChild(honeypot());
    form.appendChild(el("p", { class: "reader-feedback__actions" }, [send, " ", cancel]));
    form.appendChild(noteLine(manifest));
    form.appendChild(status);

    cancel.addEventListener("click", () => onDone(false));
    form.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        event.preventDefault();
        onDone(false);
      }
    });

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const data = new FormData(form);
      const category = data.get("category");
      if (!category) {
        setStatus(status, MESSAGES.needCategory, true);
        form.querySelector("input[name=category]").focus();
        return;
      }
      const payload = Object.assign(basePayload(manifest, session, target), extra, {
        client_submission_id: submissionId,
        category,
        comment: normalize(data.get("comment")).slice(0, 2000),
        website: data.get("website") || "",
      });
      if (manifest.contact_optin && normalize(data.get("contact"))) {
        payload.contact = {
          email: normalize(data.get("contact")),
          consent: data.get("contact_consent") === "yes",
        };
      }
      send.disabled = true;
      setStatus(status, MESSAGES.sending, false);
      const result = await post(endpoint, payload);
      send.disabled = false;
      if (result.ok) {
        submissionId = uuid();
        onDone(true);
        return;
      }
      // The same client id is reused on retry, so a request that reached the
      // service but lost its response cannot be stored twice.
      setStatus(status, result.rejected ? MESSAGES.rejected : MESSAGES.failed, true);
    });

    return form;
  }

  function attachControl(anchor, insertAfter, context) {
    const button = el("button", {
      type: "button",
      class: "reader-feedback__button",
      "aria-expanded": "false",
      "aria-controls": `${context.prefix}-form`,
      "aria-label": context.buttonLabel,
      text: "Give feedback",
    });
    const done = el("span", { class: "reader-feedback__done", hidden: true });
    let form = null;

    function close(sent) {
      if (form) {
        form.remove();
        form = null;
      }
      button.setAttribute("aria-expanded", "false");
      if (sent) {
        done.textContent = MESSAGES.sent;
        done.hidden = false;
      }
      button.focus();
    }

    button.addEventListener("click", () => {
      if (form) {
        close(false);
        return;
      }
      done.hidden = true;
      form = buildFeedbackForm(Object.assign({}, context, { onDone: close }));
      insertAfter.insertAdjacentElement("afterend", form);
      button.setAttribute("aria-expanded", "true");
      form.querySelector("input[name=category]").focus();
    });

    anchor.appendChild(document.createTextNode(" "));
    anchor.appendChild(button);
    anchor.appendChild(done);
  }

  function translationBlocks() {
    const start = document.querySelector("h2#translation");
    if (!start) return [];
    const blocks = [];
    const stop = new Set(["H2"]);
    const passageTags = new Set(["P", "UL", "OL", "BLOCKQUOTE", "PRE", "TABLE"]);
    let node = start.nextElementSibling;
    while (node && !stop.has(node.tagName) && !node.classList.contains("reader-terms")) {
      const candidates = node.classList.contains("reader-repeated-section")
        ? Array.from(node.children)
        : [node];
      candidates.forEach((candidate) => {
        if (!passageTags.has(candidate.tagName)) return;
        if (candidate.classList.contains("reader-section-progress")) return;
        blocks.push(candidate);
      });
      node = node.nextElementSibling;
    }
    return blocks;
  }

  function attachPassageControls(manifest, session, endpoint) {
    const blocks = translationBlocks();
    let cursor = 0;
    manifest.passages.forEach((passage) => {
      const prefix = normalize(passage.prefix);
      let found = null;
      for (let i = cursor; i < blocks.length; i += 1) {
        const text = normalize(blocks[i].textContent);
        if (text.startsWith(prefix)) {
          found = blocks[i];
          cursor = i + 1;
          break;
        }
      }
      if (!found) return; // fail closed: no control for an unmatched passage
      const shown = normalize(found.textContent);
      found.dataset.passageId = passage.id;
      if (!found.id) found.id = `passage-${passage.id}`;
      const glossaryVersions = {};
      const termIds = new Set(passage.terms.map((term) => term.id));
      Object.entries(manifest.glossary || {}).forEach(([term, info]) => {
        if (info.term_id && termIds.has(info.term_id)) glossaryVersions[term] = info.version;
      });
      attachControl(found, found, {
        manifest,
        session,
        endpoint,
        target: "translation",
        prefix: `reader-feedback-${passage.id}`,
        buttonLabel: "Give feedback on this passage",
        quote: shown.length > 600 ? `${shown.slice(0, 599)}…` : shown,
        extra: {
          passage_id: passage.id,
          passage_fingerprint: passage.fingerprint,
          passage_section: passage.section,
          passage_text: shown,
          terms: passage.terms,
          mapping: passage.mapping,
          glossary_versions: glossaryVersions,
        },
      });
    });
  }

  function attachIntroductionControl(manifest, session, endpoint) {
    const heading = document.querySelector("h2#before-you-read");
    if (!heading) return;
    const parts = [];
    let node = heading.nextElementSibling;
    let last = heading;
    while (node && node.tagName !== "H2") {
      parts.push(normalize(node.textContent));
      last = node;
      node = node.nextElementSibling;
    }
    const text = normalize(parts.join(" "));
    if (!text) return;
    const control = el("p", { class: "reader-feedback__control" });
    last.insertAdjacentElement("afterend", control);
    attachControl(control, control, {
      manifest,
      session,
      endpoint,
      target: "introduction",
      prefix: "reader-feedback-introduction",
      buttonLabel: "Give feedback on this introduction",
      quote: text.length > 600 ? `${text.slice(0, 599)}…` : text,
      extra: {
        introduction_kind: manifest.introduction ? manifest.introduction.kind : null,
        passage_text: text.slice(0, 2000),
      },
    });
  }

  // ---------------------------------------------------------------------
  // glossary feedback
  // ---------------------------------------------------------------------

  function attachGlossaryControls(manifest, session, endpoint) {
    const panel = document.querySelector("details.reader-terms dl");
    if (!panel || !manifest.glossary) return;
    Array.from(panel.querySelectorAll("dt")).forEach((dt, index) => {
      const dfn = dt.querySelector("dfn");
      const dd = dt.nextElementSibling;
      if (!dfn || !dd || dd.tagName !== "DD") return;
      const term = normalize(dfn.textContent);
      const info = manifest.glossary[term];
      if (!info) return;
      const prefix = `reader-feedback-gloss-${index}`;
      let submissionId = uuid();

      const form = el("form", { class: "reader-feedback__gloss", novalidate: true });
      const legend = el("legend", { text: `Did this explanation of “${term}” help?` });
      const fieldset = el("fieldset", { class: "reader-feedback__choices reader-feedback__choices--inline" }, [legend]);
      RATING_LABELS.forEach(([value, label], i) => {
        const input = el("input", { type: "radio", name: "rating", value, id: `${prefix}-rating-${i}` });
        fieldset.appendChild(el("label", { for: `${prefix}-rating-${i}` }, [input, ` ${label}`]));
      });
      const commentId = `${prefix}-comment`;
      const comment = el("textarea", { id: commentId, name: "comment", rows: "1", maxlength: "1000" });
      const status = el("p", { class: "reader-feedback__status", role: "status", "aria-live": "polite" });
      const send = el("button", { type: "submit", class: "reader-feedback__submit reader-feedback__submit--small", text: "Send" });

      form.appendChild(fieldset);
      form.appendChild(
        el("p", { class: "reader-feedback__field" }, [
          el("label", { for: commentId, text: "Comment (optional)" }),
          comment,
        ])
      );
      form.appendChild(honeypot());
      form.appendChild(el("p", { class: "reader-feedback__actions" }, [send]));
      form.appendChild(status);

      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const data = new FormData(form);
        const rating = data.get("rating");
        if (!rating) {
          setStatus(status, MESSAGES.needCategory, true);
          form.querySelector("input[name=rating]").focus();
          return;
        }
        const payload = Object.assign(basePayload(manifest, session, "glossary"), {
          client_submission_id: submissionId,
          glossary_term: term,
          glossary_version: info.version,
          terms: info.term_id ? [{ id: info.term_id, basis: "glossary" }] : [],
          mapping: info.term_id ? "mapped" : "unmapped",
          passage_text: normalize(dd.textContent).slice(0, 2000),
          rating,
          comment: normalize(data.get("comment")).slice(0, 1000),
          website: data.get("website") || "",
        });
        send.disabled = true;
        setStatus(status, MESSAGES.sending, false);
        const result = await post(endpoint, payload);
        send.disabled = false;
        if (result.ok) {
          submissionId = uuid();
          setStatus(status, MESSAGES.sent, false);
          form.querySelectorAll("input, textarea, button").forEach((node) => {
            node.disabled = true;
          });
          return;
        }
        setStatus(status, result.rejected ? MESSAGES.rejected : MESSAGES.failed, true);
      });

      dd.appendChild(form);
    });
  }

  // ---------------------------------------------------------------------
  // comprehension review
  // ---------------------------------------------------------------------

  function wireReview(manifest, session, endpoint) {
    const form = document.getElementById("reader-review");
    const review = manifest.comprehension;
    if (!form || !review) return;
    const status = form.querySelector(".reader-feedback__status");
    const send = form.querySelector("button[type=submit]");
    let submissionId = uuid();

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const data = new FormData(form);
      const answers = {};
      let anyAnswer = false;
      review.questions.forEach((question) => {
        const answer = normalize(data.get(question.id)).slice(0, 2000);
        answers[question.id] = answer;
        if (answer) anyAnswer = true;
      });
      if (!anyAnswer) {
        setStatus(status, MESSAGES.needAnswer, true);
        form.querySelector("textarea").focus();
        return;
      }
      const payload = Object.assign(basePayload(manifest, session, "comprehension"), {
        client_submission_id: submissionId,
        question_version: review.version,
        question_set_sha256: review.sha256,
        question_editorial_status: review.editorial_status,
        answers,
        familiarity: data.get("familiarity") || null,
        website: data.get("website") || "",
      });
      send.disabled = true;
      setStatus(status, MESSAGES.sending, false);
      const result = await post(endpoint, payload);
      send.disabled = false;
      if (result.ok) {
        submissionId = uuid();
        setStatus(status, MESSAGES.sent, false);
        form.querySelectorAll("textarea, input, button").forEach((node) => {
          node.disabled = true;
        });
        return;
      }
      setStatus(status, result.rejected ? MESSAGES.rejected : MESSAGES.failed, true);
    });
  }

  function revealSection(session) {
    const section = document.getElementById("reader-feedback");
    if (!section) return;
    section.hidden = false;
    if (session) {
      const heading = section.querySelector("h2");
      heading.insertAdjacentElement(
        "afterend",
        el("p", { class: "reader-feedback__session" }, [
          `Facilitated session ${session.code}, participant ${session.participant}. Your answers will be counted for this session only.`,
        ])
      );
    }
  }

  // ---------------------------------------------------------------------
  // entry point
  // ---------------------------------------------------------------------

  async function enhance() {
    const manifest = readManifest();
    if (!manifest || manifest.format !== 1) return;
    const root = document.querySelector("h2#translation");
    if (!root || root.dataset.readerFeedback === "ready") return;
    root.dataset.readerFeedback = "ready";

    const endpoint = endpointFor(manifest);
    if (!(await serviceIsHealthy(endpoint))) return;
    const session = sessionContext();

    revealSection(session);
    attachPassageControls(manifest, session, endpoint);
    attachIntroductionControl(manifest, session, endpoint);
    attachGlossaryControls(manifest, session, endpoint);
    wireReview(manifest, session, endpoint);
    document.documentElement.dataset.readerFeedback = "active";
  }

  enhance();
  if (typeof document$ !== "undefined") {
    document$.subscribe(() => {
      enhance();
    });
  }
})();
