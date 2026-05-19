---
name: pretext-brainstormer
description: Research recent public events and brainstorm phishing pretext ideas for a named target organization. Use when the user provides a client name and a phishing goal such as payload delivery or credential capture and wants timely subject ideas.
---

# Pretext Brainstormer

Research current public context for a target organization and generate timely pretext ideas tied to the user's phishing goal.

Read `../references/persuasion-principles.md` before scoring and ranking ideas.

## Required Inputs

- target organization name
- phishing goal

Supported goals:

- `payload delivery`
- `credential capture`

If the user gives a close variant such as `payload`, `installer`, `document`, `creds`, or `credential`, normalize it to one of the supported goals.

## Workflow

1. Research recent target context.
   - Search for recent news, press releases, events, product updates, policy changes, hiring pages, benefits pages, blog posts, leadership updates, and public-facing operational notices.
   - Prefer official sources first, then high-quality secondary coverage.

2. Extract usable anchors.
   - Pull out dated events, recurring initiatives, deadlines, office changes, benefits, technology rollouts, webinars, conferences, publications, and public controversies.
   - Record the exact terms the target uses for teams, programs, and locations.

3. Map anchors to the phishing goal.
   - For `payload delivery`, favor meetings, software updates, documents, invoices, statements, policies, templates, installers, and attachments.
   - For `credential capture`, favor SSO prompts, secure document portals, benefits access, HR systems, webmail, VPN, training, and meeting joins.

4. Score anchors against social-engineering principles.
   - Prefer ideas that naturally support one or more of:
     - Authority
     - Reciprocity
     - Greed
     - Commitment and consistency
     - Social proof
     - Liking
     - Scarcity
     - Curiosity
     - Fear and anxiety
     - Trust
     - Shame or embarrassment
   - Choose the principle that best fits the public anchor and requested goal.

5. Generate candidate pretexts.
   - Produce a list of concise subject ideas tied to recent anchors.
   - Keep each pretext plausible and easy to expand into an email or landing page.
   - Avoid ideas that rely on unsupported internal details.
   - Favor ideas where the social-engineering principle is obvious and supports the call to action.

6. Rank the ideas.
   - Put the strongest, most current, most target-specific ideas first.
   - Prefer pretexts with a clean explanation for the requested action.
   - Prefer ideas that combine timely public context with a strong persuasion principle.

## Output

Return:

1. Short research summary
2. A list of 8-15 pretext ideas
3. For each idea:
   - subject / theme
   - source anchor
   - social-engineering principle
   - why it fits the goal
   - suggested sender persona
   - suggested call to action
4. Top 3 recommendations

## Quality Rules

- Use current public information.
- Prefer exact dates where useful.
- Prefer official language from the target's own public materials.
- Keep ideas goal-aligned.
- Tag each idea with its primary persuasion principle.
- State when an idea is weaker or more generic.

## Example Triggers

- `Use Social Engineering to brainstorm pretexts for Acme Corp with the goal of payload delivery.`
- `Research recent events for Contoso and generate credential capture pretext ideas.`
