# Expert-Attention Phase 1C: Boundary Preservation

**Status:** frozen follow-up before fresh hold-out execution  
**Date frozen:** 2026-09-24  
**Motivated by:** Phase 1B marginal-review-value result

## Question

If the purpose of an additional review is specifically to protect papers whose aggregate recommendation could cross the review-scale midpoint, how much review work can a simple near-boundary rule avoid while preserving those cases?

Phase 1B found this objective only after the broader disagreement hypotheses were adjudicated. Phase 1C is therefore a **follow-up validation**, not an independent discovery test.

## Fresh validation splits

Use the same eligible ICLR 2017–2021 review corpus and the same deterministic three-review synthetic hold-out construction as Phase 1B, but use **new split seeds**:

**20261001 through 20261020 inclusive**

None of these seeds were used in Phase 1B.

The experiment still makes no chronological review-order claim and uses no conference decision or citation outcome.

## Policies

Evaluate:
1. random;
2. disagreement;
3. boundary uncertainty;
4. hybrid.

Rank independently within year.

Boundary uncertainty remains:

`max(0, 1 - 2 * abs(mean2 - 0.5))`

No learned model is permitted in Phase 1C.

## Target event

A **midpoint crossing** occurs when adding the held-out third rating moves the three-review mean to the opposite side of normalized 0.5 from the two-review mean.

This is a recommendation-instability proxy, not conference acceptance.

## Budget curve

Evaluate review budgets from **5% to 100% in 5-point increments**.

For each policy and split, find the minimum budget achieving at least **95% midpoint-crossing recall**.

Define:

`RWS@95 = 1 - minimum_budget_for_95%_crossing_recall`

If no tested budget reaches 95%, RWS@95 = 0.

## Primary hypothesis

A simple boundary-uncertainty rule can preserve recommendation-instability cases while saving substantial extra-review work.

Support requires all of:

- median boundary-policy RWS@95 across 20 fresh splits >= **40%**;
- at least 18/20 splits have boundary-policy RWS@95 >= **30%**;
- median boundary-policy RWS@95 exceeds random by >= **30 percentage points**.

Failure of any condition means the hypothesis is not supported.

## Secondary reporting

Report:
- RWS@95 for all four policies;
- the distribution across fresh split seeds;
- primary-seed-style full recall curve averaged across the 20 fresh splits;
- year-specific crossing counts and recall at the median required boundary-policy budget as a descriptive diagnostic.

## Stop rule

If the fixed boundary rule satisfies the target, do not build a learned allocator merely to improve a benchmark number.

The next question would become operational validity: whether the same simple rule remains useful in a prospective review process where ratings arrive sequentially.

If it fails, do not rescue it by changing the target after seeing results.
