# Track A v0.1 Pre-Outcome Feasibility Result

**Date:** 20 September 2026  
**Verdict:** **ABSTAIN_PRE_OUTCOME**  
**Citation outcomes opened:** **No**

## Executive result

Track A v0.1 reached its frozen pre-outcome decision point without inspecting the preregistered citation outcome.

The historical ICLR 2020 substrate is technically excellent and lineage contamination is small. Exact OpenAlex outcome observability is substantial but historically selection-linked. The decisive failure is prospective precision:

> **0 of 5 preregistered primary policy contrasts can distinguish the frozen five-percentage-point smallest effect of interest under the frozen design.**

The broader gate therefore returns `ABSTAIN_PRE_OUTCOME`.

The post-gate runner then independently confirmed the firewall:

- `citation_outcome_acquisition_authorized=false`;
- `network_activity_started=false`;
- no citation-acquisition directory was created.

This is a valid negative feasibility result. It does **not** show that the allocation policies have no effect. It shows that Track A v0.1, with this cohort and this top-decile recall endpoint, cannot resolve the effect size it promised to resolve without looking at the answer first.

## 1. Historical T0 content availability

Initial candidate frame:

**1,816 ICLR 2020 T0 revision-reference candidates**

Terminal acquisition:

- successful historical PDFs: **1,815 / 1,816 = 99.945%**
- extraction success among acquired PDFs: **1,815 / 1,815 = 100%**
- primary-usable records: **1,815 / 1,816 = 99.945%**
- page-level extraction-error records: **0**
- low-text records below the frozen 1,000-character floor: **0**

The one failed acquisition is historical REJECT candidate `S1efAp4YvB`. Its frozen reference PDF exceeded the prospectively enforced 100 MiB safety ceiling:

`105,906,176 > 104,857,600 bytes`.

The failure was retained rather than repaired after historical decision was known.

Decision-stratified primary usability:

| Historical decision | Usable | Total | Fraction |
|---|---:|---:|---:|
| ACCEPT | 549 | 549 | **100.00%** |
| REJECT | 1,266 | 1,267 | **99.92%** |

ACCEPT-minus-REJECT usable fraction:

**+0.079 percentage points**

95% Newcombe-Wilson interval:

**[-0.619 pp, +0.446 pp]**

Technical verdict:

**PASS_TECHNICAL_AVAILABILITY**

## 2. Frozen outcome-blind policy substrate

The final usable cohort contains:

**N = 1,815 candidates**

The finalizer regenerated, without downstream outcomes:

- the frozen historical text representation;
- the preregistered 20% policy selections;
- the seeded-random baseline;
- the prospective design-precision audit.

The finalizer status is:

`OUTCOME_BLIND_T0_STAGE_COMPLETE`

with `outcomes_touched=false`.

## 3. Exact OpenAlex identity observability

On the final cohort:

- primary exact identity matches: **1,692 / 1,815 = 93.22%**
- historical ACCEPT: **528 / 549 = 96.17%**
- historical REJECT: **1,164 / 1,266 = 91.94%**

ACCEPT-minus-REJECT identity-match difference:

**+4.23 percentage points**

95% Newcombe-Wilson interval:

**[+1.84 pp, +6.32 pp]**

Therefore historical-decision observability neutrality inside ±5 pp is **not established**.

However, on the actual frozen 20% policy selections, the expected policy-vs-random recall shifts attributable solely to unequal identity availability are small:

| Policy | Expected observability-only recall shift |
|---|---:|
| centrality | -0.47 pp |
| centroid novelty | -0.30 pp |
| exploration quota | -0.41 pp |
| k-center coverage | -0.41 pp |
| local sparsity | -0.65 pp |

All are comfortably inside the frozen ±5 pp materiality bound.

The admissible interpretation would therefore have been conditional on the exact matched cohort, not the full candidate frame.

## 4. Manuscript lineage

On the final 1,815-candidate cohort:

- exact later-ICLR lineage candidates: **10 = 0.55%**
- exact + frozen near-title sensitivity lineage: **19 = 1.05%**
- later-ACCEPT descendants under sensitivity: **3 = 0.17%**

The final lineage substrate passes the ±5 pp balance rule both by historical decision and across the actual policy selections:

**LINEAGE_BALANCE_SUPPORTED_WITHIN_5PP**

Detected later-ACCEPT descendants would nevertheless have remained a mandatory sensitivity stratum.

## 5. Prospective precision

The frozen primary endpoint is high-recognition recall at the 20% attention budget.

Design constants:

- final cohort: **N = 1,815**
- design top decile: **H = 182**
- selected per policy: **k = 363**
- smallest effect of interest: **5 percentage points**

Prospective 95% half-widths versus seeded random:

| Policy | Symmetric difference vs random | 95% half-width | Adequate for 5 pp? |
|---|---:|---:|---:|
| centrality | 580 | **7.79 pp** | No |
| centroid novelty | 594 | **7.89 pp** | No |
| exploration quota | 600 | **7.93 pp** | No |
| k-center coverage | 598 | **7.91 pp** | No |
| local sparsity | 568 | **7.71 pp** | No |

Result:

**DESIGN_PRECISION_INADEQUATE**

**0 / 5** primary comparisons meet the frozen precision requirement.

This is the fatal gate condition.

## 6. Broader feasibility adjudication

Passed axes:

- temporal integrity;
- technical availability;
- nonzero exact identity support;
- exact entity resolution;
- final lineage balance;
- fixed five-year coverage contract;
- construct non-circularity.

Prospective restrictions that would otherwise have applied:

- exact matched cohort only because historical identity observability is not neutral;
- mandatory later-ACCEPT lineage sensitivity.

Fatal reason:

`design_precision_inadequate_for_frozen_5pp_effect`

Final verdict:

`ABSTAIN_PRE_OUTCOME`

Citation acquisition authorization:

`false`

## 7. Firewall verification

The post-gate outcome runner was executed against the real final adjudication.

It returned:

`POST_GATE_OUTCOME_STAGE_NOT_AUTHORIZED`

and recorded:

`network_activity_started=false`.

No OpenAlex citation query for Track A outcomes was issued.

The primary C5 outcome therefore remains unopened and can still be used in a genuinely prospective successor design.

## 8. What v0.1 established

Track A v0.1 produced useful evidence even though it did not open its primary outcome.

It established that:

1. historical decision-time paper recovery is technically feasible at very high coverage;
2. bibliographic identity observability is selection-linked enough to require explicit conditioning;
3. later manuscript lineage exists but is sparse under conservative matching;
4. a 1,815-candidate cohort is insufficient for the promised five-point top-decile-recall contrast at the observed policy overlaps;
5. the research firewall actually stops the experiment when its own prerequisites fail.

The fifth result is methodological infrastructure, not merely process. The system successfully prevented an underpowered but potentially interesting-looking downstream result from becoming the basis for post-hoc interpretation.

## 9. Prospective successor target

Using the frozen v0.1 policy-overlap geometry and the same top-decile recall / 5 pp precision requirement, the approximate matched-cohort sizes required for a 95% half-width no greater than five points are:

| Policy | Required matched N |
|---|---:|
| centrality | **4,412** |
| centroid novelty | **4,521** |
| exploration quota | **4,571** |
| k-center coverage | **4,551** |
| local sparsity | **4,321** |

A successor protocol should therefore target at least **4,600 exact-outcome-observable candidates**, preferably with additional margin for technical and identity loss, before the citation outcome box is opened.

The v0.1 outcome remains sealed.
