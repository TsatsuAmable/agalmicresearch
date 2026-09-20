# Track A v0.2 Source Feasibility Result

**Date:** 20 September 2026  
**Status:** outcome-blind source-feasibility adjudication  
**Verdict:** `SOURCE_FEASIBILITY_INADEQUATE_NEUTRAL_COHORT_REQUIRED`  
**Bulk content acquisition authorized:** **No**  
**Citation outcomes opened:** **No**

## Executive result

The prospective v0.2 multi-cohort redesign cannot yet reach the already-frozen precision target using the historically neutral text sources currently established.

The required floor remains:

**at least 4,600 exact-outcome-observable candidates**

The source audit deliberately uses candidate counts **before** technical extraction loss and exact-identity attrition. These are therefore optimistic upper bounds on eventual exact-observable N.

Currently verified pre-review or decision-time candidate upper bounds are:

| Cohort | Source | Candidate upper bound |
|---|---|---:|
| ICLR 2018 | clean historical pre-review Git snapshot | 826 |
| ICLR 2019 | clean historical pre-review Git snapshot | 1,419 |
| ICLR 2020 | frozen v0.1 decision-time T0 cohort | 1,815 |
| **Verified subtotal** |  | **4,060** |

Even if every one of the **442** raw ICLR 2017 ACCEPT/REJECT records were later proven temporally admissible, technically usable and exact-outcome-observable, the optimistic total would be:

**4,502**

This is already **98 candidates below** the 4,600 exact-observable target, before any identity or technical loss is applied.

Therefore the programme must obtain a neutral additional cohort contribution before another bulk acquisition campaign is justified.

## ICLR 2018 historical snapshot

Historical source:

`Smerity/search_iclr_2018`

Frozen commit:

`2a1c732f3683e48b3bc084052f17919ff3877c54`

The commit timestamp is approximately **103.1 hours after** the conservative submission deadline. It is therefore a near-deadline, pre-review snapshot rather than an exact-deadline archive.

Against the 828-record ACCEPT/REJECT metadata frame:

- snapshot root matches: **827 / 828**
- extracted text matches: **826 / 828 = 99.76%**
- matched roots anonymous: **827 / 827**
- official review records in snapshot: **0**
- public/official comment records in snapshot: **0**
- decision records in snapshot: **0**

Decision-stratified extracted-text coverage:

- ACCEPT: **336 / 336 = 100.00%**
- REJECT: **490 / 492 = 99.59%**

Missing root:

`SJtfOEn6-`

Matched root without archived extracted text:

`SkERSm-0-`

The source therefore passes the mechanical pre-review cleanliness audit but retains a temporal caveat: approximately four days existed between the paper deadline and the archived snapshot.

## ICLR 2019 historical snapshot

Historical source:

`Smerity/search_iclr_2019`

Frozen commit:

`245bbf3ed39fd33981e56cc20ae6c9dd66fc48bc`

The commit timestamp is approximately **91.9 hours after** the submission deadline.

Against the 1,419-record ACCEPT/REJECT metadata frame:

- snapshot root matches: **1,419 / 1,419**
- extracted text matches: **1,419 / 1,419**
- matched roots anonymous: **1,419 / 1,419**
- official review records in snapshot: **0**
- public/official comment records in snapshot: **0**
- decision records in snapshot: **0**

Decision-stratified extracted-text coverage:

- ACCEPT: **502 / 502 = 100.00%**
- REJECT: **917 / 917 = 100.00%**

This source is also mechanically pre-review clean but is a near-deadline snapshot, not proof of the exact state at the submission deadline.

Inspection of individual records confirms that the archived anonymous snapshot can differ materially from the later public OpenReview record. The historical snapshot must therefore remain pinned by Git commit rather than regenerated from today's forum state.

## ResearchArcade revision index

The ResearchArcade revision parquet is useful for explicit revision references but is **not** a complete archive of historical base submission states.

Applying the conservative pre-deadline revision rule mechanically to 2017–2021 produced:

- ICLR 2017: 0 candidates
- ICLR 2018: 0
- ICLR 2019: 0
- ICLR 2020: 1,816
- ICLR 2021: 557

This must not be interpreted as evidence that the earlier cohorts lacked decision-time papers. Inspection of the source crawler shows that legacy records with insufficient PDF-reference history can be omitted from the revision export. The parquet is therefore a positive witness for explicit revisions, not a valid denominator for historical text availability.

## ICLR 2021 reviewed-version route

A separate audit tested whether the archived OpenReview field `reviewed_version_(pdf)` could supply a neutral historical paper version.

It cannot.

Among the 2,594 ICLR 2021 ACCEPT/REJECT candidates with archived root notes:

| Historical decision | reviewed-version available | matched roots | fraction |
|---|---:|---:|---:|
| ACCEPT | 0 | 859 | **0.0%** |
| REJECT | 1,735 | 1,735 | **100.0%** |

ACCEPT-minus-REJECT availability difference:

**-100 percentage points**

Adjudication:

`REVIEWED_VERSION_ROUTE_DISQUALIFIED_SELECTION_LINKED`

The route is therefore prohibited as the primary v0.2 substrate. Using it would bake historical selection directly into paper-version observability.

## ICLR 2017

ICLR 2017 remains unresolved as a temporal source.

The raw ACCEPT/REJECT frame contains **442** candidates. For source-feasibility arithmetic, all 442 were granted as an intentionally optimistic upper bound.

Even that impossible best case does not rescue v0.2:

`826 + 1,419 + 1,815 + 442 = 4,502 < 4,600`

Consequently, exhaustive 2017 reconstruction is no longer the critical path. It may still improve the eventual design, but it cannot make the current design feasible by itself.

## Gate decision

The v0.2 source-feasibility gate therefore returns:

`SOURCE_FEASIBILITY_INADEQUATE_NEUTRAL_COHORT_REQUIRED`

with:

- `proceed_to_bulk_content_acquisition=false`
- `citation_outcome_acquisition_authorized=false`
- `outcomes_observed=false`

The result is deliberately stronger than a planning estimate. Because candidate counts precede technical and identity losses, any real downstream exact-observable count can only be lower unless an additional neutral cohort is added.

## Next admissible routes

The preferred next route is to recover a neutral ICLR 2021 submission state from an immutable historical source, ideally a deadline-state archive or a complete pre-review snapshot whose availability is not linked to acceptance.

An OpenReview support request has been sent asking specifically for:

1. the immutable ICLR 2021 submission revision current at the 2 October 2020 paper deadline;
2. a documented legacy API path for resolving historical v1 revision/reference IDs to PDF/content;
3. a public pre-review archival dump if one exists.

If no neutral ICLR 2021 route exists, the successor design must add another historically reconstructable cohort or venue under a new prospectively frozen source-comparability rule.

## Scientific interpretation

This is not a failed implementation.

The source gate has prevented two invalid shortcuts:

1. treating an incomplete revision index as evidence of historical paper absence;
2. using a paper-version field whose availability is perfectly confounded with historical rejection.

The scarcity has migrated again: the limiting resource is now **selection-neutral historical state**, not candidate metadata, downloader throughput, or evaluation code.

The v0.1 C5 outcome remains sealed.
