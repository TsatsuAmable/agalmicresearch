# Attention Allocation Under Cognitive Abundance

**Status:** empirical programme, feasibility phase  
**Gate:** NOT YET EVALUATED  
**Empirical policy simulations:** prohibited until feasibility criteria are frozen and the gate passes.  
**Synthetic engineering fixtures:** permitted only to test harness mechanics; they are non-evidentiary.

## Research question

Given more potentially valuable knowledge candidates than humans can evaluate, which allocation policies maximise realised epistemic value per unit of scarce human attention without systematically suppressing uncertain, novel, minority, dissenting, or otherwise unconventional candidates?

The programme is explicitly falsification-capable. Null, negative, contradictory, ambiguous, CONDITIONAL PASS and ABSTAIN outcomes are valid.

## Constructs kept separate

Candidate generation, candidate evaluation, selection, realised discovery and downstream epistemic value are separate stages. More generated candidates do not imply more discovery.

The initial pressure parameter is rho = lambda E[C] / B, where lambda is candidate arrival, C evaluation cost and B attention budget. This is a provisional experimental coordinate, not a claimed universal law.

## Current prior-art verdict

The broad allocation problem is **not novel**. Active learning already studies allocation of expensive oracle labels; bandit and exploration/exploitation literatures study scarce sampling; selective-label research establishes that historical decisions alter which outcomes become observable.

The programme can still contribute if it demonstrates something narrower and empirical: how scientific-candidate allocation policies behave as candidate pressure changes when outcome observability is selection-affected, novelty is measured pluralistically, and the evaluation preserves a temporal firewall.

A particularly important falsifier already exists. Teplitskiy et al. (2022) found no general anti-novelty pattern in peer review across their journal samples and instead observed higher acceptance for their novelty measure. The programme therefore MUST NOT encode “peer review suppresses novelty” as a premise.

Novelty measurement is itself contested. Fontana et al. (2020) found common combinatorial novelty indicators sensitive to construction and overlapping with interdisciplinarity. Embedding distance or atypical citation combinations may therefore be candidate measures, never ground truth.

## Empirical substrate

Development cohort: ICLR/OpenReview 2017–2022. Later years are held back for temporal validation.

Raw source records are immutable. Clean/canonical records are derived. Every field used by an allocation policy must be classified AVAILABLE_AT_DECISION_TIME. Future outcomes and fields with unresolved timestamps are blocked by architecture.

## Stage A synthetic engineering harness

A deterministic synthetic harness may be built and exercised before the empirical gate passes, but only to test software and protocol invariants. It must not be used to rank policies for the research programme or to support publication claims.

The harness must:

- expose identical candidate pools and budgets to every policy;
- structurally redact evaluator-only latent value from policy inputs;
- use multiple scenario families so one assumed world cannot masquerade as a general result;
- preserve deterministic seeds and versioned configuration;
- fail on budget overspend, duplicate selection or evaluator leakage;
- label all outputs `ENGINEERING_FIXTURE_ONLY`.

The authoritative specification is `research/attention_allocation/synthetic/STAGE_A_SPEC.md`.

## Feasibility before hypotheses

Before any empirical policy comparison, report completeness by year and decision; longitudinal match rates by decision/year/metadata; unresolved matches; lineage ambiguity; resubmissions; outcome-window completeness; missingness; and temporal leakage.

The gate criteria themselves must be frozen before substantive empirical policy outcomes are inspected. We will not invent a threshold after seeing whether it permits the desired experiment.

## Causal boundary

Later citations/publication are not intrinsic counterfactual values. Conference selection changes visibility, publication opportunity, subsequent attention and potentially the work itself. Retrospective policy simulation can describe recovery of *observable future outcomes* but cannot, without stronger identification, claim what rejected work would have achieved under acceptance.

## Immediate stop rules

ABSTAIN or redesign if longitudinal coverage of non-selected work is inadequate, selection strongly determines observability without a defensible correction, temporal leakage persists, value becomes circular, conclusions depend on arbitrary construct choices, or adversarial review finds an unresolved fatal flaw.

## Public outputs

Research-commons artefacts may be released throughout feasibility: acquisition tooling, provenance, corpus manifests, matching methodology, leakage tests, feasibility reports, synthetic engineering fixtures and negative results. A journal manuscript is downstream of evidence, not a production target.

## References

- Lakkaraju, H. et al. (2017). *The Selective Labels Problem*. KDD. DOI: 10.1145/3097983.3098066.
- Settles, B. (2009). *Active Learning Literature Survey*. UW-Madison TR1648.
- Uzzi, B. et al. (2013). *Atypical Combinations and Scientific Impact*. Science 342(6157), 468–472.
- Fontana, M. et al. (2020). *New and atypical combinations: An assessment of novelty and interdisciplinarity*. Research Policy 49(7), 104063.
- Teplitskiy, M. et al. (2022). *Is novel research worth doing? Evidence from peer review at 49 journals*. PNAS 119(47), e2118046119.
- OpenReview. *Using the API*.
