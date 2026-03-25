---
name: evidence-ontology
description: Use at agent/session start, when writing documents with evidence tags and source footnotes, or mid-session when context has drifted and tags need re-grounding. Loads the complete 13-tag Evidence Ontology ([OBS], [M], [F-ID], [F-LK], [E], [H], [A], [C], [O], [G], [Q], [P], [D]) with tag format rules, required properties, valid/invalid examples, strengthening loops, bucket model, and common rationalizations. This skill GROUNDS context. Use verifying-evidence to CHECK artifacts.
---

# Evidence Ontology — Context Grounding

## Purpose

Load the complete Evidence Ontology into agent context so every downstream claim, tag, and derivation is grounded in the canonical rules. This is not a verification pass. This is the reference itself.

**When this skill activates, you have the full ontology. Use it.**

## When to Use

1. **Session/agent start** — Fresh context with design, evidence, or artifact work ahead
2. **Writing mode** — Creating any document that uses evidence tags and source footnotes
3. **Mid-session refresh** — Context has drifted, tags are getting sloppy, or you catch yourself guessing at tag rules. Invoke manually with `/evidence-ontology`.

## Writing Mode Output Structure

When writing design or analysis documents grounded in this ontology, follow the whiteboard template and instructions:

- **Template:** Read `whiteboard-template.md` in the project root for required sections (BID buckets, NBA table, evidence source paths)
- **Instructions:** Read `whiteboard-instruction.md` for section rules, footnote validation, and NBA table maintenance
- **Never overwrite the template itself** — copy it to create a new `{{YYYYMMDD}}-{{change-name}}.md` file
- **NBA table is mandatory** — every open [Q], [A], [H] must appear in the NBA prioritization table ranked by Utility x Cost

## Skill Boundary

| This skill (evidence-ontology) | verifying-evidence |
|---|---|
| LOADS ontology into context | CHECKS artifacts against ontology |
| Use BEFORE writing | Use AFTER writing |
| Reference content — read and internalize | Verification workflow — 4-pass checklist |
| No output artifact | Produces verification report |

---

## Complete Evidence Ontology

The canonical ontology is defined in: [EVIDENCE-ONTOLOGY.md](references/EVIDENCE-ONTOLOGY.md) %% force-extract %%

**Fallback:** If the force-extract link does not resolve, read `references/EVIDENCE-ONTOLOGY.md` in this skill's directory.

---

## Critical Distinctions

These are the most common sources of context rot. Internalize these before writing.

**[OBS] vs [A]:** If you didn't read the specific file:line in THIS codebase, it's [A], not [OBS]. General knowledge about how Node.js or libraries work is [A] unless you verified it in the actual source.

**Secondhand information is [A]:** If someone TOLD you "line 142 uses fetch()", that's [A] until YOU read line 142. Use `[A: reported — not independently verified]` and note the source.

**[F-ID] vs [F-LK]:**
- `[F-ID]` = Structural/logical derivation. Necessarily true given the evidence. P=1.0.
- `[F-LK]` = Empirical-but-frozen fact. Contingently true, treated as fixed for this analysis.
- **Test:** If you could derive it from trace steps alone using logic/math, it's `[F-ID]`. If you'd need to re-measure to confirm it's still true, it's `[F-LK]`.

**[C] vs [D]:** Constraints are things you CANNOT change. If you COULD choose differently, it's a [D]ecision. Test: "Could a different team reasonably make a different choice here?" If yes, it is [D].

**[O] meaning:** [O] is a stable end state, NOT an observation pointer. Must pass three disqualifiers (no from/to language, no condition clauses, no tool/data references). Use [OBS] for observation pointers.

**[H] vs [A] — Default to [H]:** Both express uncertainty, but [H] is a testable claim about reality. [A] is an acknowledged gap. A hypothesis can be wrong; an assumption is honest about not knowing.

**Preference rule:** In Ideal and Delta buckets, default to `[H]` (hypothesis with negate-first strengthen step). Only downgrade to `[A]` when the cost of strengthening exceeds the utility. The goal is falsification: design the first test to disprove the claim, not confirm it.

**Baseline verification rule:** Minimize `[A]` tags in the Baseline bucket. If the agent can verify a claim (read a file, run a command, check a config), do it immediately and tag as `[OBS]` or `[M]`. Assumptions belong in Baseline only when verification is genuinely blocked (e.g., requires access the agent doesn't have, or the user must provide context).

---

## Strengthening Loop

**[H] Hypothesis strengthening via [E] Evidence:**
- [H] starts as a mutable claim about how reality works
- [E] is gathered — an observation + source that directly updates the hypothesis
- Path: `[H] → gather [E] → [F-LK]` (confirmed) or `[H] → gather [E] → revised [H]` (refuted)

**[A] Assumption strengthening via verification:**
- [A] starts as an acknowledged unknown
- Verification (reading code, running commands) produces [OBS] or [M] evidence
- Path: `[A] → verify → [OBS]/[M] → derive [F-ID]` (structural) or `[A] → verify → [M] → [F-LK]` (empirical)

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The tag type is close enough" | Wrong tag = misleading evidence strength. [OBS] vs [A] is the difference between verified and guessed. |
| "Everyone knows how fetch() works" | General knowledge is [A]. Only code you READ in THIS repo is [OBS]. |
| "Context says line 142 uses fetch()" | Secondhand info is [A]. Promote to [OBS] only after you read it yourself. |
| "I'll create a custom tag for this" | The taxonomy is fixed at 13 tags. Use [A] with a source note. |
| "The measurement is approximately right" | [M] requires a reproduction command. "About 94KB" is [A]. `wc -c → 94,231 bytes` is [M]. |
| "The constraint is obvious" | If you could choose differently, it is [D]. Constraints are immutable. |
| "F-ID follows logically" | [F-ID] must reference specific evidence, not appeal to reasoning. |
| "This hypothesis is obviously true" | If it is obviously true, gather [E] and promote it to [F-LK]. Until then, it is still [H]. |
| "No open questions — this is straightforward" | Most artifacts surface unknowns. Zero questions means you stopped looking. |
| "Everything is high priority" | [P] requires relative ranking. If everything is P1, nothing is prioritized. |
| "Time pressure — we need to move on" | A weak artifact makes every downstream artifact wrong. 15 min verification saves hours of rework. |
