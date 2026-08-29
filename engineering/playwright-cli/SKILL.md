---
name: playwright-cli
description: Author, maintain, and run a persistent, CI-runnable Playwright test suite from the command line — writing .spec.ts files, using codegen to record flows, and running `npx playwright test`. Use when the user wants to write Playwright tests, build or extend a test suite, record a test with codegen, run tests / see the HTML report, or needs durable browser test coverage that lives in the repo and runs in CI. NOT for one-off live browser driving or ad-hoc page inspection — that is the job of the `playwright` MCP plugin, which drives a real browser interactively but leaves nothing behind in the repo.
---

# Playwright CLI test authoring

**Scope note:** this skill produces durable artifacts — `.spec.ts` files committed to the repo and runnable in CI. If the task is "go check what's on this page" or "click through this flow and tell me what happens" with no lasting test file wanted, use the `playwright` MCP plugin instead (it launches `npx @playwright/mcp@latest` for live, interactive browser control). Use this skill when the output should be a test that runs again tomorrow, in CI, without Claude in the loop.

## 1. Ensure the project has `@playwright/test`

```bash
# check first — don't reinstall if already present
cat package.json | grep -q '"@playwright/test"' || npm install -D @playwright/test
npx playwright --version
```

If there's no `playwright.config.ts` yet, scaffold one (`npx playwright install` to get browser binaries, then create a minimal config with `testDir: './tests'` or match the repo's existing test directory convention).

## 2. Record with codegen, don't hand-write locators

```bash
npx playwright codegen <url>
```

This opens a browser; interacting with the page emits Playwright code in real time. Use it to get real locators (`getByRole`, `getByText`, etc.) instead of guessing selectors. Copy the generated actions into a `.spec.ts` file rather than pasting the whole codegen dump — trim to the assertions and actions that matter, and add explicit `expect(...)` checks (codegen alone won't add meaningful assertions).

```bash
# record against a specific browser / device if relevant
npx playwright codegen --browser=firefox <url>
npx playwright codegen --device="iPhone 13" <url>
```

## 3. Structure specs

- Check for an existing pattern first (`tests/`, `e2e/`, page-object files) and follow it — don't introduce a second convention.
- If the repo has no pattern yet: flat `*.spec.ts` files grouped by feature/flow is fine for a small suite. Reach for Page Object Model only once specs start duplicating the same locators/actions across files.
- One `test.describe` per user-facing flow; keep individual `test()` blocks focused on one behavior so failures are easy to localize.

## 4. Run and iterate

```bash
npx playwright test                       # full suite, headless
npx playwright test path/to/file.spec.ts  # one file
npx playwright test -g "test name"        # by title
npx playwright test --ui                  # interactive UI mode — best for debugging a failing spec
npx playwright test --headed              # watch it run in a real window
```

## 5. Read results

```bash
npx playwright show-report   # opens the last HTML report (traces, screenshots, videos on failure)
```

If a test fails, prefer `--ui` or `--trace on` over re-reading raw terminal output — the trace viewer shows the DOM state and network at the point of failure.

## 6. CI

Playwright's test runner is CI-agnostic — `npx playwright test` is the entrypoint any CI system calls. Check whether the repo already has a workflow (`.github/workflows/*.yml` referencing `playwright`) before adding a new one; if adding one, install browsers with `npx playwright install --with-deps` in the CI step before running tests.
