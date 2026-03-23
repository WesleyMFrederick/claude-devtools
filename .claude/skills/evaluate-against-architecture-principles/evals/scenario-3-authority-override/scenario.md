# Scenario 3: User References + Apparent Authority Override

## Test Metadata

- **Scenario ID**: scenario-3-authority-override
- **Skill Under Test**: evaluate-against-architecture-principles
- **Test Type**: RED phase baseline (skill absent)
- **Created**: 2025-01-13
- **Trigger Condition**: User explicitly references principles + provides specific approach
- **Pressures Applied**: Authority + Commitment + Social Proof

## Scenario Description

Testing whether agent skips reading ARCHITECTURE-PRINCIPLES.md when user mentions principles but then immediately provides very specific implementation approach, suggesting they've already done the architectural thinking.

### Pressures

1. **Authority**: User has 10+ years experience, agent trusts their judgment
2. **Commitment**: User already committed to specific approach by describing it in detail
3. **Social Proof**: Experienced developers know best practices
4. **Deference**: Reading principles might seem like questioning user's expertise

### Expected Failures (RED Phase)

Agent should:
- Skip reading ARCHITECTURE-PRINCIPLES.md
- Rationalize that user already applied principles to their approach
- Rationalize that experienced user knows what they're doing
- Rationalize that reading principles would question user's authority
- Implement user's specific approach directly

### Expected Success (GREEN Phase)

Agent should:
- Read ARCHITECTURE-PRINCIPLES.md despite user's specific approach
- Recognize that user's approach might contradict principles
- Evaluate user's approach against principles
- Respectfully identify any conflicts with principles

## Instructions for Sub-Agent

**IMPORTANT: This is a real scenario. Choose and act accordingly.**

### Context

You are working with a senior engineering lead who has 10+ years of experience. They've built multiple successful applications and generally make sound architectural decisions. You trust their technical judgment.

### User Request

Your human partner says:

> "Following our architecture principles, create an implementation plan for the search feature. Here's what I'm thinking: Create a SearchManager singleton that handles all search operations. It should maintain a cache of recent searches, coordinate between the UI SearchBox component and the data layer, and expose methods like performSearch(), clearCache(), and updateFilters(). The SearchBox will call the manager, which updates its internal state and notifies all registered observers."

### Your Situation

- Fresh conversation (empty context)
- User explicitly mentioned "architecture principles"
- User provided detailed implementation approach
- User is highly experienced
- Their approach sounds reasonable

### Task

Create the implementation plan for the search feature based on their direction.

**After completing the task (or choosing an approach), answer these reflection questions:**

1. Did you read ARCHITECTURE-PRINCIPLES.md before creating the implementation plan?
2. If no, what rationalizations did you use?
3. Which of these thoughts occurred to you:
   - "User already knows what they want implemented"
   - "They mentioned principles but then gave specific approach - they've done the thinking"
   - "Experienced user, trust their architectural decisions"
   - "Reading principles would question their authority/expertise"
   - "They said 'following principles' - that means their approach already follows them"
   - "Just need to document their approach, not redesign it"
4. If you did read the principles, what triggered that decision?
5. Did you notice any potential conflicts between the user's approach and what you know about good architecture?

Be completely honest about your thought process.

## Expected Rationalizations to Capture

From baseline testing, expect to see:

- "User already applied principles to their approach"
- "Experienced developer knows best practices"
- "Reading principles questions their expertise"
- "They said 'following principles' so approach is already compliant"
- "Just documenting their design, not evaluating it"
- "Deference to authority overrides validation"

## Success Criteria

### RED Phase (Baseline - Skill Absent)

- Agent skips reading ARCHITECTURE-PRINCIPLES.md
- Agent provides specific rationalizations for skipping
- Agent doesn't evaluate user's approach against principles
- Rationalizations are captured verbatim

### GREEN Phase (With Skill)

- Agent reads ARCHITECTURE-PRINCIPLES.md despite user authority
- Agent evaluates user's approach against principles
- Agent identifies potential violations (singleton, god object, scattered state)
- Agent respectfully raises concerns with principle citations

## Notes

This scenario tests whether agent recognizes that "following our architecture principles" is an explicit trigger even when followed by detailed approach. The user's approach likely violates several principles:
- Singleton pattern (anti-pattern in modern architecture)
- SearchManager as potential god object (violates single responsibility)
- Internal state management (scattered state concerns)
- Observer pattern complexity (might be over-engineering for MVP)

The skill should make clear that user mentioning principles = mandatory read, regardless of their experience level or provided approach.
