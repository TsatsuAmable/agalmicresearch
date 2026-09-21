# Scarcity Migration and Validation-Cost Distortion

**Status:** exploratory mechanism note; not an empirical outcome  
**Date:** 2026-09-21  
**Programme:** Attention Allocation Under Cognitive Abundance  
**Effect on current Track A v0.2 gate:** none. The existing source-feasibility stop remains authoritative.

## Why this note exists

Recent 2026 evidence makes one part of the Agalmic problem more concrete: AI can increase upstream scientific throughput while downstream validation remains comparatively slow, expensive, capacity-constrained, or physically irreducible.

That observation does **not** by itself establish a novel Agalmic contribution. Evaluation bottlenecks, active learning, exploration/exploitation, queueing, constrained ranking, selective labels, and scientific topic-selection effects are established prior art.

The sharper candidate contribution is therefore:

> **scarcity migration plus allocation distortion**: when an upstream stage becomes abundant, binding scarcity can move into downstream validation resources; under pressure, allocation policies may then favor candidates that are cheaper, easier or more legible to validate rather than candidates with the highest latent epistemic value.

This is a falsifiable mechanism, not a premise.

## External evidence now relevant

### Codreanu et al. (2026), *AI in Science: Early Insights*

The Google / Google DeepMind / MIT FutureTech report combines roughly 15 million Gemini interactions, an inventory of 2,690 specialized scientific AI models, and a survey of 637 active US/UK researchers.

The survey reports:

- 43.5% said their primary research constraint shifted downstream over the prior two years;
- 40.5% said their backlog of untested hypotheses increased;
- among researchers reporting time savings, 89% spent more than 10% of those savings checking AI outputs and 46% spent more than 25%;
- 49% said AI encouraged safer, more incremental questions, compared with 28% who said it encouraged higher-risk questions.

The report explicitly warns that the scientist survey can suffer from selection bias and that the sample is too small to resolve important disciplinary heterogeneity. It also states that its results establish associations rather than causality.

Primary source: https://ai.google/static/documents/AI-in-Science.pdf

### Hao et al. (2026), *Artificial intelligence tools expand scientists’ impact but contract science’s focus*

Using 41.3 million natural-science papers, the study reports that AI-augmented researchers have higher individual publication and citation output while the collective volume of topics studied contracts by 4.63%. The authors also report movement toward data-rich areas.

This is consistent with a possible validation-cost or tractability bias, but it does not identify the mechanism causally.

DOI: https://doi.org/10.1038/s41586-025-09922-y

### Rana, Varshney & Varshney (2026), *AI-driven Acceleration and the Evaluation Bottleneck in Science*

This conceptual framework directly argues that AI can expand generative scientific capacity faster than institutions can evaluate, verify and contest claims. That substantially occupies the broad "AI creates an evaluation bottleneck" claim.

Agalmic Research therefore should not claim novelty for the bottleneck itself.

DOI: https://doi.org/10.2139/ssrn.7318643

## Formal mechanism

Let candidate (i) arrive with:

- latent epistemic value (V_i);
- observable features (x_i);
- uncertainty (u_i);
- novelty / unconventionality descriptors (n_i);
- validation-resource demand vector

[
c_i = (c_i^{human}, c_i^{compute}, c_i^{lab}, c_i^{capital}, c_i^{time}, ldots).
]

Let the available validation-capacity vector be

[
B = (B^{human}, B^{compute}, B^{lab}, B^{capital}, B^{time}, ldots).
]

Let candidate arrival rate be (lambda).

For each validation resource (k), define a provisional pressure coordinate

[
ho_k = \frac{\lambda E[c_i^k]}{B^k}.
]

The programme already uses the scalar pressure coordinate

[
ho = \frac{\lambda E[C]}{B}.
]

The vector form is a generalization for heterogeneous validation resources, not a replacement for the frozen Track A design.

A downstream resource becomes a candidate binding constraint as its (ho_k) approaches or exceeds sustainable capacity. If AI reduces upstream generation cost or increases (lambda) faster than it increases downstream (B^k), the identity of the binding constraint may move downstream.

Call that **scarcity migration**.

This is intentionally close to established queueing and production-bottleneck ideas. The empirical question is not whether bottlenecks can exist. It is whether abundance shocks measurably change which resource binds and whether that change alters which candidates receive validation.

## Allocation-distortion mechanism

Let an allocation policy estimate candidate value as (hat V_i) and choose candidates under a resource budget.

A simple cost-aware allocator might implicitly or explicitly prefer:

[
S_i = \hat V_i - \sum_k \alpha_k c_i^k
]

or a value-per-cost form such as

[
S_i = \frac{\hat V_i}{\epsilon + \sum_k \alpha_k c_i^k}.
]

As validation pressure rises, the effective shadow price (alpha_k) of scarce resources can rise.

That is not inherently irrational. Under hard budgets, cost sensitivity is often necessary.

The research risk appears when validation cost is correlated with properties such as novelty, weak benchmarkability, interdisciplinarity, minority status, unconventional methodology, long time-to-result, or physical experimentation. Then rational local allocation can produce a collective **streetlight effect** in which high-cost candidates are systematically under-tested.

The target phenomenon is therefore not merely "too many ideas". It is a possible change in the selection function.

## Candidate hypotheses

These hypotheses are **not yet preregistered** and must not be treated as Track A outcomes.

**H1: backlog response.** Holding validation capacity fixed, an exogenous increase in candidate arrival raises unresolved-candidate backlog once downstream utilization is sufficiently high.

**H2: scarcity migration.** Upstream acceleration changes the identity or relative shadow price of the binding resource toward downstream validation resources.

**H3: validation-cost tilt.** As validation pressure increases, selection probability becomes more negatively associated with expected validation cost, conditional on estimated value and uncertainty.

**H4: costly-novelty starvation.** If validation cost is positively correlated with novelty or weak benchmarkability, higher pressure disproportionately reduces selection of those candidates.

**H5: exploration protection.** Policies that reserve explicit exploration capacity can recover some high-cost or unconventional candidates while preserving acceptable realised epistemic value under equal total budgets.

**Null / falsifying possibilities:** no downstream shift; no pressure-dependent cost tilt; novelty and cost are uncorrelated; expensive candidates are not starved; exploration protection adds no value; or apparent effects disappear after field, institutional or measurement controls.

## What the current flagship experiment can and cannot test

Track A v0.2 should **not** be redesigned around this new mechanism while its source-feasibility gate is closed.

The current retrospective ICLR design is useful for testing allocation policies under scarce attention with temporal and observability controls. It is not presently equipped to identify an AI-driven abundance shock or real physical-validation cost.

Changing the frozen design now would destroy the very pre-outcome discipline the programme is trying to demonstrate.

The correct relationship is therefore:

1. keep Track A v0.2 unchanged and outcome-sealed;
2. treat scarcity migration as a new mechanism candidate supported by external evidence;
3. only after the current source gate resolves, decide whether a separate amendment or successor experiment can measure validation cost and pressure directly.

## Candidate successor experiment

A strong design would preserve the same candidate pool and total validation budget across conditions while varying candidate pressure or validation-resource availability.

Minimum structure:

- identical candidate distribution across conditions;
- prospectively defined validation-cost measurements, not post-hoc proxies chosen after outcomes;
- at least one condition with increased candidate arrival and fixed validation capacity;
- allocation policies compared under identical resource budgets;
- hidden or independently adjudicated outcome value where possible;
- explicit exploration policy alongside cost-efficient and value-ranked baselines;
- field / domain stratification because "wet" and "dry" sciences have structurally different validation costs.

Candidate outcomes:

- backlog size and age;
- resource utilization by validation dimension;
- probability of selection as a function of expected validation cost;
- high-value recall;
- false-negative loss;
- tail capture;
- candidate diversity / coverage;
- starvation rate for costly candidates;
- time-to-validation;
- cost-weighted regret against an oracle or delayed-ground-truth benchmark.

A synthetic harness may continue to test software invariants, but it cannot establish these claims.

## Novelty boundary

The following are **not** Agalmic novelty claims:

- AI can generate many hypotheses;
- downstream scientific validation can become a bottleneck;
- expensive labels should be allocated selectively;
- exploration/exploitation trade-offs exist;
- peer review or scientific topic choice can be biased;
- tractable or data-rich problems can receive disproportionate attention.

A plausible Agalmic contribution would require empirical evidence for a narrower conjunction:

> abundance changes the vector of binding validation constraints, and the resulting resource prices measurably alter candidate selection in ways that affect realised epistemic value and the survival of expensive-to-validate candidates.

Even that formulation must survive prior-art review.

## Decision for the programme

**Do not open a new active programme.** This mechanism belongs inside the existing Attention Allocation lineage.

**Do not reopen Track A v0.2 design choices.** Its current source gate remains binding.

**Do update the prior-art boundary.** The 2026 literature now makes the generic "evaluation bottleneck" claim too occupied to carry Agalmic novelty.

**Next discriminating move after the v0.2 source gate:** determine whether a prospectively measurable validation-cost / scarcity-pressure experiment is feasible. If not, retain scarcity migration as an explanatory hypothesis rather than promoting it to a research claim.
