# T0 Revision-PDF Provenance Audit v0.1

**Date:** 20 September 2026  
**Status:** feasibility evidence; empirical allocation-policy comparison remains gated.

## Question

Can the Track A ICLR cohort recover any allocator-visible candidate content that is demonstrably available no later than the historical submission deadline, rather than relying on later snapshots?

## Sources and provenance

The audit joins the frozen Track A 2020–2021 cohort to the public ResearchArcade `openreview-papers-revisions` relation. The local relation parquet has SHA-256:

`5e1e37616b44fe6435333c2cf5c4a80cee96fa03db64b539fbabda5aed2add58`

ResearchArcade's crawler uses the OpenReview v1 revision history via `get_references(referent=paper_id, original=True)` and records each returned note's `tmdate`. OpenReview documents `tmdate` as the true modification date and states that users cannot set or modify it:

- https://docs.openreview.net/reference/api-v1/entities/note/fields
- ResearchArcade crawler at commit `ecf9c7c2490840b029bd2add4f02d04aca1d014e`:
  https://github.com/ulab-uiuc/research-arcade/blob/ecf9c7c2490840b029bd2add4f02d04aca1d014e/research_arcade/openreview_utils/openreview_crawler.py

The conference deadlines are taken from the official ICLR records:

- ICLR 2020 paper deadline: 25 September 2019, 15:00 UTC.
  https://iclr.cc/Conferences/2020/Dates
- ICLR 2021 paper deadline: 2 October 2020, 15:00 UTC.
  https://iclr.cc/Conferences/2021/Dates

## Conservative admissibility rule

For each ACCEPT/REJECT candidate, select only the latest ResearchArcade revision reference whose recorded true modification time is **at or before the paper submission deadline**.

This creates a historical revision reference that was present by T0. It does **not** assume that a later current snapshot reproduces T0, and it does not infer the original submission from a post-deadline revision chain.

The generated reference set is therefore labelled `T0_OBSERVED_REVISION_REFERENCE`, not `T0_OBSERVED_PDF`. The latter requires successful acquisition, hashing, and extraction of the referenced historical PDF.

## Coverage

| Cohort | Primary ACCEPT/REJECT | T0 revision references | Fraction | ACCEPT coverage | REJECT coverage |
|---|---:|---:|---:|---:|---:|
| ICLR 2020 | 2,213 | 1,816 | 82.1% | 549/687 = 79.9% | 1,267/1,526 = 83.0% |
| ICLR 2021 | 2,594 | 195 | 7.5% | 52/859 = 6.1% | 143/1,735 = 8.2% |

The 2020 window is unusually useful: pre-deadline revision-reference coverage is high and similar across ACCEPT and REJECT strata. The 2021 route is too sparse to support a primary comparison on its own.

This difference is itself a warning against silently generalising across venue-years. The archive mechanism and conference workflow changed.

## Retrieval probe

The public historical-PDF route used by ResearchArcade is:

`https://openreview.net/references/pdf?id=<revision_id>`

A deterministic exploratory probe used the lexicographically first 10 ACCEPT and 10 REJECT reference candidates in each year.

- ICLR 2020: **20/20** returned HTTP 200 with `application/pdf` and PDF magic bytes. Text extraction from the first three pages succeeded for all 20 sampled PDFs.
- ICLR 2021: **20/20** returned HTTP 200 with `application/pdf` and PDF magic bytes.

This is evidence that the identified revision references can resolve to historical content. It is not evidence that all 2,011 references are retrievable.

The normal current-paper route returned HTTP 403 in the same environment, while the historical revision-PDF route returned 200 for the sampled IDs. We do not bypass the blocked current/API routes.

## Adversarial findings

1. **Do not promote 2021 yet.** Seven-and-a-half percent coverage is a strongly selected subset even though both decision strata are represented.
2. **Do not infer T0 from post-deadline history.** ResearchArcade's separate revision-diff and paper-revision tables expose some internal lineage ambiguities. The present candidate set avoids that inference entirely.
3. **2020 is a conditional archival window, not a representative sample of all scientific review.** Its usefulness must not be generalized to later ICLR years.
4. **Reference existence is not content acquisition.** Each PDF still requires successful fetch, integrity hashing, extractability checks, and a failure/missingness report before its content enters an allocation policy.
5. **No outcome fields enter the candidate content.** Decision labels are retained only for coverage diagnostics and downstream evaluation.

## Gate consequence

The temporal-provenance blocker has moved.

Previously, no allocator-visible content had a defensible route back to T0. We now have **1,816 ICLR 2020 and 195 ICLR 2021 pre-deadline revision references** with immutable-time provenance and a successful 40-record retrieval probe.

The empirical gate is **still not passed**. The next gate is acquisition integrity:

1. acquire the ICLR 2020 historical PDFs conservatively and resumably;
2. hash every retrieved PDF and record failures;
3. extract a minimal, pre-specified text representation;
4. quantify retrieval/extraction missingness by historical decision;
5. only then decide whether the 2020 subset can be promoted to a `T0_OBSERVED_PDF` primary feasibility cohort.

A failed or decision-differential acquisition result is an ABSTAIN/redesign outcome, not a reason to loosen the gate.
