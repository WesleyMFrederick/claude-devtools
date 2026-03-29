# GitHub Issue Draft: Session ID Lookup in CommandPalette

## Title
[FEAT] Session ID lookup in CommandPalette (Cmd+K)

## Labels
feature request

## Body

**Is your feature request related to a problem? Please describe.**

When debugging across sessions or resuming work, users often have a session UUID (from `claude --resume`, logs, or another devtools tab). Currently there's no way to navigate directly to a session by its ID. You have to visually scan the sidebar or search by message content.

Related prior art:
- #34 requested exposing session IDs for easier resume
- #115 / PR #129 adds session ID display and copy in chat UI
- #41 explored cross-project search

This complements those by adding the ability to **navigate to a session by pasting its ID** in the existing CommandPalette.

**Describe the solution you'd like**

Extend the CommandPalette (Cmd+K) with session ID detection:

1. **Full UUID paste** - Direct file lookup across all projects, single result, instant navigation (~50ms debounce)
2. **Partial ID fragment** - Type 3+ hex-dash chars (e.g., `eb7`), matches session filenames sorted by recency (~300ms debounce)
3. **Mode indicator** - Green "Session ID search" label when hex input is detected
4. **Existing text search unchanged** - Non-hex queries work exactly as before

**Empty palette** - updated placeholder text:
![CommandPalette empty](docs/screenshots/cmdpalette-empty.png)

**Partial hex fragment** (`eb7`) - green mode indicator, cross-project matches:
![Hex fragment search](docs/screenshots/cmdpalette-hex-fragment.png)

**Full UUID paste** - single exact match:
![UUID exact match](docs/screenshots/cmdpalette-uuid-match.png)

**Normal text search** - unchanged behavior, no green indicator:
![Text search](docs/screenshots/cmdpalette-text-search.png)

**Describe alternatives you've considered**

- **Sidebar filter**: Adding a session ID filter to the sidebar session list. Rejected because the CommandPalette already handles search and this keeps the UI consistent.
- **Dedicated "Go to session" dialog**: A separate modal just for session ID input. Rejected because adding to the existing Cmd+K palette is more discoverable and requires no new keybinding.
- **URL-based navigation** (e.g., `localhost:3456/session/:id`): Would work for standalone mode but not Electron, and requires router changes.

**Additional context**

- No new dependencies added
- No changes to existing text search, sidebar, or session list
- All quality gates pass: typecheck clean, 653/653 tests pass, build clean
- Backend endpoints verified via curl, frontend bundle verified to contain new code
- Implementation adds `findSessionById()` and `findSessionsByPartialId()` to ProjectScanner using existing `collectFulfilledInBatches` for parallel I/O
- Full IPC + HTTP + preload + HttpClient bridge for both Electron and standalone modes
