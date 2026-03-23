# Trace: Native Plan → CL Outcomes → Bootstrap Instructions

**Date:** 2026-03-23
**Subject:** How a Claude Code native plan mode session pivoted to incorporate Continuous Learning outcomes, architecture principles, and self-contained Bootstrap Instructions.

---

## Artifacts

| Artifact | Path | Role |
|----------|------|------|
| Session transcript | `~/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools/1476793d-a02f-4a92-817e-2f314b16817c.jsonl` | Primary evidence source |
| Plan file (output) | `~/.claude/plans/cozy-weaving-dragon.md` | Artifact being evolved through the pivot |
| CL skill definition | `.claude/skills/continuous-learning/SKILL.md` | Defines BID workflow, [O] format, phase gates |
| Evidence Ontology skill | `.claude/skills/evidence-ontology/SKILL.md` | Tag grounding dependency |
| Architecture Principles | `ARCHITECTURE-PRINCIPLES.md` | Deterministic Offloading Principles (L102-109) |
| Deterministic analysis | `docs/traces/20260323-deterministic-trace-analysis.md` | Input artifact: 73% deterministic classification |

---

## TRACE: Plan-to-Bootstrap Pivot
══════════════════════════════════════════

### PHASE A: NATIVE PLAN MODE
─────────────────────────────

 1. [OBS: session context — user message]
    User: "create a plan for trace-deps tool"
    Claude Code enters plan mode.
    Plan file assigned: `~/.claude/plans/cozy-weaving-dragon.md`

 2. [OBS: session context — agent action]
    Agent launches 2 parallel Explore agents:
    ├── Agent 1: Existing CLI tools, scripts, ts-morph usage, AST patterns
    └── Agent 2: MCP/hook registration, tsconfig, dependencies
    Results: No ts-morph installed, `tsx` as script runner, 4 path aliases, hooks in `.claude/settings.json`

 3. [OBS: session context — agent action]
    Agent launches 1 Plan agent with full context from Explore results.
    Plan agent produces: ts-morph recommendation, output schema, BFS algorithm,
    detection patterns (JSX, useStore, API calls), test strategy.

 4. [OBS: session context — agent action]
    Agent writes plan file: `~/.claude/plans/cozy-weaving-dragon.md`
    Contents: Context, Files to Create/Modify, 5 Implementation Steps,
    Verification, Edge Cases.

 5. [OBS: session context — agent action]
    Agent calls ExitPlanMode.
    USER REJECTS.                                                    ← KEY EVENT

### PHASE B: CL SKILL PIVOT
────────────────────────────

 6. [OBS: session context — user message]
    User invokes `/continuous-learning` with explicit scope:
    "only do parts b, b.1, c, ↻(→(d, e, ×(e1, e2)), τ)"
    "add output to plan"

    [F-ID: from step 6] User rejected the native plan because it lacked
    outcome-level analysis. The CL skill provides the BID framework to
    ground the plan in observed friction → outcomes → deltas.

 7. [OBS: session context — agent action]
    Agent executes CL phases:
    │
    │  [b] Read session context
    │  ────────────────────────
    │  7a. Agent reviews conversation history for friction signals.
    │      No transcript search needed — current session.
    │
    │  [b.1] Produce artifacts table
    │  ─────────────────────────────
    │  7b. Agent outputs 6-row artifacts table:
    │      Session transcript, 3 trace docs, CLAUDE.md, Learnings #1/#8/#9
    │
    │  [c] Surface friction → findings table
    │  ──────────────────────────────────────
    │  7c. Agent outputs 5 findings (F1-F5):
    │      F1: 33 calls for 73% deterministic task
    │      F2: LSP fails 30% on barrel re-exports
    │      F3: Agent does mechanical BFS decisions
    │      F4: Wrong path guess requiring recovery
    │      F5: LLM synthesis is CORRECT (untargeted)
    │
    │  [d] Build BI table in [O] units
    │  ────────────────────────────────
    │  7d. Agent outputs 5-row BI table:
    │      Row 1: ~33 calls → 1 deterministic call + synthesis
    │      Row 2: Grep fallback on re-exports → zero failures
    │      Row 3: Sequential directory guessing → pre-computed graph
    │      Row 4: LLM synthesis → LLM synthesis (untargeted)
    │      Row 5: Manual pattern detection → structured graph

 8. [OBS: session context — agent action]
    Agent appends CL analysis (artifacts, findings, BI table) to plan file.
    Plan file now has: Implementation Plan + CL Analysis.

### PHASE C: USER CORRECTIONS
─────────────────────────────

 9. [OBS: session context — user message]
    Agent presents hard gate [e2] via AskUserQuestion.
    USER REJECTS the question.

10. [OBS: session context — user message]
    User: "artifacts missing"
    User provides: `jact extract ARCHITECTURE-PRINCIPLES.md "Deterministic Offloading Principles"`

    [F-ID: from step 10] User identified that the architecture principles
    — the very document that DEFINES deterministic offloading — was not
    in the artifacts table. The plan's rationale was ungrounded.

11. [OBS: session context — agent action]
    Agent reads `ARCHITECTURE-PRINCIPLES.md` (150 lines).
    Adds artifact row: "Deterministic Offloading Principles (L102-109)".
    Adds architecture grounding to Context section (4 principles).

12. [OBS: session context — user message]                            ← KEY EVENT
    Agent re-presents hard gate [e2].
    USER REJECTS again.
    User: "add continuous-learning reference as well to explain outcomes,
    and /evidence-ontology as dependencies for using this plan"

    [F-ID: from step 12] User's correction reveals a design requirement:
    the plan must be self-contained. Without the CL and evidence-ontology
    skill references, a reader cannot understand the [O] tags, the BI
    table format, or the phase gates.

13. [OBS: session context — agent action]
    Agent adds 3 artifact rows:
    ├── Continuous Learning skill (SKILL.md)
    ├── Evidence Ontology skill (SKILL.md)
    └── Evidence Ontology reference (EVIDENCE-ONTOLOGY.md)

### PHASE D: BOOTSTRAP INSTRUCTIONS
────────────────────────────────────

14. [OBS: session context — user message]
    Agent re-presents hard gate [e2] a third time.
    USER REJECTS again.
    User: "#USER-FRICTION: goal is to use the plan as a self-contained
    state file so we can restart at any point"

    [F-ID: from step 14] This is the pivotal insight. The user's three
    rejections of [e2] were not about the BI table content — they were
    about the plan's INFRASTRUCTURE. A plan file is useless if a new
    session cannot bootstrap itself from it.                          ← KEY LINE

15. [OBS: session context — agent action]
    Agent creates Prerequisites section with:
    ├── Skills to load
    ├── Key reference files
    └── Current state marker

16. [OBS: session context — user message]
    User: "#USER-FRICTION: it will have the conversation history because
    you are attaching the transcript file. It can use /searching-transcripts
    to get context"

    [F-ID: from step 16] The agent's Prerequisites section was incomplete.
    It listed reference files but not the mechanism to recover conversation
    context. The transcript IS the conversation history — and
    /searching-transcripts is how a new session reads it.

17. [OBS: session context — agent action]
    Agent resolves transcript path:
    `~/.claude/projects/-Users-wesleyfrederick-...-claude-devtools/1476793d-...jsonl`

18. [OBS: session context — agent action]
    Agent replaces Prerequisites with Bootstrap Instructions:
    1. Load skills (/evidence-ontology, /continuous-learning)
    2. Load conversation context via /searching-transcripts (with path + search terms)
    3. Read this plan file (self-contained state)
    4. Read key reference files
    5. Resume at current state

══════════════════════════════════════════
END TRACE

---

## Fact Derivations

1. **[F-ID: from steps 5 + 6]** The user rejected ExitPlanMode because the native plan lacked outcome-level analysis. The CL skill was invoked specifically to add the BID layer (findings → outcomes → deltas) that native plan mode doesn't provide.

2. **[F-ID: from steps 9 + 12 + 14]** Three consecutive rejections of the BI table hard gate were not about BI content — they were about plan infrastructure. Each rejection added a new requirement: (a) architecture principles grounding, (b) skill dependency references, (c) bootstrap instructions for session resumption.

3. **[F-LK: from steps 14 + 16 + 18]** The Bootstrap Instructions section required two user corrections to reach completeness: first the self-contained state file requirement (#USER-FRICTION), then the transcript + /searching-transcripts mechanism. The final pattern has 5 numbered steps covering skills, transcript, plan-as-state, references, and resume point.

4. **[F-ID: from steps 1-18]** The plan file evolved through 4 distinct phases:
   - Phase A (steps 1-5): Implementation-only plan (rejected)
   - Phase B (steps 6-8): + CL analysis (artifacts, findings, BI table)
   - Phase C (steps 9-13): + Architecture grounding + skill dependencies
   - Phase D (steps 14-18): + Bootstrap Instructions (self-contained state file)

5. **[F-ID: from step 14]** The #USER-FRICTION tag was the pivot signal. Prior corrections (steps 10, 12) were incremental additions; step 14 reframed the plan's PURPOSE from "implementation instructions" to "resumable state file."

---

## Process Tree

### Canonical

```
→(a, ×(b, →(c, d, e, ↻(→(f, g, ×(g1, →(h, f))), τ))))
```

### Visual Tree

```
→ plan-to-bootstrap-workflow
├── [a] USER enters plan mode, agent produces native implementation plan
└── × plan-sufficiency
    ├── [b] IF plan accepted: ExitPlanMode (not observed)
    └── → enrichment-sequence
        ├── [c] USER invokes /continuous-learning with scoped phases
        ├── [d] AGENT executes CL phases (b, b.1, c, d) → appends to plan
        ├── [e] AGENT presents hard gate [e2]
        └── ↻ correction-loop
            ├── → correction-cycle                                ← do part
            │   ├── [f] USER rejects gate with correction
            │   ├── [g] AGENT applies correction to plan
            │   └── × re-present
            │       ├── [g1] IF more corrections: re-present gate → back to [f]
            │       └── [τ] (gate accepted — not yet observed)
            └── [τ] (loop exit)                                   ← redo part
```

### Activity Legend

| Node | Activity | Trace Evidence |
|------|----------|---------------|
| [a] | Agent produces native plan (Explore → Plan → Write → ExitPlanMode) | Steps 1-5 |
| [b] | Plan accepted, proceed to execution | Not observed (user rejected at step 5) |
| [c] | User invokes `/continuous-learning` with phase scope | Step 6 |
| [d] | Agent runs CL phases b, b.1, c, d — appends findings + BI to plan | Steps 7-8 |
| [e] | Agent presents hard gate [e2] for BI table lock | Step 9 |
| [f] | User rejects gate: missing architecture principles / missing CL+EO refs / missing bootstrap | Steps 10, 12, 14, 16 |
| [g] | Agent adds: architecture artifact / skill dependencies / Bootstrap Instructions / transcript path | Steps 11, 13, 15-18 |
| [g1] | Re-present gate after correction | Steps 9 (re-presented after 11), (re-presented after 13), (re-presented after 15) |
