---
name: poc-whiteboard-to-plan
description: "Use when converting a completed POC whiteboard (all Q/A/H resolved) into an implementation plan with sketch-level code blocks. POC-specific: skips LSP deep trace, tech debt audit, and architecture principles evaluation since all files are new."
---

# POC Whiteboard to Plan

## Overview

Converts a completed POC whiteboard into an implementation plan. The whiteboard must have all research done — every Q, A, and H item resolved. This skill handles the gap between "research complete" and "ready to implement" by scanning for residual open items, framing schema decisions via baseline/ideal comparison, updating the whiteboard with new decisions, and writing the plan with sketch-level code blocks.

POC-specific: no LSP deep trace (all files are new), no tech debt audit (no existing code), no architecture principles evaluation (POC scope).

## Input Contracts

### Whiteboard (required)

The input whiteboard must contain the following sections and item formats. If any section is missing, flag to the user before scanning.

| Required Section | Expected Item Format | Example |
|-----------------|---------------------|---------|
| Baseline Observations | `OBS-NNN: description` with source footnotes | `[OBS-010: persistence layout: messages.json]` |
| Ideal Constraints | `C-NNN: description` | `[C-001: no Effect framework for POC]` |
| Ideal/Delta Decisions | `D-NNN: description` with evidence citations | `[D-002: three-file module structure]` |
| Delta Potential Decisions | Same as Decisions, but not yet promoted | Labeled "Potential Decision" |
| Questions (Q) | `Q-NNN: question` with resolve status | Status: Open, Resolved |
| Assumptions (A) | `A-NNN: claim` with resolve status | Status: Open, Confirmed, Refuted |
| Hypotheses (H) | `H-NNN: claim` with resolve status | Status: Open, Confirmed, Falsified |
| Goals (G) | `G-NNN: description` | `[G-001: sync Slack messages]` |

### Other Required Inputs

- **Plan template**: Co-located at [references/plan-template.md](references/plan-template.md)
- **Baseline artifact path**: Provided by whiteboard or user (data shape for schema comparison)
- **Domain model path**: Provided by whiteboard or user (ideal type mappings)

---

## Hard Gates

1. **Whiteboard completeness**: All Q, A, and H items in the whiteboard must show resolved/confirmed status. If any remain open, flag them for user resolution before proceeding.
2. **User resolves open items**: After scanning the whiteboard for unresolved items (step [c]), present all findings to the user. Do not proceed to schema decisions or plan writing until user resolves each item.
3. **User resolves schema decisions**: After framing baseline/ideal delta (step [g]), present schema decisions to the user. Do not write to the whiteboard until user resolves each.
4. **SKETCH RULES enforcement**: ADDED code blocks must contain only function signatures, type definitions, algorithmic comments, and dependency composition. NO function bodies, loops, conditionals, or runnable code. Test: if you can copy-paste and execute it, it's too much.

## Process Tree

### Canonical

```
→(a, b, c, ×(d, →(e, f, g, h)), i, j, k, l, m, n)
```

### Visual Tree

```
→ poc-whiteboard-to-plan
├── [a] read plan template; note SKETCH RULES
├── [b] scan whiteboard for unresolved items
├── [c] present open items to user → user resolves              ← HARD GATE
├── × schema-decisions-needed
│   ├── [d] IF no schema gaps: skip to [i]
│   └── → frame-schema-decisions
│       ├── [e] read baseline artifact (existing data shape)
│       ├── [f] read domain model (ideal data shapes)
│       ├── [g] frame delta: new D items with schema definitions
│       └── [h] present schema decisions to user → user resolves ← HARD GATE
├── [i] write decisions to whiteboard (promote, add, reclassify)
├── [j] read analogous implementation files + files to modify
├── [k] write plan Context + Baseline Tracing Guide + Tech Debt
├── [l] write plan File Changes with SKETCH code blocks          ← HARD GATE
├── [m] write plan Decision Coverage table
└── [n] write plan Verification section
```

### Activity Legend

| Node | Actor | Activity | Tool Calls | Trace Evidence |
|------|-------|----------|------------|----------------|
| [a] | Agent | Read plan template. Internalize SKETCH RULES (lines 63-72). | Read | step 1 |
| [b] | Agent | Scan whiteboard systematically: (1) un-promoted Delta Potential Decisions, (2) misclassified OBS items (naming paths without defining schemas = open D item), (3) deferred design decisions in constraints, (4) Q/A/H without resolved status. | Read | step 2 |
| [c] | User | Present numbered list of open items with options and recommendations. User resolves each. | — | step 3 |
| [d] | Agent | IF all schemas already defined in whiteboard: skip to [i]. | — | not observed in trace |
| [e] | Agent | Read baseline artifact. Extract: field names, nesting, enrichment fields, custom formats, wrapper metadata. | Read | step 4 |
| [f] | Agent | Read domain model for relevant bounded contexts. Extract: which domain types sync data maps to, entity relationships, what's NOT modeled yet. | Read | step 5 |
| [g] | Agent | Frame delta between baseline shape and domain ideal. For each gap, define a new D item with options, schema definition, and evidence citations. | — | step 6 |
| [h] | User | Present schema decisions to user. User resolves each (e.g., raw API shape vs cleaned intermediate). | — | step 7 |
| [i] | Agent | Write all new/promoted decisions to whiteboard: promote potential decisions, add schema decisions with field-level comments, add supporting decisions, reclassify mistyped items with annotations. | Edit | steps 8-9 |
| [j] | Agent | Read analogous CLI entry point (copy structure, note what NOT to copy). Read files that will be MODIFIED (confirm current state). | Read | steps 10-11 |
| [k] | Agent | Write Context (1-3 sentences + whiteboard reference). Write Baseline Tracing Guide (folder map, LSP commands — "not applicable" for POC, key files to read). Write Tech Debt ("not applicable — POC scope"). | Write | steps 12-14 |
| [l] | Agent | Write File Changes with SKETCH code blocks per SKETCH RULES. Types files: full interfaces (no bodies to fill). Core logic: function signatures + return types + algorithmic comments. CLI entry: sketch ≈ implementation when small. MODIFIED: diff blocks. | Write | step 15 |
| [m] | Agent | Write Decision Coverage table. Every D-NNN, C-NNN, G-NNN from whiteboard mapped to plan location. | Write | step 16 |
| [n] | Agent | Write Verification section. Smoke test commands, verify output files, verify incremental behavior, verify constraints. | Write | step 17 |

---

## Step-by-Step

### Phase 1: Scan Whiteboard for Unresolved Items

**Step 1 — Read plan template.**
Read [plan-template.md](references/plan-template.md). Internalize the SKETCH RULES comment block (lines 63-72) — this defines what ADDED code blocks may and may not contain.

**Step 2 — Validate whiteboard structure, then scan.**
First, confirm the whiteboard contains the required sections from the Input Contracts table above. If any section is missing, flag to the user before scanning — a missing section means the scan will silently miss issues.

Then scan the whiteboard for:

| Check | What to look for | Example |
|-------|------------------|---------|
| Un-promoted decisions | Delta Potential Decisions still labeled "Potential" | D-002 "three-file module" needs user confirmation |
| Misclassified observations | OBS items that name file paths or schemas without defining content — these are open design decisions, not observations | OBS-010 "persistence layout: messages.json, sync-state.json" names files but doesn't define schemas |
| Deferred design decisions | Constraints that defer decisions to "specs phase" or "implementation" | C-001 "HTTP client choice is a design decision for the specs phase" |
| Unresolved Q/A/H | Items without RESOLVED/CONFIRMED status | Any Q, A, or H without status → flag |

**Step 3 — Present open items to user.** ← HARD GATE
Present all findings as a numbered list. Each item includes: what it is, options (if applicable), recommendation. User resolves each with short answers.

### Phase 2: Frame Schema Decisions (conditional)

Skip this phase if all schemas are already defined in the whiteboard.

**Step 4 — Read baseline artifact.**
Read the artifact that shows the current data format. Extract: field names, nesting structure, enrichment fields, custom formats, wrapper metadata.

**Step 5 — Read domain model.**
Read the domain model for relevant bounded contexts. Extract: which domain types the sync data maps to, what entity relationships exist, what is NOT modeled yet.

**Step 6 — Frame the delta.**
Compare baseline shape against domain ideal. Identify design decisions the plan needs but the whiteboard didn't capture. For each gap, define a new D item with:
- Options (if a choice exists)
- Schema definition (if a format decision)
- Evidence citations back to baseline artifact + domain model

Key insight: baseline fields that come from API enrichment calls the POC won't make (e.g., `users.info`) must be handled explicitly — the POC message shape differs from the baseline.

**Step 7 — Present schema decisions to user.** ← HARD GATE
Present each schema decision with options. User resolves each.

### Phase 3: Update Whiteboard

**Step 8 — Write decisions to whiteboard.**
Write all new/promoted decisions into the whiteboard's Ideal Decisions section:

| Action | Example |
|--------|---------|
| Promote potential decisions | D-002 → add to Ideal Decisions; mark Delta copy as "PROMOTED → Ideal Decisions #N" |
| Add schema decisions with full definitions | D-006 includes Message + ChannelMessages shapes with field-level comments citing D-004, D-005, F-LK-NNN |
| Add supporting decisions | D-009 (HTTP client) cites D-001, C-001, F-LK-002 |
| Reclassify mistyped items | OBS-010 gets annotation: "schemas resolved in D-006, D-007, D-008" |

**Step 9 — Validate links.**
If a citation-manager hook fires, verify 0 critical errors. Fix broken anchors if needed.

### Phase 4: Read Analogous Files

**Step 10 — Read analogous implementation.**
Read the existing CLI pattern this POC mirrors. Extract: shebang, argv parsing, program structure, run pattern. Note what to copy (structure) vs what NOT to copy (e.g., Effect framework if constraint says no Effect for POC).

**Step 11 — Read files to modify.**
Read `package.json` and `.gitignore` (or equivalent files being MODIFIED). Confirm current state before writing diff blocks.

### Phase 5: Write Plan

Use the [plan template](references/plan-template.md) as the structural guide.

**Step 12 — Write Context.**
1-3 sentences: what this change does + why. Include whiteboard path reference.

**Step 13 — Write Baseline Tracing Guide.**
- **Folder map**: every file with ADDED/MODIFIED/UNTOUCHED label
- **LSP commands**: for POC with all-new files, write "Not applicable — all files ADDED, no existing callers to trace." Include `documentSymbol` on analogous files for reference.
- **Key files to read**: ordered list with line ranges + what to extract from each

**Step 14 — Write Tech Debt.**
For POC: "Not applicable — POC scope. All files are ADDED; no existing code to audit."

**Step 15 — Write File Changes with SKETCH code blocks.** ← HARD GATE

Enforce SKETCH RULES:

| Allowed | Not Allowed |
|---------|-------------|
| Function signatures (name, params, return type) | Function bodies |
| Type definitions and interfaces | Loops, conditionals |
| Key algorithmic decisions as comments | Error handling implementation |
| Dependency/layer composition (imports, wiring) | Runnable code |
| Test assertions (what to verify, not how) | — |

**Exceptions:**
- **Types files**: Full interface definitions are the sketch — interfaces have no bodies to fill in.
- **Small CLI entry points**: When the entire file is argument extraction + one function call, sketch ≈ implementation.

**For MODIFIED files**: Use diff blocks showing exact before/after.

**Step 16 — Write Decision + Outcome Coverage table.**
Every tagged item from the whiteboard must trace to the plan:

| Whiteboard Tag | Maps to Plan Section | Coverage Type |
|---------------|---------------------|---------------|
| O-NNN (Outcomes) | Verification → Success Criteria / Acceptance Criteria | How the plan proves this outcome is achieved |
| D-NNN (Decisions) | File Changes → specific file or code sketch | Where the decision is implemented |
| C-NNN (Constraints) | File Changes or Verification → constraint assertion | How the constraint is enforced or tested |
| G-NNN (Goals) | Verification → Definition of Done | How the goal's achievement is measured |

**Outcomes are mandatory.** Every O-NNN from the whiteboard's Ideal bucket must appear in the coverage table with a concrete success criterion, acceptance criterion, or definition of done item. An outcome without a verification path means the plan cannot prove it delivered value.

**Step 17 — Write Verification section.**
For POC: smoke test commands (no TDD). Include:
- Run command
- Verify output files exist
- Verify incremental behavior (e.g., re-run produces same result)
- Verify .gitignore / config changes
- Verify constraints (e.g., raw user IDs only, no enrichment)

---

## Common Mistakes

| Mistake | Fix | Source |
|---------|-----|--------|
| Skipping the whiteboard scan and going straight to plan writing | Always scan for un-promoted decisions, misclassified OBS, and unresolved Q/A/H first. Decisions that exist only in chat produce uncheckable coverage tables. | F-LK from step 8 |
| Writing runnable code in ADDED code blocks | ADDED blocks are sketches. If you can copy-paste and execute it, it's too much. Only types files and tiny CLI entry points are exempt. | F-LK from step 15 |
| Treating OBS items that name file paths as schema definitions | An observation that names `messages.json` is not a schema definition. If the shape/format is unspecified, reclassify as an open design decision (D item). | F-LK from step 2b |
| Writing schema decisions directly into the plan without updating the whiteboard | New decisions must be written to the whiteboard BEFORE creating the plan. The plan's Decision Coverage table references whiteboard D-NNN items. | F-LK from step 8 |
| Including LSP deep trace and tech debt sections for all-new-file POCs | For POC changes where all files are ADDED: LSP commands = "not applicable", Tech Debt = "not applicable". Sections are present but explicitly marked as skipped with rationale. | F-ID from steps 13+14 |
| Copying framework patterns the POC constraints exclude | Read analogous files for structure, but NOTE what NOT to copy. If a constraint says "no Effect", do not copy Effect.gen, BunRuntime.runMain, pipe composition. | Step 10 |
| Writing Decision Coverage without Outcomes | The coverage table must include O-NNN outcomes mapped to success criteria, acceptance criteria, or definition of done. A plan that only covers D/C/G items but not outcomes cannot prove it delivers value. | User friction |

---

## References

- [Plan template](references/plan-template.md) — template with SKETCH RULES for plan output structure
