---
name: phishing-email-html
description: Generate a phishing email in HTML from an approved pretext. Use when the task needs polished email copy plus HTML formatted for common delivery workflows such as GoPhish or Phishmonger.
icon: ./assets/icon.png
---

# Phishing Email HTML

Turn a researched pretext into a clean HTML email that renders well in common mail clients.

If `gophish` or `phishmonger` mode is requested, read `references/delivery-platform-fields.md` before drafting.
Also read `../references/persuasion-principles.md` to preserve the chosen persuasion principle in the copy.

## Delivery Modes

Support these output modes when requested:

- `generic`: plain subject, text, and HTML
- `gophish`: GoPhish-ready subject, text, HTML, and GoPhish merge fields
- `phishmonger`: Phishmonger-ready subject, HTML section text, and Phishmonger substitution fields

If no mode is specified, default to `generic`.

## Workflow

1. Start from the pretext.
   - Extract sender persona, subject, body copy, CTA, persuasion principle, and claims to avoid.
   - Keep the language aligned with the researched organizational voice.

2. Build the email content.
   - Produce a plain-text draft first.
   - Then convert it into simple table-based HTML.
   - Keep formatting restrained and enterprise-like.

3. Keep the markup portable.
   - Use inline CSS.
   - Prefer a single-column layout around 600px wide.
   - Avoid external assets unless the request explicitly needs them.

4. Preserve plausibility.
   - Use realistic footer/signature formatting.
   - Match the target's public naming for teams, offices, and programs.
   - Do not add unsupported policy claims.
   - Preserve the chosen persuasion principle in a subtle, consistent way.

5. Fit the delivery platform.
   - For GoPhish, use GoPhish-native merge fields directly in the subject, text, and HTML.
   - For Phishmonger, use Phishmonger-native substitution fields directly in the output.
   - Do not emit generic placeholders in `gophish` or `phishmonger` mode.

## Output

Return:

1. Subject line
2. Plain-text version
3. HTML version in a code block
4. Platform-specific notes on merge fields used

## HTML Rules

- Use tables for layout.
- Inline all CSS.
- Include a hidden preheader when useful.
- Keep fonts to common system-safe stacks.
- Make links and buttons easy to swap with placeholders.
- Avoid JavaScript, forms, and external CSS.

## GoPhish Notes

- Use `{{.URL}}` for the primary phishing link.
- Use recipient fields such as `{{.FirstName}}`, `{{.LastName}}`, `{{.Email}}`, and `{{.Position}}` when personalization helps.
- Add `{{.Tracker}}` when the user wants open tracking in the HTML template.
- Emit GoPhish merge fields directly in the template so GoPhish populates them at send time.
- When helpful, also return a JSON-ready object with:
  - `name`
  - `subject`
  - `text`
  - `html`

## Phishmonger Notes

- Prefer Phishmonger substitutions such as `SuppliedPhishingLink` and `SuppliedFirstName` when the content needs per-target replacement.
- Keep HTML modular so it can be pasted into a captured HTML content section after decode / pretty-print workflows.
- When useful, shape the output for Phishmonger capture and template workflows rather than for a generic ESP.
- Emit Phishmonger substitution fields directly in the template so Phishmonger populates them at send time.
- When helpful, also return:
  - subject
  - HTML body fragment
  - suggested find/replace markers
  - optional raw RFC 2045 email skeleton for import/capture workflows

## Generic Mode Placeholders

Only for `generic` mode:

- `{{recipient_name}}`
- `{{sender_name}}`
- `{{sender_title}}`
- `{{cta_url}}`
- `{{meeting_date}}`
- `{{meeting_time}}`

## Platform Placeholder Reference

- GoPhish:
  - `{{.URL}}`
  - `{{.Tracker}}`
  - `{{.FirstName}}`
  - `{{.LastName}}`
  - `{{.Email}}`
  - `{{.Position}}`
- Phishmonger:
  - `SuppliedPhishingLink`
  - `SuppliedFirstName`

## Example Triggers

- `Generate HTML for this phishing pretext.`
- `Turn this town hall lure into a realistic enterprise email template.`
- `Create the email copy and HTML body for a Zoom installer pretext.`
- `Generate a GoPhish-ready template with {{.URL}} and {{.Tracker}}.`
- `Generate a Phishmonger-ready HTML body using SuppliedPhishingLink.`
