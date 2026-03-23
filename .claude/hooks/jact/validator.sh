#!/usr/bin/env bash
# citation-validator.sh - Validates markdown files with jact after edits/writes
#
# SYNOPSIS
#   citation-validator.sh
#
# DESCRIPTION
#   Automatically runs jact validate on markdown files after Edit/Write operations.
#   Receives hook input via stdin from Claude Code PostToolUse event.
#
# EXIT CODES
#   0 - Success (not a markdown file or validation passed)
#   2 - Validation errors found (blocking - Claude must fix)

set +e  # Don't exit on errors - we control exit codes

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} jq is required but not installed" >&2
    exit 1
fi

# Check if jact is available
if ! command -v jact &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} jact is required but not installed" >&2
    exit 1
fi

# Read JSON input from stdin
if [[ -t 0 ]]; then
    # No stdin available (not running as a hook)
    echo -e "${YELLOW}[INFO]${NC} This script is designed to run as a Claude Code hook" >&2
    exit 0
fi

# Parse hook input
json_input=$(cat)

# Extract file path from hook input
file_path=$(echo "$json_input" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

# Check if we got a file path
if [[ -z "$file_path" || "$file_path" == "null" ]]; then
    # Not a file operation or no file path - exit silently
    exit 0
fi

# Check if the file is a markdown file
if [[ ! "$file_path" =~ \.md$ ]]; then
    # Not a markdown file - exit silently
    exit 0
fi

# Skip test fixtures
if [[ "$file_path" =~ /test/fixtures/ ]]; then
    # Test fixture - exit silently
    exit 0
fi

# Check if file exists
if [[ ! -f "$file_path" ]]; then
    echo -e "${YELLOW}[WARNING]${NC} File does not exist: $file_path" >&2
    exit 0
fi

echo "" >&2
echo -e "${BLUE}🔗 Citation Validation${NC} - Checking markdown citations..." >&2
echo "────────────────────────────────────────────" >&2

# Run jact validate
validation_output=$(jact validate "$file_path" 2>&1)
validation_exit_code=$?

if [[ $validation_exit_code -eq 0 ]]; then
    # Validation passed
    echo -e "${GREEN}✅ Citations validated successfully${NC} in $file_path" >&2
    exit 0
else
    # Validation failed
    echo -e "${RED}❌ Citation validation failed${NC} in $file_path" >&2
    echo "" >&2
    echo "$validation_output" >&2
    echo "" >&2
    echo -e "${RED}════════════════════════════════════════════${NC}" >&2
    echo -e "${RED}❌ CITATION ERRORS ARE BLOCKING ❌${NC}" >&2
    echo -e "${RED}════════════════════════════════════════════${NC}" >&2
    echo -e "${YELLOW}📋 NEXT STEPS:${NC}" >&2
    echo -e "${YELLOW}  1. Fix the citation errors listed above${NC}" >&2
    echo -e "${YELLOW}  2. Run 'jact validate $file_path' to verify${NC}" >&2
    echo -e "${YELLOW}  3. Continue with your original task${NC}" >&2

    # Exit with code 2 to block and show stderr to Claude
    exit 2
fi
