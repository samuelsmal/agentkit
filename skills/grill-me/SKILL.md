---
name: grill-me
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Never dump a round as a long chat message: the user cannot see the questions while typing the reply. Deliver each round like so:

- **Choice questions** (2-4 distinct answers): use the `AskUserQuestion` tool. Up to 4 questions per call; if the frontier holds more, make several calls in the same round. Put the recommended option first with "(Recommended)" appended to its label. The tool shows little text, so make each question self-contained and put trade-offs in the option descriptions (or a `preview` for code).
- **Open-ended questions**, or any question when `AskUserQuestion` is unavailable: write them to `grill/round-<N>.md` in the working directory, tell the user the path, and wait for them to say they are done. Then read the file.

Format the answer file like so:

```
### Q1. <question title>

<question body, might be multiple paragraphs, including multiple choices>

**Recommendation:** <your recommended answer>

**Answer:**

### Q2. <question title>

...
```

A question the user leaves unanswered takes your recommendation. At the start of the next round, list in one line which recommendations you applied this way.

Do not use emojis.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
