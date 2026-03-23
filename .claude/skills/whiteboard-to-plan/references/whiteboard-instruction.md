# Whiteboard Instruction

Create the whiteboard — the scratchpad that organizes research and user
feedback into Baseline, Ideal, and Delta buckets.

This is a PARSING step, not a deep-dive. Research the codebase, gather
user feedback, and sort everything into three buckets. Do not go deep
on any bucket — that happens in the baseline and ideal artifacts.

## Evidence Ontology

<CRITICAL>
Before tagging ANY claims, insert the live evidence glossary extract into
the Evidence Glossary section:

![Ontology Tag Types Table](../../../../EVIDENCE-ONTOLOGY.md#Ontology%20Tag%20Types%20Table)%% force-extract %%

Follow the Requires column and Invalid Source Examples for each tag.

Rules:
1. No untagged claims. No tags without their required properties.
2. Every tag MUST use the format: [TAG-NNN: short-display] [^S-NNN]
   - Number items sequentially per tag type: OBS-001, OBS-002, G-001, etc.
   - Tag + footnote ref + description + block anchor all on ONE line
   - Source detail lives in [^S-NNN] footnotes — keep tag display SHORT
   Example: `1. [OBS-001: schema.yaml] [^S-002] my-workflow has 6 artifacts ^OBS-001`
3. [Q], [A], and [H] additionally require two follow-up lines:
   - Strengthen: how to test/verify this
   - Utility: what decision this unlocks
4. Items within each section are NUMBERED LISTS — no blank lines between items
5. Resolved items use STRIKETHROUGH: ~~[Q: resolved question]~~
</CRITICAL>

## Footnote Validation

After writing all claims, run the `artifact-validate-claim-create-footnotes`
skill to validate every [^S-NNN] footnote against its source file. No
footnote without verified source. No abbreviated paths.

## Required Sections

- **Original Request**: Tag the user request source as [OBS-001: source description] [^S-001]
  with block anchor ^OBS-001. Tag the synthesized goal as [G-001: goal statement] [^S-001]
  with block anchor ^G-001. Include verbatim user request in a code block (``` not blockquote).

- **Evidence Glossary**: Live extract from EVIDENCE-ONTOLOGY.md (inserted above).

- **Artifacts Investigated**: Files reviewed, grouped by concern (not by type).
  Use markdown links for .md files with :line-range. Use codeblock paths for
  non-.md files. Include hooks and consumers — they define constraints.

- **Baseline Bucket**: What we know about how the system works today.
  Sub-sections: Observations, Questions, Facts-Locked.
  High-level observations, pointers to code, initial measurements.

- **Ideal Bucket**: What the user wants. Target behavior, goals, mockups.
  Sub-sections: Observations, Constraints, Assumptions, Questions, Decisions.
  Capture user intent, not implementation.

- **Delta Bucket**: Initial notes on what changes. Placeholder — cannot be
  completed until baseline and ideal are done.
  Sub-sections: Potential Decisions, Hypotheses, Questions.

- **Evidence Source Paths**: Footnote block at document bottom. Every source
  referenced by [^S-NNN] gets one line:
  [^S-NNN]: `full/absolute/path:line-range`

Place [Q] items in the bucket they relate to — not in a separate section.
A question about current system behavior goes in Baseline. A question about
target behavior goes in Ideal. A question about scope of change goes in Delta.

<CRITICAL>
**AFTER CREATING ARTIFACT** - Run /artifact-validate-claim-create-footnotes skill
</CRITICAL>

## Next Best Actions Prioritization Table Maintenance

After resolving any Q/H/A item in the Next Best Actions prioritization table,
run `/nba-table-promotion` to apply gold standard formatting. The skill's
co-located script deterministically applies strikethrough, bold status, and
linked evidence anchors to answered rows.