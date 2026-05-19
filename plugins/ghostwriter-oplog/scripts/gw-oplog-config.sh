#!/usr/bin/env bash
set -euo pipefail

# Configure ghostwriter-oplog settings in project's .claude/settings.local.json
# Usage: ./ghostwriter-oplog-config.sh [--oplog-id ID] [--operator NAME] [--source-ip IP] [project_path]

usage() {
    echo "Usage: $0 [OPTIONS] [project_path]" >&2
    echo "Options:" >&2
    echo "  --oplog-id ID     Set GW_OPLOG_ID" >&2
    echo "  --operator NAME   Set GW_OPERATOR_NAME" >&2
    echo "  --source-ip IP    Set GW_SOURCE_IP" >&2
    echo "  project_path      Project directory (default: current dir)" >&2
    exit 1
}

# Check for jq
if ! command -v jq &>/dev/null; then
    echo "Error: jq is required but not installed" >&2
    echo "Install: apt install jq / brew install jq" >&2
    exit 1
fi

OPLOG_ID=""
OPERATOR_NAME=""
SOURCE_IP=""
PROJECT_PATH="."

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --oplog-id) OPLOG_ID="$2"; shift 2 ;;
        --operator) OPERATOR_NAME="$2"; shift 2 ;;
        --source-ip) SOURCE_IP="$2"; shift 2 ;;
        --help|-h) usage ;;
        -*) echo "Unknown option: $1" >&2; usage ;;
        *) PROJECT_PATH="$1"; shift ;;
    esac
done

# Require at least one setting
if [[ -z "$OPLOG_ID" && -z "$OPERATOR_NAME" && -z "$SOURCE_IP" ]]; then
    echo "Error: At least one setting required" >&2
    usage
fi

CLAUDE_DIR="$PROJECT_PATH/.claude"
SETTINGS_FILE="$CLAUDE_DIR/settings.local.json"

# Create .claude/ if missing
if [[ ! -d "$CLAUDE_DIR" ]]; then
    mkdir -p "$CLAUDE_DIR"
    echo "Created $CLAUDE_DIR/"
fi

# Initialize or load settings
if [[ ! -f "$SETTINGS_FILE" ]]; then
    echo '{}' > "$SETTINGS_FILE"
    echo "Created $SETTINGS_FILE"
elif ! jq empty "$SETTINGS_FILE" 2>/dev/null; then
    BACKUP="$SETTINGS_FILE.bak.$(date +%s)"
    mv "$SETTINGS_FILE" "$BACKUP"
    echo "Warning: Invalid JSON, backed up to $BACKUP"
    echo '{}' > "$SETTINGS_FILE"
fi

# Apply settings
TMP_FILE=$(mktemp)
cp "$SETTINGS_FILE" "$TMP_FILE"

if [[ -n "$OPLOG_ID" ]]; then
    jq --arg v "$OPLOG_ID" '.env.GW_OPLOG_ID = $v' "$TMP_FILE" > "$TMP_FILE.new" && mv "$TMP_FILE.new" "$TMP_FILE"
    echo "Set GW_OPLOG_ID"
fi

if [[ -n "$OPERATOR_NAME" ]]; then
    jq --arg v "$OPERATOR_NAME" '.env.GW_OPERATOR_NAME = $v' "$TMP_FILE" > "$TMP_FILE.new" && mv "$TMP_FILE.new" "$TMP_FILE"
    echo "Set GW_OPERATOR_NAME"
fi

if [[ -n "$SOURCE_IP" ]]; then
    jq --arg v "$SOURCE_IP" '.env.GW_SOURCE_IP = $v' "$TMP_FILE" > "$TMP_FILE.new" && mv "$TMP_FILE.new" "$TMP_FILE"
    echo "Set GW_SOURCE_IP"
fi

mv "$TMP_FILE" "$SETTINGS_FILE"

# Check .gitignore
GITIGNORE="$PROJECT_PATH/.gitignore"
if [[ -f "$GITIGNORE" ]]; then
    if ! grep -q "settings.local.json" "$GITIGNORE" 2>/dev/null; then
        echo "Warning: Add 'settings.local.json' to .gitignore"
    fi
else
    echo "Warning: No .gitignore found - ensure settings.local.json is not committed"
fi

echo "Done! ghostwriter-oplog configured."
