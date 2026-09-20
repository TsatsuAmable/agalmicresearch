# T0 Technical Availability Gate v0.1

**Frozen:** 20 September 2026  
**Scope:** additional technical loss after a candidate has already entered the ICLR 2020 pre-deadline revision-reference cohort.  
**Status:** frozen before bulk acquisition/extraction completes.

## Why this gate exists

The broader feasibility gate deliberately avoids a universal matching percentage because balanced missingness can be more informative than a high but strongly outcome-dependent match rate.

This narrower gate addresses a different question: once a historical T0 revision reference has already been identified, did our own acquisition and extraction machinery introduce another material selection mechanism?

The answer must be fixed before the final download counts are known.

## Primary usable-content rule

A candidate is primary-usable only when:

- acquisition has terminal success;
- extraction has `status=ok`;
- extracted character count is at least 1,000;
- page-level extraction error count is zero.

Records with lower text yield or page errors remain preserved for audit and sensitivity work but are not silently promoted into the primary representation.

The 1,000-character rule is an engineering integrity floor, not a scientific-quality score.

## Completion rule

Do not adjudicate while the pipeline is still running.

The audit is complete only when every T0 reference candidate has:

- a terminal acquisition record; and
- where acquisition succeeded, a terminal extraction record.

Before that point the only valid gate status is:

`INCOMPLETE_DO_NOT_ADJUDICATE`.

## Decision-stratum balance

Compute primary-usable fractions separately for historical ACCEPT and REJECT strata.

The balance statistic is:

`usable_fraction_ACCEPT - usable_fraction_REJECT`

with a 95% Newcombe-Wilson confidence interval for the difference of two proportions.

Historical decision is used only for this diagnostic. It does not enter acquisition, extraction, candidate representation, or allocation policy.

## Frozen equivalence margin

The decision-stratum equivalence margin is **±5 percentage points**.

This is tied to the downstream programme's already-frozen smallest effect of interest: a 5 percentage-point change in high-recognition recall. If the technical pipeline can plausibly induce a decision-linked availability shift of the same order, the experiment should not pretend to resolve effects at that scale.

## Adjudication

### PASS_TECHNICAL_AVAILABILITY

Requires all of:

- primary-usable fraction >= 95% overall;
- primary-usable fraction >= 95% among ACCEPT;
- primary-usable fraction >= 95% among REJECT;
- the full 95% Newcombe-Wilson interval for ACCEPT-minus-REJECT usable fraction lies inside [-0.05, +0.05].

### CONDITIONAL_TECHNICAL_AVAILABILITY

Used when all of:

- primary-usable fraction >= 90% overall;
- primary-usable fraction >= 90% among ACCEPT;
- primary-usable fraction >= 90% among REJECT;
- observed ACCEPT-minus-REJECT usable-fraction gap lies inside [-0.05, +0.05];

but the stricter PASS criteria are not met.

A conditional result permits only a prospectively narrowed observable-content cohort and must carry the missingness limitation forward.

### ABSTAIN_TECHNICAL_AVAILABILITY

Required otherwise.

Do not repair an ABSTAIN result by substituting current PDFs, arXiv copies, OCR services, or alternate sources after seeing the decision-linked failure pattern. Any such redesign is a new protocol version.

## Boundary

Passing this gate does **not** pass the full empirical programme.

The broader `PRE_OUTCOME_FEASIBILITY_GATE.md` still governs:

- downstream outcome support;
- outcome-observability differences;
- entity resolution;
- resubmission lineage;
- fixed follow-up window;
- construct non-circularity;
- statistical precision.

This gate closes only the technical T0-content-availability question.
