# Trace: Sidebar Session List — Entry to Render

## Data Flow (Backend → Frontend)

```
ProjectScanner.listSessionsPaginated()     ← reads ~/.claude/projects/{encoded}/
        │
        ▼
IPC: 'get-sessions-paginated'              ← src/main/ipc/sessions.ts:48
        │
        ▼
preload: ipcRenderer.invoke(...)           ← src/preload/index.ts:132
        │
        ▼
api.getSessionsPaginated()                 ← called by store
        │
        ▼
sessionSlice.fetchSessionsInitial()        ← src/renderer/store/slices/sessionSlice.ts:124
  → set({ sessions: result.sessions })     ← line 140
  → loadPinnedSessions()                   ← line 159
  → loadHiddenSessions()                   ← line 160
        │
        ▼
DateGroupedSessions component              ← src/renderer/components/sidebar/DateGroupedSessions.tsx:53
```

## Filtering Pipeline (in DateGroupedSessions)

All filtering happens client-side in `DateGroupedSessions.tsx` via `useMemo` chains:

```
sessions (from store)                      ← line 55, raw session array
    │
    ▼
visibleSessions = sessions.filter(         ← line 112-115
  s => !hiddenSet.has(s.id)                   hidden toggle: show/hide hidden
)
    │
    ├─→ pinnedSessions                     ← line 118-121 (separated out)
    │
    ├─→ unpinnedSessions                   ← line 118-121
    │       │
    │       ▼
    │   groupedSessions = groupByDate()    ← line 124
    │       │
    │       ▼
    │   nonEmptyCategories                 ← line 127-130
    │
    └─→ contextSortedSessions             ← line 133-138 (alt sort mode)
            │
            ▼
        virtualItems                       ← line 141 (flattened for virtualizer)
            │
            ▼
        rowVirtualizer (TanStack Virtual)  ← line 235-240
            │
            ▼
        RENDERED SESSION LIST
```

## Current Filter Mechanisms

| Mechanism | Where | How |
|-----------|-------|-----|
| **Hide** | `hiddenSessionIds` in store (persisted to config) | Toggle per-session, bulk hide. Filter in `visibleSessions` memo |
| **Pin** | `pinnedSessionIds` in store (persisted to config) | Pinned sessions shown in separate section above date groups |
| **Sort** | `sessionSortMode` in store | 'recent' (default) or 'most-context' |

## Key Types

```typescript
// Session item (simplified)
interface SessionSummary {
  id: string;
  label: string;          // first user message preview
  timestamp: number;       // last modified
  contextConsumption?: number;
}

// Virtual list item (union type at line 36)
type VirtualItem =
  | { type: 'session'; session: SessionSummary; isPinned; isHidden }
  | { type: 'header'; id: string }
  | { type: 'pinned-header'; id: string }
  | { type: 'date-header'; id: string; category: DateCategory }
  | { type: 'hidden-toggle'; id: string }
  | { type: 'load-more'; id: string }
```

## Where a Filter Feature Would Plug In

**Insertion point:** Between `sessions` (store) and `visibleSessions` (line 112).

Current flow:
```
sessions → filter out hidden → visibleSessions
```

With filter:
```
sessions → apply user filter → filter out hidden → visibleSessions
```

### What needs changing:

1. **Store** (`sessionSlice.ts`): Add `sessionFilter` state (string/regex/predicate) and `setSessionFilter` action
2. **DateGroupedSessions.tsx** line 112: Add filter step before hidden filter
3. **Sidebar UI**: Add filter input above session list (search bar or dropdown)
4. **Key decision**: Filter by what? Options:
   - Session label text (substring match)
   - Date range
   - Token usage threshold
   - Regex on first message
   - Tags/labels (would need new metadata)

### Files to modify:
- `src/renderer/store/slices/sessionSlice.ts` — state + action
- `src/renderer/components/sidebar/DateGroupedSessions.tsx` — filter logic + UI
- `src/renderer/store/types.ts` — SessionSlice type update (if needed)
