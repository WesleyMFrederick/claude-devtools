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
- **reasoning:** Only relevant when writing evidence-tagged content to LEARNINGS.md. Shares anti-domain with [L2](#2.%20Learnings%20entries%20require%20real%20datetime%20and%20source%20paths%20with%20line%20numbers%20(2026-03-23%2009%2005))  since both are LEARNINGS.md authoring rules.

[^L4a]: `/Users/wesleyfrederick/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools/355bd796-a554-400b-a35e-b4456c1e95d7.jsonl:L401` (user: "each tag needs a link to a source")

### 5. Show falsification steps when presenting [H] in chat (2026-03-23 09:50)

- [OBS: Agent presented hypothesis "dynamic require will work" in chat without showing specific steps to falsify it — user flagged #USER-FRICTION via `/evidence-ontology why do you think this will work`] [^L5a]
- [F-ID: EVIDENCE-ONTOLOGY.md L67 says "negate-first is mandatory for hypotheses" but only addresses the resolve step in file artifacts. The chat presentation of [H] also needs the falsification plan visible so the user can steer before the agent runs off testing the wrong thing.] [^L5b]
- [F-ID: Per Learning #4, chat uses the evidence ontology thinking process. Falsification steps are part of that process — they show the agent's testing plan, not just the claim.] [^L5c]
- [D: When presenting an [H] in chat, always include the specific falsification steps. Format:] [^L5a]
  ```
  Testing [H]: (description)
  - Utility: L/M/H — what decision this unlocks
  - Cost: L/M/H — effort to test
  - (first falsification step — what would disprove it)
  - (second step)
  - Expected result if hypothesis holds / fails
  ```
  This lets the user approve or redirect the testing plan before execution.
- **domain:** chat output, hypothesis, [H], evidence ontology, testing plan, falsification, negate-first
- **anti-domain:** file artifacts (already covered by ontology), code editing, git, build, deploy
- **reasoning:** Triggers whenever the agent presents an uncertain claim in chat that it plans to act on. Prevents wasted cycles on wrong testing approach.

[^L5a]: `/Users/wesleyfrederick/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools/355bd796-a554-400b-a35e-b4456c1e95d7.jsonl` (user: "/evidence-ontology why do you think this will work" — flagged missing falsification steps)

[^L5b]: `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools/.claude/skills/evidence-ontology/references/EVIDENCE-ONTOLOGY.md:L67` ("Strengthen must be negate-first")

[^L5c]: LEARNINGS.md L42-50 (Learning #4 — evidence ontology thinking process applies in chat)

### 6. All assertions require evidence grounding — no bare claims (2026-03-23 10:11)

- [OBS: Agent presented "option 1 is the simplest fix" and "that's the smallest change" as bare assertions without evidence tags or falsification — user flagged #USER-FRICTION: "I don't trust your assertions unless you present them with evidence, tags, and as a hypothesis that you're going to falsify"] [^L6a]
- [F-ID: Per Learning #5, [H] in chat needs falsification steps. But this is broader — even non-hypothesis claims ("simplest fix", "smallest change") need grounding. A claim about relative simplicity is itself a hypothesis unless backed by measurement.] [^L6b]
- [D: Every actionable claim in chat must be grounded. Three levels:] [^L6a]
  1. **Verified fact** — cite the observation: "line 388 uses `new Notification()` (read from file)"
  2. **Derivation** — show the logic chain: "only 1 of 17 files imports a value, so blast radius is 1 file"
  3. **Hypothesis** — present with falsification plan per Learning #5
  Never present bare "I think X" or "X is simpler" without one of these.
- **domain:** chat output, assertions, evidence, claims, recommendations, options, tradeoffs
- **anti-domain:** file artifacts (already tagged), git commit messages, LEARNINGS.md authoring mechanics
- **reasoning:** Broadest chat-output rule. Triggers on any recommendation or option presentation. Prevents the pattern of sounding confident without showing work.

[^L6a]: current session (user: "#USER-FRICTION: I don't trust your assertions unless you present them with evidence, tags, and as a hypothesis that you're going to falsify")

[^L6b]: LEARNINGS.md L52-75 (Learning #5 — falsification steps for [H] in chat)
