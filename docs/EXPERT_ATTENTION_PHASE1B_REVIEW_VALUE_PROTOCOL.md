# Expert-Attention Phase 1B: Marginal Review Value Benchmark

**Status:** frozen descriptive benchmark before policy outcomes  
**Date frozen:** 2026-09-24  
**Extends:** `EXPERT_ATTENTION_PHASE1_RESEARCH_NOTE.md` and `EXPERT_ATTENTION_TRIAGE_VALIDITY_BENCHMARK.md`

## Question

When a paper already has two expert ratings, can a simple allocation rule identify the papers for which an additional independent rating would change the aggregate assessment most?

This is a narrower and more directly observable expert-attention question than Track A's later-citation design. It tests the premise that disagreement or uncertainty can identify where another unit of expert attention has high information value.

## Why this is a separate benchmark

The source database stores final review records whose ratings may have been edited after their initial creation. It is therefore not valid to reconstruct a literal historical sequence such as “review 1, then review 2, then review 3.”

Instead, this benchmark is explicitly synthetic:

1. take papers with at least three scored reviews;
2. deterministically choose three review records using a seed that does not depend on scores;
3. expose two ratings to the allocator;
4. hide the third rating as an evaluation target;
5. ask which papers should receive the simulated extra review.

No claim is made that the hidden review was chronologically third.

## Data

Use the same frozen public ICLR conference database already used by the Attention Allocation audits.

Eligible years: **2017–2021**.

Eligibility:
- conference = ICLR;
- at least three reviews with a parseable `rating_int`;
- no accept/reject decision is required or supplied to the allocation policy.

The source database SHA-256 is recorded at execution.

## Review-score normalization

Allocation is stratified by year.

Normalize scores to [0,1] using frozen ordinal scales:

- 2017: 1–10 mapped linearly;
- 2018: 1–10 mapped linearly;
- 2019: 1–10 mapped linearly;
- 2020: ordered categories 1, 3, 6, 8 mapped to 0, 1/3, 2/3, 1;
- 2021: 1–10 mapped linearly.

Any rating outside the frozen year-specific scale is an error.

## Deterministic hold-out

Primary split seed: **20260924**.

For each paper, order its scored review IDs by SHA-256 of:

`split_seed | paper_id | review_id`

Use:
- first two = observed ratings;
- third = hidden rating;
- additional reviews, if any, are unused in that split.

Sensitivity splits use seeds **20260924 through 20260943 inclusive**.

## Observable state

For each episode:

- `mean2`: mean of the two observed normalized ratings;
- `disagreement`: absolute difference between the two observed normalized ratings;
- `boundary_uncertainty`: `max(0, 1 - 2 * abs(mean2 - 0.5))`.

No paper text, review text, decision, meta-review, citation, author identity, affiliation or topic is used.

## Allocation policies

At each budget, rank independently within each year.

Budgets: **5%, 10%, 20%, 40%**.

Policies:

1. **random**: deterministic hash ranking independent of scores;
2. **disagreement**: highest observed pairwise disagreement first;
3. **boundary_uncertainty**: observed mean closest to the normalized midpoint first;
4. **hybrid**: equal-weight mean of disagreement and boundary uncertainty.

Ties use paper ID as a deterministic secondary key.

## Hidden-review information value

After allocation is frozen, reveal the held-out normalized rating `r3`.

Define:

`mean3 = (r1 + r2 + r3) / 3`

`absolute_update = abs(mean3 - mean2)`

This is the amount by which the extra review changes the three-review mean relative to the two-review estimate.

The benchmark does **not** interpret this as scientific value or truth. It is a direct measure of marginal reviewer information under the chosen aggregation rule.

## Primary metric

### Update-Mass Capture

At budget b:

`UMC_b = sum(absolute_update for selected papers) / sum(absolute_update for all eligible papers)`

Random allocation should capture approximately its budget fraction.

The primary operating point is **20%**.

## Secondary metrics

### Large-Update Recall

Within each year, label the top decile of `absolute_update` as large updates. Report the fraction selected at each budget.

### Midpoint-Crossing Recall

A midpoint crossing occurs when adding the hidden review moves the aggregate from one side of 0.5 to the other. Report the fraction selected.

This is a sensitivity measure only. It is not equated with conference acceptance.

## Preregistered hypotheses

### H1: disagreement predicts marginal review value

At a 20% budget, disagreement allocation captures more hidden-review update mass than random.

**Material support:** the primary split advantage is at least **5 percentage points**, the median advantage over all 20 sensitivity splits is at least **5 percentage points**, and at least 18 of 20 splits have positive advantage.

**Evidence against H1:** any of those conditions fails.

### H2: disagreement preserves large updates

At a 20% budget, disagreement allocation has Large-Update Recall at least 5 percentage points above random on the primary split.

### H3: a more elaborate score is not automatically better

The hybrid policy is exploratory. It earns no preference merely by combining signals. If it does not materially exceed disagreement alone, prefer the simpler disagreement rule.

## Leakage controls

The allocator may not use:
- final conference decision;
- review text;
- reviewer identity;
- review modification time;
- hidden rating;
- other hidden reviews;
- citations or later publication outcomes.

The experiment uses final stored ratings only as exchangeable review observations. It makes no historical sequencing claim.

## Interpretation boundaries

A positive result would support a narrow claim:

> disagreement between two observed reviewers is useful for identifying papers where another reviewer is likely to move the aggregate assessment.

It would **not** establish:
- which papers are scientifically better;
- that a third review causally improves decisions;
- that review disagreement is always desirable;
- that the same routing rule works before any reviews exist.

A negative result is equally useful because it would falsify a central intuition behind disagreement-preserving expert-attention allocation.

## Next step after execution

If H1 is supported, treat this benchmark as evidence for **mid-review escalation**, distinct from pre-review triage.

If H1 is not supported, narrow or retire the claim that disagreement is a useful proxy for marginal expert-attention value.

Either way, do not reopen Track A's sealed citation outcomes.
