# Cobalt Strike Aggressor Function Reference

This directory contains individual documentation files for 421 Cobalt Strike Aggressor Script functions. Each function has its own markdown file named after the function (lowercase).

## Usage

To look up a function, simply open the corresponding `.md` file. For example:
- `addvisualization.md` - Documentation for the `addVisualization` function
- `beacon_info.md` - Documentation for the `beacon_info` function
- `bshell.md` - Documentation for the `bshell` function

## Organization

All functions are stored in individual files with lowercase filenames matching the function name. This makes it easy to:
- Load only the specific function documentation you need
- Keep context windows small when using these as skill resources
- Quickly find and reference specific functions

## Categories

The functions are organized into several categories:

### Beacon Commands (b* prefix)
Functions that control Beacon sessions and execute commands on compromised systems.
- Examples: `bshell`, `bupload`, `bdownload`, `bps`, `bkill`, etc.

### Listener Functions
Functions for managing listeners and payload delivery.
- Examples: `listener_create`, `listener_delete`, `listener_info`, etc.

### Dialog Functions
Functions for creating UI dialogs and components.
- Examples: `dialog`, `drow_*`, `dbutton_*`, etc.

### Data Functions
Functions for data manipulation and encoding.
- Examples: `base64_encode`, `gzip`, `gunzip`, `transform`, etc.

### Event Functions
Functions for event handling and custom events.
- Examples: `on`, `fireEvent`, `custom_event`, etc.

### Open Dialog Functions
Functions for opening various Cobalt Strike dialogs.
- Examples: `openBeaconBrowser`, `openCredentialManager`, `openScriptConsole`, etc.

### PE Manipulation Functions
Functions for modifying portable executable files.
- Examples: `pe_mask`, `pe_set_*`, `pe_stomp`, etc.

### Artifact Functions
Functions for generating artifacts and payloads.
- Examples: `artifact`, `artifact_general`, `artifact_payload`, etc.

### Beacon Registration Functions
Functions for registering custom beacon commands and features.
- Examples: `beacon_command_register`, `beacon_elevator_register`, etc.

## Source

This documentation was extracted from the official Cobalt Strike user guide:
https://hstechdocs.helpsystems.com/manuals/cobaltstrike/current/userguide/content/topics_aggressor-scripts/as-resources_functions.htm

## File Naming Convention

All function files use lowercase naming:
- Function `addVisualization` → File `addvisualization.md`
- Function `beacon_info` → File `beacon_info.md`
- Function `bShell` → File `bshell.md`

Functions starting with special characters (like `-is64`) keep the special character in the filename:
- Function `-is64` → File `-is64.md`
