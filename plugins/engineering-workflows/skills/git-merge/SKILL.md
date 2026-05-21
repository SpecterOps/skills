---
name: git-merge
description: Complex git operations — merge conflict resolution, cherry-picks, rebases. Use when merging branches, resolving conflicts, cherry-picking commits, or rebasing.
icon: ./assets/icon.png
---

# Git Merge & Conflict Resolution

Handle complex git operations: merges, cherry-picks, rebases, and conflict resolution.

Parse the user's input to determine the action:
- `$git-merge` or `$git-merge resolve` — detect and resolve current conflicts
- `$git-merge branch <name>` — merge a branch into current, handle conflicts
- `$git-merge cherry-pick <commit>...` — cherry-pick with conflict handling
- `$git-merge rebase <base>` — non-interactive rebase onto base
- `$git-merge abort` — abort in-progress merge/rebase/cherry-pick
- `$git-merge status` — show current merge/rebase/cherry-pick state

## Prerequisites

1. Verify we're in a git repository (`git rev-parse --is-inside-work-tree`)
2. If not in a git repo, tell the user and stop

## Action: status

1. Run `git status` to show branch and state
2. Check for in-progress operations:
   - `.git/MERGE_HEAD` → merge in progress
   - `.git/rebase-merge/` or `.git/rebase-apply/` → rebase in progress
   - `.git/CHERRY_PICK_HEAD` → cherry-pick in progress
3. If conflicts exist, list conflicted files with `git status --porcelain` (look for `UU`, `AA`, `DD`, `AU`, `UA`)
4. Report current branch, upstream tracking, and any in-progress operation

## Action: resolve (default)

1. Run `git status --porcelain` to find conflicted files (`UU`, `AA`, `DD`, `AU`, `UA` prefixes)
2. If no conflicts found, report clean state and stop
3. For each conflicted file:
   a. Read the file to find `<<<<<<<`, `=======`, `>>>>>>>` conflict markers
   b. Read surrounding context and related tests to understand intent of both sides
   c. If the resolution is clear (e.g., both sides made non-overlapping changes within the same hunk), resolve by editing the file — remove all conflict markers and produce the correct merged result
   d. If the resolution is ambiguous, show both sides to the user and ask which approach to take — **never silently pick a side**
   e. For binary file conflicts, ask the user to choose `--ours` or `--theirs`
   f. After resolving each file, run `git add <file>`
4. After all files are resolved:
   - If merge: `git commit` (use git's default merge message, do NOT use conventional commit style)
   - If rebase: `git rebase --continue`
   - If cherry-pick: `git cherry-pick --continue`

## Action: branch <name>

1. Verify the branch exists (`git rev-parse --verify <name>`)
2. Show what will be merged: `git log --oneline HEAD..<name>` (commits coming in)
3. Run `git merge <name>`
4. If merge succeeds cleanly, report success with merge commit
5. If merge has conflicts, follow the **resolve** workflow above
6. Use git's default merge commit message — do NOT override with conventional commit style

## Action: cherry-pick <commit>...

1. Validate each commit exists (`git rev-parse --verify <commit>`)
2. Show what will be cherry-picked: `git log --oneline -1 <commit>` for each
3. Run `git cherry-pick <commit>...`
4. If clean, report success
5. If conflicts, follow the **resolve** workflow above

## Action: rebase <base>

1. Identify current branch name
2. **Protected branch warning**: If current branch is `main`, `master`, or `develop`, warn the user that rebasing a protected branch is dangerous and ask for explicit confirmation before proceeding
3. Show what will be replayed: `git log --oneline <base>..HEAD`
4. Warn the user: after rebase, they'll need `git push --force-with-lease` to update the remote — **never force-push automatically**
5. Run `git rebase <base>` (non-interactive only — `git rebase -i` requires an interactive terminal)
6. If clean, report success
7. If conflicts, follow the **resolve** workflow for each step, using `git rebase --continue` after each resolution

## Action: abort

1. Detect what's in progress:
   - `.git/MERGE_HEAD` → `git merge --abort`
   - `.git/rebase-merge/` or `.git/rebase-apply/` → `git rebase --abort`
   - `.git/CHERRY_PICK_HEAD` → `git cherry-pick --abort`
2. If nothing is in progress, tell the user
3. Run the appropriate abort command
4. Show `git status` to confirm clean state

## Safety Rules

- **Never force-push** — warn the user they'll need `--force-with-lease` after rebase
- **Never use `git rebase -i`** — interactive mode requires a terminal that cannot be provided in this context
- **Ask on ambiguous conflicts** — never silently choose a side
- **Warn on protected branches** — `main`, `master`, `develop` get explicit warnings before rebase
- **Merge commits use git's default message** — only manual commits follow conventional commit style
- **Check for uncommitted changes** before starting operations — warn if working tree is dirty
