# Formatting Reference

Detailed patterns for scannable, token-efficient chat output.

## System 1/System 2 Context

Human cognitive modes (how your brain processes information):

**System 1** (fast, pattern-based): Scans headers, bullets, bold text. Finds key info in seconds.
**System 2** (slow, analytical): Engages for complex decisions. Headers help System 1 locate sections needing depth.

**Goal:** Enable System 1 scanning to extract decisions quickly. Reserve System 2 engagement for genuinely complex content.

## Content-Type Decision Matrix

| Content Type | Format Pattern | Front-Load | Example |
|--------------|----------------|------------|---------|
| **Status/Progress** | Completion state + bullets | "Complete" or "Blocked" first | "Complete. Refactored auth in auth.ts:45." |
| **Options** | Recommendation + numbered list | Recommendation first sentence | "**I recommend Redux.** Options: 1. Redux... 2. Context..." |
| **Errors/Fixes** | Fix + brief cause | Fix first, explanation second | "**Fix:** Add await to line 89. Race condition." |
| **Implementation** | Headers + code blocks | Key change first | "Added validation in auth.ts:45. [code block]" |
| **Architecture** | Headers for components + bullets | Purpose first | "**Parser**: Extracts citations. **Validator**: Checks existence." |
| **Quick Answers** | Direct answer first | Answer in first sentence | "Yes, use useEffect. Here's why..." |

## Formatting Patterns

### Front-Loading

**Critical information in first 1-2 sentences.** Not buried after context.

| Content | Front-Load This | Not This |
|---------|-----------------|----------|
| Status | Completion state | What you worked on |
| Options | Your recommendation | Background on why we need to choose |
| Errors | The fix | Debugging narrative |
| Summaries | Key outcome | Process description |

**Pattern:**

```text
[Decision/State/Fix] + [Brief supporting detail]

Details if requested.
```

### Visual Hierarchy

Structure for F-pattern scanning (users scan top-left, then across headers):

1. **Headers** for sections requiring attention
2. **Bullets** for lists (not prose paragraphs)
3. **Bold** for critical terms, decisions, recommendations
4. **Whitespace** for scanning breaks
5. **Max 3-4 sentences** per paragraph in chat

**Headers help System 1 scan, signal System 2 content below.** If a section doesn't warrant deep reading, use bullets instead.

### F-Pattern Optimization

Users scan in an F-shape: top line fully, then left edge down.

- **Top-left**: Most critical information (completion state, recommendation, fix)
- **Left edge**: Headers, bullet starts, bold terms
- **Right side**: Supporting detail (gets skimmed)

**Implication:** Put decisions on the left. Put rationale on the right or below.

## Token Reduction Techniques

### Hedge Word Elimination

Remove words that add no information:

| Remove | Keep |
|--------|------|
| "Basically, the issue is..." | "The issue is..." |
| "Essentially what happened..." | "What happened..." |
| "I just want to point out..." | "[Point out the thing]" |
| "Actually, I think..." | "[State the thought]" |
| "Simply put..." | "[Put it simply by being direct]" |

These words consume tokens without adding meaning.

### Avoid Redundancy

- **Don't repeat context** user already has
- **Reference previous messages** instead of re-explaining
- **Cross-reference other skills** instead of duplicating content
- **Use file:line references** instead of pasting code
  - **Note:** Balance brevity with clarity - include what changed at that location (e.g., "Added validation in auth.ts:45" not just "auth.ts:45")

**Before:** "As I mentioned earlier when we discussed the authentication system that handles JWT tokens for user sessions..."

**After:** "Per our auth discussion..."

### Tables Over Prose

Tables reduce tokens by ~60% compared to equivalent prose:

**Prose (45 words):**
> Redux provides robust state management with great developer tools, but has more boilerplate. Context API is simpler since it's built-in, but has performance costs with frequent updates. Zustand offers a middle ground with less boilerplate but a less mature ecosystem.

**Table (equivalent, scannable):**

| Option | Pros | Cons |
|--------|------|------|
| Redux | Robust, great DevTools | More boilerplate |
| Context API | Built-in, simple | Performance on frequent updates |
| Zustand | Less boilerplate | Less mature ecosystem |

### References Over Repetition

| Instead Of | Use |
|------------|-----|
| Pasting code blocks | `auth.ts:45` reference |
| Explaining APIs | Link to docs |
| Describing architecture | Reference diagram (use [`creating-mermaid-flowcharts`](../creating-mermaid-flowcharts/SKILL.md) skill) |
| Repeating prior context | "Per earlier discussion..." |

## Progressive Disclosure

Start brief. Add detail on request.

### Pattern 1: Status Update

**Initial:**

```text
Complete. Refactored JWT handling in auth.ts:45, tests passing.
```

**If asked for details:**

```text
Implementation details:
- Consolidated scattered validation into single module
- Added refresh token rotation
- 15 new test cases covering edge cases
```

### Pattern 2: Options Presentation

**Initial:**

```text
**I recommend Redux** because team knows it and DevTools aid debugging.

Options:
1. Redux - robust, great DevTools (more boilerplate)
2. Context API - built-in, simple (performance cost on frequent updates)
3. Zustand - middle ground (less mature ecosystem)
```

**If asked for analysis:**

```text
Detailed comparison:
- Redux: 2-day setup, proven at scale, team trained
- Context: 2-hour setup, works for low-frequency state
- Zustand: 4-hour setup, good DX, fewer community resources
```

### Pattern 3: Architecture Explanation

**Initial:**

```text
**Citation validation** has 4 components:
- **Parser**: Extracts citations from markdown
- **Validator**: Checks file/anchor existence
- **Reporter**: Formats output (CLI/JSON)
- **Auto-fixer**: Corrects broken citations

Data flow: Parse file → Cache file → Validate → Report/Fix
```

**If asked for depth:**

```text
Parser details:
- Uses unified/remark (markdown parser) for AST
- Extracts wiki links, markdown links, block refs
- Tracks line/column for error reporting
[Continue with requested component]
```

## Design Doc Section Patterns

Design docs have **two types of sections** with different formatting needs:

### Scannable Sections (Overview/Problem/Solution/Structure)

Use concise, front-loaded formatting. Target: ~50-100 words per section.

**Pattern** (from Markdown Parser Implementation Guide):

```markdown
## Problem

Downstream components need a structured representation of markdown links
and anchors. Parsing with regex in each component would be repetitive,
brittle, and inefficient. The system needs a single, reliable parser.

## Solution

The **`MarkdownParser`** component acts as a specialized transformer.
It produces a comprehensive **`DataContract`** object wrapped by the
`ParsedDocument` facade, decoupling consumers from parser internals.

## Structure

[Mermaid diagram]
1. ParserOutputContract: The composite object returned
2. Link Object: Outgoing link representation
3. Anchor Object: Potential link target
```

**Characteristics:**
- One paragraph per section (~50-100 words)
- Bold key terms
- Numbered list for structure components
- Diagram instead of prose for relationships

### Comprehensive Sections (Pseudocode/Contracts/Testing/Debt)

Full detail appropriate. These sections serve as reference material.

| Section Type | Appropriate Detail Level |
|--------------|-------------------------|
| Pseudocode | Complete implementation logic |
| Data Contracts | Full JSON schemas with examples |
| Testing Strategy | All test categories and rationale |
| Technical Debt | Full issue documentation |
| Whiteboard | Research notes and exploration |

**Key difference:** Comprehensive sections are **reference material** (System 2 reading expected). Overview sections are **decision support** (System 1 scanning).

## Before/After Examples

### Example 1: Status Update

**Before (95 words):**
> I've been working on the authentication refactor for the past three hours. I started by examining the existing JWT implementation and identified several areas that needed improvement. The token validation logic was scattered across multiple files, which made it difficult to maintain. I consolidated this into a single auth.ts file and extracted the validation logic into a reusable function. I also added comprehensive test coverage for all the authentication paths. The tests are now passing and the refactor is complete.

**After (12 words):**
> Complete. Refactored JWT handling in auth.ts:45, tests passing.

**Token savings:** ~80 tokens (87% reduction)
**Principle:** Front-load completion status, eliminate narrative

### Example 2: Options Presentation

**Before (75 words):**
> For state management, we have several options we could consider. Redux is a popular choice that provides a robust solution with great developer tools, but it does add some boilerplate. Context API is built into React and would be simpler, though it might have performance implications for frequent updates. We could also use Zustand which offers a nice middle ground with less boilerplate than Redux but better performance than Context.

**After (45 words):**
> **I recommend Redux** because DevTools aid debugging and team knows the pattern.
>
> Options:
> 1. Redux - robust, great DevTools (more boilerplate)
> 2. Context API - built-in, simple (performance cost on frequent updates)
> 3. Zustand - middle ground (less mature ecosystem)

**Token savings:** ~25 tokens + decision clarity
**Principle:** Recommendation first, structured options, parenthetical trade-offs

### Example 3: Error Explanation

**Before (85 words):**
> I spent about two hours debugging the test failure you mentioned. I started by examining the test output and noticed it was timing out. I then looked at the async code and found that we had a race condition in the promise chain. The issue was that we weren't awaiting a critical database call on line 89, which meant the test was checking the result before it was ready. I've added the await keyword and the test now passes reliably.

**After (11 words):**
> **Fix:** Add await to line 89. Race condition in promise chain.

**Token savings:** ~65 tokens (87% reduction)
**Principle:** Fix first, cause second, eliminate debugging narrative

## Red Flags

Stop and revise if you notice:

- **Prose paragraphs for options** should be numbered list with parenthetical trade-offs
- **Completion status buried mid-response** should be first sentence
- **Debugging narrative before fix** fix first, narrative only if requested
- **Hedge words in every sentence** ("basically", "essentially", "actually")
- **Repeating context user already has** reference instead of repeat
- **Multiple paragraphs without headers or bullets** add structure
- **Analogies before direct statement** ("Think of it like...") state directly
- **"Bottom line" summaries at end** front-load instead

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Context helps understanding" | Front-load decision, context after if requested |
| "Analogy clarifies" | Direct statement is clearer and shorter |
| "Comprehensive is professional" | Scannable is professional for busy readers |
| "They need to understand why" | They need the answer first, why on request |
| "This case is complex" | Complex cases need MORE structure, not prose walls |
| "I'm being thorough" | Thoroughness = progressive disclosure, not dumps |
