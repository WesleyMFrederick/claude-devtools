# Continuous Learning — Eval 2: Mixed Friction (3 Patterns)

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

### Delta 1: Context-aware file reads
**Domain: Skill/prompt**
- Add memory file: `feedback_context-window-discipline.md` — reinforcing "check session context before re-reading"
- Already in MEMORY.md but agent isn't following it. Strengthen CLAUDE.md wording.

### Delta 2: jact absolute paths
**Domain: Skill/prompt**
- CLAUDE.md already has the rule. Strengthen with explicit example showing wrong (relative) vs right (absolute).
- Consider adding a wrapper script that auto-resolves to absolute path.

### Delta 3: Auto-touch after markdown edits
**Domain: Code (hook)**
- PostToolUse:Write/Edit hook that checks if the edited file is a `.md` in project root, then runs `touch` on it.
- This is deterministic — route to a tool, not an LLM instruction.

### Coverage verification:
- Delta 1: memory + CLAUDE.md strengthening
- Delta 2: CLAUDE.md + wrapper script
- Delta 3: PostToolUse hook

### Open items:
- [H] A PostToolUse hook for touch will eliminate all manual touch calls
- [Q] Should the jact wrapper be a shell script or integrated into the hook system?
- [A] Write the touch hook and test it

**HARD GATE**: Presenting Delta architecture to user. Waiting for user to lock architecture before proceeding.

---

## Phase 6: DIFF Expression

### DIFF-1: Strengthen CLAUDE.md context-window discipline
**Covers: BID row 1** (small diff — inline)

```diff
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ context-window section
+**Context Window Discipline (CRITICAL):**
+- Before issuing a Read call, check if the file was already read in this session
+- If content is in session context, reference it directly — do NOT re-read
+- This saves tokens and avoids user frustration from redundant operations
```

### DIFF-2: Add jact absolute path example to CLAUDE.md
**Covers: BID row 2** (small diff — inline)

```diff
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ jact section
 - **jact requires absolute file paths.**
+- Wrong: `jact validate ./docs/file.md`
+- Right: `jact validate /Users/wesleyfrederick/Documents/.../docs/file.md`
```

### DIFF-3: PostToolUse hook for auto-touch markdown in root
**Covers: BID row 3** (small diff — inline)

```diff
--- /dev/null
+++ b/.claude/hooks/touch-root-md.sh
@@ -0,0 +1,8 @@
+#!/bin/bash
+# Auto-touch .md files in project root after Write/Edit
+FILE="$1"
+PROJECT_ROOT="$(git rev-parse --show-toplevel)"
+DIR="$(dirname "$FILE")"
+if [[ "$DIR" == "$PROJECT_ROOT" && "$FILE" == *.md ]]; then
+  touch "$FILE"
+fi
```

**HARD GATE**: Waiting for user to approve DIFFs before any edit takes effect.

---

## Phase 7: Apply
(Awaiting user approval of DIFFs above)
