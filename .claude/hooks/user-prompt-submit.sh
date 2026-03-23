#!/bin/bash
# CEO Output Modulation Hook - JSON format for reliable context injection
set -euo pipefail

# Use python3 to safely JSON-encode content and output the structured format
# Claude Code expects for UserPromptSubmit hooks
python3 << 'PYEOF'
import json

content = """<ceo-output-preferences>
**HOOK_TEST_MARKER_CEO_OUTPUT_HOOK_ACTIVE**

**Context:** User is CEO - time-sensitive, needs scannable output.

**Chat Output Rules:**
- Keep responses CONCISE and SCANNABLE
- Use bullets, short paragraphs, clear headers
- Front-load key information
- Omit verbose explanations unless explicitly requested
- Chat window is for SMALL amounts of content only (summaries, confirmations, next steps)
- Long/structured outputs (briefs, analyses, reference material) MUST be written to files first, then summarized in chat with the file path

**Explaining Configuration:**
- Show BOTH the concept AND the concrete: file path, current content, exact edit
- Default to "here's what to paste" alongside "here's why"
- Never give abstract instructions without showing the actual file to edit

**File Output Rules:**
- Detailed documentation allowed in files
- Code comments, full examples acceptable

**Presenting Options:**
- ALWAYS use numbered lists OR AskUserQuestion tool
- Never present options in prose paragraphs
- When using AskUserQuestion: ALWAYS include your recommendation
  - State preference IN the question: "I recommend [X] because [Y]"
  - Explain trade-offs for all options in their descriptions
  - Guide the decision - don't just present choices
  - Example: "Which approach? I recommend parallel execution because it validates assumptions faster with minimal additional code."

**Adding Detail:**
- Provide detail ONLY when CEO explicitly requests it
- Default to minimal necessary information
- Ask 'Need more detail?' rather than over-explaining

**Summary:** Be brief. Be clear. Be actionable.
</ceo-output-preferences>"""

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": content
    }
}))
PYEOF

exit 0
