# Prior Art Review: Expert-Attention Handoff Triage

Version: 0.1  
Status: working research note / novelty boundary  
Date: 9 September 2026

## Question

Is there a defensible research contribution in formalizing and testing a mechanism that pre-filters machine-assisted or low-authority candidate ideas before scarce domain experts are asked to evaluate them?

## Bottom line

**The generic mechanism is established. The narrower evaluation problem remains worth formalizing and testing.**

Prior work already establishes that:

- expert evaluation is scarce, expensive and difficult to scale;
- machine and crowd screening can reduce expert workload;
- selective prediction and learning-to-defer formalize when automated systems should abstain or escalate to humans;
- active learning studies how to spend scarce labeling or expert-query budgets;
- editorial triage and peer review already use pre-screening to protect reviewer capacity;
- idea-screening systems can learn to eliminate low-potential candidates or imitate expert rankings;
- value-of-information methods formalize whether additional information or research is worth acquiring.

Agalmic Research therefore should **not** claim to invent triage, expert escalation, AI-assisted screening, learning to defer, active learning, or the scarcity of expert attention.

The remaining opportunity is narrower:

> **Can a claim-sensitive handoff policy allocate scarce expert attention to candidate knowledge so that expert time produces more useful epistemic state change, while controlling false negatives, resisting prestige and presentation bias, preserving provenance, and never allowing triage itself to manufacture epistemic authority?**

This is not yet shown to be novel. It is a researchable synthesis and operationalization opportunity whose distinct contribution must survive comparison with adjacent literatures.

## Closest antecedent families

### 1. AI-assisted idea screening

Bell, Kavadias and Sommer (2023) study 4,191 ideas from 21 crowdsourcing contests and explicitly motivate AI screening by the limited number, objectivity and attention of experts. Their models are more successful at screening out ideas experts consider poor than at identifying the very best ideas.

This is close prior art for any claim that automated pre-filtering can protect scarce expert attention.

Reference: Bell, J. J., Kavadias, S. & Sommer, S. C. (2023). *Can AI Help in Ideation? A Theory-Based Model for Idea Screening in Crowdsourcing Contests.* Marketing Science. https://doi.org/10.1287/mksc.2023.1434

### 2. Specialist idea evaluation by crowds and LLMs

Gimpel et al. (2025) describe specialist expert juries as scarce and expensive bottlenecks and compare expert, crowd and LLM evaluations of innovation-contest proposals. They explicitly recommend crowds/LLMs for parts of the preselection problem, while warning that high-stakes error rates can still make expert review preferable.

This is exceptionally close prior art for "use cheap evaluators to reduce expert-jury load."

Reference: Gimpel, H., Laubacher, R., Probost, F., Schäfer, R. et al. (2025). *Idea Evaluation for Solutions to Specialized Problems: Leveraging the Potential of Crowds and Large Language Models.* Group Decision and Negotiation, 34, 903–932. https://doi.org/10.1007/s10726-025-09935-y

Probost et al. (2026) further examine multi-agent LLM systems as idea evaluators and explicitly discuss their use to pre-evaluate ideas or challenge human evaluation.

Reference: Probost, F. et al. (2026). *The Crowd Without People: Multi-agent Large Language Models as Idea Evaluators.* Group Decision and Negotiation, 35, 48. https://doi.org/10.1007/s10726-026-09993-w

### 3. Selective prediction and learning to defer

Classification with a reject option and selective prediction formalize the accuracy/coverage trade-off: an automated system may abstain on cases it should not decide. El-Yaniv and Wiener (2010) characterize the risk-coverage trade-off; Franc, Prusa and Voracek (2023) provide optimal strategies for reject-option classifiers.

Learning-to-defer work makes the downstream human part of the decision system rather than treating rejection as a terminal outcome. Madras, Pitassi and Zemel (2018) explicitly model an automated system that can pass a decision to another decision-maker. Later work addresses limited expert predictions and heterogeneous expert costs/capabilities.

This means "the machine should know when to send a case to a human" is established.

References:

- El-Yaniv, R. & Wiener, Y. (2010). *On the Foundations of Noise-free Selective Classification.* JMLR, 11, 1605–1641.
- Franc, V., Prusa, D. & Voracek, V. (2023). *Optimal Strategies for Reject Option Classifiers.* JMLR, 24(11), 1–49.
- Madras, D., Pitassi, T. & Zemel, R. (2018). *Predict Responsibly: Improving Fairness and Accuracy by Learning to Defer.* NeurIPS / arXiv:1711.06664.
- Hemmer, P. et al. (2023). *Learning to Defer with Limited Expert Predictions.* arXiv:2304.07306.

### 4. Active learning and scarce expert-query budgets

Active learning asks which observations are worth sending to a costly oracle under limited labeling budgets. Cost-sensitive variants explicitly trade off information gain, accuracy and labeling cost, including heterogeneous annotators.

This is direct mathematical prior art for allocating scarce expert queries.

The handoff problem differs only if the candidate object, expert function, provenance state and epistemic transition add structure that materially changes the objective or constraints.

### 5. Editorial and peer-review triage

Editorial desk screening already protects scarce reviewer capacity. Checco et al. (2021) review AI-assisted peer review and identify initial screening as a natural automation target under growing submission volumes. A 2026 scoping review of 189 sources distinguishes assistive triage from autonomous review and emphasizes the continuing need for human oversight.

Large deployments such as the AAAI-26 AI review pilot show that AI can contribute to review at scale, while other 2026 studies show substantial weaknesses, positivity bias, uneven grounding and vulnerability to manipulation.

References:

- Checco, A. et al. (2021). *AI-assisted peer review.* Humanities and Social Sciences Communications, 8, 25. https://doi.org/10.1057/s41599-020-00703-8
- *Artificial intelligence in scholarly peer review: a scoping review of applications, risks, and governance challenges.* International Journal of Medical Informatics 214 (2026), 106418.
- Biswas, J. et al. (2026). *AI-Assisted Peer Review at Scale: The AAAI-26 AI Review Pilot.* arXiv:2604.13940.
- Li, L. et al. (2026). *Gaming AI-Assisted Peer Reviews Poses New Risks to the Scientific Community.* arXiv:2606.10159.

### 6. Idea evaluation is not ground truth

Recent reviews emphasize that idea evaluation is multidimensional, biased and uncertain. Expertise helps recognize and select novel ideas, but experts and decision-makers are not perfect ground-truth oracles. Gimpel et al. explicitly acknowledge this limitation when treating expert juries as the closest available benchmark.

This matters for the Agalmic formulation. A triage system should not merely learn "what experts tend to approve." It should measure what expert review *adds* to the epistemic state and retain independent tests of later correctness, usefulness or survival where those outcomes are observable.

References:

- Baraboshkin, V. et al. (2026). *Unpacking idea evaluation process: Key insights and future directions.* Technovation 154, 103563.
- Röth et al. / Research Policy (2025). *Do you see what I see? How expertise and a decision-maker role influence the recognition and selection of novel ideas.* Research Policy 54(1), 105139.

### 7. Value of information

Value-of-information methods already ask whether acquiring additional evidence is worth its cost and are used in research-priority and health-decision settings.

This provides a natural normative ancestor for asking whether an expert review is worth spending scarce expert time on a particular candidate.

## Defensible delta to test

The strongest possible contribution is not a new classifier. It is an **epistemic allocation protocol** with a different target and stricter boundary conditions.

The candidate contribution is the combination of:

1. **claim-level state** rather than generic document quality;
2. an explicit **authority deficit** describing what kind of warrant is missing;
3. routing to a **specific epistemic function** rather than a generic human fallback;
4. optimization against **expert attention cost**;
5. explicit estimation of **false-negative loss**, including unconventional and low-status-origin candidates;
6. **origin/credential invariance tests** so status does not silently become a triage feature;
7. **random audit of rejected candidates** so false negatives remain measurable;
8. **provenance continuity** across generation, triage, expert review and resulting state change;
9. a rule that **triage can route but cannot confer epistemic authority**;
10. adversarial tests against presentation gaming and score manipulation.

Any one of these has antecedents. The research question is whether their combination defines a useful and empirically superior handoff protocol under AI-scale candidate abundance.

## Proposed formal target

For candidate `c`, expert or expert class `e`, and routing policy `π`, define the expert-review action as valuable only insofar as it changes an epistemic state.

A practical first objective is:

> **maximize useful epistemic state change per unit of expert attention, subject to constraints on false negatives, calibration, auditability and authority preservation.**

Do not collapse the whole problem into a single unvalidated "idea quality" score.

Candidate metrics:

- expert minutes per decisive state transition;
- proportion of reviews producing `supported`, `weakened`, `rejected`, `reframed` or `unresolved` transitions;
- high-value recall among escalated candidates;
- false-negative rate estimated from random audits of screened-out candidates;
- expert opt-in / acceptance rate;
- routing accuracy to the right expertise class;
- calibration of escalation probability;
- sensitivity to originator status or institutional prestige;
- sensitivity to superficial rewriting or presentation changes;
- inter-rater disagreement and adjudication burden;
- downstream survival after independent replication, implementation or later evidence where observable.

## Minimal empirical test

Compare at least four blinded routing arms on the same candidate corpus:

1. **Direct expert review:** no pre-filter.
2. **Rule-based triage:** explicit claim/evidence/lineage completeness checks only.
3. **Model triage:** model-assisted ranking/escalation.
4. **Claim-sensitive handoff triage:** model/rule assistance plus explicit authority deficit, provenance, uncertainty and mandatory reject-audit sampling.

For all filtered-out arms, randomly sample rejected candidates for full expert adjudication. This is required to estimate false negatives.

Use multiple experts or panel adjudication on a benchmark subset rather than equating one reviewer with truth. Blind or randomize originator credentials. Include adversarially paraphrased candidate pairs to test whether surface presentation changes routing.

## Success condition

The formalism earns further development only if it can show a reproducible improvement over simpler baselines on a constrained quantity such as:

- equal or better high-value recall at materially lower expert time; or
- more decisive epistemic state transitions per expert-hour without unacceptable false-negative inflation;
- with no large credential/status effect and tolerable sensitivity to superficial rewriting.

If a simple ranking model or ordinary editorial triage performs equivalently, adopt the simpler mechanism and retire the special terminology.

## Novelty classification

**Established components + plausible integration/formalization/test contribution. Novelty not yet established.**

The correct next move is an experiment and formal comparison, not a stronger naming claim.
