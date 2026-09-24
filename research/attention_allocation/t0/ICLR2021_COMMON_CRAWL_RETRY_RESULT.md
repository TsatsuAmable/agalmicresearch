# ICLR 2021 Common Crawl bounded retry result

**Date:** 2026-09-24  
**Programme:** Attention Allocation Under Cognitive Abundance  
**Track:** A v0.2 source recovery  
**Status:** outcome-blind bounded archive audit  
**Verdict:** `COMMON_CRAWL_ROUTE_NOT_PROMISING_AT_SCALE`  
**Citation outcomes opened:** **No**

## Question

Does Common Crawl `CC-MAIN-2020-45`, which falls wholly inside the locked ICLR 2021 review interval, contain enough evidence of historical OpenReview forum or PDF captures to justify a larger recovery campaign?

## Why this retry was allowed

The earlier archive sweep could not query the historical Common Crawl index because even control requests returned 504 errors. The programme therefore froze exactly one later retry once the index became queryable.

OpenReview Support has since confirmed that the requested historical PDF version is not public through OpenReview and would require a request to the ICLR organisation. That closes the normal public provider route but does not establish that independent archives contain nothing.

## Index health

On 2026-09-24 the `CC-MAIN-2020-45` index responded successfully to the control query `example.com`. At least one capture was returned, with an observed timestamp beginning `20201019153719`.

The earlier 504 failure was therefore an infrastructure/access problem, not evidence of absence.

## Frozen sample

The retry used the first ten ICLR 2021 primary-comparison-eligible forum IDs in lexicographic order from the frozen cohort manifest. Decision labels were not used to choose the sample.

| Forum ID | Historical decision | forum capture | PDF capture |
|---|---|---:|---:|
| `_0kaDkv3dVf` | ACCEPT | 0 | 0 |
| `_77KiX2VIEg` | REJECT | 0 | 0 |
| `_adSMszz_g9` | REJECT | 0 | 0 |
| `_b8l7rVPe8z` | REJECT | 0 | 0 |
| `_bF8aOMNIdu` | REJECT | 0 | 0 |
| `_cadenVdKzF` | REJECT | 0 | 0 |
| `_CrmWaJ2uvP` | REJECT | 0 | 0 |
| `_Ea-ECV6Vkm` | REJECT | 0 | 0 |
| `_HsKf3YaWpG` | REJECT | 0 | 0 |
| `_i3ASPp12WS` | ACCEPT | 0 | 0 |

Each exact forum query used:

`openreview.net/forum?id=<forum_id>`

Each exact PDF query used:

`openreview.net/pdf?id=<forum_id>`

## Result

- forum captures: **0 / 10**
- PDF captures: **0 / 10**
- total exact OpenReview URL captures: **0 / 20**
- control index query: **successful**

Every sampled OpenReview forum/PDF query returned no indexed capture.

This does not prove that Common Crawl contains no ICLR 2021 material under any URL form. It does answer the prospectively bounded feasibility question: exact forum/PDF recovery shows no positive signal on the frozen sample and does not justify a broad crawl of thousands of candidates.

## Adjudication

`COMMON_CRAWL_ROUTE_NOT_PROMISING_AT_SCALE`

Consequences:

1. stop the ICLR 2021 immutable-archive recovery lane for the current design;
2. do not broaden the Common Crawl search into an unbounded archive hunt;
3. keep bulk content acquisition closed;
4. keep citation-outcome acquisition closed;
5. preserve the ICLR 2020 C5 outcome seal;
6. move to the prospectively frozen source-comparability amendment.

The machine-readable evidence record is stored at:

`t0/commoncrawl_audit/iclr2021_cc_main_2020_45_retry.json`
