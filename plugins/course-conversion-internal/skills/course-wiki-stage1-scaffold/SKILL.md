---
name: course-wiki-stage1-scaffold
description: "Bootstrap a new course wiki from the wiki-course-atd-instructor scaffold and stop after the first deployable shell is validated. Use when Codex or the course-wiki-migration orchestrator needs to copy the shared instructor template without legacy content, set course identity values, create the minimal homepage labs resources and slides shell, prepare the first deploy, or confirm the shell in local or deployed browser checks before any legacy content import begins."
---

# Course Wiki Stage1 Scaffold

Create the initial Hextra course shell from the `wiki-course-atd-instructor` scaffold. This skill is intended to be callable by the migration orchestrator sub-agent, but it can also be used directly. Stop after the scaffold is browser-validated. Do not import or convert legacy course material with this skill.

Load [references/stage1-atrto-reference.md](references/stage1-atrto-reference.md) when you need the proven ATRTO example, the exact validation checklist, or a reminder of the files that were touched.

## Inputs To Confirm From The Environment

- Source template scaffold repo path.
- Target course repo path.
- Course title and course acronym/image asset to use on the landing page.
- Current git state of the target repo.
- Whether the target repo already exists and has a remote/branch workflow.
- Requested QA mode: `local`, `deployed`, or `both`.

Default assumptions:
- Copy template scaffold contents but exclude `.git` and `content/`.
- Keep template build pipeline files, but make sure both `amplify.yml` and `buildspec.yml` support Git LFS asset pulls during stage 1 when those files are present.
- Keep the template top nav model: `Labs`, `Resources`, `Slides`.
- Create a minimal shell only. Do not pull in old course material yet.

## Workflow

## 1. Ground In The Target Repo

- Inspect the target repo before editing anything.
- Confirm whether it is empty, already initialized as git, or already contains scaffold files.
- Confirm the source scaffold repo structure and identify the minimal assets needed for the course shell.
- Never copy the source repo’s `.git` directory.

## 2. Copy The Stage-1 Scaffold

- Copy the template scaffold into the target repo excluding `content/` and `.git`.
- Preserve top-level build and theme files from the template:
  - `hugo.yaml`
  - `amplify.yml`
  - `buildspec.yml`
  - Go module files
  - shared layouts/partials
- Treat Git LFS support as part of the scaffold, not a later-stage fix:
  - add a `GIT_LFS_VERSION` variable
  - install `git-lfs` in user space during the build
  - verify `git lfs version`
  - run `git lfs install --local`
  - run `git lfs pull`
- If the target repo is not empty, read it carefully and work with existing files instead of blindly overwriting user changes.

## 3. Set Course Identity

- Update the course title and description in the target repo config.
- Update the repo README title if the template placeholder repo name is still present.
- Ensure the build pipeline can fetch LFS-backed PDFs and images before Hugo runs.
- Treat the stage-1 shell as template-styled: same overall navigation and page structure, course-specific identity only.

## 4. Hugo Compatibility Preflight

- Do not assume the system `hugo` on PATH is new enough for Hextra.
- Check the active Hugo version against the theme requirement before local QA.
- Prefer this order when selecting a Hugo binary for local validation:
  - `HUGO_BIN` if explicitly provided
  - `/tmp/course-tools/hugo/hugo` if present
  - `hugo` on PATH
- If the PATH version is too old but a newer local binary exists, use the newer local binary for build and preview.
- If no compatible binary exists, stop and report the minimum required version instead of claiming local QA passed.

## 5. Create The Minimal Content Shell

- Create `content/` with only the files needed for a first deployable shell:
  - homepage
  - `labs/_index.md`
  - `resources/_index.md`
  - `slides/_index.md`
- Copy only the image assets required for the initial landing page and navbar logo.
- Keep the homepage short and stage-appropriate:
  - course title
  - landing image
  - cards for `Labs`, `Resources`, and `Slides`
  - a callout or note that the shell is ready for content migration
- Do not add legacy course material during this stage.

## 6. Prepare And Verify The First Deploy

- Check git status after the scaffold changes.
- Commit only when the repo state is clean and the user expects a commit in this stage.
- Respect the repo’s existing branch workflow.
- For `local` QA, start a local Hugo preview and verify the shell in browser with Playwright MCP.
- For `deployed` QA, verify the deployed preview URL in browser with Playwright MCP.
- For `both`, run the local checks first and the deployed checks second.

Minimum browser verification:
- Homepage loads.
- Page title is course-correct.
- `Labs`, `Resources`, and `Slides` all load.
- Navigation/search shell renders.

Minimum build-pipeline verification:
- `amplify.yml` contains the Git LFS install and pull steps.
- `buildspec.yml` contains the same Git LFS install and pull steps.
- Stage-1 output is ready to handle later course assets that may be stored as Git LFS objects.

If Playwright MCP fails because its configured browser is missing, install the required browser runtime first, then retry.

## 7. Stop Condition

Stop when all of the following are true:
- The target repo contains the template-derived scaffold.
- The course identity is updated.
- The minimal shell content exists.
- The requested local and/or deployed checks are complete.

At that point, hand off to stage 2. Do not start importing or converting legacy content from this skill.

## Reference

- Use [references/stage1-atrto-reference.md](references/stage1-atrto-reference.md) as the canonical example of a completed stage-1 migration.
