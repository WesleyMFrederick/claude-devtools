---
name: whiteboard-to-plan
description: "Use when converting a whiteboard into an implementation plan — handles both full path (goal → whiteboard → comments → arch eval → plan) and POC path (completed whiteboard → scan → schema decisions → plan). Includes LSP research, comment integration, architecture evaluation, baseline tracing, tech debt audit, and plan creation with SKETCH code blocks."
---

# Whiteboard to Plan

## Overview

Converts a whiteboard into an implementation plan. Two entry paths:

- **Full path**: User provides a goal. Agent creates the whiteboard from scratch via LSP research, writes all BID sections, integrates user comments from Obsidian, runs architecture evaluation, then writes the plan with deep LSP tracing and tech debt audit.
- **POC path**: Whiteboard is already complete (all Q/A/H resolved). Agent scans for residual open items, frames schema decisions via baseline/ideal comparison, updates the whiteboard, then writes the plan. Skips LSP deep trace, tech debt audit, and architecture evaluation since all files are new.

Both paths converge on the same plan-writing sequence with the same SKETCH RULES and Decision + Outcome Coverage table.

## Input Contracts

### Whiteboard (required for both paths)

| Required Section | Expected Item Format | Example |
|-----------------|---------------------|---------|
| Original Request | `OBS-001: description` + `G-001: goal` with source footnotes | `[OBS-001: user chat message] [^S-001]` |
| Artifacts Investigated | Grouped by concern, with paths | CLI, Core, Types, Tests, Hooks |
| Baseline Bucket | OBS-NNN, Q items, Facts-Locked | `[OBS-010: schema.yaml has 6 artifacts]` |
| Ideal Bucket | OBS (outcomes), C (constraints), A (assumptions), Q, Decisions | `[C-001: no Effect for POC]` |
| Delta Bucket | Potential Decisions, Hypotheses, Questions | `[D-002: three-file module]` |
| Evidence Source Paths | `[^S-NNN]: absolute/path:line-range` | Every footnote verified |

**Full path**: agent creates this from scratch.
**POC path**: whiteboard must already exist with all Q/A/H resolved.

### Other Inputs

- **Plan template**: Co-located at [references/plan-template.md](references/plan-template.md)
- **Whiteboard template**: Co-located at [references/whiteboard.md](references/whiteboard.md)
- **Whiteboard instruction**: Co-located at [references/whiteboard-instruction.md](references/whiteboard-instruction.md)

---

## Hard Gates

1. **Evidence ontology first** (full path): Read EVIDENCE-ONTOLOGY before tagging ANY claims in the whiteboard
2. **jact validate**: Must pass 0 critical errors on every whiteboard write — blocks workflow until fixed
3. **User reviews whiteboard** (full path): User adds comments in Obsidian before comment integration
4. **User resolves open items** (POC path): All unresolved Q/A/H/un-promoted D items must be resolved before plan writing
5. **User resolves schema decisions** (POC path, conditional): Schema gaps must be resolved before writing to whiteboard
6. **SKETCH RULES enforcement**: ADDED code blocks must contain only signatures, types, algorithmic comments, and composition — NO function bodies, loops, conditionals, or runnable code
7. **User approves plan**: User reviews complete plan before implementation begins

---

## Process Tree

### Canonical

```
→(a, ×(→(b, →(c, d), e, ↻(f, τ), g, h, ↻(i, τ), j), →(k, l, ×(τ, →(m, n, o, p)), q, ↻(r, τ))), s, ×(t, τ), ×(→(u, v), τ), w, x, ×(y, τ), z)
```

### Visual Tree

```
→ whiteboard-to-plan
├── [a] determine entry path: full (no whiteboard) or POC (whiteboard complete)
├── × entry-path
│   ├── → full-whiteboard-creation
│   │   ├── [b] read whiteboard template + instruction + evidence ontology
│   │   ├── → codebase-research
│   │   │   ├── [c] LSP: workspaceSymbol, findReferences, documentSymbol, goToDefinition
│   │   │   └── [d] read key files (entry points, services, tests, config)
│   │   ├── [e] write whiteboard (all BID sections + evidence source paths)
│   │   ├── ↻ validate-whiteboard
│   │   │   ├── [f] jact validate → fix + re-validate if errors
│   │   │   └── [τ]
│   │   ├── [g] user reviews whiteboard, adds comments in Obsidian          ← HARD GATE
│   │   ├── [h] /comments-integrate processes all <mark> comments
│   │   ├── ↻ validate-comments
│   │   │   ├── [i] jact validate
│   │   │   └── [τ]
│   │   └── [j] architecture evaluation → resolve Qs via principle anchors → lock Ds
│   └── → poc-whiteboard-completion
│       ├── [k] scan whiteboard for unresolved items
│       ├── [l] present open items → user resolves                          ← HARD GATE
│       ├── × schema-decisions
│       │   ├── [τ] no schema gaps: skip
│       │   └── → frame-schemas
│       │       ├── [m] read baseline artifact (current data shape)
│       │       ├── [n] read domain model (ideal type mappings)
│       │       ├── [o] frame delta: new D items with schema definitions
│       │       └── [p] present schema decisions → user resolves            ← HARD GATE
│       ├── [q] write decisions to whiteboard (promote, add, reclassify)
│       └── ↻ validate-decisions
│           ├── [r] jact validate
│           └── [τ]
├── [s] read plan template + SKETCH RULES
├── × plan-mode
│   ├── [t] full: EnterPlanMode
│   └── [τ] POC: skip
├── × deep-research
│   ├── → full-trace
│   │   ├── [u] deep LSP: findReferences on all functions being created/deleted/moved
│   │   └── [v] tech debt audit: getDiagnostics on all in-scope files
│   └── [τ] POC: skip — all files new
├── [w] read analogous implementation files + files to modify
├── [x] write plan (Context, Baseline Tracing, Tech Debt, File Changes, Coverage, Verification)
├── × exit-plan
│   ├── [y] full: ExitPlanMode
│   └── [τ] POC: skip
└── [z] user reviews + approves plan                                        ← HARD GATE
```

### Activity Legend

| Node | Actor | Activity | Tool Calls | Trace Evidence |
|------|-------|----------|------------|----------------|
| [a] | Agent | Determine entry: does a completed whiteboard exist with all Q/A/H resolved? Full = no whiteboard. POC = whiteboard complete. | Read | — |
| [b] | Agent | Read whiteboard template, instruction, and evidence ontology. Internalize tag rules before writing. | Read | full:step 2-3 |
| [c] | Agent | LSP research: workspaceSymbol (discover types/functions), findReferences (ALL callers), documentSymbol (type shapes), goToDefinition (trace definitions) | LSP | full:step 4 |
| [d] | Agent | Read key files AFTER LSP: CLI entry points, services, tests, package.json scripts | Read | full:step 5 |
| [e] | Agent | Write whiteboard: Original Request (OBS-001 + G-001), Artifacts, Baseline (OBS from LSP + reads), Ideal (user intent, C, A, Q), Delta (potential D, H, Q), Evidence Source Paths | Write | full:step 6 |
| [f] | Agent | jact validate on whiteboard write. 0 errors → continue. Errors → fix paths/footnotes → re-validate. | Bash (jact) | full:step 7 |
| [g] | User | Opens whiteboard in Obsidian, adds `<mark>` comments on specific items | — | full:step 9 |
| [h] | Agent | Run /comments-integrate. Process each comment: Q→resolve, OBS→update, constraint→add C-NNN, design answer→add D-NNN. Remove all `<mark>` markup. | Skill, Edit | full:steps 10-11 |
| [i] | Agent | jact validate after comment integration | Bash (jact) | full:step 12 |
| [j] | Agent | Evaluate open Qs against ARCHITECTURE-PRINCIPLES.md anchors. Resolve each Q → add D item with principle citation. Lock decisions. | Read, Edit | full:steps 13-14 |
| [k] | Agent | Scan whiteboard: (1) un-promoted Delta Potential Decisions, (2) misclassified OBS (naming paths without defining schemas = open D), (3) deferred design decisions in constraints, (4) Q/A/H without resolved status | Read | poc:step 2 |
| [l] | User | Review numbered list of open items. Resolve each with short answers. | — | poc:step 3 |
| [m] | Agent | Read baseline artifact. Extract: field names, nesting, enrichment fields, custom formats, wrapper metadata. | Read | poc:step 4 |
| [n] | Agent | Read domain model for relevant bounded contexts. Extract: domain type mappings, entity relationships, what's NOT modeled. | Read | poc:step 5 |
| [o] | Agent | Frame delta: baseline shape vs domain ideal. For each gap, define new D item with options, schema definition, evidence citations. | — | poc:step 6 |
| [p] | User | Resolve each schema decision (e.g., raw API shape vs cleaned intermediate). | — | poc:step 7 |
| [q] | Agent | Write decisions to whiteboard: promote potential decisions, add schema decisions with field-level comments, add supporting decisions, reclassify mistyped items with annotations. | Edit | poc:steps 8-9 |
| [r] | Agent | jact validate after whiteboard update | Bash (jact) | poc:step 9 |
| [s] | Agent | Read plan template. Internalize SKETCH RULES comment block. | Read | full:step 17 / poc:step 1 |
| [t] | Agent | Enter plan mode (read-only except plan file). Full path only. | EnterPlanMode | full:step 15 |
| [u] | Agent | Deep LSP trace: findReferences on EVERY function being created/deleted/moved. Confirms safe deletion scope (no hidden callers). findReferences on shared utilities. documentSymbol on domain types for function signatures. | LSP | full:step 16 |
| [v] | Agent | Tech debt audit: Explore subagents run getDiagnostics on ALL in-scope files (ADDED + MODIFIED + callee chain). Collect CRITICAL errors → Tech Debt section. Suppress severity labels in plan headers. | LSP, Agent | full:step 16.5 |
| [w] | Agent | Read analogous implementation (copy structure, note what NOT to copy). Read files to MODIFIED (confirm current state for diff blocks). | Read | poc:steps 10-11 / full:step 5 |
| [x] | Agent | Write plan: Context, Baseline Tracing Guide, Tech Debt, File Changes (ADDED sketches / MODIFIED diffs / REMOVED / RENAMED / UNTOUCHED), Decision + Outcome Coverage, Verification | Write | full:step 17 / poc:steps 12-17 |
| [y] | Agent | Exit plan mode. Full path only. | ExitPlanMode | full:step 18 |
| [z] | User | Review complete plan. Approve → implementation begins. | — | full:step 18 / poc:end |

---

## Step-by-Step

### Step 0 — Determine Entry Path

Read the whiteboard (if it exists). Check:
- Does a whiteboard exist for this change?
- Are all Q, A, H items resolved/confirmed?

| Condition | Path |
|-----------|------|
| No whiteboard exists | **Full path** — create from scratch |
| Whiteboard exists but has open Q/A/H | **Full path** — treat as incomplete |
| Whiteboard complete, all items resolved | **POC path** — scan + plan |

---

### Full Path: Whiteboard Creation (Steps 1-9)

**Step 1 — Read templates.**
Read [whiteboard-instruction.md](references/whiteboard-instruction.md), [whiteboard.md](references/whiteboard.md), and the evidence ontology. HARD GATE: evidence ontology must be loaded before tagging any claims.

**Step 2 — LSP research.**
RULE: LSP first, Read files second. NEVER skip.

| LSP Command | Purpose | Example |
|-------------|---------|---------|
| workspaceSymbol | Discover key types/functions by name | search "ExcelService", "SheetRow" |
| findReferences | Surface ALL callers of every function in scope | updateMappingFile → 3 callers |
| documentSymbol | Get domain type shapes | DataTypes.ts → SheetRow, MappingEntry |
| goToDefinition | Trace from callers to definitions | — |

**Step 3 — Read key files** (informed by LSP results).
CLI entry points, services, tests, package.json scripts block.

**Step 4 — Write whiteboard** with all required sections per [whiteboard-instruction.md](references/whiteboard-instruction.md).

**Step 5 — jact validate.** Loop until 0 critical errors.

**Step 6 — User reviews whiteboard.** ← HARD GATE
User opens in Obsidian, adds `<mark>` comments. Agent waits for /comments-integrate invocation.

**Step 7 — /comments-integrate** processes each comment type:

| Comment Type | Agent Action |
|-------------|--------------|
| On Q item | Resolve: ~~strikethrough~~ + "RESOLVED: ..." |
| Correcting OBS | Update OBS text; add new OBS if LSP needed |
| Requesting LSP | Run findReferences/documentSymbol; add OBS-NNN |
| Adding constraint | Create new C-NNN item |
| Answering design Q | Create D-NNN decision item |
| "answered in previous" | Cross-reference + resolve |

RULE: Do NOT use AskUserQuestion if comments already answer the question.

**Step 8 — jact validate.** Loop until 0 critical errors.

**Step 9 — Architecture evaluation.**
Evaluate open Qs in Delta Bucket against ARCHITECTURE-PRINCIPLES.md anchors. For each resolved Q: ~~strikethrough~~ Q + add D item with principle anchor reference. Update Whiteboard Decision Coverage table.

---

### POC Path: Whiteboard Completion (Steps 10-15)

**Step 10 — Scan whiteboard** systematically:

| Check | What to look for |
|-------|-----------------|
| Un-promoted decisions | Delta Potential Decisions still labeled "Potential" |
| Misclassified observations | OBS items naming paths/schemas without defining content — these are open D items |
| Deferred design decisions | Constraints deferring decisions to "specs phase" or "implementation" |
| Unresolved Q/A/H | Items without RESOLVED/CONFIRMED status |

**Step 11 — Present open items to user.** ← HARD GATE
Numbered list. Each item: what it is, options, recommendation. User resolves.

**Step 12-13 — Frame schema decisions** (conditional — skip if all schemas defined).
Read baseline artifact (current data shape) + domain model (ideal types). Frame delta: identify design decisions the whiteboard missed. For each gap, define new D item with options, schema definition, evidence citations.

**Step 14 — Present schema decisions to user.** ← HARD GATE
User resolves each.

**Step 15 — Write decisions to whiteboard.**
Promote potential decisions, add schema decisions with field-level comments, add supporting decisions, reclassify mistyped items with annotations. jact validate.

---

### Common: Plan Creation (Steps 16-21)

**Step 16 — Read plan template.**
Read [plan-template.md](references/plan-template.md). Internalize SKETCH RULES (lines 63-72).

**Step 17 — Enter plan mode** (full path only).
EnterPlanMode → read-only except plan file.

**Step 18 — Deep research** (full path only).

| Research | Scope | Purpose |
|----------|-------|---------|
| findReferences | Every function being created/deleted/moved | Confirm safe deletion scope |
| findReferences | Shared utilities | Reveal hidden callers |
| documentSymbol | Domain types in new interfaces | Confirm type shapes |
| getDiagnostics | All in-scope files (ADDED + MODIFIED + callee chain) | Tech debt collection |

POC: skip — all files are new. Write "Not applicable" in LSP and Tech Debt sections.

**Step 19 — Read analogous files.**
Read existing CLI pattern for structure. Read files to MODIFIED for current state. Note what to copy vs. what NOT to copy.

**Step 20 — Write plan** using [plan-template.md](references/plan-template.md):

| Section | Content |
|---------|---------|
| Context | 1-3 sentences + whiteboard reference |
| Baseline Tracing Guide | Folder map, LSP commands, key files to read |
| Tech Debt | getDiagnostics results (full) or "Not applicable" (POC) |
| File Changes | ADDED (SKETCH code blocks), MODIFIED (diff blocks), REMOVED, RENAMED, UNTOUCHED |
| Decision + Outcome Coverage | **Every O-NNN, D-NNN, C-NNN, G-NNN from whiteboard** |
| Verification | TDD sequence (full) or smoke tests (POC) + constraint assertions |

**SKETCH RULES for ADDED code blocks:**

| Allowed | Not Allowed |
|---------|-------------|
| Function signatures (name, params, return type) | Function bodies |
| Type definitions and interfaces | Loops, conditionals |
| Key algorithmic decisions as comments | Error handling implementation |
| Dependency/layer composition (imports, wiring) | Runnable code |
| Test assertions (what to verify, not how) | — |

**Exceptions:** Types files (interfaces ARE the sketch). Small CLI entry points (sketch ≈ implementation).

**Decision + Outcome Coverage table — MANDATORY format:**

| Tag | Label | Coverage Type | How Covered |
|-----|-------|--------------|-------------|
| O-NNN | outcome label | Success Criteria / Acceptance Criteria | How the plan proves this outcome is achieved |
| D-NNN | decision label | Implementation | File or code sketch where implemented |
| C-NNN | constraint label | Enforcement / Test | How constraint is enforced or tested |
| G-NNN | goal label | Definition of Done | How goal achievement is measured |

**Outcomes are mandatory.** Every O-NNN from the whiteboard's Ideal bucket must appear with a concrete verification path. A plan without outcome coverage cannot prove it delivers value.

**Step 21 — Exit plan mode** (full path only). ExitPlanMode.

**Step 22 — User reviews + approves plan.** ← HARD GATE
Approved → implementation begins.

---

## Common Mistakes

| Mistake | Fix | Source |
|---------|-----|--------|
| Skipping LSP research and going straight to file reads | LSP first, Read second. findReferences surfaces ALL callers — file reads alone miss hidden dependencies. | F-LK full:step 4b |
| Skipping the whiteboard scan (POC) and going straight to plan | Scan for un-promoted decisions, misclassified OBS, deferred choices. Decisions only in chat produce uncheckable coverage tables. | F-LK poc:step 2 |
| Writing runnable code in ADDED code blocks | ADDED blocks are sketches. If you can copy-paste and execute it, it's too much. Types files and tiny CLI entry points are exempt. | F-LK full:step 17 / poc:step 15 |
| Treating OBS items that name file paths as schema definitions | An observation that names `messages.json` without defining the shape is an open design decision (D item), not an observation. Reclassify. | F-LK poc:step 2b |
| Writing schema decisions directly into plan without updating whiteboard | Decisions must be written to the whiteboard BEFORE creating the plan. The coverage table references whiteboard D-NNN items. | F-LK poc:step 8 |
| Including full LSP trace + tech debt for all-new-file POCs | For POC: LSP = "not applicable", Tech Debt = "not applicable". Sections present but marked as skipped with rationale. | F-ID poc:steps 13-14 |
| Copying framework patterns the POC constraints exclude | Read analogous files for structure, but NOTE what NOT to copy. If constraint says "no Effect", skip Effect.gen, BunRuntime, pipe composition. | poc:step 10 |
| Writing Decision Coverage without Outcomes | Coverage table MUST include O-NNN mapped to success/acceptance criteria. A plan covering only D/C/G cannot prove it delivers value. | Learning #23 |
| Processing comments before running /comments-integrate | If `<mark>` markup is present, /comments-integrate must run first — otherwise agent re-asks questions the user already answered. | F-LK full:step 11 |
| Running tech debt audit ad hoc instead of as a formal phase | Tech debt audit is a distinct phase between deep LSP trace and plan writing. Ad hoc execution causes items to be missed or misclassified. | F-LK full:step 16.5 |
| Suppressing LSP severity labels in plan | Never copy severity labels ("SUGGESTED", "HINT") into plan section headers. Use neutral labels like "Fix Required". | F-LK full:step 16.5 |

---

## Provenance

This skill was derived from two traces:

| Trace | Path | Covers |
|-------|------|--------|
| Full workflow | `lbnl-benefits/design-docs/workflows/openspec-artifacts/whiteboard-to-plan-trace.md` | Phases 1-4.5: goal → whiteboard → comments → arch eval → LSP → tech debt → plan |
| POC variant | `lbnl-benefits/design-docs/workflows/openspec-artifacts/poc-whiteboard-to-plan-trace.md` | Completed whiteboard → scan → schema decisions → plan (skips phases 1-3, 4.5) |

---

## References

- [Plan template](references/plan-template.md) — output structure with SKETCH RULES and Decision + Outcome Coverage
- [Whiteboard template](references/whiteboard.md) — BID bucket structure for whiteboard creation
- [Whiteboard instruction](references/whiteboard-instruction.md) — evidence ontology rules, required sections, footnote validation
