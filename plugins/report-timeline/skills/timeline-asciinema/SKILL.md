---
name: timeline-asciinema
description: Convert Asciinema recordings into timeline entries.
metadata:
  author: "GhostWorks"
---

# Timeline Asciinema Parser

Parse terminal recordings (.cast) to infer commands, timestamps, and output for the timeline.

## Input Contract
- Directory input/terminallogs/ containing .cast or .json Asciinema v2 recordings.

## Output
- Write output/terminal_entries.json with entries (timestamp, source, operator, action, details, raw_timestamp).

## Workflow
1. Read the Asciinema header to capture start timestamp, operator username, and recording title.
2. Walk the event stream; when Enter is detected, capture the accumulated command plus its timestamp and output.
3. Infer commands by detecting prompts for shells ($, #, PS C:\\>), Evil-WinRM, Impacket, and offensive CLI prompts.
4. Normalize timestamps relative to the recording start and convert to UTC.
5. Strip ANSI sequences and control characters before inference.
6. Offer export formats (JSON, commands, timeline, text) for downstream verification.

## Notes
- Provide CLI examples for JSON/timeline output and prompt pattern extensions.
- Use prompt-strip helpers before capturing command content.
