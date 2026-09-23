# ICLR 2021 Immutable Archive Recovery Log

**Date:** 2026-09-23

**Programme:** Attention Allocation Under Cognitive Abundance

**Status:** bounded recovery sweep complete; no full selection-neutral historical-text source recovered

## Purpose

This sweep follows the `ARXIV_ROUTE_CONDITIONAL` result. Its purpose is narrow: find an immutable ICLR 2021 source that preserves paper text during the locked review interval without making availability depend on the later acceptance decision.

The required historical interval is bounded by the ICLR 2021 full-paper deadline, **2020-10-02 15:00 UTC**, and the release of reviews on **2020-11-10**. ICLR stated that submissions could not be changed while under review and could be edited again during the discussion period after reviews were released. A source independently timestamped inside this interval is therefore a strong positive witness for review-period state, subject to any residual post-deadline/pre-capture edit sensitivity.

## 1. Contemporaneous Git snapshot: real, but topic-restricted and metadata-only

A GitHub history search recovered:

- repository: `RchalYang/RLPaperList`
- commit: `0bccd4d0bc895d26c63a32883dc53d543895b9df`
- commit message: `add ICLR 2021 Submissions`
- commit time: `2020-10-05T22:28:09-07:00` (`2020-10-06T05:28:09Z`)
- elapsed time after the frozen full-paper deadline: approximately **86.5 hours**

The committed scraper queries the complete OpenReview invitation `ICLR.cc/2021/Conference/-/Blind_Submission`, but then retains only submissions whose keywords contain `reinforcement learning` or are exactly `rl`.

The snapshot records **338** such submissions and stores title, authors, keywords and abstract. It does **not** preserve the submission PDFs or extracted whole-document text.

Adjudication:

`T0_METADATA_WITNESS_ONLY`

The snapshot is valuable evidence that public submission metadata were queryable and independently frozen during the locked interval. It is not a substitute for the full historical-text source required by the frozen representation protocol, and its topical selection rule means it is not a complete conference cohort.

## 2. Later public Git dumps: too late to certify pre-review state

### `evanzd/ICLR2021-OpenReviewData`

The earliest commit carrying `paperlist.tsv` is:

- commit: `39038e1ae9e73b6cb7bf1116505c199ef452a8cd`
- timestamp: **2020-11-11**, after reviews were released

The dump remains useful as a later witness but cannot certify the locked pre-review state.

### `xcfcode/openreview_spider`

The individual ICLR 2021 forum JSON archive was committed in **April 2021** and contains reviews and decisions as well as the root note. It is a post-outcome archival witness, not a clean T0 source.

## 3. Wayback Machine bounded probe

A ten-paper canonical sample was queried against the CDX index for captures no later than **2020-11-09**.

### Forum URLs

- resolved archive queries: **7 / 10**
- pre-review captures among resolved queries: **0 / 7**
- archive lookup failures/timeouts: **3 / 10**

### Content-hash PDF URLs

Later OpenReview dumps expose content-hash PDF paths such as `/pdf/ec2ff3db1ada0ee31556cfa8ddeb61656db40b80.pdf`. The same ten-paper sample was queried for those immutable-looking paths before review release.

- resolved archive queries: **7 / 10**
- pre-review captures among resolved queries: **0 / 7**
- archive lookup failures/timeouts: **3 / 10**

Adjudication:

`WAYBACK_NOT_PROMISING_AT_SCALE`

This is not proof that Wayback contains zero ICLR 2021 pre-review material. It is a bounded feasibility result: the observed sample gives no positive capture and does not justify thousands of slow CDX queries as the next critical path.

## 4. Common Crawl: unusually well-timed but temporarily non-queryable

`CC-MAIN-2020-45` spans approximately:

- start: `2020-10-19T14:59:01`
- end: `2020-11-01T03:12:51`

That crawl lies wholly inside the locked review interval and is therefore an unusually attractive immutable source if OpenReview forum or PDF URLs were captured.

At the time of this sweep, the historical index endpoint returned **504 Gateway Timeout** even for control queries such as `example.com`. This is treated as an infrastructure/access failure, not evidence of absence.

Adjudication:

`COMMON_CRAWL_RETRY_ONCE_WHEN_QUERYABLE`

## 5. OpenReview legacy revision route

Later archived ICLR 2021 root notes contain an `original` reference identifier distinct from the current forum ID. Direct public API attempts to resolve those legacy identifiers now return `ChallengeRequiredError` from OpenReview.

A targeted support request was sent to OpenReview on **2026-09-20** asking for:

1. the immutable paper revision current at the ICLR 2021 full-paper deadline;
2. a documented legacy API route for resolving historical v1 revision/reference IDs to PDF/content;
3. a complete public pre-review archive if one exists.

As of this audit, only the automated acknowledgement has been received. No human technical response has arrived.

Adjudication:

`OFFICIAL_ROUTE_PENDING`

No attempt is made to circumvent the browser challenge.

## 6. Adjacent-year same-venue check

The public Smerity repositories that provide the programme's strong ICLR 2018 and 2019 near-deadline snapshots are discoverable as:

- `Smerity/search_iclr_2018`
- `Smerity/search_iclr_2019`

No corresponding discoverable `Smerity/search_iclr_2017` or `Smerity/search_iclr_2021` repository was found in the bounded repository search.

A contemporaneous Stephen Merity article dated **2016-11-05** demonstrates that the ICLR 2017 submission list was publicly browsable then, but the article is a curated reading list linking back to OpenReview rather than a frozen full-corpus PDF/text archive. It therefore does not resolve the ICLR 2017 T0 source problem.

## Recovery verdict

The sweep does **not** change the source-feasibility gate.

- full neutral ICLR 2021 historical text recovered: **No**
- bulk content acquisition authorized: **No**
- citation-outcome acquisition authorized: **No**
- downstream outcomes observed: **No**

The strongest new positive witness is the 5 October 2020 RL metadata snapshot. It establishes that a contemporaneous public snapshot existed, but not the full-text, full-cohort substrate required by the current protocol.

## Stop rule and pivot

Archive recovery must not become an unbounded search cost. The ICLR 2021 recovery lane now has two remaining bounded actions:

1. adjudicate the first substantive OpenReview support response to the existing request;
2. retry `CC-MAIN-2020-45` once when the historical index is queryable and test a canonical sample before any scale-up.

If neither yields a complete or sufficiently neutral historical-text route, stop ICLR 2021 archive recovery for this design and draft a **prospectively frozen source-comparability amendment** adding an additional historically reconstructable cohort or venue. The amendment must be frozen before any new bulk paper acquisition or citation-outcome acquisition.

The v0.1 C5 outcome remains sealed.
