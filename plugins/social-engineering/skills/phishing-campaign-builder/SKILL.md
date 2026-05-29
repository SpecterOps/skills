---
name: phishing-campaign-builder
description: Run the end-to-end phishing pretext workflow from research to final email. Use when the user has a target organization and phishing goal and wants Codex to brainstorm, refine, and produce the final email copy or HTML in one sequence.
metadata:
  author: "GhostWorks"
---

# Phishing Campaign Builder

Run the social-engineering workflow in this order:

1. `pretext-brainstormer`
2. `phishing-pretext`
3. `phishing-email-html`

Optionally continue with:

4. `credential-harvest-landing-page-copy`
5. `vishing-pretext`

## Required Inputs

- target organization
- phishing goal

Optional inputs:

- audience or role
- delivery mode: `generic`, `gophish`, or `phishmonger`
- preferred persuasion principle
- call to action

## Workflow

1. Brainstorm.
   - Use `pretext-brainstormer` to research current public context and rank pretext options.

2. Choose the best pretext.
   - Select the strongest idea unless the user already chose one.
   - Favor current, target-specific, goal-aligned ideas with a clean persuasion principle.

3. Refine the pretext.
   - Use `phishing-pretext` to research org voice, department names, and sender persona.
   - Produce the polished pretext draft.

4. Build the email.
   - Use `phishing-email-html` to generate the subject, plain text, and HTML.
   - If a delivery mode is specified, format the output for that platform.

5. Extend when needed.
   - If the goal is credential capture and a landing page is needed, use `credential-harvest-landing-page-copy`.
   - If the user wants phone follow-up, use `vishing-pretext`.

## Output

Return:

1. Top brainstormed ideas
2. Chosen pretext
3. Sender persona / department
4. Primary persuasion principle
5. Subject line
6. Plain-text email
7. HTML email
8. Optional landing-page copy or vishing script if requested

## Rules

- Use current public information.
- Prefer official target language.
- Keep the chosen persuasion principle subtle and consistent.
- Do not add unsupported policy claims.
- Keep outputs concise and reusable.

## Example Triggers

- `Use Social Engineering to build a phishing campaign for Acme with the goal of payload delivery.`
- `Run the full phishing workflow for Contoso targeting help desk users in GoPhish mode.`
