# Continuous Learning — Eval 3 (Iteration 2): Large Diff (Commit Messages + Worktree Cleanup)

## Phase 0: Read Context
Read MEMORY.md and session transcript.

## Phase 1: Surface Friction → Findings Table

| ID | Pattern Found | Scope | Trigger | Friction Caused |
|----|--------------|-------|---------|-----------------|
| F-1 | User Correction | global | Claude used generic "update" in every commit message | User had to rewrite commit messages or ask Claude to redo them |
| F-2 | Tool Preferences | specific workflow (git worktree) | Worktree skill doesn't clean up merged branches | Stale branches accumulate; user has to manually delete them |

## Phase 2: BI Table in [O] Units

| # | Baseline [O] | Ideal [O] |
|---|-------------|-----------|
| 1 | [O] Claude generates commit messages using generic "update" verb regardless of change type | [O] Claude generates commit messages that accurately describe the nature of changes (add, fix, refactor, etc.) |
| 2 | [O] Worktree branches remain after merge, requiring manual cleanup | [O] Worktree branches are automatically cleaned up after successful merge |

Self-checks:
- Like-for-like: Both rows [O] ↔ [O] ✓
- Immutability: Both Baseline rows from findings preserved ✓

**HARD GATE**: Presenting BI table to user. Waiting for user to lock BI table before proceeding.

---

## Phase 3: BDI Table in [O] Units

| # | Baseline [O] | Delta [O] | Ideal [O] |
|---|-------------|-----------|-----------|
| 1 | [O] Claude generates generic "update" commit messages | [O] Claude classifies each change by type (add/fix/refactor/docs) and uses the appropriate verb in commit messages | [O] Claude generates accurate, type-specific commit messages |
| 2 | [O] Worktree branches remain after merge | [O] Worktree finish workflow includes branch deletion after successful merge | [O] Worktree branches are automatically cleaned up after merge |

Self-checks:
- Row 1: "classifies change type" applied to "generic update" → "type-specific messages" ✓
- Row 2: "finish includes branch deletion" applied to "branches remain" → "branches cleaned up" ✓

**HARD GATE**: Presenting BDI table to user. Waiting for user to lock BDI table before proceeding.

---

## Phase 4: Baseline → Source Mapping

| # | Baseline Outcome | Source | Baseline Notes |
|---|-----------------|--------|----------------|
| 1 | Generic "update" commit messages | Session transcript: commits at messages 18, 35, 52 all used "update" | git-create-commit-skill exists but doesn't enforce verb classification |
| 2 | Branches remain after merge | git-finishing-a-development-branch-skill — no branch cleanup step | Skill handles merge options but not post-merge cleanup |

## Phase 5: Delta Architecture
Read ARCHITECTURE-PRINCIPLES.md to ground architecture decisions in project principles.

**Deterministic offloading classification:**
- F-1 (commit message verbs): **Semantic** — classifying change type requires understanding the diff content. This is LLM judgment work → CLAUDE.md rule is appropriate.
- F-2 (branch cleanup): **Mechanical** — branch deletion after merge is deterministic (check merge status, delete if merged). Could be a script, but the worktree skill already orchestrates this workflow → skill modification is appropriate.

Fix path priority applied:

### Delta 1: Commit message verb classification
**Priority 3 — CLAUDE.md rule**
- This is semantic work: the LLM must read the diff and classify the change type. A hook cannot do this.
- Add explicit verb classification rule with wrong/right examples.
- Grounded in ARCHITECTURE-PRINCIPLES.md: tools handle mechanical work, LLMs handle semantic judgment.

### Delta 2: Worktree branch cleanup
**Priority 2 — Script/tool (within skill)**
- Add cleanup phase to git-finishing-a-development-branch-skill
- The cleanup steps (delete branch, remove worktree) are deterministic after merge verification
- 15+ line change → plan-template format

### Coverage verification:
- Delta 1: CLAUDE.md rule (semantic, correctly classified)
- Delta 2: Skill modification with deterministic cleanup steps

### Open items:
- [H] Explicit verb classification will eliminate generic "update" messages
- [Q] Should branch cleanup be automatic or prompt-gated?

**HARD GATE**: Presenting Delta architecture to user. Waiting for user to lock architecture before proceeding.

---

## Phase 6: DIFF Expression

### DIFF-1: CLAUDE.md commit message verb rule
**Covers: BID row 1** (small diff — 7 lines, inline)

```diff
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ after existing commit rules
+**Commit Message Verb Classification:**
+- Never use generic "update" as a commit verb
+- Classify changes: `add` (new feature), `fix` (bug), `refactor` (restructure),
+  `docs` (documentation), `test` (tests), `chore` (maintenance)
+- The verb must match the actual nature of the change
+- Wrong: "update user authentication" → Right: "add JWT-based authentication"
+- Wrong: "update broken login" → Right: "fix broken login redirect"
```

### DIFF-2: git-finishing-a-development-branch-skill cleanup phase
**Covers: BID row 2** (large diff — 20+ lines, plan-template format)

---

# Plan: worktree-branch-cleanup

## Context

The git-finishing-a-development-branch-skill handles merge options but leaves branches behind after merge. This adds a deterministic cleanup phase.

Whiteboard: N/A — friction-driven improvement

---

## Baseline Tracing Guide (for dev agent)

### Folder map
```
.claude/
  skills/
    git-finishing-a-development-branch-skill/
      SKILL.md     ← MODIFIED — add cleanup phase
```

### Key files to read (in order)
1. `.claude/skills/git-finishing-a-development-branch-skill/SKILL.md` — current skill content

---

## File Changes

### ADDED

**(none)**

### MODIFIED

**`.claude/skills/git-finishing-a-development-branch-skill/SKILL.md`**
```markdown
## Post-Merge Cleanup (new section after existing merge options)

After successful merge, offer cleanup options:

1. **Full cleanup** (recommended):
   - Delete local branch: `git branch -d <branch-name>`
   - Delete remote branch: `git push origin --delete <branch-name>`
   - Remove worktree directory: `git worktree remove <worktree-path>`

2. **Local only**:
   - Delete local branch and worktree, keep remote

3. **Skip cleanup**:
   - Leave everything in place (user handles manually)

Present options to user. Default to full cleanup.
Verify merge was successful before any deletion.
Never force-delete (`-D`) — use `-d` which refuses if unmerged.
```

### REMOVED
**(none)**

### UNTOUCHED
- All other skills and commands

---

## Verification

```bash
# Manual verification: create worktree, merge, run cleanup
git worktree add ../test-cleanup -b test-cleanup-branch
# ... make changes, merge ...
# Verify branch and worktree are cleaned up
git branch | grep test-cleanup  # should not appear
git worktree list | grep test-cleanup  # should not appear
```

---

**HARD GATE**: Waiting for user to approve DIFFs before any edit takes effect.

---

## Phase 7: Apply
(Awaiting user approval of DIFFs above)
