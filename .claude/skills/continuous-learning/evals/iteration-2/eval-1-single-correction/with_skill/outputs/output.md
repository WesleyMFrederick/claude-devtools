# Continuous Learning — Eval 1 (Iteration 2): Single Correction (bun vs npm)

## Phase 0: Read Context
Read MEMORY.md and session transcript.

## Phase 1: Surface Friction → Findings Table

| ID | Pattern Found | Scope | Trigger | Friction Caused |
|----|--------------|-------|---------|-----------------|
| F-1 | User Correction | global | Claude ran `npm install` instead of `bun add` | User had to intervene 3 times to correct package manager |
| F-2 | User Correction | global | Claude ran `npx` instead of `bunx` | Same root cause as F-1, different command |
| F-3 | Error Resolution | specific workflow | `npm` command failed or produced unexpected output | Time wasted on wrong tool output before correction |

## Phase 2: BI Table in [O] Units

| # | Baseline [O] | Ideal [O] |
|---|-------------|-----------|
| 1 | [O] User corrects Claude's package manager choice on each invocation | [O] User never needs to correct Claude's package manager choice |
| 2 | [O] Claude defaults to npm/npx commands in a bun-configured project | [O] Claude uses bun/bunx commands in any project with bun.lockb or bunfig.toml |
| 3 | [O] User loses focus context-switching to correct tool commands | [O] User maintains focus because tool commands are correct on first attempt |

Self-checks:
- Like-for-like: All rows are [O] ↔ [O] ✓
- Immutability: All 3 Baseline rows from findings preserved ✓

**HARD GATE**: Presenting BI table to user. Waiting for user to lock BI table before proceeding.

---

## Phase 3: BDI Table in [O] Units

| # | Baseline [O] | Delta [O] | Ideal [O] |
|---|-------------|-----------|-----------|
| 1 | [O] User corrects Claude's package manager choice on each invocation | [O] Claude detects project package manager from lockfile and uses it without prompting | [O] User never needs to correct Claude's package manager choice |
| 2 | [O] Claude defaults to npm/npx commands in a bun-configured project | [O] Claude reads project signals (bun.lockb, bunfig.toml, CLAUDE.md) to select correct package manager | [O] Claude uses bun/bunx commands in any project with bun.lockb or bunfig.toml |
| 3 | [O] User loses focus context-switching to correct tool commands | (blank — follows from rows 1-2) | [O] User maintains focus because tool commands are correct on first attempt |

Self-checks:
- Row 1: Applying "Claude detects package manager" to "user corrects on each invocation" → "user never corrects" ✓
- Row 2: Applying "reads project signals" to "defaults to npm" → "uses bun in bun projects" ✓
- Row 3: Untargeted — Delta blank, Baseline carries through ✓

**HARD GATE**: Presenting BDI table to user. Waiting for user to lock BDI table before proceeding.

---

## Phase 4: Baseline → Source Mapping

| # | Baseline Outcome | Source | Baseline Notes |
|---|-----------------|--------|----------------|
| 1 | User corrects Claude's package manager choice | Session transcript: messages 12, 28, 41 — user said "use bun not npm" | Correction happened 3 times across different command types |
| 2 | Claude defaults to npm/npx | CLAUDE.md:L8 — "This project uses **bun**" already present but not followed | Instruction exists but is overridden by training prior |
| 3 | User loses focus context-switching | Session transcript: message 42 — user expressed frustration | Cumulative friction from repeated corrections |

## Phase 5: Delta Architecture

**Deterministic offloading classification:**
- F-1/F-2 (wrong package manager): **Mechanical** — identical inputs (npm command) should always yield identical result (block and suggest bun). This belongs in a hook, not a CLAUDE.md rule.
- F-3 (error from wrong tool): Resolved by fixing F-1/F-2.

Fix path priority applied:

### Delta 1+2: Block npm/npx at the hook level

**Priority 1 — Hook (PreToolUse:Bash)**
- PreToolUse:Bash hook that pattern-matches `npm`, `npx`, `yarn` commands and blocks execution
- Returns a message: "This project uses bun. Use `bun add` instead of `npm install`, `bunx` instead of `npx`."
- Deterministic: identical inputs → identical block. No LLM judgment needed.

**Priority 3 — CLAUDE.md rule (backup)**
- Strengthen existing Package Manager section with explicit wrong/right examples
- This is backup guidance if the hook isn't installed; the hook is the primary fix.

### Coverage verification:
- Delta row 1: Hook blocks npm commands (primary), CLAUDE.md reinforces (backup)
- Delta row 2: Same hook + CLAUDE.md
- Row 3: Untargeted — resolved by rows 1+2

### Open items:
- [Q] Should the hook auto-replace npm→bun or just block and suggest?
- [H] A PreToolUse hook will eliminate 100% of npm invocations regardless of CLAUDE.md compliance

**HARD GATE**: Presenting Delta architecture to user. Waiting for user to lock architecture before proceeding.

---

## Phase 6: DIFF Expression

### DIFF-1: PreToolUse:Bash hook to block npm/npx/yarn
**Covers: BID rows 1, 2** (small diff — inline)

```diff
--- /dev/null
+++ b/.claude/hooks/block-npm.sh
@@ -0,0 +1,12 @@
+#!/bin/bash
+# PreToolUse:Bash — block npm/npx/yarn in bun projects
+COMMAND="$1"
+if echo "$COMMAND" | grep -qE '^\s*(npm|npx|yarn)\b'; then
+  echo "BLOCKED: This project uses bun, not npm."
+  echo "Use: bun add (not npm install), bunx (not npx), bun run (not npm run)"
+  exit 1
+fi
```

### DIFF-2: Strengthen CLAUDE.md Package Manager section (backup)
**Covers: BID rows 1, 2** (small diff — inline)

```diff
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ Package Manager section
 This project uses **bun** (not npm/npx). Always use `bun` for:
 - Running scripts: `bun run <script>`
 - Installing packages: `bun add <package>`
+- NEVER use `npm`, `npx`, or `yarn` — a PreToolUse hook blocks these commands
+- Wrong: `npm install foo` → Right: `bun add foo`
+- Wrong: `npx some-tool` → Right: `bunx some-tool`
```

**HARD GATE**: Waiting for user to approve DIFFs before any edit takes effect.

---

## Phase 7: Apply
(Awaiting user approval of DIFFs above)
