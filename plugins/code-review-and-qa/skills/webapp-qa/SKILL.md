---
name: webapp-qa
description: Quick-invoke QA testing for a web app URL. Use when you want the `qa` subagent to smoke test, exercise flows, and run Lighthouse against a target URL.
icon: ./assets/icon.png
---

# QA — Web App Testing

Quick-invoke skill that delegates to the `qa` subagent. Parse the URL and optional flow instructions, then run a focused QA session.

## Argument Parsing

Args follow the pattern: `<url> [-- <flow instructions>]`

- **URL** — first token (required). Must start with `http://` or `https://`.
- **Flow instructions** — everything after ` -- ` (optional). Free text describing specific flows to test.
- **No args** — ask the user for the URL before proceeding.

**Examples:**
- `$webapp-qa http://localhost:3000` — full smoke test + Lighthouse on localhost
- `$webapp-qa https://staging.example.com -- test the login flow and dashboard` — targeted flow test
- `$webapp-qa http://localhost:4000 -- check that form validation works on signup` — form-specific QA
- `$webapp-qa` — ask user for URL

## Behavior

Parse args, then delegate to the `qa` agent with a focused prompt:

### If URL provided, no flow instructions:
Delegate with:
> Run a full QA session on `<url>`. Perform the smoke test, exercise all visible user flows (navigation, forms, buttons), and run a Lighthouse audit. Report all findings using the standard QA report format.

### If URL provided with flow instructions:
Delegate with:
> Run a QA session on `<url>`. Focus on: `<flow instructions>`. Also run a quick smoke test (console errors, network failures) and a Lighthouse audit. Report all findings using the standard QA report format.

### If no URL:
Ask the user:
> What URL should I test? (e.g., `http://localhost:3000`)
Then proceed with the full smoke test default.

## Delegation

Spawn the `qa` agent and pass the constructed prompt. The `qa` agent owns the browser session, interaction, and reporting.

Do not interact with the browser directly from this skill — that is the agent's responsibility.
