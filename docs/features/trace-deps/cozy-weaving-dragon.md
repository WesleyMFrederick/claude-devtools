# Plan: `trace-deps` — Deterministic Dependency Tracer

## Bootstrap Instructions

To resume this plan in a new session:

1. **Load skills:**
   - `/evidence-ontology` — canonical tag definitions ([OBS], [H], [F-ID], etc.)
   - `/continuous-learning` — [O] outcome format and BID table structure

2. **Load conversation context** via `/searching-transcripts`:
   ```
   /searching-transcripts --dir ~/.claude/projects/-Users-wesleyfrederick-Documents-ObsidianVault-0-SoftwareDevelopment-claude-devtools --file 1476793d-a02f-4a92-817e-2f314b16817c.jsonl
   ```
   Key search terms: `"trace-deps"`, `"deterministic"`, `"BI table"`, `"#USER-FRICTION"`

3. **Read this plan file** — it is the self-contained state file. All decisions, findings, and BI table are inline below.

4. **Read key reference files:**
   - `ARCHITECTURE-PRINCIPLES.md` L102-109 — Deterministic Offloading Principles
   - `docs/traces/20260323-sidebar-filter-baseline.md` — the trace this tool replaces
   - `docs/traces/20260323-sidebar-trace-methodology.md` — 15-step methodology being automated
   - `docs/traces/20260323-deterministic-trace-analysis.md` — deterministic vs. semantic classification

5. **Resume at current state:** CL phases b, b.1, c, d complete. Hard gate [e2] (BI table lock) pending.

## Context

When tracing a codebase feature path (e.g., "how does sidebar filtering work?"), the agent makes ~33 LLM tool calls (LSP, Read, Grep, Glob). 73% are fully deterministic. LSP fails 30% of the time on barrel re-exports (`export * from`). This tool replaces the deterministic portion with a single CLI invocation that outputs a structured dependency graph.

**Goal:** 33 tool calls → 1 tool call + LLM synthesis. ~60s → <5s. 30% failure rate → 0%.

**Architecture grounding:** Deterministic Offloading Principles (`ARCHITECTURE-PRINCIPLES.md:102-109`):
- **Mechanical Separation**: Route deterministic tasks (I/O, parsing, search) to tools
- **Focused Context**: Fill LLM context with semantic info, not mechanical I/O
- **Tool-First Design**: Build specialized tools for repetitive operations
- **No Surprises**: Identical inputs must yield consistent results

---

## Files to Create

| File | Purpose |
|------|---------|
| `scripts/trace-deps.ts` | Main CLI script (~250 lines) |
| `scripts/trace-deps-types.ts` | Output schema types |
| `test/scripts/trace-deps.test.ts` | Tests |

## Files to Modify

| File | Change |
|------|--------|
| `package.json` | Add `ts-morph` devDep + `"trace-deps"` script |

---

## Implementation

### Step 1: Add ts-morph

```bash
pnpm add -D ts-morph
```

ts-morph wraps the TypeScript compiler API. It resolves path aliases and barrel re-exports natively from `tsconfig.json` — eliminates the LSP failure mode entirely.

### Step 2: Output Schema (`scripts/trace-deps-types.ts`)

```typescript
interface TraceDepsOutput {
  entry: string;
  depth: number;
  fileCount: number;
  files: Record<string, FileNode>;
  storeConnections: StoreConnection[];
  apiCalls: ApiCall[];
}

interface FileNode {
  path: string;
  depth: number;
  imports: string[];
  importedBy: string[];
  exports: ExportedSymbol[];
  rendersComponents: string[];
  isBarrel: boolean;
}

interface ExportedSymbol {
  name: string;
  kind: 'function' | 'class' | 'interface' | 'type' | 'const' | 'enum' | 'component';
  line: number;
  signature?: string;     // compact: "(a: string) => void"
  fields?: string[];      // interface field NAMES only (saves tokens)
}

interface StoreConnection {
  file: string;
  fields: string[];
  shallow: boolean;
}

interface ApiCall {
  file: string;
  method: string;
  line: number;
}
```

**Token budget:** Interfaces list field names only, not types. Barrel files omit exports. Target ~3K tokens for depth-2 traversal.

### Step 3: Main Script (`scripts/trace-deps.ts`)

**CLI:**
```
pnpm trace-deps --entry <file> [--depth N] [--compact]
```

- `--depth N` (default 2): BFS depth. `-1` = full transitive closure.
- `--compact`: Omit exports for files at depth > 1 (for large traversals).

**Algorithm — BFS traversal:**

```
1. Create ts-morph Project from tsconfig.json
2. Resolve entry file
3. BFS queue with depth counter:
   - For each file:
     a. Extract imports (resolve path aliases + barrel chains)
     b. Extract exported symbols (name, kind, line, fields)
     c. Detect JSX component renders (<Component />)
     d. Detect useStore() calls → extract state field names
     e. Detect api.* calls → extract method names
     f. Queue imported files if within depth limit
   - Barrel files don't increment depth (they add no logic)
   - Skip: node_modules, CSS/JSON imports, dynamic imports
4. Backfill importedBy edges
5. Output JSON to stdout
```

**Key detection patterns:**

| Pattern | ts-morph Method |
|---------|----------------|
| Imports | `sourceFile.getImportDeclarations()` |
| Exports | `sourceFile.getExportedDeclarations()` |
| Barrel detection | All statements are ExportDeclarations |
| JSX renders | `getDescendantsOfKind(SyntaxKind.JsxSelfClosingElement)` |
| useStore fields | CallExpression where callee is `useStore`, walk arrow body for `s.fieldName` property access |
| API calls | CallExpression where callee matches `api.*` pattern |
| Re-export resolution | ts-morph handles natively via TypeScript module resolution |

### Step 4: Package.json

```json
"trace-deps": "tsx scripts/trace-deps.ts"
```

### Step 5: Tests (`test/scripts/trace-deps.test.ts`)

| Test | Assertion |
|------|-----------|
| Barrel resolution | `src/shared/types/index.ts` → resolves through to `src/main/types/domain.ts` |
| Path alias resolution | `@main/types` → `src/main/types/index.ts` |
| JSX detection | `DateGroupedSessions.tsx` → `rendersComponents` includes `SessionItem` |
| Store connection | `DateGroupedSessions.tsx` → fields include `sessions`, `selectedSessionId` |
| Depth limit | depth=0 → only entry file; depth=1 → entry + direct imports |
| API call detection | Component calling `api.getSessionsPaginated()` appears in `apiCalls` |
| Circular import safety | BFS visited set prevents infinite loops |

---

## Verification

1. **Probe test:** `pnpm trace-deps --entry src/renderer/components/sidebar/DateGroupedSessions.tsx --depth 1` — verify JSON output includes SessionItem, dateGrouping, store connection with expected fields
2. **Barrel test:** `pnpm trace-deps --entry src/renderer/types/data.ts --depth 3` — verify Session interface resolves to `src/main/types/domain.ts:81` with field names
3. **Run tests:** `pnpm vitest run test/scripts/trace-deps.test.ts`
4. **Token budget:** Pipe output through `wc -c` — should be <12KB for depth-2 on DateGroupedSessions

---

## Edge Cases

- **Dynamic imports:** Log warning, skip (not deterministically resolvable)
- **Type-only imports:** Include in graph (reveal type deps)
- **CSS/JSON imports:** Silently skip
- **node_modules:** Exclude from graph (only `src/` files)
- **Large traversals:** `--compact` flag omits exports at depth > 1

---

## Continuous Learning Analysis

### Artifacts

| Artifact | Path | Role |
|----------|------|------|
| Session transcript | (current session) | Primary evidence for friction patterns |
| Sidebar filter trace | `docs/traces/20260323-sidebar-filter-baseline.md` | Output showing 33-call methodology |
| Methodology trace | `docs/traces/20260323-sidebar-trace-methodology.md` | Meta-trace classifying each call |
| Deterministic analysis | `docs/traces/20260323-deterministic-trace-analysis.md` | Classification scorecard + architecture |
| CLAUDE.md (global) | `~/.claude/CLAUDE.md` | Contains LSP-first rule (L58-67) |
| Learnings #1, #8, #9 | Session context | Prior corrections driving trace methodology |
| Architecture Principles | `ARCHITECTURE-PRINCIPLES.md` | Deterministic Offloading Principles (L102-109) ground the tool's rationale: Mechanical Separation, Focused Context, Tool-First Design, No Surprises |
| Continuous Learning skill | `.claude/skills/continuous-learning/SKILL.md` | Defines [O] outcome format, BI/BDI table structure, and phased workflow used to derive this plan's CL analysis |
| Evidence Ontology skill | `.claude/skills/evidence-ontology/SKILL.md` | Dependency: loads ontology tags ([OBS], [H], [F-ID], etc.) into context. Required by CL skill for tag grounding |
| Evidence Ontology reference | `.claude/skills/evidence-ontology/references/EVIDENCE-ONTOLOGY.md` | Canonical tag definitions and rules referenced by both skills |

### Findings

| ID | Pattern Found | Scope | Trigger | Friction Caused |
|----|--------------|-------|---------|-----------------|
| F1 | Agent makes 33 LLM tool calls for a task that is 73% deterministic | Codebase tracing | Any "trace how X works" request | ~60s latency, ~15K context tokens on mechanical I/O, 30% LSP failure on barrel re-exports |
| F2 | LSP goToDefinition fails on barrel re-exports, requiring 5 extra Grep/Read fallback calls | TS symbol resolution | Import chain through barrel files | 15% of all tool calls were recovery from this single failure mode |
| F3 | Agent chooses which files to read (semantic), but traversal itself is mechanical BFS | Trace methodology | Entry file identified → need dependency graph | LLM context spent on "what next" decisions a graph walker handles deterministically |
| F4 | Agent guessed wrong path for Sidebar.tsx, requiring recovery | File discovery | Component not at expected directory | Wasted tool call + recovery; ts-morph project index finds it instantly |
| F5 | Output trace requires LLM to synthesize 2,400 lines into structured narrative | Trace writing | All source read → need coherent document | CORRECT use of LLM — validates synthesis stays with LLM (untargeted row) |

### BI Table

| # | Baseline [O] | Ideal [O] |
|---|-------------|-----------|
| 1 | Agent can trace a codebase feature path by making ~33 LLM tool calls across LSP, Read, Grep, and Glob | Agent can trace a codebase feature path with a single deterministic tool call plus LLM synthesis |
| 2 | Agent can resolve TypeScript import chains by falling back to Grep when LSP fails on barrel re-exports | Agent can resolve TypeScript import chains with zero failures regardless of barrel re-export depth |
| 3 | Agent can discover which files to read by making sequential judgment calls about directory structure | Agent can discover all files in a dependency graph without guessing directory structure |
| 4 | Agent can build structured trace documents from raw source code | Agent can build structured trace documents from raw source code |
| 5 | Agent can identify store connections, JSX renders, and API calls by reading source and applying judgment | Agent can identify store connections, JSX renders, and API calls from a pre-computed structured graph |

Row 4 is untargeted — LLM synthesis is the correct tool for narrative writing. No delta needed.
