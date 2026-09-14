# Evaluating the Agalmic Cognitive Kernel Without Grader Illusions

**Research note 0.1 — 14 September 2026**

## Result

The current Cognitive Kernel benchmark is useful as a **conformance test**, but it is not by itself sufficient evidence that the kernel improves general task utility.

That distinction matters because the benchmark dimensions were derived from the kernel's intended behaviour. A kernel can therefore improve its score by becoming more legible to the rubric without necessarily improving downstream outcomes.

> The benchmark can establish whether the kernel reliably causes the behaviours it was designed to cause. Separate consequence tests are required before claiming that those behaviours improve real work.

## Validity risks

1. **Judge position and prompt sensitivity.** Blind conditions, counterbalance A/B position, and retain mappings.
2. **Rubric-construction alignment.** Report behavioural conformance separately from downstream consequences.
3. **Evaluator-family dependence.** Publish per-judge results and preserve disagreement instead of averaging it away.

A release candidate should not become canonical merely because it passes the conformance rubric.

## Decision rule

Promote the kernel only when:

1. conformance lift is reproducible across generator model families;
2. the result survives blinded, order-robust grading;
3. no hard-boundary regression appears;
4. consequence tests show a material improvement in real work;
5. the full kernel materially improves upon the compact invocation.

Otherwise retain it as an experimental prompt, not a validated general capability.

## Prior art

- Shi et al. (2025), *Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge*. https://doi.org/10.18653/v1/2025.ijcnlp-long.18
- Moon et al. (2026), *Don't Judge Code by Its Cover: Exploring Biases in LLM Judges for Code Evaluation*. https://doi.org/10.18653/v1/2026.findings-eacl.70
- Bhat & Varma (2026), *All Prompts Are Created Equal? Evaluating Robustness of LLM Judges Against Non-Adversarial Prompt Variations*. https://aclanthology.org/2026.findings-acl.1929/

## Novelty boundary

This note does not claim novelty for blinded evaluation, counterbalancing, paired experiments, or LLM-judge bias measurement. Its contribution is the local separation of **conformance** from **consequence** evidence for the Agalmic Cognitive Kernel.
