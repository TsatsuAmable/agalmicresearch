# Expert-Attention Phase 1B Findings: Marginal Review Value

**Date:** 24 September 2026  
**Protocol:** `EXPERT_ATTENTION_PHASE1B_REVIEW_VALUE_PROTOCOL.md`  
**Executable:** `research/expert_attention/review_value_holdout.py`  
**Input database SHA-256:** `ceeaa4316f76f6a22a5856128f34e8c3f35693d145db756f9688eda42ee20ed2`  
**Eligible papers:** 7,531  
**Decision labels used:** No  
**Citation outcomes used:** No

## Result

The preregistered strong claim that reviewer disagreement materially identifies where another review has high marginal information value is **not supported** at the frozen threshold.

At the primary 20% review budget:

| Policy | Update-mass capture | Large-update recall | Midpoint-crossing recall |
|---|---:|---:|---:|
| Random | 19.5% | 19.6% | 19.3% |
| Disagreement | 22.4% | 22.9% | 24.1% |
| Boundary uncertainty | 20.2% | 19.8% | 65.3% |
| Hybrid | 21.5% | 20.3% | 48.9% |

Disagreement beat random on Update-Mass Capture in all 20 deterministic hold-out sensitivity splits, but the advantage was small: **+2.9 percentage points** on the primary split and **+2.3 points median** across sensitivity splits, below the frozen five-point materiality threshold. Its Large-Update Recall advantage was **+3.2 points**, also below threshold.

Therefore H1 and H2 are both **not supported** under the preregistered decision rules.

## What changed

The result narrows the preservation argument.

Reviewer disagreement is not a sufficiently strong general-purpose proxy for the marginal value of another review under this benchmark. It has a consistent positive association, but not one large enough to justify a disagreement-first allocator on the frozen criteria.

By contrast, the intentionally simple boundary-uncertainty rule has a very different profile. With 20% of review slots it captures **65.3%** of cases where the hidden review moves the aggregate across the normalized recommendation midpoint, while capturing essentially random levels of total update mass.

This means “valuable extra attention” is not one scalar target. A policy that is efficient for decision-instability cases is not necessarily efficient for aggregate opinion change, and vice versa.

## Primary hypothesis adjudication

### H1: disagreement predicts marginal review value — NOT SUPPORTED

Frozen material-support rule:
- primary Update-Mass Capture advantage >= 5 pp;
- median advantage across 20 sensitivity splits >= 5 pp;
- at least 18/20 sensitivity splits positive.

Observed:
- primary advantage: **+2.9 pp**;
- median sensitivity advantage: **+2.3 pp**;
- positive splits: **20/20**.

The directional signal is stable but materially smaller than preregistered.

### H2: disagreement preserves large updates — NOT SUPPORTED

Frozen rule: Large-Update Recall advantage >= 5 pp at 20% budget.

Observed: **+3.2 pp**.

### H3: hybrid complexity earns no automatic preference — retained

The hybrid does not dominate the simpler policies. At 20% it captures less update mass than disagreement and fewer midpoint crossings than boundary uncertainty. There is no evidence here for preferring the more elaborate combination.

## Post-hoc robustness diagnostic

The following analysis was performed only after the primary result was visible and is **not preregistered evidence**.

At the 20% budget, boundary-uncertainty midpoint-crossing recall by year was:
- 2017: 77.3%
- 2018: 58.0%
- 2019: 66.9%
- 2020: 70.4%
- 2021: 60.4%

The effect is therefore not confined to the unusual 2020 four-level rating scale.

Disagreement Update-Mass Capture remained only modestly above random within each year.

## Interpretation boundary

This benchmark uses final stored reviewer ratings as exchangeable observations in a deterministic synthetic hold-out. It does not reconstruct chronological review order and does not show that an extra review causally improves a conference decision.

It supports a narrower operational distinction:

- if the objective is **broad opinion-update mass**, disagreement provides only a small routing advantage;
- if the objective is **protecting cases near a recommendation boundary from a consequential extra-review shift**, proximity to the boundary is a much stronger simple routing signal.

Neither outcome is a measure of scientific worth.

## Decision

Do **not** proceed with a bespoke disagreement-first allocation mechanism on the strength of Phase 1B.

The next experiment should remain simple and objective-specific: quantify how much review work a boundary-targeting rule can save while preserving a preregistered fraction of recommendation-boundary crossings. If a fixed rule is already sufficient, prefer it to learned or Agalmic-specific routing machinery.
