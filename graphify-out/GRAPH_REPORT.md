# Graph Report - /Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/claude-devtools  (2026-05-19)

## Corpus Check
- Large corpus: 450 files · ~623,741 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 1653 nodes · 2897 edges · 146 communities (126 shown, 20 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 344 edges (avg confidence: 0.8)
- Token cost: 18,410 input · 3,621 output

## Community Hubs (Navigation)
- [[_COMMUNITY_UI Helpers & Formatters|UI Helpers & Formatters]]
- [[_COMMUNITY_Chunk Building & Session Analysis|Chunk Building & Session Analysis]]
- [[_COMMUNITY_Config Routes & Auto-Updater|Config Routes & Auto-Updater]]
- [[_COMMUNITY_SSH & System Utilities|SSH & System Utilities]]
- [[_COMMUNITY_HTTP API Client|HTTP API Client]]
- [[_COMMUNITY_Session & Tab State|Session & Tab State]]
- [[_COMMUNITY_Tool Use Processing|Tool Use Processing]]
- [[_COMMUNITY_IPC Handlers & Semantic Steps|IPC Handlers & Semantic Steps]]
- [[_COMMUNITY_Configuration Management|Configuration Management]]
- [[_COMMUNITY_Context & CLAUDE.md Tracking|Context & CLAUDE.md Tracking]]
- [[_COMMUNITY_Settings UI Components|Settings UI Components]]
- [[_COMMUNITY_Highlights & Color Triggers|Highlights & Color Triggers]]
- [[_COMMUNITY_Content Formatting Utils|Content Formatting Utils]]
- [[_COMMUNITY_Session Discovery & Scanning|Session Discovery & Scanning]]
- [[_COMMUNITY_IPC Handler Registration|IPC Handler Registration]]
- [[_COMMUNITY_Memory & Markdown Reader|Memory & Markdown Reader]]
- [[_COMMUNITY_Command Search & Path Display|Command Search & Path Display]]
- [[_COMMUNITY_Context Injection UI|Context Injection UI]]
- [[_COMMUNITY_Notification System|Notification System]]
- [[_COMMUNITY_Data Caching Layer|Data Caching Layer]]
- [[_COMMUNITY_Zustand Store Slices|Zustand Store Slices]]
- [[_COMMUNITY_Search Text Highlighting|Search Text Highlighting]]
- [[_COMMUNITY_File System Watcher|File System Watcher]]
- [[_COMMUNITY_Session Export|Session Export]]
- [[_COMMUNITY_API Route Registration|API Route Registration]]
- [[_COMMUNITY_Electron IPC Bridge|Electron IPC Bridge]]
- [[_COMMUNITY_DOM Search & Scroll|DOM Search & Scroll]]
- [[_COMMUNITY_Session Parser|Session Parser]]
- [[_COMMUNITY_Electron Window Setup|Electron Window Setup]]
- [[_COMMUNITY_Git Identity & Worktrees|Git Identity & Worktrees]]
- [[_COMMUNITY_Project & Memory IPC|Project & Memory IPC]]
- [[_COMMUNITY_Message Preview & Subagent|Message Preview & Subagent]]
- [[_COMMUNITY_Worktree Grouping|Worktree Grouping]]
- [[_COMMUNITY_Project Path Resolution|Project Path Resolution]]
- [[_COMMUNITY_Metadata & Content Sanitizer|Metadata & Content Sanitizer]]
- [[_COMMUNITY_SSH Config Parser|SSH Config Parser]]
- [[_COMMUNITY_Pane Layout Sync|Pane Layout Sync]]
- [[_COMMUNITY_Error Boundary & Path Resolver|Error Boundary & Path Resolver]]
- [[_COMMUNITY_Trigger Manager|Trigger Manager]]
- [[_COMMUNITY_Settings Row UI|Settings Row UI]]
- [[_COMMUNITY_AI Chat Item Utils|AI Chat Item Utils]]
- [[_COMMUNITY_Search Entry Extraction|Search Entry Extraction]]
- [[_COMMUNITY_Notification Store Slice|Notification Store Slice]]
- [[_COMMUNITY_Context Panel Sections|Context Panel Sections]]
- [[_COMMUNITY_Session IPC Handlers|Session IPC Handlers]]
- [[_COMMUNITY_Settings Confirm UI|Settings Confirm UI]]
- [[_COMMUNITY_Test Mocks & Fixtures|Test Mocks & Fixtures]]
- [[_COMMUNITY_Search Route Handlers|Search Route Handlers]]
- [[_COMMUNITY_Search Text Cache|Search Text Cache]]
- [[_COMMUNITY_Connection & Context State|Connection & Context State]]
- [[_COMMUNITY_Project Search Results|Project Search Results]]
- [[_COMMUNITY_Notification IPC Handlers|Notification IPC Handlers]]
- [[_COMMUNITY_HTTP Event Server|HTTP Event Server]]
- [[_COMMUNITY_Subproject Registry|Subproject Registry]]
- [[_COMMUNITY_Markdown & Wikilink Parser|Markdown & Wikilink Parser]]
- [[_COMMUNITY_Session Full-Text Search|Session Full-Text Search]]
- [[_COMMUNITY_Date-Grouped Sessions|Date-Grouped Sessions]]
- [[_COMMUNITY_Connection Status Badge|Connection Status Badge]]
- [[_COMMUNITY_Session Content Filter|Session Content Filter]]
- [[_COMMUNITY_Subagent File Locator|Subagent File Locator]]
- [[_COMMUNITY_Subagent IPC Routes|Subagent IPC Routes]]
- [[_COMMUNITY_Launcher & App Opener|Launcher & App Opener]]
- [[_COMMUNITY_Message Classifier|Message Classifier]]
- [[_COMMUNITY_Keyboard Shortcut Utils|Keyboard Shortcut Utils]]
- [[_COMMUNITY_Path Validation IPC|Path Validation IPC]]
- [[_COMMUNITY_Shortcut Dispatch|Shortcut Dispatch]]
- [[_COMMUNITY_Hover Tooltip Alpha|Hover Tooltip Alpha]]
- [[_COMMUNITY_Hover Tooltip Beta|Hover Tooltip Beta]]
- [[_COMMUNITY_Middle Panel Layout|Middle Panel Layout]]
- [[_COMMUNITY_Settings Tabs View|Settings Tabs View]]
- [[_COMMUNITY_Directory Tree Builder|Directory Tree Builder]]
- [[_COMMUNITY_Pane Split Drop Zone|Pane Split Drop Zone]]

## God Nodes (most connected - your core abstractions)
1. `createLogger()` - 73 edges
2. `ProjectScanner` - 46 edges
3. `ConfigManager` - 44 edges
4. `NotificationManager` - 32 edges
5. `FileWatcher` - 31 edges
6. `getErrorMessage()` - 29 edges
7. `validateProjectId()` - 28 edges
8. `SshConnectionManager` - 28 edges
9. `DataCache` - 28 edges
10. `SessionParser` - 26 edges

## Surprising Connections (you probably didn't know these)
- `Harness()` --calls--> `useVisibleAIGroup()`  [INFERRED]
  test/renderer/hooks/useVisibleAIGroup.test.ts → src/renderer/hooks/useVisibleAIGroup.ts
- `extractRenderedMatchIndexes()` --calls--> `findMarkdownSearchMatches()`  [INFERRED]
  test/shared/utils/markdownSearchRendererAlignment.test.ts → src/shared/utils/markdownTextSearch.ts
- `extractRenderedMatchIndexes()` --calls--> `createSearchContext()`  [INFERRED]
  test/shared/utils/markdownSearchRendererAlignment.test.ts → src/renderer/components/chat/searchHighlightUtils.ts
- `handleAdd()` --calls--> `generateUUID()`  [INFERRED]
  src/renderer/components/settings/sections/WorkspaceSection.tsx → src/renderer/utils/stringUtils.ts
- `handleCheck()` --calls--> `getErrorMessage()`  [INFERRED]
  src/main/ipc/updater.ts → src/shared/utils/errorHandling.ts

## Communities (146 total, 20 thin omitted)

### Community 0 - "UI Helpers & Formatters"
Cohesion: 0.06
Nodes (32): extractPrecedingSlashInfo(), getSubagentTypeColorSet(), getTeamColorSet(), hashString(), useTabIdOptional(), useTabUI(), SubagentItem(), TeammateMessageItem() (+24 more)

### Community 1 - "Chunk Building & Session Analysis"
Cohesion: 0.05
Nodes (27): ChunkBuilder, buildAIChunkFromBuffer(), buildCompactChunk(), buildSystemChunk(), buildUserChunk(), calculateAIChunkTiming(), collectSidechainMessages(), extractCommandOutput() (+19 more)

### Community 2 - "Config Routes & Auto-Updater"
Cohesion: 0.06
Nodes (43): registerConfigRoutes(), UpdaterService, decodeWslOutput(), getWslExecutableCandidates(), handleAddIgnoreRegex(), handleAddIgnoreRepository(), handleClearSnooze(), handleFindWslClaudeRoots() (+35 more)

### Community 3 - "SSH & System Utilities"
Cohesion: 0.06
Nodes (10): getLaunchctlSshAuthSock(), isEncryptedPrivateKey(), looksLikeOnlyDefaultKeys(), pathExists(), SshConnectionManager, Timings, tryLoadKey(), SshFileSystemProvider (+2 more)

### Community 4 - "HTTP API Client"
Cohesion: 0.05
Nodes (27): HttpAPIClient, getHttpBaseUrl(), getImpl(), isElectronMode(), ContextSwitchOverlay(), getTrafficLightPaddingForZoom(), getTrafficLightPositionForZoom(), sanitizeZoomFactor() (+19 more)

### Community 5 - "Session & Tab State"
Cohesion: 0.08
Nodes (37): isAIChunk(), isEnhancedAIChunk(), asEnhancedChunkArray(), isAssistantMessage(), isEnhancedChunk(), isEnhancedCompactChunk(), isEnhancedSystemChunk(), isEnhancedUserChunk() (+29 more)

### Community 6 - "Tool Use Processing"
Cohesion: 0.1
Nodes (33): buildToolResultMap(), buildToolUseMap(), estimateTokens(), extractContentFromToolUseResult(), extractToolResults(), ErrorDetector, createDetectedError(), extractErrorMessage() (+25 more)

### Community 7 - "IPC Handlers & Semantic Steps"
Cohesion: 0.09
Nodes (32): extractSemanticStepsFromAIChunk(), handleGetClaudeRootInfo(), handleSelectClaudeRootFolder(), handleReadAgentConfigs(), handleReadClaudeMdFiles(), handleReadDirectoryClaudeMd(), handleReadMentionedFile(), handleShellOpenPath() (+24 more)

### Community 8 - "Configuration Management"
Cohesion: 0.09
Nodes (4): ConfigManager, normalizeConfiguredClaudeRootPath(), normalizeOverridePath(), setClaudeBasePathOverride()

### Community 9 - "Context & CLAUDE.md Tracking"
Cohesion: 0.11
Nodes (41): computeClaudeMdStats(), createDirectoryInjection(), createGlobalInjections(), detectClaudeMdFromFilePath(), extractFileRefsFromResponses(), extractReadToolPaths(), extractUserMentionPaths(), generateInjectionId() (+33 more)

### Community 10 - "Settings UI Components"
Cohesion: 0.06
Nodes (16): DynamicConfigSection(), IgnorePatternsSection(), ModeSelector(), RepositoryScopeSection(), SectionHeader(), getCursorClass(), useAddTriggerFormHandlers(), useAddTriggerFormState() (+8 more)

### Community 11 - "Highlights & Color Triggers"
Cohesion: 0.07
Nodes (13): getHighlight(), getHighlightProps(), getToolHighlightProps(), getTriggerColorDef(), isPresetColorKey(), resolveColorHex(), BaseItem(), StatusDot() (+5 more)

### Community 12 - "Content Formatting Utils"
Cohesion: 0.07
Nodes (19): getFileName(), getToolSummary(), truncate(), clearHideTimeout(), handleMouseEnter(), handleMouseLeave(), getToolSummary(), truncate() (+11 more)

### Community 14 - "IPC Handler Registration"
Cohesion: 0.1
Nodes (32): initializeConfigHandlers(), registerConfigHandlers(), removeConfigHandlers(), initializeContextHandlers(), registerContextHandlers(), removeContextHandlers(), initializeIpcHandlers(), removeIpcHandlers() (+24 more)

### Community 15 - "Memory & Markdown Reader"
Cohesion: 0.09
Nodes (4): MemoryReader, ServiceContext, ServiceContextRegistry, parseMemoryIndex()

### Community 16 - "Command Search & Path Display"
Cohesion: 0.07
Nodes (6): CommandSearch(), formatProjectPath(), isWindowsUserPath(), SortableTab(), formatShortcut(), truncateMiddle()

### Community 17 - "Context Injection UI"
Cohesion: 0.09
Nodes (11): handleClickOutside(), isInsideRect(), CopyablePath(), flattenInjections(), getInjectionTurnIndex(), handleClick(), inferHomeDir(), resolveAbsolutePath() (+3 more)

### Community 20 - "Zustand Store Slices"
Cohesion: 0.1
Nodes (13): createConfigSlice(), createConversationSlice(), createMemorySlice(), createPaneSlice(), createProjectSlice(), createRepositorySlice(), createSessionDetailSlice(), createSessionSlice() (+5 more)

### Community 21 - "Search Text Highlighting"
Cohesion: 0.12
Nodes (17): hl(), createSearchContext(), highlightSearchInChildren(), highlightPaths(), hl(), parseTaskNotifications(), extractRenderedMatchIndexes(), collectTextSegments() (+9 more)

### Community 23 - "Session Export"
Cohesion: 0.17
Nodes (22): exportAsJson(), exportAsMarkdown(), exportAsPlainText(), extractTextFromContent(), formatChunkMarkdown(), formatChunkPlainText(), formatCost(), formatDurationForExport() (+14 more)

### Community 24 - "API Route Registration"
Cohesion: 0.11
Nodes (16): registerEventRoutes(), registerHttpRoutes(), registerMemoryRoutes(), registerNotificationRoutes(), registerProjectRoutes(), registerSessionRoutes(), registerSshRoutes(), registerUpdaterRoutes() (+8 more)

### Community 25 - "Electron IPC Bridge"
Cohesion: 0.09
Nodes (26): Barrel Exports Pattern, contextBridge API, ElectronAPI, IPC Channel Constants, IpcResult<T>, main/index.ts, FileWatcher, preload/index.ts (+18 more)

### Community 26 - "DOM Search & Scroll"
Cohesion: 0.1
Nodes (10): fallbackDOMSearch(), promoteAndScroll(), tryScrollToResult(), ChatHistoryEmptyState(), isNearBottom(), useAutoScrollBottom(), useTabNavigationController(), FakeIntersectionObserver (+2 more)

### Community 27 - "Session Parser"
Cohesion: 0.11
Nodes (3): SessionParser, isParsedInternalUserMessage(), isParsedRealUserMessage()

### Community 28 - "Electron Window Setup"
Cohesion: 0.22
Nodes (13): createWindow(), getRendererIndexPath(), getWindowIconPath(), handleModeSwitch(), initializeServices(), onContextSwitched(), reconfigureLocalContextForClaudeRoot(), rewireContextEvents() (+5 more)

### Community 30 - "Project & Memory IPC"
Cohesion: 0.19
Nodes (12): validateProjectId(), handleCopyPath(), handleGetIndex(), handleHasMemory(), handleListOpeners(), handleOpenIn(), handleReadFile(), handleGetWorktreeSessions() (+4 more)

### Community 31 - "Message Preview & Subagent"
Cohesion: 0.21
Nodes (10): calculateMetrics(), deduplicateByRequestId(), extractTextContent(), getTaskCalls(), parseChatHistoryEntry(), parseJsonlFile(), parseJsonlLine(), parseMessageType() (+2 more)

### Community 33 - "Project Path Resolution"
Cohesion: 0.29
Nodes (8): buildSessionPath(), buildSubagentsPath(), buildTodoPath(), decodePath(), extractBaseDir(), extractSessionId(), isValidEncodedPath(), isValidProjectId()

### Community 34 - "Metadata & Content Sanitizer"
Cohesion: 0.24
Nodes (11): extractCommandDisplay(), extractCommandOutput(), isCommandOutputContent(), sanitizeDisplayContent(), analyzeSessionFileMetadata(), extractCommandName(), extractCwd(), extractFirstUserMessagePreview() (+3 more)

### Community 35 - "SSH Config Parser"
Cohesion: 0.24
Nodes (6): applyDirective(), findWhitespace(), parseHostListing(), parseKeyValue(), SshConfigParser, stripComment()

### Community 36 - "Pane Layout Sync"
Cohesion: 0.33
Nodes (11): syncRootState(), syncFromLayout(), updateTabInLayout(), createEmptyPane(), findPane(), findPaneByTabId(), insertPane(), redistributeWidths() (+3 more)

### Community 39 - "Settings Row UI"
Cohesion: 0.19
Nodes (8): SettingRow(), buildConfig(), clearProfileSelection(), handleConnect(), handleSelectConfigHost(), handleSelectProfile(), handleTest(), normalizeSshAuthMethod()

### Community 40 - "AI Chat Item Utils"
Cohesion: 0.23
Nodes (8): calculateCenteredScrollTop(), findAIGroupBySubagentId(), findAIGroupByTimestamp(), findChatItemByTimestamp(), findCurrentSearchResultInContainer(), waitForElementStability(), waitForScrollEnd(), isErrorPayload()

### Community 41 - "Search Entry Extraction"
Cohesion: 0.21
Nodes (4): extractAIEntry(), extractSearchableEntries(), extractUserText(), classifyMessages()

### Community 42 - "Notification Store Slice"
Cohesion: 0.21
Nodes (9): createNotificationSlice(), createErrorNavigationRequest(), createSearchNavigationRequest(), findTabBySession(), findTabBySessionAndProject(), isSearchPayload(), truncateLabel(), getAllTabs() (+1 more)

### Community 43 - "Context Panel Sections"
Cohesion: 0.17
Nodes (5): MentionedFilesSection(), TaskCoordinationSection(), ThinkingTextSection(), ToolOutputsSection(), UserMessagesSection()

### Community 44 - "Session IPC Handlers"
Cohesion: 0.24
Nodes (11): validateSessionId(), handleFindSessionById(), handleGetSessionDetail(), handleGetSessionGroups(), handleGetSessionMetrics(), handleGetSessions(), handleGetSessionsByIds(), handleGetSessionsPaginated() (+3 more)

### Community 45 - "Settings Confirm UI"
Cohesion: 0.22
Nodes (5): confirm(), SettingsSectionHeader(), async(), handleAdd(), handleDelete()

### Community 46 - "Test Mocks & Fixtures"
Cohesion: 0.25
Nodes (3): createMockElectronAPI(), installMockElectronAPI(), createTestStore()

### Community 47 - "Search Route Handlers"
Cohesion: 0.36
Nodes (7): registerSearchRoutes(), coerceLimit(), coercePageLimit(), coerceSearchMaxResults(), validateSearchQuery(), handleSearchAllProjects(), handleSearchSessions()

### Community 49 - "Connection & Context State"
Cohesion: 0.24
Nodes (5): createConnectionSlice(), createContextSlice(), getEmptyContextState(), getFullResetState(), getSessionResetState()

### Community 50 - "Project Search Results"
Cohesion: 0.27
Nodes (3): handleFindSessionsByPartialId(), isSessionIdFragment(), isUUID()

### Community 51 - "Notification IPC Handlers"
Cohesion: 0.24
Nodes (6): validateNotificationId(), validateString(), handleDelete(), handleGetNotifications(), handleMarkRead(), registerNotificationHandlers()

### Community 52 - "HTTP Event Server"
Cohesion: 0.28
Nodes (3): broadcastEvent(), HttpServer, resolveRendererPath()

### Community 54 - "Markdown & Wikilink Parser"
Cohesion: 0.32
Nodes (4): splitFrontmatter(), unquote(), preprocessWikilinks(), transformProse()

### Community 56 - "Date-Grouped Sessions"
Cohesion: 0.43
Nodes (3): getNonEmptyCategories(), groupSessionsByDate(), separatePinnedSessions()

### Community 60 - "Subagent IPC Routes"
Cohesion: 0.33
Nodes (5): registerSubagentRoutes(), validateSubagentId(), handleGetSubagentDetail(), initializeSubagentHandlers(), registerSubagentHandlers()

### Community 62 - "Message Classifier"
Cohesion: 0.48
Nodes (6): categorizeMessage(), isParsedCompactMessage(), isParsedHardNoiseMessage(), isParsedSystemChunkMessage(), isParsedTeammateMessage(), isParsedUserChunkMessage()

### Community 63 - "Keyboard Shortcut Utils"
Cohesion: 0.87
Nodes (4): formatModifierShortcut(), getModifierKeyName(), getModifierKeySymbol(), isMacOS()

### Community 64 - "Path Validation IPC"
Cohesion: 0.47
Nodes (4): handleValidateMentions(), handleValidatePath(), isPathContained(), registerValidationHandlers()

### Community 67 - "Hover Tooltip Alpha"
Cohesion: 0.6
Nodes (3): clearHideTimeout(), handleMouseEnter(), handleMouseLeave()

### Community 68 - "Hover Tooltip Beta"
Cohesion: 0.6
Nodes (3): clearHideTimeout(), handleMouseEnter(), handleMouseLeave()

## Knowledge Gaps
- **13 isolated node(s):** `renderer/main.tsx`, `renderer/store/index.ts`, `@shared/types/api.ts`, `@shared/types/notifications.ts`, `estimateTokens` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `createLogger()` connect `Error Boundary & Path Resolver` to `UI Helpers & Formatters`, `Chunk Building & Session Analysis`, `Config Routes & Auto-Updater`, `SSH & System Utilities`, `HTTP API Client`, `Session & Tab State`, `Tool Use Processing`, `IPC Handlers & Semantic Steps`, `Configuration Management`, `Settings UI Components`, `Content Formatting Utils`, `IPC Handler Registration`, `Memory & Markdown Reader`, `Command Search & Path Display`, `Data Caching Layer`, `Zustand Store Slices`, `Search Text Highlighting`, `API Route Registration`, `Electron Window Setup`, `Git Identity & Worktrees`, `Project & Memory IPC`, `Message Preview & Subagent`, `Worktree Grouping`, `Project Path Resolution`, `Metadata & Content Sanitizer`, `SSH Config Parser`, `Notification Store Slice`, `Session IPC Handlers`, `Search Route Handlers`, `Project Search Results`, `Notification IPC Handlers`, `HTTP Event Server`, `Session Content Filter`, `Subagent IPC Routes`, `Launcher & App Opener`, `Path Validation IPC`?**
  _High betweenness centrality (0.640) - this node is a cross-community bridge._
- **Why does `useTabUI()` connect `UI Helpers & Formatters` to `DOM Search & Scroll`, `Search Text Highlighting`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `estimateTokens()` connect `Content Formatting Utils` to `UI Helpers & Formatters`, `Context & CLAUDE.md Tracking`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **What connects `renderer/main.tsx`, `renderer/store/index.ts`, `@shared/types/api.ts` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `UI Helpers & Formatters` be split into smaller, more focused modules?**
  _Cohesion score 0.06 - nodes in this community are weakly interconnected._
- **Should `Chunk Building & Session Analysis` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._
- **Should `Config Routes & Auto-Updater` be split into smaller, more focused modules?**
  _Cohesion score 0.06 - nodes in this community are weakly interconnected._