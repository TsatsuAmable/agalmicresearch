# Expert-Attention Triage Validity Benchmark

Version: 0.1  
Status: research design / benchmark specification  
Date: 10 September 2026  
Extends: `HANDOFF_RETROSPECTIVE_STUDY_PROTOCOL.md`

## Core question

When expert attention is scarce, can a machine-assisted triage system reduce review load while preserving candidates that are valuable, difficult, controversial, novel, or poorly served by historical review conventions?

This benchmark deliberately does **not** treat historical accept/reject decisions or raw reviewer scores as ground truth. Its purpose is to test whether a routing policy can allocate scarce expert attention without merely learning to reproduce past gatekeeping.

## Prior-art boundary

The generic mechanism is not novel. Relevant established lines include:

- selective prediction / reject-option systems;
- learning-to-defer (L2D) from machine predictors to one or more human experts;
- active-learning screening such as ASReview, including workload metrics such as WSS@95;
- reviewer assignment and expertise matching;
- AI-assisted peer-review and editorial triage;
- capacity-constrained expert routing and online learning-to-defer.

Therefore Agalmic Research should not claim novelty for "AI triage", "AI pre-screening", "routing uncertain cases to experts", or "reducing reviewer workload".

A potentially original contribution would instead need to combine and validate elements that existing work usually treats separately:

1. scarce and varying expert capacity;
2. selective observation of expert labels because only routed candidates are reviewed;
3. topic-dependent and reviewer-dependent measurement scales;
4. preservation of disagreement, heterodoxy, and later-recognised value;
5. robustness to superficial rewriting or strategic manipulation;
6. explicit reject auditing so false negatives remain observable;
7. evaluation against multiple imperfect outcome proxies rather than a single historical decision label.

Novelty is provisional until a systematic literature search confirms that this combination has not already been operationalised.

## Why acceptance prediction is the wrong primary task

Acceptance is an institutional outcome, not an epistemic truth label. A high-performing acceptance predictor may simply recover prevailing topical priors, scoring cultures, prestige signals, or stylistic conventions.

Recent ICLR analysis reports that, at the same reviewer score, acceptance probability varies sharply across topics, making raw scores non-comparable across research areas. This is a direct threat to any benchmark that rewards reproduction of historical decisions without stratification or calibration.

Similarly, reviewer disagreement is substantial in open-review corpora. A triage system that preferentially discards high-disagreement candidates may appear accurate while eliminating exactly the cases for which additional expert attention is most informative.

## Threat model

A useful triage system must survive at least five failure modes.

### 1. Gatekeeping mimicry

The system learns historical accept/reject decisions and therefore reproduces historical biases, topical priors, and blind spots.

### 2. False-negative invisibility

Candidates denied review generate no expert labels, so the system can become increasingly confident while losing the ability to observe its own misses.

### 3. Calibration failure

Confidence or uncertainty is not comparable across topics, candidate types, or subpopulations. Selective prediction can therefore worsen outcomes even when the underlying classifier appears strong.

### 4. Strategic manipulation

Authors adapt wording, formatting, abstracts, or prompt-injection-like content to increase the chance of expert escalation or favorable automated assessment without improving the underlying contribution.

### 5. Attention congestion

Even correct deferrals can fail operationally if too many candidates are routed to the same scarce expertise. Routing quality must therefore include capacity and queueing effects, not only classification error.

## Benchmark object

For each candidate research artefact i, define a pre-review feature set X_i available at the simulated routing moment. Post-review information is hidden from the router and retained only for evaluation.

The router chooses one of:

- `NO_ESCALATION`
- `GENERAL_EXPERT_REVIEW`
- `SPECIALIST_REVIEW:<class>` where data permits
- `AUDIT_SAMPLE` for randomized reject auditing

The first benchmark release should validate only the binary question `expert attention vs no expert attention`. Specialist routing should be reported separately unless the dataset exposes defensible expertise labels.

## Data substrates

### Primary contemporary corpus

Use the public ICLR OpenReview corpus, preferably 2020-2025 for completed decisions, with 2026 held out until decision completeness is verified. A public May 2026 dump contains 50,106 papers and 201,658 official reviews across ICLR 2020-2026, which is sufficient for topic-stratified and temporal evaluation.

A second useful public derivative corpus labels ICLR abstracts into 40+ topic classes and reports low-to-moderate same-paper reviewer-score correlation, providing a convenient substrate for topic-stratified analysis.

### Compact feasibility corpus

PeerRead remains useful for pipeline validation because it provides more than 14,000 paper drafts, accept/reject decisions, and more than 10,000 textual peer reviews. It should not be the sole evidential basis because it is older and mixes venue-specific collection regimes.

### Downstream linkage

Use OpenAlex only as a secondary linkage source for later citation and topic trajectories. Citation outcomes must be field- and age-normalized and must not be treated as ground truth.

## Outcome families

No single outcome is sufficient. Report each separately and, only secondarily, construct composite measures.

### A. Immediate institutional outcomes

- accept/reject decision;
- mean reviewer score after within-topic/year normalization;
- meta-review recommendation where available;
- reviewer confidence;
- reviewer-score dispersion / disagreement.

### B. Later-recognition outcomes

- field- and age-normalized citation percentile;
- later publication in another venue where reliable matching exists;
- delayed citation acceleration;
- later related-work centrality where measurable;
- correction or retraction status as a negative signal where applicable.

### C. Information-value outcomes

These attempt to measure when expert review is especially informative rather than merely favorable:

- high reviewer disagreement;
- large divergence between initial reviews and meta-review/final decision;
- low reviewer confidence;
- cross-topic or interdisciplinary placement;
- strong sensitivity of outcome to reviewer assignment, where estimable.

These are proxies for "review value", not intrinsic scientific value.

## Primary benchmark metrics

### 1. Review Work Saved at Preservation r: RWS@r

Adapt the logic of WSS@95 from active-learning screening.

For a specified preservation target r (for example 0.95), measure the fraction of expert-review slots avoided while retaining at least r of candidates satisfying a predefined value proxy.

Report RWS@95 separately for each value proxy. Do not collapse citation, acceptance, and disagreement into one label.

### 2. Preservation frontier

For review-budget fractions B/N in {0.05, 0.10, 0.20, 0.40, 0.60, 0.80, 1.00}, report recall of:

- accepted candidates;
- topic-normalized high-score candidates;
- high-disagreement candidates;
- later highly cited candidates;
- delayed-recognition candidates, if available.

The full curves are the result. A single operating point is insufficient.

### 3. Counter-Gatekeeping Recall (CGR)

Define a candidate as `counter_gatekeeping_positive` under a preregistered proxy when it received an unfavorable immediate institutional outcome but later achieved a strong downstream signal, for example a high field/age-normalized citation percentile or later publication/recognition.

CGR = routed counter-gatekeeping positives / all counter-gatekeeping positives.

This metric tests whether the triage system systematically suppresses candidates that historical review underestimated. It is deliberately conservative because downstream recognition is also biased and noisy.

### 4. Dissent Preservation Rate (DPR)

Among candidates in the top q percentile of reviewer disagreement, report the fraction escalated for expert attention at each budget.

A system that improves average acceptance prediction while sharply lowering DPR should be treated as suspect rather than superior.

### 5. Topic-Conditional Preservation Gap (TCPG)

For each topic t and value proxy V:

`gap_t = recall_V,t - recall_V,overall`

Report the worst absolute gap and distribution of gaps. Primary comparisons should use topic/year-normalized signals rather than raw reviewer scores.

### 6. Reject-Audit Discovery Rate (RADR)

Randomly escalate a fixed fraction a of candidates the router would otherwise reject. Measure the fraction of audited rejects that satisfy each value proxy.

This creates a continuing empirical estimate of hidden false negatives and is mandatory for any prospective deployment.

### 7. Rewrite Sensitivity

Generate semantics-preserving surface variants of a preregistered sample: copy edit, reordered abstract, fluency improvement, formatting perturbation, and adversarially optimized wording. Measure routing-decision flip rate and score movement.

A 2026 study reports that superficial abstract rewriting can materially improve AI peer-review scores without changing scientific content. A triage system intended to allocate scarce expert attention must therefore be evaluated against this attack class.

## Capacity-aware evaluation

Static deferral metrics assume that expert review is immediately available. Real scarcity creates queues.

For a simulated expert pool j with capacity C_j(t), define routing utility over a horizon as a function of:

- value proxy preserved;
- expert slots consumed;
- delay to review;
- overload / queue growth;
- false-negative cost;
- audit cost.

At minimum compare:

1. fixed threshold routing;
2. top-k ranking under a global budget;
3. topic-stratified quota or calibrated ranking;
4. uncertainty-based deferral;
5. the proposed claim-sensitive handoff mechanism;
6. random allocation;
7. oracle ranking for each evaluation proxy as an unattainable ceiling.

Learning-to-defer work with varying experts and content-moderation queueing shows that expert availability and congestion are first-class parts of the problem. Agalmic evaluation should therefore avoid assuming a fixed, frictionless human oracle.

## Mandatory leakage controls

The router must never receive information created after the simulated routing decision. In particular exclude:

- review text;
- reviewer scores;
- meta-reviews;
- decision labels;
- later citation counts;
- post-submission revised text if revision followed reviewer feedback.

Temporal splits are preferred: train on earlier years, evaluate on later years. Random paper splits should be secondary because topical and stylistic leakage can make the problem artificially easy.

## Benchmark phases

### Phase 1: descriptive audit

Before training any triage model:

- reproduce paper/review counts by year;
- quantify missingness;
- calculate per-topic acceptance rates;
- calculate per-topic score distributions;
- estimate reviewer disagreement;
- quantify how much raw scores fail cross-topic comparability;
- define which downstream links can be made reproducibly.

### Phase 2: intentionally weak baselines

Run random routing, abstract-length/format heuristics, and global mean-score predictors only to establish floors and expose leakage.

### Phase 3: strong conventional baselines

Use simple text embeddings plus logistic/ranking models, topic-stratified calibration, and uncertainty-based deferral. The special Agalmic mechanism earns no credit unless it beats these.

### Phase 4: handoff representation

Add only pre-review claim/evidence/deficit descriptors:

- principal claim;
- evidence type;
- unresolved epistemic deficit;
- requested review function;
- uncertainty;
- estimated need for specialist attention.

Ablate each component. If gains vanish after topic calibration or can be reproduced by a simpler embedding model, retire the special machinery.

### Phase 5: adversarial and reject-audit simulation

Run rewrite perturbations and simulated random reject audits. Measure whether audit discoveries would update thresholds or model calibration.

## What would count as an original contribution?

A credible contribution is not "an LLM that predicts whether a paper deserves review".

A stronger candidate contribution would be an **expert-attention preservation benchmark** showing how to evaluate triage systems when expert labels are capacity-limited, selectively observed, topic-incomparable, and institutionally biased, with explicit metrics for later-recognised false negatives, dissent preservation, reject auditing, and manipulation robustness.

An even stronger contribution would be empirical evidence that a specific claim-sensitive handoff representation improves this benchmark out of sample, especially at low review budgets, without worsening topic-conditional preservation or counter-gatekeeping recall.

A negative result would still be useful: if simple calibrated embeddings plus reject auditing match the claim-sensitive mechanism, the benchmark itself may be the contribution and the special handoff formalism should be simplified.

## Falsification criteria

Do not advance the mechanism as distinctive if any of the following hold:

- gains disappear under temporal or cross-year validation;
- gains are explained by topic or stylistic proxies;
- the mechanism improves acceptance recall but worsens counter-gatekeeping recall or dissent preservation;
- rewrite sensitivity is high;
- calibration fails for minority topics;
- random reject auditing finds an unacceptably high hidden-value rate;
- simple calibrated baselines perform equivalently within uncertainty;
- downstream outcome linkage is too incomplete or biased to support the claimed inference.

## Immediate executable analysis

The next script should consume an ICLR paper table with at least:

`paper_id, year, topic, decision, reviewer_scores[]`

and produce:

1. counts and missingness;
2. topic/year acceptance rates;
3. topic/year score normalization;
4. reviewer disagreement distribution;
5. score-conditional acceptance rates by topic;
6. simulated random-routing preservation frontiers;
7. a data-quality report identifying which planned metrics are currently adjudicable.

Only after this descriptive layer is frozen should model development begin.

## Selected prior art

- Mozannar H, Sontag D. Consistent Estimators for Learning to Defer to an Expert. ICML 2020. https://proceedings.mlr.press/v119/mozannar20b.html
- Charusaie M-A et al. Sample Efficient Learning of Predictors that Complement Humans. ICML 2022. https://proceedings.mlr.press/v162/charusaie22a.html
- Verma R, Barrejon D, Nalisnick E. Learning to Defer to Multiple Experts. AISTATS 2023. https://proceedings.mlr.press/v206/verma23a.html
- Tailor D et al. Learning to Defer to a Population. AISTATS 2024. https://proceedings.mlr.press/v238/tailor24a.html
- Lykouris T, Weng W. Learning to Defer in Content Moderation: The Human-AI Interplay. 2024. https://arxiv.org/abs/2402.12237
- OpenL2D / FiFAR benchmark. Scientific Data 2025. https://www.nature.com/articles/s41597-025-04664-y
- Montreuil Y et al. Adversarial Robustness in Two-Stage Learning-to-Defer. ICML 2025. https://proceedings.mlr.press/v267/montreuil25a.html
- Montreuil Y et al. Online Learning-to-Defer with Varying Experts. AISTATS 2026. https://proceedings.mlr.press/v300/montreuil26b.html
- van de Schoot R et al. ASReview: open-source machine learning for efficient and transparent systematic reviews. Nature Machine Intelligence 2021. https://www.nature.com/articles/s42256-020-00287-7
- Thakkar N et al. A large-scale randomized study of large language model feedback in peer review. Nature Machine Intelligence 2026. https://www.nature.com/articles/s42256-026-01188-x
- Xu B et al. Reviewer Scores Are Not Comparable Across Research Areas in ML Peer Review. 2026. https://arxiv.org/abs/2607.27209
- Li L et al. Gaming AI-Assisted Peer Reviews Poses New Risks to the Scientific Community. 2026. https://arxiv.org/abs/2606.10159
- Kang D et al. PeerRead. NAACL 2018. https://aclanthology.org/N18-1149/
- ICLR 2020-2026 public OpenReview dump snapshot, May 2026. https://github.com/qhjqhj00/iclr-openreview-reviews/releases

## Research claim discipline

The benchmark should be described as a proposed operationalization of scarce expert-attention preservation, not as a validated measure of scientific worth. Its strongest purpose is diagnostic: to make visible which candidates, topics, and forms of disagreement are lost when a system tries to save expert attention.