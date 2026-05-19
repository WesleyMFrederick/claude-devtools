---
type: "query"
date: "2026-05-19T22:10:30.852938+00:00"
question: "Why does createLogger connect so many communities and what breaks if its signature changes?"
contributor: "graphify"
source_nodes: ["createLogger", "ProjectScanner", "ConfigManager", "NotificationManager", "FileWatcher", "SessionParser"]
---

# Q: Why does createLogger connect so many communities and what breaks if its signature changes?

## Answer

createLogger() lives in src/shared/utils/logger.ts (community 37). BFS depth-2 reaches 444 nodes across 36 communities because every service (ConfigManager, NotificationManager, FileWatcher, SshConnectionManager, DataCache, SessionParser), every IPC handler file (config.ts, sessions.ts, search.ts, notifications.ts, memory.ts), and every infrastructure class imports it. It is the single cross-cutting dependency in the entire main process. If its signature changes — e.g., the return type, parameter shape, or module path — every class in communities 1-3, 6-8, 13-15, 18-19, 22, 24, 27-35, 38, 44, 47-48, 51, 55 breaks simultaneously. The risk is compounded because it lives in shared/ (imported by both main and renderer), meaning a breaking change propagates to both processes.

## Source Nodes

- createLogger
- ProjectScanner
- ConfigManager
- NotificationManager
- FileWatcher
- SessionParser