# Track A v0.2 Multi-Cohort Redesign Draft

**Status:** prospective redesign after v0.1 ABSTAIN and before any Track A citation outcome is opened  
**Date:** 20 September 2026

## Design objective

Retain the v0.1 scientific question and primary endpoint while increasing the outcome-observable candidate count enough to satisfy the already-frozen five-percentage-point precision target.

The redesign is permitted because v0.1 stopped before citation acquisition. No C5 outcome has been inspected.

v0.1 remains permanently recorded as:

`ABSTAIN_PRE_OUTCOME`

v0.2 is a new protocol version, not a reinterpretation of v0.1.

## What does not change

Unless a later preregistration explicitly argues otherwise, retain:

- candidate state at the historical paper-submission deadline;
- historical text-only outcome-blind representation;
- 20% primary attention budget;
- seeded-random baseline;
- transparent structured policies;
- high-recognition recall as the primary endpoint;
- top-decile high-recognition definition;
- five-percentage-point smallest effect of interest;
- exact OpenAlex identity as the primary outcome-observation route;
- fixed five-year follow-up per conference cohort;
- exact and sensitivity manuscript-lineage diagnostics;
- paired bootstrap and exchangeability-randomization analysis;
- ABSTAIN when prospective precision is inadequate.

## Precision target

Under the actual v0.1 policy-overlap geometry, the matched sample sizes required for a normal-approximation 95% half-width no greater than five percentage points are:

| Policy | Required exact-outcome-observable N |
|---|---:|
| centrality | 4,412 |
| centroid novelty | 4,521 |
| exploration quota | 4,571 |
| k-center coverage | 4,551 |
| local sparsity | 4,321 |

The prospective v0.2 floor is therefore:

**at least 4,600 exact-outcome-observable candidates**

A practical acquisition target should be higher to allow for technical loss and identity non-observability.

## Proposed historical cohorts

Use ICLR conference years:

**2017, 2018, 2019, 2020, 2021**

These cohorts can all support a completed five-year downstream follow-up horizon by September 2026.

Metadata-only ACCEPT+REJECT frame sizes in the frozen ICLR dataset are:

| Year | ACCEPT + REJECT records |
|---|---:|
| 2017 | 442 |
| 2018 | 828 |
| 2019 | 1,419 |
| 2020 | 2,213 |
| 2021 | 2,594 |
| **Total** | **7,496** |

This is only an upper candidate frame. It is not the final T0 cohort.

For orientation only, applying the 2020 pre-deadline-revision retention ratio to the five-year frame would imply roughly 6,148 T0 candidates; applying the 2020 exact-identity match fraction again would imply roughly 5,731 observable candidates. These are planning heuristics, not evidence that v0.2 will pass.

The multi-year protocol must still build and audit each historical cohort independently before pooling.

## Historical-deadline integrity

For every year, freeze the paper-submission deadline from an authoritative contemporaneous conference source before selecting revision references.

Known sources currently include:

- ICLR 2017 Call for Papers: https://iclr.cc/archive/www/doku.php%3Fid%3Diclr2017%3Acallforpapers.html
- ICLR 2018 Dates: https://iclr.cc/Conferences/2018/Dates
- ICLR 2018 Call for Papers: https://iclr.cc/Conferences/2018/CallForPapers
- ICLR 2019 Dates: https://iclr.cc/Conferences/2019/Dates
- ICLR 2019 Call for Papers: https://iclr.cc/Conferences/2019/CallForPapers
- existing frozen ICLR 2020 and 2021 date sources.

Where contemporaneous sources disagree on a deadline time, use the earliest defensible cutoff for the primary T0 definition and preserve the alternative as a temporal sensitivity analysis.

Do not infer missing deadlines from later revision timestamps.

## Year-stratified allocation

Do **not** pool all candidate representations into one cross-year geometry by default.

For each conference year:

1. build the decision-time T0 candidate frame;
2. acquire and extract historical PDFs under the same safety rules;
3. fit the representation only on that year's usable candidate pool;
4. apply every policy at the same 20% within-year budget;
5. define seeded random within year using a deterministic year-specific seed derived from the frozen global seed;
6. freeze the selected IDs before any citation outcome is opened.

This preserves the historical meaning of “20% of available attention” and avoids giving large later conference cohorts disproportionate influence over the geometry used for earlier cohorts.

## Multi-year primary estimand

For each year, define high recognition as the top decile of C5 **within that cohort's exact observable matched set** using the same fixed five-year follow-up horizon relative to that cohort.

The multi-year primary recall for a policy is:

`total high-recognition candidates recovered across years / total high-recognition candidates across years`.

The primary contrast remains:

`structured policy recall - seeded random recall`.

Bootstrap resampling should be stratified by conference year so that each resample preserves cohort structure.

The exchangeability randomization should permute high-recognition labels within year, not across years.

## Cohort-specific follow-up windows

Each conference year receives the same duration, not the same calendar dates.

The exact date window for each cohort must be frozen before citation acquisition.

A cohort is admitted only when the complete five-year window is available at execution time.

## Identity observability

Repeat the exact identity-support audit for every cohort before citation acquisition.

Then audit:

- exact match fraction by year;
- historical decision within year;
- policy-specific match support within year;
- pooled policy-specific observability effect after year stratification.

Candidates without exact identity remain unobserved, never zero-valued.

If one conference year lacks comparison support, exclude that year prospectively before pooled outcome acquisition or ABSTAIN if the remaining design loses required precision.

## Lineage

Run the same conservative later-manuscript lineage logic from each source year into later ICLR years.

Because later cohorts can themselves contain descendants of earlier candidates, the multi-year candidate graph must prevent the same manuscript lineage from behaving as independent scientific candidates in a pooled sensitivity analysis.

Primary policy selection remains year-local.

Lineage sensitivity must include at least:

- exclusion of any detected exact/near descendant chain;
- exclusion of source candidates with a later ACCEPT descendant.

## Precision gate

The multi-year candidate frame does not automatically authorize outcomes.

After all year-specific policy selections and exact identity support are frozen, compute the actual stratified prospective precision using those fixed selections.

Required condition:

- at least one preregistered primary comparison must have a 95% design half-width <= 5 pp for CONDITIONAL PASS;
- all declared primary comparisons must meet the bound for unrestricted PASS.

If none meet the bound, v0.2 also ABSTAINS before outcome acquisition.

## Acquisition sequencing

The next implementation sequence is:

1. freeze authoritative 2017–2019 deadline cutoffs;
2. recover or reacquire the OpenReview revision index for 2017–2021;
3. construct year-specific ACCEPT/REJECT manifests;
4. build revision-reference candidates without downloading PDFs;
5. run a **candidate-count and prospective precision feasibility audit**;
6. only if the candidate count can plausibly produce >=4,600 exact-observable cases, proceed to multi-year PDF acquisition;
7. otherwise redesign again without opening C5.

This ordering prevents another multi-gigabyte acquisition from becoming the way we discover an obviously underpowered design.

## Stop rule

Do not open the still-sealed ICLR 2020 C5 outcomes merely because v0.1 has completed.

The existing outcome box becomes admissible only as part of a prospectively frozen successor protocol whose precision gate passes before any cohort's citation outcomes are queried.
