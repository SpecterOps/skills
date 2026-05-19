---
name: sccmhunter-install-local
description: Clone SCCMHunter into operating-tools and install it in a local Python virtual environment using the repository's documented setup flow.
---

# SCCMHunter Local Install

Use this skill to install SCCMHunter in a local, repo-adjacent workspace without polluting the main project environment.

This skill follows the validated workflow:
- clone the SCCMHunter repo into `operating-tools/SCCMHunter`
- create/use `operating-tools/.venv`
- install from `requirements.txt`
- verify with `python3 sccmhunter.py -h`
- keep `operating-tools/` ignored in git

## Direct Triggers

Use this skill when the task mentions any of the following:
- install SCCMHunter
- clone SCCMHunter
- local SCCM tooling setup
- operating-tools environment
- repo-local SCCMHunter virtualenv

## Input Contract

Accept input as:
`BASE_DIR [MODE]`

Where:
- `BASE_DIR` defaults to current repo root
- `MODE` is `execute` (default) or `plan`

Examples:
- `$sccmhunter-install-local execute`
- `$sccmhunter-install-local /home/defaultuser/Working/codex-config execute`
- `$sccmhunter-install-local /path/to/repo plan`

## Preconditions

1. Confirm target directory is operator-controlled.
2. Confirm `git` and `python3` are available.
3. Confirm outbound access to GitHub is permitted in the environment.
4. Ensure `operating-tools/` is git-ignored before completion.

## Execution Workflow

1. Prepare destination paths:
- `<BASE_DIR>/operating-tools`
- `<BASE_DIR>/operating-tools/SCCMHunter`
- `<BASE_DIR>/operating-tools/.venv`

2. Clone SCCMHunter if missing:

```bash
mkdir -p <BASE_DIR>/operating-tools
cd <BASE_DIR>/operating-tools
git clone https://github.com/garrettfoster13/sccmhunter.git SCCMHunter
```

If already present, do not reclone; reuse the existing checkout.

3. Create/reuse virtualenv:

```bash
cd <BASE_DIR>/operating-tools
[ -d .venv ] || python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
```

4. Install tool dependencies using repo instructions:

```bash
./.venv/bin/pip install -r <BASE_DIR>/operating-tools/SCCMHunter/requirements.txt
```

5. Verify SCCMHunter runs:

```bash
cd <BASE_DIR>/operating-tools/SCCMHunter
<BASE_DIR>/operating-tools/.venv/bin/python3 sccmhunter.py -h
```

6. Ensure git exclusion exists in `<BASE_DIR>/.gitignore`:
- required entry: `operating-tools/`

## Output Requirements

For each run, include:
- `BASE_DIR` used
- whether clone was new or reused
- virtualenv path
- exact install command(s)
- verification output snippet from `sccmhunter.py -h`
- `.gitignore` status for `operating-tools/`
- UTC timestamp

## Troubleshooting

If install fails:
1. verify network reachability to `github.com` and Python package indexes
2. rerun pip install with verbose output:

```bash
./.venv/bin/pip install -v -r requirements.txt
```

3. confirm Python version compatibility and report exact exception text
