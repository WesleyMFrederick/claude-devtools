# Session ID Lookup — Feature Trace

Traces both lookup paths through CommandPalette (Cmd+K):
- **Path A**: Full UUID → exact match via `findSessionById`
- **Path B**: 3+ char hex fragment → partial match via `findSessionsByPartialId`

Both paths share transport selection, handler validation, and navigation destination.

---

## Artifacts

| Artifact | Path | Role |
|----------|------|------|
| Shared validator | `src/shared/utils/sessionIdValidator.ts` | `isUUID`, `isSessionIdFragment`, regex constants |
| Domain types | `src/main/types/domain.ts` | `FindSessionByIdResult`, `FindSessionsByPartialIdResult` |
| IPC channel constants | `src/preload/constants/ipcChannels.ts` | `FIND_SESSION_BY_ID`, `FIND_SESSIONS_BY_PARTIAL_ID` |
| Preload bridge | `src/preload/index.ts` | IPC `ipcRenderer.invoke` wiring |
| IPC handler | `src/main/ipc/search.ts` | `handleFindSessionById`, `handleFindSessionsByPartialId` |
| HTTP handler | `src/main/http/search.ts` | `GET /api/sessions/:sessionId/locate`, `GET /api/sessions/search-by-id/:fragment` |
| API adapter | `src/renderer/api/index.ts` | IPC vs HTTP transport selection |
| HTTP client | `src/renderer/api/httpClient.ts` | HTTP transport implementation |
| ProjectScanner | `src/main/services/discovery/ProjectScanner.ts` | `findSessionById`, `findSessionsByPartialId` |
| CommandPalette | `src/renderer/components/search/CommandPalette.tsx` | Query classification, effects, render, navigation |

---

## Trace

~~~text
TRACE: Session ID Lookup (CommandPalette → ProjectScanner)
══════════════════════════════════════════════════════════

 SHARED TYPES
 ─────────────
 1. [OBS: src/main/types/domain.ts:267-274]
    FindSessionByIdResult:
      { found: boolean; projectId?: string; session?: Session }

 2. [OBS: src/main/types/domain.ts:279-284]
    FindSessionsByPartialIdResult:
      { found: boolean; results: { projectId: string; session: Session }[] }

 SHARED VALIDATOR (src/shared/utils/sessionIdValidator.ts)
 ──────────────────────────────────────────────────────────
 3. [OBS: src/shared/utils/sessionIdValidator.ts:7]
    UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

 4. [OBS: src/shared/utils/sessionIdValidator.ts:10]
    SESSION_FRAGMENT_REGEX = /^[0-9a-f][0-9a-f-]{2,}$/i

 5. [OBS: src/shared/utils/sessionIdValidator.ts:13]
    MIN_FRAGMENT_LENGTH = 3

 6. [OBS: src/shared/utils/sessionIdValidator.ts:15-17]
    isUUID(value): trims whitespace, tests UUID_REGEX
    PASS → full UUID; FAIL → not a UUID

 7. [OBS: src/shared/utils/sessionIdValidator.ts:22-28]
    isSessionIdFragment(value): trim → length >= 3 AND !isUUID AND SESSION_FRAGMENT_REGEX test
    PASS → valid fragment; FAIL → below threshold or full UUID or non-hex

 IPC CHANNEL CONSTANTS
 ──────────────────────
 8. [OBS: src/preload/constants/ipcChannels.ts:186]
    FIND_SESSION_BY_ID = 'find-session-by-id'

 9. [OBS: src/preload/constants/ipcChannels.ts:189]
    FIND_SESSIONS_BY_PARTIAL_ID = 'find-sessions-by-partial-id'

 RENDERER: QUERY CLASSIFICATION
 ────────────────────────────────
10. [OBS: src/renderer/components/search/CommandPalette.tsx:253-255]
    User types in palette input → every keystroke recalculates:
      queryIsUUID     = useMemo(() => isUUID(query), [query])
      queryIsFragment = useMemo(() => isSessionIdFragment(query), [query])
      queryIsSessionId = queryIsUUID || queryIsFragment

    ├── queryIsUUID = true     → PATH A (steps 11–18a)
    └── queryIsFragment = true → PATH B (steps 11b–18b)

 ─────────────────────────────────────────
 PATH A: UUID EXACT MATCH
 ─────────────────────────────────────────

11. [OBS: src/renderer/components/search/CommandPalette.tsx:340-366]
    UUID useEffect fires immediately (no debounce):
    │  Generate requestId for staleness checking
    │  setLoading(true)
    │  CALL ──→ api.findSessionById(query.trim())
    │
    │  RETURN ←── FindSessionByIdResult
    │
    │  Stale-check: latestSearchRequestRef.current !== requestId → discard
    │  setSessionIdMatch(result)      ← KEY LINE
    │  setSessionResults([])
    │  setLoading(false)

 PATH B: FRAGMENT SEARCH
 ──────────────────────────────────────────

11b.[OBS: src/renderer/components/search/CommandPalette.tsx:373-403]
    Fragment useEffect fires with 300ms debounce:
    │  setTimeout(async () => { ... }, 300)          ← KEY LINE (debounce)
    │  Generate requestId for staleness checking
    │  setLoading(true)
    │  CALL ──→ api.findSessionsByPartialId(query.trim())
    │
    │  RETURN ←── FindSessionsByPartialIdResult
    │
    │  Stale-check: latestSearchRequestRef.current !== requestId → discard
    │  setPartialIdMatches(result.results)
    │  setLoading(false)

 RENDERER → TRANSPORT (shared for both paths)
 ─────────────────────────────────────────────
12. [OBS: src/renderer/api/index.ts:37-44]
    api.getImpl():
    ├── window.electronAPI present → IPC PATH (steps 13a–16a)
    └── absent (browser mode)     → HTTP PATH (steps 13b–16b)

 IPC PATH
 ─────────
13a.[OBS: src/preload/index.ts:144-146]
    Preload bridge:
      findSessionById: (sessionId) => ipcRenderer.invoke(FIND_SESSION_BY_ID, sessionId)
      findSessionsByPartialId: (fragment) => ipcRenderer.invoke(FIND_SESSIONS_BY_PARTIAL_ID, fragment)

14a.[OBS: src/main/ipc/search.ts:45-46]
    Registered channels:
      ipcMain.handle('find-session-by-id', handleFindSessionById)
      ipcMain.handle('find-sessions-by-partial-id', handleFindSessionsByPartialId)

 IPC → MAIN: handleFindSessionById
 ───────────────────────────────────
15a.[OBS: src/main/ipc/search.ts:131-148]
    Guard: validateSessionId(sessionId) → { valid, value, error }
    FAIL → return { found: false }
    PASS → registry.getActive().projectScanner.findSessionById(validatedSession.value!)
    RETURN ←── FindSessionByIdResult

 IPC → MAIN: handleFindSessionsByPartialId
 ──────────────────────────────────────────
15b.[OBS: src/main/ipc/search.ts:154-169]
    Guard: isSessionIdFragment(fragment) → false → return { found: false, results: [] }
    PASS → registry.getActive().projectScanner.findSessionsByPartialId(fragment)
    RETURN ←── FindSessionsByPartialIdResult

 HTTP PATH (browser / server mode)
 ────────────────────────────────────
13b.[OBS: src/renderer/api/httpClient.ts:226-231]
    findSessionById: GET /api/sessions/${sessionId}/locate
    findSessionsByPartialId: GET /api/sessions/search-by-id/${fragment}

14b.[OBS: src/main/http/search.ts:87-100]
    Route: GET /api/sessions/:sessionId/locate
    Guard: validateSessionId(params.sessionId) → fail → { found: false }
    PASS → projectScanner.findSessionById(validated.value!)

14c.[OBS: src/main/http/search.ts:102-117]
    Route: GET /api/sessions/search-by-id/:fragment
    Guard: isSessionIdFragment(fragment) → fail → { found: false, results: [] }
    PASS → projectScanner.findSessionsByPartialId(fragment)

 MAIN: ProjectScanner.findSessionById
 ──────────────────────────────────────
16. [OBS: src/main/services/discovery/ProjectScanner.ts:1189-1226]
    │  readdir(projectsDir) → filter by isValidEncodedPath(entry.name)
    │
    │  [OBS: ProjectScanner.ts:1197]
    │  batchSize = fsProvider.type === 'ssh' ? 8 : 24
    │
    │  [OBS: ProjectScanner.ts:1198-1218]                     ← KEY LOOP (early exit)
    │  for (let i = 0; i < projectDirs.length; i += batchSize):
    │    batch = projectDirs.slice(i, i + batchSize)
    │    Promise.allSettled(
    │      batch.map(dir => {
    │        sessionPath = buildSessionPath(projectsDir, dir.name, sessionId)
    │        return fsProvider.exists(sessionPath) ? dir.name : null
    │      })
    │    ) → matchedProjectId = first non-null value
    │
    │    if (matchedProjectId):
    │      session = getSessionWithOptions(matchedProjectId, sessionId, { metadataLevel: 'light' })
    │      RETURN ←── { found: true, projectId: matchedProjectId, session }  ← EARLY EXIT
    │
    │  [OBS: ProjectScanner.ts:1221]
    │  All batches exhausted, no match →
    RETURN ←── { found: false }

 MAIN: ProjectScanner.findSessionsByPartialId
 ─────────────────────────────────────────────
17. [OBS: src/main/services/discovery/ProjectScanner.ts:1235-1296]
    │  [OBS: ProjectScanner.ts:1240]
    │  lowerFragment = fragment.toLowerCase()
    │
    │  [OBS: ProjectScanner.ts:1241-1260]
    │  collectFulfilledInBatches(projectDirs, batchSize, async (dir) =>
    │    readdir(projectPath) → filter .jsonl files by includes(lowerFragment)
    │    → extractSessionId(filename) → { projectId, sessionIds }
    │  )
    │
    │  [OBS: ProjectScanner.ts:1263-1270]
    │  Flatten matches; cap at maxResults (default 50)
    │  allMatches = [] → push { projectId, sessionId }
    │  allMatches.length === 0 → return { found: false, results: [] }
    │
    │  [OBS: ProjectScanner.ts:1276-1284]
    │  Second batch pass: getSessionWithOptions(match.projectId, match.sessionId, { metadataLevel: 'light' })
    │  Null results filtered out
    │
    │  [OBS: ProjectScanner.ts:1287-1291]
    │  Sort by session.createdAt DESC
    RETURN ←── { found: results.length > 0, results }

 RENDERER: DISPLAY
 ──────────────────
18a.[OBS: src/renderer/components/search/CommandPalette.tsx:717-736]
    queryIsUUID && sessionIdMatch?.found && sessionIdMatch.session →
      <SessionIdMatchItem
        projectName   = projectNameByWorktreeId.get(sessionIdMatch.projectId)
        sessionTitle  = sessionIdMatch.session.firstMessage
        messageCount  = sessionIdMatch.session.messageCount
        createdAt     = sessionIdMatch.session.createdAt
        sessionId     = query.trim()
        isSelected    = true
        onClick       = handleSessionIdMatchClick
      />

18b.[OBS: src/renderer/components/search/CommandPalette.tsx:743-760]
    queryIsFragment && partialIdMatches.length > 0 →
      partialIdMatches.map(match => <SessionIdMatchItem key={match.session.id} ... />)

 SessionIdMatchItem: DEFENSIVE TIMESTAMP
 ─────────────────────────────────────────
19. [OBS: src/renderer/components/search/CommandPalette.tsx:56-96]
    createdAt > 0
      ? formatDistanceToNow(new Date(createdAt), { addSuffix: true })
      : 'Unknown'                                  ← guard against zero/missing timestamps

 RENDERER: NAVIGATION
 ─────────────────────
20. [OBS: src/renderer/components/search/CommandPalette.tsx:480-484]
    handleSessionIdMatchClick:
      closeCommandPalette()
      navigateToSession(sessionIdMatch.projectId, sessionIdMatch.session.id, false)

21. [OBS: src/renderer/components/search/CommandPalette.tsx:488-494]
    handlePartialMatchClick(projectId, sessionId):
      closeCommandPalette()
      navigateToSession(projectId, sessionId, false)

    Enter key also triggers match at selectedIndex:
    [OBS: CommandPalette.tsx:550-560]
      queryIsUUID  → handleSessionIdMatchClick()
      queryIsFragment → handlePartialMatchClick(match.projectId, match.session.id)

══════════════════════════════════════════════════════════
END TRACE
~~~

---

## Fact Derivations

1. **[F-LK: from steps 6-7]** `isSessionIdFragment` is a composite guard: it requires length ≥ 3, non-UUID, and regex match — in that order. A full UUID typed into the palette will always route to Path A, never Path B, because `!isUUID()` fails first.

2. **[F-LK: from steps 11 + 11b]** UUID lookup is latency-optimised (no debounce); fragment lookup has a 300ms debounce. A full UUID typed quickly returns a result before a fragment of equal length would even fire.

3. **[F-LK: from step 12]** Transport selection is runtime-determined per `window.electronAPI` presence. The same `ProjectScanner` methods execute in both IPC and HTTP paths — no logic duplication at the service layer.

4. **[F-LK: from step 16]** `findSessionById` stops scanning after the first batch that contains a match (`return` inside the for-loop). It never reads all project directories when the session is in an early-numbered project.

5. **[F-LK: from step 17]** `findSessionsByPartialId` always scans ALL project directories (via `collectFulfilledInBatches`), then sorts by `createdAt` descending. The first match in the list is always the most recently created matching session.

6. **[F-ID: from steps 8-9 + 13a]** IPC channel strings `'find-session-by-id'` and `'find-sessions-by-partial-id'` are defined exactly once (in `ipcChannels.ts`) and referenced as constants in both preload and main. There are no duplicate string literals in the codebase.

---

## Process Tree

**Canonical:**
```
→(a, b, ×(c, d), e, f, ×(g, h), i, j, k)
```

**Visual tree:**
```
→ session-id-lookup
├── [a] user opens CommandPalette, types query
├── [b] useMemo classifies query (isUUID / isSessionIdFragment)
├── × fetch-strategy
│   ├── [c] IF UUID: fire immediate fetch (no debounce)
│   └── [d] IF fragment: fire 300ms debounced fetch
├── [e] api.getImpl() selects transport (IPC or HTTP)
├── [f] handler: validateSessionId / isSessionIdFragment → delegate to ProjectScanner
├── × scanner-method
│   ├── [g] findSessionById: batched early-exit (batchSize 24 local / 8 SSH)
│   └── [h] findSessionsByPartialId: full parallel scan + sort by createdAt desc
├── [i] store result in React state (sessionIdMatch or partialIdMatches)
├── [j] render SessionIdMatchItem(s)
└── [k] user selects → closeCommandPalette + navigateToSession(projectId, sessionId)
```

**Activity legend:**

| Node | Actor | Actor Name | Activity | Tool | Trace evidence |
|------|-------|------------|----------|------|----------------|
| [a] | user | Wesley | opens palette (Cmd+K), types session ID | — | steps 10 |
| [b] | agent | React renderer | recalculates `queryIsUUID` / `queryIsFragment` on keystroke | — | steps 10 |
| [c] | agent | React renderer | fires immediate `api.findSessionById()` call | — | step 11 |
| [d] | agent | React renderer | fires `api.findSessionsByPartialId()` after 300ms debounce | — | step 11b |
| [e] | agent | api/index.ts | resolves `window.electronAPI` or creates `HttpAPIClient` | — | step 12 |
| [f] | agent | Main process | validates input; delegates to `ProjectScanner` | — | steps 15a, 15b, 14b, 14c |
| [g] | agent | ProjectScanner | batched `exists()` checks with early-exit return | — | step 16 |
| [h] | agent | ProjectScanner | full `readdir` scan + metadata load + sort | — | step 17 |
| [i] | agent | React renderer | calls `setSessionIdMatch` or `setPartialIdMatches` | — | steps 11, 11b |
| [j] | agent | React renderer | renders `SessionIdMatchItem` component(s) | — | steps 18a, 18b, 19 |
| [k] | user | Wesley | selects match (click or Enter) → navigate to session | — | steps 20, 21 |
