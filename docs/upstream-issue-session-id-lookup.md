# GitHub Issue Draft: Session ID Lookup in CommandPalette

## Title
[FEAT] Session ID lookup in CommandPalette (Cmd+K)

## Body

**Is your feature request related to a problem? Please describe.**

When debugging across sessions or resuming work, users often have a session UUID (from `claude --resume`, logs, or another devtools tab). Currently there's no way to navigate directly to a session by its ID. You have to visually scan the sidebar or search by message content.

Related: #115 requested session ID visibility in the UI. PR #129 adds a SessionInfoBar to display/copy session IDs. This proposal complements that by adding the ability to **navigate to a session by pasting its ID**.

**Describe the solution you'd like**

Extend the existing CommandPalette (Cmd+K) with session ID detection:

1. **Full UUID paste** - When a UUID is pasted, bypass text search and do a direct file lookup across all projects. Single result, instant navigation. (~50ms debounce)
2. **Partial ID fragment** - When 3+ hex-dash characters are typed (e.g., `eb7`), match against session filenames. Returns a list of matching sessions sorted by recency. (~300ms debounce)
3. **Mode indicator** - Green "Session ID search" label appears when hex input is detected, so users know the search mode switched.
4. **Existing text search unchanged** - Non-hex queries continue to work exactly as before.

**Implementation scope**

- Types: `FindSessionByIdResult`, `FindSessionsByPartialIdResult` in domain types
- Service: `findSessionById()` and `findSessionsByPartialId()` on ProjectScanner (parallel I/O with existing `collectFulfilledInBatches`)
- IPC + HTTP: New handlers/routes for both lookup modes
- Preload + HttpClient: Bridge methods
- Shared: `sessionIdValidator.ts` with regex + helpers (single source of truth)
- CommandPalette: Query classification, debounced lookups, `SessionIdMatchItem` component

**What it does NOT change**

- No new dependencies
- No changes to existing text search behavior
- No changes to sidebar or session list
- No new settings or configuration

**Validation**

- `pnpm typecheck` clean
- `pnpm test` 653/653 pass
- `pnpm build` clean
- Backend endpoints manually verified via curl
- Frontend bundle verified to contain new code
