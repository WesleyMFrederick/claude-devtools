# Evidence Ontology Skill — Kick-off / Continue Prompt

Use this prompt to start or resume work on the evidence-ontology skill.

## Kick-off Prompt

```
I'm building an evidence-ontology skill for this project. The whiteboard has the full decomposition and decisions.

Read the whiteboard first:
- 20260322-evidence-ontology-skill.md — all BID buckets, resolved decisions, NBA table, and phase tracking

Then read the current deliverables:
- .claude/skills/evidence-ontology/SKILL.md — the skill (force-extract from EVIDENCE-ONTOLOGY.md)
- .claude/settings.json — hooks (SessionStart, SubagentStart, compact)
- CLAUDE.md — evidence discipline directive

Definition of done: Skill gives complete ontology during:
1. AGENT start (SessionStart, subagent start, etc) — via hooks in .claude/settings.json
2. Writing documents with evidence tags and source footnotes — via skill auto-load + CLAUDE.md directive
3. Mid-session when context rot sneaks in — via compact hook + manual /evidence-ontology

Key decisions already locked (see whiteboard for evidence):
- D-002: This skill GROUNDS, verifying-evidence CHECKS
- D-007: Use force-extract link to EVIDENCE-ONTOLOGY.md, not inline
- D-008: Mid-session manual trigger via /evidence-ontology
- D-011: SessionStart hook cats EVIDENCE-ONTOLOGY.md for deterministic injection
- D-012: Hooks in .claude/settings.json (not skill frontmatter)
- C-008: Agent start must be deterministic via hooks

Check the whiteboard phases section for current phase and what's next.
Do not overwrite the whiteboard template structure (C-005, C-006).
Every user steer must be captured as a whiteboard constraint (C-007).
Iterate on NBA items until definition of done is achieved.
```

## Continue Prompt (After Compact or New Session)

```
Resuming evidence-ontology skill work. Read 20260322-evidence-ontology-skill.md to restore state.
Check the Phases section for current phase and NBA table for open items.
The whiteboard has all decisions, evidence, and source paths.
```
