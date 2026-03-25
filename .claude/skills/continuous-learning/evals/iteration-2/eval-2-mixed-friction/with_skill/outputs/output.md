# Continuous Learning — Eval 2 (Iteration 2): Mixed Friction (3 Patterns)

## Phase 0: Read Context
Read MEMORY.md and session transcript.

## Phase 1: Surface Friction → Findings Table

| ID | Pattern Found | Scope | Trigger | Friction Caused |
|----|--------------|-------|---------|-----------------|
| F-1 | Repeated Workflow | global | Claude re-read files already loaded earlier in session | Wasted tokens and time; user said "I already showed you that file" |
| F-2 | Error Resolution | specific workflow (jact) | jact validate called with relative path instead of absolute | Validation failed twice before correct path was used |
| F-3 | Repeated Workflow | specific workflow (markdown editing) | User had to manually run `touch` after every markdown edit in project root | Extra step after every edit, easily automatable |

## Phase 2: BI Table in [O] Units

| # | Baseline [O] | Ideal [O] |
|---|-------------|-----------|
| 1 | [O] Claude re-reads files that were already loaded in the current session | [O] Claude references previously-read file content from session context without redundant reads |
| 2 | [O] Claude calls jact with relative paths, causing validation failures | [O] Claude calls jact with absolute paths on every invocation |
| 3 | [O] User manually runs touch after every markdown edit in project root | [O] Markdown files in project root are automatically touched after edits |

Self-checks:
- Like-for-like: All rows [O] ↔ [O] ✓
- Immutability: All 3 Baseline rows from findings preserved ✓

**HARD GATE**: Presenting BI table to user. Waiting for user to lock BI table before proceeding.

---

## Phase 3: BDI Table in [O] Units

| # | Baseline [O] | Delta [O] | Ideal [O] |
|---|-------------|-----------|-----------|
| 1 | [O] Claude re-reads files already loaded in session | [O] Claude checks session context before issuing Read calls for previously-loaded files | [O] Claude references previously-read content without redundant reads |
| 2 | [O] Claude calls jact with relative paths | [O] Claude resolves all jact file arguments to absolute paths before invocation | [O] Claude calls jact with absolute paths on every invocation |
| 3 | [O] User manually runs touch after markdown edits | [O] A post-edit hook automatically touches markdown files in project root | [O] Markdown files in project root are automatically touched after edits |

Self-checks:
- Row 1: "checks context before Read" applied to "re-reads loaded files" → "references without redundant reads" ✓
- Row 2: "resolves to absolute" applied to "calls with relative" → "calls with absolute" ✓
- Row 3: "post-edit hook touches files" applied to "user manually touches" → "automatically touched" ✓

**HARD GATE**: Presenting BDI table to user. Waiting for user to lock BDI table before proceeding.

---

## Phase 4: Baseline → Source Mapping

| # | Baseline Outcome | Source | Baseline Notes |
|---|-----------------|--------|----------------|
| 1 | Claude re-reads loaded files | Session transcript: Read calls on messages 15, 32 for files loaded at messages 3, 8 | MEMORY.md already has "Context Window Discipline" entry |
| 2 | jact called with relative paths | Session transcript: jact validate failures at messages 20, 22; success at message 24 | CLAUDE.md has "JACT CLI PATH RULE" with absolute path requirement |
| 3 | User manually touches markdown | Session transcript: user ran `touch` after messages 35, 42, 48 | CLAUDE.md has "Touch After Write" section |

## Phase 5: Delta Architecture

**Deterministic offloading classification:**
- F-1 (redundant reads): **Mechanical** — file identity is deterministic (hash comparison). A hook can detect re-reads without LLM judgment.
- F-2 (relative paths): **Mechanical** — path resolution is deterministic. Could be a wrapper script.
- F-3 (missing touch): **Mechanical** — post-edit touch is deterministic. A PostToolUse hook is the correct fix.

Fix path priority applied:

### Delta 1: PreToolUse:Read hook for file deduplication
**Priority 1 — Hook (PreToolUse:Read)**
- PreToolUse:Read hook that hashes file content on first read, stores in session cache
- On subsequent Read of same file: if hash matches, injects reminder "This file was already read (hash unchanged). Content is in session context."
- Deterministic: identical file → identical hash → identical reminder. No LLM judgment needed.
- Reference: jact already implements this pattern with its citation cache.

### Delta 2: jact path resolution
**Priority 2 — Script/tool**
- Wrapper script or shell alias that auto-resolves relative paths to absolute before passing to jact
- Alternatively, strengthen CLAUDE.md rule with concrete wrong/right examples (Priority 3 fallback)

### Delta 3: PostToolUse:Write/Edit hook for auto-touch
**Priority 1 — Hook (PostToolUse:Write, PostToolUse:Edit)**
- PostToolUse hook that checks if edited file is `.md` in project root
- If yes, runs `touch` on the file
- Deterministic: file path + extension → touch or skip. No LLM judgment.

### Coverage verification:
- Delta 1: PreToolUse:Read hook
- Delta 2: Wrapper script + CLAUDE.md examples
- Delta 3: PostToolUse hook

### Open items:
- [H] PreToolUse:Read hash-check hook will eliminate redundant reads without relying on LLM memory
- [Q] Should the Read hook block the re-read entirely or just inject a reminder?
- [A] jact's cache pattern is the reference implementation for file dedup

**HARD GATE**: Presenting Delta architecture to user. Waiting for user to lock architecture before proceeding.

---

## Phase 6: DIFF Expression

### DIFF-1: PreToolUse:Read hook for file deduplication
**Covers: BID row 1** (small diff — inline)

```diff
--- /dev/null
+++ b/.claude/hooks/read-dedup.sh
@@ -0,0 +1,14 @@
+#!/bin/bash
+# PreToolUse:Read — remind if file was already read this session
+FILE="$1"
+CACHE_DIR="/tmp/claude-read-cache-$$"
+mkdir -p "$CACHE_DIR"
+HASH=$(md5 -q "$FILE" 2>/dev/null || echo "new")
+CACHE_FILE="$CACHE_DIR/$(echo "$FILE" | md5 -q)"
+if [ -f "$CACHE_FILE" ] && [ "$(cat "$CACHE_FILE")" = "$HASH" ]; then
+  echo "REMINDER: $FILE was already read this session (hash unchanged)."
+  echo "Content is in your session context. Consider referencing it instead."
+fi
+echo "$HASH" > "$CACHE_FILE"
```

### DIFF-2: PostToolUse:Write/Edit hook for auto-touch markdown
**Covers: BID row 3** (small diff — inline)

```diff
--- /dev/null
+++ b/.claude/hooks/touch-root-md.sh
@@ -0,0 +1,8 @@
+#!/bin/bash
+# PostToolUse:Write,Edit — auto-touch .md files in project root
+FILE="$1"
+PROJECT_ROOT="$(git rev-parse --show-toplevel)"
+DIR="$(dirname "$FILE")"
+if [[ "$DIR" == "$PROJECT_ROOT" && "$FILE" == *.md ]]; then
+  touch "$FILE"
+fi
```

### DIFF-3: Strengthen CLAUDE.md jact path examples
**Covers: BID row 2** (small diff — inline)

```diff
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ jact section
 - **jact requires absolute file paths.**
+- Wrong: `jact validate ./docs/file.md`
+- Right: `jact validate /Users/wesleyfrederick/Documents/.../docs/file.md`
+- Always resolve with `$(realpath <file>)` before passing to jact
```

**HARD GATE**: Waiting for user to approve DIFFs before any edit takes effect.

---

## Phase 7: Apply
(Awaiting user approval of DIFFs above)
