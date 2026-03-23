# Learnings

### 1. Use LSP-first for static analysis tracing (2026-03-23 09:05)

- [OBS: Agent used Read/Grep 10x at L57-L98 to trace electron imports instead of LSP] [^L1a]
- [OBS: User corrected at L115 (rejected edit without analysis), L143 ("proceed with LSP trace"), L229 ("why are you reading vs using LSP?")] [^L1b][^L1c][^L1d]
- [F-ID: LSP `findReferences` gives definitive usage sites; `incomingCalls` traces callers; `workspaceSymbol` indexes full project — faster and more reliable than Grep/Read for TS/JS]
- [D: For TypeScript import chain analysis, always start with LSP. The `~/.claude/CLAUDE.md:L58-L67` TYPESCRIPT/JAVASCRIPT SYMBOL SEARCH RULE already mandates this.]
- **domain:** trace imports, find usages, where is X defined, dependency chain, refactor, debug, investigate, fix error, understand code, electron
- **anti-domain:** create new file from scratch, git commit, vault sync, markdown editing, interview prep
- **reasoning:** Triggers whenever the agent will need to search/trace TS/JS code. Broad because almost any code task starts with search. Anti-domains are tasks with zero code search.

[^L1a]: `/Users/wesleyfrederick/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools/355bd796-a554-400b-a35e-b4456c1e95d7.jsonl:L57,L61,L65,L70,L74,L86,L90,L94,L98` (agent Read/Grep tool calls on electron dependency files)
[^L1b]: `/Users/wesleyfrederick/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools/355bd796-a554-400b-a35e-b4456c1e95d7.jsonl:L115` (user: "try again" — rejected edit attempt without analysis)
[^L1c]: `/Users/wesleyfrederick/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools/355bd796-a554-400b-a35e-b4456c1e95d7.jsonl:L143` (user: "no. proceed with LSP trace to understand all impacted code")
[^L1d]: `/Users/wesleyfrederick/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools/355bd796-a554-400b-a35e-b4456c1e95d7.jsonl:L229` (user: "why are you reading vs using LSP?")

### 2. Learnings entries require real datetime and source paths with line numbers (2026-03-23 09:05)

- [OBS: Agent fabricated timestamp "16:00" instead of using `date` command to get actual time] [^L2a]
- [OBS: Agent used vague source ref "User corrections across 3 turns" instead of file:line citation] [^L2a]
- [D: Always use `date '+%Y-%m-%d %H:%M'` via Bash for timestamps. Always include exact file path and line number in `[^REF]` footnotes.] [^L2a]
- **domain:** LEARNINGS.md, capture learning, #USER-FRICTION, write learning, evidence tag
- **anti-domain:** code editing, testing, debugging, git, build, deploy, UI
- **reasoning:** Only relevant when writing to LEARNINGS.md itself. Narrow domain prevents injection noise on unrelated tasks.

[^L2a]: `/Users/wesleyfrederick/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools/355bd796-a554-400b-a35e-b4456c1e95d7.jsonl:L269` (user: "#USER-FRICTION: we always include the source path and exact line number. Use bash to get actual datetime")

### 3. Transcript path is available in hook input JSON (2026-03-23 09:08)

- [OBS: Agent used `search-transcripts.py` to locate the session file instead of reading `transcript_path` from hook input] [^L3a]
- [OBS: Hook input JSON contains `session_id` and `transcript_path` fields per Claude Code hooks spec] [^L3b]
- [D: When referencing the current session transcript in learnings, use the `transcript_path` from hook input rather than searching.] [^L3a]
- **domain:** transcript, session file, search-transcripts, hook input, session_id, JSONL
- **anti-domain:** code editing, testing, UI, git, build, deploy
- **reasoning:** Only relevant when the agent needs to reference the current session transcript. Prevents injection when user is doing normal dev work.

[^L3a]: `/Users/wesleyfrederick/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools/355bd796-a554-400b-a35e-b4456c1e95d7.jsonl:L293` (user: "#USER-FRICTION: The source of these learnings will be the session transcript")

[^L3b]: Claude Code hooks spec — `session_id` and `transcript_path` are common fields in all hook input JSON (verified via claude-code-guide agent)

### 4. Every evidence tag must link to a source footnote (2026-03-23 09:12)

- [OBS: Agent wrote [OBS] tags without per-tag `[^ref]` links — user corrected "each tag needs a link to a source"] [^L4a]
- [D: Every `[OBS]`, `[F-ID]`, `[D]`, etc. tag in LEARNINGS.md must have a `[^LNx]` footnote linking to the specific transcript line(s) that evidence it.] [^L4a]
- **domain:** LEARNINGS.md, evidence tag, footnote, [OBS], [H], [A], [F-ID], [D], write learning
- **anti-domain:** code editing, testing, debugging, git, build, deploy, UI
- **reasoning:** Only relevant when writing evidence-tagged content to LEARNINGS.md. Shares anti-domain with L2 since both are LEARNINGS.md authoring rules.

[^L4a]: `/Users/wesleyfrederick/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools/355bd796-a554-400b-a35e-b4456c1e95d7.jsonl:L401` (user: "each tag needs a link to a source")
