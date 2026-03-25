# Session Friction Analysis: bun vs npm Corrections

## Issue Summary
During this session, I used `npm` commands three times when the project uses `bun`. The user had to correct me each time.

## Observations
1. First correction: I ran `npm install` when the user asked to add a dependency. User said "use bun not npm."
2. Second correction: I used `npx` to run a CLI tool. User corrected to `bunx`.
3. Third correction: I ran `npm run test` instead of `bun run test`. User was visibly frustrated.

## Root Cause
The CLAUDE.md file already specifies "This project uses **bun**" but this instruction was overridden by default npm training patterns.

## Proposed Improvements

### 1. Strengthen CLAUDE.md wording
Add explicit "NEVER use npm" language with wrong/right examples.

```diff
- This project uses **bun** (not npm/npx). Always use `bun` for:
+ This project uses **bun** (not npm/npx). ALWAYS use `bun` for:
  - Running scripts: `bun run <script>`
  - Installing packages: `bun add <package>`
+ - NEVER use npm, npx, or yarn
```

### 2. Add a memory file
Create a feedback memory reinforcing the bun preference so it persists across sessions.

### 3. Consider a pre-command hook
A hook could intercept npm/npx commands before they execute, providing a hard technical gate.

### 4. Add to global CLAUDE.md
If this is a pattern across projects, add a global reminder to check for bun.lockb before defaulting to npm.

## Priority
High — this caused friction 3 times in a single session and the fix is straightforward.
