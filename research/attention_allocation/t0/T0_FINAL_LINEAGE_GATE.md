# Final T0 Lineage Substrate Gate v0.1

**Frozen:** 20 September 2026  
**Scope:** the final technically usable ICLR 2020 T0 cohort and the actual preregistered policy selections, before citation outcomes are opened.

## Purpose

The initial lineage audit is defined on the full 1,816-candidate historical T0 reference frame.

After technical acquisition/extraction completes, the usable cohort can be smaller. The final policy selections are also made on that reduced outcome-blind substrate. This gate therefore re-intersects the already-frozen lineage flags with the **actual final cohort and policy selections**.

No citation outcome is read.

## Inputs

- final frozen decision-free T0 cohort;
- frozen per-candidate lineage flags from the pre-outcome resubmission audit;
- final frozen policy selections;
- final policy manifest.

Historical decision labels contained in the lineage diagnostic file may be used only for lineage-balance diagnostics. They never enter representation or selection.

## Diagnostics

Report, on the final cohort:

- primary exact-lineage incidence;
- exact + near-title sensitivity-lineage incidence;
- later-ACCEPT lineage incidence;
- historical ACCEPT vs REJECT incidence with 95% Newcombe-Wilson intervals.

For every policy and budget, report the same lineage fractions.

At the primary 20% attention budget, compare each structured policy with seeded random on:

- primary exact lineage;
- exact + sensitivity lineage;
- later-ACCEPT lineage.

## Frozen materiality rule

The existing **±5 percentage-point** diagnostic margin is reused.

Final lineage balance is supported only when:

1. the full ACCEPT-minus-REJECT 95% interval lies inside ±5 pp for both primary exact lineage and exact + sensitivity lineage; and
2. every structured-policy minus seeded-random lineage fraction at the primary 20% budget lies inside ±5 pp for both primary exact lineage and exact + sensitivity lineage.

Otherwise report:

`LINEAGE_BALANCE_NOT_ESTABLISHED`.

A failure narrows interpretation. It does not assign low value to lineage candidates and does not justify post-hoc deletion.

## Later-ACCEPT descendants

Later-ACCEPT lineage is always reported separately because it is direct evidence that manuscript revision and later selection can contribute to downstream visibility.

Later-ACCEPT candidates remain a mandatory sensitivity stratum even when the aggregate lineage-balance gate passes.

## Interpretation

A balanced final lineage substrate means detected manuscript evolution is too sparse and too similarly distributed across the frozen policies to plausibly create a five-point policy contrast by itself under the frozen rule.

It does **not** establish that undetected lineage is absent, or that citations to a descendant are causally attributable to the original 2020 manuscript.

## Outcome boundary

This gate is outcome-free. It must complete before the broader pre-outcome feasibility decision.

Citation acquisition remains prohibited until technical availability, identity observability, lineage, design precision, fixed-window support and construct constraints are jointly adjudicated.
