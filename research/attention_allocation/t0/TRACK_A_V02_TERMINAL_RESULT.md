# Track A v0.2 terminal pre-outcome result

**Date:** 2026-09-24  
**Programme:** Attention Allocation Under Cognitive Abundance  
**Protocol:** Track A v0.2 multi-cohort redesign + source-comparability amendment  
**Verdict:** `ABSTAIN_PRE_OUTCOME_SOURCE_INADEQUATE`  
**Bulk paper acquisition authorized:** **No**  
**Citation-outcome acquisition authorized:** **No**  
**Track A C5 outcomes opened:** **No**

## Result

Track A v0.2 cannot meet its already-frozen precision requirement with the admissible historical sources available under the prospectively frozen protocol.

The precision floor remains:

**at least 4,600 exact-outcome-observable candidates**

Verified full-cohort historical text contributes:

- ICLR 2018: 826
- ICLR 2019: 1,419
- ICLR 2020: 1,815
- subtotal: **4,060**

The ICLR 2021 public archive lane is closed for this design:

- current OpenReview state is not T0;
- `reviewed_version_(pdf)` is perfectly historical-decision-linked;
- the pre-cutoff arXiv route is materially decision-linked and only supports a restricted source-defined population;
- OpenReview confirmed the requested historical PDF is not public;
- a healthy, bounded Common Crawl retry found 0/10 forum and 0/10 PDF captures.

The source-comparability amendment then tested PeerRead ICLR 2017. PeerRead contains real conference submissions and real decisions, but at least one preserved accepted-paper PDF demonstrably incorporates material added after reviewer discussion. It therefore fails the frozen submission-time provenance requirement.

The only remaining amended stratum is the conservatively deduplicated pre-cutoff ICLR 2021 arXiv set:

- optimistic maximum: **487**

Even granting all 487 before technical or identity loss:

**4,060 + 487 = 4,547 < 4,600**

The design is therefore impossible under the frozen v0.2 source rules before further acquisition.

## Scientific interpretation

This is a substantive negative result, not an implementation failure.

Two successive protocol versions stopped without observing the downstream citation outcome:

- v0.1 stopped because 1,815 candidates could not deliver the required prospective precision;
- v0.2 stopped because historically admissible source coverage cannot reach the sample floor required to test the same effect without relaxing temporal integrity or population definition.

The protocol has therefore prevented three tempting but invalid moves:

1. opening outcomes for an underpowered design;
2. treating decision-linked historical availability as neutral missingness;
3. substituting post-review revised papers for submission-time candidate state.

## What does not happen next

- Do not lower the five-percentage-point precision target.
- Do not open the sealed ICLR 2020 citation outcomes.
- Do not download the 2021 arXiv stratum merely because tooling exists.
- Do not resume unbounded ICLR 2021 archive hunting.
- Do not treat PeerRead PDFs as T0 after the provenance counterexample.

## Next research version

Any continuation is **Track A v0.3**, not a reinterpretation of v0.2.

Before collecting new paper text, v0.3 must prospectively choose and freeze an additional source population. The source-screening order is:

1. same-venue older ICLR cohorts, beginning with ICLR 2016 if a defensible historical state exists;
2. only then a cross-venue cohort with explicit venue/source stratification and comparability rules.

The first v0.3 action is a metadata/provenance screen only. No citation outcomes are required or authorized.

## Outcome seal

The ICLR 2020 C5 outcome remains unopened.

`network_activity_started=false` remains the governing state for Track A citation acquisition.
