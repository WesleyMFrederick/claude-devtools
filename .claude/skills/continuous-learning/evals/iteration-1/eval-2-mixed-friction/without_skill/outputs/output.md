# Session Friction Analysis: Mixed Issues

## Issues Found

### 1. Redundant File Reads
Claude re-read files that were already in the session context. This wasted tokens and frustrated the user.

**Fix:** Add a CLAUDE.md rule: "Before reading a file, check if it was already loaded in this session."

### 2. jact Path Errors
jact validate was called with relative paths, causing failures. The tool requires absolute paths.

**Fix:** The CLAUDE.md already has this rule but it's not being followed. Strengthen the wording and add wrong/right examples.

### 3. Missing touch After Edits
User had to manually run `touch` on markdown files after each edit to trigger Obsidian refresh.

**Fix:** Create a PostToolUse hook that automatically touches `.md` files in the project root after Write/Edit operations.

## Proposed Changes

1. Strengthen CLAUDE.md context-window discipline section
2. Add explicit wrong/right examples to jact path rule
3. Create a post-edit hook script for auto-touching markdown files
4. Add memory entries for recurring friction patterns

## Priority
- Hook for auto-touch: **High** (eliminates manual step on every edit)
- jact path examples: **Medium** (rule exists, needs reinforcement)
- Context discipline: **Medium** (saves tokens, reduces user frustration)
