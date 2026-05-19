# ATRTO Stage 1 Reference

## Purpose

Use this reference when bootstrapping another course from the shared `wiki-course-atd-instructor` scaffold. It records the exact stage-1 shape that was proven on ATRTO and the baseline checks that the orchestrator sub-agent should run.

## Source And Target

- Source scaffold repo: `/path/to/templates/wiki-course-atd-instructor`
- Target repo: `/path/to/output/wiki-course-atrto`
- Target branch used for preview deploy: `mnickerson-updates`

## Files Changed In The Proven ATRTO Stage 1

- `hugo.yaml`
- `README.md`
- `amplify.yml`
- `buildspec.yml`
- `content/_index.md`
- `content/labs/_index.md`
- `content/resources/_index.md`
- `content/slides/_index.md`
- `content/images/atrto.jpg`
- `content/images/specter_light.png`
- `content/images/specter_dark.png`

## Stage-1 Decisions

- Copy the template scaffold excluding `.git` and `content/`.
- Add Git LFS support to both `amplify.yml` and `buildspec.yml` during stage 1 so later LFS-backed assets render without pipeline surprises.
- Keep the template top navigation model: `Labs`, `Resources`, `Slides`.
- Create only the minimal deployable shell. Do not import old course material.

## Build Pipeline Baseline

- Add `GIT_LFS_VERSION` to both build configs.
- Install `git-lfs` from the official GitHub release tarball in user space.
- Verify `git lfs version`.
- Run `git lfs install --local`.
- Run `git lfs pull` before `hugo --gc --minify`.

## Deployment And Browser Verification

- Preview URL used for ATRTO: `https://pr-1.d3i8gdc0r1f7xa.amplifyapp.com/`
- Browser verification completed with Playwright MCP.
- The generalized skill suite should support local preview checks first, then deployed preview checks when available.

Minimum checks performed:
- homepage loads
- page title matches the course
- `/labs/` loads
- `/resources/` loads
- `/slides/` loads

## Playwright Note

If Playwright MCP is configured but fails to launch because Chrome/Chromium is missing, install the browser expected by the MCP config and retry the preview checks.
