---
name: git-preflight
description: Pre-commit and pre-edit git checklist — staged diff code-review, macOS case renames, remote branch sync verification. Run before committing or starting work on a feature branch.
icon: ./assets/icon.png
---

# Git Preflight Checklist

Run before committing (`commit`) or before editing a feature branch (`branch`). Default (`all`) runs both.

## `branch` — Before Editing a Feature Branch

Verify the local branch is in sync with remote before making any changes:

```bash
git fetch origin
git log --oneline HEAD..origin/$(git branch --show-current)
```

If output is non-empty, the remote is ahead — pull before editing:

```bash
git pull --ff-only
```

If the branch has diverged, report to user and stop. Do not start editing on a stale branch.

## `commit` — Before Committing

### 1. Review staged diff

```bash
git diff --staged
```

Check for:
- **Unintended lines** — edits from before the current session that got staged with `git add`
- **Debug output** — leftover print/log statements
- **Secrets** — any tokens, passwords, or API keys accidentally staged

If unintended changes are staged, unstage the file and re-add only the intended hunks:
```bash
git restore --staged <file>
git add -p <file>
```

### 2. Check for case-rename traps (macOS)

If any staged files look like case-only renames (e.g., `foo.md` → `FOO.md`), verify git actually tracked it:

```bash
git status
```

On macOS (case-insensitive FS), `git mv foo.md FOO.md` is a no-op. The correct approach:
```bash
git mv foo.md tmp.md && git mv tmp.md FOO.md
```

### 3. Verify branch

```bash
git branch --show-current
```

Confirm you're on the intended feature branch, not `main` or `master`. If on main/master, create a feature branch before committing unless this is intentional.

## Output

Report pass/fail for each check:

```
Git Preflight — commit
✓ Staged diff reviewed — N files, no unintended changes
✓ No case-rename issues detected
✓ On branch feat/my-feature (not main)
Ready to commit.
```

Or with issues:

```
Git Preflight — commit
✗ Staged diff contains lines from before current session in src/main.py
  → Run: git restore --staged src/main.py && git add -p src/main.py
✓ No case-rename issues detected
✓ On branch feat/my-feature
Fix staged diff before committing.
```
