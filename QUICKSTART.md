# Quickstart

## Standalone Server (Browser Mode — No Electron)

### First Time Setup
```bash
pnpm install
pnpm standalone:build
pnpm standalone:start
```
Open http://127.0.0.1:3456 in your browser.

### After Code Changes
```bash
pnpm standalone:build && pnpm standalone:start
```

### Environment Variables
| Variable | Default | Purpose |
|----------|---------|---------|
| `PORT` | `3456` | Server port |
| `HOST` | `0.0.0.0` | Bind address |
| `CLAUDE_ROOT` | `~/.claude` | Path to .claude directory |
| `CORS_ORIGIN` | `*` | CORS policy |

### What Works Without Electron
- Full UI in browser (React renderer served as static files)
- All session parsing and visualization
- Real-time file watching via SSE
- REST API at `/api/*`

### What Requires Electron
- Native macOS notifications
- SSH remote connections
- Auto-updater
- Native window controls

## Electron Desktop App

### Setup
```bash
pnpm install
```
If `pnpm dev` fails with "Electron uninstall" or "Electron failed to install correctly":
```bash
# Electron's postinstall script may have been blocked by pnpm
cd node_modules/.pnpm/electron@40.3.0/node_modules/electron && node install.js
```
Then:
```bash
pnpm dev
```

## Dev Mode (tsx, no build step)

`pnpm standalone` runs the server entry point directly via tsx. Currently crashes because the `electron` module's ESM exports don't work outside the Electron runtime. The production build path (`standalone:build`) uses Vite plugins to stub electron imports, so use that instead.
