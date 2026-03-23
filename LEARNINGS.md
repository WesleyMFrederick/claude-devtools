# Learnings

### 1. Use LSP-first for static analysis tracing (2026-03-23 09:05)

- [OBS: Agent defaulted to Read/Grep for tracing import chains and electron dependency impact instead of using LSP `findReferences`, `incomingCalls`, `workspaceSymbol`]
- [OBS: User corrected 3x: (1) rejected initial edit attempt without analysis, (2) requested "LSP trace to understand all impacted code", (3) asked "why are you reading vs using LSP?"]
- [F-ID: LSP `findReferences` on a symbol gives definitive usage sites without manual file reading; `incomingCalls` traces callers; `workspaceSymbol` indexes the full project — all faster and more reliable than Grep/Read for TS/JS codebases]
- [D: For TypeScript import chain analysis, always start with LSP operations before falling back to Grep/Read. The CLAUDE.md TYPESCRIPT/JAVASCRIPT SYMBOL SEARCH RULE already mandates this — agent failed to follow it.]

[^L1-REF]: `~/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools/355bd796-a554-400b-a35e-b4456c1e95d7.jsonl:L143` (user: "no. proceed with LSP trace to understand all impacted code"), `:L229` (user: "why are you reading vs using LSP?")

### 2. Learnings entries require real datetime and source paths with line numbers (2026-03-23 09:05)

- [OBS: Agent fabricated timestamp "16:00" instead of using `date` command to get actual time]
- [OBS: Agent used vague source ref "User corrections across 3 turns" instead of file:line citation]
- [D: Always use `date '+%Y-%m-%d %H:%M'` via Bash for timestamps. Always include exact file path and line number in `[^REF]` footnotes.]

[^L2-REF]: `~/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools/355bd796-a554-400b-a35e-b4456c1e95d7.jsonl:L269` (user: "#USER-FRICTION: we always include the source path and exact line number. Use bash to get actual datetime")

### 3. Transcript path is available in hook input JSON (2026-03-23 09:08)

- [OBS: Agent used `search-transcripts.py` to locate the session file instead of reading `transcript_path` from hook input]
- [OBS: Hook input JSON contains `session_id` and `transcript_path` fields per Claude Code hooks spec. The existing `user-prompt-submit.sh` already parses `hook_input.get("prompt")` but ignores `session_id` and `transcript_path`]
- [D: When referencing the current session transcript in learnings, use the `transcript_path` from hook input rather than searching. The agent has access to this via env/hook context.]

[^L3-REF]: `~/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools/355bd796-a554-400b-a35e-b4456c1e95d7.jsonl` (user: "#USER-FRICTION: you have access to the session transcript path via hooks")
