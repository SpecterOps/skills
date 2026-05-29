---
name: course-wiki-stage3-qa
description: "Run stage 3 of the course wiki workflow: browser QA, template-shell comparison, targeted rendering-only polish, and post-fix validation for a migrated course wiki. Use when stage 1 or stage 2 has been deployed or previewed and the next task is to verify the course against the wiki-course-atd-instructor presentation benchmark, preserve original course content, apply bounded polish fixes, and summarize residual risks."
metadata:
  author: "GhostWorks"
---

# Course Wiki Stage 3 QA

This skill is the current stage-3 entrypoint. It performs the QA pass, compares the course to the template shell, applies targeted rendering-only polish, and reruns validation. It does not own an endless fix/deploy/retest loop, and it must preserve the original course's content and structure.

Load these references as needed:
- [references/stage3-qa-checklist.md](references/stage3-qa-checklist.md) for the stage-3 checklist and findings format.
- [references/stage3-atrto-reference.md](references/stage3-atrto-reference.md) for the proven ATRTO stage-3 run and acceptable template-shell differences.

## Inputs To Confirm From The Environment

- QA mode: `local`, `deployed`, or `both`.
- Local preview URL if local QA is requested.
- Deployed preview URL if deployed QA is requested.
- The stage that was just completed: `stage1` or `stage2`.
- Target course repo path so routes can be derived from the content tree.

## Workflow

## 1. Pick The Correct QA Target

- Use local preview for fast iteration before push.
- Use deployed preview to confirm build-pipeline behavior, LFS assets, and public rendering.
- Use both when the user wants confidence before and after push.

## 2. Run The Representative Browser Sweep

Check:
- homepage
- top navigation
- sidebar rendering on representative pages
- one PDF embed/download page
- one image-heavy page
- one representative lab page
- one representative lab-solution page
- one representative resource page
- one page with expand/callout UI in dark mode
- one representative page with long sample-output code blocks

For stage 1, focus on shell correctness.
For stage 2, focus on migrated content correctness.

## 3. Run The Full Route Sweep

- Derive every expected content route from the course `content/` tree.
- Confirm for each route:
  - successful page load
  - title
  - primary `h1`
- Treat full route coverage as required, not optional.

## 4. Run The Build-Output Sanity Sweep

After any polish pass, inspect generated output for migration-specific rendering failures that browser spot checks may miss.

Required checks:
- grep built HTML/XML for leaked Hextra UI markup such as:
  - `hextra-code-copy-btn`
  - `hextra-copy-icon`
  - `Copy code` appearing inside article content
- check for obvious route-case mismatches in migrated internal links
- check for reader-facing bare URLs left in prose where descriptive links would be clearer
- confirm no known missing-asset references remain unresolved unless explicitly accepted as residual risk

If leaked Hextra markup appears in content, treat it as a rendering defect, not a cosmetic issue.

## 5. Compare To The Template Correctly

- Compare shell and presentation behavior against the `wiki-course-atd-instructor` shell or a current course derived from it:
  - homepage structure and spacing feel
  - labs landing behavior
  - resources landing behavior
  - slides page pattern
  - one comparable shared resource page such as Guacamole
- Use the template shell as a presentation benchmark, not as a mandate to flatten original course content.
- Preserve richer or denser course-specific material when it is rendering correctly.

## 6. Apply Targeted Rendering-Only Polish

- Fix only rendering and presentation issues such as:
  - malformed callout formatting
  - spacing artifacts
  - markdown normalization issues
  - broken asset references
  - malformed links
  - dark-mode contrast problems in custom notice/expand blocks
  - missing docs sidebar behavior on migrated lab and lab-solution sections
  - broken code/output rendering caused by ambiguous fences or placeholder syntax
- Do not rewrite or remove instructional content just to increase template parity.

Preferred fixes:
- use local layout overrides or section cascade for docs/sidebar behavior
- use custom CSS for dark-mode readability
- normalize ambiguous code fences to explicit `text` fences
- replace HTML-like placeholder tokens in sample output with bracketed placeholders when needed to preserve rendering

## 7. Rerun Validation

- Rerun the local build after polish changes.
- Rerun browser checks on affected pages.
- Rerun the build-output sanity sweep.
- Confirm that targeted fixes did not introduce regressions.

## 8. Report Findings

Group findings by:
- navigation
- broken assets
- PDF rendering
- layout or spacing mismatches
- content placement issues
- dark-mode issues
- code-block rendering issues
- deployed-preview authentication or asset-loading issues

Also report:
- acceptable intentional differences from the template shell
- full route sweep summary
- post-fix validation status
- residual risks or untested areas

## 9. Current Boundary

- This skill performs one bounded polish pass.
- It does not perform unlimited deploy/retest loops.
- Use the final findings to decide whether another explicit stage-3 run is needed.

## Reference

- Use [references/stage3-qa-checklist.md](references/stage3-qa-checklist.md) as the standard QA checklist.
- Use [references/stage3-atrto-reference.md](references/stage3-atrto-reference.md) as the canonical example of the current stage-3 workflow.
