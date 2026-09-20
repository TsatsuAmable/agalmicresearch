# Track A Allocation Policy Preregistration v0.1

**Date frozen:** 20 September 2026  
**Scope:** ICLR 2020 batch-allocation feasibility cohort after T0 acquisition/extraction and representation gates pass.  
**Status:** pre-outcome protocol. No future-value outcome has been inspected under these policies.

## Purpose

Freeze a small set of transparent allocation rules before downstream epistemic-value outcomes are joined.

The first empirical question is intentionally narrower than the full Agalmic thesis:

> Under a fixed candidate-count attention budget, how do transparent batch-allocation policies change which regions of an outcome-blind T0 representation are selected, and, only after the feasibility gate passes, how do those selections differ in observable future-value recovery?

This is not a model of all scientific funding or laboratory validation. It is a controlled test bed for selection under candidate abundance.

## Common information set

Every policy receives exactly the same frozen T0 representation generated under `T0_CANDIDATE_REPRESENTATION_PROTOCOL.md`.

Allowed policy inputs:

- row identity only for deterministic tie-breaking;
- 128-dimensional outcome-blind SVD vector;
- centroid cosine distance;
- five-nearest-neighbour mean cosine distance;
- pre-specified resource budget.

Forbidden policy inputs:

- conference decision;
- review score, reviewer confidence or review text;
- later publication;
- later citations or citation graph;
- author identity or affiliation;
- any supervised prediction fitted to historical outcomes;
- any post-2020 pretrained embedding;
- downstream epistemic-value labels.

## Primary budget grid

The first analysis uses equal unit cost per candidate.

The selected set size is frozen at:

- 5% of the eligible cohort;
- 10%;
- 20%;
- 40%;
- 80%.

For each fraction, `k = max(1, floor(fraction * N))`.

This equal-count budget is a coarse model of scarce attention. It does **not** claim that all papers take equal real-world effort to evaluate.

No page-count/token-count cost weighting is permitted in the primary analysis. Cost-sensitive variants require a separately justified and frozen validation-cost proxy.

## Policies

### P0 — Seeded random

Uniform sample without replacement using seed `20260920`.

Purpose: null allocation baseline.

### P1 — Centrality

Rank ascending by cosine distance from the cohort centroid.

Purpose: transparent "mainstream/representative" comparator. It deliberately favors dense central regions and is not endorsed as a desirable policy.

### P2 — Centroid novelty

Rank descending by cosine distance from the cohort centroid.

Purpose: extreme-distance comparator.

The score is an operational geometric descriptor, not scientific novelty.

### P3 — Local sparsity

Rank descending by mean cosine distance to the five nearest other candidates.

Purpose: local-tail comparator that is less dependent on a single global centroid.

Again, this is not ground-truth novelty.

### P4 — Greedy k-center coverage

Select a deterministic medoid-like starting point: the candidate nearest the cohort centroid.

Then repeatedly select the unselected candidate whose minimum cosine distance to the already selected set is largest.

Purpose: maximize representation-space coverage under a fixed number of selections.

Tie-break by immutable row identity.

### P5 — Exploration quota

For budget `k`:

- reserve 25% of slots for the highest local-sparsity candidates;
- fill the remaining slots with greedy k-center coverage among candidates not already selected.

For small `k`, exploration slots are `max(1, floor(0.25 * k))` when `k >= 2`; otherwise the single slot follows k-center.

Purpose: a transparent mixture of tail exploration and broad coverage.

The 25% quota is frozen before outcome inspection and must not be tuned to improve later results.

## Determinism

All stochastic behavior is confined to P0 and uses the single seed `20260920`.

Every policy output must include:

- protocol version;
- representation-manifest SHA-256;
- budget fraction;
- `N` and `k`;
- ordered selected row IDs;
- selected-set SHA-256;
- implementation version.

Repeated execution against the same representation must reproduce the same selected sets exactly.

## Engineering-only diagnostics before the outcome gate

Before any future-value outcome is joined, it is permitted to inspect:

- selected-set sizes;
- duplicate violations;
- budget violations;
- deterministic rerun equality;
- pairwise Jaccard overlap between policy selections;
- selected distributions of the same policy-visible geometry descriptors.

It is **not** permitted to inspect historical ACCEPT/REJECT enrichment or future-value enrichment to tune a policy. Conference decision exists only for acquisition/extraction missingness diagnostics and must remain unavailable to the allocator.

## Post-gate evaluation boundary

Only after the feasibility gate passes may an evaluation layer join separately governed future outcomes.

The policy implementation itself must remain unchanged.

Permitted evaluation questions may include observable future-value recovery, precision/recall on a pre-frozen outcome definition, tail recovery, selection diversity, and sensitivity across budget fractions.

Causal claims remain prohibited unless a separately justified identification strategy is added. A rejected paper's observed later trajectory is not automatically the counterfactual trajectory it would have had if selected.

## Interpretation discipline

No policy is called "best", "optimal", or "superior" solely because it wins on one retrospective outcome.

The empirical analysis must report trade-offs and uncertainty across the frozen policies and budgets. Null, contradictory, budget-dependent, or representation-dependent results are valid.

## Stop rule

If the final eligible T0 cohort is materially outcome-differential after acquisition/extraction, if the representation leakage audit fails, or if downstream outcome support violates the frozen feasibility gate, policy-outcome evaluation does not run. The correct result is CONDITIONAL PASS, redesign, or ABSTAIN.
