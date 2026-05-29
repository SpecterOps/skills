---
name: readme-generation
description: Generate a professional README.md for a project. Works on local codebases and remote GitHub repos. Use when a project needs a README, when an existing README is outdated, or when documenting someone else's tool.
metadata:
  author: "GhostWorks"
---

# README Generator

Analyze a codebase and produce a complete, professional README.md.

Parse the user's input to determine:
- **Target**: a local path, a remote GitHub repo (e.g., `fortra/impacket`), or current directory (default)
- **Style**: `security-tool`, `library`, `cli`, `webapp`, `minimal`, or auto-detect (default)
- **Update mode**: if the user says "update" or the project already has a README, preserve custom sections

Common patterns:
- `$readme-generation` → generate for current directory, auto-detect style
- `$readme-generation ~/projects/mytool` → generate for local path
- `$readme-generation fortra/impacket` → clone and generate for remote repo
- `$readme-generation --style security-tool` → force a specific style
- `$readme-generation --update` → update existing README, keeping custom sections

## Steps

### 1. Acquire the codebase

- If a remote repo is given: `gh repo clone owner/repo /tmp/readme-target` and work from there
- If a local path is given: use that directory
- Otherwise: use current working directory

### 2. Deep scan the project

Read and analyze these files (skip any that don't exist):

**Project metadata:**
- `pyproject.toml`, `setup.py`, `setup.cfg` — Python project info, dependencies, entry points
- `Cargo.toml` — Rust project info
- `go.mod` — Go module info
- `package.json` — Node.js project info
- `Makefile`, `Justfile` — Build commands
- `Dockerfile`, `docker-compose.yml` — Container setup
- `.github/workflows/` — CI/CD configuration

**Source code (sample, don't read everything):**
- Entry points: `main.py`, `cli.py`, `main.go`, `main.rs`, `src/main.*`, `cmd/`
- Top-level source files for imports and structure
- CLI argument definitions (argparse, typer, cobra, clap)
- Config file examples

**Existing docs:**
- Current `README.md` (if updating)
- `CONTRIBUTING.md`, `CHANGELOG.md`, `LICENSE`
- `docs/` directory contents

**Git context:**
- `git log --oneline -30` — recent activity and feature descriptions
- `git tag --sort=-v:refname | head -5` — version history
- `git remote -v` — origin URL

### 3. Determine project type and style

Auto-detect from user input or infer:

| Signal | Type |
|---|---|
| nmap/scanning/enum imports, --target flags | `security-tool` |
| Library with no CLI, published to PyPI/crates | `library` |
| CLI with subcommands, --help output | `cli` |
| Web framework (Flask, FastAPI, Express, Next.js) | `webapp` |
| Few files, single purpose | `minimal` |

### 4. Generate README using the appropriate template

#### Security Tool Template
```markdown
# [Name]

[One-line description of what it does and why you'd use it]

## Features

- [Key capability 1]
- [Key capability 2]
- [Key capability 3]

## Installation

[Package manager install or build from source — include both if applicable]

## Quick Start

```bash
[Single command showing the most common usage]
```

## Usage

```
[Full --help output or manual command reference]
```

### Examples

```bash
# [Description of scenario 1]
[command]

# [Description of scenario 2]
[command]

# [Description of scenario 3]
[command]
```

## Output Formats

[If the tool supports multiple output formats, show examples of each]

## Requirements

- [Runtime dependencies]
- [System requirements]
- [Required access/permissions]

## Building from Source

```bash
[Build steps]
```

## License

[License type and link]
```

#### Library Template
```markdown
# [Name]

[One-line description]

## Installation

```bash
[pip install / cargo add / go get command]
```

## Quick Start

```python  (or appropriate language)
[Minimal working example — 5-10 lines]
```

## API Reference

### [Module/Class Name]

#### `function_name(params) -> return_type`

[Description and example]

## Configuration

[Config options if applicable]

## Contributing

[How to contribute, run tests, submit PRs]

## License

[License]
```

#### CLI Template
```markdown
# [Name]

[One-line description]

## Installation

```bash
[Install command]
```

## Usage

```
[Command syntax overview]
```

### Commands

#### `command-name`

[Description, flags, example]

## Configuration

[Config file location and format if applicable]

## Examples

[2-3 real-world usage scenarios]

## License

[License]
```

#### Webapp Template
```markdown
# [Name]

[One-line description]

## Tech Stack

- [Frontend framework]
- [Backend framework]
- [Database]
- [Deployment]

## Getting Started

### Prerequisites

[Required software and versions]

### Setup

```bash
[Clone, install deps, configure, run — step by step]
```

### Environment Variables

| Variable | Description | Default |
|---|---|---|
| `VAR_NAME` | What it does | `default` |

## Development

```bash
[Dev server, test, lint commands]
```

## Deployment

[How to deploy]

## License

[License]
```

#### Minimal Template
```markdown
# [Name]

[One-line description]

## Usage

```bash
[Primary usage command]
```

## Install

```bash
[Install steps]
```

## License

[License]
```

### 5. Writing guidelines

- **First line matters most** — the description after `# Name` should explain what the tool does AND why someone would use it, in one sentence
- **Show, don't tell** — real command examples over descriptions of what's possible
- **Copy-pasteable** — every code block should work if pasted into a terminal
- **No filler** — skip badges, excessive formatting, or sections with no content
- **Accurate dependencies** — only list what's actually required, pulled from the project files
- **Version-aware** — if the project has tags, reference the latest version in install commands

### 6. Update mode

When updating an existing README (user said "update" or `--update`):

1. Read the existing README fully
2. Identify **custom sections** — any section not in the standard template (acknowledgments, special notes, contributor lists, etc.)
3. Regenerate the standard sections with current project data
4. **Preserve custom sections in their original position** — do not delete or rewrite them
5. If a standard section has user-added content beyond what the template provides (e.g., extra examples), keep the user additions and only update the generated parts
6. Show a diff summary of what changed before writing

### 7. Output

- Write the README to the project directory
- If working on a remote repo in `/tmp/`, also copy the output to the current directory as `README-[project-name].md`
- Report the file path and a brief summary of what was generated
