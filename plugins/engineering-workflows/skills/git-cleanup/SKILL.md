---
name: git-cleanup
description: Repository hygiene — prune merged/stale branches, detect orphans, repo health checks. Use when cleaning up branches, checking repo health, or scanning projects.
icon: ./assets/icon.png
---

# Git Repository Cleanup

Repository hygiene: prune branches, detect stale work, and check repo health.

Parse the user's input to determine the action:
- `$git-cleanup` or `$git-cleanup branches` — find and prune merged/stale branches
- `$git-cleanup stale [days]` — branches with no commits in N days (default 30)
- `$git-cleanup health` — large files, dangling refs, worktrees, repo size
- `$git-cleanup all` — scan all git repos under ~/Projects/

## Prerequisites

1. Verify we're in a git repository (`git rev-parse --is-inside-work-tree`) — except for `all` action which scans directories
2. If not in a git repo (and not using `all`), tell the user and stop

## Protected Branches

The following branches are NEVER suggested for deletion: `main`, `master`, `develop`

## Action: branches (default)

1. Fetch latest remote state: `git fetch --prune`
2. Identify the default branch (`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null` or fall back to `main`/`master`)
3. Find merged branches:
   - `git branch --merged <default>` — local branches already merged into default
   - Exclude protected branches and current branch
4. Find branches with deleted remotes:
   - `git branch -vv` — look for `[origin/...: gone]` entries
5. Present findings as a **dry-run preview**:
   - List branches that can be safely deleted (merged)
   - List branches whose remote is gone
   - Show last commit date and message for each
6. Ask the user which branches to delete (or "all listed")
7. On confirmation, delete with `git branch -d <branch>` (safe delete)
8. If a branch fails `-d` (unmerged), warn the user and offer `-D` with explicit explanation that commits may be lost — only proceed with user confirmation

## Action: stale [days]

1. Default to 30 days if no argument provided
2. For each local branch (excluding protected branches):
   - Get last commit date: `git log -1 --format='%ci' <branch>`
   - Calculate age in days
3. List branches older than the threshold, sorted by age (oldest first)
4. Show for each: branch name, last commit date, last commit message, age in days
5. Present as dry-run preview — ask before deleting
6. On confirmation, use `git branch -d` first; offer `-D` only with warning if unmerged

## Action: health

Run a comprehensive repository health check:

1. **Repository size**:
   - `.git` directory size: `du -sh .git`
   - Working tree size: `du -sh . --exclude=.git` (or equivalent)
   - Object count: `git count-objects -vH`

2. **Large files** (top 10 by size in history):
   - `git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | awk '/^blob/ {print $3, $4}' | sort -rn | head -10`
   - Flag files over 10MB

3. **Dangling objects**:
   - `git fsck --no-reflogs 2>&1` — look for dangling commits, blobs, trees
   - Report count and suggest `git gc` if significant

4. **Worktrees**:
   - `git worktree list` — show active worktrees

5. **Remote status**:
   - `git remote -v` — list remotes
   - Check if local is ahead/behind remote

6. **Stale tracking branches**:
   - `git remote prune origin --dry-run` — branches that would be pruned

7. Present findings with recommendations
8. If cleanup is recommended (gc, prune), show the commands but **always ask before running them**

## Action: all

1. Find all git repositories under `~/Projects/`:
   - `find ~/Projects -maxdepth 3 -name .git -type d`
2. For each repository found:
   a. Show repo name and path
   b. Run the **branches** check (merged + gone remotes)
   c. Show summary: N merged branches, M gone-remote branches
3. **Per-repo confirmation** — ask before deleting branches in each repo
4. Show overall summary at the end

## Safety Rules

1. **Never delete without confirmation** — always preview first
2. **Never delete protected branches** (main, master, develop)
3. **Never `git push origin --delete` on protected branches**
4. **Never run `git gc` without asking**
5. **Always preview first** — every action starts as a dry run
6. **Per-repo confirmation for `all`** — don't batch-delete across repos
7. Use `git branch -d` (safe delete) first; only offer `-D` with explicit warning
