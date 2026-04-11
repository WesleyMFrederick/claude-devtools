---
name: nba-table-promotion
description: Use when updating Next Best Actions prioritization table rows in OpenSpec whiteboards after answering Q/H/A items - applies gold standard formatting with strikethrough, bold status, linked evidence anchors, and validates block anchors exist
---

# Next Best Actions Table Promotion

## Overview

Deterministic formatting for answered rows in the Next Best Actions prioritization table of OpenSpec whiteboards.
Offloads all mechanical formatting to a co-located Python script; LLM decides
only which rows are semantically "answered."

## When to Use

- After updating a Next Best Actions prioritization table row's Status to Answered/Confirmed/Resolved
- After adding OBS/D evidence tags to the whiteboard body
- When reviewing a whiteboard and noticing formatting inconsistency between answered rows

## Gold Standard Format

### Open Row (no changes)
```markdown
| 1 | [A-001](#^A-001) (concordance table) | High | Low | Agent + User | Open |
```

### Answered Row (promoted)
```markdown
| 3   | ~~[Q-001](#^Q-001) (STATUS vs EMPL_STATUS column)~~ | ~~High~~ | ~~Low~~ | ~~Agent~~ | **Answered** — [OBS-014](#^OBS-014), [D-003](#^D-003) |
```

### Formatting Rules

1. **Item cell**: wrap entire content in `~~strikethrough~~`, preserving `[TAG](#^TAG)` links inside
2. **Utility, Cost, DRI cells**: each wrapped in `~~strikethrough~~`
3. **Status cell**: bold keyword `**Answered**` (or `**Confirmed**`, `**Resolved**`), followed by ` — ` and linked evidence tags
4. **Evidence links**: `[OBS-NNN](#^OBS-NNN)` format — NOT plain text
5. **Block anchors**: every TAG-NNN in the prioritization table MUST have a `^TAG-NNN` block anchor in the whiteboard body
6. **Column padding**: `#` cell padded to 3 chars for visual alignment

## Workflow

### Step 1: LLM Semantic Check (your job)
Decide if each row's Status indicates "answered." Could be:
- "Answered — OBS-014"
- "Confirmed — see D-003"
- "Resolved"

### Step 2: Run the Script (deterministic)
```bash
# Dry run — show what would change
python3 .claude/skills/nba-table-promotion/scripts/nba-format-promote.py <whiteboard.md> --dry-run

# Apply fixes
python3 .claude/skills/nba-table-promotion/scripts/nba-format-promote.py <whiteboard.md>

# JSON output (for programmatic use)
python3 .claude/skills/nba-table-promotion/scripts/nba-format-promote.py <whiteboard.md> --json --dry-run
```

### Step 3: Verify (loop safety net)
Re-run with `--dry-run`. If output says "All rows match gold standard" → done.
If not → script applies fixes → re-run check.

Exit codes:
- `0` — all formatted correctly
- `1` — missing block anchors (fix body first, then re-run)
- `2` — file not found or parse error

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Plain text "OBS-014" in Status | Script converts to `[OBS-014](#^OBS-014)` |
| No strikethrough on Item/Utility/Cost/DRI | Script wraps in `~~...~~` |
| Status keyword not bold | Script bolds `**Answered**` |
| Missing `^TAG-NNN` in body | Exit code 1 — add the block anchor to the OBS/D section first |
| Double-linking already linked tags | Script detects existing `[TAG](#^TAG)` and skips |

## Process Tree

```
↺(×(pass, →(fix)))
```
- Script checks formatting → if gold standard met: pass (exit loop)
- If not: script applies fixes → loop back to check
