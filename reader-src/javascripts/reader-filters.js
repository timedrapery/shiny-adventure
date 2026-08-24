(() => {
  "use strict";

  function labelThemeSearchDialog() {
    const search = document.querySelector(".md-search[role='dialog']");
    if (search && !search.hasAttribute("aria-label")) {
      search.setAttribute("aria-label", "Search the reader");
    }
  }

  labelThemeSearchDialog();
  if (typeof document$ !== "undefined") {
    document$.subscribe(labelThemeSearchDialog);
  }

  const form = document.querySelector(".sutta-filters");
  const cards = Array.from(document.querySelectorAll(".sutta-card"));
  const count = document.querySelector("#sutta-filter-count");
  if (!form || !cards.length || !count) return;

  const controls = {
    query: form.querySelector("[name='query']"),
    topic: form.querySelector("[name='topic']"),
    difficulty: form.querySelector("[name='difficulty']"),
    form: form.querySelector("[name='form']"),
    length: form.querySelector("[name='length']"),
  };

  const normalized = (value) => (value || "").trim().toLocaleLowerCase();

  function applyFilters() {
    const selected = {
      query: normalized(controls.query.value),
      topic: normalized(controls.topic.value),
      difficulty: normalized(controls.difficulty.value),
      form: normalized(controls.form.value),
      length: normalized(controls.length.value),
    };
    let visible = 0;
    for (const card of cards) {
      const topics = (card.dataset.topic || "").split("|");
      const matches =
        (!selected.query || (card.dataset.search || "").includes(selected.query)) &&
        (!selected.topic || topics.includes(selected.topic)) &&
        (!selected.difficulty || card.dataset.difficulty === selected.difficulty) &&
        (!selected.form || card.dataset.form === selected.form) &&
        (!selected.length || card.dataset.length === selected.length);
      card.hidden = !matches;
      if (matches) visible += 1;
    }
    count.textContent = visible === cards.length
      ? `Showing all ${cards.length} suttas.`
      : `Showing ${visible} of ${cards.length} suttas.`;
  }

  form.addEventListener("input", applyFilters);
  form.addEventListener("change", applyFilters);
  form.addEventListener("reset", () => window.setTimeout(applyFilters, 0));
})();
