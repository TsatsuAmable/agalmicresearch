# ICLR 2021 arXiv Recovery Audit Result

**Date:** 2026-09-23
**Programme:** Attention Allocation Under Cognitive Abundance
**Protocol:** `ICLR2021_ARXIV_RECOVERY_PROTOCOL.md`
**Status:** metadata-only audit complete
**Adjudication:** `ARXIV_ROUTE_CONDITIONAL`

## Executive result

The frozen ICLR 2021 arXiv route recovers a substantial historically bounded partial source, but it does **not** pass the programme's neutrality condition and does not by itself close the v0.2 source-feasibility deficit.

Under the preregistered exact-title rule and the fixed **2020-10-02 15:00 UTC** cutoff, **497 / 2,594** canonical ACCEPT+REJECT candidates have an unambiguous exact pre-cutoff arXiv match. After a conservative cross-year deduplication against known ICLR 2017-2020 titles and arXiv identities, **487** remain as additional candidates.

The key blocking result is decision-linked observability:

| Historical decision | Exact pre-cutoff matches | Canonical frame | Match fraction |
|---|---:|---:|---:|
| ACCEPT | 228 | 859 | 26.54% |
| REJECT | 269 | 1,735 | 15.50% |
| **ACCEPT - REJECT** |  |  | **+11.04 pp** |

The 95% Newcombe-Wilson interval for the ACCEPT-minus-REJECT difference is **[+7.68, +14.50] percentage points**. The entire interval lies beyond the programme's already-frozen ±5 percentage-point materiality margin.

No restricted arXiv-only estimand was frozen before this result was observed. It would therefore be post hoc to reinterpret this decision-linked substrate as `USEFUL_PARTIAL_SOURCE` for the existing representative estimand.

## Canonical candidate frame

The audit uses the existing Agalmic Track A manifest as the decision authority rather than adopting the external database's decision labels.

Canonical 2021 primary comparison frame:

- ACCEPT: **859**
- REJECT: **1,735**
- total: **2,594**

This resolves a one-record discrepancy in the external source. Forum `xGZG2kS5bFk` is labelled ACCEPT by an external witness but is canonically `WITHDRAWN` in the frozen Agalmic manifest and is therefore excluded from the primary frame.

The pre-existing canonical title mismatch `lJuOUWlAC8i` is excluded from exact-title reconstruction. Its relevant arXiv candidate is post-cutoff, so the exclusion does not alter the primary pre-cutoff count.

Canonical manifest SHA-256:

`7a2f692468ef3e86ecebe71d6f5642d55588c7498e5dd016d7644f18199a195a`

## Metadata source and provenance

The audit uses the public ICLR database snapshot referenced by the CogComp ICLR Database project. The local frozen input is:

- file: `cs_conf_release.db`
- bytes: **1,242,087,424**
- SHA-256: `ceeaa4316f76f6a22a5856128f34e8c3f35693d145db756f9688eda42ee20ed2`

The database supplies ICLR submission identities plus candidate arXiv IDs, titles, and second-resolution publication/update timestamps. The Agalmic audit independently reapplies the frozen title-normalization and cutoff rules rather than accepting the source's precomputed `submission_arxiv` linkage as the primary result.

The source snapshot is hash-bound and the admitted arXiv identities/timestamps are reproducible from it. Independent reconstruction of the upstream candidate-discovery process remains outstanding, so this is strong snapshot provenance rather than a complete independent reproduction of the source crawler.

## Frozen matching audit

Primary matching performs Unicode NFKC normalization, case folding, punctuation normalization, and whitespace collapse, followed by exact title equality. Historical decision is not used to generate or admit matches.

Results:

- exact title matches at any arXiv timestamp: **1,232**
- exact matches with first publication no later than the cutoff: **497**
- ambiguous exact pre-cutoff submissions: **0**
- arXiv-identity collisions across submissions: **0**
- admitted exact pre-cutoff matches: **497**
- separately identified fuzzy/source-linked pre-cutoff sensitivity leads: **58**

The 58 fuzzy-only leads are not admitted to the primary set. They comprise 7 ACCEPT and 51 REJECT candidates and therefore cannot be used to soften the primary decision-linkedness result without violating the frozen rule.

## Timestamp distribution

For the 497 admitted exact matches, arXiv first-publication timestamps relative to the fixed cutoff are:

- minimum: **651.73 days before** cutoff
- 25th percentile: **128.62 days before**
- median: **103.49 days before**
- 75th percentile: **64.90 days before**
- latest admitted record: approximately **66 seconds before** cutoff

Counts by age at cutoff:

| Age before cutoff | Count |
|---|---:|
| >365 days | 21 |
| 180-365 days | 81 |
| 90-180 days | 217 |
| 30-90 days | 110 |
| 7-30 days | 39 |
| <=7 days | 29 |

This confirms that the route is genuinely historically bounded. It does not make author-selected arXiv availability selection-neutral.

## Conservative cross-year deduplication

A conservative sensitivity deduplication removes a 2021 match when either its normalized title or known arXiv ID already appears in any ICLR 2017-2020 submission in the same source snapshot.

- exact pre-cutoff set: **497**
- conservative cross-year duplicates removed: **10**
- additional candidates remaining: **487**

This is intentionally stricter than the eventual manuscript-lineage adjudicator and should be treated as a source-feasibility lower count, not as a final pooled-lineage definition.

## v0.2 feasibility arithmetic

The already-established neutral/pre-review 2018-2020 subtotal is **4,060** candidates.

Adding the 487 conservative arXiv candidates gives:

`4,060 + 487 = 4,547`

This remains **53 candidates below** the frozen 4,600 exact-observable target before technical retrieval loss and downstream identity attrition.

If all **442** unresolved ICLR 2017 candidates were optimistically granted as admissible, the upper arithmetic becomes:

`4,060 + 487 + 442 = 4,989`

That creates a nominal cushion of 389 candidates, but it is not an authorization to proceed: 2017 is not yet proven fully admissible, technical loss has not been measured for the arXiv route, and the arXiv route itself materially violates the neutrality criterion.

## Adjudication

The frozen route returns:

`ARXIV_ROUTE_CONDITIONAL`

because:

1. the route provides hundreds of exact, historically bounded records;
2. it is not sufficient by itself to reach 4,600 from the verified 2018-2020 base;
3. pre-cutoff arXiv observability is materially decision-linked, with an ACCEPT-minus-REJECT gap of +11.04 pp and a 95% interval of [+7.68, +14.50] pp;
4. no outcome leakage was used in matching or inclusion;
5. source snapshot provenance is frozen and reproducible, but upstream candidate-discovery reconstruction is not yet independently reproduced;
6. a restricted arXiv-observable estimand was not prospectively frozen and cannot be introduced after observing this imbalance merely to rescue the route.

Therefore:

- `proceed_to_bulk_content_acquisition=false`
- `citation_outcome_acquisition_authorized=false`
- `outcomes_observed=false`

Bulk arXiv PDF acquisition remains prohibited under the current protocol.

## Next admissible action

Continue outcome-blind recovery of an immutable, selection-neutral ICLR 2021 pre-review/deadline-state archive. In parallel, bounded ICLR 2017 reconstruction remains useful because at least 53 additional admissible candidates would be required even if all 487 conservative arXiv candidates were eventually usable.

If neutral historical recovery fails, a new protocol amendment may prospectively define a restricted arXiv-observable estimand or add another venue/cohort with explicit source-comparability and stratification rules. That amendment must be frozen before acquiring downstream outcomes or using the observed arXiv imbalance to tune inclusion.

The present result is a source-level constraint, not evidence about the downstream attention-allocation hypothesis.
