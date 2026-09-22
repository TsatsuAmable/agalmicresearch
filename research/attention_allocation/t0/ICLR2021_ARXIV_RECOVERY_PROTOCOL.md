# ICLR 2021 arXiv Recovery Audit Protocol

**Date:** 2026-09-22  
**Programme:** Attention Allocation Under Cognitive Abundance  
**Track:** A v0.2 source recovery  
**Status:** frozen before arXiv coverage measurement  
**Epistemic role:** source-feasibility audit only; no citation outcome may be opened

## Purpose

Test the highest-value unresolved recovery lead from the ICLR 2021 public-source audit: whether timestamped arXiv versions can contribute enough historically bounded candidates to close the frozen v0.2 source-feasibility deficit without pretending that author-selected arXiv availability is neutral.

This is not a new programme and does not change the estimand, precision target, policy set, outcome definition, or temporal firewall.

## Fixed historical boundary

ICLR 2021 states:

- abstract deadline: 2020-09-28 15:00 UTC;
- full-paper deadline: 2020-10-02 15:00 UTC;
- reviews released: 2020-11-10;
- revisions were not allowed in the conference system while the paper was under review, and edits were allowed again during discussion;
- posting to non-peer-reviewed repositories such as arXiv was permitted.

Primary arXiv admissibility therefore uses the conservative cutoff **2020-10-02 15:00 UTC**. A candidate is not admitted merely because an arXiv version existed before review release. The arXiv version timestamp must be no later than the full-paper deadline.

Source: ICLR 2021 Call for Papers and Author Guide.

## Inputs

1. A fixed ICLR 2021 candidate identity frame with OpenReview forum ID, title, and historical ACCEPT/REJECT decision. The decision may be used only to audit differential source availability; it must not affect matching or inclusion.
2. arXiv public metadata including identifier, version timestamp, title, authors, abstract, and version history.
3. The frozen v0.2 arithmetic: verified neutral/pre-review 2018-2020 subtotal 4,060; optimistic all-2017 upper bound 442; maximum without a new source 4,502; exact-observable target at least 4,600 before technical and identity attrition.

## Matching rule

Matching is outcome-blind and conservative.

A candidate may enter the primary recovery set only when:

- an arXiv version timestamp is at or before the fixed cutoff;
- normalized title is an exact match after Unicode normalization, case folding, whitespace collapse, and punctuation normalization; and
- no competing ICLR candidate maps to the same arXiv identity under that exact-title rule.

Author information may be used only as a confirmation or collision-rejection signal after a title candidate is generated. Fuzzy title matching is excluded from the primary set and may appear only as a separately reported sensitivity lead.

No acceptance status, review score, review text, citation count, later publication venue, or downstream impact signal may influence linkage.

## Required audit outputs

Before any recovered content can join Track A, report:

- total ACCEPT and REJECT candidates in the fixed frame;
- exact pre-cutoff arXiv matches overall and by historical decision;
- ACCEPT and REJECT match fractions;
- ACCEPT-minus-REJECT difference with a 95% Newcombe-Wilson interval;
- duplicate/collision count;
- ambiguous and fuzzy-only leads separately;
- arXiv-version timestamp distribution relative to the cutoff;
- the number of additional candidates that would remain after deduplication against already admitted 2017-2020 identities;
- a conservative lower bound after observed technical retrieval loss, if retrieval is subsequently authorized.

## Adjudication

The route is not automatically admissible because it yields many records.

`USEFUL_PARTIAL_SOURCE` requires all of:

1. enough additional exact pre-cutoff candidates to make the frozen 4,600 target feasible after observed/prospectively bounded technical attrition;
2. no material evidence that arXiv observability is strongly decision-linked under the programme's existing ±5 percentage-point materiality margin, or an explicit restricted estimand that does not claim representativeness beyond the observable arXiv substrate;
3. no outcome leakage in matching or inclusion;
4. immutable arXiv identifiers/version timestamps and reproducible query provenance.

Otherwise record `ARXIV_ROUTE_INADEQUATE` or `ARXIV_ROUTE_CONDITIONAL` as appropriate. Do not lower the 4,600 target to rescue the route.

## Important limitation

Even a pre-deadline arXiv version is a public author-selected manifestation, not proof that its bytes equal the anonymous ICLR submission. The route can provide a historically bounded representation witness only under the restricted interpretation that the public version is an observable candidate representation at T0. It cannot support claims about unobserved conference-submission differences.

This limitation is structural, not a reason to silently widen matching.

## Prior-art and novelty boundary

Using arXiv timestamps for historical reconstruction is not claimed as novel. The contribution, if any, is the programme-specific admissibility discipline: prospectively fixing the temporal cutoff and matching rule, measuring decision-linked observability before outcomes, and allowing ABSTAIN rather than treating contemporary availability as historical truth.

Existing peer-review datasets such as PeerRead and later ICLR/OpenReview corpora establish that retrospective conference datasets are common research infrastructure; they do not remove the need to prove decision-time observability for this experiment.

## Stop rule

Run the metadata-only coverage audit once under this frozen rule. If the route cannot plausibly supply the source deficit after conservative attrition, stop pursuing arXiv as the primary ICLR 2021 recovery route. Continue immutable archive recovery; only after those bounded recovery routes fail may an additional-venue amendment be designed.

Bulk PDFs remain prohibited until this metadata-only gate passes. Citation outcomes remain sealed.