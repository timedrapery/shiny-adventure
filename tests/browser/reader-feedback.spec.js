import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync } from "node:fs";

// These tests run against the feedback service serving the built reader on
// its own origin (see playwright.config.js), so the page's health probe
// succeeds and the feedback controls appear. The service uses a throwaway
// database under test-results/, so nothing here touches real feedback.

const FEEDBACK_BASE = process.env.FEEDBACK_BASE_URL || "http://127.0.0.1:8765";
const PILOT = `${FEEDBACK_BASE}/suttas/sn36-6-salla-sutta/`;
const OTHER = `${FEEDBACK_BASE}/suttas/an2-9-cariya-sutta/`;
const ADMIN_USER = "editor";
const ADMIN_PASSWORD = "browser-test-password";

// The committed config points the public site at the Google Form transport.
// The service-path tests below rewrite the manifest to use the local service
// instead, so both paths are exercised against the same build.
async function useServiceTransport(page) {
  await page.route(`${FEEDBACK_BASE}/suttas/**`, async (route) => {
    if (route.request().resourceType() !== "document") {
      await route.continue();
      return;
    }
    const pathname = new URL(route.request().url()).pathname.replace(/\/$/, "/index.html");
    const file = new URL(`../../site${pathname}`, import.meta.url);
    const body = readFileSync(file, "utf8").replace(/"transport":\s*\{[^}]*\}/, '"transport":null');
    await route.fulfill({ status: 200, contentType: "text/html; charset=utf-8", body });
  });
}

async function adminGet(request, path) {
  return request.get(`${FEEDBACK_BASE}${path}`, {
    headers: { Authorization: "Basic " + Buffer.from(`${ADMIN_USER}:${ADMIN_PASSWORD}`).toString("base64") },
  });
}

test.describe("passage feedback", () => {
  test.beforeEach(async ({ page }) => { await useServiceTransport(page); });

  test("controls appear only on the enabled pilot text, after the service answers", async ({ page }) => {
    await page.goto(PILOT);
    const buttons = page.locator("button.reader-feedback__button");
    await expect(buttons.first()).toBeVisible();
    expect(await buttons.count()).toBeGreaterThan(30);
    await expect(page.locator("#reader-feedback")).toBeVisible();

    await page.goto(OTHER);
    await expect(page.locator("button.reader-feedback__button")).toHaveCount(0);
    await expect(page.locator("#reader-feedback")).toHaveCount(0);
  });

  test("the enhanced page has no serious accessibility violations", async ({ page }) => {
    await page.goto(PILOT);
    await expect(page.locator("button.reader-feedback__button").first()).toBeVisible();
    await page.locator("button.reader-feedback__button").first().click();
    await expect(page.locator("form.reader-feedback__form")).toBeVisible();
    const results = await new AxeBuilder({ page }).analyze();
    const serious = results.violations.filter(({ impact }) => ["serious", "critical"].includes(impact));
    expect(serious).toEqual([]);
  });

  test("keyboard: open with Enter, choose an option, submit, and the feedback reaches storage", async ({ page, request }) => {
    await page.goto(PILOT);
    const passage = page.locator("[data-passage-id='p009']");
    await expect(passage).toContainText("They feel it twice");
    const button = passage.locator("button.reader-feedback__button");
    await button.focus();
    await page.keyboard.press("Enter");
    await expect(button).toHaveAttribute("aria-expanded", "true");
    const form = page.locator("#reader-feedback-p009-form");
    await expect(form).toBeVisible();
    await expect(form.locator("blockquote")).toContainText("They feel it twice");
    await expect(form.locator("input[name=category]").first()).toBeFocused();
    await page.keyboard.press("ArrowDown"); // second option: the sentence, not the words
    await page.keyboard.press("Tab");
    await page.keyboard.type("Twice? I thought there was one arrow so far. <b>not markup</b>");
    await page.keyboard.press("Tab");
    await page.keyboard.press("Enter");
    await expect(passage.locator(".reader-feedback__done")).toContainText("received");
    await expect(button).toBeFocused();

    const response = await adminGet(request, "/admin/export.json?passage=p009&surface=sn36_6");
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    const record = data.submissions.find((s) => s.comment.startsWith("Twice? I thought"));
    expect(record).toBeTruthy();
    expect(record.category).toBe("sentence");
    expect(record.body_sha256).toMatch(/^[0-9a-f]{64}$/);
    expect(record.passage_text).toBe("They feel it twice: once in the body and once in the mind.");
    expect(record.terms.map((t) => t.id)).toContain("sn36-6-two-feelings-painful-feeling");
    expect(record.introduction_version).toMatch(/^[0-9a-f]{12}$/);
    expect(record.channel).toBe("public");
  });

  test("a failed submission keeps the form contents and a retry does not duplicate", async ({ page, request }) => {
    await page.goto(PILOT);
    const passage = page.locator("[data-passage-id='p010']");
    await passage.locator("button.reader-feedback__button").click();
    const form = page.locator("#reader-feedback-p010-form");
    await form.locator("input[name=category][value=background]").check();
    await form.locator("textarea[name=comment]").fill("Who is shooting the arrows? unique-retry-marker");

    // First attempt: the service is unreachable from the page's point of view.
    await page.route("**/api/submissions", (route) => route.abort("connectionrefused"));
    await form.locator("button[type=submit]").click();
    const status = form.locator(".reader-feedback__status");
    await expect(status).toContainText("could not be sent");
    await expect(status).toHaveAttribute("role", "alert");
    await expect(form.locator("textarea[name=comment]")).toHaveValue("Who is shooting the arrows? unique-retry-marker");
    await expect(form.locator("input[name=category][value=background]")).toBeChecked();

    // Second attempt: the request reaches the service, but the reply is lost.
    await page.unroute("**/api/submissions");
    await page.route("**/api/submissions", async (route) => {
      await route.fetch();
      await route.abort("failed");
    });
    await form.locator("button[type=submit]").click();
    await expect(status).toContainText("could not be sent");

    // Third attempt succeeds and must reuse the same client id.
    await page.unroute("**/api/submissions");
    await form.locator("button[type=submit]").click();
    await expect(passage.locator(".reader-feedback__done")).toContainText("received");

    const response = await adminGet(request, "/admin/export.json?passage=p010");
    const data = await response.json();
    const matches = data.submissions.filter((s) => s.comment.includes("unique-retry-marker"));
    expect(matches).toHaveLength(1);
  });

  test("works on a phone-sized viewport", async ({ browser }) => {
    const phone = await browser.newContext({ viewport: { width: 360, height: 740 }, hasTouch: true, isMobile: true });
    const page = await phone.newPage();
    await useServiceTransport(page);
    await page.goto(PILOT);
    const passage = page.locator("[data-passage-id='p022']");
    await passage.locator("button.reader-feedback__button").tap();
    const form = page.locator("#reader-feedback-p022-form");
    await expect(form).toBeVisible();
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth
    );
    expect(overflow).toBeLessThanOrEqual(1);
    await form.locator("label[for='reader-feedback-p022-category-3']").tap();
    await form.locator("button[type=submit]").tap();
    await expect(passage.locator(".reader-feedback__done")).toContainText("received");
    await phone.close();
  });

  test("escape closes the form and returns focus to the control", async ({ page }) => {
    await page.goto(PILOT);
    const passage = page.locator("[data-passage-id='p001']");
    const button = passage.locator("button.reader-feedback__button");
    await button.click();
    await expect(page.locator("#reader-feedback-p001-form")).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(page.locator("#reader-feedback-p001-form")).toHaveCount(0);
    await expect(button).toBeFocused();
    await expect(button).toHaveAttribute("aria-expanded", "false");
  });
});

test.describe("glossary and comprehension feedback", () => {
  test.beforeEach(async ({ page }) => { await useServiceTransport(page); });

  test("glossary rating records the explanation version", async ({ page, request }) => {
    await page.goto(PILOT);
    await expect(page.locator("button.reader-feedback__button").first()).toBeVisible();
    const terms = page.locator("details.reader-terms");
    await terms.locator("summary").click();
    const gloss = terms.locator("form.reader-feedback__gloss").filter({ hasText: "underlying tendency" });
    await gloss.locator("input[name=rating][value=partly]").check();
    await gloss.locator("textarea[name=comment]").fill("Underneath what? glossary-marker");
    await gloss.locator("button[type=submit]").click();
    await expect(gloss.locator(".reader-feedback__status")).toContainText("received");

    const response = await adminGet(request, "/admin/export.json?target=glossary");
    const data = await response.json();
    const record = data.submissions.find((s) => s.comment.includes("glossary-marker"));
    expect(record.glossary_term).toBe("underlying tendency");
    expect(record.glossary_version).toMatch(/^[0-9a-f]{12}$/);
    expect(record.rating).toBe("partly");
    expect(record.terms.map((t) => t.id)).toEqual(["anusaya"]);
  });

  test("the optional review is submitted with its question version, and public answers never count", async ({ page, request }) => {
    await page.goto(PILOT);
    const review = page.locator("#reader-review");
    await expect(review).toBeVisible();
    await review.locator("#reader-review-paraphrase").fill("Two people feel the same pain; one adds a second layer. review-marker");
    await review.locator("#reader-review-arrows").fill("The pain, and being upset about the pain.");
    await review.locator("input[name=familiarity][value=new]").check();
    await review.locator("button[type=submit]").click();
    await expect(review.locator(".reader-feedback__status")).toContainText("received");

    const response = await adminGet(request, "/admin/export.json?target=comprehension");
    const data = await response.json();
    const record = data.submissions.find((s) => (s.answers.paraphrase || "").includes("review-marker"));
    expect(record.question_version).toBe(1);
    expect(record.question_editorial_status).toBe("draft");
    expect(record.question_set_sha256).toMatch(/^[0-9a-f]{64}$/);
    expect(record.familiarity).toBe("new");
    expect(record.channel).toBe("public");
    expect(record.counts_for_session).toBe(0);
  });
});

test.describe("maintainer access", () => {
  test.beforeEach(async ({ page }) => { await useServiceTransport(page); });

  test("the queue and exports refuse unauthenticated and wrongly authenticated requests", async ({ request }) => {
    for (const path of ["/admin/", "/admin/export.json", "/admin/terms", "/admin/sessions"]) {
      const anonymous = await request.get(`${FEEDBACK_BASE}${path}`);
      expect(anonymous.status()).toBe(401);
      const wrong = await request.get(`${FEEDBACK_BASE}${path}`, {
        headers: { Authorization: "Basic " + Buffer.from("editor:nope-nope-nope").toString("base64") },
      });
      expect(wrong.status()).toBe(401);
      expect(await wrong.text()).not.toContain("marker");
    }
  });

  test("submitted markup is escaped in the queue and the page carries no scripts", async ({ page }) => {
    await page.goto(PILOT);
    const passage = page.locator("[data-passage-id='p003']");
    await passage.locator("button.reader-feedback__button").click();
    const form = page.locator("#reader-feedback-p003-form");
    await form.locator("input[name=category][value=other]").check();
    await form.locator("textarea[name=comment]").fill('<img src=x onerror="document.title=\'pwned\'"> xss-marker');
    await form.locator("button[type=submit]").click();
    await expect(passage.locator(".reader-feedback__done")).toContainText("received");

    const admin = await page.context().browser().newContext({
      httpCredentials: { username: ADMIN_USER, password: ADMIN_PASSWORD },
    });
    const queue = await admin.newPage();
    const fired = [];
    queue.on("dialog", (d) => { fired.push(d.message()); d.dismiss(); });
    await queue.goto(`${FEEDBACK_BASE}/admin/?passage=p003`);
    await expect(queue.locator("body")).toContainText("xss-marker");
    expect(await queue.locator("img").count()).toBe(0);
    expect(await queue.locator("script").count()).toBe(0);
    await expect(queue).not.toHaveTitle(/pwned/);
    const link = queue.locator("table a").filter({ hasText: /\d{4}-\d{2}-\d{2}/ }).first();
    await link.click();
    await expect(queue.locator("blockquote")).toContainText("So what's the difference");
    await expect(queue.locator(".original")).toContainText("<img src=x");
    expect(await queue.locator("img").count()).toBe(0);
    expect(fired).toEqual([]);
    await admin.close();
  });

  test("a maintainer can record a disposition from the queue", async ({ browser }) => {
    const admin = await browser.newContext({
      httpCredentials: { username: ADMIN_USER, password: ADMIN_PASSWORD },
    });
    const queue = await admin.newPage();
    await queue.goto(`${FEEDBACK_BASE}/admin/?surface=sn36_6&target=translation`);
    await queue.locator("table a").filter({ hasText: /\d{4}-\d{2}-\d{2}/ }).first().click();
    await queue.locator("select[name=status]").selectOption("examined");
    await queue.locator("textarea[name=problem]").fill("Reader lost the antecedent of 'twice'.");
    await queue.locator("select[name=fix_layer]").selectOption("translation");
    await queue.locator("textarea[name=rationale]").fill("The second arrow is introduced only after this line.");
    await queue.locator("input[name=change_reference]").fill("to be decided");
    await queue.locator("button", { hasText: "Record disposition" }).click();
    await expect(queue.locator(".notice")).toContainText("Disposition recorded");
    await expect(queue.locator("table").last()).toContainText("Examined");
    await expect(queue.locator("table").last()).toContainText("Translation");
    await admin.close();
  });
});

test.describe("google form transport (the committed public configuration)", () => {
  test("the page posts the submission as one JSON field to the editors' form", async ({ page }) => {
    const posts = [];
    await page.route("https://docs.google.com/**", async (route) => {
      posts.push({ url: route.request().url(), body: route.request().postData() || "" });
      await route.fulfill({ status: 200, body: "" });
    });
    await page.goto(PILOT);
    const passage = page.locator("[data-passage-id='p013']");
    await expect(passage.locator("button.reader-feedback__button")).toBeVisible();
    await passage.locator("button.reader-feedback__button").click();
    const form = page.locator("#reader-feedback-p013-form");
    await form.locator("input[name=category][value=word]").check();
    await form.locator("textarea[name=comment]").fill("What is an underlying tendency? form-marker");
    await form.locator("button[type=submit]").click();
    await expect(passage.locator(".reader-feedback__done")).toContainText("received");
    expect(posts).toHaveLength(1);
    expect(posts[0].url).toMatch(/^https:\/\/docs\.google\.com\/forms\/d\/e\/[A-Za-z0-9_-]+\/formResponse$/);
    const match = posts[0].body.match(/name="entry\.1359254143"\r?\n\r?\n([\s\S]*?)\r?\n--/);
    expect(match).toBeTruthy();
    const payload = JSON.parse(match[1]);
    expect(payload.target).toBe("translation");
    expect(payload.passage_id).toBe("p013");
    expect(payload.comment).toContain("form-marker");
    expect(payload.body_sha256).toMatch(/^[0-9a-f]{64}$/);
    expect(payload.client_submission_id).toMatch(/^[0-9a-f-]{36}$/);
    expect(payload.terms.map((t) => t.id)).toContain("patigha");
  });

  test("a failed post to the form keeps the form contents", async ({ page }) => {
    await page.route("https://docs.google.com/**", (route) => route.abort("connectionrefused"));
    await page.goto(PILOT);
    const passage = page.locator("[data-passage-id='p014']");
    await passage.locator("button.reader-feedback__button").click();
    const form = page.locator("#reader-feedback-p014-form");
    await form.locator("input[name=category][value=awkward]").check();
    await form.locator("textarea[name=comment]").fill("keep me");
    await form.locator("button[type=submit]").click();
    await expect(form.locator(".reader-feedback__status")).toContainText("could not be sent");
    await expect(form.locator("textarea[name=comment]")).toHaveValue("keep me");
  });
});
