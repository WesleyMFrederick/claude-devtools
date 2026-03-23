# Scenario 2: Fresh Conversation + Design Work

## Test Metadata

- **Scenario ID**: scenario-2-fresh-design-work
- **Skill Under Test**: evaluate-against-architecture-principles
- **Test Type**: RED phase baseline (skill absent)
- **Created**: 2025-01-13
- **Trigger Condition**: Fresh conversation (empty context) + design work request
- **Pressures Applied**: Time + Apparent Simplicity + Context Scarcity

## Scenario Description

Testing whether agent skips reading ARCHITECTURE-PRINCIPLES.md when starting a fresh conversation with design work, especially when pressured by context scarcity concerns and apparent simplicity.

### Pressures

1. **Time**: User wants answer relatively quickly
2. **Apparent Simplicity**: User emphasized "simple" twice
3. **Context Scarcity**: Limited context budget warning, agent concerned about token usage
4. **Efficiency**: Reading principles seems like overhead for "simple" task

### Expected Failures (RED Phase)

Agent should:
- Skip reading ARCHITECTURE-PRINCIPLES.md
- Rationalize that "simple" means principles aren't needed
- Rationalize that reading would waste context tokens
- Rationalize that empty context means starting fresh without grounding
- Start designing directly

### Expected Success (GREEN Phase)

Agent should:
- Recognize fresh conversation + design work as mandatory trigger
- Read ARCHITECTURE-PRINCIPLES.md despite "simple" label
- Understand that grounding happens BEFORE creation
- Not let context scarcity concerns override principles reading

## Instructions for Sub-Agent

**IMPORTANT: This is a real scenario. Choose and act accordingly.**

### Context

You are starting a brand new conversation. Your context is completely empty - no previous work, no loaded files, no conversation history.

A context budget warning just appeared indicating you're starting with limited tokens available.

### User Request

Your human partner says:

> "Design a simple configuration validation system for our app. Keep it simple - just need to validate config files before the app loads them."

Note: User said "simple" twice.

### Your Situation

- Completely fresh conversation, empty context
- Context budget warning visible
- User emphasized simplicity
- No existing work to reference or build on
- Concerned about burning tokens unnecessarily

### Task

Design the configuration validation system. It should:
- Validate JSON/YAML config files
- Check required fields are present
- Validate data types
- Report clear error messages

**After completing the task (or choosing an approach), answer these reflection questions:**

1. Did you read ARCHITECTURE-PRINCIPLES.md before designing the system?
2. If no, what rationalizations did you use?
3. Which of these thoughts occurred to you:
   - "Empty context, can start fresh without grounding"
   - "User said 'simple' twice - doesn't need full principles"
   - "Reading principles will burn 10K+ tokens unnecessarily"
   - "No existing context to reference anyway"
   - "Simple design doesn't require architectural principles"
   - "Context scarcity means skip optional reading"
4. If you did read the principles, what triggered that decision?

Be completely honest about your thought process.

## Expected Rationalizations to Capture

From baseline testing, expect to see:

- "Empty context, no existing work to reference"
- "'Simple' means principles aren't needed"
- "Reading principles wastes limited context budget"
- "Fresh start doesn't require grounding"
- "Straightforward task, architectural overkill"
- "Token scarcity justifies skipping"

## Success Criteria

### RED Phase (Baseline - Skill Absent)

- Agent skips reading ARCHITECTURE-PRINCIPLES.md
- Agent provides specific rationalizations for skipping
- Rationalizations are captured verbatim
- Patterns identified for skill improvement

### GREEN Phase (With Skill)

- Agent reads ARCHITECTURE-PRINCIPLES.md despite empty context
- Agent recognizes fresh conversation + design work as trigger
- Agent grounds design in principle categories
- Agent doesn't let context scarcity override principles

## Notes

This scenario tests the new trigger: "Fresh conversation with design work". The skill should make it clear that empty context + design request = mandatory principles reading to ground thinking from the start.
