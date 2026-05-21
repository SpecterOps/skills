---
name: timeline-workflow
description: Orchestrate the full Pentest Timeline workflow (parsers + consolidator) for reporting delivery.
icon: ./assets/icon.png
---

# Timeline Workflow

Use when the task is to generate or update an engagement timeline for reporting.

## Behavior
1. Run each parser skill (timeline-cobaltstrike, timeline-mythic, timeline-asciinema, timeline-markdown-notes, timeline-pdf-notes, timeline-ghostwriter) over their respective inputs.
2. Execute timeline-consolidator after parser outputs exist to merge, tag, and sort the entries.
3. Produce output/timeline.md and output/timeline.json, then feed the consolidated timeline into the report-writer agent for findings if requested.

## Input Requirements
- Populate the input/ directory with sections: c2logs/, terminallogs/, notes/, gw_oplog/, matching the skill-specific expectations.
- Provide MITRE tagging config or use defaults documented in references/timeline-config.yaml.

## Output
- Consolidated timeline files plus diagnostics described in timeline-consolidator.
- Optionally call report-writer to weave timelines into findings.

## Notes
- If some inputs are missing, run the available parsers and document gaps in timeline-gaps.txt.
- Provide logistic details (input structure, MITRE settings) in references/timeline-readme.md.
