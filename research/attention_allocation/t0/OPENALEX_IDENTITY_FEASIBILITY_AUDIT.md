# OpenAlex Identity-Linkage Feasibility Audit v0.1

**Date:** 20 September 2026  
**Scope:** ICLR 2020 Track A pre-deadline revision-reference cohort  
**Status:** identity feasibility only; **no citation outcomes were acquired**

## Question

Before opening any downstream-value outcome, can the historical candidates be linked to OpenAlex work identities with enough support to make later outcome observation meaningful, and is that support materially different across historical ACCEPT and REJECT strata?

This is an observability audit, not an analysis of scientific value.

## Population

The audit uses the existing 1,816-candidate ICLR 2020 T0 revision-reference cohort:

- 549 historical ACCEPT
- 1,267 historical REJECT

Candidate titles and authors are used **only for evaluation-side identity resolution**. They do not enter the allocation representation or policy.

## Matching rule

The frozen primary identity rule from `TRACK_A_DOWNSTREAM_OUTCOME_PREREGISTRATION.md` is used:

- OpenAlex publication year 2019–2022;
- exact normalized title;
- at least one exact author-surname overlap;
- all satisfying OpenAlex manifestations are retained as one identity cluster.

No fuzzy match is promoted into the primary set.

## Budget-efficient acquisition

The candidate query manifest was converted into OR-batched OpenAlex `title.search.exact` filters, with at most 25 candidate titles per request and `per_page=100`.

This reduced 1,816 candidate searches to **73 API calls**.

OpenAlex currently documents up to 100 OR values per filter, a 100-result page maximum, a $0.10/day anonymous keyless API budget, and a $1/day free budget with a free API key:

- https://help.openalex.org/api/authentication/
- https://help.openalex.org/access/pricing/
- https://help.openalex.org/access/example-costs/

The completed identity acquisition recorded **$0.073 of API cost units** and used no API key. This stage requested identity metadata only and did not request citing works or citation counts.

## Acquisition correction and provenance

The first batch implementation exposed an OpenAlex filter-grammar defect in our client: unquoted title values containing commas were rejected with HTTP 400.

No failed response was treated as acquired data.

The repair quotes every exact-title value and escapes literal double quotes. The already-successful v0 batches were preserved because OpenAlex had accepted those requests; failed batches were retried under v1.

Raw-response provenance was then reconciled explicitly:

- 34 retained batches originated from valid v0 unquoted queries;
- 39 retained batches originated from corrected v1 quoted queries;
- transition to the corrected run: `2026-09-20T16:23:18Z`;
- every retained raw batch has a source-query version, query-filter hash and raw-response hash.

The v0 and v1 batch manifests preserve identical candidate membership.

## Primary result

| Population | Matched | Total | Match fraction |
|---|---:|---:|---:|
| Overall | 1,693 | 1,816 | **93.23%** |
| ACCEPT | 528 | 549 | **96.17%** |
| REJECT | 1,165 | 1,267 | **91.95%** |

Unresolved primary identities:

- 117 `NO_PRIMARY_MATCH`;
- 6 `EXACT_TITLE_NO_AUTHOR_OVERLAP`.

Among matched candidates, identity clusters contain:

- 1 OpenAlex work: 1,405 candidates;
- 2 works: 283 candidates;
- 3 works: 5 candidates.

The multiple-work result confirms the need for the preregistered identity-cluster rule rather than selecting a single arbitrary OpenAlex manifestation.

## Decision-linked observability diagnostic

The ACCEPT-minus-REJECT exact-match difference is:

**+4.23 percentage points**

95% Newcombe-Wilson interval:

**[+1.84 pp, +6.31 pp]**

The observed difference is inside the pre-existing ±5 percentage-point diagnostic margin, but the full confidence interval is **not** contained inside it.

Therefore the result is:

**DECISION_BALANCE_NOT_ESTABLISHED_WITHIN_5PP**

This matters even though overall coverage is high. Historical ACCEPT candidates are measurably more likely to have an exact OpenAlex identity than historical REJECT candidates in this cohort.

That pattern is consistent with the programme's selective-observability concern: downstream bibliographic visibility can itself depend on earlier selection. This audit does not establish why the difference exists.

## Gate consequence

This result does **not** authorize citation-outcome acquisition.

It changes the broader feasibility posture in two ways:

1. the primary OpenAlex exact-match cohort is technically large enough to remain a candidate evaluation substrate;
2. it cannot be treated as outcome-observable independently of historical selection.

If later outcome analysis proceeds, claims must be restricted to the observable matched cohort and must carry this selection limitation explicitly. Unmatched candidates must not receive imputed zero citations.

The frozen fuzzy-match sensitivity route may be evaluated separately, but it cannot silently replace the exact-match primary analysis.

The next admissible steps remain outcome-blind:

- complete the T0 PDF acquisition/extraction pipeline;
- freeze the final technically usable cohort;
- regenerate representation and preregistered selections;
- intersect the final cohort with identity observability;
- run the prospective design-precision audit;
- only then adjudicate whether opening citation outcomes is scientifically worthwhile.

## Evidence artefacts

The persistent data directory contains:

- candidate query manifest;
- v0 and v1 batch query manifests;
- 73 raw OpenAlex batch responses;
- acquisition ledger;
- reconciled batch provenance;
- per-candidate resolved identity clusters;
- identity-support audit.

These are research-data artefacts and are intentionally not committed into the website repository.
