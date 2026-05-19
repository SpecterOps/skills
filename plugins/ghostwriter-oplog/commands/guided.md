---
description: Guided walkthrough to create a detailed oplog entry with evidence
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
  - mcp__ghostwriter__create_oplog_entry
---

Interactively guide the user through creating a detailed oplog entry.

## Steps

1. Verify required env vars exist (`GW_OPLOG_ID`, `GW_OPERATOR_NAME`). If missing, tell user to run `/ghostwriter-oplog:config` and stop.

2. Use AskUserQuestion to ask for **entry type**:
   - "Command execution" - ran a tool/command
   - "Discovery" - found something interesting
   - "Credential access" - obtained creds
   - "Evidence capture" - documenting with file

3. Ask for **description** (free text via "Other" option or suggest based on type):
   - Command: "Executed [tool] against [target]"
   - Discovery: "Found [what] on [where]"
   - Credential: "Obtained [type] for [account]"
   - Evidence: "Captured [what] from [where]"

4. Ask if there's an **evidence file** to attach:
   - "Yes, attach a file"
   - "No evidence file"

   If yes, ask for file path. Read the file (handle binary files appropriately).

5. Ask for **destination IP** (target):
   - "No specific target"
   - Or enter IP/hostname

6. Ask for **tool used**:
   - "Nmap"
   - "Burp Suite"
   - "BloodHound"
   - Other (free text)

7. Ask for **tags** (multi-select):
   - "creds" - credential access
   - "vuln" - vulnerability
   - "objective:1" - objective achieved
   - "ttp:TXXXX" - MITRE technique

   Allow custom tags via Other.

8. Get timestamp: `date -u +"%Y-%m-%dT%H:%M:%SZ"`

9. Call `create_oplog_entry` with all gathered fields:
   - `oplog_id`: from GW_OPLOG_ID
   - `operator_name`: from GW_OPERATOR_NAME
   - `source_ip`: from GW_SOURCE_IP (if set)
   - `dest_ip`: from step 5
   - `tool`: from step 6
   - `description`: from step 3
   - `output`: file contents from step 4 (if any)
   - `start_date`: from step 8
   - `tags`: from step 7

10. Confirm entry was logged with entry ID and summary of fields recorded.
