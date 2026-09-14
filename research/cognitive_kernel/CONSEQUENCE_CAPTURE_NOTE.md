# Consequence Capture Decision Note

**14 September 2026**

## Decision

Do **not** backfill historical Agalmic Research work as the control arm of the Cognitive Kernel consequence study.

The historical runs were not assigned under a common prospective protocol, did not share frozen verification procedures, and did not record active human attention consistently. Treating them as clean controls would create an appearance of experimental evidence without the design needed to support it.

Instead, freeze a prospective pilot before collecting outcomes.

## Why

Preregistration is useful because it distinguishes confirmatory from exploratory work and constrains researcher degrees of freedom by making design and analysis choices visible before outcomes are known. Structured preregistration has been shown to reduce, though not eliminate, analytic flexibility. This matters especially here because the intervention and its evaluation framework were developed by the same research programme.

The pilot therefore freezes:

- the matched-pair unit;
- permitted task families;
- attention and guardrail outcomes;
- the direction of favourable effects;
- no scalar utility score;
- descriptive-only pilot interpretation;
- stop conditions;
- explicit prohibition on retrospective controls;
- an amendment rule after outcome inspection.

## What this does not establish

A frozen pilot protocol does not make the Kernel effective. It merely makes future positive or negative evidence more interpretable.

Twelve pairs is a coverage target, not a powered sample-size claim. The pilot exists to test measurement feasibility, estimate outcome variability, expose pairing failures, and determine whether a later confirmatory study is justified.

## Evidence lineage

- Nosek et al. (2019), *Preregistration Is Hard, And Worthwhile*. Trends in Cognitive Sciences. https://doi.org/10.1016/j.tics.2019.07.009
- Bakker et al. (2020), *Ensuring the quality and specificity of preregistrations*. PLOS Biology. https://doi.org/10.1371/journal.pbio.3000937
- Crüwell et al. (2021), *Preregistration in diverse contexts: a preregistration template for the application of cognitive models*. Royal Society Open Science. https://doi.org/10.1098/rsos.210155

## Resulting artefacts

- `CONSEQUENCE_PILOT_MANIFEST.json`
- `consequence-record.schema.json`
- `scripts/record-kernel-consequence.mjs`
- `scripts/summarize-kernel-consequences.mjs`
- `scripts/test-kernel-consequence.mjs`

Raw records remain authoritative. Summaries are derived and reproducible.
