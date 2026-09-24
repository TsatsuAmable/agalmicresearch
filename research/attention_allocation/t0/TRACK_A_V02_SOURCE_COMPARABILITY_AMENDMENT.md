# Track A v0.2 source-comparability amendment

**Date frozen:** 2026-09-24  
**Status:** prospective amendment, frozen before any new bulk paper acquisition or citation-outcome acquisition  
**Parent protocol:** `TRACK_A_V02_MULTICOHORT_REDESIGN.md`  
**Outcome status:** all Track A C5 outcomes remain sealed

## Why an amendment is required

The original v0.2 design required at least **4,600 exact-outcome-observable candidates** while preserving historical paper state.

Verified full-cohort historical text currently contributes:

- ICLR 2018: 826
- ICLR 2019: 1,419
- ICLR 2020: 1,815
- subtotal: **4,060**

The public ICLR 2021 recovery lane is now bounded closed:

- current OpenReview state is not historical T0;
- the reviewed-version field is perfectly decision-linked;
- pre-cutoff arXiv availability is materially decision-linked;
- OpenReview says the requested historical PDF is not public;
- the bounded Common Crawl retry recovered 0/10 forum and 0/10 PDF captures.

The programme will therefore stop trying to make ICLR 2021 look like a neutral full cohort.

## Candidate source strata admitted for audit

This amendment prospectively permits exactly two additional source strata to be audited before any outcome is opened.

### A. ICLR 2017 via PeerRead

PeerRead is an external public dataset introduced by Kang et al. (NAACL 2018). Its public repository contains **427 ICLR 2017 paper PDFs**, 427 parsed-paper records and 427 review/decision records across train/dev/test. The paper describes the ICLR section as all ICLR 2017 submissions collected from OpenReview, with actual conference decisions.

This source is **not yet admitted** to the empirical cohort. It first must pass all of the following outcome-blind gates:

1. map records to the frozen canonical ICLR 2017 ACCEPT/REJECT frame;
2. report exact mapping and decision agreement;
3. establish that the preserved PDF is a reviewed submission draft rather than a post-decision camera-ready substitution;
4. report technical extraction coverage overall and by historical decision;
5. require >=95% primary usability overall and in both decision strata;
6. require the 95% interval for the ACCEPT-minus-REJECT technical-availability gap to lie wholly inside +/-5 percentage points;
7. audit exact downstream identity support without acquiring citation outcomes.

If provenance cannot distinguish submission drafts from post-decision substitutions, this stratum is rejected.

### B. ICLR 2021 pre-cutoff arXiv stratum

The frozen metadata audit identified 497 exact pre-cutoff arXiv matches and **487** after conservative cross-year deduplication.

This source is known not to be a neutral representation of all ICLR 2021 submissions:

- ACCEPT coverage: 26.54%
- REJECT coverage: 15.50%
- ACCEPT-minus-REJECT gap: +11.04 percentage points
- 95% interval: [+7.68, +14.50] percentage points

Therefore this stratum **must never be described or analysed as a full ICLR 2021 cohort**.

It may be admitted only under the restricted estimand:

> ICLR 2021 primary-comparison candidates with an exact, unique, pre-cutoff arXiv version surviving the frozen cross-year deduplication rule.

Before admission it must pass:

1. deterministic PDF retrieval from the frozen arXiv identity/version;
2. technical extraction under the same safety and minimum-text rules;
3. exact downstream identity support audit without citation acquisition;
4. manuscript-lineage audit;
5. fixed source manifest and hashes before policy selection.

Its decision-linked availability remains a limitation of external validity, not a defect to be statistically wished away.

## Representation and allocation

Every admitted **year × source** stratum is treated independently.

For each stratum:

1. fit the historical text representation only within that stratum;
2. apply the same frozen 20% primary attention budget within the stratum;
3. derive the deterministic random seed from the global seed plus year/source identifier;
4. freeze all policy selections before any citation outcome is queried.

No cross-source representation geometry is allowed.

## Outcome definition

For each admitted stratum:

- use the same exact OpenAlex identity rule;
- use the same five-year C5 follow-up duration;
- define high recognition as the top decile within the exact-observable stratum;
- leave unmatched identities unobserved rather than assigning zero.

The augmented primary estimand is explicitly source-stratified:

`sum(high-recognition candidates recovered across admitted strata) / sum(high-recognition candidates across admitted strata)`

for each policy, contrasted with seeded random.

This estimand applies only to the admitted source-defined populations. It is **not** an estimate for all ICLR 2021 submissions.

Bootstrap resampling and exchangeability randomization must operate within year/source strata.

## Same-venue full-cohort diagnostic

A separate diagnostic must report the estimate using only admitted strata that approximate full conference cohorts.

The restricted 2021 arXiv stratum is excluded from this diagnostic.

This prevents the augmented estimand from silently replacing the broader population question.

## Pre-outcome feasibility arithmetic

Before technical and identity loss:

- verified 2018-2020 subtotal: 4,060
- PeerRead ICLR 2017 maximum: +427
- deduplicated pre-cutoff ICLR 2021 arXiv maximum: +487
- optimistic amended total: **4,974**
- optimistic cushion over the 4,600 target: **374**

This arithmetic authorizes **audits only**. It does not authorize bulk acquisition or outcomes.

## Authorization gate

After source admission, technical extraction, exact identity support and policy selections are frozen, recompute the actual prospective precision using the fixed overlap geometry.

- unrestricted PASS: all declared primary comparisons have 95% design half-width <= 5 pp;
- CONDITIONAL PASS: at least one preregistered primary comparison meets the bound and the restriction is frozen before outcomes;
- otherwise: `ABSTAIN_PRE_OUTCOME`.

Citation acquisition remains prohibited until this gate passes.

## Stop rule

If the admitted source strata cannot produce a sufficiently precise design after technical and identity loss:

1. v0.2 returns `ABSTAIN_PRE_OUTCOME`;
2. do not weaken the five-point precision target;
3. do not reopen unbounded ICLR 2021 archive recovery;
4. a cross-venue design, if pursued, becomes a separately versioned v0.3 amendment with venue-specific comparability rules frozen before source acquisition.

## Immediate next action

Audit the PeerRead ICLR 2017 source first. It is the highest-value unresolved source because it may add a nearly complete historical same-venue cohort without changing the target population.

Only after that audit should the programme decide whether the restricted 2021 arXiv stratum needs technical acquisition.
