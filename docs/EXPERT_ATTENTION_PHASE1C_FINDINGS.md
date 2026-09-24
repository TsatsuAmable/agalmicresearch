# Expert-Attention Phase 1C Findings: Boundary Preservation

**Date:** 24 September 2026  
**Protocol:** `EXPERT_ATTENTION_PHASE1C_BOUNDARY_PROTOCOL.md`  
**Fresh hold-out seeds:** 20261001–20261020  
**Decision labels used:** No  
**Citation outcomes used:** No

## Result

The preregistered Phase 1C hypothesis is **supported**.

Using a simple rule that prioritizes papers whose two observed normalized reviewer ratings average closest to the recommendation midpoint, the benchmark reaches at least 95% pooled midpoint-crossing recall while saving a median **45%** of simulated third-review work across 20 fresh hold-out splits.

| Policy | Median RWS@95 | Range across fresh splits | Splits saving >=30% |
|---|---:|---:|---:|
| Random | 0% | 0–5% | 0/20 |
| Disagreement | 10% | 5–10% | 0/20 |
| Boundary uncertainty | **45%** | **45–50%** | **20/20** |
| Hybrid | 35% | 35–40% | 20/20 |

Boundary uncertainty exceeds random by a median **45 percentage points** of Review Work Saved at 95% crossing preservation.

## What this means

Phase 1B showed that reviewer disagreement is only a weak general predictor of how much another review changes the aggregate rating. Phase 1C asks a narrower question: if the operational risk is that another review could move the aggregate recommendation across its midpoint, where should scarce additional review effort go?

For that objective, a fixed near-boundary rule is much more effective than disagreement and also outperforms the more complicated hybrid.

This is evidence **against adding algorithmic complexity** at this stage. A learned allocator has not earned a role.

## Fresh-split protection

The exact Phase 1C hold-out partitions were not used in Phase 1B. The primary criterion required:

- median boundary-policy RWS@95 >= 40%;
- at least 18/20 fresh splits with RWS@95 >= 30%;
- median boundary-minus-random RWS@95 >= 30 percentage points.

Observed:

- median RWS@95: **45%**;
- splits saving >=30%: **20/20**;
- boundary-minus-random: **+45 pp**.

All three conditions pass.

## Important limitation: pooled versus stratum-specific preservation

The preregistered 95% target is pooled across years, with allocation ranked separately within each year.

A post-hoc diagnostic on the first fresh split shows that the median 55% budget reaches:

- 2017: 100.0% crossing recall;
- 2018: 97.4%;
- 2019: 99.4%;
- 2020: 93.2%;
- 2021: 94.6%.

At 65% budget the same split reaches at least 97.7% in every year.

These per-year checks were performed after the primary result and are **not preregistered evidence**. They identify the correct safety condition for any operational follow-up: aggregate preservation is not enough; each rating-scale/year stratum needs its own floor.

## Interpretation boundary

This remains a synthetic hold-out over final stored review ratings. It does not reconstruct chronological review arrival and does not show that reducing real conference reviewer assignments would preserve decision quality.

The result supports a narrower operational proposition:

> When two review ratings already exist, proximity of their mean to the recommendation midpoint is a strong simple signal for preserving cases where one additional rating could change the recommendation side.

It does not measure scientific merit.

## Decision

Do not build a learned or Agalmic-specific mid-review allocator now.

The simplest rule has earned the next test. Any prospective or closer-to-operational study should:

1. use sequentially observed ratings rather than synthetic exchangeable hold-outs;
2. enforce preservation floors separately by rating regime or year;
3. audit whether saved reviewer effort causes unacceptable losses in review quality, topic coverage or difficult cases;
4. compare the fixed boundary rule against random and ordinary editorial heuristics.

Until such evidence exists, treat the 45% pooled work-saving estimate as a retrospective benchmark result, not a deployment promise.
