# T0 Identity-Observability Gate v0.1

**Frozen:** 20 September 2026  
**Scope:** final technically usable ICLR 2020 T0 cohort after representation and policy selection, before citation outcomes are opened.

## Purpose

OpenAlex identity support is not itself a scientific outcome, but later citation outcomes are observable only for candidates with a defensible identity cluster.

This gate asks whether that observability layer is sufficiently neutral for the preregistered policy comparisons to be interpreted without silently rewarding or penalizing a policy because its selected candidates are easier to identify bibliographically.

## Inputs

Only outcome-free artefacts are allowed:

- frozen decision-free T0 cohort;
- historical ACCEPT/REJECT label for missingness diagnostics only;
- frozen exact OpenAlex identity clusters;
- final outcome-blind representation;
- final preregistered policy selections.

No citation counts or citing-work sets are read.

## Historical-decision diagnostic

Compute exact-identity match fraction separately for historical ACCEPT and REJECT.

Use a 95% Newcombe-Wilson interval for:

`match_fraction_ACCEPT - match_fraction_REJECT`.

Identity-observability balance is supported on this axis only when the full interval lies inside **±5 percentage points**.

Failure does not convert unmatched candidates into negative outcomes. It means later claims must remain explicitly conditional on the observable matched cohort.

## Policy-specific observability diagnostic

At each frozen attention budget, report the exact-identity match fraction of every policy's selected set.

At the primary 20% budget, compare each structured policy with seeded random on the matched substrate.

For a matched cohort of size `N`, a fixed top-decile design count `H`, and fixed selected sets, define candidate weights:

- +1 for policy-only selected candidates;
- -1 for random-only selected candidates;
- 0 otherwise.

The expected recall difference under uniformly distributed high-recognition labels is:

`(|policy ∩ matched| - |random ∩ matched|) / N`.

This is a pure observability effect. Its absolute value must be reported before any real citation outcome is opened.

A magnitude above **5 percentage points** is a material observability warning because it equals the preregistered smallest downstream effect of interest.

## Prospective matched-substrate precision

Using the same fixed weights, compute the finite-population variance of the recall difference under a fixed-H random high-recognition set.

Report the normal-approximation 95% half-width and compare it with the frozen 5-point smallest effect of interest.

This is a design diagnostic, not a realized power calculation.

## Geometry diagnostics

When the final representation is available, report exact-identity support by quintile of:

- centroid cosine distance;
- local five-nearest-neighbour sparsity.

These do not create new exclusion thresholds. They diagnose whether the outcome-observation mechanism varies over the same geometry consumed by allocation policies.

## Gate status

`OBSERVABILITY_NEUTRALITY_SUPPORTED_WITHIN_5PP` requires:

- the full historical ACCEPT-minus-REJECT match interval inside ±5 pp; and
- every primary structured-policy expected null recall shift from identity availability inside ±5 pp.

Otherwise report:

`OBSERVABILITY_NEUTRALITY_NOT_ESTABLISHED`.

This status does not automatically authorize or prohibit downstream outcome acquisition. It feeds the broader pre-outcome feasibility decision together with technical availability, lineage, fixed-window support, construct validity, and precision.

## Interpretation boundary

Identity observability is part of the measurement process. It is not epistemic value.

An unmatched paper must never be treated as a zero-citation paper merely because the evaluation system cannot resolve it.
