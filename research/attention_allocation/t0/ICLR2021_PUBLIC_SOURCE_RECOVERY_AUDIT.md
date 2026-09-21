# ICLR 2021 Public Source Recovery Audit

**Date:** 2026-09-21  
**Programme:** Attention Allocation Under Cognitive Abundance  
**Track:** A v0.2 source recovery  
**Status:** outcome-blind source audit  
**Verdict:** `NO_NEW_ADMISSIBLE_T0_SOURCE_YET`

## Question

Can a public historical source recover a selection-neutral ICLR 2021 paper state close enough to the frozen submission-time estimand to unlock the v0.2 source-feasibility gate?

The current gate remains:

`V02_SOURCE_FEASIBILITY_INADEQUATE_NEUTRAL_COHORT_REQUIRED`

No citation outcome has been opened.

## Frozen timing facts

ICLR 2021 lists:

- abstract deadline: 28 September 2020, 15:00 UTC;
- full-paper deadline: 2 October 2020, 15:00 UTC;
- review release: 10 November 2020.

Author guidance states that authors were free to upload modifications once reviews were posted during the discussion period.

Sources:

- https://iclr.cc/Conferences/2021/Dates
- https://iclr.cc/Conferences/2021/AuthorGuide
- https://iclr.cc/Conferences/2021/CallForPapers

These dates matter because a snapshot created after 10 November can contain review-induced revisions and is not automatically admissible as submission-time state.

## Positive evidence that a clean pre-review state once existed publicly

On 8 October 2020, ICLR publicly announced that more than 3,000 final submissions had been received and were available on OpenReview.

Source:

- https://iclr-conf.medium.com/3-000-submissions-received-let-the-reviewing-begin-b421d44a6dfe

This is useful provenance evidence. It shows that a broad, anonymous, pre-review public candidate state existed six days after the paper deadline and more than a month before reviews were released.

It does **not** by itself preserve that state. The remaining problem is historical reconstruction.

## Candidate source 1: evanzd/ICLR2021-OpenReviewData

Repository:

- https://github.com/evanzd/ICLR2021-OpenReviewData

The repository contains a 2,000+ paper `paperlist.tsv` with title, keywords and abstract fields, plus later review/rating files.

A contemporaneous Changelog Nightly record lists the repository among projects open-sourced on **11 November 2020**:

- https://nightly.changelog.com/2020/11/11/email-day.html

That publication date is one day after ICLR's stated 10 November review release. The repository also contains a file named `ratings.20201111.tsv`, which is consistent with review data being collected at that point.

### Adjudication

`PROVENANCE_INSUFFICIENT_NOT_ADMITTED`

The evidence does **not** prove that `paperlist.tsv` itself was crawled after review release. It could have been collected earlier and uploaded later.

But the repository, as currently observable, does not establish a pre-review crawl timestamp for the paper list. Because authors could revise after review release, it cannot be admitted as T0 evidence without stronger provenance such as:

- an original crawl timestamp;
- an earlier immutable commit/blob;
- a dated archive or checksum;
- maintainer confirmation tied to preserved artefacts;
- another independently timestamped copy of the same dataset.

The source remains a recovery lead, not an admissible cohort.

An attempt was made to ask the upstream repository maintainer for provenance through the connected GitHub integration, but the integration is not permitted to create issues in that external repository (`403 Resource not accessible by integration`). No external message was sent.

## Candidate source 2: current OpenReview records

Current ICLR 2021 OpenReview pages frequently preserve original note creation dates while showing much later modification dates.

Example:

- https://openreview.net/forum?id=WoLQsYU8aZ

This demonstrates why note creation time is not enough to establish decision-time content. A surviving current record may be useful as an identity witness but cannot be assumed to reproduce the text visible at the historical deadline.

### Adjudication

`CURRENT_STATE_NOT_T0`

No change to the existing temporal firewall.

## Candidate source 3: timestamped arXiv versions

ICLR explicitly allowed submissions to appear on non-peer-reviewed repositories such as arXiv during the review process.

This creates a possible partial recovery route:

1. exact-match ICLR 2021 candidates to arXiv identities;
2. retain only versions whose timestamp is no later than the prospectively chosen historical cutoff;
3. recover title/abstract/PDF from that timestamped version;
4. audit availability by historical ACCEPT/REJECT status;
5. reject the route if source availability is materially decision-linked or topic/geometry coverage is badly distorted.

This route has important limitations:

- arXiv posting is author-selected, so missingness is unlikely to be random;
- many submissions will have no pre-deadline arXiv version;
- public versions can differ from anonymous conference submissions;
- title changes complicate exact linkage;
- selection into arXiv may correlate with field, institution, seniority, visibility or later acceptance.

### Adjudication

`AUDITABLE_PARTIAL_ROUTE_NOT_YET_AUTHORIZED`

It is worth measuring because v0.2 needs only a neutral additional contribution, not necessarily a complete ICLR 2021 reconstruction. But it must pass the same outcome-blind observability discipline before use.

## Candidate source 4: web/archive snapshots of the 8 October public state

The 8 October ICLR announcement establishes that the candidate set was publicly visible before review release. A sufficiently complete immutable web archive from the 2 October to 9 November interval could therefore be valuable.

No complete archive has yet been established in this audit.

A browser-accessible archive of only the conference landing page would not be enough. The source must preserve candidate-level metadata and preferably the referenced PDF/content with stable identifiers and timestamps.

### Adjudication

`RECOVERY_LEAD_UNVERIFIED`

## What this changes

Nothing is unlocked yet.

The verified optimistic candidate arithmetic remains:

- ICLR 2018: 826
- ICLR 2019: 1,419
- ICLR 2020: 1,815
- verified subtotal: 4,060
- optimistic all-2017 upper bound: +442
- optimistic total without a new neutral source: 4,502

The frozen exact-outcome-observable target remains at least 4,600 before technical and identity attrition.

Bulk PDF acquisition remains prohibited.

Citation-outcome acquisition remains prohibited.

## Next autonomous source-recovery actions

Proceed in this order:

1. **Audit the timestamped-arXiv route outcome-blind.** Measure how many ICLR 2021 ACCEPT+REJECT candidates have an exact or conservatively linked arXiv version available at the chosen historical cutoff, and report decision-stratified coverage before acquiring any downstream citation outcome.
2. **Continue immutable-web-archive search** for the public OpenReview candidate state known to exist by 8 October 2020.
3. **Use upstream confirmation only as provenance evidence, not as a substitute for preserved bytes.** If maintainer or OpenReview support replies, require a recoverable immutable artefact or documented historical-revision route.
4. **Do not broaden to another venue yet** unless ICLR 2021 recovery remains inadequate. A venue addition requires the already-planned prospective source-comparability and year/venue-stratification amendment.

## Stop rule

If neither a sufficiently neutral ICLR 2021 partial source nor a complete historical snapshot can contribute enough candidates after prospective identity/technical loss, record another source-level ABSTAIN and only then design an additional-venue amendment.

The programme should not lower the 4,600 precision target to make the available sources fit.
