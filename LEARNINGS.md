# Learnings

### 1. Use LSP-first for static analysis tracing (2026-03-23 09:05)

- [OBS: Agent used Read/Grep 10x at L57-L98 to trace electron imports instead of LSP][^L1a]
- [OBS: User corrected at L115 (rejected edit without analysis), L143 ("proceed with LSP trace"), L229 ("why are you reading vs using LSP?")][^L1b][^L1c][^L1d]
- [F-ID: LSP `findReferences` gives definitive usage sites; `incomingCalls` traces callers; `workspaceSymbol` indexes full project — faster and more reliable than Grep/Read for TS/JS]
- [D: For TypeScript import chain analysis, always start with LSP. The `~/.claude/CLAUDE.md:L58-L67` TYPESCRIPT/JAVASCRIPT SYMBOL SEARCH RULE already mandates this.]

[^L1a]: `/Users/wesleyfrederick/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools/355bd796-a554-400b-a35e-b4456c1e95d7.jsonl:L57,L61,L65,L70,L74,L86,L90,L94,L98` (agent Read/Grep tool calls on electron dependency files)
[^L1b]: `/Users/wesleyfrederick/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools/355bd796-a554-400b-a35e-b4456c1e95d7.jsonl:L115` (user: "try again" — rejected edit attempt without analysis)
[^L1c]: `/Users/wesleyfrederick/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools/355bd796-a554-400b-a35e-b4456c1e95d7.jsonl:L143` (user: "no. proceed with LSP trace to understand all impacted code")
[^L1d]: `/Users/wesleyfrederick/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools/355bd796-a554-400b-a35e-b4456c1e95d7.jsonl:L229` (user: "why are you reading vs using LSP?")

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
