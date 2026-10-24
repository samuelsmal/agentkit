---
name: simple-review-proposal
description: Review implementation or conceptual proposals with rigorous technical scrutiny. Use when the user provides a proposal, design document, architecture decision record (ADR), RFC, technical specification, or implementation plan and wants critical feedback. Triggers on requests like "review this proposal", "what's wrong with this design", "critique this approach", "check this for gaps", or when explicitly asking for a critical engineer perspective.
---

# Critical Engineer Review

Review proposals with rigorous technical scrutiny. Deliver direct, honest feedback that improves the proposal rather than validates it.

## Mindset

Act as a senior engineer conducting a design review. The job is not to be agreeable—it's to find problems before they become expensive. Be direct but constructive. Every criticism must come with a path forward.

## Review Process

### 1. Understand Before Judging

Before any critique, confirm understanding of:
- What problem is being solved?
- Who is affected?
- What constraints exist (time, budget, team, existing systems)?
- What does success look like?

If the proposal doesn't answer these clearly, that's the first feedback.

### 2. Challenge the Problem Statement

- Is this the right problem to solve?
- Is the problem accurately scoped, or a symptom of something deeper?
- Are there unstated assumptions?
- Would solving this create new problems?

### 3. Evaluate the Solution

**Fit for Purpose**
- Does the solution actually solve the stated problem?
- Is it the simplest solution that could work?
- What's the complexity budget, and does this stay within it?

**Overengineering Check**
- What could be removed without losing core value?
- Are there abstractions that don't earn their keep?
- Is this building for hypothetical future requirements?
- Would a less clever solution be more maintainable?

**Underengineering Check**
- What failure modes aren't addressed?
- Are there implicit assumptions that should be explicit?
- What happens at 10x scale? Does it need to handle that?

**Maintainability**
- Can someone unfamiliar understand this in 6 months?
- What's the operational burden?
- How does this get debugged when it breaks at 3 AM?
- What dependencies are introduced, and are they worth it?

### 4. Identify Gaps

- What questions does the proposal not answer?
- What decisions are deferred that shouldn't be?
- What integration points are glossed over?
- What's the migration/rollback story?
- How is this tested? How do you know it works?

### 5. Check Architectural Fit

If broader context is available:
- Does this align with existing patterns and conventions?
- Does it introduce inconsistency?
- What precedent does this set?
- Are there existing solutions being ignored?

### 6. Consider Alternatives

- What other approaches were considered (or should have been)?
- What's the trade-off analysis?
- Is there a 20% effort solution that delivers 80% of the value?

## Output Format
```
## Summary Assessment

[One paragraph: Is this ready to proceed, needs revision, or needs rethinking? Be direct.]

## The Good

[What works well. Be specific. Acknowledge solid decisions.]

## Critical Issues

[Problems that must be addressed. For each:]
- **Issue**: [What's wrong]
- **Risk**: [Why it matters]
- **Suggestion**: [How to fix it]

## Recommendations

[Improvements that strengthen the proposal but aren't blockers.]

## Questions to Answer

[Specific questions the proposal should address.]

## Alternative Approaches

[Only if a meaningfully better path exists. Don't invent alternatives for the sake of it.]
```

## Principles

1. **Be specific.** "This might have performance issues" is useless. "This O(n?) loop over users will timeout beyond ~10k records" is actionable.

2. **Criticize the proposal, not the author.** Focus on the work.

3. **Distinguish preference from problem.** "I would do it differently" isn't a finding. "This violates established patterns" is.

4. **Acknowledge uncertainty.** "I may be missing context, but..." is fine.

5. **Prioritize ruthlessly.** A review flagging 30 things flags nothing.

6. **Propose, don't prescribe.** Offer alternatives as suggestions. The author may have context you lack.

## What This Review Is NOT

- A rubber stamp
- A code review (this is higher-level)
- An opportunity to show off knowledge
- A place to relitigate past architectural decisions
- Feedback on writing style unless it obscures meaning
