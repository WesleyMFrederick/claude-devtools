---
name: writing-traces
description: Use when tracing how a system, format, or workflow works today - provides trace format, process tree definitions, hard gates for trace subject confirmation, and a mandatory gold standard reference. Applies to baseline investigations, debugging, and any "how does this work now" analysis.
---

# Writing Traces

## Overview

Traces record the factual state of how a system works through literal execution records and optionally process trees (abstracted workflow models). Use this skill whenever you need to trace "how does this work now" — whether for OpenSpec baselines, debugging investigations, or any current-state analysis. 

### CRITICAL REQUIREMENT
- **READ** `reference/evidence-ontology-one-page.md` for evidence tag rules


## Hard Gates

These are mandatory checkpoints. Do NOT proceed past them without user confirmation.

1. **Trace Subject Confirmation**: Before reading source files or writing trace content, STOP and ask the user: "What system/format should I trace?" Present candidates from the whiteboard (or context) and let the user choose. Do not speculatively read source files in parallel.

2. **Gold Standard Review**: Before writing your first trace step, you MUST read the Gold Standard Trace section below. Match its format exactly — numbered steps, evidence tags, boundary crossings, sub-steps, key line callouts.

## Large Transcript Handling

When the trace subject is a session transcript that exceeds the Read tool's line limit:

1. Use the `searching-transcripts` skill to search and extract segments from the JSONL file
2. Use `--dir` to point at the transcript's directory or the JSONL file directly
3. Use `--from` / `--to` with `--full` to extract bounded segments for detailed tracing

## Key Definitions

**Trace** = Literal execution record. This is the **evidence layer**. Each step is numbered and tagged with `[OBS: file:line]` or `[M: command → result]`. Boundary crossings between components are explicit (e.g., `HOOK → CLI`, `RETURN ←──`). A trace records what ACTUALLY HAPPENED in a specific execution path.

**Process Tree** = Abstracted workflow model derived FROM traces. This is the **derivation layer**, tagged with `[F-LK]`. Uses operators (→ sequential, × exclusive choice, ∧ parallel, ↻ redo loop) to describe POSSIBLE paths — not a single execution. Every branch must reference the trace step(s) that evidence it.

**Write traces first. Derive process trees from them.** You cannot model structure until you have recorded evidence. A trace document may have only traces if the workflow is purely linear.

## Process Tree Notation

Based on van der Aalst §3.2.8, *Process Mining: Data Science in Action*. Adapted for readability.

### Operators

| Symbol | Name | Meaning | Children |
|--------|------|---------|----------|
| `→` | sequential | execute children left-to-right | 1+ |
| `×` | exclusive choice | execute exactly ONE child | 2+ |
| `∧` | parallel | execute ALL children in any order | 2+ |
| `↻` | redo loop | first child is "do", rest are "redo" options | 2+ |
| `τ` | silent activity | invisible/skip — no observable output | leaf |

### τ Patterns

| Pattern | Meaning |
|---------|---------|
| `×(a, τ)` | activity `a` can be skipped |
| `↻(a, τ)` | execute `a` one or more times (silent redo) |
| `↻(τ, a)` | execute `a` zero or more times (silent do) |

### Dual Representation

Every process tree has TWO forms. Both must appear in trace documents.

**1. Canonical inline (source of truth, parseable):**
```
→(a, b, ×(c, →(×(d, e, f), g, h, ×(i, τ))))
```

**2. Visual tree (reading aid):**
```
→ workflow-name
├── [a] first activity
├── [b] second activity
└── × choice-name
    ├── [c] IF condition-1: outcome
    └── → sequence-name
        ├── × inner-choice
        │   ├── [d] IF condition-2: outcome
        │   ├── [e] IF condition-3: outcome
        │   └── [f] IF condition-4: outcome
        ├── [g] next activity                        ← HARD GATE
        ├── [h] final activity
        └── × optional
            ├── [i] optional activity
            └── [τ] (skip)
```

### Visual Tree Rules

- **Root line**: `operator workflow-name` — operator governs children, name is a label
- **Operator lines**: `operator group-name` — appear at group/parent level, govern their children
- **Leaf lines**: `[letter] activity description` — no operator needed, indent under parent
- **IF prefix**: use on `×` children to make choice conditions explicit
- **Annotations**: `← HARD GATE`, `← do part`, `← redo part` for semantics not visible in structure
- **Indentation** = depth in the tree
- **Activity legend table** follows the tree — maps each `[letter]` to concrete activity + trace evidence

### Gold Standard Process Tree

From skill-sync-trace workflow:

**Canonical:**
```
→(a, b, ×(c, →(×(d, e, f), g, h, ×(i, τ))))
```

**Visual tree:**
```
→ skill-sync-workflow
├── [a] user requests skill sync
├── [b] diff consumer vs hub
└── × classification
    ├── [c] IF identical: report "in sync"
    └── → needs-sync
        ├── × direction
        │   ├── [d] IF hub-newer: recommend pull
        │   ├── [e] IF consumer-newer: recommend push
        │   └── [f] IF diverged: show diff, recommend merge
        ├── [g] user decides + approves              ← HARD GATE
        ├── [h] copy + commit destination
        └── × optional-push
            ├── [i] push hub to origin
            └── [τ] (skip)
```

**Activity legend:**

| Node | Activity | Trace evidence |
|------|----------|---------------|
| [a] | user names skill to sync | steps 1, 6 |
| [b] | `diff` consumer vs hub SKILL.md | steps 3, 7 |
| [c] | IF identical: report "in sync" | not observed |
| [d] | IF hub-newer: show diff + recommend pull | step 3 |
| [e] | IF consumer-newer: show diff + recommend push | step 7 |
| [f] | IF diverged: show diff + recommend merge | not observed |
| [g] | user decides direction + confirms | steps 4, 8 |
| [h] | `cp` in chosen direction + `git commit` | steps 4-5, 8-9 |
| [i] | `git push origin main` | step 13 |

## Gold Standard Trace

This is the mandatory format reference. Every trace you write must match this structure.

### What Makes a Trace Sound

1. **Artifacts section** comes first — lists every source file, transcript, or artifact needed to replay the trace
2. **Every step has an evidence tag** with file:line
3. **Boundary crossings** are explicit (HOOK → CLI → RETURN)
4. **Sub-steps** (6a-6e) model what happens inside the called component
5. **Key lines** are called out where the interesting behavior lives
6. **Fact derivations** cite specific step numbers they derive from

### Artifacts Section (mandatory, before trace body)

Every trace document must open with an Artifacts table. Include only what is needed to **locate and re-read** the evidence — no detail that belongs in the trace itself.

```markdown
## Artifacts

| Artifact | Path | Role |
|----------|------|------|
| CLI Command | `src/cli/extract-schema.ts` | Entry point traced |
| Session transcript | `claude-code-transcripts/abc123.jsonl` | Primary evidence source |
| Plan file | `.claude/plans/my-plan.md` | Artifact being evaluated |
```

Rules:
- Path must be absolute or repo-relative — enough to open the file without searching
- Role is one phrase: what this artifact contributes to the trace
- Do NOT duplicate content from the artifact — just point to it

### Full 14-Step Reference Trace

~~~text
TRACE: extractor hook (PostToolUse:Read)
══════════════════════════════════════════

 HOOK TRIGGER
 ─────────────
 1. [C: Claude Code runtime]
    Event: PostToolUse:Read fires
    Matcher: "Read" → extractor.sh

 HOOK: GUARDS
 ────────────
 2. [OBS: extractor.sh:27-30]
    Guard: jq available?
    FAIL → exit 0 (silent skip)

 3. [OBS: extractor.sh:34-45]
    Resolve: jact binary
    Try: local build (dist/jact.js)
    Fallback: global CLI
    FAIL → exit 0 (silent skip)

 4. [OBS: extractor.sh:56-63]
    Parse: stdin JSON from Claude Code
    Extract: file_path, session_id
    FAIL (no file_path) → exit 0

 5. [OBS: extractor.sh:77-80]
    Guard: file_path ends in .md?
    FAIL → exit 0 (silent skip)

 HOOK → CLI (boundary crossing)
 ──────────────────────────────
 6. [OBS: extractor.sh:92]
    CALL ──→ jact extract links "$file_path" --session "$session_id"
    │
    │  CLI: PARSE ARGS
    │  ────────────────
    │  6a. [OBS: jact.ts:1131-1291]
    │      Commander.js parses: extract links <file> --session <id>
    │
    │  CLI: ORCHESTRATE
    │  ────────────────
    │  6b. [OBS: jact.ts:429-480]
    │      extractLinks() → validate links → extract content
    │
    │  CLI: EXTRACT + DEDUPLICATE
    │  ──────────────────────────
    │  6c. [OBS: ContentExtractor.ts:88-235]
    │      Strategy chain → content extraction → SHA-256 dedup
    │
    │  CLI: OUTPUT
    │  ───────────
    │  6d. [OBS: jact.ts:466]
    │      console.log(JSON.stringify(result, null, 2))
    │      ├── extractedContentBlocks  (50KB)  [M]
    │      ├── outgoingLinksReport     (44KB)  [M]
    │      └── stats                   (124B)  [M]
    │      TOTAL: 94KB to stdout               [M]
    │
    │  6e. [OBS: jact.ts:exit codes]
    │      Exit: 0 (success) | 1 (no content) | 2 (error)
    │
    RETURN ←── stdout (94KB JSON) + exit code
    │

 HOOK: PROCESS CLI OUTPUT
 ────────────────────────
 7. [OBS: extractor.sh:93]
    Capture: exit code from CLI

 8. [OBS: extractor.sh:97-106]
    Branch on exit code:
    ├── 0 + empty output → exit 0 (cache hit, already extracted)
    ├── 1             → exit 0 (no citations found)
    └── 2 or empty    → exit 0 (error, silent)

 9. [OBS: extractor.sh:109]                         ← KEY LINE
    Parse: jq '.extractedContentBlocks'
    USES:    50KB (content blocks)
    DISCARDS: 44KB (outgoingLinksReport) + 124B (stats)
    WASTE:   46% of received data                  [M: 44KB / 94KB]

10. [OBS: extractor.sh:112-116]
    Guard: extracted content not null/empty?
    FAIL → exit 0

11. [OBS: extractor.sh:121]                         ← KEY LINE
    Transform: jq maps content blocks →
    "## Citation: <contentId>\n\n<content>\n---"

    INPUT FORMAT:  JSON (extractedContentBlocks object)
    OUTPUT FORMAT: markdown text (flat string)

 HOOK: EMIT RESULT
 ─────────────────
12. [OBS: extractor.sh:132-139]
    Wrap: jq builds hookSpecificOutput JSON envelope
    {
      "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": "<formatted markdown>"
      }
    }

13. [OBS: extractor.sh:141]
    Output: JSON to stdout → Claude Code injects as additionalContext

14. [OBS: extractor.sh:144]
    Exit: 0 (always non-blocking)

══════════════════════════════════════════
END TRACE
~~~

### Fact Derivations From This Trace

These show how sound derived facts cite specific steps:

1. **[F-LK: from steps 6d + 9]** The hook receives 94KB but uses only 50KB. The 44KB (46%) is **pipe waste, not context waste** — the CLI serializes it, the pipe transmits it, and the hook immediately discards it via `jq '.extractedContentBlocks'`. Claude never sees the `outgoingLinksReport`.

2. **[F-LK: from steps 9 + 11]** The hook performs two format transformations: JSON → extracted blocks (jq) → markdown text (jq). The final output to Claude is markdown, not JSON.

3. **[F-LK: from step 6d]** The CLI's `console.log(JSON.stringify(result, null, 2))` is the single output point. Any change to default output format affects ALL consumers simultaneously.

4. **[F-ID: from steps 2-5]** The hook has 4 guard clauses that exit silently (exit 0). Any of these failing means no content injection.

### Why Each Fact Is Sound

| Fact | Cites | Derivation is valid because |
|------|-------|---------------------------|
| #1 [F-LK] | steps 6d + 9 | 6d measures total output (94KB); 9 shows jq filter discards report (44KB). Math checks out. |
| #2 [F-LK] | steps 9 + 11 | 9 shows jq extracts JSON blocks; 11 shows jq maps to markdown. Two transformations, verified. |
| #3 [F-LK] | step 6d | 6d shows single `console.log` call. One output point = all consumers get same format. |
| #4 [F-ID] | steps 2-5 | Four sequential guards, each with `exit 0` on failure. Count matches. |

## Trace-Specific Red Flags — STOP and Fix

- Process tree with untagged steps
- "Trace" that uses → × ∧ ↻ operators instead of numbered [OBS]/[M]-tagged steps (this is a process tree mislabeled as a trace)
- Process tree with no [F-LK]/[F-ID] references back to trace steps
