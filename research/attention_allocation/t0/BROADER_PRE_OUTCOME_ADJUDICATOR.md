# Broader Pre-Outcome Feasibility Adjudicator v0.1

**Frozen:** 20 September 2026  
**Scope:** Track A ICLR 2020 historical-allocation experiment after outcome-blind T0 finalization and before any real citation outcome is acquired.

## Purpose

The programme already has separate gates for:

- decision-time provenance and T0 acquisition;
- technical PDF/extraction availability;
- exact OpenAlex identity observability;
- resubmission/manuscript lineage;
- final policy-specific observability;
- final policy-specific lineage exposure;
- prospective design precision;
- fixed downstream outcome definition.

The broader adjudicator combines those frozen artefacts into one final pre-outcome verdict.

It reads **no citation outcomes**.

## Verdicts

### PASS_PRE_OUTCOME

All frozen criteria pass without material restriction.

This authorizes only the preregistered descriptive downstream-outcome recovery analysis.

It never authorizes a causal claim that historical acceptance would have caused the observed later value.

### CONDITIONAL_PASS_PRE_OUTCOME

The experiment can proceed only under restrictions that were determined before outcome inspection.

Examples include:

- exact matched cohort only because identity observability is not historically neutral;
- technical usable subset only;
- only precision-adequate policy contrasts;
- mandatory lineage sensitivity analysis.

Every restriction is written into the adjudication output before citation acquisition.

### ABSTAIN_PRE_OUTCOME

Citation acquisition does not run under protocol v0.1.

ABSTAIN is mandatory for:

- unresolved temporal leakage;
- terminal technical-availability failure;
- absent identity support in a required comparison stratum;
- policy-specific observability bias at or above the frozen materiality margin;
- lineage ambiguity that materially affects a primary contrast;
- construct circularity;
- failure of the fixed follow-up contract;
- no preregistered primary contrast with prospective precision adequate for the frozen smallest effect of interest.

## Inputs

The adjudicator requires:

- finalization status;
- technical-availability audit;
- final identity-observability audit;
- final lineage-substrate audit;
- prospective design-precision audit;
- frozen representation manifest;
- frozen row index;
- frozen policy manifest;
- downstream-outcome preregistration document.

Every input is SHA-256 bound into the output.

## Temporal integrity

The adjudicator requires:

- `OUTCOME_BLIND_T0_STAGE_COMPLETE`;
- `outcomes_touched=false`;
- `FROZEN_T0_REPRESENTATION`;
- `FROZEN_T0_POLICY_SELECTIONS`;
- a frozen cohort hash bound into the representation;
- no decision, review, citation, C5, downstream-value or acceptance-prediction fields in the row index.

Failure is fatal.

## Outcome support

Exact OpenAlex identity support must be nonzero for:

- the final frozen cohort;
- historical ACCEPT;
- historical REJECT;
- every policy at the primary 20% budget.

This does not require a universal match-rate threshold.

Unmatched candidates remain unobservable rather than being imputed as zero-value outcomes.

## Differential observability

If final identity observability is neutral inside the frozen ±5 percentage-point margin, this axis passes.

If historical-decision neutrality is not established but every primary policy-vs-random observability-induced recall shift remains inside ±5 points, the gate may proceed conditionally on the exact matched cohort.

If policy-specific observability bias itself exceeds the five-point materiality margin, the primary comparison ABSTAINS.

## Entity resolution

The primary analysis uses the frozen exact-title+author OpenAlex identity clusters.

Fuzzy identity recovery remains sensitivity-only.

## Lineage

If final lineage balance is supported, the axis passes with a mandatory later-ACCEPT lineage sensitivity analysis.

If historical lineage balance is uncertain but policy-specific exact and sensitivity-lineage differences remain inside ±5 points, the analysis may proceed conditionally.

If lineage imbalance materially affects a primary policy contrast, ABSTAIN.

## Coverage window

The downstream protocol must still contain the frozen:

- start: **2019-09-26**;
- end: **2024-09-25**;
- primary outcome: **C5**.

No horizon can be changed after policy geometry or outcome support is observed.

## Construct non-circularity

The final representation and policy artefacts must remain outcome-blind.

The adjudicator checks for prohibited outcome keys in the row index and verifies the frozen policy seed and 20% primary budget.

## Precision

The prospective design-precision audit is decisive.

- `DESIGN_PRECISION_ADEQUATE`: all frozen primary contrasts may proceed.
- `DESIGN_PRECISION_MIXED`: only prospectively adequate primary contrasts may proceed.
- `DESIGN_PRECISION_INADEQUATE`: ABSTAIN before citation acquisition.

This rule exists specifically to prevent a wide interval from being reinterpreted after seeing interesting outcomes.

## Fixture validation

A complete 100-document outcome-blind fixture was adjudicated.

It passed temporal integrity, nonzero exact identity support, exact entity resolution, fixed coverage and construct non-circularity.

It carried conditional technical, observability and lineage restrictions.

Because **0/5 primary policy contrasts** were prospectively precise enough for the frozen five-percentage-point smallest effect, the broader verdict was:

`ABSTAIN_PRE_OUTCOME`

and citation acquisition remained unauthorized.

That is the intended fail-closed behavior.

## Execution boundary

The adjudicator itself does not call OpenAlex citation endpoints.

A separate downstream acquisition step may run only when the adjudication output explicitly sets:

`citation_outcome_acquisition_authorized=true`.

A later protocol revision may redesign an underpowered experiment, but it must do so before opening the existing outcome box and must not relabel v0.1 as a successful primary test.
