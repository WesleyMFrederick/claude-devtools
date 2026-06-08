# Architecture Compliance Eval: feat/advisor-display
%% *Last Modified: 06/08/26 11:27:17* %%

## Evaluation Metadata
%% *Last Modified: 06/08/26 11:27:17* %%

| Field | Value |
|---|---|
| Reviewer Role | Architecture compliance reviewer — object-oriented systems |
| Domain Vocabulary | modularity, single responsibility, coupling, cohesion, data-first design, discriminated union, type guard, interface segregation, format/interface design, MVP / minimum code / no speculation, deterministic offloading, self-contained naming, BECAUSE-clauses, safety-first, graceful degradation, null-guarding, anti-pattern, god object, special-case branching, parallel pipelines, two-process Electron (main/renderer), semantic steps, tool linking, token counting, server_tool_use, advisor_tool_result |
| Principle Set | object-oriented |
| Principle Set Resolution | All changed files are `.ts`/`.tsx`. No Effect imports. OO paradigm confirmed — load both core + OO deltas. |
| Graduated Loading | Phase 1: 14 category headings enumerated. Phase 2: core doc 14,686 chars; OO doc 8,301 chars — both loaded in full. |
| Output Path | `/Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools/feat-advisor-display-eval-report.md` |
| Files Evaluated | `src/main/types/jsonl.ts`, `src/main/types/messages.ts`, `src/main/utils/jsonl.ts`, `src/main/services/analysis/SemanticStepExtractor.ts`, `src/renderer/utils/displayItemBuilder.ts`, `src/renderer/utils/toolLinkingEngine.ts`, `src/renderer/components/chat/items/LinkedToolItem.tsx`, `src/renderer/components/chat/items/linkedTool/renderHelpers.tsx`, `src/renderer/utils/stringUtils.ts`, `test/mocks/advisorBlocks.fixture.ts`, `test/main/services/analysis/SemanticStepExtractor.test.ts`, `test/renderer/utils/displayItemBuilder.test.ts`, `test/renderer/utils/renderHelpers.test.ts`, `test/renderer/utils/stringUtils.test.ts`, `test/renderer/utils/toolLinkingEngine.test.ts`, `test/renderer/utils/toolRendering/toolTokens.test.ts` |
| TodoWrite Categories | Modular Design Principles, Data-First Design Principles, Action-Based File Organization, Format/Interface Design, Minimum Viable Product (MVP) Principles, Deterministic Offloading Principles, Self-Contained Naming Principles, Safety-First Design Patterns, Anti-Patterns to Avoid, OO Modularity Principles, OO Architectural Patterns, OO Operational Safety, OO Documentation Strategy, OO-Specific Anti-Patterns |

---

## Architecture Evaluation: feat/advisor-display
%% *Last Modified: 06/08/26 11:27:17* %%

### Principle Compliance
%% *Last Modified: 06/08/26 11:27:17* %%

| Category | Status | Details |
|---|---|---|
| **Modular Design Principles** | ✅ Compliant | Each file touches one concern. `SemanticStepExtractor.ts` handles main-process semantic extraction; `displayItemBuilder.ts` handles renderer display construction; `toolLinkingEngine.ts` handles call/result pairing. No cross-process coupling introduced. `capitalize` extracted to `stringUtils.ts` for DRY reuse. The `sourceModel` field threads across the pipeline through clean data handoff (not shared mutable state). |
| **Data-First Design Principles** | ✅ Compliant | `ServerToolUseContent` and `AdvisorToolResultContent` are added as named interfaces to the `ContentBlock` discriminated union (jsonl.ts:76–96). The discriminant is the `type` field — same pattern as all existing members. `advisorModel?: string` on `AssistantEntry` (jsonl.ts:203) and `ParsedMessage` (messages.ts:81) follows the optional-field pattern for entries that may or may not carry this data. `block.content?.text ?? ''` null-guard preserves the "illegal states unrepresentable" intent — the advisory text can be missing at the edge and defaults safely. |
| **Action-Based File Organization** | ✅ Compliant | No new files are created except `test/mocks/advisorBlocks.fixture.ts` (a fixture, correctly placed) and `test/main/services/analysis/SemanticStepExtractor.test.ts` (new test file, correctly co-located with its subject). All source changes land in existing files whose names already match the action they perform. |
| **Format/Interface Design** | ✅ Compliant | `ServerToolUseContent.input` is typed `Record<string, unknown>` (jsonl.ts:80) — narrow enough to be useful, permissive enough not to over-specify. `AdvisorToolResultContent.content` is typed as a literal object `{ type: 'advisor_result'; text: string }` (jsonl.ts:86), which is appropriately specific. Interface segregation is maintained: no existing interface is widened unnecessarily. |
| **Minimum Viable Product (MVP) Principles** | ➖ Gap noted | The change ships exactly what is needed to render advisor calls and results. No speculative fields are added. However, the special-case branch `name === 'advisor'` in `toolLinkingEngine.ts:86` and `displayItemBuilder.ts:462` encodes a hard-coded tool name rather than a data-driven dispatch, which is minimum code *today* but creates a residual maintenance surface. See Critical Issues §1 for the full verdict — this is a nuanced MVP/scope trade-off. |
| **Deterministic Offloading Principles** | ✅ Compliant | `capitalize` is extracted as a pure, deterministic helper in `stringUtils.ts:32–35` with documented behavior and three call sites. Token counting for advisor results delegates to `countContentTokens` (SemanticStepExtractor.ts:68), the same deterministic function used for all other content — no bespoke estimation is introduced. |
| **Self-Contained Naming Principles** | ✅ Compliant | `ServerToolUseContent`, `AdvisorToolResultContent`, `advisorModel`, `capitalize` — all names are self-explanatory without lookup. The `capitalize` JSDoc carries `@example` clauses explaining exactly what it does and why (stringUtils.ts:25–31). The comment `// advisor CALL — input is empty so callTokens stay undefined (fallback estimates ~0)` (SemanticStepExtractor.ts:94) explains the rationale, which is the correct use of comments per the Self-Documenting Code First sub-principle. |
| **Safety-First Design Patterns** | ✅ Compliant | Null-guard `block.content?.text ?? ''` appears in both extraction pipelines: SemanticStepExtractor.ts:113 and displayItemBuilder.ts:473. Consistent across both process boundaries. Zero-token fallback when `advisorText` is empty (SemanticStepExtractor.ts:68) prevents NaN or undefined token counts from propagating. `capitalize('')` returns `''` safely (stringUtils.ts:33). All new discriminated-union arms are exhausted in the consuming code before any property access. |
| **Anti-Patterns to Avoid** | ➖ Partial gap | The `name === 'advisor'` branch pattern appears four times (SemanticStepExtractor.ts:93, displayItemBuilder.ts:462, toolLinkingEngine.ts:86, LinkedToolItem.tsx:70). This is **not** the same as scattered invariant checks — each instance has a different responsibility and a legitimate reason to exist at process boundaries. However, it approaches the "branch explosion" anti-pattern in aggregate. See Critical Issues §1. No scattered checks on the *same invariant*; no leaky flags; no hidden global state introduced. |
| **OO Modularity Principles** | ✅ Compliant | No new classes or inheritance added. The change is function-level (pure extractors, pure renderers). Dependencies are not constructed inside consumers — `capitalize` is imported via module reference. `advisorModel` is passed through data, not via service locator. Composition-over-inheritance is preserved throughout. |
| **OO Architectural Patterns** | ✅ Compliant | Service layer separation is respected: parsing lives in `jsonl.ts` (data access layer), semantic extraction in `SemanticStepExtractor.ts` (service layer), display construction in `displayItemBuilder.ts` (presentation layer), UI rendering in `LinkedToolItem.tsx` (view). The advisor feature threads through all layers without violating this boundary structure. |
| **OO Operational Safety** | ➖ Not mentioned | Backup creation and dry-run capability are not relevant to a read-only rendering feature. Idempotent operations: `linkToolCallsToResults` builds a `Map` from steps — re-running on the same input yields the same map (idempotent). No state mutation introduced. N/A for backup/dry-run. |
| **OO Documentation Strategy** | ✅ Compliant | `capitalize` has a JSDoc block with `@example` annotations (stringUtils.ts:24–31). `advisorModel` has inline JSDoc on both `AssistantEntry` (jsonl.ts:203) and `ParsedMessage` (messages.ts:80). The `renderInput` docblock is updated to document the new empty-input behavior (renderHelpers.tsx:17–19). `ServerToolUseContent` and `AdvisorToolResultContent` are exported interfaces with clear names. Selective documentation standard met. |
| **OO-Specific Anti-Patterns** | ✅ Compliant | No god class introduced. No inheritance added. No shared mutable state. No service locator usage. `toolCallsById` and `toolResultsById` in `displayItemBuilder.ts` are local `Map` instances, not module-level state. The fixture file uses `as unknown as ParsedMessage` casts correctly scoped to tests. |

---

### Critical Issues (Severity: High)
%% *Last Modified: 06/08/26 11:27:17* %%

**1. Special-case branching on `name === 'advisor'` — four independent sites**

Principle: `^branch-explosion` (Anti-Patterns to Avoid — "Replace deep if-else logic with declarative tables, pattern matching, or data-driven dispatch"), and `^behavior-as-data` (Data-First — "Represent rules or configs declaratively instead of in branching logic. Data-driven dispatch replaces switch statements").

Locations:
- `SemanticStepExtractor.ts:93` — `block.type === 'server_tool_use' && block.name === 'advisor'`
- `displayItemBuilder.ts:462` — `block.type === 'server_tool_use' && block.name === 'advisor'`
- `toolLinkingEngine.ts:86` — `toolName === 'advisor' ? undefined : estimateTokens(...)`
- `LinkedToolItem.tsx:70` — `linkedTool.name === 'advisor' ? (linkedTool.sourceModel ?? 'advisor') : getToolSummary(...)`

**Verdict — conditional pass, not a blocker.** Here is the full weighing:

*For hardcoding advisor today:*
- `server_tool_use` is a general Anthropic API block type, but `advisor` is the **only** `server_tool_use` name that actually appears in Claude Code JSONL as of this writing. There is no known second server tool to dispatch against. Building a generic `server_tool_use` registry before a second case exists is speculative engineering — a direct violation of `^implement-when-needed` (MVP, "Avoid implementing features until they are necessary").
- The four sites span two process boundaries (main/renderer) and different responsibility layers (parsing, token estimation, display). Each hardcode has a different *semantic reason* — they are not four checks on the same invariant; they are four independent decisions about how advisor differs from client tools.
- The null-guard comment at toolLinkingEngine.ts:84 ("advisor input is empty ({})") is a BECAUSE-clause that documents the *why*, satisfying `^self-documenting-code-first`.

*Against hardcoding advisor across shared infrastructure:*
- If a second `server_tool_use` name (e.g., `search`, `memory`) appears in JSONL, all four sites must be updated. There is no central registry to extend — this violates `^extension-over-modification` and `^behavior-as-data`.
- The `toolLinkingEngine.ts` branch (`toolName === 'advisor' ? undefined`) is the most fragile: it makes token suppression an *ad hoc* per-name decision. A data-driven approach would be a `noCallTokens: boolean` flag on the tool call step, derived once during extraction and consumed passively in the engine. This would eliminate the name-check from the engine and move the policy to the data layer.

**Net verdict:** The pattern is acceptable for an MVP scope with one server tool. It becomes a violation the moment a second `server_tool_use` name appears. The `toolLinkingEngine.ts` branch is the highest-priority refactor target because it embeds display-layer policy (token suppression) in a linking layer. The `LinkedToolItem.tsx` branch is the second-highest because it embeds summary-formatting policy in a rendering component rather than `getToolSummary`.

---

### Recommendations
%% *Last Modified: 06/08/26 11:27:17* %%

1. **Centralize `server_tool_use` dispatch policy** (ties to `^behavior-as-data`, `^extension-over-modification`): When a second `server_tool_use` name appears, extract a `SERVER_TOOL_CONFIGS` map keyed by tool name, encoding: `{ suppressCallTokens: boolean, getSummary: (tool) => string }`. All four hardcoded branches collapse to map lookups. Cost: 30 min when triggered. Do not build it now.

2. **Move token-suppression policy to the data layer** (ties to `^behavior-as-data`, `^shift-complexity-to-data`): In `SemanticStepExtractor.ts`, emit a `suppressCallTokens: true` flag (or `callTokens: 0`) on the advisor `tool_call` step rather than relying on `toolLinkingEngine.ts` to detect the name. The linking engine should read a data property, not branch on a name. Cost: ~15 min. See Fix Now §1.

3. **Move advisor summary logic into `getToolSummary`** (ties to `^single-responsibility`, `^modular-design-principles-definition`): `LinkedToolItem.tsx:70` contains display policy (`linkedTool.sourceModel ?? 'advisor'`) that belongs in `toolSummaryHelpers.ts`'s `getToolSummary`. The component should not know that advisor uses `sourceModel` as its summary string. Cost: ~15 min. See Fix Now §2.

4. **Add a type guard for `ServerToolUseContent`** (ties to `^illegal-states-unrepresentable`, `^explicit-relationships`): `jsonl.ts` exports type guards for `TextContent` and `ToolResultContent` but not for `ServerToolUseContent` or `AdvisorToolResultContent`. All four check sites currently use inline duck-typing. A `isServerToolUseContent` guard would be consistent with the existing pattern and make the union exhaustive. Cost: ~5 min. See Fix Now §3.

5. **Guard `advisorModel` comment on `ParsedMessage`** (ties to `^jsdoc-tsdoc-on-public-apis`): The comment on `messages.ts:80` reads "Advisor model, when this entry invoked /advisor." This is accurate but phrased as a noun fragment rather than a clear contract statement. It should clarify the source: "Model identifier from `entry.advisorModel` on `AssistantEntry`; populated only for advisor calls." Low priority but consistent with existing field-level docs. Cost: 2 min. See Fix Now §4.

---

### Prioritized Findings
%% *Last Modified: 06/08/26 11:27:17* %%

#### Fix Now
%% *Last Modified: 06/08/26 11:27:17* %%

| # | Finding | Principle | File:Line | Cost (min) | What to Change |
|---|---|---|---|---|---|
| 1 | Token-suppression policy in the linking layer (name-check) | `^behavior-as-data`, `^shift-complexity-to-data` | `toolLinkingEngine.ts:85–86` | 15 | Emit `callTokens: 0` (or add a `suppressCallTokens` property) on the advisor `tool_call` step in `SemanticStepExtractor.ts:93–109`. Remove the `toolName === 'advisor' ? undefined` branch from `toolLinkingEngine.ts:85–86` — the engine reads the pre-computed value from the step. |
| 2 | Summary policy for advisor in the rendering component | `^single-responsibility` | `LinkedToolItem.tsx:69–72` | 15 | Move `linkedTool.name === 'advisor' ? (linkedTool.sourceModel ?? 'advisor') : getToolSummary(...)` into `getToolSummary` in `toolSummaryHelpers.ts`. The component calls `getToolSummary` unconditionally. |
| 3 | Missing type guards for new `ContentBlock` union members | `^explicit-relationships`, `^illegal-states-unrepresentable` | `jsonl.ts` (post line 96) | 5 | Add `export function isServerToolUseContent(content: ContentBlock): content is ServerToolUseContent { return content.type === 'server_tool_use'; }` and `isAdvisorToolResultContent` parallel to existing `isTextContent` / `isToolResultContent`. |
| 4 | `advisorModel` field comment is a noun fragment | `^jsdoc-tsdoc-on-public-apis` | `messages.ts:80` | 2 | Reword to: `/** Advisor model identifier (from AssistantEntry.advisorModel); defined only when this message invoked the advisor tool. */` |

#### Architectural Rework Required
%% *Last Modified: 06/08/26 11:27:17* %%

None. All findings above are under 30 minutes. No rework scope with named trigger is required at this time. The `SERVER_TOOL_CONFIGS` map from Recommendation §1 is deferred *pending a second server tool name appearing in JSONL* — that is a concrete, named trigger. If it fires, Recommendation §1 becomes Fix Now.

#### Already Mitigated
%% *Last Modified: 06/08/26 11:27:17* %%

- **Null-guard on `block.content?.text`**: Both pipelines (SemanticStepExtractor.ts:113, displayItemBuilder.ts:473) apply `?? ''` consistently. Graceful degradation confirmed.
- **Phantom design-doc labels (D3/D4)**: Earlier versions of test comments referenced design-doc section numbers. The fixture file (advisorBlocks.fixture.ts) still contains inline `(D3)` and `(D4)` labels in test names (toolLinkingEngine.test.ts:56, displayItemBuilder.test.ts:565). These are residual label fragments from the cleanup noted in the branch history. They are now orphaned references — the design doc sections they referenced no longer exist as numbered items. This is cosmetic, not a principle violation, but it is noise. Removal is a 2-min tidy. Not blocking.
- **`capitalize` helper extraction**: Correctly extracted to `stringUtils.ts` with TSDoc, reused at three call sites. No duplication. `^avoid-duplication` satisfied.
- **Process-boundary duplication in advisor block handling**: SemanticStepExtractor (main) and displayItemBuilder (renderer) each contain advisor block handling. This is **not** a DRY violation — it is the correct Electron two-process architecture. The main process cannot share renderer code and vice versa. The shared fixture (`advisorBlocks.fixture.ts`) covers both pipelines in tests. `^loose-coupling-tight-cohesion` satisfied.

---

### Document Hygiene
%% *Last Modified: 06/08/26 11:27:17* %%

| Area | Status |
|---|---|
| H1 Evidence tags ([OBS], [H], [A], etc.) | ➖ N/A — Code diff, not a markdown evidence-tagged document |
| H2 Source footnotes (transcript path:line) | ➖ N/A — Code diff, not a markdown evidence-tagged document |
| H3 ALWAYS/BECAUSE clause format | ➖ N/A — Code diff, not a markdown evidence-tagged document |

---

### Verdict
%% *Last Modified: 06/08/26 11:32:09* %%

- [x] **Ready to proceed** (with Fix Now items recommended before merge)
- [ ] Requires revision

---

## Resolution (applied 06/08/26)
%% *Last Modified: 06/08/26 11:32:09* %%

Fix Now bucket actioned by the parent agent (Opus 4.8). Typecheck clean, 24 affected tests pass.

| # | Finding | Action | Reason |
|---|---|---|---|
| 2 | Advisor summary policy in the component | ✅ **Fixed** | Added optional `sourceModel?` param + `case 'advisor'` to `getToolSummary` (`toolSummaryHelpers.ts`); `LinkedToolItem.tsx` now calls it unconditionally. Backward-compatible — only LinkedToolItem calls the renderer copy. |
| 4 | `advisorModel` field comment is a noun fragment | ✅ **Fixed** | Reworded to a full sentence (`messages.ts:80`). |
| — | Orphaned `(D2)/(D3)/(D4)` test-name labels | ✅ **Fixed** | Stripped from 5 test names across 3 files (dead design-doc references). |
| 1 | Token-suppression in the linking layer | ⏭️ **Skipped — genuinely expensive** | The correct data-first fix rewires the engine to read pre-computed step tokens for *every* tool, with token-count regression risk app-wide. That is >30 min with a real test surface — a true deferral, not scope-dodging. Name-check + clear comment retained. **Trigger to revisit:** when the engine's token-sourcing is refactored, or a second `server_tool_use` name appears. |
| 3 | Missing type guards for new union members | ⏭️ **Skipped — eval premise was factually wrong** | Verified: only 2 of 5 original `ContentBlock` members have guards (`isTextContent`, `isToolResultContent`), and only because they are *used* (`.filter(isTextContent)`, `isToolResultContent(block)`). The convention is "add a guard when you need to narrow," not "one per member." The advisor code uses inline `block.type === ...` checks and needs no guard — adding unused guards would be speculative dead code (MVP violation). |

**Carried forward (already in this report, unchanged):** the `SERVER_TOOL_CONFIGS` map (Recommendation §1) stays deferred pending a second `server_tool_use` name in the JSONL corpus — concrete, named trigger.

The branch is architecturally sound for its MVP scope. The four `name === 'advisor'` special-case branches are the dominant risk, but they are justified by the absence of any other `server_tool_use` name in the JSONL corpus today. Two of the four instances (toolLinkingEngine.ts, LinkedToolItem.tsx) can and should be cleaned up in the current PR — they are 15-minute fixes that move policy to the correct layer (data layer and summary helper). The other two (SemanticStepExtractor, displayItemBuilder) are structural necessities at the process boundary and cannot be eliminated without speculation. Type guards for the new union members and the field comment reword are minor hygiene items that cost under 10 minutes combined and should ship with the branch.
