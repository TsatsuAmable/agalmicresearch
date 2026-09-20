# Track A Downstream Outcome and Precision Preregistration v0.1

**Date frozen:** 20 September 2026  
**Scope:** ICLR 2020 Track A feasibility cohort, only after T0 acquisition/extraction, missingness review, cohort freeze, representation regeneration and outcome-blind policy selection are complete.  
**Status:** pre-outcome protocol. No policy has been evaluated against downstream outcomes.

## Purpose

Freeze the downstream-value proxy, matching rules, follow-up window, uncertainty procedure and practical-effect threshold before any allocation policy is scored.

This protocol does **not** treat citations as epistemic truth. It tests recovery of one observable downstream-recognition proxy under a fixed attention budget.

## Causal boundary

Historical conference selection can affect visibility, publication, citation opportunity and later development. Therefore:

- citation outcomes are selection-affected observables, not intrinsic counterfactual value;
- policy comparisons are descriptive recovery analyses unless a separate identification strategy is added;
- no result may be phrased as "this policy would have caused more valuable science to exist".

The primary estimand is:

> Among the prospectively frozen, outcome-observable Track A cohort, how much of a fixed five-year downstream citation signal is recovered by each preregistered selection policy under equal candidate-count budgets?

## Outcome source

Primary source: OpenAlex Works and citation graph.

All outcome acquisition must freeze:

- retrieval timestamp;
- OpenAlex work ID;
- raw response or exact selected fields;
- query/match provenance;
- OpenAlex `updated_date` where present;
- acquisition-script version and hashes.

OpenAlex is an evaluation-only source. Nothing acquired from OpenAlex may flow back into candidate representation or policy selection.

## Entity matching

### Primary identity cluster

A candidate enters the primary downstream analysis only when at least one OpenAlex work satisfies one of:

1. exact persistent identifier match, where a DOI or OpenAlex ID is independently available; or
2. exact-normalized-title match within publication years 2019–2022 **plus** at least one exact author-surname overlap between the evaluation metadata and the OpenAlex authorship list.

All OpenAlex work records satisfying the exact-title+author rule are retained as a single **identity cluster** for that candidate. This is necessary because preprint, conference, repository or archival manifestations can appear as separate OpenAlex work IDs even when title and authorship identify the same candidate. The downstream citation set is the union of citing OpenAlex work IDs across every member of the identity cluster, deduplicated before counting.

If a persistent-ID seed is available, exact-title+author expansion is still permitted so citation links split across manifestations are not silently lost.

Title normalization is frozen as:

- Unicode NFKC;
- lowercase;
- collapse all non-alphanumeric runs to a single space;
- collapse whitespace;
- trim.

Multiple exact-title+author records do **not** create ambiguity; they form the identity cluster. A candidate is quarantined only when results imply competing distinct works that cannot be resolved under the frozen exact rule.

### Sensitivity match set

A separately reported sensitivity analysis may admit fuzzy title matches only if all of the following hold:

- normalized token-set similarity >= 0.97;
- at least 50% overlap between available candidate author surnames and OpenAlex author surnames, with at least one surname matched;
- publication year in 2019–2022;
- the highest-scoring candidate exceeds the second-highest by >= 0.03.

Sensitivity matches never replace the exact-match primary analysis.

Thresholds are frozen here and may not be retuned after observing citations.

## Fixed follow-up window

The ICLR 2020 paper deadline is treated as the simulated decision boundary.

To avoid ambiguity within the deadline day, citing works count only when their OpenAlex publication date falls in:

**2019-09-26 through 2024-09-25 inclusive.**

This creates a conservative five-year post-decision window shared by all retained candidates.

Citing works with missing publication date are excluded from the primary count and reported separately.

## Primary downstream outcome

For each matched candidate identity cluster:

**C5 = number of distinct OpenAlex works that cite any member of the identity cluster and have publication_date within the fixed five-year window.**

Citing work IDs are unioned across all cluster members and deduplicated before counting. This prevents preprint/conference record duplication from mechanically inflating or deflating the outcome.

The raw citing-work IDs used to construct C5 must be frozen so the count can be reconstructed.

## Derived value set

Define the "high-recognition" set as candidates at or above the empirical 90th percentile of C5 **within the frozen primary matched cohort**.

Ties at the threshold are included.

This percentile rule is frozen before C5 is acquired. No citation-count threshold may be substituted later because it produces a more convenient result.

"High-recognition" is shorthand for this operational citation proxy, not a claim of high epistemic value.

## Primary policy metric

At the preregistered **20% attention budget**:

**High-recognition recall = selected high-recognition candidates / all high-recognition candidates.**

Primary comparisons are the five structured policies versus seeded random:

- centrality vs random;
- centroid-distance vs random;
- local-sparsity vs random;
- k-center coverage vs random;
- exploration-quota vs random.

The 5%, 10%, 40% and 80% budget results form a descriptive attention-efficiency frontier and are secondary.

## Secondary metrics

Report, without collapsing them into one score:

- fraction of total C5 citation mass recovered;
- mean and median C5 among selected candidates;
- count of high-recognition candidates not selected;
- citation-year breadth: number of distinct years within the five-year window containing at least one citing work;
- policy-selection diversity and overlap already defined in the outcome-blind diagnostics.

No composite "epistemic value score" is permitted in this first analysis.

## Smallest effect of interest

For the primary 20% budget, the smallest effect of interest is frozen as:

**5 percentage points absolute difference in high-recognition recall relative to seeded random.**

This is a practical-resolution target, not a theoretical constant.

## Uncertainty procedure

Use a paired candidate-level bootstrap:

- 10,000 replicates;
- seed: 20260920;
- resample frozen cohort rows with replacement;
- recompute the high-recognition threshold inside each replicate from resampled C5 values;
- evaluate every frozen policy selection against the same bootstrap replicate;
- report bootstrap median delta and 95% percentile interval versus seeded random.

The policy selections themselves are not refit inside a replicate.

For the five primary structured-policy comparisons at the 20% budget, also report Holm-adjusted two-sided randomization p-values as a secondary inferential summary. Interpretation should emphasize effect size and interval rather than thresholded significance.

## Precision stop rule

If the 95% bootstrap interval for a primary recall-delta contrast has half-width greater than 5 percentage points, label that contrast **precision-inadequate** and do not distinguish effects smaller than the frozen smallest effect of interest.

If overall outcome matching or citation observability fails the existing feasibility gate, do not run policy-outcome comparisons at all.

## Missingness and support gate

Before outcome scoring, report primary-match probability by:

- historical ACCEPT/REJECT decision;
- T0 representation geometry quantiles;
- document length quantiles.

Historical decision is used only as a diagnostic here, not as a policy feature.

If outcome matching is strongly decision-differential after available T0 covariates, restrict claims to the exact observable matched cohort and explicitly state the selection problem. Do not impute citations for unmatched candidates in the primary analysis.

## Prohibited analyses before primary results are frozen

Do not:

- tune matching thresholds to increase sample size or policy separation;
- tune policy rules using C5;
- replace the five-year window with a horizon that strengthens a result;
- choose a different high-recognition percentile after inspecting outcomes;
- use total current `cited_by_count` as the primary outcome;
- introduce FWCI, citation-normalized percentile, journal prestige or author prestige into the primary metric;
- build supervised outcome prediction models before the preregistered transparent-policy analysis is complete.

## Sensitivity analyses permitted after the primary result is frozen

- fuzzy-match sensitivity cohort;
- alternative high-recognition cutoffs at 80th and 95th percentiles;
- raw C5 instead of top-decile recall;
- OpenAlex subfield-stratified summaries;
- exclusion of self-citations if a defensible author-identity method is implemented;
- 3-year and 4-year fixed citation windows.

These are sensitivity analyses only and must not replace the primary result.

## Interpretation

A policy that recovers more C5 or high-recognition candidates has recovered more of this particular retrospective recognition signal under this cohort and representation.

It has **not** thereby been shown to select intrinsically better science, produce more science, improve peer review, or maximize social value.

Null, conflicting, budget-dependent, representation-dependent and precision-inadequate results are all valid outcomes.
