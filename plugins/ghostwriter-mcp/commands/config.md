---
description: Interactive Ghostwriter setup - configure API, select project & oplog
arguments:
  - name: options
    description: "Optional: --api-key KEY, --url URL, --ca-bundle PATH"
    required: false
---

# Ghostwriter MCP Configuration Wizard

Follow these steps in order:

## Step 1: Save Credential Options (if provided)

If the user provided any credential options (--api-key, --url, --ca-bundle), run:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/gw-mcp-config.sh $ARGUMENTS
```

## Step 2: Verify API Connection

Use the `whoami` MCP tool to verify the API connection works. This returns the authenticated user's info including their username.

If the connection fails, tell the user credentials may be missing or invalid, then proceed to credential configuration:

### API Key Configuration

Use AskUserQuestion with free text input for API key, or option "I'll get it later" to skip.

### URL Configuration

Use AskUserQuestion with free text input for Ghostwriter URL, or option "I'll get it later" to skip.

### CA Bundle Configuration

Use AskUserQuestion with:
- Option 1: "Provide CA bundle path" - lets user enter path to CA certificate bundle
- Option 2: "Disable SSL verification" - sets GHOSTWRITER_CA_BUNDLE to "false"

If user provides a path, use `--ca-bundle PATH`. If user disables SSL, use `--ca-bundle false`.

### Apply Credentials

If any credentials were provided, run the config script with those values:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/gw-mcp-config.sh [--api-key KEY] [--url URL] [--ca-bundle PATH]
```

Then retry whoami to verify the connection works.

Extract the `username` field from the whoami response - this is the operator name.

## Step 3: Select Active Project

Use the `list_projects` MCP tool with `complete: false` to get active (not completed) projects.

The response includes projects with their oplogs. Present the projects to the user showing:
- Project ID
- Codename
- Client name
- Start/end dates

Use AskUserQuestion to let the user select which project they want to work with. Include up to 4 projects as options; if more exist, add a note that they can provide another project ID.

## Step 4: Select Oplog

From the selected project's data in the list_projects response, get the available oplogs.

Each project has an `oplogs` array with oplog entries containing:
- id
- name

Use AskUserQuestion to let the user select which oplog to use for this project.

## Step 5: Save Configuration

Run the config script to save the selections:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/gw-mcp-config.sh --operator "OPERATOR_NAME" --project-id "PROJECT_ID" --oplog-id "OPLOG_ID"
```

Replace OPERATOR_NAME, PROJECT_ID, and OPLOG_ID with the values gathered above.

## Step 6: Confirm Setup

Tell the user the setup is complete and show:
- Operator: (username from whoami)
- Project: (selected project codename)
- Oplog: (selected oplog name)

**Important:** Warn the user they must exit and restart Claude Code for the new settings to take effect.
