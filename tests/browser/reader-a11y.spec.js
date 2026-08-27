import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readdirSync } from "node:fs";

const readerUtilityPages = [
  "/",
  "/start-here/",
  "/find-a-sutta/",
  "/glossary/",
];

const suttaPages = readdirSync(new URL("../../site/suttas/", import.meta.url), {
  withFileTypes: true,
})
  .filter((entry) => entry.isDirectory())
  .map((entry) => `/suttas/${entry.name}/`)
  .sort();

test("rendered accessibility suite covers the complete sutta corpus", () => {
  expect(suttaPages.length).toBeGreaterThan(50);
});

for (const path of [...readerUtilityPages, ...suttaPages]) {
  test(`${path} has no serious rendered accessibility violations`, async ({ page }) => {
    await page.goto(path);
    const results = await new AxeBuilder({ page }).analyze();
    const serious = results.violations.filter(({ impact }) =>
      ["serious", "critical"].includes(impact)
    );
    expect(serious).toEqual([]);
  });
}

test("sutta page reflows at 320 CSS pixels without horizontal scrolling", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 800 });
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/suttas/sn22-86-anuradha-sutta/");
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth
  );
  expect(overflow).toBeLessThanOrEqual(1);
});

test("skip link and disclosure panels work from the keyboard", async ({ page }) => {
  await page.goto("/suttas/sn22-86-anuradha-sutta/");
  const skip = page.locator("a.reader-skip-link");
  await skip.focus();
  await page.keyboard.press("Enter");
  await expect(page).toHaveURL(/#translation$/);

  const source = page.locator("details.reader-source-status");
  await source.locator("summary").focus();
  await page.keyboard.press("Enter");
  await expect(source).toHaveAttribute("open", "");
});

test("long repeated sections remain complete and can be collapsed", async ({ page }) => {
  await page.goto("/suttas/mn118-anapanasati-sutta/");
  const button = page.locator("button.reader-repeat-toggle").first();
  await expect(button).toBeVisible();
  await expect(button).toHaveAttribute("aria-expanded", "true");
  const controlled = await button.getAttribute("aria-controls");
  const section = page.locator(`#${controlled}`);
  await expect(section).toBeVisible();
  await button.click();
  await expect(button).toHaveAttribute("aria-expanded", "false");
  await expect(section).toBeHidden();
  await button.click();
  await expect(section).toBeVisible();
});

test("discovery filters narrow and restore the complete corpus", async ({ page }) => {
  await page.goto("/find-a-sutta/");
  const cards = page.locator(".sutta-card");
  const total = await cards.count();
  expect(total).toBeGreaterThan(40);
  await expect(page.locator(".sutta-card h2 > a:not(.headerlink)")).toHaveCount(total);
  await page.locator("#sutta-topic").selectOption("not-self");
  await expect(page.locator("#sutta-filter-count")).toContainText(`of ${total}`);
  expect(await page.locator(".sutta-card:visible").count()).toBeLessThan(total);
  await page.locator(".sutta-filters button[type='reset']").click();
  await expect(page.locator("#sutta-filter-count")).toHaveText(`Showing all ${total} suttas.`);
});

test("search finds an ASCII spelling of a Pali term", async ({ page }) => {
  await page.goto("/");
  const input = page.locator("input.md-search__input");
  await input.click();
  await input.fill("nibbana");
  await expect(page.locator(".md-search-result__item").first()).toBeVisible();
});
