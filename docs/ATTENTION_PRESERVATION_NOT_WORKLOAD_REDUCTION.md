# Attention Preservation Is Not Workload Reduction

**Research note — 11 September 2026**

## Claim

Machine-assisted triage should not be evaluated only by how much expert work it saves at a target recall. That objective is necessary in many domains, but it is not sufficient when the scarce resource is expert attention and the rejected set contains scientifically or operationally important disagreement, minority topics, rare failure modes, or candidates whose value is not well represented by historical labels.

A triage system can look efficient against an institutional target while becoming a new epistemic bottleneck.

## Why this note exists

Active-learning systems for systematic-review screening have established that large workload reductions are possible while retaining high recall. Recent work continues to report strong Work Saved over Sampling (WSS) results, including simulations that retain 95% recall while reducing screening effort substantially. Learning-to-defer research similarly studies how machines can allocate cases between models and human experts when expert predictions are costly.

These are genuine advances. The unresolved question is different:

> What should be preserved when the historical target itself is an incomplete proxy for what deserves scarce expert attention?

Agalmic Research's Phase-1 expert-attention audit gives a concrete failure case for single-objective triage evaluation.

## Empirical diagnostic

The audit uses the public Berenslab ICLR `25v2` dataset, restricted to 2020–2025.

- 33,043 submissions with interpretable final decisions
- 32,604 submissions with parsed reviewer scores
- 17,983 submissions with non-unlabeled topic assignments
- dataset SHA-256: `48215679d54ea788b8dfc1177850845f047c5810554708273b617b67ce321859`

Reviewer scores and final decisions are post-review outcomes and are **not** admissible inputs to a deployable pre-review triage system. They are used only to construct intentionally leaky diagnostic policies.

At a 20% expert-attention budget:

| Policy | Accepted-paper recall | High-disagreement recall | Worst-topic recall |
| --- | ---: | ---: | ---: |
| Random allocation | 20.0% | 19.9% | 13.8% |
| Raw reviewer-score ranking | 60.8% | 10.0% | 11.3% |
| Topic-normalized score ranking | 60.2% | 10.0% | 16.5% |

The apparent winner depends entirely on what is measured.

If the objective is preserving historical acceptance, score ranking is dramatically better than random allocation. If the objective includes retaining contested cases, it is dramatically worse. Topic normalization repairs much of the worst-topic loss without materially changing accepted-paper recall, but it does not repair disagreement loss.

Across sufficiently populated score/year/topic cells, the largest observed topic-to-topic acceptance-rate spread at approximately the same mean reviewer score is 36.6 percentage points. This does not prove topic bias. It does show that global score comparability is unsafe as an assumption.

## Relation to prior art

This note does **not** claim that machine-assisted screening, selective prediction, learning to defer, or workload-aware routing are new.

Relevant prior work includes:

1. **Active learning for systematic reviews.** Teijema et al. (2023) evaluate active-learning models using recall, WSS and Average Time to Discovery, with WSS@95 ranging from 63.9% to 91.7% across six datasets.
2. **WSS as an evaluation measure.** Kusa et al. analyze Work Saved over Sampling and show how normalized WSS relates to true-negative rate, improving comparability across review datasets.
3. **Recent systematic-review screening systems.** Contemporary evaluations continue to report substantial screening reductions at high recall, including 2026 studies using ASReview and ensemble approaches.
4. **Learning to defer.** Hemmer et al. (2023) explicitly address situations where expert predictions are costly and show that deferral systems can be trained with limited expert labels.

The proposed contribution is narrower: **a preservation-oriented evaluation layer for scarce expert-attention allocation**.

## The distinction

Workload-reduction metrics ask:

> How much expert labor can be avoided while retaining enough target positives?

Attention-preservation metrics additionally ask:

> Which classes of candidate disappear when attention is compressed, and are those losses acceptable?

These questions coincide only when the target label is a sufficient representation of value.

That condition should be demonstrated rather than assumed.

## Minimum preservation vector

For an attention-routing benchmark, report at least:

[
P(B) = (R_T, R_D, R_S, A_R)
]

where, at budget (B):

- (R_T): recall of the conventional target;
- (R_D): recall of disagreement-rich or uncertainty-rich cases;
- (R_S): worst-stratum recall across preregistered groups or evidence classes;
- (A_R): reject-audit discovery rate from a randomized sample of skipped cases.

The exact strata depend on the domain. In scientific review they may be topic, methodology, institution, novelty class, or reviewer disagreement. In engineering they may be hardware-only failures, modality, subsystem, evidence class, or rare cross-layer faults.

A scalar utility can still be used later, but the preservation vector should remain visible. Collapsing it too early hides trade-offs.

## Randomized reject auditing

The hardest quantity in a triage system is the false negative that is never examined.

A small randomized audit channel should therefore remain outside the learned or heuristic router. Some candidates the system would reject are still sent to expert review. This produces an estimate of hidden misses and makes the rejection boundary observable over time.

Without reject auditing, a mature triage system can become self-confirming: it sees only the cases it chooses to see, retrains on those cases, and gradually loses evidence about the counterfactual rejected population.

## Novelty boundary

The current evidence supports the following claim:

> In expert-attention allocation, optimizing historical-target recall or workload reduction alone can conceal large losses in disagreement-rich and stratum-specific cases. Preservation metrics and reject auditing are therefore necessary evaluation dimensions whenever the target label is an imperfect proxy for what deserves expert consideration.

The evidence does **not** yet support these stronger claims:

- high-disagreement papers are intrinsically better;
- rejected papers are systematically undervalued;
- topic normalization is a generally correct allocation policy;
- the proposed preservation vector is uniquely optimal;
- a learned router is superior to simple stratified allocation;
- later citations or publication outcomes constitute ground truth scientific value.

Those remain empirical questions.

## Next falsifiable experiment

The next phase should avoid post-review leakage entirely.

Build temporal pre-review baselines using only information available before review:

1. random allocation;
2. topic-stratified quotas;
3. TF-IDF + logistic regression;
4. calibrated embedding-based ranking;
5. only after these, structured claim/evidence representations.

Evaluate each across fixed attention budgets using both conventional recall and the preservation vector. Maintain randomized reject auditing. A bespoke model earns complexity only if it improves preservation beyond simple calibrated and stratified baselines.

## Transfer beyond peer review

The same problem appears anywhere high-fidelity attention is scarce.

For XR engineering, cheap evidence may include unit tests, browser smoke tests and simulation, while scarce evidence includes physical headset runs and human UX judgment. A router that maximizes green CI throughput can still suppress hardware-only or modality-specific failures. The allocator should decide **where to measure next**, not decide truth.

The general pattern is:

**abundant cheap evidence → triage → scarce high-fidelity measurement → randomized reject audit → recalibration**

This is a scarcity-displacement mechanism only if the compression preserves access to consequential exceptions.

## Reproducibility

Executable analysis and retained outputs:

- `research/expert_attention/iclr_preservation_audit.py`
- `research/expert_attention/results/iclr25v2_2020_2025/manifest.json`
- `research/expert_attention/results/iclr25v2_2020_2025/preservation_frontier.csv`
- `research/expert_attention/results/iclr25v2_2020_2025/report.md`

The raw public dataset is not redistributed. The manifest records the exact source URL, parameters, seed and SHA-256 digest.

## Sources

- Teijema JJ et al. *Performance of active learning models for screening prioritization in systematic reviews: a simulation study into the Average Time to Discover relevant records.* Systematic Reviews. 2023. https://doi.org/10.1186/s13643-023-02257-7
- Kusa W, Lipani A, Knoth P, Hanbury A. *An Analysis of Work Saved over Sampling in the Evaluation of Automated Citation Screening in Systematic Literature Reviews.* Intelligent Systems with Applications. https://doi.org/10.1016/j.iswa.2023.200193
- Hemmer P, Thede L, Vössing M, Jakubik J, Kühl N. *Learning to Defer with Limited Expert Predictions.* AAAI 2023. https://doi.org/10.1609/aaai.v37i5.25742
- Teijema JJ et al. *Simulation-based active learning for systematic reviews: A scoping review of literature.* Journal of Information Science. First published 17 December 2025. https://doi.org/10.1177/01655515251379058
- van der Valk et al. *To include or not to include? A prescription from the pharmacy on how to use active learning-assisted screening in systematic reviews.* Systematic Reviews. 2026. PMID 42015233.
