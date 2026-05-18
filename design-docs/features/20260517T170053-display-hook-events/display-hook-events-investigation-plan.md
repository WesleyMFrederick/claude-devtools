# Plan: Display Hook Events in claude-devtools — Phase 1 Investigation (delegated research)
%% *Last Modified: 05/17/26 17:02:50* %%

> **Plan type:** Phase 1 Step 2.5 research-to-resolve plan (Polya / How-to-Solve-It).
> **This is NOT an implementation plan.** The delegated agent TRACES the pipeline and APPENDS findings. It does not write feature code.
> **Branch:** `feat/display-hook-context` (already checked out — do not create a new branch).

---

## 0. Coldstart Bootstrap
%% *Last Modified: 05/17/26 17:02:50* %%

**WHO YOU ARE:** Read-only research agent. You did not produce this plan and have zero prior conversation context. Your sole job: resolve the open research questions in §4 by tracing the claude-devtools display pipeline, then append evidence-tagged findings to §6 (`## Research Findings`).

**SCOPE — MUST NOT:**
- Implement, edit, or scaffold any feature code (no new components, no parser changes).
- Advance to Phase 2 (Devise a Plan) or write an implementation plan.
- Write anywhere except the `## Research Findings` section of THIS file.

**ABSOLUTE PATHS:**
- Repo root: `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools`
- This plan: `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools/design-docs/features/20260517T170053-display-hook-events/display-hook-events-investigation-plan.md`
- Sample data (343 lines, 48 hook records): `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/cc-workflows-plugin/sessions/de45b08f-129e-49b2-8b1d-8521caee1790.jsonl`

**KEY FILES (verified to exist — read in this order):**
1. `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools/src/main/types/jsonl.ts` — raw JSONL record types
2. `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools/src/main/services/parsing/SessionParser.ts` — JSONL → message parsing
3. `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools/src/main/services/parsing/MessageClassifier.ts` — message classification
4. `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools/src/main/types/messages.ts` — parsed message types + type guards
5. `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools/src/main/types/chunks.ts` — chunk + display-item types
6. `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools/src/main/services/analysis/ChunkBuilder.ts` — chunk assembly
7. `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools/src/main/services/analysis/SemanticStepExtractor.ts` — display-item extraction
8. `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools/src/renderer/components/chat/items/SlashItem.tsx` — closest visual analog (the `/decompose-plan` row)
9. `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools/src/renderer/components/chat/items/BaseItem.tsx` — shared icon + expand/collapse + token affordance
10. `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools/src/renderer/components/chat/items/MetricsPill.tsx` — per-item token display
11. `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools/src/renderer/components/chat/DisplayItemList.tsx` — item dispatch/render loop

**CONTEXT YOU LACK — read before acting:**
- `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools/CLAUDE.md` § "Critical Concepts" — isMeta flag, Chunk Structure, Visible Context Tracking (6-category union). Hook content is injected into Claude's context, so it likely also intersects the Visible Context system — treat that as an open question, not a closed one.
- `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools/.claude/rules/react.md` — component conventions for any new item component the follow-on implementation will add.

**TOOLS + FALLBACKS:**
- Static tracing: LSP `findReferences` / `documentSymbol` first → fall back to `Grep` / `Read` with offset/limit only if LSP unavailable.
- Markdown orientation: `jact ast <file>` then `jact extract header` → fall back to `Read` with offset/limit.
- JSONL inspection: `sed -n 'Np'` piped to `jq` (records are long single lines — never `Read` the raw file cold).

**COMMAND DISCIPLINE:** One command per Bash call. Ingest output. Use it in the next call. Never chain with `&&` or `;`.

**FIRST ACTIONS:**
1. Read this plan end-to-end.
2. Read every file in KEY FILES (1–11) and CONTEXT YOU LACK.
3. Resolve the highest-risk open question first: **RQ-2 (what happens to `type:"attachment"` records today)** — this gates everything else.
4. Work remaining RQs by pipeline layer (RQ-1 → RQ-6).

**DEFINITION OF DONE:**
- Every RQ in §4 answered with file:line evidence.
- Findings appended to §6, each carrying an evidence tag (`[OBS]`, `[F-ID]`, `[H]`, `[A]`).
- Status line at top of §6 updated to `Research status: COMPLETE`.

**HARD STOP:** HALT after appending findings. Do NOT advance phases, do NOT implement, do NOT write an implementation plan. Return control to the user.

---

## 1. Problem Understanding (Phase 1 output)
%% *Last Modified: 05/17/26 17:02:50* %%

- **Parent Unknown (U0):** Make Claude Code hook events from JSONL session transcripts visible in the claude-devtools timeline, rendered with the same item affordances (icon, expand/collapse, per-item token count) as existing display items.
  - source: stated (user prompt)
  - confidence: high

- **Auxiliary Unknowns (the "additional tasks for Phase 1" — these are the research questions, see §4):**
  - **U1:** Where in the parse→classify→chunk→item→render→token pipeline must hook handling be injected at each of 6 layers?
  - **U2:** Which existing item is the correct visual/structural template to mirror (SlashItem vs TextItem vs BaseItem)?
  - **U3:** Does hook content also belong in the Visible Context 6-category tracking system (it is literally injected into Claude's context window)?

- **Data:**
  - Sample JSONL: 343 lines; **48** records with `type:"attachment"`; **4** distinct `attachment.hookEvent` values observed: `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`.
  - Verified hook record shape (jq on line 13):
    - Top-level keys: `attachment, cwd, entrypoint, gitBranch, isSidechain, parentUuid, sessionId, timestamp, type, userType, uuid, version`
    - `type` = `"attachment"`
    - `attachment` = `{ type: "hook_additional_context", hookEvent: <string>, hookName: <string>, toolUseID: <string|null>, content: string[] }`
    - Example line 13: `hookEvent:"UserPromptSubmit"`, `hookName:"UserPromptSubmit"`, `toolUseID:"hook-77edc30f-..."`, `content:["<chat-output-preferences>…"]` (single-element array)
  - Screenshot: desired placement is a **child item inside the AIChunk**, ordered between the `/decompose-plan` slash item (jsonl line 8) and the `Output` text item, with the same row chrome (icon, `~N tokens`, expand chevron). The red "Hook" label is the user's annotation marking the target location, not existing UI.
  - Pipeline files enumerated and verified to exist (see §3).

- **Condition:** New display must reuse existing patterns — (1) an icon, (2) expand/collapse, (3) per-item token calculation — consistent with `SlashItem`/`TextItem`/`BaseItem`/`MetricsPill`.

- **Assessment (`[d]`):** Condition is **possible** but **insufficient for implementation without a pipeline trace**. Confirmed greenfield: `grep -rn` for `attachment` / `hook_additional_context` / `hookEvent` / `hookName` across `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools/src` returns **zero matches** → hook records are unhandled at every layer. The gap is purely *knowledge of injection points*, which is exactly what a bounded trace resolves.

- **Research log (Step 2.5 bounded research already performed by planning agent):**
  - Loaded sample JSONL lines 7, 8, 13, 16; derived hook record schema via `jq`.
  - Confirmed branch `feat/display-hook-context`; only 1 commit ahead of main (docs only) → no prior implementation.
  - Enumerated parsing/analysis/renderer files; confirmed no `attachment` handling in src.
  - Loaded canonical plan template + ideal-outcomes template for format compliance.

- **Open hedges (require the delegated agent to resolve, NOT the user):**
  - "additional tasks for phase 1" trigger word → resolved into the RQ set in §4 (delegated, hence this Coldstart Bootstrap).
  - Whether hook content double-counts against Visible Context categories — flagged as **RQ-6**, must be answered with evidence.

---

## 2. Locked Ideal Outcomes (pass forward exactly on auto-compress)
%% *Last Modified: 05/17/26 17:02:50* %%

> Outcomes for the **research deliverable** (this is an investigation plan, not an implementation plan).

| Actor | [O] Outcome |
|---|---|
| **USER** | Reads a single findings section and knows every file:line where hook handling must be added, without re-tracing the codebase |
| **USER** | Hands the findings to an implementation-planning step with zero remaining "where does this go?" ambiguity |
| **AGENT (follow-on)** | Writes an implementation plan grounded only in traced file:line evidence (no guessing at injection points) |
| **AGENT (delegated researcher)** | Determines the exact parse/classify/chunk/item/render/token injection points from source alone |
| **SYSTEM** | Preserves the plan as authoritative; findings are appended, never overwrite the problem statement |

---

## 3. AC / Success Criteria / DoD Coverage Map
%% *Last Modified: 05/17/26 17:02:50* %%

| # | Outcome | Acceptance Criteria | Success Criteria | Definition of Done |
|---|---|---|---|---|
| 1 | USER reads findings, knows every injection point | §6 contains a file:line answer for each of RQ-1…RQ-6 | A reader can list every file an implementation must touch, in pipeline order, from §6 alone | Each RQ has ≥1 `file:line` citation and an evidence tag |
| 2 | USER hands off with zero ambiguity | Findings name the concrete extension mechanism per layer (discriminated-union case, type guard, factory branch, item component, token source) | No RQ answer is "unclear" or "TBD" | Every RQ marked `RESOLVED` or `BLOCKED: <reason>` |
| 3 | Follow-on agent plans from evidence only | Each finding distinguishes `[OBS]` (read from source) vs `[H]`/`[A]` (inferred) | Zero unsourced structural claims | All inference tagged with Risk-if-wrong |
| 4 | Researcher derives injection points from source | Trace is bidirectional: forward from JSONL ingest, backward from the rendered row | Entry→exit path is complete with no "and then somehow it renders" gaps | Trace covers all 6 layers end to end |
| 5 | Plan stays authoritative | Only §6 is modified by the researcher | Problem statement, Coldstart, RQs unchanged | `git diff` touches only §6 of this file |

---

## 4. Open Research Questions (the additional Phase 1 tasks)
%% *Last Modified: 05/17/26 17:02:50* %%

Trace **bidirectionally** — forward from JSONL ingest and backward from the rendered row — and use **LSP first** (`findReferences`, `documentSymbol`) at every node. The trace must be **complete entry→exit** (no skipped hops).

### RQ-1 — JSONL type layer
%% *Last Modified: 05/17/26 17:02:50* %%

**File:** `…/src/main/types/jsonl.ts`
- Is there a discriminated union over the record `type` field? Enumerate every member.
- Is there any existing member for `type:"attachment"`? If not, where exactly (line) would a new `AttachmentRecord` member be added, and what does the union's "unknown type" path do today?

### RQ-2 — Parsing / classification (HIGHEST RISK — resolve first)
%% *Last Modified: 05/17/26 17:02:50* %%

**Files:** `…/src/main/services/parsing/SessionParser.ts`, `…/src/main/services/parsing/MessageClassifier.ts`
- Trace one JSONL line from read to classified message. What happens to a `type:"attachment"` line **today** — silently dropped, error-logged, or passed through as some fallback type? Cite the exact branch (file:line).
- What is the single injection point where an attachment/hook record would be recognized and converted into a parsed message?

### RQ-3 — Parsed message type + type guard
%% *Last Modified: 05/17/26 17:02:50* %%

**Files:** `…/src/main/types/messages.ts`, `…/src/main/types/domain.ts`
- What message types + `isXxx` type guards exist (CLAUDE.md lists `isParsedRealUserMessage`, `isParsedInternalUserMessage`, `isAssistantMessage`)?
- What new message type (e.g., `ParsedHookEventMessage`) and guard (e.g., `isParsedHookEventMessage`) would be needed, and where do guards get consumed downstream (LSP `findReferences` on an existing guard to map the blast radius)?

### RQ-4 — Chunk building / item ordering
%% *Last Modified: 05/17/26 17:02:50* %%

**Files:** `…/src/main/services/analysis/ChunkBuilder.ts`, `ChunkFactory.ts`, `SemanticStepExtractor.ts`, `ToolExecutionBuilder.ts`
- How are child display items (slash, text/"Output", Bash tool calls) created and ordered within an `AIChunk`? Identify the ordering key (timestamp? parentUuid chain? array order?).
- Given the hook record's `parentUuid`, where would a hook item be inserted so it lands between the slash item and the first tool call (as in the screenshot)? Name the function + line.

### RQ-5 — Display-item type + renderer (visual pattern to mirror)
%% *Last Modified: 05/17/26 17:02:50* %%

**Files:** `…/src/main/types/chunks.ts`, `…/src/renderer/components/chat/DisplayItemList.tsx`, `…/src/renderer/components/chat/items/{SlashItem,TextItem,BaseItem,LinkedToolItem}.tsx`
- What is the display-item discriminated union? Where is each variant dispatched to its component in `DisplayItemList.tsx`?
- Which existing item is the closest structural template for a hook row? Document exactly how it wires (a) icon, (b) expand/collapse state, (c) the `~N tokens` pill. The follow-on `HookItem` must reuse these, not reinvent.
- Recommend the icon + label (e.g., `Hook` / `UserPromptSubmit`) consistent with existing iconography.

### RQ-6 — Token calculation + Visible Context interaction
%% *Last Modified: 05/17/26 17:02:50* %%

**Files:** `…/src/renderer/components/chat/items/MetricsPill.tsx`, tokenizer util under `…/src/main/utils/`, `…/src/renderer/utils/contextTracker.ts`, `…/src/renderer/types/contextInjection.ts`
- How is a per-item `~N tokens` value computed and passed to `MetricsPill`? Trace the token source for an existing item (e.g., the `~901 tokens` slash row).
- Hook `attachment.content` is `string[]` injected into Claude's context. Does/should it also register in the Visible Context 6-category union (CLAUDE.md "Visible Context Tracking")? Determine whether displaying it AND counting it in a context category would **double-count**. State the evidence either way — this is a correctness risk, not a nicety.

### RQ-7 — Authoritative hook schema cross-check
%% *Last Modified: 05/17/26 17:02:50* %%

- Cross-check the observed schema against Claude Code reference docs for the transcript/hook format (look up reference docs before relying on the sample alone). Confirm: are `hookEvent` values limited to the 4 observed, or are there more (e.g., `SessionStart`, `PreCompact`, `Notification`, `SubagentStop`)? Cite the doc source. This prevents a switch that silently drops unobserved hook types.

---

## 5. Research Methodology Constraints
%% *Last Modified: 05/17/26 17:02:50* %%

- **LSP-first static analysis** for all TypeScript/TSX tracing; `Grep`/`Read` only as fallback.
- **Bidirectional BFS** at every trace node: expand callers (backward) and callees (forward) until the JSONL-ingest end meets the rendered-row end.
- **Complete trace:** entry (JSONL line read) → exit (DOM row rendered with token pill). No "then it renders somehow" gaps.
- **Probe-first:** before any batch `jq`/`grep` across the sample file, run it on ONE line and verify output shape.
- **Evidence discipline:** `[OBS]` only for things read from source/files; `[F-ID]` for structural derivations; `[H]`/`[A]` for inference (always add Risk-if-wrong). Chat/summary uses scannable format; THIS file uses full tags.
- **One command per Bash call.**

---

## 6. Research Findings
%% *Last Modified: 05/17/26 17:02:50* %%

`Research status: NOT STARTED`

> Delegated agent: append all findings below this line. One subsection per RQ (RQ-1 … RQ-7). Do not modify any section above.
