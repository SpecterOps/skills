---
name: source-research
description: Fast topic research with source discovery, source quality evaluation, and concise synthesis. Use when looking up recent information, comparing sources, or producing a quick/detailed summary with citations.
icon: ./assets/icon.png
---

# Research

Perform focused research on a user-provided topic and return source-backed findings.

## Input Parsing

Interpret input as: `TOPIC [MODE]`

Rules:
1. Treat all input as topic except the last token when it matches a mode.
2. Supported modes: `quick`, `deep`, `sources`.
3. Default to `quick` when no mode is provided.

Examples:
- `$source-research DLL sideloading detection`
- `$source-research C2 frameworks 2026 deep`
- `$source-research ADCS ESC1 sources`

## Modes

### quick (default)

Use for rapid, high-signal answers.

1. Run 2-3 targeted web searches from different angles.
2. Open top results and extract concrete facts.
3. Evaluate source quality (recency, authority, relevance).
4. Return concise synthesis with citations.

### deep

Use for broader investigation and tradeoff analysis.

1. Run 5+ searches covering multiple angles.
2. Read the most relevant sources in detail.
3. Synthesize agreements, disagreements, and gaps.
4. Return comprehensive findings with citations.

### sources

Use for bibliography-first output without synthesis.

1. Run 3-4 targeted searches.
2. Rank and annotate the strongest sources.
3. Return a numbered source list with short notes.

## Output Templates

### quick/deep

```markdown
## TL;DR
2-3 sentence summary.

## Key Findings
- Finding 1
- Finding 2
- Finding 3

## Sources
1. [Title](url) ? one-line annotation
2. [Title](url) ? one-line annotation

## Gaps
- What remains uncertain or under-sourced.
```

### sources

```markdown
## Sources: <topic>

1. [Title](url) ? annotation (recency, authority, value)
2. [Title](url) ? annotation

**Best starting point:** Source N ? reason
**Most authoritative:** Source N ? reason
```

## Quality Rules

- Always include URLs for claims.
- Prefer primary and recent sources.
- For security topics, prioritize vendor advisories, MITRE ATT&CK, and CVE/NVD records.
- Explicitly state uncertainty rather than padding with weak sources.
- Offer to export findings to a file when helpful.
- Make sure to explain how the findings can be used in an offensive capability
