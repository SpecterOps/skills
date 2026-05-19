---
name: course-wiki-stage2-content-migration
description: Import legacy course content into the new Hextra wiki while preserving course text exactly and changing only rendering, structure, metadata, assets, and compatibility syntax. Use when stage 1 is complete and the next task is to copy participant content, align it to the shared wiki-course-atd-instructor pattern, resolve LFS-backed assets, and prepare the migrated course for local or deployed browser QA.
---

# Course Wiki Stage 2 Content Migration

Run this skill after the stage-1 scaffold exists. This skill handles the content-aware migration work for a course wiki. It preserves course content and changes only the way that content is rendered and organized in the new wiki.

Load [references/stage2-atrto-reference.md](references/stage2-atrto-reference.md) when you need the proven ATRTO decisions and QA targets.

## Inputs To Confirm From The Environment

- Legacy participant content path.
- Legacy course repo path if Git LFS hydration is needed before copy.
- Target course repo path.
- Current template scaffold state in the target repo.
- Requested QA mode: `local`, `deployed`, or `both`.
- Preview URL if deployed QA is requested.

Default assumptions:
- `wiki-course-atd-instructor` is the canonical scaffold shape for new instructor course wikis.
- Course content wording must not change.
- `Labs`, `Resources`, and `Slides` remain the top nav model.
- Heavy logistics content may move into `Resources/Course Information` if that matches the template homepage pattern.

## Workflow

## 1. Import Legacy Content

- Hydrate the legacy source repo before copying content when it uses Git LFS. The stage-2 workflow should do this itself:
  - run `git lfs install`
  - run `git lfs pull`
- If `git-lfs` is unavailable, stop and report that clearly before import.
- Check the legacy source for unresolved LFS pointer payloads before import.
- If the legacy source still contains pointer payloads under `content`, stop and recover the real files before continuing.
- Copy the legacy participant content into the target repo.
- Preserve instructional prose, commands, examples, and exercise text exactly.
- Do not bring over legacy theme infrastructure that is not actual course content.
- During migration, convert reader-facing bare prose URLs into descriptive Markdown links when that improves readability, but keep literal service endpoints raw when learners may need to copy them exactly.

## 2. Convert Rendering Only

- Normalize front matter for Hugo + Hextra.
- Remove learn-theme-only metadata.
- Convert rendering constructs:
  - `notice` to Hextra-compatible callout or a local shortcode shim
  - `children` to explicit cards or link lists
  - `attachments` to explicit file links or cards
  - `embed-pdf` to the template-compatible `pdf` shortcode when available
- Use card-based landing pages where that improves navigation without changing content.

## 3. Add Compatibility Layers Early

- Expect legacy content to rely on shortcode names or markdown behavior that Hextra does not handle cleanly.
- Add local compatibility shims when needed instead of rewriting instructional prose:
  - `layouts/shortcodes/expand.html`
  - `layouts/shortcodes/notice.html`
  - `layouts/shortcodes/video.html`
- If migrated labs or lab solutions lose the docs sidebar, add a docs-style layout override or section-level cascade so those sections render with the same sidebar behavior as the template shell.
- If dark mode makes custom callouts or expand blocks unreadable, add explicit dark-theme styles in the local custom head partial instead of changing content.

## 4. Normalize Markdown That Breaks Hextra

- Treat long sample-output blocks as a migration risk area.
- Prefer explicit language tags for unlabeled fences:
  - convert bare triple-backtick output blocks to `text` fences
  - keep code-language fences such as `bash`, `powershell`, `json`, `html`, and `csharp` when they are already known
- Do not leave literal angle-bracket placeholders inside fenced output if they can be interpreted as HTML and break rendering.
  - replace placeholder forms such as `<TGT>`, `<CLASS NAME>`, `<SNIP>`, `<BASE64_PFX>`, `<ToolName>`, and similar migration placeholders with bracketed forms such as `[TGT]`, `[CLASS NAME]`, `[SNIP]`, and `[BASE64_PFX]`
  - apply the same rule to long sample outputs and command examples when those placeholders are only stand-ins, not real HTML
- Preserve meaning exactly while normalizing syntax.

## 5. Align To The Template Pattern

- Keep the homepage light and template-shaped.
- Keep `Labs`, `Resources`, and `Slides` as the main destinations.
- Fold reference-style legacy content into `Resources` when that matches the proven pattern.
- If the legacy homepage contains logistics-heavy content, move it into a `Course Information` resource page and link it from the homepage.
- Fix obvious route-shape mismatches such as case-only link issues during migration rather than leaving them for QA.

## 6. Asset And Build Validation

- Treat legacy-source hydration as a stage-2 prerequisite, not a stage-1 task.
- Check for unresolved Git LFS pointers before browser QA.
- Check both:
  - unresolved pointers remaining in the legacy source before copy
  - unresolved pointers remaining in the target repo after copy
- Confirm images, PDFs, and linked files exist where the migrated pages expect them.
- Run a local Hugo build before push.
- If Hextra search requires remote assets that break offline local QA, either disable the search UI locally or switch to an offline-safe configuration and record the decision.
- When a deployed preview sits behind preview authentication, check the target course README or migration notes for credentials before treating the deploy as blocked.

## 7. Browser Verification Targets

- Homepage
- Slides page
- At least one PDF embed/download page
- At least one image-heavy lab page
- At least one resource page
- Any page that was restructured during migration
- At least one lab page and one lab-solution page to confirm sidebar behavior
- At least one page with expand/callout blocks in dark mode

## 8. Stop Condition

Stop when:
- the migrated content is in place
- rendering has been converted for Hextra
- the local build passes
- requested QA has been completed
- the repo is ready for commit/push or already pushed by the orchestrator

## Reference

- Use [references/stage2-atrto-reference.md](references/stage2-atrto-reference.md) as the canonical stage-2 example.
