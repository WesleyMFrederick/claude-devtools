---
name: git-automated-worktree
description: Use when creating git worktrees - LLM determines scope/feature semantically, script handles mechanical execution
---

# Automated Git Worktree Setup

## Overview

This skill uses the setup-worktree.sh script to create isolated git worktrees. The LLM handles semantic work (determining scope/feature from context), while the script handles mechanical execution (git commands, dependency installation, testing).

**Announce at start:** "I'm using the git-automated-worktree skill to set up an isolated workspace."

## When to Use

Use this skill:
- Before executing ANY implementation plan
- When user says "start implementing", "begin development", "execute the plan"
- Before starting feature work that needs isolation from current workspace
- When switching from design/planning to implementation phase

Do NOT use this skill:
- For exploratory prototypes in current directory
- For documentation-only changes
- When explicitly told to work in current directory

## Workflow

### Step 1: Determine Scope and Feature (Semantic - LLM)

Extract scope and feature using this priority:

1. **From plan file path** (if provided):
   - Pattern: `packages/{scope}/` or `tools/{scope}/`
   - Feature from filename: `{feature}.md` → kebab-case
   - Example: `/path/to/packages/ptsf-tools/plans/event-qr-codes.md` → scope="ptsf-tools", feature="event-qr-codes"

2. **From user request** (if no plan file):
   - Parse intent: "create worktree for testing GSD" → scope="gsd", feature="testing-gsd-workflows"
   - Ask clarifying questions if ambiguous using AskUserQuestion
   - Convert to kebab-case

3. **From conversation context**:
   - Review recent discussion to infer scope/feature
   - Reference project structure to validate scope exists

### Step 2: Invoke Script (Mechanical - Script)

Execute the setup script with determined arguments:

```bash
.claude/skills/git-automated-worktree/scripts/setup-worktree.sh <scope> <feature>
```

Example:
```bash
.claude/skills/git-automated-worktree/scripts/setup-worktree.sh gsd testing-gsd-workflows
```

The script handles all mechanical phases:
1. Pre-flight checks (git status, tests)
2. Naming determination
3. Cleanup of existing worktree
4. Worktree creation
5. Dependency installation (with automatic submodule fallback)
6. Verification
7. Test validation
8. Status report

**CRITICAL: Script Error Handling**

If the script exits with non-zero code:
1. **DO NOT manually complete the script's phases** (npm install, build, test)
2. Read the error output to understand what phase failed
3. Report the failure to the user with the error message
4. Let the script's built-in error handling (retries, fallbacks) handle recoverable errors
5. Only escalate to user if script cannot auto-recover

**Why:** The script contains automation specifically to avoid manual work. Manually duplicating script phases defeats the purpose of the automation and indicates the script needs to be fixed, not bypassed.

### Step 3: Report Results (Semantic - LLM)

After script completes, report to user with context:

```
Worktree setup complete:
- Location: /path/to/parent/repo.worktree.scope.feature
- Branch: scope/feature
- Dependencies: installed and verified
- Tests: passing

Ready to begin implementation of [describe the feature in user terms].
```

## Integration with Other Skills

**Pairs with:**
- **writing-plans** - Sets up environment after design is approved
- **executing-plans** or **subagent-driven-development** - Creates isolated workspace for plan execution
- **test-driven-development** - What to do after environment is verified

## Success Criteria

- ✅ LLM correctly determines scope/feature from context
- ✅ Script executes successfully
- ✅ Worktree created in sibling directory
- ✅ Dependencies installed and tests passing
- ✅ User receives clear status report with paths
