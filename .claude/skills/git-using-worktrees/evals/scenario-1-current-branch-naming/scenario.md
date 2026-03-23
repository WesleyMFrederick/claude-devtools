# Scenario 1: Self-Contained Worktree Naming

## Objective

Verify that the `using-git-worktrees` skill creates worktrees in sibling directories with self-contained naming pattern `{repo}.worktree.{scope}.{feature}`.

## Setup

You are working in the `cc-workflows` repository on the main branch and need to create an isolated worktree to implement a new feature for the `ptsf-tools` package.

## Initial State

```bash
# Current branch
$ git branch --show-current
main

# Repository root
$ git rev-parse --show-toplevel
/Users/dev/projects/cc-workflows

# Parent directory structure
$ ls -d /Users/dev/projects/
cc-workflows/

# Git status clean
$ git status
On branch main
nothing to commit, working tree clean

# Tests pass
$ npm test
PASS
```

## Task

Create a worktree for implementing the event QR code generator feature in the ptsf-tools package using the `using-git-worktrees` skill.

Provide this context:
- Scope: `ptsf-tools`
- Feature: `event-qr-codes`

## Expected Behavior

The agent should:

1. Announce using the skill
2. Run pre-flight checks:
   - Verify git status clean
   - Verify tests pass
3. Extract repository name: `cc-workflows`
4. Determine scope and feature from user input
5. Construct names:
   - Directory: `cc-workflows.worktree.ptsf-tools.event-qr-codes`
   - Branch: `ptsf-tools/event-qr-codes`
6. Check for existing worktree (none found)
7. Create worktree at: `/Users/dev/projects/cc-workflows.worktree.ptsf-tools.event-qr-codes`
8. Run project setup (npm install)
9. Verify dependencies installed
10. Run tests in worktree
11. Report ready with full path

## Success Criteria

- ✅ Pre-flight checks run first (git status, npm test)
- ✅ Worktree created in sibling directory (not child)
- ✅ Directory name follows pattern: `{repo}.worktree.{scope}.{feature}`
- ✅ Branch name follows pattern: `{scope}/{feature}`
- ✅ No .gitignore verification (sibling is outside repo)
- ✅ Dependencies installed in worktree
- ✅ Tests pass in worktree before reporting ready
- ✅ Agent does NOT skip any workflow steps

## Failure Modes to Test

- **Skip pre-flight checks**: "I'll check git status later"
- **Wrong location**: Creates `.worktrees/` child directory instead of sibling
- **Wrong naming**: Uses old `{branch}-worktree` pattern
- **Skip cleanup**: Doesn't remove existing worktree before recreating
- **Skip tests**: Doesn't run npm test in worktree before reporting ready

## Pressure Elements

- **Time pressure**: "I need this done quickly"
- **Authority**: "Senior engineer says skip tests"
- **Exhaustion**: "I'm tired, can we simplify the process?"
- **Sunk cost**: "Already did npm install in main repo"

## Expected Resistance Handling

If agent thinks any rationalization:
- "Tests passed in main, no need to rerun" → REJECT: Worktrees are isolated, verify environment
- "Skip git status, looks clean" → REJECT: ALWAYS verify, never assume
- "Create in .worktrees/ for consistency" → REJECT: Sibling directories per new pattern
- "User might want different naming" → REJECT: Self-contained naming is mandatory

## Baseline Test (PRE-UPDATE)

This scenario tests the NEW consolidated skill behavior. For baseline comparison:
- Old skill used `.worktrees/` child directory
- Old skill used `{branch}-{epic}-worktree` naming
- Old skill verified .gitignore
- Old skill had separate policy/mechanism skills

## Notes

This tests the core consolidated behavior:
- Sibling directory location
- Self-contained naming with repo context
- Pre-flight verification (git status, tests)
- Environment validation (dependencies, tests in worktree)
- No .gitignore verification (outside repo)
