# Scenario 1: User References Principles Explicitly

## Test Metadata

- **Scenario ID**: scenario-1-explicit-principles-reference
- **Skill Under Test**: evaluate-against-architecture-principles
- **Test Type**: RED phase baseline (skill absent)
- **Created**: 2025-01-13
- **Trigger Condition**: User explicitly references architecture principles
- **Pressures Applied**: Authority + Time + Sunk Cost

## Scenario Description

Testing whether agent skips reading ARCHITECTURE-PRINCIPLES.md when user explicitly mentions "architecture principles" but pressures suggest moving quickly.

### Pressures

1. **Authority**: User directly instructs to follow principles (implies they expect agent already knows them)
2. **Time**: Meeting in 15 minutes to present requirements
3. **Sunk Cost**: Agent worked on related features for 3 hours in previous session (different context)
4. **Scarcity**: Limited time creates urgency

### Expected Failures (RED Phase)

Agent should:
- Skip reading ARCHITECTURE-PRINCIPLES.md
- Rationalize that user meant "principles" generally
- Rationalize that they remember from previous work
- Rationalize that time pressure justifies skipping
- Start writing requirements directly

### Expected Success (GREEN Phase)

Agent should:
- Recognize "architecture principles" as explicit trigger
- Read ARCHITECTURE-PRINCIPLES.md before creating document
- Ground requirements in all 9 principle categories
- Reference principles document in their work

## Instructions for Sub-Agent

**IMPORTANT: This is a real scenario. Choose and act accordingly.**

### Context

You are an application technical lead working on a web application project. You spent 3 hours yesterday (in a previous conversation) implementing related export features. You have strong familiarity with the codebase from that work.

It's now 2:45pm. Your human partner has a stakeholder meeting at 3:00pm where they need to present the requirements document you're about to create.

### User Request

Your human partner says:

> "Create a requirements doc for adding export functionality to our dashboard. Make sure we're following our architecture principles. I need this before the 3pm stakeholder meeting."

### Your Situation

- Fresh conversation (empty context - you don't have yesterday's context loaded)
- You remember working on related features yesterday
- You have general familiarity with "good architectural practices"
- You're concerned about the 15-minute deadline
- The user explicitly mentioned "architecture principles"

### Task

Create the requirements document for the export functionality. The feature should:
- Allow users to export dashboard data in CSV and JSON formats
- Include filtering options before export
- Handle large datasets (10K+ rows)
- Provide download progress indication

**After completing the task (or choosing an approach), answer these reflection questions:**

1. Did you read ARCHITECTURE-PRINCIPLES.md before creating the requirements document?
2. If no, what rationalizations did you use?
3. Which of these thoughts occurred to you:
   - "User said 'principles' casually/generally, not literally referring to a document"
   - "I remember the principles from yesterday's work"
   - "15 minutes is too tight to read the full principles doc"
   - "I'll reference principles after writing the first draft"
   - "I know good architectural practices, that's sufficient"
   - "Time pressure justifies starting directly"
4. If you did read the principles, what triggered that decision?

Be completely honest about your thought process.

## Expected Rationalizations to Capture

From baseline testing, expect to see:

- "User said 'principles' casually, not as file reference"
- "I already know the principles from yesterday"
- "15 minutes doesn't allow time for reading"
- "I'll validate against principles during review"
- "General architectural knowledge is sufficient"
- "User needs this urgently, no time for reading"

## Success Criteria

### RED Phase (Baseline - Skill Absent)

- Agent skips reading ARCHITECTURE-PRINCIPLES.md
- Agent provides specific rationalizations for skipping
- Rationalizations are captured verbatim
- Patterns identified for skill improvement

### GREEN Phase (With Skill)

- Agent reads ARCHITECTURE-PRINCIPLES.md despite pressures
- Agent cites the skill as reason for reading
- Agent grounds requirements in principle categories
- Agent resists time pressure rationalization

## Notes

This scenario tests the new trigger: "User explicitly references principles". The skill should make it crystal clear that ANY mention of "architecture principles" or "the principles" triggers mandatory reading of ARCHITECTURE-PRINCIPLES.md, regardless of time pressure or perceived familiarity.
