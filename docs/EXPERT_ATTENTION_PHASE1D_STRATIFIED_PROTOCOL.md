# Expert-Attention Phase 1D: Stratified Boundary Preservation

**Status:** frozen before execution  
**Date frozen:** 2026-09-24  
**Motivated by:** Phase 1C pooled boundary-preservation result

## Question

Does the fixed near-boundary rule still save substantial simulated third-review work when preservation is required separately within each conference-year rating regime rather than only in the pooled sample?

Phase 1C passed its pooled preregistered criterion but a post-hoc diagnostic showed 2020 and 2021 below 95% recall at the pooled median budget. Phase 1D tests that limitation directly. It is a safety/robustness follow-up, not a new discovery claim.

## Frozen data and splits

Use the same eligible ICLR 2017–2021 review corpus and deterministic synthetic three-review hold-out construction as Phase 1C.

Use fresh split seeds **20261101 through 20261120 inclusive**. None were used in Phase 1B or 1C.

No conference decision labels or citation outcomes may be used. This remains non-chronological and retrospective.

## Frozen policy

Evaluate only the fixed boundary-uncertainty rule plus random as a sanity baseline. No learned model, hybrid tuning, threshold fitting, or year-specific policy parameter is permitted.

Boundary uncertainty is unchanged:

`max(0, 1 - 2 * abs(mean2 - 0.5))`

Rank independently within year.

## Stratified target

For each seed and each year, calculate midpoint-crossing recall at budgets from **5% to 100% in 5-point increments**.

For each seed, define the required budget as the smallest common budget at which **every year with at least 20 midpoint-crossing events reaches >=95% recall**. Years below 20 crossing events are reported but excluded from the all-strata gate because their recall is too discrete for this threshold.

Define stratified `RWS@95 = 1 - required_budget`.

## Primary hypothesis

The fixed boundary rule survives the stricter stratified safety constraint only if all hold:

- median stratified RWS@95 across 20 fresh splits >= **30%**;
- at least 18/20 splits have stratified RWS@95 >= **20%**;
- every eligible year reaches >=95% recall at the selected common budget in every counted split by construction;
- median stratified boundary RWS@95 exceeds the random baseline by >= **20 percentage points**.

Failure of any condition means the stratified hypothesis is **not supported**. Do not rescue it by changing strata, thresholds, seeds, or policy after execution.

## Secondary reporting

Report crossing-event counts and recall by year, the distribution of required budgets, random baseline, and the difference from Phase 1C pooled RWS@95.

## Stop rule

If supported, the next admissible question is chronological validity using genuinely sequentially observed review state. Do not build a learned allocator.

If not supported, narrow the result to pooled retrospective preservation and stop operational escalation of this policy unless a separately motivated design addresses the failed regime without post-hoc tuning.
