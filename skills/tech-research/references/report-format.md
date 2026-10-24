# Report format

The report is `reports/<Headline>.md`. The reader is a technical decision maker who reads the
executive summary and maybe one section. Write so that the summary alone is enough to act on.

## Skeleton

```markdown
# <Headline that states the answer, not the topic>

*Research date: <D Month YYYY>. <Scope: region, versions, currency, what is in and out.>
<Which figures are the author's estimates. Which earlier report this builds on, if any.>*

## Executive summary

- **Answer.** <One or two sentences that answer the question as asked.>
- **Recommendation: <option name>.** <What to do, and the key reason.>
- **<Option or finding 2>.** <Its verdict and the one fact that decides it.>
- **<Option or finding 3>.** ...
- **Open points that decide the recommendation:**
  1. <Fact that, if it turns out differently, changes the answer.>
- **Next steps.** <Concrete validation steps with rough durations.>

## <Section heading that states a finding>

<Body: evidence, numbers with dates and versions, comparison tables, inline citations.>

## Open questions

## Recommendation and next validation steps

## Conclusion

[1]: https://...
[2]: https://...
```

## Rules and the reasons for them

- **Headline states the answer.** "Consolidate on Snowflake, keep Flink" beats "Platform options
  for X". A reader who only sees the file list must still learn the result.
- **Executive summary first, 5–9 bullets, bold lead-in on each.** The lead-in lets a reader scan
  the summary in ten seconds. Put the answer and the recommendation in the first two bullets.
  Put the open points that could reverse the recommendation in the summary, not only at the end:
  they are what the reader must follow up on.
- **Section headings are findings.** "Databricks matches the latency but cannot host Postgres in
  Zurich" instead of "Databricks". The headings together are a second summary.
- **Every number carries its context.** Price with region, unit and currency; version with release
  date; status as GA, public preview or private preview. Mark vendor claims as claims ("vendor
  claim", "claimed 10 GB/s"). Mark your own estimates as estimates and state their baseline.
- **Cite with reference-style links** (`([Snowflake docs][4])` in the text, `[4]: https://...` at
  the end). They keep the prose lines short and the URLs out of the way. Number them in order of
  first use.
- **Tables for comparisons, prose for reasoning.** Keep tables narrow (four or five columns, short
  cells): table rows cannot wrap, so a wide table breaks the 100-character layout. Move long
  explanations out of cells into the text below the table.
- **The conclusion reframes, it does not repeat.** Say what the research shows about the question
  itself (for example, that it conflates two decisions), and what is time-sensitive.
- **Say what you did not find.** "No independent TCO study covers all three" is a finding.

## Tone

Direct and specific. No marketing words, no "In today's fast-paced world". Name the trade-off and
take a position. Where the evidence is thin, say so in one plain sentence instead of hedging every
claim.
