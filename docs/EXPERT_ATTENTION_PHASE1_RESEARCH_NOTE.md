# Phase 1 Research Note: Preserving Value Under Expert-Attention Scarcity

Status: preregistered descriptive analysis note  
Date: 10 September 2026  
Related benchmark: `EXPERT_ATTENTION_TRIAGE_VALIDITY_BENCHMARK.md`

## Research question

When expert review capacity is scarce, which allocation rules preserve useful scientific candidates without simply reproducing the historical acceptance boundary?

The immediate empirical target is deliberately narrower than a general theory of scientific value. We first ask whether familiar institutional proxies already contain failure modes that make naive automated triage unsafe: cross-topic score incomparability, loss of reviewer disagreement, and unequal topic preservation at low review budgets.

## Prior-art correction

The generic idea of machine-assisted triage is not an Agalmic Research contribution. Learning-to-defer, selective prediction, active-learning screening, reviewer assignment, and capacity-constrained human-AI routing already provide substantial machinery for deciding when a machine should defer to people.

Likewise, the claim that review scores can behave differently across research areas is now directly studied. Xu et al. (2026) report ICLR 2021–2026 evidence that acceptance probability at a fixed reviewer score can differ sharply by topic. Existing public analyses of ICLR data also find the largest area differences near the decision boundary rather than at score extremes.

The contribution under test is therefore a preservation-oriented evaluation regime, not a new triage algorithm.

## Candidate contribution

A defensible contribution would be a benchmark for scarce expert-attention allocation that treats expert labels as costly and selectively observed, institutional outcomes as imperfect proxies, and false negatives as first-class objects of study.

The distinctive combination currently under test is:

1. preservation curves across explicit attention budgets;
2. Dissent Preservation Rate for high reviewer disagreement;
3. topic-conditional preservation gaps;
4. Counter-Gatekeeping Recall using later-recognition proxies;
5. randomized reject auditing to keep false negatives observable;
6. rewrite/adversarial sensitivity;
7. capacity and queue-aware evaluation;
8. comparison against simple calibrated baselines before any special handoff representation receives credit.

No novelty claim should be made until a systematic literature search tests whether this combination has already been operationalized.

## Dataset decision

Phase 1 uses the public Berenslab ICLR dataset rather than beginning with the much larger raw OpenReview dump. The current public dataset contains ICLR submissions, decisions, lists of reviewer scores, keywords, and non-overlapping topic labels derived from author keywords. Its 2024v2 release reports 24,445 submissions from 2017–2024, 45 topic classes with 53.4% labeled papers, an average 3.7 reviews among reviewed submissions, and same-paper reviewer-score correlation of 0.40.

This is sufficient for the first measurement audit. Raw OpenReview notes remain the later validation source when finer-grained review or decision metadata is needed.

## Preregistered descriptive hypotheses

These hypotheses are diagnostic, not claims of causation.

### H1: Score-conditional topic heterogeneity

Within at least some year/mean-score cells near the decision boundary, acceptance rates differ materially across topic classes.

Evidence against H1: topic-conditional acceptance spreads are small and unstable once minimum cell sizes and year stratification are imposed.

### H2: Score-prioritized allocation under-preserves dissent

At low expert-attention budgets, a policy that preferentially allocates attention to high historical reviewer scores preserves historically accepted papers better than random allocation but preserves high-disagreement papers worse than its accepted-paper advantage would suggest.

Evidence against H2: high-disagreement recall tracks or exceeds accepted-paper recall under score-prioritized allocation.

### H3: Global score ranking creates topic preservation gaps

At fixed review budgets, global raw-score ranking produces a lower worst-topic recall than a within-topic/year normalized score ranking.

Evidence against H3: topic normalization does not materially reduce the worst-topic gap, or any reduction is explained by very small topic cells.

### H4: A single efficiency number is insufficient

Policies with similar accepted-paper recall differ materially in high-disagreement recall and/or worst-topic recall.

Evidence against H4: policy rankings are effectively invariant across all preservation outcomes.

## Leakage rule

Reviewer scores and final decisions occur after review. They may appear only as evaluation outcomes or deliberately leaky diagnostic policies in Phase 1. They are prohibited as inputs to a deployable pre-review router.

The first actual routing model must use only information available before review, such as title, abstract, keywords/topic, and preregistered claim/evidence descriptors. Evaluation should use temporal splits.

## Executable analysis

`research/expert_attention/iclr_preservation_audit.py` downloads a versioned Berenslab Parquet snapshot, hashes the bytes, infers the relevant schema, normalizes decisions and score lists, and produces:

- yearly summary statistics;
- topic/year summary statistics;
- score-conditional topic acceptance spreads;
- preservation frontiers for random routing;
- intentionally leaky raw-score and topic-normalized-score diagnostic frontiers;
- a manifest that records the exact dataset digest and parameters;
- a Markdown report suitable for review or later publication notes.

The script was syntax-compiled before being added to the repository. Full empirical execution requires network access to the public Parquet asset and the `pandas`, `numpy`, `requests`, and `pyarrow` dependencies.

## Stop conditions

Do not proceed to a bespoke handoff model if the descriptive audit shows no meaningful preservation conflict, or if simple topic/year calibration resolves the apparent problem.

Do not claim a scientific-value benchmark if downstream proxies such as citations or later publication cannot be linked with acceptable coverage and field/age normalization.

Do not claim the proposed handoff representation is distinctive if simple text embeddings plus calibration and randomized reject auditing match it within uncertainty.

## Why this matters for Agalmic Research

The relevant scarcity is not merely the number of available experts. It is the amount of expert cognition that can be allocated without making the allocation mechanism itself an epistemic bottleneck.

An attention-saving system that routes only what existing institutions already recognize efficiently displaces labor while preserving scarcity in a more dangerous form: access to consideration. The benchmark therefore treats preserved access to potentially worthwhile futures as a constraint on efficiency rather than assuming that workload reduction is sufficient.

## Immediate next action after the data run

If H1–H4 survive, construct the weakest possible pre-review baselines first: random routing, topic quotas, TF-IDF/logistic ranking, and calibrated embedding models. Only then test whether structured claim/evidence/deficit representations buy additional preservation at the same expert-attention budget.
