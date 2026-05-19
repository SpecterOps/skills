# Delivery Platform Fields

Use this file when generating email templates for delivery platforms.

## GoPhish

Use GoPhish merge fields directly in the output:

- `{{.FirstName}}`
- `{{.LastName}}`
- `{{.Email}}`
- `{{.Position}}`
- `{{.URL}}`
- `{{.Tracker}}`

Guidance:

- Use `{{.URL}}` for the primary phishing link.
- Use `{{.Tracker}}` only when open tracking is wanted in the HTML body.
- In API-oriented output, the core template object is:
  - `name`
  - `subject`
  - `text`
  - `html`

## Phishmonger

Use Phishmonger substitution strings directly in the output.

Known common substitutions:

- `SuppliedPhishingLink`
- `SuppliedFirstName`

Guidance:

- Shape HTML so it can be pasted into captured email sections after decode / pretty-print steps.
- Prefer modular body fragments when the operator is templating a captured message.
- Keep content easy to test-send and revise.

## Selection Rule

- If mode is `gophish`, emit only GoPhish-native fields.
- If mode is `phishmonger`, emit only Phishmonger-native fields.
- If mode is `generic`, do not emit tool-native fields unless explicitly requested.
