# Continuous Learning

**Goal**: Analyze friction in this session and propose improvements to Claude Code configuration (memories, skills, agents, commands, hooks) using the phased BID (Baseline / Ideal / Delta) workflow below.

## BID Definitions

### Outcome [O] Format

`jact extract file ${CLAUDE_SKILL_DIR}/references/evidence-ontology-one-page.md`

**BI table rule:** Every cell in Baseline [O] and Ideal [O] columns MUST be a pure [O]. Never place [OBS], [M], [C], or other tags in these columns. Observations belong in the Findings table (Phase 1), not the BI table (Phase 2).

### BID Table Format

A causal table with columns in left-to-right order: **Baseline → Delta → Ideal**.

| Column   | Meaning                                                 |
| -------- | ------------------------------------------------------- |
| Baseline | What the actor does today (observed behavior)           |
| Delta    | Outcome-level capability that bridges Baseline to Ideal |
| Ideal    | What the actor does after the delta is applied          |

### BID Invariants

1. **Baseline is immutable.** Baseline rows are observed reality. Narrowing Ideal scope or removing a Delta never removes a Baseline row.
2. **Like-for-like units.** Baseline and Ideal for the same row must use the same ontology type. If Baseline is [O], Ideal must be [O].
3. **Untargeted rows.** If a Baseline row has no targeted Ideal, the Delta cell is blank and Baseline carries through unchanged. If the Ideal is to eliminate the behavior, state that explicitly.

### Bucket Semantics

Buckets are system states, not ontology types. Any element can exist in any bucket.

| Bucket | Key Question | Purpose |
|---|---|---|
| BASELINE — Current State | Where are we now? | Understand reality and constraints before change |
| IDEAL — Target State | If success were fully achieved, what would the world look like? | Define evaluation criteria for solutions |
| DELTA — Transformation Path | What changes could move us toward the ideal? | Decision and planning |

### Entry Point Adaptation

Clients may start anywhere. Classify input before building the BI table.

| Client Entry | First Action |
|---|---|
| Baseline problem | Map BASELINE → infer IDEAL |
| Ideal vision | Clarify IDEAL → map BASELINE |
| Solution idea | Treat as DELTA H → reconstruct IDEAL + BASELINE |
| Metrics gap | Map METRICS → infer IDEAL |
| Constraints | Map CONSTRAINTS → define feasible IDEAL |
| Mixed | Decompose into ontology → bucket |

> Always reconstruct all three buckets before deciding.

## Phased Workflow

### Process Tree (formal model)

This tree defines the workflow: sequence, loops, gates, and actor responsibilities. Node expansions below add detail the tree cannot express (output templates, self-checks, config research). Follow the tree for flow control; consult expansions for node-specific instructions.

**Canonical:**
```
→(a, b, b.1, c, ↻(→(d, e, ×(e1, e2)), τ), ↻(→(f, g, ×(g1, g2)), τ), ↻(→(h1, h2, ×(h3, τ), h2.5, ×(h2.6, τ), h4, h5, ×(h5a, h5b)), τ), i0, ↻(→(i1, i2, j, ×(j1, j2)), τ), ↻(→(k, l, ×(l1, l2)), τ), m)
```

**Visual tree:**
```
→ continuous-learning
├── [a] USER invokes /continuous-learning
├── [b] AGENT reads session context (MEMORY.md + transcript)
├── [b.1] AGENT produces artifacts table
├── [c] AGENT surfaces friction patterns → findings table
├── ↻ bi-validation-loop
│   ├── → bi-in-outcome-units                                    ← do part
│   │   ├── [d] AGENT builds BI table in [O] JTBD units
│   │   ├── [e] USER reviews BI table
│   │   └── × bi-decision
│   │       ├── [e1] IF changes needed: USER corrections → back to [d]
│   │       └── [e2] IF approved: USER locks BI table            ← HARD GATE
│   └── [τ] (loop exit — BI locked)                              ← redo part
├── ↻ bdi-validation-loop
│   ├── → bdi-in-outcome-units                                   ← do part
│   │   ├── [f] AGENT adds Delta column in [O] units
│   │   ├── [g] USER reviews BDI table
│   │   └── × bdi-decision
│   │       ├── [g1] IF changes needed: USER corrections → back to [f]
│   │       └── [g2] IF approved: USER locks BDI table           ← HARD GATE
│   └── [τ] (loop exit — BDI locked)                             ← redo part
├── ↻ source-mapping-loop
│   ├── → source-mapping                                        ← do part
│   │   ├── [h1] AGENT identifies source files for each Baseline [O]
│   │   ├── [h2] AGENT reads project config + local reference docs
│   │   ├── × sub-agent-dispatch
│   │   │   ├── [h3] AGENT dispatches claude-code-guide sub-agent
│   │   │   └── [τ] (skip — local doc covers topic)
│   │   ├── [h2.5] AGENT enumerates all sources per row, assigns Source IDs
│   │   ├── × artifacts-table-update
│   │   │   ├── [h2.6] AGENT updates artifacts table with newly discovered sources
│   │   │   └── [τ] (skip — no new sources found)
│   │   ├── [h4] AGENT outputs source mapping table (multi-row per Baseline [O])
│   │   ├── [h5] USER reviews source mapping
│   │   └── × source-mapping-decision
│   │       ├── [h5a] IF changes needed: USER corrections → back to [h1]
│   │       └── [h5b] IF approved: USER locks source mapping    ← HARD GATE
│   └── [τ] (loop exit — source mapping locked)                 ← redo part
├── [i0] AGENT invokes /evaluate-against-architecture-principles skill
├── ↻ delta-architecture-loop
│   ├── → delta-architecture                                     ← do part
│   │   ├── [i1] AGENT translates Deltas into domain units
│   │   ├── [i2] AGENT verifies BID coverage, surfaces gaps
│   │   ├── [j] USER reviews Delta architecture
│   │   └── × architecture-decision
│   │       ├── [j1] IF changes needed: USER corrections → back to [i1]
│   │       └── [j2] IF approved: USER locks architecture        ← HARD GATE
│   └── [τ] (loop exit — architecture locked)                    ← redo part
├── ↻ diff-approval-loop
│   ├── → diff-review                                            ← do part
│   │   ├── [k] AGENT expresses architecture as DIFFs
│   │   ├── [l] USER reviews DIFFs
│   │   └── × diff-decision
│   │       ├── [l1] IF changes needed: USER corrections → back to [k]
│   │       └── [l2] IF approved: USER locks DIFFs               ← HARD GATE
│   └── [τ] (loop exit — DIFFs locked)                           ← redo part
└── [m] AGENT applies approved DIFFs
```

**Activity legend:**

| Node | Actor | Activity | Phase |
|------|-------|----------|-------|
| [a] | USER | invokes `/continuous-learning` | 0 |
| [b] | AGENT | reads MEMORY.md + session transcript | 0 |
| [b.1] | AGENT | produces artifacts table (sources, paths, roles) | 0 |
| [c] | AGENT | surfaces friction patterns → findings table | 1 |
| [d] | AGENT | builds BI table in [O] JTBD units, like-for-like, immutable Baseline | 2 |
| [e] | USER | reviews BI table for correct [O] units and scope | 2 |
| [e1] | USER | suggests corrections to BI table | 2 |
| [e2] | USER | locks BI table | 2 |
| [f] | AGENT | adds Delta column; each Delta bridges its Baseline → Ideal | 3 |
| [g] | USER | reviews BDI table for full coverage | 3 |
| [g1] | USER | suggests corrections to BDI table | 3 |
| [g2] | USER | locks BDI table | 3 |
| [h1] | AGENT | identifies source files for each Baseline [O] | 4 |
| [h2] | AGENT | reads project config + local reference docs per source category | 4 |
| [h3] | AGENT | dispatches claude-code-guide sub-agent (conditional on h2 coverage gaps) | 4 |
| [h2.5] | AGENT | enumerates ALL sources per row, assigns Source IDs (S{row}{letter}) | 4 |
| [h2.6] | AGENT | compares enumerated sources against artifacts table, adds missing entries | 4 |
| [h4] | AGENT | outputs source mapping table with Source ID column, one row per source | 4 |
| [h5] | USER | reviews source mapping for completeness | 4 |
| [h5a] | USER | suggests corrections to source mapping | 4 |
| [h5b] | USER | locks source mapping | 4 |
| [i0] | AGENT | invokes `/evaluate-against-architecture-principles` skill (full evaluation, all 9 categories) | 5 |
| [i1] | AGENT | translates each Delta [O] into domain-appropriate units (code/skill/org) | 5 |
| [i2] | AGENT | verifies BID coverage, surfaces uncovered rows as gaps, [H], [Q], [A] | 5 |
| [j] | USER | reviews Delta architecture | 5 |
| [j1] | USER | suggests corrections to architecture | 5 |
| [j2] | USER | locks Delta architecture | 5 |
| [k] | AGENT | expresses architecture as DIFFs, annotates BID coverage | 6 |
| [l] | USER | reviews DIFFs | 6 |
| [l1] | USER | suggests corrections to DIFFs | 6 |
| [l2] | USER | locks DIFFs | 6 |
| [m] | AGENT | applies approved DIFFs | 7 |

**Five HARD GATEs:**
1. **[e2]** Lock BI in [O] units before introducing Delta
2. **[g2]** Lock BDI in [O] units before mapping to files
3. **[h5b]** Lock source mapping before proposing Delta architecture
4. **[j2]** Lock Delta architecture before expressing as DIFFs
5. **[l2]** Approve DIFFs before applying edits

### Phase Lock Format

When a phase is locked at a HARD GATE, mark it with `#LOCKED` on its own line immediately under the phase header. Do NOT put "Locked" in the header itself.

```markdown
## Phase 2 — BI Table
#LOCKED

| # | Baseline [O] | Ideal [O] |
```

**Never:** `## Phase 2 — BI Table (LOCKED)` or `## Phase 2 — BI Table (Locked)`

### Hard Gate Output Format

Every hard gate prompt MUST use this structure:

1. **Phase output in tables.** Use the per-phase table schema below.
2. **Numbered options.** Always end with a numbered list (never prose options).

**Per-Phase Table Schemas:**

| Phase | Required Columns |
|-------|-----------------|
| 1 — Findings | ID, Pattern Found, Scope, Trigger, Friction Caused |
| 2 — BI | #, Baseline [O], Ideal [O] |
| 3 — BDI | #, Baseline [O], Delta [O], Ideal [O] |
| 4 — Source Mapping | #, Baseline Outcome, Source, Baseline Notes |
| 5 — Architecture | #, File, Line, Before, After, Principle, BDI Row |
| 6 — DIFF | diff block + summary table (What Changes, Why) |

**Numbered Options Per Gate:**

| Gate | Options |
|------|---------|
| [e2] | 1. Lock BI  2. Correct BI |
| [g2] | 1. Lock BDI  2. Correct BDI |
| [h5b] | 1. Lock source mapping  2. Correct source mapping |
| [j2] | 1. Lock architecture  2. Correct architecture |
| [l2] | 1. Lock DIFF, apply  2. Correct DIFF |

### [b] [b.1] Read Context
Read MEMORY.md and the session transcript. **If the transcript exceeds 25K tokens (Read tool will error), use the `searching-transcripts` skill** to extract structured messages from the JSONL file.

**Search terms for friction signals** (priority order): `#USER` tags first (explicit user-flagged friction), then `"No,"`, `"error"`, `"interrupted"`, `"Actually"` for corrections and failures.

Use the line numbers from search results to Read with offset/limit for full context on friction hits.

**If analyzing the current session** (no JSONL file), surface frictions from conversation context directly.

Then output an **Artifacts Table** declaring all sources in scope:

| Column | What to include |
|--------|----------------|
| Artifact | Human-readable name (e.g., "Session transcript", "Current CL skill", "Evidence ontology") |
| Path | Repo-relative path to the file. Current session uses `(current session)`. |
| Role | Why this artifact matters to the analysis (e.g., "Primary evidence for Baseline behaviors", "Target artifact being updated") |

**What qualifies as an artifact:**
- The session transcript(s) being analyzed (always present)
- The target file(s) the skill will propose changes to
- Reference documents the skill loads (Evidence Ontology, Architecture Principles)
- Any prior BID analysis documents referenced
- Intermediate traces or synthesized artifacts that add context

This is agent output for traceability, not a user review gate.

### [c] Surface Friction → Findings Table
Review the session transcript for these pattern categories:

| Category | Signal | Output Template |
|----------|--------|-----------------|
| **User Corrections** | "No, use X instead of Y", "Actually, I meant...", "Why are you...", immediate undo/redo | "When doing X, prefer Y" |
| **Error Resolutions** | Tool error followed by fix, same error type resolved similarly multiple times | "When encountering error X, try Y" |
| **Repeated Workflows** | Same tool sequence with similar inputs, file patterns that change together, time-clustered operations | "When doing X, follow steps Y, Z, W" |
| **Tool Preferences** | Consistent preference for one tool over another, specific flags that work better. Do NOT repeat directives already in CLAUDE.md or active skills. | "When needing X, use tool Y" |

Output a findings table: **ID** | **Pattern Found** | **Scope** (global / specific workflow) | **Trigger** | **Friction Caused**

### [d] BI Table in [O] Units
For each finding, express Baseline and Ideal as JTBD outcomes (see Outcome [O] Format above).
- Self-check: are B and I in matching units? (Like-for-like invariant)
- Self-check: are all Baseline rows from findings preserved? (Immutability invariant)

### [f] BDI Table in [O] Units
Add a Delta column: each Delta must logically bridge its Baseline to its Ideal.
- Self-check: does applying this Delta to this Baseline produce this Ideal?
- Untargeted rows: Delta cell is blank, Baseline carries through (Untargeted rows invariant)

### Baseline → Source Mapping (Phase 4)
Each Baseline [O] maps to one or many source files. Sources must trace to primary evidence; intermediate artifacts kept where they add synthesis.

#### Local Reference Docs Directory

`references/claude-code-docs/` contains pre-fetched Claude Code documentation as clean markdown. These are the primary reference for Phase 4 config research. The agent reads these directly; no sub-agent needed when the topic is covered.

**Naming convention:** `docs-en-{topic-slug}.md` where `{topic-slug}` matches the URL path at `code.claude.com/docs/en/{topic-slug}`.

| File | Covers | Use for source category |
| ---- | ------ | ---------------- |
| `docs-en-skills.md` | Skill frontmatter fields, `context: fork`, `allowed-tools`, `hooks` in skills, supporting files, invocation control, sub-agent execution | Skill |
| `docs-en-hooks-guide.md` | Hook events (PreToolUse, PostToolUse, Stop, etc.), matchers, exit codes, skill-scoped hooks, prompt hooks, agent hooks | Hook |
| `docs-en-sub-agents.md` | Agent definition files (`.claude/agents/`), frontmatter fields (tools, model, skills, mcpServers, hooks, memory), built-in agents (Explore, Plan, general-purpose), `Agent(type)` tool restrictions | Agent |
| `docs-en-memory.md` | Memory system, MEMORY.md format, memory types, auto-memory behavior | Memory |
| `docs-en-settings.md` | CLAUDE.md files (project, user, enterprise), settings.json, permissions, precedence rules | CLAUDE.md |

**Staleness check:** If a file is missing or contains unextracted HTML (nav chrome, `<img>` tags, no markdown heading structure), it's stale. Refresh before reading — see **Reference doc refresh protocol** below.

#### Config Research Process

**[h1] Identify source files.** For each Baseline [O], identify the file(s) that produce that behavior from what is already known (BDI table, artifacts table, session context).

**[h2] Read project config + local reference docs (deterministic).**

| Source category | Project config files to read | Local reference doc |
| -------- | ---------------------------- | ------------------- |
| Skill | Project `.claude/skills/` + user `~/.claude/skills/` — target skill SKILL.md + its `references/` dir | `docs-en-skills.md` |
| CLAUDE.md | Project CLAUDE.md + global CLAUDE.md | `docs-en-settings.md` |
| Memory | MEMORY.md + linked memory files | `docs-en-memory.md` |
| Hook | `.claude/settings.json` hooks section | `docs-en-hooks-guide.md` |
| Agent | Agent definition file (`.claude/agents/`) or command script | `docs-en-sub-agents.md` |
| Cross-Skill Reference | Referenced skill's SKILL.md + its `references/` dir | (same as primary source category) |

Read order:
1. Read all project config files (column 2) for each source category
2. Read the local reference doc (column 3) for each source category
3. If a local reference doc is stale or missing, refresh it first (see protocol below)


**[h3] Sub-agent dispatch (conditional, after h2).**

Only dispatch if the local reference doc doesn't cover the specific capability being investigated. Example: local `docs-en-skills.md` covers frontmatter fields and hooks but may not cover a new feature added after the doc was fetched.

**What is `claude-code-guide`:** A built-in Claude Code sub-agent type specialized for answering questions about Claude Code features. Tools: Glob, Grep, Read, WebFetch, WebSearch. It can search the local reference docs directory AND fetch current docs from the web. It cannot edit files.

**When to dispatch:**
- Local reference doc exists and covers the topic → skip sub-agent, use local doc directly
- Local reference doc exists but doesn't cover the specific capability → dispatch sub-agent with narrowed question
- Local reference doc is missing or stale → refresh via protocol below, then read; dispatch sub-agent only if refreshed doc still doesn't cover the topic
- Source category has no matching table row → dispatch sub-agent with the source category as research question

**Sub-agent dispatch template:**
```
Agent:
  subagent_type: "claude-code-guide"
  description: "CL Phase 4 config research: {source category}"
  prompt: |
    Find Claude Code documentation about: {specific capability question}.

    Local reference docs directory: {$CLAUDE_SKILL_DIR}/references/claude-code-docs/
    I've already read {local doc filename} and it doesn't cover: {what's missing}.

    Search for the specific capability. Return findings as:
    - source: absolute file path or URL where you found the information
    - capability: name of the feature/config option
    - details: 2-3 sentences on how it works and how to configure it
```

**[h2.5]** Source ID format: `S{row}{letter}` (e.g., S3a, S3b, S3c).

**[h2.6]** Artifacts table sync (mandatory after h2.5):
1. Compare each Source ID from h2.5 against the [b.1] artifacts table
2. For any Source ID referencing a file not in the artifacts table: add a row (Artifact name, Path, Role)
3. If no new sources found, skip (per process tree `×(h2.6, τ)`)
4. Self-check: re-read artifacts table after edits to confirm all Source IDs have a matching row

**[h4]** Output template: **#** | **Baseline [O]** | **Source ID** | **Source** | **Baseline Notes**

One row per source file. Source IDs trace forward into Phase 5/6. Baseline Notes column records what was found in project config, local reference docs, and sub-agent results.

Process sub-tree: `→(h1, h2, ×(h3, τ), h2.5, ×(h2.6, τ), h4)` — h3 conditional on h2 findings; h2.6 conditional on h2.5 discovering new sources.

#### Reference Doc Refresh Protocol

The docs site (`code.claude.com`) is JS-rendered (Mintlify). Plain HTTP fetch returns only the HTML shell. Use WebFetch for content extraction.

```
WebFetch:
  url: "https://code.claude.com/docs/en/{topic-slug}"
  prompt: "Extract the COMPLETE documentation. Return full content as clean markdown. Do not summarize."
```

Write the result to `{$CLAUDE_SKILL_DIR}/references/claude-code-docs/docs-en-{topic-slug}.md`.

Known topic slugs:

| Source category | Topic slug | Filename |
| -------- | ---------- | -------- |
| Skill | `skills` | `docs-en-skills.md` |
| Hook | `hooks-guide` | `docs-en-hooks-guide.md` |
| Agent | `sub-agents` | `docs-en-sub-agents.md` |
| Memory | `memory` | `docs-en-memory.md` |
| CLAUDE.md | `settings` | `docs-en-settings.md` |

For source categories not in this table, ask the `claude-code-guide` sub-agent to find the correct URL, then add a new row.

### [i0] Evaluate Against Architecture Principles

Invoke the `/evaluate-against-architecture-principles` skill. This runs a full evaluation against all principle categories.

The skill handles extraction, evaluation, and output formatting. Its results become evaluation criteria for DIFF review in Phase 6.

### [i1] Translate Deltas

Translate each Delta [O] into domain-appropriate units:
- **Code**: technology, patterns, pseudo-code
- **Skill/prompt**: sections, instructions, gates, output templates
- **Org**: people, processes, values

### [i2] Verify BID Coverage

Load the evidence ontology for tag definitions:

!`jact extract file ${CLAUDE_SKILL_DIR}/references/evidence-ontology-one-page.md 2>/dev/null`

Every Delta row must appear in the architecture. Surface uncovered rows as gaps, assumptions as [H], open questions as [Q], and actions as [A].

Present `/evaluate-against-architecture-principles` results alongside Delta architecture at HARD GATE [j2] for user review.

### [k] DIFF Expression
Express locked Delta architecture as DIFFs, each annotated with which BID [O] rows it covers.
- Small diff (< 15 lines changed): show inline in chat as a `diff` block
- Large diff (15+ lines changed): write a plan artifact following [plan-template](plan-template.md) %% force-extract %% format (File Changes: ADDED/MODIFIED/REMOVED/UNTOUCHED with sketch-level code blocks)

#### Process Tree Sync Check

When ANY DIFF adds, removes, or reorders a process tree node, ALL THREE representations must be updated in the same DIFF:

1. **Canonical notation** — the inline parseable form (e.g., `→(a, b, ×(c, τ))`)
2. **Visual tree** — the indented reading aid with `├──` connectors
3. **Activity legend** — the table mapping node letters to Actor, Activity, Phase

**Notation rules (co-located):**

| Symbol | Name | Meaning |
|--------|------|---------|
| `→` | sequential | execute children left-to-right |
| `×` | exclusive choice | execute exactly ONE child |
| `∧` | parallel | execute ALL children in any order |
| `↻` | redo loop | first child is "do", rest are "redo" options |
| `τ` | silent activity | invisible/skip — no observable output |

**Common τ patterns:**
- `×(a, τ)` — activity `a` can be skipped
- `↻(a, τ)` — execute `a` one or more times

**Visual tree rules:**
- Root line: `operator workflow-name`
- Operator lines: `operator group-name` — govern their children
- Leaf lines: `[letter] activity description` — indent under parent

**Self-check:** If DIFF touches any process tree node, verify all three representations are consistent before presenting.

### [m] Apply
Apply user-approved DIFFs only.

## Ontology Output Rules

When using ontology tags in findings, follow Evidence Ontology format:
- **[OBS] requires source pointers**: `[OBS: SKILL.md:45-49 → "Upgrade to latest" uses @latest tag]`
- **[OBS] executions require command + result**: `[OBS: npm view dist-tags → stable: 2.1.50, latest: 2.1.63]`
- **Never bare [OBS]**: `[OBS: the skill uses @latest]` is invalid — no pointer
- All other tags ([H], [A], [D], [O], [C], [Q]) follow Evidence Ontology One Page definitions

