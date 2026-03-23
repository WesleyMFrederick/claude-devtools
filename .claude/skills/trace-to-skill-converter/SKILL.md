---
name: trace-to-skill-converter
description: Use when converting a completed trace document into a skill SKILL.md. Takes a trace with numbered steps, evidence tags, and optionally a process tree, then produces a draft skill by deterministically extracting structure before semantically synthesizing instructions. Applies to any workflow trace that should become a repeatable skill.
---

# Trace-to-Skill Converter

## Overview

Converts a completed trace document into a draft skill SKILL.md by splitting work into two phases:

1. **Deterministic extraction** — a Python script (`extract-trace-structure.py`) parses the trace and outputs structured JSON. No LLM involved.
2. **Semantic synthesis** — LLM reads the JSON output and writes skill sections that require judgment (name, description, hard gates, step-by-step instructions, common mistakes).

This follows the Deterministic Offloading principle: route parsing and validation to tools, reserve LLM for intent, design, and naming.

## Acceptance Criteria

1. Skill produces a valid SKILL.md with: frontmatter, overview, hard gates, process tree (canonical + visual + activity legend), step-by-step, common mistakes
2. `extract-trace-structure.py` runs before any semantic work and its JSON output is the sole input to Phase 2
3. Output is a draft with a user review hard gate before finalization
4. Skill handles traces with or without an existing process tree/activity legend
5. Architecture evaluation delegates to a sub-agent via Agent tool

## Definition of Done

1. All AC met
2. Tested on at least one trace from `workflows/`
3. Generated SKILL.md passes structure validation (has all required sections)

## Hard Gates

1. **Trace Selection**: Before processing, confirm which trace file to convert. Do not guess.
2. **Draft Review**: After generating the draft SKILL.md, STOP and present it to the user. Do not write to disk without approval.

## Process Tree

### Canonical

```
→(a, b, ×(c, →(d, e, f, g, h, i)))
```

### Visual Tree

```
→ trace-to-skill
├── [a] user selects trace file
├── [b] run extract-trace-structure.py (validates + extracts)
└── × trace-completeness
    ├── [c] IF script reports missing steps/tags: reject with guidance
    └── → convert
        ├── [d] create TodoWrite tasks for remaining phases
        ├── [e] SEMANTIC: synthesize skill sections from JSON
        ├── [f] assemble SKILL.md from template
        ├── [g] delegate architecture eval to sub-agent
        ├── [h] present draft to user                          ← HARD GATE
        └── [i] write approved skill to disk
```

### Activity Legend

| Node | Actor | Activity | Tool Calls |
|------|-------|----------|------------|
| [a] | User | selects trace file to convert | — |
| [b] | Agent | run extraction script on trace file | Bash (python3 extract-trace-structure.py) |
| [c] | Agent | IF script output shows 0 steps or 0 phases: report what's missing | — |
| [d] | Agent | create TodoWrite tasks tracking Phase 2 + 3 steps | TodoWrite |
| [e] | Agent | semantic synthesis: name, description, hard gates, step-by-step, common mistakes | — (LLM reasoning from JSON input) |
| [f] | Agent | assemble sections into SKILL.md template | — (string assembly) |
| [g] | Agent | spawn sub-agent to run /evaluate-against-architecture-principles | Agent (subagent_type: general-purpose) |
| [h] | User | reviews draft + arch eval findings, approves or requests changes | — |
| [i] | Agent | write SKILL.md to skill directory (with backup if exists) | Write, Bash (cp) |

---

## Intermediate Data Contract

Phase 1 (script) outputs JSON. Phase 2 (LLM) consumes it. This is the contract.

```json
{
  "source_file": "string — absolute path to trace",
  "title": "string — first H1 heading",
  "artifacts": [{"artifact": "str", "path": "str", "role": "str"}],
  "steps": [{
    "step_number": "str",
    "tag_type": "str (OBS, M, F-LK, etc.)",
    "source_ref": "str",
    "phase": "str",
    "has_boundary_crossing": "bool",
    "has_substeps": "bool",
    "is_key_line": "bool",
    "body_preview": "str (first 200 chars)"
  }],
  "phases": ["str — PHASE headers"],
  "process_tree": {
    "canonical": "str | null",
    "visual_tree": "str | null",
    "activity_legend": [{"node": "str", "actor": "str", "activity": "str", "tool_calls": "str", "trace_evidence": "str"}]
  },
  "steering_events": [{"number": "str", "source_ref": "str", "description": "str"}],
  "learnings": [{"id": "str", "body": "str"}],
  "fact_derivations": [{"tag_type": "str", "step_refs": "str", "description": "str"}],
  "complexity": {
    "total_steps": "int",
    "phase_count": "int",
    "boundary_crossing_count": "int",
    "steering_event_count": "int",
    "substep_count": "int",
    "key_line_count": "int"
  },
  "has_process_tree": "bool",
  "has_activity_legend": "bool"
}
```

---

## Phase 1: Deterministic Extraction (Script)

Run the co-located Python script. This is the ONLY step in Phase 1.

```bash
python3 .claude/skills/trace-to-skill-converter/extract-trace-structure.py "<trace-file-path>"
```

The script:
- Validates minimum structure (numbered steps, evidence tags, phase headers)
- Extracts artifacts table, step inventory, phases, process tree, steering events, learnings, fact derivations
- Measures complexity metrics
- Outputs JSON to stdout matching the Intermediate Data Contract above

**If `total_steps` is 0 or the script exits non-zero:** reject the trace with specific guidance on what's missing.

**Save the JSON output** for use in Phase 2. You can pipe to a temp file or hold in context.

---

## Phase 2: Semantic Synthesis (LLM)

Before starting, create TodoWrite tasks to track progress:

```
Tasks:
1. Propose skill name + description
2. Identify hard gates
3. Synthesize process tree (if not extracted)
4. Write step-by-step instructions
5. Derive common mistakes
6. Assemble SKILL.md
7. Run architecture eval (sub-agent)
8. Present draft for review
```

Use the JSON from Phase 1 as your sole input. Do not re-read the trace file.

### 2.1 Propose Skill Name and Description

From `title`, `phases`, and `steps`:
- **Name**: verb-noun pattern (e.g., `writing-traces`, `syncing-skills-with-hub`)
- **Description**: one sentence starting with "Use when..." that covers trigger conditions

### 2.2 Identify Hard Gates

From `steering_events` and `steps`, identify mandatory checkpoints:
- Steps where user confirmation was required
- Steps where wrong assumptions caused rework (from `steering_events`)
- Steps marked with `← HARD GATE` in existing `process_tree.visual_tree`

### 2.3 Synthesize Process Tree (if not extracted)

If `has_process_tree` is false, derive one from `steps` and `phases`:
1. Group steps by phase
2. Identify sequential vs choice vs parallel patterns
3. Build canonical form using van der Aalst operators
4. Build visual tree with activity labels
5. Build activity legend with Node, Actor, Activity, Tool Calls, Trace evidence columns

If `has_process_tree` is true, use the extracted tree directly.

### 2.4 Write Step-by-Step Instructions

Transform trace steps (past tense) into skill steps (imperative):
- Trace: "Agent reads 4 existing skills for pattern recognition"
- Skill: "Read existing skills in the same domain to identify patterns"

Use `steps[].tag_type` and `steps[].body_preview` as source material.

### 2.5 Derive Common Mistakes

From `steering_events` and `learnings`:
- Each steering event becomes a row: | Mistake | Fix | Source |

---

## Phase 3: Assembly + Eval

### 3.1 Assemble SKILL.md

Use this template, filling sections from Phase 2 output:

```markdown
---
name: {{name}}
description: {{description}}
---

# {{Title}}

## Overview

{{1-2 sentence overview derived from trace goal}}

## Hard Gates

{{numbered list from Phase 2.2}}

## Process Tree

### Canonical

\`\`\`
{{canonical from extraction or Phase 2.3}}
\`\`\`

### Visual Tree

\`\`\`
{{visual tree}}
\`\`\`

### Activity Legend

{{table with Node | Actor | Activity | Tool Calls | Trace evidence}}

## Step-by-Step

{{from Phase 2.4}}

## Common Mistakes

| Mistake | Fix | Source |
|---------|-----|--------|
{{from Phase 2.5}}
```

### 3.2 Architecture Evaluation (Sub-Agent)

Delegate to a sub-agent. Do not run inline.

```
Agent(
  subagent_type: "general-purpose",
  prompt: "Run /evaluate-against-architecture-principles on the SKILL.md at
           .claude/skills/{name}/SKILL.md. Return the structured evaluation
           with prioritized findings (Fix Now vs Fix Post-MVP)."
)
```

Incorporate "Fix Now" findings into the draft before presenting to user.

### 3.3 Present Draft (HARD GATE)

**STOP.** Present the assembled SKILL.md and architecture eval summary to the user. Do not write to disk without approval.

### 3.4 Write to Disk

After approval:

1. **Backup if exists**: If `.claude/skills/{name}/SKILL.md` already exists, copy it to `.claude/skills/{name}/SKILL.md.bak` before overwriting.
2. **Write**: Write the approved SKILL.md to `.claude/skills/{name}/SKILL.md`.

---

## Common Mistakes

| Mistake | Fix | Source |
|---------|-----|--------|
| Skipping the extraction script and going straight to writing | Always run `extract-trace-structure.py` first. It prevents hallucinating structure. | L1 from trace |
| Re-reading the trace file during Phase 2 | Use the JSON output from Phase 1. The script already extracted everything mechanical. | Deterministic Offloading principle |
| Omitting the process tree from the generated skill | Every skill needs a process tree with dual representation. Check `has_process_tree` in JSON. | L7 from trace |
| Generating a "complete" skill without user review | Output is always a draft. Present for review before writing to disk. | Q-002 resolution |
| Assuming all traces have activity legends | Only 1/13 traces in the corpus have legends. Check `has_activity_legend` in JSON. | H-001 refutation |
| Writing skill to wrong location | Skill goes in `.claude/skills/{name}/SKILL.md`. Confirm directory before writing. | L3 from trace |
| Running architecture eval inline instead of delegating | Spawn a sub-agent for arch eval. Keeps main context focused on synthesis. | User steering feedback |
| Skipping TodoWrite task creation | Create tasks at start of Phase 2. Makes progress trackable and prevents skipped steps. | User feedback |
| Labeling LLM-executed steps as "deterministic" | A step is deterministic ONLY if a script/tool runs it without LLM involvement. | F-ID from trace step 44 |
