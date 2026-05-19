---
name: electron-candidate-discovery
description: Find practical Electron apps that are likely patchable with the same Electron-plus-Squirrel method. Use when building an actionable shortlist of candidate apps rather than a broad inventory.
---

# Electron Candidate Discovery

Use this skill to identify practical Electron app candidates for the same patching and delivery method.

## Goal
Return a ranked shortlist of realistic candidates, not a broad catalog.

## For Each Candidate Include
- app name
- why it is practical
- packaging shape
- installer/update mechanism
- whether it appears Squirrel-like or similarly patchable
- likely main-process entrypoint location
- obvious blockers or drawbacks

## Selection Bias
Prioritize apps that are:
- clearly Electron-based
- locally patchable without bespoke tooling
- packaged in a way that exposes entrypoints or repackable resources
- delivered through Squirrel or a closely similar updater/install chain
- realistic for user delivery and repeated rebuild workflows

## Output
Return a ranked shortlist with concise, actionable reasoning for each entry.
