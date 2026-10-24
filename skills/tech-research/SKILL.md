---
name: tech-research
description: >-
  Research technology architecture and tooling questions on the web and write a decision-ready
  Markdown report with an executive summary on top, backed by per-question research notes. Starts
  by asking the user clarifying questions to expose blind spots in the request. Use this whenever
  the user wants to research, compare, evaluate or assess platforms, vendors, frameworks, tools,
  cloud services or architecture options (for example "Snowflake vs Databricks", "can X replace
  Y", "options to consolidate our data stack", "is tool Z mature enough", "what does it cost to
  run A in region B"), or asks for a market scan, technology landscape or vendor direction, even
  if they do not say "research" or "report".
---

# Tech research

Turn a technology question into a report that a decision maker can act on from its executive
summary alone. The work has five phases. Phases 1 and 3 stop for the user; the rest run without
stops.

```
1. Blind-spot questions  ->  2. Scan  ->  3. Outline checkpoint  ->  4. Parallel research  ->
5. Report + format check
```

Outputs, relative to the project root:

- `reports/<Headline>.md`: the report. Format: `references/report-format.md`.
- `research_notes/<Report topic>/<sub_question>.md`: one note per sub-question. Format:
  `references/note-format.md`.

All Markdown is wrapped at 100 characters. A pre-commit hook enforces this (see the last section).

## Before phase 1: read what exists

List `reports/` and `research_notes/`. If earlier reports exist, read their executive summaries:
the new question often builds on them, and the user expects you not to redo settled research.
Note today's date. Technology facts expire fast, so every note and report carries it.

## Phase 1: blind-spot questions (stop)

The user's prompt is a compressed view of what they need. Your job here is to find what the
prompt leaves out that would change where the research goes, before you spend an hour searching
in the wrong direction. Do not search the web yet, except for a quick term lookup you need to
ask a sensible question.

Consider these dimensions and ask only about the ones the prompt and the existing files leave
open, and whose answer would change the research:

- **The decision.** What decision does this research support, who makes it, and by when? A
  "should we migrate" report differs from a "brief me on the market" report.
- **Constraints.** Cloud and region, data residency, existing stack that must stay, budget,
  team skills, licensing, procurement rules.
- **Options in scope.** Which candidates did the user not name? Include "keep the current
  setup" and the obvious alternative the prompt skips.
- **Criteria.** Latency, cost, maturity, lock-in, operating effort, migration effort. Which
  matter most?
- **Maturity tolerance and horizon.** GA only, or are previews acceptable? Decision for now or
  for next year?
- **Depth and audience.** Internal notes or a client-facing report? Cost figures and effort
  estimates wanted?

Ask 4–8 questions in one round. Give your recommended answer for each, so the user can accept
the defaults quickly. A question the user leaves unanswered takes your recommendation; say in
one line which ones you applied.

Delivery: if the `AskUserQuestion` tool is available, use it (up to 4 questions per call, the
recommended option first with "(Recommended)" in its label, trade-offs in the option
descriptions). Otherwise write the questions to `research_notes/<Report topic>/questions.md`, in
the format `### Q1. <title>`, body, `**Recommendation:**`, `**Answer:**`, give the user the
path, and wait for them to say they are done.

## Phase 2: scan

Run a short landscape scan, about 5–10 searches: the latest releases and status of each option,
the terms the vendors use, and options or recent events the user did not mention (an
acquisition, a deprecation, a new GA). The scan exists to make the outline right, not to answer
the question. Do not write notes yet.

## Phase 3: outline checkpoint (stop)

Propose to the user:

- **Sub-questions**, typically 4–8. Each becomes one research note and one parallel worker. Cut
  them so they do not overlap: per option (stack, pricing, regional availability) or per
  cross-cutting concern (cost, maturity, migration effort) — whichever matches the decision.
- **Scan findings that change the scope**, for example "Ververica retired its managed cloud in
  June 2026, so the comparison is BYOC vs self-managed".
- **A draft headline and section list** for the report.

Ask the user to confirm, add or drop sub-questions. Use the same delivery as phase 1.

## Phase 4: parallel research

Start one subagent per sub-question, all in the same turn, so they run concurrently. If you have
no subagent tool, work through the sub-questions yourself, one after the other, with the same
brief and note format.

Each subagent starts with no context, so its brief must carry everything it needs:

```
You research one sub-question for a technology report. Today is <date>.
Context: <the architecture or situation, constraints, region, the user's answers that matter>.
Sub-question: <the question>.
Also check: <specific points from the scan or the user's answers>.
Out of scope: <what other workers cover>.
Write your findings to research_notes/<Report topic>/<slug>.md, following the format in
<absolute path to references/note-format.md>. Wrap lines at 100 characters.
Prefer primary sources (vendor docs, release notes, pricing pages, GitHub, filings). Date every
fact, give versions and GA/preview status, tag key facts [confirmed] or [unconfirmed], and list
what you could not verify under "Gaps". Reply with the note's verdict in 3 sentences.
```

## Phase 5: report and format check

1. Read every note in full, not only the verdicts. Where notes contradict each other, check the
   primary source yourself and resolve it, or present the contradiction as an open question.
2. Write `reports/<Headline>.md` following `references/report-format.md`. The executive summary
   comes first and must stand on its own. Turn the notes' gaps into the open-questions section.
3. Format and check every Markdown file you wrote (see below). Fix headings or other lines the
   check still reports.
4. Reply to the user with the report path, the answer and the recommendation in two or three
   sentences, and the open points that could change it.

## Line length: 100 characters

Wrap all Markdown at 100 characters as you write it. Short lines make diffs and reviews in the
editor readable, which is how these reports are reviewed. The project's pre-commit hook rewraps
prose with `mdformat --wrap 100` and then runs `scripts/check_md_width.py`, which fails on any
line over 100 characters that is not a table row, code, a link definition or an unbreakable URL.

Run the same check yourself before you finish, so the files are clean before anyone commits:

```bash
pre-commit run --files reports/*.md research_notes/<Report topic>/*.md
```

If the project has no `.pre-commit-config.yaml`, tell the user to run
`agentkit add tech-research` once, which installs the hook. For this run, use the tools directly:

```bash
uvx --from mdformat==1.0.0 --with mdformat-gfm==1.0.0 --with mdformat-frontmatter==2.1.2 mdformat --wrap 100 --number <files>
python3 <this skill's dir>/scripts/check_md_width.py --max 100 <files>
```

A heading the check reports cannot wrap. Shorten it.
