# trace-deps — Whiteboard

> **Change:** Deterministic Dependency Tracer
> **Domain:** claude-devtools / agent tooling
> **Date:** 2026-03-23

<!-- TEMPLATE RULE: After populating all buckets, wrap any section that has
     NO tagged items (only the placeholder comment remains) in HTML comment
     delimiters so it is hidden from the human reader. Keep the heading inside
     the comment so the section can be restored later.

     Example — empty section hidden:
     <!--
     ### Baseline Evidence
     [E] tags: observation + source + link that updates a hypothesis
     - ->

     Example — populated section (visible, comment removed):
     ### Baseline Evidence
     1. [E-001: CPU spike confirms bottleneck] [^S-005] ...
-->

## Bootstrap Instructions

To resume this whiteboard in a new session:

1. **Load skills:**
   - `/evidence-ontology` — canonical tag definitions ([OBS], [H], [F-ID], etc.)
   - `/continuous-learning` — [O] outcome format and BID table structure
   - `/writing-for-token-optimized-and-ceo-scannable-content` — scannability patterns, callout syntax

2. **Load conversation context** via `/searching-transcripts`:
   ```
   /searching-transcripts --dir ~/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools --file 1476793d-a02f-4a92-817e-2f314b16817c.jsonl
   ```
   Key search terms: `"trace-deps"`, `"deterministic"`, `"BI table"`, `"#USER-FRICTION"`

3. **Read this whiteboard file** — it is the self-contained state file. All decisions, findings, and BI table are inline below.

4. **Read key reference files:**
   - `ARCHITECTURE-PRINCIPLES.md` L102-109 — Deterministic Offloading Principles
   - `docs/traces/20260323-sidebar-filter-baseline.md` — the trace this tool replaces
   - `docs/traces/20260323-sidebar-trace-methodology.md` — 15-step methodology being automated
   - `docs/traces/20260323-deterministic-trace-analysis.md` — deterministic vs. semantic classification
   - `docs/traces/templates/whiteboard.md` — whiteboard template (source format)
   - `docs/traces/templates/whiteboard-instruction.md` — whiteboard population rules

5. **Resume at current state:** CL phases b, b.1, c, d complete. Hard gate [e2] (BI table lock) pending.

## Original Request

[OBS-001: session transcript] [^S-001] User requested a deterministic dependency tracer after observing 73% of codebase trace tool calls are mechanical ^OBS-001

```
When tracing a codebase feature path (e.g., "how does sidebar filtering work?"),
the agent makes ~33 LLM tool calls (LSP, Read, Grep, Glob). 73% are fully
deterministic. LSP fails 30% of the time on barrel re-exports. Build a tool
that replaces the deterministic portion with a single CLI invocation.
```

[G-001: 33 tool calls to 1 tool call plus LLM synthesis] [^S-001] Replace deterministic trace operations with a single `trace-deps` CLI invocation, reducing latency from ~60s to <5s and failure rate from 30% to 0% ^G-001

---

## Artifacts Investigated

| Artifact | Path | Role |
|----------|------|------|
| Session transcript | `~/.claude/projects/-Users-wesleyfrederick-...-claude-devtools/1476793d-a02f-4a92-817e-2f314b16817c.jsonl` | Primary evidence for friction patterns |
| Sidebar filter trace | [20260323-sidebar-filter-baseline.md](../traces/20260323-sidebar-filter-baseline.md) | Output showing 33-call methodology |
| Methodology trace | [20260323-sidebar-trace-methodology.md](../traces/20260323-sidebar-trace-methodology.md) | Meta-trace classifying each call |
| Deterministic analysis | [20260323-deterministic-trace-analysis.md](../traces/20260323-deterministic-trace-analysis.md) | Classification scorecard + architecture |
| Architecture Principles | [ARCHITECTURE-PRINCIPLES.md](../../../ARCHITECTURE-PRINCIPLES.md):102-109 | Deterministic Offloading Principles |
| CLAUDE.md (global) | `~/.claude/CLAUDE.md` | Contains LSP-first rule (L58-67) |
| Learnings #1, #8, #9 | Session context | Prior corrections driving trace methodology |
| Continuous Learning skill | `.claude/skills/continuous-learning/SKILL.md` | CL workflow and BI table rules |
| Evidence Ontology skill | `.claude/skills/evidence-ontology/SKILL.md` | Loads ontology tags into context |
| Evidence Ontology reference | `.claude/skills/evidence-ontology/references/EVIDENCE-ONTOLOGY.md` | Canonical tag definitions |
| Whiteboard template | [whiteboard.md](../traces/templates/whiteboard.md) | Source template for this artifact |
| Whiteboard instruction | [whiteboard-instruction.md](../traces/templates/whiteboard-instruction.md) | Population rules |
| Formatting reference | `.claude/skills/writing-for-token-optimized-and-ceo-scannable-content/formatting-reference.md` | Scannability patterns, callout syntax |
| Source plan file | `~/.claude/plans/cozy-weaving-dragon.md` | Original plan being pivoted |

---

## Findings

| ID | Pattern Found | Scope | Trigger | Friction Caused |
|----|--------------|-------|---------|-----------------|
| F1 | Agent makes 33 LLM tool calls for a task that is 73% deterministic | Codebase tracing | Any "trace how X works" request | ~60s latency, ~15K context tokens on mechanical I/O, 30% LSP failure on barrel re-exports |
| F2 | LSP goToDefinition fails on barrel re-exports, requiring 5 extra Grep/Read fallback calls | TS symbol resolution | Import chain through barrel files | 15% of all tool calls were recovery from this single failure mode |
| F3 | Agent chooses which files to read (semantic), but traversal itself is mechanical BFS | Trace methodology | Entry file identified → need dependency graph | LLM context spent on "what next" decisions a graph walker handles deterministically |
| F4 | Agent guessed wrong path for Sidebar.tsx, requiring recovery | File discovery | Component not at expected directory | Wasted tool call + recovery; ts-morph project index finds it instantly |
| F5 | Output trace requires LLM to synthesize 2,400 lines into structured narrative | Trace writing | All source read → need coherent document | CORRECT use of LLM — validates synthesis stays with LLM (untargeted row) |

---

## Baseline Bucket

### Baseline Outcomes

1. [O-001: Agent can trace a codebase feature path by making ~33 LLM tool calls across LSP, Read, Grep, and Glob] [^S-002] ^O-001
2. [O-002: Agent can resolve TypeScript import chains by falling back to Grep when LSP fails on barrel re-exports] [^S-003] ^O-002
3. [O-003: Agent can discover which files to read by making sequential judgment calls about directory structure] [^S-003] ^O-003
4. [O-004: Agent can build structured trace documents from raw source code] [^S-003] ^O-004
5. [O-005: Agent can identify store connections, JSX renders, and API calls by reading source and applying judgment] [^S-003] ^O-005

### Baseline Metrics

1. [M-001: 33 total tool calls per trace] [^S-003] Steps counted in methodology trace ^M-001
2. [M-002: 30% LSP failure rate on re-exported types] [^S-003] 4 of 13 LSP calls failed ^M-002
3. [M-003: ~60s latency for full trace] [^S-004] Sequential LSP + reads ^M-003
4. [M-004: ~15K context tokens consumed by mechanical I/O] [^S-004] Tool results from 33 calls ^M-004
5. [M-005: ~2,400 source lines read] [^S-003] Across 13 unique files ^M-005

### Baseline Observations

1. [OBS-002: 73% of tool calls fully deterministic] [^S-004] Steps 4, 6-13 in methodology trace ^OBS-002
2. [OBS-003: LSP goToDefinition fails on barrel re-exports] [^S-003] DateCategory, SessionSortMode — 3 layers of `export * from` ^OBS-003
3. [OBS-004: Session interface required 5 tool calls across 3 directories to resolve] [^S-003] shared/types → main/types → domain.ts ^OBS-004

### Baseline Facts — Identity

1. [F-ID-001: All sidebar filtering is client-side via useMemo chain] [^S-002] No server-side filtering in paginated API ^F-ID-001
2. [F-ID-002: ts-morph uses actual TypeScript module resolution, not LSP heuristics] [^S-004] Resolves re-exports natively ^F-ID-002

### Baseline Facts — Locked

1. [F-LK-001: Filtering pipeline is 5 useMemo calls in DateGroupedSessions.tsx L108-138] [^S-002] hiddenSet → visibleSessions → pinned/unpinned → grouped → nonEmpty ^F-LK-001

<!--
### Baseline Evidence
[E] tags: observation + source + link that updates a hypothesis
-->

<!--
### Baseline Goals
[G] tags: directional intent explaining why outcomes matter
-->

### Baseline Constraints

1. [C-001: Mechanical Separation principle] [^S-005] Route deterministic tasks to tools, reserve LLMs for semantic work ^C-001
2. [C-002: Focused Context principle] [^S-005] Fill LLM context with high-value semantic info, not mechanical I/O ^C-002
3. [C-003: Tool-First Design principle] [^S-005] Build specialized tools for repetitive operations ^C-003
4. [C-004: No Surprises principle] [^S-005] Identical inputs must yield consistent deterministic results ^C-004

<!--
### Baseline Hypotheses
[H] tags: mutable claims requiring validation
-->

<!--
### Baseline Assumptions
[A] tags: provisional claims with risk-if-wrong
-->

<!--
### Baseline Questions
[Q] tags: labeled uncertainties organizing exploration
-->

<!--
### Baseline Priorities
[P] tags: relative importance ordering
-->

<!--
### Baseline Decisions
[D] tags: explicit resource commitments with supporting evidence
-->

---

## Ideal Bucket

### Ideal Outcomes

1. [O-006: Agent can trace a codebase feature path with a single deterministic tool call plus LLM synthesis] [^S-004] ^O-006
2. [O-007: Agent can resolve TypeScript import chains with zero failures regardless of barrel re-export depth] [^S-004] ^O-007
3. [O-008: Agent can discover all files in a dependency graph without guessing directory structure] [^S-004] ^O-008
4. [O-009: Agent can build structured trace documents from raw source code] [^S-004] Untargeted — carries through from baseline ^O-009
5. [O-010: Agent can identify store connections, JSX renders, and API calls from a pre-computed structured graph] [^S-004] ^O-010

### Ideal Metrics

1. [M-006: 1 tool call (deterministic) + ~3 LLM calls (synthesis)] [^S-004] Down from 33 ^M-006
2. [M-007: 0% failure rate on import resolution] [^S-004] ts-morph handles natively ^M-007
3. [M-008: <5s total latency (tool: 2s, LLM synthesis: 3s)] [^S-004] Down from ~60s ^M-008
4. [M-009: ~3K context tokens for structured JSON output] [^S-004] Down from ~15K ^M-009

<!--
### Ideal Observations
[OBS] tags: exact pointers to source reads or command results
-->

<!--
### Ideal Facts — Identity
[F-ID] tags: truths by definition, math, or structural logic (P=1.0)
-->

<!--
### Ideal Facts — Locked
[F-LK] tags: high-confidence empirical reality frozen for this cycle
-->

<!--
### Ideal Evidence
[E] tags: observation + source + link that updates a hypothesis
-->

<!--
### Ideal Goals
[G] tags: directional intent explaining why outcomes matter
-->

<!--
### Ideal Constraints
[C] tags: non-negotiable boundary conditions
-->

<!--
### Ideal Hypotheses
[H] tags: mutable claims requiring validation
-->

<!--
### Ideal Assumptions
[A] tags: provisional claims with risk-if-wrong
-->

<!--
### Ideal Questions
[Q] tags: labeled uncertainties organizing exploration
-->

<!--
### Ideal Priorities
[P] tags: relative importance ordering
-->

<!--
### Ideal Decisions
[D] tags: explicit resource commitments with supporting evidence
-->

---

## Delta Bucket

### Delta Outcomes

1. [O-011: trace-deps CLI produces structured dependency graph JSON from a single entry file] [^S-004] Bridges O-001→O-006, O-003→O-008 ^O-011
2. [O-012: ts-morph resolves barrel re-export chains natively without LSP] [^S-004] Bridges O-002→O-007 ^O-012
3. [O-013: Structured JSON output includes store connections, JSX renders, and API calls] [^S-004] Bridges O-005→O-010 ^O-013

<!--
### Delta Metrics
[M] tags: measured change values
-->

<!--
### Delta Observations
[OBS] tags: exact pointers to source reads or command results
-->

<!--
### Delta Facts — Identity
[F-ID] tags: truths by definition, math, or structural logic (P=1.0)
-->

<!--
### Delta Facts — Locked
[F-LK] tags: high-confidence empirical reality frozen for this cycle
-->

<!--
### Delta Evidence
[E] tags: observation + source + link that updates a hypothesis
-->

<!--
### Delta Goals
[G] tags: directional intent explaining why outcomes matter
-->

<!--
### Delta Constraints
[C] tags: non-negotiable boundary conditions
-->

### Delta Hypotheses

1. [H-001: ts-morph can detect useStore() field access patterns via AST walking] [^S-004] ^H-001
   - Strengthen: Find a Zustand store pattern that ts-morph CallExpression walking cannot parse (negate-first)
   - Utility: H — determines if store connection detection is viable without LSP
   - Cost: L — write a test case with actual codebase pattern
   - Next actions: 1. Read DateGroupedSessions.tsx useStore call 2. Write ts-morph extraction POC 3. Compare output to manual trace
   - DRI: Agent
2. [H-002: Dynamic imports can be safely skipped without losing critical dependency edges] [^S-004] ^H-002
   - Strengthen: Find a dynamic import in the codebase that IS on a critical path (negate-first)
   - Utility: M — determines if warning-only is sufficient for dynamic imports
   - Cost: L — grep for dynamic import patterns
   - Next actions: 1. Grep `import(` across src/ 2. Check if any are on main render paths
   - DRI: Agent

<!--
### Delta Assumptions
[A] tags: provisional claims with risk-if-wrong
-->

### Delta Questions

1. [Q-001: Should trace-deps be registered as an MCP tool or a pnpm script?] [^S-004] ^Q-001
   - Strengthen: Compare invocation ergonomics — MCP tool call vs. Bash `pnpm trace-deps`
   - Utility: M — determines integration path
   - Cost: L — review MCP tool registration docs
   - Next actions: 1. Check if script output can be piped to LLM context 2. Compare token overhead of each approach
   - DRI: Agent

<!--
### Delta Priorities
[P] tags: relative importance ordering
-->

### Delta Decisions

1. [D-001: Use ts-morph as the AST engine] Based on: F-ID-002 (native re-export resolution), OBS-003 (LSP failure on barrels), C-003 (Tool-First Design) ^D-001
2. [D-002: BFS traversal with depth limit, barrel files don't increment depth] Based on: OBS-004 (5 calls to resolve through 3 re-export layers) ^D-002
3. [D-003: Output JSON to stdout with compact mode for large traversals] Based on: C-002 (Focused Context), M-004 (15K tokens consumed) ^D-003

---

## Next Best Actions Prioritization Table

### Tier 1 — High utility, blocks design

| # | Item | Utility | Cost | DRI | Status |
|---|------|---------|------|-----|--------|
| 1 | BI table lock [e2] — review Baseline/Ideal outcomes above | High | Low | User | Open |

### Tier 2 — Medium utility, informs schema decisions

| # | Item | Utility | Cost | DRI | Status |
|---|------|---------|------|-----|--------|
| 2 | [H-001](#^H-001) useStore field detection via ts-morph | High | Low | Agent | Open |
| 3 | [Q-001](#^Q-001) MCP tool vs pnpm script | Medium | Low | Agent | Open |
| 4 | [H-002](#^H-002) Dynamic import skip safety | Medium | Low | Agent | Open |

### Tier 3 — Low utility, defer

| # | Item | Utility | Cost | DRI | Status |
|---|------|---------|------|-----|--------|

> [!info]- Resolved (0)
>
> _(none yet)_

---

## Evidence Source Paths

[^S-001]: Current session transcript (user request + agent analysis)

[^S-002]: `docs/traces/20260323-sidebar-filter-baseline.md` — sidebar filter baseline trace

[^S-003]: `docs/traces/20260323-sidebar-trace-methodology.md` — 15-step methodology trace with metrics

[^S-004]: `docs/traces/20260323-deterministic-trace-analysis.md` — deterministic vs. semantic classification scorecard

[^S-005]: `ARCHITECTURE-PRINCIPLES.md:102-109` — Deterministic Offloading Principles
