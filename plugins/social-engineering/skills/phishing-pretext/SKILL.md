---
name: phishing-pretext
description: Research and draft a target-specific phishing email pretext. Use when building or refining a believable lure for a named company, policy change, department, or employee audience and when the work benefits from current public-source research.
metadata:
  author: "GhostWorks"
---

# Phishing Pretext

Build a believable pretext by grounding it in current public information, matching the target's public voice, and removing claims that are easy to falsify.

Read `../../references/persuasion-principles.md` when selecting the pretext's primary persuasion principle.

## Input Parsing

Interpret the request as having these fields when available:

- target organization
- audience or role
- pretext theme
- delivery channel
- payload or call to action
- constraints to avoid

If some are missing, infer them from the request and proceed.

## Workflow

1. Identify the anchor.
   - Extract the concrete event, policy, initiative, deadline, or workflow change that makes the lure timely.
   - Prefer anchors with a real date, named team, or public artifact.

2. Research current facts.
   - Search the web for official pages first.
   - Use high-authority secondary sources only to confirm timing or context.
   - Capture exact department names, office names, benefit names, and policy wording when available.

3. Model organizational voice.
   - Read 2-4 public pages from the target such as benefits, careers, press releases, leadership pages, event invites, or policy pages.
   - Note recurring phrasing, tone, and formatting patterns.
   - Prefer the target's own terminology over generic corporate wording.

4. Pressure-test the claim set.
   - Remove or soften details that public sources contradict or fail to support.
   - If a claim is only partially supported, convert it into a code-review, update, FAQ, or working session rather than a finalized policy change.
   - Avoid over-specific operational details unless directly supported.

5. Select the persuasion principle.
   - Choose the strongest primary principle for the pretext:
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
   - Make sure the chosen principle fits both the public anchor and the requested action.

6. Fit the audience.
   - Rewrite the lure so it matches the recipient's function.
   - For IT or service desk audiences, emphasize tools, support readiness, rollout reviews, dry runs, or workflow alignment.
   - For business or HR audiences, emphasize benefits, policy clarifications, enrollment, or employee communications.

7. Explain the payload.
   - Give the meeting, file, or portal a plausible reason to exist.
   - If the call to action requires software, justify it with an external guest, production support, or compatibility need.

8. Produce at least two variants when helpful.
   - Offer different sender personas or tones.
   - Keep one conservative variant and one more tailored variant.

## Output

Return:

1. A short research summary with the strongest anchor facts.
2. The recommended sender department or persona.
3. The primary persuasion principle.
4. A polished subject line.
5. A polished email draft.
6. A short list of claims to avoid.

## Quality Rules

- Prefer exact dates over relative timing.
- Prefer official sources for names and phrasing.
- Keep the email concise and operational.
- Make the persuasion principle clear but not cartoonish.
- Do not introduce benefits, reimbursement types, or policy changes that public sources do not support.
- If the request names a specific department, verify whether that department plausibly owns the message.

## Useful Patterns

- `year-one review`
- `town hall`
- `dry run`
- `FAQ refresh`
- `support readiness`
- `rollout follow-up`

## Example Triggers

- `Draft a phishing pretext for a help desk employee based on a new RTO policy.`
- `Refine this town hall invitation so it sounds like the target company.`
- `Research the exact department name that would send a workplace tools update.`
