# Course Wiki Migration Orchestrator Workflow

## Purpose

This reference defines how the orchestrator sub-agent should sequence the course wiki migration stages and when it should load each stage skill.

## Stage Order

1. Stage 1 scaffold
2. Stage 2 content migration
3. Stage 3 QA and targeted polish

Do not skip backward across stages in a single run unless the user explicitly asks for a single-stage rerun.

## QA Modes

- `local`: run local Hugo preview and browser checks only
- `deployed`: run deployed preview checks only
- `both`: run local checks first, then deployed checks

## Stage 1 Handoff

Required outputs:
- template-derived scaffold in target repo
- course identity updated
- minimal shell content present
- LFS-ready `amplify.yml` and `buildspec.yml`
- local build and requested browser checks completed
- compatible Hugo binary choice documented if PATH `hugo` is too old

Optional outputs:
- auto-commit
- auto-push

## Stage 2 Handoff

Required outputs:
- legacy source repo hydrated by stage 2 if it uses Git LFS
- legacy participant content copied in
- rendering converted for Hextra
- content text preserved
- homepage aligned to the template pattern
- LFS pointers resolved or reported
- local build and requested browser checks completed
- markdown/code-fence normalization applied where needed to avoid Hextra rendering failures
- shortcode/layout compatibility added where needed for legacy `expand`, `notice`, `video`, sidebar layout, and dark-mode readability
- reader-facing prose URLs converted to descriptive links where appropriate

Optional outputs:
- auto-commit
- auto-push

## Stage 3 Outputs

- structured QA findings
- representative page checks
- full route sweep summary
- build-output sanity sweep summary
- deployed-auth handling summary when preview auth is enabled
- template-shell comparison summary
- polish fixes applied
- post-fix validation summary
- recommended next manual fix targets

## Sub-Agent Contract

- The orchestrator is intended to run inside a worker sub-agent.
- It may call stage skills and helper scripts.
- It should not claim that stage 3 performs unlimited fix loops or deploy cycles.
