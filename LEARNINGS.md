# Learnings

### 1. Use LSP-first for static analysis tracing (2026-03-23 09:05)

- [OBS: Agent defaulted to Read/Grep for tracing import chains and electron dependency impact instead of using LSP `findReferences`, `incomingCalls`, `workspaceSymbol`]
- [OBS: User corrected 3x: (1) rejected initial edit attempt without analysis, (2) requested "LSP trace to understand all impacted code", (3) asked "why are you reading vs using LSP?"]
- [F-ID: LSP `findReferences` on a symbol gives definitive usage sites without manual file reading; `incomingCalls` traces callers; `workspaceSymbol` indexes the full project — all faster and more reliable than Grep/Read for TS/JS codebases]
- [D: For TypeScript import chain analysis, always start with LSP operations before falling back to Grep/Read. The CLAUDE.md TYPESCRIPT/JAVASCRIPT SYMBOL SEARCH RULE already mandates this — agent failed to follow it.]

[^L1-REF]: `~/.claude/CLAUDE.md:L58-L67` (user: "why are you reading vs using LSP?", "proceed with LSP trace to understand all impacted code")

### 2. Learnings entries require real datetime and source paths with line numbers (2026-03-23 09:05)

- [OBS: Agent fabricated timestamp "16:00" instead of using `date` command to get actual time]
- [OBS: Agent used vague source ref "User corrections across 3 turns" instead of file:line citation]
- [D: Always use `date '+%Y-%m-%d %H:%M'` via Bash for timestamps. Always include exact file path and line number in `[^REF]` footnotes.]

[^L2-REF]: `LEARNINGS.md:L3` (user: "we always include the source path and exact line number. Use bash to get actual datetime")
