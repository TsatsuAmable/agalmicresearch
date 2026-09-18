# OpenReview Acquisition: Policy, Provenance, and Current Blocker

**Agalmic Research — 18 September 2026**

## Result

The current failure to acquire the ICLR 2017–2022 corpus should not be treated as evidence that public historical records are unavailable. OpenReview's public venue directory exposes ICLR conference records across the target years, including explicit accepted/rejected navigation for ICLR 2017. However, live bulk API probes from the current runner returned HTTP 429 and then persistent HTTP 403 even after conservative throttling.

The correct state is therefore **acquisition blocked at the API/interface layer**, not **dataset unavailable**.

## Acquisition policy

This programme adopts the following rule for public research data acquisition:

1. Prefer documented source APIs or source-provided exports.
2. Respect access controls, rate limits, robots/service protections, licensing, privacy, and record-level restrictions.
3. Do not evade 403/429 controls through IP rotation, credential borrowing, browser scraping intended to bypass API controls, or other circumvention.
4. Preserve source responses immutably and hash every acquired page before transformation.
5. Record endpoint/API generation, invitation/group identifier, query parameters, acquisition timestamp, response status, and software version.
6. Separate source acquisition from canonicalisation. Cleaning never overwrites raw source records.
7. If a source has multiple supported interfaces, switching interfaces is allowed only when the alternative is documented or source-sanctioned and preserves equivalent provenance.
8. Third-party mirrors may be used for feasibility exploration only unless their completeness, provenance, licensing, and transformation history are independently validated. They must never silently replace the primary source.
9. If primary-source acquisition remains unavailable, contact/support or an official bulk-export route is preferred to circumvention.
10. A source-access failure is an infrastructure result. It must not be repaired by weakening the temporal firewall, silently dropping rejected papers, or selecting a convenience sample that changes the estimand.

## What current evidence says

OpenReview's public venue pages demonstrate that the target ICLR years remain represented on the platform. The 2017 conference page visibly includes rejected submissions as a first-class category, which is important because rejected-candidate observability is central to this programme.

Fresh web retrieval on 18 September 2026 also encountered OpenReview pages reporting that the API was temporarily unavailable. This makes a service-side or interface-wide availability problem plausible and weakens the hypothesis that our request rate alone caused the continuing failure.

This does **not** establish that every field required by the work order remains retrievable, nor that all historical versions/timestamps are preserved. In particular, later work using OpenReview notes that historical review snapshots can be overwritten during discussion. The temporal-firewall audit must therefore test field-level timestamp/version availability rather than infer it from page visibility.

## Blocker classification

- Physical: no evidence.
- Legal/policy: acquisition must respect OpenReview controls and record licences; no evidence currently justifies circumvention.
- Permission: possible for some endpoints/records, unresolved.
- Architecture: API1/API2 and historical venue-schema differences remain relevant.
- Tooling: acquisition script now throttles conservatively and preserves provenance.
- Interface/service: **current leading blocker** because 403 persists at very low request rate and public OpenReview pages simultaneously report API unavailability.
- Procedure: official support/bulk-export discovery remains an available next path.
- Assumption: rejected. The assumption that slower requests alone would solve acquisition is not supported.

## Decision rule

Do not spend additional attention tuning request cadence unless OpenReview supplies a rate requirement. Retry the documented API after service recovery; in parallel identify an official authenticated/bulk route or ask OpenReview support for the sanctioned method for reproducible historical research acquisition.

If an official route cannot supply rejected submissions with adequate temporal provenance, the programme should test a narrower corpus or issue CONDITIONAL PASS/ABSTAIN rather than substitute outcome-biased data.

## Research consequence

This blocker is already informative for the programme's reproducibility architecture: acquisition availability and source-interface identity belong in the dataset manifest. A reproducible study cannot merely publish transformation code if the source query itself is fragile or permission-dependent.

## Sources

- OpenReview Venue Directory and ICLR venue pages, retrieved 18 September 2026.
- OpenReview Contact page, retrieved 18 September 2026, providing a support route for non-bug queries.
- OpenReview public pages observed 18 September 2026 reporting API unavailability on multiple venue pages.
- Agalmic Research live acquisition probes, 18 September 2026: HTTP 429 followed by HTTP 403 under reduced request pressure.

This note makes no claim that OpenReview guarantees bulk historical access or that the present outage explains every 403 response. Those questions remain empirical.