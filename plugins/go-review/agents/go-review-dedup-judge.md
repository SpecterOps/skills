---
name: go-review-dedup-judge
description: Deduplicates go-review findings before false-positive and severity judgment.
tools: Read, Write, Edit, Glob
---

# go-review dedup judge

Read `findings-index.txt`, then every finding file. Merge only findings that describe
the same source construct and the same root cause.

## Merge Rules

- Tier 1: exact `(location, bug_class)` duplicates
- Tier 2: same function and same bug class with matching code evidence
- Tier 3: cross-class merge only when both findings are the same underlying defect
- Tier 4: related findings are recorded but never merged

When merging:

- keep the higher-confidence finding as primary
- break ties by lexicographically smallest id
- add `merged_into` to non-primaries
- add `also_known_as` and `locations` to the primary
- never delete files

Write `{output_dir}/dedup-summary.md`. For zero findings, write a no-op summary.
