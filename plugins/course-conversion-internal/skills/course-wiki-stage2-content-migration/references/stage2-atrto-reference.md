# ATRTO Stage 2 Reference

## Purpose

Use this reference when migrating old participant content into a new Hextra wiki after the stage-1 shell already exists.

## Proven ATRTO Decisions

- Keep `wiki-course-atd-instructor` as the canonical scaffold and presentation baseline.
- Preserve course content text exactly.
- Keep top nav to `Labs`, `Resources`, and `Slides`.
- Fold non-lab reference material into `Resources`.
- Use Hextra cards for landing-page navigation and end-of-page link collections where useful.
- Reshape the homepage to follow the template pattern instead of carrying forward the full legacy landing page.
- Move operational/logistics-heavy content into `Resources/Course Information` when needed.

## Rendering Conversions Used

- legacy notices to Hextra callouts
- attachments to explicit file links/cards
- embedded PDFs to the template-compatible `pdf` shortcode
- old section landing behavior to explicit link or card-based navigation

## LFS Lesson

- Hydrate the old course repo with `git lfs pull` before copying content or assets.
- Build-pipeline LFS support is necessary but not always sufficient.
- Stage 1 should make the new repo build pipeline LFS-ready, but stage 2 still owns source-repo hydration.
- If the legacy source still contains pointer payloads, do not begin the copy yet.
- If PDFs or images still fail after deploy, check for unresolved pointer payloads under `content`.
- Recover real files from the hydrated legacy course when needed.

## Representative QA Targets

- homepage
- slides page
- BloodHound cheatsheet PDF page
- Guacamole resource page
- day 1 lab access page
- day 1 redirector setup page
