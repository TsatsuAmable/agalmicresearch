# Retrospective Study Protocol: Expert-Attention Handoff Triage

Version: 0.1  
Status: proposed executable study  
Date: 9 September 2026

## Research question

When candidate research output exceeds available expert-review capacity, can a claim-sensitive routing policy allocate review more efficiently than simpler baselines while preserving valuable or controversial candidates?

The study does **not** ask whether an LLM can mimic expert acceptance decisions. It asks whether scarce expert attention can be allocated with higher epistemic yield under explicit false-negative constraints.

## Why retrospective first

A one-human research programme should not consume new expert attention before extracting information from expert attention already spent.

Historical peer-review datasets provide candidate papers, reviews, reviewer confidence/ratings in some venues, meta-reviews and decisions. They allow simulated scarcity experiments before any prospective recruitment.

Initial substrates:

- PeerRead for a compact reproducible benchmark;
- public OpenReview venues for a larger and more contemporary replication/extension where visibility permits;
- OpenAlex for downstream citation/topic metadata after careful entity matching.

## Unit of analysis

A submitted research paper or other candidate research object at the moment before expert evaluation.

The model/filter must not receive information created after the simulated routing decision.

## Simulated review budget

Let a venue contain N candidates and let B be the number of candidates that scarce experts can review.

Run the experiment across budget ratios such as:

- B/N = 0.05
- 0.10
- 0.20
- 0.40
- 0.60
- 0.80
- 1.00

The purpose is an **expert-attention efficiency frontier**, not a single arbitrary threshold.

## Baselines

At minimum compare:

1. random allocation;
2. simple rule-based triage using pre-review features;
3. conventional predictive/model ranking;
4. claim-sensitive handoff triage with explicit uncertainty/deferral;
5. oracle / full review as a ceiling where appropriate.

Do not allow the proposed mechanism to win merely by comparing it with a weak baseline.

## Candidate inputs

Use only pre-review information available for the historical candidate, such as:

- title;
- abstract;
- manuscript text where legally/publicly available;
- declared field/topic;
- references / lineage features;
- methodological descriptors;
- claim/evidence structure derived without using reviews;
- uncertainty or missing-capability descriptors generated from the candidate itself.

Author identity, institution and prestige signals should be excluded from the primary condition and introduced separately as a bias/sensitivity experiment where the data permits.

## Outcomes

No single historical label is epistemic truth. Report several outcomes separately.

### Immediate review outcomes

- expert rating / recommendation where available;
- accept/reject decision;
- reviewer confidence;
- reviewer disagreement;
- meta-review assessment;
- review text-derived strengths / weaknesses only with validated extraction methods.

### Downstream proxies

Where matching is reliable:

- publication outcome;
- citation trajectory normalized within field/time;
- later correction/retraction status where relevant;
- sustained vs transient citation uptake;
- later related-work recognition.

These remain proxies, not ground truth.

## Primary metrics

### Valuable-candidate recall

For each operational definition of value V:

Recall_V = valuable candidates escalated / all valuable candidates

Report this across budgets rather than hiding the trade-off in one threshold.

### Expert yield

Expert Yield = useful reviewed candidates / review slots consumed

Where expert-time estimates are available, replace slots with time.

### False-negative burden

Report both count and weighted burden of candidates screened out that later satisfy the chosen value proxy.

### Controversy preservation

Measure whether candidates with high reviewer disagreement are disproportionately removed by triage.

### Calibration / selective risk

When the mechanism expresses uncertainty, test whether lower-confidence decisions are actually less reliable and whether deferral improves performance.

## Mandatory reject audit

Any prospective version of the mechanism must randomly escalate a sample of candidates it would reject. The retrospective study should simulate this.

Purpose:

- estimate false negatives;
- detect distribution shift;
- prevent a gatekeeper from becoming unobservable precisely where it is most dangerous.

## Bias and robustness tests

Where feasible:

- add/remove author and institution signals;
- compare semantically equivalent rewrites;
- perturb formatting and fluency;
- stratify by field/topic;
- stratify by submission quality / reviewer disagreement;
- compare older vs newer venues;
- test sensitivity to different definitions of downstream value;
- bootstrap candidate sets and budget allocations.

## Handoff-specific mechanism

The proposed mechanism differs from ordinary ranking by representing an **epistemic deficit** and requested next function.

For each candidate, attempt to infer or encode:

- current claim state;
- principal claims;
- supporting evidence type;
- uncertainty / unresolved deficit;
- required epistemic function, e.g. domain review, statistical review, formal verification, replication, lineage search;
- confidence that expert escalation is necessary;
- suggested recipient class.

The historical dataset may not expose the true routing target. The first retrospective study should therefore separate two questions:

1. **Should this candidate consume expert attention?**
2. **What kind of expertise should receive it?**

Do not pretend to validate the second question if the dataset cannot adjudicate it.

## Study phases

### Phase 0 — reproducibility and rights audit

- verify source licenses and public visibility;
- select one small reproducible corpus;
- define legal/ethical boundaries for manuscript/review text processing;
- freeze dataset version and extraction script;
- create a data dictionary.

### Phase 1 — descriptive baseline

- candidate counts;
- decision rates;
- review counts;
- missingness;
- score/confidence distributions;
- disagreement;
- temporal / venue heterogeneity.

No model before the data-generating process is understood.

### Phase 2 — scarcity simulation

- impose budget ratios;
- run random and simple baselines;
- produce attention-efficiency frontiers.

### Phase 3 — model triage

- build a conventional predictive baseline;
- evaluate out-of-sample and preferably cross-venue / cross-year.

### Phase 4 — handoff triage

- add claim-sensitive deficit representation and selective deferral;
- compare incrementally with the predictive baseline;
- quantify whether the additional machinery earns its cost.

### Phase 5 — downstream linkage

- match candidates to OpenAlex only with documented matching confidence;
- introduce downstream outcomes as secondary analyses;
- report failures to match and sensitivity to linkage rules.

### Phase 6 — external validation decision

Only if retrospective evidence shows a credible delta should Agalmic Research seek scarce expert participation for a small prospective validation.

## Stop / retire conditions

Retire the special handoff formalism, or reduce it to a simpler implementation, if:

- simple rules perform equivalently within uncertainty;
- conventional model ranking captures the full practical gain;
- gains depend mainly on prestige/credential features;
- false-negative burden is unacceptable;
- results collapse out of sample;
- historical labels are too weak to adjudicate the proposed contribution;
- the extra claim-state machinery cannot be measured reliably.

A negative result is a successful study outcome.

## Immediate next actions

1. Use PeerRead as the small feasibility corpus.
2. Build a source/data dictionary and confirm exactly which pre-review and review fields exist.
3. Reproduce basic dataset counts from the original paper.
4. Define three outcome families before model development: decision, disagreement, downstream proxy.
5. Implement random and simple baselines first.
6. Produce the first review-budget frontier.
7. Decide from that evidence whether contemporary OpenReview replication is warranted.

## Sources

- Kang et al. (2018), PeerRead, ACL Anthology: https://aclanthology.org/N18-1149/
- OpenReview data retrieval documentation: https://docs.openreview.net/how-to-guides/data-retrieval-and-modification/how-to-get-all-notes-for-submissions-reviews-rebuttals-etc
- OpenAlex works/data documentation: https://help.openalex.org/data/works/
- OpenAlex public snapshot: https://help.openalex.org/access/snapshot/
