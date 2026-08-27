(() => {
  "use strict";

  // These sections contain long, intentionally repeated patterns. JavaScript
  // adds an optional collapse control, but the complete governed translation
  // remains visible by default and remains fully present when scripting is off.
  const collapsibleSections = {
    "mn10-satipatthana-sutta": [
      "Contemplation of Felt Experience",
      "Contemplation of the Heart",
      "Contemplation of Dhammas",
    ],
    "mn118-anapanasati-sutta": [
      "How Ānāpānasati Fulfills the Four Establishments of Sati",
      "How the Four Establishments of Sati Fulfill the Seven Awakening Factors",
      "How the Seven Awakening Factors Fulfill Knowledge and Release",
    ],
    "mn22-alagaddupama-sutta": [
      "The Full Sweep",
      "The Five Epithets of Liberation",
    ],
    "dn2-samannaphala-sutta": [
      "The Teachers Ajātasattu Consulted",
      "The Second Mental Theme",
      "The Third Mental Theme",
      "The Fourth Mental Theme",
    ],
    "dn15-mahanidana-sutta": [
      "Birth as Condition for Ageing and Dying",
      "Becoming as Condition for Birth",
      "Taking Personally as Condition for Becoming",
      "Ignorant Wanting as Condition for Taking Personally",
      "Felt Experience as Condition for Ignorant Wanting",
      "Contact as Condition for Felt Experience",
    ],
    "mn38-mahatanhasankhaya-sutta": [
      "The Arising Chain",
      "The Cessation Chain",
    ],
  };

  function currentSuttaSlug() {
    const parts = window.location.pathname.split("/").filter(Boolean);
    const suttaIndex = parts.lastIndexOf("suttas");
    return suttaIndex >= 0 ? parts[suttaIndex + 1] || "" : "";
  }

  function translationHeadings() {
    const translation = document.querySelector("h2#translation");
    if (!translation) return [];
    const headings = [];
    let node = translation.nextElementSibling;
    while (node && node.tagName !== "H2") {
      if (node.tagName === "H3") headings.push(node);
      node = node.nextElementSibling;
    }
    return headings;
  }

  function addSectionProgress(headings) {
    if (headings.length < 6) return;
    headings.forEach((heading, index) => {
      const marker = document.createElement("p");
      marker.className = "reader-section-progress";
      marker.textContent = `Section ${index + 1} of ${headings.length}`;
      heading.insertAdjacentElement("afterend", marker);
    });
  }

  function addCollapseControl(heading, index) {
    const content = document.createElement("div");
    const contentId = `reader-repeated-section-${index + 1}`;
    content.id = contentId;
    content.className = "reader-repeated-section";

    let node = heading.nextElementSibling;
    while (node && !["H2", "H3"].includes(node.tagName)) {
      const next = node.nextElementSibling;
      content.appendChild(node);
      node = next;
    }
    if (!content.childElementCount) return;

    const button = document.createElement("button");
    button.type = "button";
    button.className = "reader-repeat-toggle";
    button.setAttribute("aria-expanded", "true");
    button.setAttribute("aria-controls", contentId);
    button.textContent = "Hide this repeated pattern";
    button.addEventListener("click", () => {
      const expanded = button.getAttribute("aria-expanded") === "true";
      button.setAttribute("aria-expanded", String(!expanded));
      content.hidden = expanded;
      button.textContent = expanded
        ? "Show this repeated pattern"
        : "Hide this repeated pattern";
    });

    heading.insertAdjacentElement("afterend", content);
    heading.insertAdjacentElement("afterend", button);
  }

  function headingLabel(heading) {
    const copy = heading.cloneNode(true);
    copy.querySelector(".headerlink")?.remove();
    return copy.textContent.trim();
  }

  function enhanceReader() {
    const translation = document.querySelector("h2#translation");
    if (!translation || translation.dataset.readerGuidance === "ready") return;
    translation.dataset.readerGuidance = "ready";

    const headings = translationHeadings();
    addSectionProgress(headings);

    const wanted = new Set(collapsibleSections[currentSuttaSlug()] || []);
    headings
      .filter((heading) => wanted.has(headingLabel(heading)))
      .forEach(addCollapseControl);
  }

  enhanceReader();
  if (typeof document$ !== "undefined") {
    document$.subscribe(enhanceReader);
  }
})();
