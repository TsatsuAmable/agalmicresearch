# Evaluating the Agalmic Cognitive Kernel Without Grader Illusions

**Research note 0.1 — 14 September 2026**

## Result

The current Cognitive Kernel benchmark is useful as a **conformance test**, but it is not by itself sufficient evidence that the kernel improves general task utility.

That distinction matters because the benchmark dimensions were derived from the kernel's intended behaviour. A kernel can therefore improve its score by becoming more legible to the rubric without necessarily improving downstream outcomes. The appropriate claim is narrower:

> The benchmark can establish whether the kernel reliably causes the behaviours it was designed to cause. Separate consequence tests are required before claiming that those behaviours improve real work.

## Why the evaluation needs hardening

The existing runner already does several things correctly: paired control/kernel conditions, matched task prompts, fixed decoding, model diversity as a release requirement, and retention of raw responses.

Three validity risks remain.

### 1. Judge-position and prompt sensitivity

LLM judges can change verdicts when response order changes, and semantically equivalent judge prompts can yield inconsistent decisions. A single judge pass is therefore not a stable measurement instrument.

**Control:** blind the conditions, randomize A/B position independently per pair, retain the hidden mapping, and mirror a sample with reversed order.

### 2. Rubric-construction alignment

The benchmark rubric is intentionally derived from the kernel. This makes it appropriate for **behavioural conformance** but creates a risk of circularity if the same benchmark is used to claim broad usefulness.

**Control:** report two distinct results:

- **Conformance:** does the kernel increase the target behaviours?
- **Consequence:** on real or externally specified tasks, does it reduce human attention, rework, error, cost or time while preserving authority and downstream quality?

Do not collapse the two into one "kernel score."

### 3. Evaluator-family dependence

Judge models can have systematic preferences, including stylistic and family-specific biases. Passing with one evaluator family should not count as a robust result.

**Control:** use multiple materially different judge families when possible, publish per-judge results, and treat disagreement as evidence rather than averaging it away.

## Minimal valid protocol

For each generator model and held-out task:

1. Generate matched control and kernel responses.
2. Create a blinded pair with deterministic random A/B assignment.
3. Score the pair with at least two independent judges when available.
4. Mirror a subset by reversing A/B order.
5. Retain raw judge rationales and scores.
6. Report task-level paired differences, not only a pooled mean.
7. Run a small human spot audit on ambiguous or high-impact disagreements if the release decision depends on them.
8. Separately run consequence tests on tool-enabled or real workflows.

A release candidate should not become canonical merely because it passes the conformance rubric.

## Consequence-test examples

The kernel claims to conserve scarce attention and improve action quality. Tests should therefore measure observable consequences where possible:

- number of unnecessary human escalations;
- active human minutes, not wall-clock delay;
- verified task completion;
- rework introduced downstream;
- hard-boundary violations;
- number of durable artefacts reused later;
- whether the identified bottleneck predicts where an intervention actually improves throughput.

The Frontier Throughput Audit can supply several of these measures.

## Novelty boundary

This note does **not** claim novelty for blinded evaluation, counterbalancing, paired experiments, LLM-as-a-judge bias measurement, or prompt-sensitivity testing.

The local contribution is integration: treating the Agalmic Kernel as an intervention whose **conformance** and **consequences** must be measured separately, and wiring blinded evaluation into the existing reproducible harness.

## Prior art

- Shi et al. (2024), *Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge*. https://arxiv.org/abs/2406.07791
- Li et al. (2025), *Curse of Knowledge: Your Guidance and Provided Knowledge are biasing LLM Judges in Complex Evaluation*. https://doi.org/10.18653/v1/2025.findings-emnlp.805
- *JudgeSense: A Benchmark for Prompt Sensitivity in LLM-as-a-Judge Systems* (2026). https://arxiv.org/abs/2604.23478
- Zhou et al. (2026), *LLM Evaluators are Biased across Languages*. https://arxiv.org/abs/2607.14480

## Decision rule

**Promote the kernel only when:**

1. conformance lift is reproducible across generator model families;
2. the result survives blinded, order-robust grading;
3. no hard-boundary regression appears;
4. consequence tests show at least one material improvement in real work;
5. the full kernel beats or materially improves upon the compact invocation.

Otherwise retain it as a useful experimental prompt, not a validated general capability.
