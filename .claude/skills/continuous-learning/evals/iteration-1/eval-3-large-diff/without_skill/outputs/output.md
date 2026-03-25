# Session Friction Analysis: Commit Messages + Worktree Cleanup

## Issues Found

### 1. Generic Commit Messages
Claude used "update" for every commit message regardless of whether the change was a new feature, bug fix, or refactoring. This makes git history unhelpful.

**Fix:** Add a rule to CLAUDE.md requiring specific verbs: add, fix, refactor, docs, test, chore. Include wrong/right examples.

```diff
+ ## Commit Message Rules
+ - Never use generic "update" as commit verb
+ - Use: add (new), fix (bug), refactor, docs, test, chore
+ - Example: "update auth" → "add JWT authentication"
```

### 2. Worktree Branch Accumulation
After merging a worktree branch, the branch and worktree directory remain. User has to manually clean up.

**Fix:** Update the git-finishing skill to include a cleanup step after merge:
- Delete local branch
- Delete remote branch
- Remove worktree directory

This could be a post-merge option in the finishing skill.

## Proposed Changes

1. Add commit verb classification rule to CLAUDE.md (small, immediate)
2. Update git-finishing skill with cleanup phase (larger change, needs testing)

## Priority
- Commit messages: **High** (affects every commit)
- Worktree cleanup: **Medium** (affects worktree-based workflows only)
