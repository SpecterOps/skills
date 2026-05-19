#!/usr/bin/env bash
set -euo pipefail

# Configure Ghostwriter MCP settings in project's .claude/settings.local.json
# Usage: ./gw-mcp-config.sh [OPTIONS] [project_path]

usage() {
    echo "Usage: $0 [OPTIONS] [project_path]" >&2
    echo "Options:" >&2
    echo "  --api-key KEY     Set GHOSTWRITER_API_KEY" >&2
    echo "  --url URL         Set GHOSTWRITER_URL" >&2
    echo "  --ca-bundle PATH  Set GHOSTWRITER_CA_BUNDLE" >&2
    echo "  --project-id ID   Set GHOSTWRITER_PROJECT_ID" >&2
    echo "  --oplog-id ID     Set GHOSTWRITER_OPLOG_ID" >&2
    echo "  --operator NAME   Set GHOSTWRITER_OPERATOR" >&2
    echo "  project_path      Project directory (default: current dir)" >&2
    exit 1
}

# Check for jq
if ! command -v jq &>/dev/null; then
    echo "Error: jq is required but not installed" >&2
    echo "Install: apt install jq / brew install jq" >&2
    exit 1
fi

API_KEY=""
URL=""
CA_BUNDLE=""
PROJECT_ID=""
OPLOG_ID=""
OPERATOR=""
PROJECT_PATH="."

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --api-key) API_KEY="$2"; shift 2 ;;
        --url) URL="$2"; shift 2 ;;
        --ca-bundle) CA_BUNDLE="$2"; shift 2 ;;
        --project-id) PROJECT_ID="$2"; shift 2 ;;
        --oplog-id) OPLOG_ID="$2"; shift 2 ;;
        --operator) OPERATOR="$2"; shift 2 ;;
        --help|-h) usage ;;
        -*) echo "Unknown option: $1" >&2; usage ;;
        *) PROJECT_PATH="$1"; shift ;;
    esac
done

# Require at least one setting
if [[ -z "$API_KEY" && -z "$URL" && -z "$CA_BUNDLE" && -z "$PROJECT_ID" && -z "$OPLOG_ID" && -z "$OPERATOR" ]]; then
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

if [[ -n "$API_KEY" ]]; then
    jq --arg v "$API_KEY" '.env.GHOSTWRITER_API_KEY = $v' "$TMP_FILE" > "$TMP_FILE.new" && mv "$TMP_FILE.new" "$TMP_FILE"
    echo "Set GHOSTWRITER_API_KEY"
fi

if [[ -n "$URL" ]]; then
    jq --arg v "$URL" '.env.GHOSTWRITER_URL = $v' "$TMP_FILE" > "$TMP_FILE.new" && mv "$TMP_FILE.new" "$TMP_FILE"
    echo "Set GHOSTWRITER_URL"
fi

if [[ -n "$CA_BUNDLE" ]]; then
    jq --arg v "$CA_BUNDLE" '.env.GHOSTWRITER_CA_BUNDLE = $v' "$TMP_FILE" > "$TMP_FILE.new" && mv "$TMP_FILE.new" "$TMP_FILE"
    echo "Set GHOSTWRITER_CA_BUNDLE"
fi

if [[ -n "$PROJECT_ID" ]]; then
    jq --arg v "$PROJECT_ID" '.env.GHOSTWRITER_PROJECT_ID = $v' "$TMP_FILE" > "$TMP_FILE.new" && mv "$TMP_FILE.new" "$TMP_FILE"
    echo "Set GHOSTWRITER_PROJECT_ID"
fi

if [[ -n "$OPLOG_ID" ]]; then
    jq --arg v "$OPLOG_ID" '.env.GHOSTWRITER_OPLOG_ID = $v' "$TMP_FILE" > "$TMP_FILE.new" && mv "$TMP_FILE.new" "$TMP_FILE"
    echo "Set GHOSTWRITER_OPLOG_ID"
fi

if [[ -n "$OPERATOR" ]]; then
    jq --arg v "$OPERATOR" '.env.GHOSTWRITER_OPERATOR = $v' "$TMP_FILE" > "$TMP_FILE.new" && mv "$TMP_FILE.new" "$TMP_FILE"
    echo "Set GHOSTWRITER_OPERATOR"
fi

mv "$TMP_FILE" "$SETTINGS_FILE"

# Check .gitignore
GITIGNORE="$PROJECT_PATH/.gitignore"
if [[ -f "$GITIGNORE" ]]; then
    if ! grep -q "settings.local.json" "$GITIGNORE" 2>/dev/null; then
        echo "Warning: Add 'settings.local.json' to .gitignore to protect secrets"
    fi
else
    echo "Warning: No .gitignore found - ensure settings.local.json is not committed"
fi

echo "Done! Ghostwriter MCP configured."
