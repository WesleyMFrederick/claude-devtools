# UNIVERSAL DECISION ONTOLOGY + BUCKET MODEL (ONE-SHEET)

This sheet is designed to work for **any entry point**:

- Case interviews
- Product strategy
- Hackathons
- Feature design
- Transformation programs
- Research planning

Clients may bring:

- Baseline problem
- Ideal vision
- Delta solution
- Metrics gap
- Constraints
- Or any combination

Therefore we separate:

1. **Ontology (atomic thinking units)**
2. **Buckets (state organization: Baseline / Ideal / Delta)**

Any ontology element can live in any bucket.

---

## Tag Format Rule

**Every tag MUST use the format: `[TAG: short-display]`**

- The tag type and content are a single bracketed unit with a colon separator
- Examples: `[OBS: file:line → result]`, `[Q: what is unknown?]`, `[G: reduce costs]`
- **Never:** `[TAG] bare text after bracket` — the colon and display content must be inside the brackets
- **[Q], [A], and [H] additionally require** two follow-up lines:
  - **Strengthen:** how to test/verify this
  - **Utility:** what decision this unlocks

---

## Ontology Tag Types Table

|**Tag**|**Requires**|**Valid Source Examples**|**Invalid Source Examples**|
|---|---|---|---|
|**[OBS] Observation**|Exact pointer for a Simple Read, OR Reproduction Command + Result with explicit boundary crossings.|**Simple Reads:**<br>• `[OBS: src/auth.ts:12-15 → token expires in 1h]`<br>• `[OBS: system-prompt.md:42 → "always output JSON"]`<br>• `[OBS: Stripe API Docs, Auth Section, Line 3 → "Bearer token required"]`<br><br>**Executions:**<br>• `[OBS: HOOK → CLI: node extract.js → "Parsed 3 anchors"]`<br>• `[OBS: git remote -v → "origin-local"]`|`[OBS: Context says it outputs JSON]`_(Secondhand)_<br><br>`[OBS: it failed]` _(Not a literal result)_|
|**[F-ID] Identity Fact**|Truth by definition, math, or structural logic (Probability = 1.0).|• `[F-ID: Profit = Revenue - Cost]`<br>• `[F-ID: Total Latency = Net + App + DB]`<br>• `[F-ID: Time Spent (Path A) = Time Lost (Alternative Paths)]`|`[F-ID: AWS costs are too high]`_(Assumption)_|
|**[F-LK] Locked Fact**|High-confidence empirical reality frozen for the current decision cycle.|• `[F-LK: Q3 Revenue (via NetSuite Q3 Close) = $4.2M]`<br>• `[F-LK: Current DB size (RDS Metrics) = 4TB]`|`[F-LK: We will reach $5M next quarter]`_(Hypothesis)_|
|**[M] Metric**|A numerical observation. Follows the exact same rules as `[OBS]`: precise pointer OR command + result.|**Simple Reads:**<br>• `[M: package.json:14 → "jest": "^29.5.0"]`<br>• `[M: Github API Docs, Rate Limits → 5000/hr]`<br><br>**Executions:**<br>• `[M: wc -c logs.txt → 94KB]`<br>• `[M: DB_READ → SELECT count(*) FROM users → 14,230]`|`[M: about 94KB]`_(Estimation)_<br><br>`[M: Customer Acquisition Cost]` _(No pointer)_|
|**[E] Evidence**|An observation (`[OBS]` or `[M]`) + Source + Link that updates a Hypothesis.|• `[E: [OBS] (Mixpanel drop-off @ step 2) supports [H] (UX confusing)]`<br>• `[E: [M] (DB CPU 99%) refutes [H] (Network bottleneck)]`|`[E: The marketing campaign failed]`_(Missing observation link)_|
|**[H] Hypothesis**|A mutable claim about reality requiring validation (Probability 0–1)._Must include strengthening steps & utility._|• `[H: Adding Redis will cut latency by 50%]`<br>• `[H: Free trial will increase top-of-funnel by 20%]`|`[H: Profit = Revenue - Cost]` _(Identity Fact)_|
|**[A] Assumption**|Provisional claim to unblock progress. **If wrong, it introduces risk to any other decisions built upon it.**_Must include strengthening steps & utility._|• `[A: Users understand the 'Archive' icon]`<br>• `[A: Legacy API behaves identically to v2]`|`[A: wc -l src/index.ts → 142]` _(Observation)_|
|**[C] Constraint**|Non-negotiable boundary condition that limits the solution space.|• `[C: SOC2 compliance required per Legal (Ticket #92)]`<br>• `[C: jq required by hook]`|`[C: We should use GraphQL]` _(Decision)_|
|**[O] Outcome**|A stable, end state a person or system inhabits — independent of how it was built, what came before, or what enables it. _(No from/to language, no condition clauses, no tool/data references)._|• `[O: Regulators can identify top-emitting vessels in their jurisdiction]`<br>• `[O: Analysts can explain and defend any emissions estimate to external auditors]`|`[O: Build an emissions dashboard]`_(Feature)_<br><br>`[O: Move compliance teams from manual to automated]`_(Delta/Transition)_<br><br>`[O: Increase model accuracy to 85%]`_(Key Result / Metric)_|
|**[G] Goal**|Directional intent or strategic motivation explaining _why_outcomes matter.|• `[G: Reduce infrastructure costs]`<br>• `[G: Expand to enterprise market]`|`[G: Cost per click]`_(Metric)_|
|**[Q] Question**|A labeled uncertainty organizing exploration and evidence collection._Must include strengthening steps & utility._|• `[Q: Why did churn spike in March?]`<br>• `[Q: header/extract same path?]`|`[Q: API response is 400ms]` _(Observation)_|
|**[P] Priority**|Relative importance or ordering of questions, goals, or hypotheses.|• `[P: Reliability > Feature Velocity]`<br>• `[P: Resolving Q1 is required before Q2]`|`[P: We need to fix the bug]` _(Goal/Decision)_|
|**[D] Decision**|Explicit resource commitment or allocation among options. Commits [F-Rule: Time] or budget.|• `[D: Path-Primary] Grow by acquiring new accounts`<br>• `[D: use --verbose flag]`|`[D: SOC2 compliance required]` _(Constraint)_<br><br>`[D: The API returns JSON]` _(Observation)_|

---

## PART 1 — ONTOLOGY (GENERIC ATOMIC ELEMENTS)

These are the primitive building blocks of reasoning.

They are **bucket-agnostic**.

---

### OBS — Observation

Definition:
A direct empirical reading. Requires an exact pointer for a Simple Read, OR a Reproduction Command + Result with explicit boundary crossings.

Examples:
- `src/auth.ts:12-15 → token expires in 1h`
- `system-prompt.md:42 → "always output JSON"`
- `CLI: node extract.js → "Parsed 3 anchors"`

Properties:
- Literal result (not a summary like "it failed")
- Objective and reproducible
- Verifiably linked to a precise source

Use:
The fundamental grounding for metrics and evidence.

---

### F-ID — Identity Fact

Definition:
True by definition, math, or logic. Cannot change.

Examples:
- Profit = Revenue − Cost
- Emissions = Activity × Emission Factor
- Total Latency = Net + App + DB

Properties:
- Probability = 1.0
- Immutable
- Structural relationships

Use:
Provides reasoning scaffolding.

---

### F-LK — Locked Fact

Definition:
Empirical fact treated as true for this decision cycle.

Examples:
- Current revenue (via NetSuite Q3) = $200M
- Approval time = 10 days
- Current DB size (RDS Metrics) = 4TB

Properties:
- High confidence
- Frozen during analysis
- May update later with evidence

Use:
Defines baseline reality.

---

### M — Metric

Definition:
A quantitative measurement used to evaluate outcomes or hypotheses. Follows the exact same rules as an Observation: it must include a precise pointer OR a command + result.

Examples:
- `wc -c logs.txt → 94KB`
- `Github API Docs, Rate Limits → 5000/hr`
- `DB_READ → SELECT count(*) FROM users → 14,230`

Properties:
- Observable and trackable
- Requires precise source pointer

Use:
Decision grounding and validation.

---

### E — Evidence

Definition:
An observation (`OBS` or `M`) + Source + Link that updates a Hypothesis.

Examples:
- `[M] (DB CPU 99%)` refutes `[H] (Network bottleneck)`
- `[OBS] (Mixpanel drop-off @ step 2)` supports `[H] (UX confusing)`

Properties:
- Has weight of evidence
- Updates hypothesis probability

Use:
Learning and validation.

---

### H — Hypothesis

Definition:
A claim about reality with uncertain truth value.

Examples:
- Adding Redis will cut latency by 50%
- Free trial will increase top-of-funnel by 20%
- Transparency will change regulator behavior

Properties:
- Probability 0–1
- Mutable
- Requires evidence

Two Required Questions:
1. What steps would strengthen or test this hypothesis?
2. What decision utility does this validation provide?

Use:
Drives exploration and testing.

---

### A — Assumption

Definition:
A provisional claim adopted to unblock progress when evidence is missing.

Key Property:
If wrong, downstream work may collapse. Introduces risk to any decisions built upon it.

Examples:
- Users will understand the 'Archive' icon
- Legacy API behaves identically to v2
- Integration cost is manageable

Two Required Questions:
1. What would strengthen confidence in this assumption?
2. What decision utility would that stronger confidence provide?

Use:
Risk surface mapping.

---

### C — Constraint

Definition:
A boundary condition that limits feasible solutions. Usually derived from F-ID or F-LK but elevated to decision importance.

Examples:
- SOC2 compliance required per Legal (Ticket #92)
- Budget ≤ $5M
- `jq` required by hook

Properties:
- Non-negotiable within scope

Use:
Prunes solution space.

---

### O — Outcome

<mark class="user-highlight" data-user-name="Wesley" data-created="2026-03-02 07:45">not so much stable, but a Job To Be Done kind of statement that ties to a person's (entity, or group of people) ultimate motivation. When outcome is in the ideal bucket, it is usually some kind of comparison *-er, like "Regulators can identify top-emitting vessels in their jurisdiction **better | quicker**, etc. This is what gets is to comparing the baseline outcome to the ideal outcome to get the key result metrics. This kind of conflicts with the From/To language. We want outcomes in baseline and outcomes in ideal (expressed with that *er extra if the change is impacting the outcome). the delta then becomes how we design the change that creates the impact on a person (group's) outcomes. 

**OUTCOMES SPEAK TO A PERSON OR GROUP OF PERSON'S MOTIVATIONS**</mark>

Definition:
A stable, end state a person or system inhabits — independent of how it was built, what came before, or what enables it.

The actor can do X. Full stop.

Patterns ✓

| Example | Why It Works |
|---------|-------------|
| "Regulators can identify top-emitting vessels in their jurisdiction" | Stable capability, actor-owned, tool-agnostic |
| "Port authorities can demonstrate emissions accountability to policymakers" | End state, falsifiable, no implementation dependency |
| "Analysts can explain and defend any emissions estimate to external auditors" | Durable — holds regardless of model or vendor |

Anti-Patterns ✗

| Example | What It Actually Is |
|---------|-------------------|
| "Build an emissions dashboard" | Output / feature |
| "Improve AIS data coverage" | Enabler / assumption / hypothesis on effect of change on ideal outcome |
| "Move compliance teams from manual assembly to prioritized action" | Delta — describes a transition, not a state |
| "Estimates remain auditable even when AIS data is incomplete" | Constraint / design requirement |
| "Increase model accuracy to 85%" | Key result / metric |
| "Regulators understand the tool" | Activity / vague intent |

The Three Disqualifiers — strip the outcome if it contains any:
1. **From/to language** — describes a transition, not a state
2. **Condition clauses** — even when, as long as, provided that
3. **Tool or data references** — via AIS, through the dashboard, using the model

If any appear, you're one level too low. The real outcome is above it.

Properties:
- External manifestation of success

Use:
Target state definition.

---

### G — Goal

Definition:
Directional intent or strategic motivation explaining _why_ outcomes matter.

Examples:
- Reduce infrastructure costs
- Expand to enterprise market
- Improve transparency

Properties:
- Strategic orientation
- May be qualitative

Use:
Explains _why_ outcomes matter.

---

### Q — Question

Definition:
A labeled uncertainty organizing exploration and evidence collection. Not a primitive claim — a pointer to missing knowledge.

Examples:
- Why did churn spike in March?
- Will regulators trust model outputs?
- Do the header and extract use the same path?

Properties:
- Organizes exploration
- Guides evidence collection

Two Required Questions:
1. What are the verification/strengthening steps?
2. What is the utility of answering this?

Use:
Focuses analysis and testing.

---

### P — Priority (Optional)

Definition:
Relative importance or ordering of questions, goals, or hypotheses.

Examples:
- Reliability > Feature Velocity
- Resolving Q1 is required before Q2
- Risk reduction highest priority

Use:
Decision alignment and tradeoffs.

---

### D — Decision

Definition:
Explicit resource commitment or allocation among options. Commits time or budget.

Examples:
- Path-Primary: Grow by acquiring new accounts
- Use the `--verbose` flag

Properties:
- Resolves options into action
- Consumes resources

Use:
Records chosen paths and boundary commitments.

---

## PART 2 — BUCKETS (STATE ORGANIZATION)

Buckets represent **system states**, not ontology types. Any ontology element can exist in any bucket.

### BASELINE BUCKET — Current State

Definition:
The system as it exists today.

Key Question:
> Where are we now?

Purpose:
Understand reality and constraints before change.

### IDEAL BUCKET — Target State

Definition:
The future system if everything worked perfectly.

Key Question:
> If success were fully achieved, what would the world look like?

Purpose:
Define evaluation criteria for solutions.

### DELTA BUCKET — Transformation Path

Definition:
Candidate ways to move from baseline to ideal.

Key Question:
> What changes could move us toward the ideal?

Purpose:
Decision and planning.

---

# PART 3 — ENTRY POINT ADAPTATION

Clients may start anywhere:

| Client Entry | First Action |
|-------------|-------------|
| Baseline problem | Map BASELINE → infer IDEAL |
| Ideal vision | Clarify IDEAL → map BASELINE |
| Solution idea | Treat as DELTA H → reconstruct IDEAL + BASELINE |
| Metrics gap | Map METRICS → infer IDEAL |
| Constraints | Map CONSTRAINTS → define feasible IDEAL |
| Mixed | Decompose into ontology → bucket |

Core Rule:

> Always reconstruct all three buckets before deciding.

---

# PART 4 — ASSUMPTION & HYPOTHESIS STRENGTHENING LOOP

For any **H** or **A**, ask:

1. What evidence would strengthen confidence?
2. What decision utility would that stronger confidence create?

This ensures effort targets decisions, not curiosity.

---

# PART 5 — UNIVERSAL FLOW

1. Decompose prompt into ontology elements
2. Place elements into buckets (Baseline / Ideal / Delta)
3. Identify gaps (Q)
4. Evaluate deltas against constraints and outcomes
5. Decide next action or recommendation

---
