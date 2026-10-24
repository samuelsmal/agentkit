# Research note format

A note is `research_notes/<Report topic>/<sub_question_slug>.md`. One note answers one
sub-question. Notes are the evidence base for the report and the place a reader goes to check a
claim, so they keep more detail and more sources than the report.

## Skeleton

```markdown
# <Sub-question, phrased as a short title>

Research date: <YYYY-MM-DD>. <Versions checked, with release dates.>
Context: <the architecture or situation under review, one or two sentences>.

Legend: **[confirmed]** means a primary source was checked. **[unconfirmed]** means only secondary
sources, or an inference.

## Verdict

**<One-sentence answer.>** <Two or three sentences of reasoning.>

- **<Key fact>.** <Detail.> [confirmed]
- **<Key fact>.** <Detail.> [unconfirmed]

## 1. <Aspect>

| Item | Finding | Source |
| ---- | ------- | ------ |

## Gaps

- <What could not be found or verified, and who could answer it (vendor, customer).>

## Sources

- [<Publisher: title>](<url>), <date>
```

## Rules

- **Primary sources first:** vendor docs, release notes, pricing pages, GitHub issues and
  releases, regulatory filings, region availability pages. Blogs, analysts and press come second.
  Tag each key fact [confirmed] or [unconfirmed].
- **Date everything.** Technology status changes monthly. Give the date of the source and the
  status (GA, public preview, private preview, roadmap, deprecated).
- **Region and edition matter.** A feature that is GA on AWS us-east-1 may be absent in the
  region in scope. Check the region pages when the brief names a region.
- **Record contradictions** between sources, with both sources, instead of silently picking one.
- **Gaps are results.** List what you could not verify so the report can turn it into an open
  question.
