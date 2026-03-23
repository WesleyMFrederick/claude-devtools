# Sidebar Session Filtering — Baseline Trace

**Date:** 2026-03-23
**Purpose:** Full entry-to-exit trace of the sidebar session list pipeline, covering data types, store state, filtering/grouping logic, component tree, user interactions, and real-time update paths. This is the baseline for adding session type, model, and date filters.

---

## 1. Data Types

### Session (`src/main/types/domain.ts:81-112`)
[OBS: Read directly from source]

```typescript
export interface Session {
  id: string;                          // Session UUID
  projectId: string;                   // Parent project ID
  projectPath: string;                 // Filesystem path
  todoData?: unknown;                  // Task list data
  createdAt: number;                   // Unix timestamp
  firstMessage?: string;               // Preview text
  messageTimestamp?: string;           // RFC3339
  hasSubagents: boolean;               // Subagent flag
  messageCount: number;                // Total messages
  isOngoing?: boolean;                 // Still running?
  gitBranch?: string;                  // Git branch
  metadataLevel?: SessionMetadataLevel; // 'light' | 'deep'
  contextConsumption?: number;         // Compaction-aware token sum
  compactionCount?: number;            // Compaction events
  phaseBreakdown?: PhaseTokenBreakdown[]; // Per-phase tokens
}
```

**Key observation for new filters:**
- [OBS] No `model` field exists on Session. Model info lives inside the JSONL messages, extracted per-session only at detail level.
- [OBS] No `sessionType` field exists (e.g., team session, solo, subagent). `hasSubagents` is the closest boolean.
- [OBS] `createdAt` is present — date filtering already has data to work with.

### SessionSortMode (`src/renderer/types/data.ts:77`)
[OBS] `type SessionSortMode = 'recent' | 'most-context';`

### DateCategory (`src/renderer/types/tabs.ts:127`)
[OBS] `type DateCategory = 'Today' | 'Yesterday' | 'Previous 7 Days' | 'Older';`

### DateGroupedSessions (`src/renderer/types/tabs.ts:132`)
[OBS] `type DateGroupedSessions = Record<DateCategory, Session[]>;`

---

## 2. Store Layer — sessionSlice

**File:** `src/renderer/store/slices/sessionSlice.ts`

### State Shape (Lines 24-44)
[OBS] Key state fields for filtering:

| Field | Type | Purpose |
|-------|------|---------|
| `sessions` | `Session[]` | Full loaded session list |
| `sessionsLoading` | `boolean` | Initial load indicator |
| `sessionsHasMore` | `boolean` | Pagination flag |
| `sessionsCursor` | `string \| null` | Cursor for next page |
| `sessionsLoadingMore` | `boolean` | Page load indicator |
| `pinnedSessionIds` | `string[]` | User-pinned sessions |
| `hiddenSessionIds` | `string[]` | User-hidden sessions |
| `showHiddenSessions` | `boolean` | Toggle hidden visibility |
| `sessionSortMode` | `SessionSortMode` | 'recent' or 'most-context' |
| `sidebarMultiSelectActive` | `boolean` | Multi-select mode |
| `sidebarSelectedSessionIds` | `string[]` | Checked sessions |

### Data Fetch Actions

| Action | Line | Description |
|--------|------|-------------|
| `fetchSessionsInitial` | 124 | Fetches first page (20 sessions), then loads pinned/hidden |
| `fetchSessionsMore` | 170 | Loads next page via cursor, deduplicates |
| `refreshSessionsInPlace` | 258 | Real-time refresh without loading state (generation-guarded) |
| `loadPinnedSessions` | 332 | Reads config, fetches missing pinned sessions beyond page |
| `loadHiddenSessions` | 447 | Reads config for hidden session IDs |

### Filtering Actions (client-side only)

| Action | Line | Description |
|--------|------|-------------|
| `setSessionSortMode` | 372 | Sets 'recent' or 'most-context' |
| `toggleShowHiddenSessions` | 467 | Toggles hidden session visibility |
| `toggleHideSession` | 377 | Optimistic hide/unhide single session |
| `hideMultipleSessions` | 406 | Bulk hide (optimistic) |
| `unhideMultipleSessions` | 427 | Bulk unhide (optimistic) |

[F-ID: All filtering is client-side. The store holds the raw `sessions[]` array; the component applies filters via `useMemo`. No server-side filtering exists in the paginated API.]

---

## 3. API / IPC Layer

### Paginated Fetch (`src/preload/index.ts:132`)
[OBS] `getSessionsPaginated(projectId, cursor, limit, options)` → `PaginatedSessionsResult`

Options include:
- `includeTotalCount: boolean`
- `prefilterAll: boolean`
- `metadataLevel: 'light' | 'deep'`

[F-ID: The API returns sessions with `metadataLevel: 'light'` for the sidebar. Light metadata does NOT include model info. Adding a model filter would require either: (a) enriching light metadata with model, or (b) server-side filtering.]

---

## 4. Component Tree — Entry to Exit

### 4.1 TabbedLayout (`src/renderer/components/layout/TabbedLayout.tsx:23`)
[OBS] Root layout. Renders `<Sidebar />` alongside `<PaneContainer />`.

```
TabbedLayout
├── CustomTitleBar
├── UpdateBanner
├── CommandPalette
├── Sidebar          ← entry point
└── PaneContainer
```

### 4.2 Sidebar (`src/renderer/components/layout/Sidebar.tsx:26`)
[OBS] Shell component. Reads `projects`, `projectsLoading`, `sidebarCollapsed` from store. Renders:

```
Sidebar (width: 200-500px, resizable)
├── SidebarHeader     ← project/worktree selection
├── DateGroupedSessions ← session list (overflow-hidden container)
└── Resize handle
```

- Returns `null` when `sidebarCollapsed === true`
- Fetches projects on mount if empty

### 4.3 SidebarHeader (`src/renderer/components/layout/SidebarHeader.tsx:197`)
[OBS] Two-row header:
- **Row 1:** Project name dropdown (selects project → triggers session fetch)
- **Row 2:** Worktree selector (grouped mode only)

Store reads: `repositoryGroups`, `selectedRepositoryId`, `selectedWorktreeId`, `viewMode`, `projects`, `activeProjectId`

Actions: `selectWorktree`, `selectRepository`, `setActiveProject`, `toggleSidebar`

[F-ID: Project/worktree selection drives which sessions load. A new filter bar would logically sit between SidebarHeader and DateGroupedSessions, or as a sub-header within DateGroupedSessions.]

### 4.4 DateGroupedSessions (`src/renderer/components/sidebar/DateGroupedSessions.tsx:53`)
[OBS] **This is the core filtering and rendering component.** ~590 lines.

#### Store Reads (Lines 54-101)
Reads 20+ fields from store via `useShallow`:
- Session data: `sessions`, `selectedSessionId`, `selectedProjectId`
- Loading: `sessionsLoading`, `sessionsError`, `sessionsHasMore`, `sessionsLoadingMore`
- Filtering: `pinnedSessionIds`, `hiddenSessionIds`, `showHiddenSessions`, `sessionSortMode`
- Actions: `fetchSessionsMore`, `setSessionSortMode`, `toggleShowHiddenSessions`, multi-select actions

#### Filtering Pipeline (Lines 108-138)
**This is the critical path where new filters would be inserted:**

```
sessions (raw from store)
    │
    ▼
hiddenSet = new Set(hiddenSessionIds)              // Line 108
    │
    ▼
visibleSessions = sessions.filter(                  // Line 112-115
    s => showHiddenSessions || !hiddenSet.has(s.id)
)
    │
    ├─── if sortMode === 'most-context' ──────────►  contextSortedSessions  // Line 133-138
    │                                                  (sorted by contextConsumption desc)
    │
    ▼
{ pinned, unpinned } = separatePinnedSessions(     // Line 118-121
    visibleSessions, pinnedSessionIds
)
    │
    ▼
groupedSessions = groupSessionsByDate(unpinnedSessions)  // Line 124
    │
    ▼
nonEmptyCategories = getNonEmptyCategories(groupedSessions)  // Line 127-129
```

[F-ID: **New filters should be inserted between `visibleSessions` and `separatePinnedSessions`.** This is the single point where all sessions pass through before being split into pinned/unpinned and date-grouped. A filtered set at this stage would propagate correctly to both the date-grouped view and the context-sorted view.]

#### Virtual List Construction (Lines 141-211)
`virtualItems` is a flat `VirtualItem[]` built from the grouped data:

Two modes:
1. **`most-context` mode:** Flat list of `contextSortedSessions` (no headers, no pinned section)
2. **Default (`recent`) mode:** Pinned header + pinned sessions → Date category headers + sessions → Loader

Types in the virtual list:
- `{ type: 'header', category: DateCategory }` — date section header
- `{ type: 'pinned-header' }` — pinned section header
- `{ type: 'session', session, isPinned, isHidden }` — session item
- `{ type: 'loader' }` — infinite scroll trigger

#### Virtualizer Setup (Lines 233-270)
[OBS] Uses `@tanstack/react-virtual` `useVirtualizer`:
- `HEADER_HEIGHT = 28px`, `SESSION_HEIGHT = 48px`, `LOADER_HEIGHT = 36px`
- `OVERSCAN = 5`
- Infinite scroll: when last virtual item is within 3 of end, calls `fetchSessionsMore()`

#### UI Controls (Lines 371-452)
Current toolbar between header and list:

| Control | Line | Action |
|---------|------|--------|
| Calendar icon + "Sessions" label | 374-379 | Static header |
| Session count badge | 382-391 | Shows `(N+)` with tooltip |
| Multi-select toggle | 416-425 | `toggleSidebarMultiSelect` |
| Hidden sessions toggle | 427-438 | `toggleShowHiddenSessions` (only when hidden exist) |
| Sort mode toggle | 440-451 | Toggles 'recent' ↔ 'most-context' |

[F-ID: **This toolbar (lines 373-452) is the insertion point for filter controls.** It already has multi-select, hidden toggle, and sort toggle. New filter buttons/dropdowns would fit naturally here.]

#### Bulk Action Bar (Lines 455-507)
[OBS] Shown when multi-select is active and sessions are selected. Actions: Pin, Hide, Unhide, Cancel.

#### Render Loop (Lines 509-587)
Each virtual row renders based on item type:
- `pinned-header` → sticky header with Pin icon
- `header` → sticky header with category name
- `loader` → loading spinner or "scroll to load more"
- `session` → `<SessionItem />` with props: session, isActive, isPinned, isHidden, multiSelectActive, isSelected, onToggleSelect

### 4.5 SessionItem (`src/renderer/components/sidebar/SessionItem.tsx:133`)
[OBS] Individual session row. Key interactions:

| Action | Method | Line |
|--------|--------|------|
| Click | `handleClick` | 164 — opens tab via `openTab()` |
| Right-click | `handleContextMenu` | 189 — shows `SessionContextMenu` |
| Context: Open in current | `handleOpenInCurrentPane` | 196 |
| Context: Open in new tab | `handleOpenInNewTab` | 210 |
| Context: Split right | `handleSplitRightAndOpen` | 224 |

Props interface (`SessionItemProps`, line 22):
```typescript
interface SessionItemProps {
  session: Session;
  isActive: boolean;
  isPinned: boolean;
  isHidden: boolean;
  multiSelectActive: boolean;
  isSelected: boolean;
  onToggleSelect: () => void;
}
```

Also renders `ConsumptionBadge` (line 57) showing per-session context consumption with phase breakdown popover.

### 4.6 SessionContextMenu (`src/renderer/components/sidebar/SessionContextMenu.tsx:30`)
[OBS] Right-click menu with: Open in current pane, Open in new tab, Split right, Pin/Unpin, Hide/Unhide, Copy session ID.

---

## 5. Utility Functions

### dateGrouping.ts (`src/renderer/utils/dateGrouping.ts`)

| Function | Line | Purpose |
|----------|------|---------|
| `groupSessionsByDate` | 26 | Groups by Today/Yesterday/Previous 7 Days/Older using date-fns |
| `getNonEmptyCategories` | 56 | Filters empty categories from `DATE_CATEGORY_ORDER` |
| `separatePinnedSessions` | 68 | Splits into pinned (preserving pin order) and unpinned |

---

## 6. Real-Time Update Path

[OBS: From `sessionSlice.ts:258`]

```
FileWatcher (main process)
    → IPC 'file-change' event
    → store.initializeNotificationListeners() (App.tsx)
    → refreshSessionsInPlace(projectId)
        → api.getSessionsPaginated(projectId, null, 20, { metadataLevel: 'light' })
        → set({ sessions: result.sessions, ... })
        → React re-renders DateGroupedSessions
        → visibleSessions recalculated via useMemo
        → Virtual list re-renders
```

[F-ID: Filters must be reactive to `refreshSessionsInPlace`. Since filters operate on `sessions` via `useMemo`, any store update to `sessions` will automatically re-trigger filter memos. No special handling needed.]

---

## 7. Gap Analysis for New Filters

### What exists (can filter on today):
| Filter | Data Available | Location |
|--------|---------------|----------|
| **Date range** | `session.createdAt` (unix timestamp) | Already grouped by date; custom range needs new UI |
| **Hidden** | `hiddenSessionIds` + `showHiddenSessions` | Working |
| **Sort** | `sessionSortMode` ('recent' \| 'most-context') | Working |
| **Pinned** | `pinnedSessionIds` | Working (visual separation, not a filter) |
| **Has subagents** | `session.hasSubagents` | Available but no filter UI |

### What's missing (requires new data):
| Filter | Gap | Effort |
|--------|-----|--------|
| **Model** | [H: Session type has no `model` field. Model is extracted per-message inside JSONL. Light metadata level skips this.] Need to either: (a) add `model` to `Session` during light parse, or (b) add server-side filter to `getSessionsPaginated`. | Medium — requires main process parser change |
| **Session type** | [H: No explicit session type enum. Would need to derive from: `hasSubagents`, team data (`Process.team`), or JSONL content.] Need to define what "session type" means and populate it. | Medium — type definition + parser enrichment |
| **Custom date range** | [OBS: `createdAt` exists. Need date picker UI + filter logic.] Client-side only. | Low — UI + filter memo |

### Insertion Points Summary

1. **Store:** Add filter state fields to `SessionSlice` (e.g., `sessionFilters: { model?: string, type?: string, dateRange?: [number, number] }`)
2. **Filtering pipeline:** Insert after `visibleSessions` memo (line 112) and before `separatePinnedSessions` (line 118)
3. **UI controls:** Add to toolbar area (lines 373-452) — filter dropdown/popover next to existing controls
4. **Session type:** Enrich `Session` interface in `domain.ts:81` with `model?: string` and `sessionType?: SessionType`
5. **Parser:** Update light metadata extraction in main process to capture model from first assistant message

---

## 8. File Index

| File | Role |
|------|------|
| `src/main/types/domain.ts:81` | Session interface definition |
| `src/renderer/types/data.ts:77` | SessionSortMode type |
| `src/renderer/types/tabs.ts:127-132` | DateCategory, DateGroupedSessions types |
| `src/renderer/store/slices/sessionSlice.ts` | Session state + actions |
| `src/renderer/utils/dateGrouping.ts` | Date grouping + pinned separation |
| `src/renderer/components/layout/TabbedLayout.tsx` | Root layout |
| `src/renderer/components/layout/Sidebar.tsx` | Sidebar shell |
| `src/renderer/components/layout/SidebarHeader.tsx` | Project/worktree selection |
| `src/renderer/components/sidebar/DateGroupedSessions.tsx` | **Core: filtering, grouping, virtual list** |
| `src/renderer/components/sidebar/SessionItem.tsx` | Individual session row |
| `src/renderer/components/sidebar/SessionContextMenu.tsx` | Right-click menu |
| `src/preload/index.ts:132` | IPC bridge for paginated fetch |
| `src/renderer/api/index.ts:59` | API proxy |
