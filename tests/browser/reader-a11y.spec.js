import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const representativePages = [
  "/",
  "/start-here/",
  "/find-a-sutta/",
  "/suttas/sn22-86-anuradha-sutta/",
  "/suttas/mn131-bhaddekaratta-sutta/",
  "/glossary/",
];

for (const path of representativePages) {
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
