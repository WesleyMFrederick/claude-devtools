#!/usr/bin/env bash
# citation-extractor.sh - Extracts citation content after reading markdown files
#
# SYNOPSIS
#   citation-extractor.sh
#
# DESCRIPTION
#   Automatically runs jact extract links on markdown files after Read operations.
#   Injects extracted content as context for Claude via JSON hookSpecificOutput.
#   Receives hook input via stdin from Claude Code PostToolUse event.
#
#   Passes --session to jact for session-based caching (cache logic
#   lives in the tool, not the hook).
#
# EXIT CODES
#   0 - Always (non-blocking, context injection only)

set +e  # Don't exit on errors - we control exit codes

# Debug logging
DEBUG_LOG="/tmp/citation-hook-debug.log"
echo "=== Hook invoked at $(date) ===" >> "$DEBUG_LOG"
echo "CLAUDE_PROJECT_DIR: [$CLAUDE_PROJECT_DIR]" >> "$DEBUG_LOG"
echo "PWD: $(pwd)" >> "$DEBUG_LOG"

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "EXIT: jq not available" >> "$DEBUG_LOG"
    exit 0  # Silently skip if jq not available
fi
echo "jq: available" >> "$DEBUG_LOG"

# Resolve jact: prefer local build, fallback to global
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_CM="$SCRIPT_DIR/../../../dist/jact.js"
if [[ -f "$LOCAL_CM" ]]; then
    CM_CMD="node $LOCAL_CM"
    echo "jact: local build ($LOCAL_CM)" >> "$DEBUG_LOG"
elif command -v jact &> /dev/null; then
    CM_CMD="jact"
    echo "jact: global" >> "$DEBUG_LOG"
else
    echo "EXIT: jact not available" >> "$DEBUG_LOG"
    exit 0
fi

# Read JSON input from stdin
if [[ -t 0 ]]; then
    # No stdin available (not running as a hook)
    echo "EXIT: No stdin available" >> "$DEBUG_LOG"
    exit 0
fi
echo "stdin: available" >> "$DEBUG_LOG"

# Parse hook input
json_input=$(cat)
echo "json_input received: ${json_input:0:200}..." >> "$DEBUG_LOG"

# Extract session_id and file path from hook input
session_id=$(echo "$json_input" | jq -r '.session_id // empty' 2>/dev/null)
file_path=$(echo "$json_input" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
echo "session_id: [$session_id]" >> "$DEBUG_LOG"
echo "file_path: [$file_path]" >> "$DEBUG_LOG"

# Check if we got required data
if [[ -z "$file_path" || "$file_path" == "null" ]]; then
    echo "EXIT: No file_path in input" >> "$DEBUG_LOG"
    exit 0
fi

if [[ -z "$session_id" || "$session_id" == "null" ]]; then
    # No session_id available, skip caching
    session_id="no-session"
fi

# Check if the file is a markdown file
if [[ ! "$file_path" =~ \.md$ ]]; then
    echo "EXIT: Not a markdown file" >> "$DEBUG_LOG"
    exit 0
fi
echo "file type: markdown" >> "$DEBUG_LOG"

# Check if file exists
if [[ ! -f "$file_path" ]]; then
    echo "EXIT: File does not exist" >> "$DEBUG_LOG"
    exit 0
fi
echo "file exists: yes" >> "$DEBUG_LOG"

# Run jact extract links — capture exit code separately from output
echo "Running: $CM_CMD extract links $file_path --session $session_id" >> "$DEBUG_LOG"
raw_output=$($CM_CMD extract links "$file_path" --session "$session_id" 2>/dev/null)
cm_exit_code=$?
echo "cm_exit_code: $cm_exit_code, raw_output length: ${#raw_output}" >> "$DEBUG_LOG"

# Distinguish three exit conditions by exit code + output
if [[ $cm_exit_code -eq 0 && -z "$raw_output" ]]; then
    echo "EXIT: Citations have already been extracted in this session. Review your context window. (session: ${session_id})" >> "$DEBUG_LOG"
    exit 0
elif [[ $cm_exit_code -eq 1 ]]; then
    echo "EXIT: No citations found in $file_path" >> "$DEBUG_LOG"
    exit 0
elif [[ $cm_exit_code -eq 2 || -z "$raw_output" ]]; then
    echo "EXIT: Extraction error (exit code: $cm_exit_code)" >> "$DEBUG_LOG"
    exit 0
fi

# Filter to extractedContentBlocks
extracted_content=$(echo "$raw_output" | jq '.extractedContentBlocks' 2>/dev/null)
echo "extracted_content length: ${#extracted_content}" >> "$DEBUG_LOG"

# Check if content is usable
if [[ -z "$extracted_content" || "$extracted_content" == "null" || "$extracted_content" == "{}" ]]; then
    echo "EXIT: Extraction returned no content blocks" >> "$DEBUG_LOG"
    exit 0
fi
echo "extraction: successful" >> "$DEBUG_LOG"

# Format the extracted content for Claude
# Filter out _totalContentCharacterLength and format remaining blocks
formatted_content=$(echo "$extracted_content" | jq -r 'to_entries | map(select(.key != "_totalContentCharacterLength")) | map("## Citation: \(.key)\n\n\(.value.content)\n") | join("\n---\n\n")' 2>/dev/null)
echo "formatted_content length: ${#formatted_content}" >> "$DEBUG_LOG"

if [[ -z "$formatted_content" || "$formatted_content" == "null" ]]; then
    echo "EXIT: Formatting failed" >> "$DEBUG_LOG"
    exit 0
fi
echo "formatting: successful" >> "$DEBUG_LOG"

# Output JSON with hookSpecificOutput for context injection
echo "Generating JSON output..." >> "$DEBUG_LOG"
output=$(jq -n \
  --arg content "$formatted_content" \
  '{
    "hookSpecificOutput": {
      "hookEventName": "PostToolUse",
      "additionalContext": $content
    }
  }')
echo "JSON output generated (length: ${#output})" >> "$DEBUG_LOG"
echo "$output"
echo "EXIT: Success - JSON output sent" >> "$DEBUG_LOG"

exit 0
