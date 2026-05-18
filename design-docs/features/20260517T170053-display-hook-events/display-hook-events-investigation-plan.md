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
%% *Last Modified: 05/17/26 18:00:16* %%

- **Parent Unknown (U0) — CORRECTED 2026-05-17 (user steering, mid-session):** Make **every `type:"attachment"` context injection** from JSONL session transcripts visible in the claude-devtools timeline — hook events **and** nested memory, task reminders, skill listings, MCP instructions, and the rest — rendered with the same item affordances (icon, expand/collapse, per-item token count) as existing display items. The end goal is: the user can see *all the extra material being fed into Claude's context* that the timeline does not currently show. "Display hookEvent" was one *means*; this is the *end*.
  - source: stated as "hookEvent" (user prompt) → broadened by explicit user clarification mid-session: "the goal is for me to be able to see all the extra stuff being sent to claude. so nested memory, task reminders, would also be good to include"
  - confidence: high
  - **Scope-correction impact:** This *simplifies* the build. §6 RQ-2 already enumerated all 12+ `attachment` subtypes; RQ-7 already recommends a **catch-all render path, not a narrow `hook_additional_context` gate**. The corrected scope = display all `attachment` records as a generic "context injection" item, differentiated by `attachment.type` (label/icon). No allow-list to maintain. Every §6 injection point stays valid; only the gate condition broadens (from one subtype to "any attachment").

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

- **Open hedges:**
  - "additional tasks for phase 1" trigger word → RESOLVED into the RQ set in §4; all 7 RQs filed in §6.
  - Visible Context double-count → RESOLVED by RQ-6 (no double-count; a dedicated context category is a separate, out-of-scope feature).
  - **Scope boundary → RESOLVED 2026-05-17 (user: "so ALL"):** Display **every `attachment` subtype**, no exclusions. User supplied real samples proving the "status-only" subtypes actually carry meaningful content: `hook_success` carries `stdout` with injected `hookSpecificOutput.additionalContext`; `hook_blocking_error` carries the full `blockingError.blockingError` text injected back into Claude; `queued_command` carries the user's queued `prompt`. None are noise.
  - **NEW auxiliary unknown (U4) — opened by the user's samples:** `attachment` subtypes have **heterogeneous payload shapes**; displayable content lives in a different field per subtype (`hook_additional_context`→`content[]`, `hook_success`→`stdout`, `hook_blocking_error`→`blockingError.blockingError`, `queued_command`→`prompt`, and `queued_command` has **no** `hookEvent`/`hookName` — it is not a hook). The §6 research found subtype *names/counts* but not per-subtype *content-field locations*. This blocks a grounded implementation plan (the renderer needs a per-subtype content extractor). → dispatched as **RQ-8** (cheap mechanical jq probe), findings to be appended to §6.

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
%% *Last Modified: 05/17/26 17:10:23* %%

`Research status: COMPLETE`

> Delegated agent: append all findings below this line. One subsection per RQ (RQ-1 … RQ-7). Do not modify any section above.

---

### RQ-1 — JSONL type layer
%% *Last Modified: 05/17/26 17:10:23* %%

**File:** `src/main/types/jsonl.ts`

[OBS] The `EntryType` discriminated union at `jsonl.ts:15–21` enumerates exactly 6 members:
```
'user' | 'assistant' | 'system' | 'summary' | 'file-history-snapshot' | 'queue-operation'
```
`attachment` is **not** a member. [OBS:jsonl.ts:15-21]

[OBS] The `ChatHistoryEntry` union at `jsonl.ts:212–218` is the top-level discriminated union consumed by the parser. It includes `UserEntry | AssistantEntry | SystemEntry | SummaryEntry | FileHistorySnapshotEntry | QueueOperationEntry`. No `AttachmentEntry` exists. [OBS:jsonl.ts:212-218]

[OBS] The "unknown type" path is handled in `parseMessageType()` in `src/main/utils/jsonl.ts:199–216`:
```typescript
default:
  // Unknown types are skipped
  return null;
```
When `parseMessageType` returns `null`, `parseChatHistoryEntry` returns `null` at line 111 (`if (!type) { return null; }`), and the caller `parseJsonlFile` silently discards that record (no log, no error). [OBS:jsonl.ts:199-216, jsonl.ts:110-113, jsonl.ts:71-79]

**Injection point for RQ-1:** A new `AttachmentEntry` interface must be added to `jsonl.ts` and included in the `ChatHistoryEntry` union. The `EntryType` alias must gain `'attachment'` as a member **OR** (preferred, to avoid touching `EntryType`) the attachment can be handled as a parallel type whose presence bypasses the `EntryType` check. The simplest surgical approach: add `AttachmentEntry` to `ChatHistoryEntry` union at `jsonl.ts:212` and add a new type guard `isAttachmentEntry`.

**RESOLVED**

---

### RQ-2 — Parsing / classification (HIGHEST RISK)
%% *Last Modified: 05/17/26 17:10:23* %%

**Files:** `src/main/utils/jsonl.ts`, `src/main/services/parsing/MessageClassifier.ts`

[OBS] Complete trace of a `type:"attachment"` line through the parse stack:

1. `parseJsonlFile` reads the line, calls `parseJsonlLine(line)` at `jsonl.ts:73`. [OBS:jsonl.ts:68-79]
2. `parseJsonlLine` calls `JSON.parse(line) as ChatHistoryEntry` and passes to `parseChatHistoryEntry`. [OBS:jsonl.ts:88-95]
3. `parseChatHistoryEntry` calls `parseMessageType(entry.type)` at `jsonl.ts:110`. [OBS:jsonl.ts:104-115]
4. `parseMessageType` hits the `default` branch for `"attachment"`, returns `null`. [OBS:jsonl.ts:199-216]
5. `parseChatHistoryEntry` checks `if (!type) { return null; }` at `jsonl.ts:111-113` and returns `null`. [OBS:jsonl.ts:110-113]
6. `parseJsonlFile` receives `null` from `parseJsonlLine` and skips adding it to the `messages` array (checked via `if (parsed) { messages.push(parsed); }` at `jsonl.ts:73`). [OBS:jsonl.ts:72-75]
7. **Result:** Attachment records are **silently dropped with no error log**. They never reach `MessageClassifier`, `ChunkBuilder`, or any downstream layer.

[OBS] `MessageClassifier.categorizeMessage()` is never reached for attachment records because `parseJsonlFile` returns only non-null `ParsedMessage[]`. [OBS:MessageClassifier.ts:42-65]

**Single injection point for attachment recognition:**

The minimal injection point is `parseChatHistoryEntry` in `src/main/utils/jsonl.ts`, specifically before the `isConversationalEntry` check at line 134. A new early-return branch should handle `entry.type === 'attachment'` and convert `hook_additional_context` records into a new `ParsedHookEventMessage` (or into an extended `ParsedMessage` with additional fields). The `parseMessageType` function at `jsonl.ts:199-216` also needs `'attachment'` added to return the new type.

**Important nuance discovered:** `type:"attachment"` records contain multiple `attachment.type` subtypes beyond `hook_additional_context`. The 48 records in the sample break down as: `hook_additional_context` (18), `hook_success` (6), `hook_cancelled` (5), `nested_memory` (5), `task_reminder` (5), `edited_text_file` (2), `skill_listing` (2), and one each of `command_permissions`, `deferred_tools_delta`, `hook_blocking_error`, `mcp_instructions_delta`, `queued_command`. The injection point must gate on `attachment.type === 'hook_additional_context'` (and optionally `hook_success`, `hook_cancelled`, `hook_blocking_error`) to avoid rendering every attachment subtype. [OBS: sample JSONL probe via jq]

**RESOLVED**

---

### RQ-3 — Parsed message type + type guard
%% *Last Modified: 05/17/26 17:10:23* %%

**Files:** `src/main/types/messages.ts`, `src/main/types/domain.ts`

[OBS] Existing `MessageType` union in `domain.ts:26-32`:
```typescript
type MessageType = 'user' | 'assistant' | 'system' | 'summary' | 'file-history-snapshot' | 'queue-operation';
```
No `'attachment'` member exists. [OBS:domain.ts:26-32]

[OBS] Existing `ParsedMessage` interface in `messages.ts:63-108` has `type: MessageType` as a required field. Adding a new message type requires either (a) extending `MessageType` with `'attachment'`, or (b) creating a parallel type `ParsedHookEventMessage` that does not extend `ParsedMessage`. Option (a) is simpler — the switch in `SessionParser.processMessages` at `SessionParser.ts:98-116` has a `default: byType.other.push(m)` branch that would safely absorb the new type without touching the existing `user`/`assistant`/`system` branches. [OBS:SessionParser.ts:98-116]

[OBS] Existing type guards consumed downstream (from `messages.ts`):
- `isParsedRealUserMessage` — checks `msg.type !== 'user'` [OBS:messages.ts:125]
- `isParsedUserChunkMessage` — checks `msg.type !== 'user'` [OBS:messages.ts:165]
- `isParsedSystemChunkMessage` — checks `msg.type !== 'user'` [OBS:messages.ts:245]
- `isParsedInternalUserMessage` — checks `msg.type === 'user'` [OBS:messages.ts:270]
- `isParsedHardNoiseMessage` — checks specific types by name [OBS:messages.ts:298-352]
- `isParsedCompactMessage` — checks `isCompactSummary` flag [OBS:messages.ts:358]

[F-ID] All existing type guards use explicit `msg.type === 'user'`/`=== 'assistant'` checks. None use wildcard patterns. A new `msg.type === 'attachment'` value would fall through all existing guards unchanged — no existing guard would incorrectly match or reject it. This means adding `'attachment'` to `MessageType` carries zero blast-radius risk to existing guard logic.

**New message type needed:** Add `'attachment'` to `MessageType` in `domain.ts:32`. Add the following new type guard in `messages.ts`:
```typescript
export function isParsedHookEventMessage(msg: ParsedMessage): boolean {
  return msg.type === 'attachment';
}
```

**Where guards are consumed downstream:** `MessageClassifier.ts:44-64` imports and calls `isParsedHardNoiseMessage`, `isParsedCompactMessage`, `isParsedSystemChunkMessage`, `isParsedUserChunkMessage`. The new `isParsedHookEventMessage` guard would be consumed in `MessageClassifier.categorizeMessage` to create a new `'hook'` category (or route to `'ai'` for passthrough). [OBS:MessageClassifier.ts:32-65]

**RESOLVED**

---

### RQ-4 — Chunk building / item ordering
%% *Last Modified: 05/17/26 17:10:23* %%

**Files:** `src/main/services/analysis/ChunkBuilder.ts`, `src/main/services/analysis/SemanticStepExtractor.ts`

[OBS] The `buildChunks` method in `ChunkBuilder.ts:78-152` iterates classified messages and dispatches by `category`. The current switch handles `'hardNoise'` (skip), `'compact'`, `'user'`, `'system'`, `'ai'` (buffer). A new `'hook'` category would be processed here. [OBS:ChunkBuilder.ts:98-135]

[OBS] Child display items within an `AIChunk` are ordered by **timestamp** in `SemanticStepExtractor.ts:208`: `return steps.sort((a, b) => a.startTime.getTime() - b.startTime.getTime())`. The sort is performed after all steps are collected. [OBS:SemanticStepExtractor.ts:208-210]

[OBS] A hook record carries `timestamp` and `parentUuid` as top-level fields (confirmed by JSONL probe). The `parentUuid` links the hook record to the assistant message that triggered it (e.g., a `PreToolUse` hook record's `parentUuid` matches the assistant message UUID of the tool call that preceded it).

[F-ID] There are two viable insertion strategies:

**Strategy A (preferred — simplest):** Route attachment records with `attachment.type === 'hook_additional_context'` into the existing `'ai'` category in `MessageClassifier`. This means they land in the `aiBuffer` in `ChunkBuilder` and are passed to `buildAIChunkFromBuffer`. Then `SemanticStepExtractor` must be extended to extract a new `'hook_event'` `SemanticStepType` from messages of type `'attachment'`. The timestamp-based sort in `SemanticStepExtractor.ts:208` will then automatically place hook items at the correct position relative to other steps. No new chunk type needed. **Ordering key is `timestamp`.**

**Strategy B (parallel path):** Create a new `MessageCategory` `'hook'` and produce new `HookChunk` items. This is heavier and unnecessary since hook events are logically part of the AI response stream.

[OBS] In the sample JSONL, a `UserPromptSubmit` hook record appears at line 13 with `timestamp` between the preceding user message (line 12) and the first assistant message. A `PreToolUse` hook appears immediately before its linked tool call. This confirms that timestamp-based ordering within the AI buffer will naturally produce the correct position — between the slash item and the first tool call output — matching the screenshot target. [OBS: JSONL probe, lines 13, 16]

**Injection point for RQ-4:** `SemanticStepExtractor.ts` — add a new branch in the `for (const msg of chunk.responses)` loop at line 33 to handle `msg.type === 'attachment'`. This runs after `Strategy A` makes attachment records flow into `chunk.responses`. The sort at line 208 handles ordering automatically.

**New `SemanticStepType` needed:** Add `'hook_event'` to the union in `chunks.ts:226-232`.

**RESOLVED**

---

### RQ-5 — Display-item type + renderer (visual pattern to mirror)
%% *Last Modified: 05/17/26 17:10:23* %%

**Files:** `src/renderer/types/groups.ts`, `src/renderer/components/chat/DisplayItemList.tsx`, `src/renderer/components/chat/items/SlashItem.tsx`

[OBS] The `AIGroupDisplayItem` discriminated union in `groups.ts:250-264`:
```typescript
export type AIGroupDisplayItem =
  | { type: 'thinking'; content: string; timestamp: Date; tokenCount?: number }
  | { type: 'tool'; tool: LinkedToolItem }
  | { type: 'subagent'; subagent: Process }
  | { type: 'output'; content: string; timestamp: Date; tokenCount?: number }
  | { type: 'slash'; slash: SlashItem }
  | { type: 'teammate_message'; teammateMessage: TeammateMessage }
  | { type: 'subagent_input'; content: string; timestamp: Date; tokenCount?: number }
  | { type: 'compact_boundary'; ... }
```
No `'hook'` variant exists. [OBS:groups.ts:250-264]

[OBS] `DisplayItemList.tsx:100-340` contains a `switch (item.type)` dispatch. Every case maps to a component. There is a `default: return null` fallback at line 322. A new `'hook'` case must be added here. [OBS:DisplayItemList.tsx:104-324]

**Closest visual template:** `SlashItem` / `BaseItem` pattern. Evidence:
- [OBS] `SlashItem.tsx` wraps `BaseItem` with: `icon={<Slash className="size-4" />}`, `label={`/${slash.name}`}`, `tokenCount={slash.instructionsTokenCount}`, `hasExpandableContent={hasInstructions}`, children = `<MarkdownViewer content={slash.instructions!} />`. [OBS:SlashItem.tsx:46-71]
- [OBS] `BaseItem.tsx:142-153` renders the token count pill inline in the header row: `~{formatTokens(tokenCount)} {tokenLabel}`. It is NOT `MetricsPill` — `MetricsPill` is a separate component used at the AI group level for main session impact / subagent context display. [OBS:BaseItem.tsx:142-153, MetricsPill.tsx:1-215]
- [OBS] Expand/collapse is handled entirely by `BaseItem` via the `isExpanded` prop and `ChevronRight` icon at `BaseItem.tsx:172-178`. The expanded content is `children` rendered below the header at `BaseItem.tsx:182-189`. [OBS:BaseItem.tsx:172-189]

[F-ID] A `HookItem` component should be structured identically to `SlashItem`: pass `BaseItem` an appropriate icon, `label` = e.g. `Hook`, `summary` = `hookEvent` value (e.g. `"UserPromptSubmit"`), `tokenCount` = estimated tokens from `attachment.content.join('\n')`, `hasExpandableContent={!!contentText}`, children = `<MarkdownViewer content={contentText} />`.

**Icon recommendation:** `Webhook` from lucide-react (not yet used in chat items; conveys hook event semantics). Fallback: `Zap` or `Activity`. [OBS: inventory of existing item icons shows `Slash`, `MailOpen`, `ChevronRight`, `Wrench`, `Layers`, `Brain`, `RefreshCw`, `MessageSquare`, `CornerDownLeft` — none convey hook/webhook semantics; `Webhook` is the natural fit]

**New variant to add to `AIGroupDisplayItem`:**
```typescript
| {
    type: 'hook';
    hookEvent: string;   // e.g. "UserPromptSubmit"
    hookName: string;    // e.g. "UserPromptSubmit" or "PreToolUse:Bash"
    content: string;     // joined attachment.content
    timestamp: Date;
    tokenCount?: number;
  }
```

**Files to touch for RQ-5:**
1. `src/renderer/types/groups.ts` — add `'hook'` variant to `AIGroupDisplayItem`
2. `src/renderer/components/chat/DisplayItemList.tsx` — add `case 'hook':` dispatch
3. `src/renderer/components/chat/items/HookItem.tsx` — new file (mirrors `SlashItem.tsx`)
4. `src/renderer/utils/displayItemBuilder.ts` — add `case 'hook_event':` in `buildDisplayItems` switch at line 149

**RESOLVED**

---

### RQ-6 — Token calculation + Visible Context interaction
%% *Last Modified: 05/17/26 17:10:23* %%

**Files:** `src/renderer/components/chat/items/BaseItem.tsx`, `src/shared/utils/tokenFormatting.ts`, `src/renderer/utils/contextTracker.ts`, `src/renderer/types/contextInjection.ts`

**Token calculation for the `~N tokens` pill:**

[OBS] `BaseItem.tsx:142-153` renders the per-item token pill directly from a `tokenCount` prop using `formatTokens(tokenCount)`. `formatTokens` is defined in `src/shared/utils/tokenFormatting.ts` and delegates to `estimateTokens(text)` = `Math.ceil(text.length / 4)`. [OBS:BaseItem.tsx:142-153, tokenFormatting.ts]

[OBS] `SlashItem` passes `slash.instructionsTokenCount` to `BaseItem.tokenCount`. `instructionsTokenCount` is computed in `slashCommandExtractor.ts:125`: `estimateTokens(followUp.text)` where `followUp.text` is the raw instructions string. [OBS:slashCommandExtractor.ts:125]

[F-ID] For a `HookItem`, token count should be computed as `estimateTokens(attachment.content.join('\n'))` at display-item build time in `displayItemBuilder.ts`. This mirrors the slash pattern exactly. The value is passed as `tokenCount` on the new `'hook'` display item variant.

**Visible Context double-count analysis:**

[OBS] The `ContextInjection` union in `contextInjection.ts:214-220` has 6 categories: `claude-md`, `mentioned-file`, `tool-output`, `thinking-text`, `task-coordination`, `user-message`. Hook content is not currently tracked in any category. [OBS:contextInjection.ts:214-220]

[OBS] `contextTracker.ts:184-252` (`aggregateToolOutputs`) scans `linkedTools` values for tool-output tokens. Hook content arrives as an attachment record separate from tool results — it does NOT appear in `linkedTools` (which are built from `tool_use`/`tool_result` pairs in assistant/user messages). Hook records are separate JSONL lines, not content blocks within existing messages. [OBS:contextTracker.ts:184-252]

[F-ID] Hook context IS injected into Claude's context window (that is the semantic purpose of `hook_additional_context`). However, since the Visible Context system currently tracks context consumption from the _next_ assistant message's `input_tokens` (which includes everything: CLAUDE.md, tool results, hook injections, etc.), displaying hook tokens in a new `ContextInjection` category would NOT double-count against the raw `input_tokens` total. The `input_tokens` field is a measured total; the `ContextInjection` breakdown is an estimated decomposition of that total.

[H] The correctness risk is: adding a `'hook'` category to `ContextInjection` would cause the estimated breakdown total to exceed the measured `input_tokens` only if the hook tokens are also accidentally counted in another category (e.g., `tool-output`). Since hook records are separate lines not processed by `aggregateToolOutputs`, this cross-counting does not occur today. Risk-if-wrong: if a future attachment subtype is also processed as a tool result, the category could double-count — but this would be a future bug in that future subtype's handling, not in the hook category itself.

**Recommendation:** For Phase 1, display hook tokens in the `BaseItem` token pill (per-item display) only. Do NOT add a new `ContextInjection` category in this feature — the correct extension would be a dedicated `HookInjection` category, but that is a non-trivial addition to the context tracking system that should be treated as a separate feature. Adding it now is out of scope and risks the implementation plan scope-creeping.

**RESOLVED**

---

### RQ-7 — Authoritative hook schema cross-check
%% *Last Modified: 05/17/26 17:10:23* %%

**Source:** Claude Code official documentation at `https://code.claude.com/docs/en/hooks` (fetched live during this research session).

[OBS] The 4 `hookEvent` values observed in the sample (`UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`) are confirmed valid hook events. However, the official documentation lists **far more** hook event types than observed in the sample. Full authoritative list:

**Session-level:** `SessionStart`, `Setup`, `SessionEnd`
**Per-turn:** `UserPromptSubmit`, `UserPromptExpansion`, `Stop`, `StopFailure`
**Agentic loop / tool execution:** `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `PermissionRequest`, `PermissionDenied`
**File and config:** `FileChanged`, `ConfigChange`, `InstructionsLoaded`, `CwdChanged`
**Agent and team:** `SubagentStart`, `SubagentStop`, `TeammateIdle`
**Task and compaction:** `TaskCreated`, `TaskCompleted`, `PreCompact`, `PostCompact`
**Worktree:** `WorktreeCreate`, `WorktreeRemove`
**MCP server:** `Elicitation`, `ElicitationResult`
**Notification:** `Notification`

[OBS] Total distinct `hookEvent` values in sample: 4 (`UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`). Total events in official docs: approximately 25. The gap is large. [OBS: JSONL probe; WebFetch of docs]

[OBS] Additionally, the sample reveals that `type:"attachment"` records carry multiple `attachment.type` values beyond `hook_additional_context`: `hook_success`, `hook_cancelled`, `hook_blocking_error` are also hook-related subtypes. These represent hook lifecycle outcomes (not just content injection). [OBS: JSONL probe, `jq -r '.attachment.type' | sort | uniq -c`]

**Critical implementation risk:** Any `switch (hookEvent)` that handles only the 4 observed values will silently drop the other ~21 hook types. The implementation must use a **catch-all display path** (render any unrecognized `hookEvent` as a generic hook row with the hookEvent name as label) rather than an exhaustive switch over only known values.

**RESOLVED**

---

### Pipeline Trace Summary (complete entry → exit)
%% *Last Modified: 05/17/26 18:06:12* %%

[F-ID] The complete 6-layer pipeline for hook event display, with injection points at each layer:

| Layer | File | Current behavior | Injection point |
|---|---|---|---|
| 1. JSONL type | `src/main/types/jsonl.ts:212` | `'attachment'` not in `ChatHistoryEntry` union | Add `AttachmentEntry` interface + add to union |
| 2. Parser | `src/main/utils/jsonl.ts:199-216` | `'attachment'` hits `default: return null` in `parseMessageType` | Add `case 'attachment': return 'attachment'` + handle in `parseChatHistoryEntry` |
| 3. Classifier | `src/main/services/parsing/MessageClassifier.ts:42-65` | Never reached (records dropped) | Add `isParsedHookEventMessage` guard; route to `'ai'` category |
| 4. Chunk builder | `src/main/services/analysis/ChunkBuilder.ts:131-133` | Never reached | No change needed if category = `'ai'`; hook messages join `aiBuffer` |
| 5. Semantic step extractor | `src/main/services/analysis/SemanticStepExtractor.ts:33` | Never reached | Add new branch in `for (msg of chunk.responses)` loop; emit `SemanticStep` with new type `'hook_event'` |
| 6a. Display item builder | `src/renderer/utils/displayItemBuilder.ts:149` | `'hook_event'` case missing from switch | Add `case 'hook_event':` emitting `{ type: 'hook', hookEvent, hookName, content, timestamp, tokenCount }` |
| 6b. Display item union | `src/renderer/types/groups.ts:250` | No `'hook'` variant | Add `'hook'` member to `AIGroupDisplayItem` union |
| 6c. Display item list | `src/renderer/components/chat/DisplayItemList.tsx:104` | No `case 'hook':` | Add `case 'hook':` dispatching to new `HookItem` |
| 6d. Item component | (new file) | Does not exist | Create `src/renderer/components/chat/items/HookItem.tsx` mirroring `SlashItem.tsx` |

**New type also required:** Add `'hook_event'` to `SemanticStepType` union in `src/main/types/chunks.ts:226`.

### RQ-8 — Per-subtype payload shapes (which field holds displayable content)
%% *Last Modified: 05/17/26 18:06:12* %%

All 12 subtypes verified from session `de45b08f-129e-49b2-8b1d-8521caee1790.jsonl` [OBS].

| attachment.type | All keys under .attachment | Displayable content field | Field type / inner shape | Has hookEvent/hookName? | Extractor rule |
|---|---|---|---|---|---|
| `hook_additional_context` | `type, content, hookName, toolUseID, hookEvent` | `content` | `string[]` — each element is a raw string (not `{type,text}` objects) | Yes | `content.join('\n')` |
| `hook_success` | `type, command, content, durationMs, exitCode, hookEvent, hookName, stderr, stdout, toolUseID` | `stdout` (primary); `content` is always `""` | `string` — often JSON; when JSON, human-readable part at `.hookSpecificOutput.additionalContext` | Yes | `JSON.parse(stdout)?.hookSpecificOutput?.additionalContext ?? stdout` |
| `hook_cancelled` | `type, command, durationMs, hookEvent, hookName, toolUseID` | None — no content field | n/a — metadata only (records that hook was cancelled before completion) | Yes | Display as "Hook cancelled: `{hookName}` ({hookEvent})" — no content to extract |
| `hook_blocking_error` | `type, hookName, toolUseID, hookEvent, blockingError` | `blockingError.blockingError` | `string` (nested: outer `blockingError` is an object `{blockingError: string, command: string}`) | Yes | `attachment.blockingError.blockingError` |
| `queued_command` | `type, prompt, commandMode` | `prompt` | `string` | No | `prompt` |
| `nested_memory` | `type, path, content, displayPath` | `content.content` | Outer `content` is object `{path, type, content, contentDiffersFromDisk}`; inner `content` is a `string` (the file text) | No | `content.content` (with `displayPath` as label) |
| `task_reminder` | `type, content, itemCount` | `content` | `array` of task objects `{id, subject, description, activeForm, status, blocks, blockedBy}` | No | `content.map(t => \`${t.status} — ${t.subject}\`).join('\n')` (or render per-task cards) |
| `edited_text_file` | `type, filename, snippet` | `snippet` | `string` — line-numbered file content (format: `"N\t<line text>\n..."`) | No | `snippet` (with `filename` as label) |
| `skill_listing` | `type, content, skillCount, isInitial` | `content` | `string` — newline-delimited list of skill names and descriptions | No | `content` (with `skillCount` as metadata) |
| `command_permissions` | `type, allowedTools` | `allowedTools` | `string[]` — tool name strings (empty array `[]` observed) | No | `allowedTools.length ? allowedTools.join(', ') : '(none)'` |
| `deferred_tools_delta` | `type, addedNames, addedLines, removedNames, readdedNames, pendingMcpServers` | `addedNames` + `removedNames` | `string[]` each — tool name strings | No | Summary: `+${addedNames.length} tools, -${removedNames.length} tools`; detail: `addedNames.join(', ')` |
| `mcp_instructions_delta` | `type, addedNames, addedBlocks, removedNames` | `addedBlocks` | `string[]` — each element is a full MCP server instruction block (markdown) | No | `addedNames.join(', ')` as label; `addedBlocks.join('\n---\n')` as body |

**Notes:**

[OBS] `hook_cancelled`: No `content`, `stdout`, or `stderr` fields. The record is purely metadata confirming a hook ran but was cancelled before producing output. The renderer has nothing to display as body text — it should render as a collapsed "cancelled" badge with `hookName` and `hookEvent`.

[OBS] `nested_memory`: The double-nested `content.content` is not a mistake. The outer `content` object carries provenance (`path`, `type`, `contentDiffersFromDisk`); the inner `content` string is the actual CLAUDE.md body text. `displayPath` (e.g. `"src/CLAUDE.md"`) is a relative display label, not an absolute path.

[OBS] `hook_success`: `content` field is always `""` (empty string). `stdout` is the real payload and may be empty-string when the hook produced no output. Parse defensively: `stdout` is not guaranteed to be valid JSON.

[OBS] `task_reminder`: `content` is an array of task objects, not strings. Each object has 7 fields. `description` contains the full task body (may be multi-line markdown); `subject` is the one-line title. `activeForm` is a gerund phrase ("Listing branches") suitable for display headers. `itemCount` equals `content.length`.

[A] `command_permissions.allowedTools` was `[]` in the single observed record. It may contain tool names when permissions are actually granted. Risk-if-wrong: rendering it as "(none)" when names are present would hide real permissions.

[A] `deferred_tools_delta.addedLines` appeared identical to `addedNames` in the observed record. Its distinct purpose (if any) is unknown. Risk-if-wrong: if they diverge in other records, using `addedNames` for display may omit info that `addedLines` carries.

Research status: RQ-8 COMPLETE
