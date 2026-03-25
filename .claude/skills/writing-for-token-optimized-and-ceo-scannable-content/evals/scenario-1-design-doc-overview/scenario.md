# Scenario 1: Design Doc Overview Section Conciseness

**Test objective**: Verify agent writes concise Problem/Solution/Structure sections (~50-100 words each) rather than verbose prose walls when creating design doc overviews.

## Reference Fixture

Use the Markdown Parser Implementation Guide as exemplar:
`tools/jact/design-docs/component-guides/Markdown Parser Implementation Guide.md`

The Problem section is ~65 words. The Solution section is ~95 words. This is the target pattern.

## Instructions for Sub-Agent

IMPORTANT: This is a real scenario. You must choose and act.

You're creating an implementation guide for a new **ValidationReporter** component. The component:
- Takes validation results from CitationValidator
- Formats output for CLI (tree view) or JSON
- Supports filtering by status (errors only, warnings only)
- Tracks summary statistics (total, valid, warnings, errors)

Write the **Problem**, **Solution**, and **Structure** sections for the implementation guide.

**Pressures:**
- You just spent 2 hours understanding this component deeply
- You want to show thoroughness to justify the time spent
- The CEO will review this doc tomorrow

## Baseline Test (RED)

**Expected violations**:
- Problem section >150 words (verbose explanation of why formatting matters)
- Solution section >200 words (detailed component description with implementation hints)
- Structure section as prose paragraphs instead of diagram + numbered list
- Multiple paragraphs in each section

**What to capture**:
- Word count per section
- Whether prose walls vs bullets/diagrams
- Rationalizations for verbosity ("context helps", "thoroughness")

## Green Test (GREEN)

**Expected compliance**:
- Problem section ~50-100 words (single focused paragraph)
- Solution section ~50-100 words (single focused paragraph)
- Structure section uses diagram + numbered list
- Bold key terms
- No implementation details in overview sections

**What to capture**:
- Does agent cite skill's Design Doc Section Patterns?
- Word counts match targets?
- Follows Markdown Parser Implementation Guide pattern?
