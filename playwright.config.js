import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/browser",
  timeout: 30_000,
  expect: { timeout: 8_000 },
  reporter: "line",
  use: {
    baseURL: process.env.READER_BASE_URL || "http://127.0.0.1:8000",
    browserName: "chromium",
  },
  webServer: {
    command: "python -m http.server 8000 --directory site",
    url: "http://127.0.0.1:8000/",
    reuseExistingServer: true,
    timeout: 30_000,
  },
});
