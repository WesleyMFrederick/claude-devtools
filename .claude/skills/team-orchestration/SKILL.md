---
name: team-orchestration
description: Use when coordinating multiple persistent agents via TeamCreate for implementation tasks with code review - provides the complete workflow for team creation, task decomposition with dependencies, message-driven routing, fix loops, and shutdown sequence while enforcing pure delegation where orchestrator never does implementation work
---

# Team Orchestration

## Overview

Coordinate persistent agents via TeamCreate + SendMessage for implementation tasks with code review and delegated commits.

**Core principle:** Orchestrator is a pure dispatcher — creates team, creates tasks, spawns agents, routes messages, reports results. ALL implementation work (coding, reviewing, committing, investigating) is delegated to agents.

**vs. other execution skills:**
- **subagent-driven-development** — Fresh subagent per task, same session, no persistent agents
- **executing-plans** — Batch execution with human review checkpoints
- **team-orchestration** (this) — Coordinated agents (fresh or persistent), message-driven routing

## Agent Model: Fresh vs Persistent

**Default: Fresh-agent-per-task** — Spawn a new agent for each task. Agent gets one job, shuts down when done. Use this when:
- User says "fresh context per task" or tasks are independent
- impl / review / commit are separate isolated jobs

**Persistent agents** — Spawn once, loop over task list. Use only when agents need stateful memory across steps or explicit inter-agent communication mid-task.

**REQUIRED: Every fresh-agent prompt MUST end with:**
```
Shut yourself down when done — do not stay idle.
```
Omitting this causes idle pane accumulation and hits the tmux hard limit.

## Concurrency Limit (HARD RULE)

**Max 2-3 concurrent agents at any time.** tmux has a hard pane limit (~8-10 active panes). Exceeding it causes silent `no space for new pane` failures.

- Before spawning a batch: count active (running + idle) agents
- If at limit: wait for shutdown confirmations before spawning more
- Send `shutdown_request` to idle agents immediately after they report done — do not wait

## When to Use

- User says "use a team" or "spawn agents" or "coordinate agents"
- Task needs agents that communicate with each other (coder ↔ reviewer)
- Multiple specialized roles needed (coder, reviewer, committer)
- Want message-driven coordination rather than subagent dispatch-and-collect

**When NOT to use:**
- Single-agent tasks → dispatch with Agent tool directly
- Independent tasks, no inter-agent communication → use `subagent-driven-development`
- Need human review between batches → use `executing-plans`

## The Workflow

```text
1. READ SPEC       — Read context ONCE to write task descriptions
2. CREATE TEAM     — TeamCreate with name + description
3. CREATE TASKS    — TaskCreate × N with blockedBy dependencies
4. SPAWN AGENTS    — Agent tool for each role (coder, reviewer)
5. BROADCAST ROSTER — Broadcast all teammate names so agents can peer-message directly
   Include in the broadcast: teammate names, instruction to send/receive messages directly with peers, and to ignore duplicates of their own recent messages.
6. ROUTE MESSAGES  — Branch on agent verdicts (APPROVED / FIX_REQUIRED)
7. SHUTDOWN        — SendMessage type: shutdown_request to all agents
8. CLEANUP         — TeamDelete
9. REPORT          — Text output to user: commit SHA, summary, verdict
```

## Task Decomposition

**Always create commit as a separate task:**

```text
Task #1: Implement (RED→GREEN)     — coder
Task #2: Review                    — reviewer, blockedBy: [1]
Task #3: Commit via /commit skill  — coder, blockedBy: [2]
```

Dependencies auto-unblock via TaskUpdate. Orchestrator doesn't manually sequence.

**Commit is a TASK, not orchestrator work.** Coder uses `/commit` skill which handles staging, diff analysis, and commit message generation.

## Agent Spawn Requirements

### Required fields on every Agent tool call

```
subagent_type: <role>
name: <name>
team_name: <team>
model: sonnet
description: <5-10 word summary of what the agent does>   ← REQUIRED, causes InputValidationError if missing
prompt: ...
run_in_background: true
```

**Always include `description`.** The Agent tool requires it — omitting it causes an `InputValidationError` and wastes a retry turn.


## DDD Review Gate (Effect Projects)

For Effect projects with domain types, add a **mandatory DDD gate** after foundational domain/error tasks complete and before service implementation tasks spawn:

```text
Group A (domain types, errors, config) → commits → DDD GATE → Group B (services, CLI)
```

**DDD gate agent**: Spawn `effect-ddd-review` after Group A commits. It checks:
- Branded types for domain primitives (IDs, hashes, salts, column names)
- `Schema.TaggedError` on all error types
- Consistent service tag style (`Context.Tag` class pattern across all services)
- No plain `string` / `number` used for domain values that should be branded

If DDD gate passes → spawn Group B. If it fails → fix before spawning Group B.

This catches cross-cutting domain issues before they propagate across all service files, avoiding expensive multi-file refactors later.

## Reviewer Spawn Prompt Requirements

When spawning the reviewer agent, the prompt **must** include:

1. **Require tool invocation before verdict** — The reviewer must call `Skill: effect-expert` for any ambiguous Effect pattern question (e.g., error type boundaries, R channel rules, Layer construction patterns) before issuing a verdict. Reviewer heuristics are not sufficient for Effect idiom questions.

2. **Authority hierarchy** — State explicitly: `ARCHITECTURE-PRINCIPLES.md` is the canonical source of truth and overrides any task spec, GH issue, or plan document. If the task spec contradicts an arch principle, that is a spec error — flag it as Critical.

3. **Critical verdicts require FIX_REQUIRED** — Any Critical finding (R channel leak on service interface, wrong error type at service boundary, mutation in pure functions) must produce `FIX_REQUIRED`, not `APPROVED with warnings`.

Example reviewer prompt addition:
```
IMPORTANT REVIEW RULES:
- For any ambiguous Effect idiom (error type boundaries, R channel rules, Layer patterns), invoke Skill: effect-expert BEFORE issuing your verdict.
- ARCHITECTURE-PRINCIPLES.md overrides the task spec. If the spec says X and arch principles say Y, flag X as Critical.
- Any Critical finding = FIX_REQUIRED verdict. Do not APPROVE with Critical warnings.
```

## Orchestrator's Only Jobs

| DO | DON'T |
|----|-------|
| Read spec ONCE for task descriptions | Re-read code after delegation |
| Create team + tasks with dependencies | Run git commands (diff, add, commit) |
| Spawn agents with clear prompts | Inspect code or verify boundaries |
| Route messages based on verdicts | Stage files or write commit messages |
| Shutdown agents when done | Duplicate reviewer's work |
| Report results to user | Investigate or "quick check" anything |

**Front-load context into task descriptions** — if you know file paths, function signatures, and locations from your initial spec read, include them in the task prompt. This reduces agent ramp-up time without violating delegation (you're describing the task, not doing it).

## Message-Driven Routing

Every agent-to-orchestrator boundary crossing is a **SendMessage**. Orchestrator decisions are message-driven — route based on the reviewer's **structured verdict line**, not on prose summaries:

```text
Coder    → "Task #1 done"                          → Unblock review (task #2)
Reviewer → "Verdict: PASS — ..."                   → Check for Suggestions → commit (task #3)
Reviewer → "Verdict: NEEDS WORK — ..."             → FIX_REQUIRED → route to coder
Reviewer → "Verdict: FAIL — ..."                   → Escalate to user immediately
Coder    → "Committed: abc123 'feat: add X'"       → Shutdown + report
```

**Verdict routing rules:**
- `Verdict: PASS` → Proceed to commit. If reviewer included findings/suggestions: present them to user as-is — do NOT label them "non-blocking". Let the user classify severity and decide next action (fix now / GH issue / skip). Do not anchor the user with a severity label.
- `Verdict: NEEDS WORK` → FIX_REQUIRED — route the full Findings Table to coder
- `Verdict: FAIL` → Escalate to user — do not route to coder

**Suggestion handling (after PASS):**
After the coder commits, present any Suggestion findings to the user:

```text
Review PASS — committed {SHA}.

Reviewer flagged {N} non-blocking suggestion(s):
  1. {file}:{line} — {description}
  2. ...

Fix now → coder will address before shutdown
Create GH issue → open issue(s) for later
Skip → done
```

**When reviewer disagrees with spec:** Route the conflict BACK to the reviewer with specific evidence. Don't read files yourself to arbitrate.

**Reject prose-only verdicts:** If reviewer message contains no `Verdict: [PASS|NEEDS WORK|FAIL]` line, send back: "Please resend with the structured verdict line from your Final Verdict section."

## Fix Loop

```text
Reviewer returns → Verdict: PASS? ── yes ──→ Suggestions? ── no ──→ Task #3 (coder commits)
                        │                          │
                        │                         yes
                        │                          └──→ Present to user → fix / issue / skip
                        │
                        no (NEEDS WORK / FAIL → FIX_REQUIRED)
                        │
                  ┌─ Message coder: "Fix {issues}"
                  ├─ Coder fixes → messages back
                  ├─ Message reviewer: "Re-review"
                  ├─ Reviewer re-reviews → messages back
                  └─ Max 2 cycles, then:
                        │
                  ┌─────┴─────┐
                  │           │
            Non-trivial    Trivial failure
            failure        (agent confusion,
                           typo, careless)
                  │           │
            Escalate      Spawn FRESH agent
            to user       with specific
                          instructions
```

**Fix loop nuance:** "Max 2 cycles → escalate" prevents infinite loops. But when the failure is clearly agent confusion (not a hard problem), spawning a fresh agent with hyper-specific instructions is pragmatic delegation — not a protocol violation. Reserve user escalation for genuine blockers.

## Shutdown Sequence

```text
1. SendMessage type: shutdown_request → coder
2. SendMessage type: shutdown_request → reviewer
3. (Wait for shutdown confirmations)
4. TeamDelete → cleans up team config + task list
5. Text output → user: commit SHA, summary, verdict
6. Offer to merge branch → user decides
```

**Always shut down ALL agents before TeamDelete.** TeamDelete fails with active members.

**Post-report merge offer (REQUIRED):** After reporting the commit SHA, offer to merge the branch for the user. Never auto-merge — always wait for explicit confirmation.

```text
Committed {SHA}. Offer: "Merge `{branch}` into `main`? I'll run `git checkout main && git merge {branch}`."
```

Never proceed with the merge unless the user explicitly says yes.

## Anti-Patterns

| Anti-Pattern | Why It's Wrong |
|---|---|
| Orchestrator reads diff after delegation | Duplicates reviewer's work, wastes context |
| Orchestrator runs `git add` / `git commit` | Implementation work — delegate to coder with /commit |
| Orchestrator re-verifies code quality | Reviewer already verified — trust the verdict |
| No commit task in task list | Commit is work — needs a task for delegation |
| Orchestrator reads spec to override reviewer | Unilateral investigation — route conflict to reviewer instead |
| Orchestrator fixes "trivial" issue directly | Erosion starts with "just this once" — delegate everything |

## Red Flags — STOP and Reconsider

If you catch yourself doing ANY of these as orchestrator:

- Running `git diff`, `git add`, `git commit`, `git status`
- Reading source files after agents were spawned
- Verifying code changes yourself ("just a quick check")
- Writing commit messages
- Running tests yourself
- Reading spec to arbitrate a reviewer finding
- Fixing a "trivial" issue directly

**All mean: You're doing agent work. Delegate it.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Quick git status check" | That's agent work. Trust their reports. |
| "Just verify the boundary" | Reviewer verified it. Trust the verdict. |
| "I'll commit, it's faster" | Speed ≠ correct. Coder commits via /commit skill. |
| "I already saw the diff (muscle memory)" | Sunk cost. Don't act on accidental information — route it. |
| "I have full context, spawning agent wastes time" | Front-load context into task description. Don't bypass delegation. |
| "It's a 3-character fix" | No carve-out for trivial. Delegate or it erodes the model. |
| "I remember the spec says X" | Route your memory as evidence to the reviewer. Don't investigate. |
| "Escalating a typo to user is embarrassing" | Precise escalation with actionable context is professional. Or spawn fresh agent. |

---

## Document Writing Variant

When orchestrating document writing (vs code implementation):

### Roles

- **domain-expert** replaces reviewer (terminology accuracy, not code review)
- **analyst** replaces coder (data verification against pre-computed outputs, not implementation)
- **writer** is the sole document editor
- **scanability-critic** is the readability reviewer

### Phase 0: Deterministic Offloading

Before creating the team, run ALL data scripts and verify outputs populate marker regions in the target document. Agents work from pre-computed outputs, not live script execution. This converts 60 minutes of LLM brute force into seconds of script execution.

Scripts populate content between `%% begin_TAG %%` / `%% end_TAG %%` markers. LLM agents only write prose OUTSIDE marker regions. Re-running scripts refreshes all data without touching prose.

### Peer Messaging

After all agents ready, broadcast TEAM ROSTER with names + roles. Agents message each other directly; orchestrator mediates conflicts only.

```
TEAM ROSTER:
- domain-expert: terminology accuracy, NotebookLM policy research
- analyst: data verification against pre-computed script outputs
- writer: document editing (sole editor)
- scanability-critic: readability diffs

You may message any teammate directly using SendMessage(recipient="<name>").
For conflicts, message team-lead for routing.
```

### Writer Skill Invocations

Writer's spawn prompt must include instructions to invoke writing skills before sending completion:
- `/writing-for-token-optimized-and-ceo-scannable-content` — applied before finalizing each section
- `/elements-of-style` (via `/writing-clearly-and-concisely`) — applied for prose quality

Scanability-critic still reviews independently, but writer self-applies skills BEFORE critic sees the draft. This reduces critic diff volume.

### Per-Section Workflow

1. Route section to domain-expert + analyst in parallel (jact commands)
2. Both send findings to writer via peer DM
3. Writer applies findings + invokes writing skills
4. Route to scanability-critic
5. Critic sends diffs to writer via peer DM
6. User approval gate (HARD GATE)

### Verdict Routing (Document Variant)

- Writer: "section written" → route to critic
- Critic: "N diffs" → writer applies, confirms
- Any agent: "blocker" → orchestrator mediates or escalates
- No PASS/FAIL structured verdicts — use completion messages

### Re-Analysis (Future Runs)

After prose is finalized, re-running scripts refreshes all marker content without touching prose. Analyst verifies prose claims still match new numbers. Domain-expert + writer update prose only if semantics changed.
