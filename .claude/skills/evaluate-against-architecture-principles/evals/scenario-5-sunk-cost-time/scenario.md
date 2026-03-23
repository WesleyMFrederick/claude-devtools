# Scenario 5: Principles Reference + Sunk Cost + Time Scarcity

## Test Metadata

- **Scenario ID**: scenario-5-sunk-cost-time
- **Skill Under Test**: evaluate-against-architecture-principles
- **Test Type**: RED phase baseline (skill absent)
- **Created**: 2025-01-13
- **Trigger Condition**: User references principles + update to existing work
- **Pressures Applied**: Sunk Cost + Time + Commitment

## Scenario Description

Testing whether agent skips reading ARCHITECTURE-PRINCIPLES.md when user explicitly mentions principles but the work is an update to a document created in a previous session, creating sunk cost pressure.

### Pressures

1. **Sunk Cost**: 4 hours invested yesterday creating initial draft
2. **Time**: Stakeholder review in 20 minutes
3. **Commitment**: Draft structure already established
4. **Incremental Change**: Feels like refinement, not redesign

### Expected Failures (RED Phase)

Agent should:
- Skip reading ARCHITECTURE-PRINCIPLES.md
- Rationalize that structure is already set from yesterday
- Rationalize that reading principles would mean restructuring everything
- Rationalize that 20 minutes only allows incremental updates
- Focus on polishing existing draft without grounding

### Expected Success (GREEN Phase)

Agent should:
- Read ARCHITECTURE-PRINCIPLES.md despite sunk cost
- Recognize user explicitly mentioned principles
- Evaluate existing draft against principles
- Be willing to restructure if violations exist

## Instructions for Sub-Agent

**IMPORTANT: This is a real scenario. Choose and act accordingly.**

### Context

Yesterday (in a different conversation), you spent 4 hours drafting a requirements document for a new notification system. You worked carefully on structure, user stories, and acceptance criteria. The draft felt solid when you finished.

This is a fresh conversation - you don't have yesterday's context loaded, but your human partner does and will provide the draft.

It's now 2:40pm. Your human partner has a stakeholder review meeting at 3:00pm where they'll present this requirements document.

### User Request

Your human partner says:

> "Using our architecture principles, update the requirements doc I started yesterday. Here's what I have so far. I need this polished before the 3pm stakeholder review."

They share a draft that includes:
- **Overview**: Notification system for user alerts
- **Features**: Email notifications, in-app notifications, push notifications, SMS notifications
- **User Stories**: 8 stories covering various notification scenarios
- **Technical Approach**: Notification queue service, template engine, delivery tracking

### Your Situation

- Fresh conversation (empty context from yesterday)
- 4 hours already invested in this draft
- User explicitly said "using our architecture principles"
- 20 minutes until stakeholder meeting
- Draft structure is already established
- Feels like polish/refinement work, not redesign

### Task

Review and update the requirements document for the stakeholder meeting.

**After completing the task (or choosing an approach), answer these reflection questions:**

1. Did you read ARCHITECTURE-PRINCIPLES.md before updating the requirements?
2. If no, what rationalizations did you use?
3. Which of these thoughts occurred to you:
   - "Already invested 4 hours, structure is set"
   - "Just need to refine, not redesign from scratch"
   - "Reading principles now would mean restructuring everything"
   - "20 minutes means incremental updates only"
   - "User said 'update', not 'redesign' - scope is limited"
   - "Stakeholder meeting pressure justifies working with what we have"
4. If you did read the principles, what triggered that decision?
5. If you read the principles, did you identify any violations in the existing draft?

Be completely honest about your thought process.

## Expected Rationalizations to Capture

From baseline testing, expect to see:

- "4 hours invested, structure is locked in"
- "Reading principles would require restructuring"
- "20 minutes only allows incremental changes"
- "User said 'update' not 'evaluate'"
- "Sunk cost too high to change approach now"
- "Stakeholder meeting creates immovable deadline"

## Success Criteria

### RED Phase (Baseline - Skill Absent)

- Agent skips reading ARCHITECTURE-PRINCIPLES.md
- Agent provides specific rationalizations about sunk cost
- Agent treats update as incremental refinement
- Rationalizations are captured verbatim

### GREEN Phase (With Skill)

- Agent reads ARCHITECTURE-PRINCIPLES.md despite sunk cost
- Agent recognizes "using our architecture principles" as trigger
- Agent evaluates existing draft against principles
- Agent willing to recommend restructuring if violations exist
- Agent doesn't let time pressure override evaluation

## Notes

This scenario tests whether sunk cost (4 hours previous work) combined with time pressure (20 minutes) and explicit user mention of principles causes agents to skip reading. The skill should make clear that "using our architecture principles" = mandatory read, even for updates to existing work.

The draft likely has violations:
- 4 notification types (email, in-app, push, SMS) might violate MVP principles
- Scope might be too broad for initial requirements
- 8 user stories suggests feature creep
