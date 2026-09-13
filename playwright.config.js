import { defineConfig } from "@playwright/test";
import { mkdirSync, rmSync } from "node:fs";

// The feedback browser tests need the submission service serving the built
// reader on its own origin, with a throwaway database. The credentials below
// exist only for that test database; the hash matches "browser-test-password".
mkdirSync("test-results", { recursive: true });
rmSync("test-results/feedback-browser-test.sqlite", { force: true });
const feedbackEnv = {
  FEEDBACK_DB: "test-results/feedback-browser-test.sqlite",
  FEEDBACK_SITE_DIR: "site",
  FEEDBACK_MAINTAINER_USER: "editor",
  FEEDBACK_MAINTAINER_PASSWORD_HASH:
    "pbkdf2_sha256$20000$7ae520310b85977bd762d144af16acff$64d8965a67e9e376be9056db6d478e34fdfc8d9604dea05d70d0bbf808b30fc0",
  FEEDBACK_SECRET_KEY: "browser-test-secret",
  FEEDBACK_RATE_LIMIT_PER_HOUR: "0",
};

export default defineConfig({
  testDir: "./tests/browser",
  timeout: 30_000,
  expect: { timeout: 8_000 },
  reporter: "line",
  use: {
    baseURL: process.env.READER_BASE_URL || "http://127.0.0.1:8000",
    browserName: "chromium",
    // An environment that ships its own Chromium can point at it instead of
    // downloading the version this package pins.
    launchOptions: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE
      ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE }
      : {},
  },
  webServer: [
    {
      command: "python -m http.server 8000 --directory site",
      url: "http://127.0.0.1:8000/",
      reuseExistingServer: true,
      timeout: 30_000,
    },
    {
      command: "python -m feedback_service serve --port 8765",
      url: "http://127.0.0.1:8765/api/health",
      reuseExistingServer: false,
      timeout: 30_000,
      env: feedbackEnv,
      // The service logs one line per request; keep the test output readable.
      stderr: "ignore",
    },
  ],
});
