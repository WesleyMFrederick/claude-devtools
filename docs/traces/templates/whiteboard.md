# {{change-name}} — Whiteboard

> **Change:** {{change-name}}
> **Domain:** {{domain}}
> **Date:** {{date}}

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

## Original Request

[OBS-001: {{source description}}] [^S-001]
^OBS-001

```
{{verbatim user request}}
```

[G-001: {{synthesized goal statement}}] [^S-001]
^G-001

---

## Artifacts Investigated

<!-- Link every .md file reviewed with markdown links -->
<!-- Use codeblock paths for non-.md files (e.g., `src/foo.ts`) -->
<!-- Group by concern: CLI, Core, Types, Tests, Hooks, etc. -->
<!-- Include specific line ranges for key sections -->
<!-- Include hooks and consumers — they define constraints -->

---

## BI Table — Outcomes

<!-- [O] tags live here, NOT in the buckets. Each row pairs a Baseline outcome
     with its Ideal outcome side-by-side. Untargeted rows repeat Baseline in Ideal.
     Row 0 is the synthesized goal. -->

| # | Baseline [O] | Ideal [O] |
|---|-------------|-----------|
| 0 | {{current state for goal}} | {{target state for goal}} |

---

## Baseline Bucket

### Baseline Metrics
<!-- [M] tags: numerical observations with reproduction commands -->

### Baseline Observations
<!-- [OBS] tags: exact pointers to source reads or command results -->

### Baseline Facts — Identity
<!-- [F-ID] tags: truths by definition, math, or structural logic (P=1.0) -->

### Baseline Facts — Locked
<!-- [F-LK] tags: high-confidence empirical reality frozen for this cycle -->

### Baseline Evidence
<!-- [E] tags: observation + source + link that updates a hypothesis -->

### Baseline Goals
<!-- [G] tags: directional intent explaining why outcomes matter -->

### Baseline Constraints
<!-- [C] tags: non-negotiable boundary conditions -->

### Baseline Hypotheses
<!-- [H] tags: mutable claims requiring validation -->

### Baseline Assumptions
<!-- [A] tags: provisional claims with risk-if-wrong -->

### Baseline Questions
<!-- [Q] tags: labeled uncertainties organizing exploration -->

### Baseline Priorities
<!-- [P] tags: relative importance ordering -->

### Baseline Decisions
<!-- [D] tags: explicit resource commitments with supporting evidence -->

---

## Ideal Bucket

### Ideal Metrics
<!-- [M] tags: target numerical values -->

### Ideal Observations
<!-- [OBS] tags: exact pointers to source reads or command results -->

### Ideal Facts — Identity
<!-- [F-ID] tags: truths by definition, math, or structural logic (P=1.0) -->

### Ideal Facts — Locked
<!-- [F-LK] tags: high-confidence empirical reality frozen for this cycle -->

### Ideal Evidence
<!-- [E] tags: observation + source + link that updates a hypothesis -->

### Ideal Goals
<!-- [G] tags: directional intent explaining why outcomes matter -->

### Ideal Constraints
<!-- [C] tags: non-negotiable boundary conditions -->

### Ideal Hypotheses
<!-- [H] tags: mutable claims requiring validation -->

### Ideal Assumptions
<!-- [A] tags: provisional claims with risk-if-wrong -->

### Ideal Questions
<!-- [Q] tags: labeled uncertainties organizing exploration -->

### Ideal Priorities
<!-- [P] tags: relative importance ordering -->

### Ideal Decisions
<!-- [D] tags: explicit resource commitments with supporting evidence -->

---

## Delta Bucket

### Delta Metrics
<!-- [M] tags: measured change values -->

### Delta Observations
<!-- [OBS] tags: exact pointers to source reads or command results -->

### Delta Facts — Identity
<!-- [F-ID] tags: truths by definition, math, or structural logic (P=1.0) -->

### Delta Facts — Locked
<!-- [F-LK] tags: high-confidence empirical reality frozen for this cycle -->

### Delta Evidence
<!-- [E] tags: observation + source + link that updates a hypothesis -->

### Delta Goals
<!-- [G] tags: directional intent explaining why outcomes matter -->

### Delta Constraints
<!-- [C] tags: non-negotiable boundary conditions -->

### Delta Hypotheses
<!-- [H] tags: mutable claims requiring validation -->

### Delta Assumptions
<!-- [A] tags: provisional claims with risk-if-wrong -->

### Delta Questions
<!-- [Q] tags: labeled uncertainties organizing exploration -->

### Delta Priorities
<!-- [P] tags: relative importance ordering -->

### Delta Decisions
<!-- [D] tags: explicit resource commitments with supporting evidence -->

---

## Next Best Actions Prioritization Table

<!-- After populating all buckets, collect every open [Q], [A], [H] tag and rank by Utility x Cost. -->
<!-- Link each item to its block anchor using [TAG-NNN](#^TAG-NNN) format. -->
<!-- After resolving any item, run /nba-table-promotion to apply gold standard formatting. -->

### Tier 1 — High utility, blocks design

| # | Item | Utility | Cost | DRI | Status |
|---|------|---------|------|-----|--------|
| 1 | [TAG-NNN](#^TAG-NNN) (short description) | High | Low | Agent | Open |

### Tier 2 — Medium utility, informs schema decisions

| # | Item | Utility | Cost | DRI | Status |
|---|------|---------|------|-----|--------|
| 2 | [TAG-NNN](#^TAG-NNN) (short description) | Medium | Low | Agent | Open |

### Tier 3 — Low utility, defer

| # | Item | Utility | Cost | DRI | Status |
|---|------|---------|------|-----|--------|
| 3 | [TAG-NNN](#^TAG-NNN) (short description) | Low | Low | Agent | Open |

> [!info]- Resolved (0)
>
> _(none yet)_

---

## Evidence Source Paths
