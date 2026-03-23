# Learnings

### 1. Use LSP-first for static analysis tracing (2026-03-23 16:00)

- [OBS: Agent defaulted to Read/Grep for tracing import chains and electron dependency impact instead of using LSP `findReferences`, `incomingCalls`, `workspaceSymbol`]
- [OBS: User corrected 3x: (1) rejected initial edit attempt without analysis, (2) requested "LSP trace to understand all impacted code", (3) asked "why are you reading vs using LSP?"]
- [F-ID: LSP `findReferences` on a symbol gives definitive usage sites without manual file reading; `incomingCalls` traces callers; `workspaceSymbol` indexes the full project — all faster and more reliable than Grep/Read for TS/JS codebases]
- [D: For TypeScript import chain analysis, always start with LSP operations before falling back to Grep/Read. The CLAUDE.md TYPESCRIPT/JAVASCRIPT SYMBOL SEARCH RULE already mandates this — agent failed to follow it.]

[^L1-REF]: User corrections across 3 turns in session. Rule already exists in `~/.claude/CLAUDE.md` under "TYPESCRIPT / JAVASCRIPT SYMBOL SEARCH RULE".
