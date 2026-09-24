# OpenReview support adjudication — ICLR 2021 historical versions

**Date:** 2026-09-24  
**Programme:** Attention Allocation Under Cognitive Abundance  
**Epistemic status:** authoritative provider response for access status; does not establish non-existence of other archives

## Question under adjudication

The programme asked OpenReview whether the immutable paper revision current at the ICLR 2021 full-paper deadline could be retrieved through a documented legacy route or public pre-review archive.

## Provider response

OpenReview Support replied on 2026-09-23 that the requested PDF version **is not public** and that access would require a request to the ICLR organisation.

This is treated as an authoritative statement about OpenReview's public-access route, not as evidence that no independently archived historical copy exists.

## Adjudication

`OPENREVIEW_PUBLIC_ROUTE_CLOSED`

Consequences:

- Do not attempt to bypass OpenReview access controls or browser challenges.
- Do not treat current public submission PDFs as equivalent to the deadline/review-period version.
- Do not request privileged ICLR access merely to rescue the existing retrospective design unless the remaining neutral public-archive route fails and a later protocol explicitly justifies expert/organiser handoff.
- Keep bulk paper acquisition and citation-outcome acquisition closed.
- Preserve the v0.1 C5 outcome seal.

## Remaining bounded action

The existing stop rule leaves one public-archive action: a single canonical-sample retry against Common Crawl `CC-MAIN-2020-45`, whose crawl interval falls inside the locked ICLR 2021 review period. Common Crawl currently documents that this historical crawl exists and that its CDXJ index is publicly queryable, while also warning that the CDX API is heavily rate-limited. The retry must therefore be single-threaded, low-rate, and bounded to the frozen sample.

If that retry does not recover a complete or sufficiently selection-neutral historical-text route, **stop ICLR 2021 archive recovery** and prospectively freeze a source-comparability amendment before any new bulk content or citation-outcome acquisition.

## Search boundary

This adjudication used the first substantive provider response to the existing support request plus the programme's already-frozen archive-recovery protocol. It does not claim that every possible private, institutional, or web archive has been exhausted.
