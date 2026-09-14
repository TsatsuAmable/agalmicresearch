# Cognitive Kernel Consequence Protocol v0.1

**Agalmic Research — 14 September 2026**

## Question

Does using the Agalmic Cognitive Kernel improve real work, or merely make model outputs conform more closely to the kernel's own rubric?

The conformance benchmark cannot answer that question by itself. This protocol measures observable downstream consequences using matched control/kernel task pairs.

## Why consequence evidence is separate

Recent field experiments on generative AI measure outcomes such as task quality, time use, and retained capability rather than relying only on model-graded preference. Dillon et al. report a randomized field experiment across 66 firms and 7,137 workers in which treated users who adopted the tool spent about two fewer hours per week on email, while broader task composition did not measurably shift. Dell'Acqua et al. evaluate performance on real product-innovation challenges in a preregistered field experiment. Cruces et al. use randomized workplace-style tasks and a later unassisted follow-up to separate immediate assistance from retained capability. CollabSkill similarly argues for evaluation on real occupational tasks with actual human-agent collaboration.

These precedents do not validate the Agalmic Kernel. They establish a stronger measurement norm: **evaluate consequences at the level where the claimed benefit is supposed to occur.**

LLM judges remain useful for some conformance checks, but position and superficial-form biases are documented, including in 2026 code-evaluation work. They should not be the sole authority for real-work utility.

## Unit of evidence

A **matched pair** contains the same task family under two conditions:

- `control`: ordinary model/tool workflow;
- `kernel`: the same workflow with the Agalmic Kernel intervention.

Each pair should hold constant, where feasible:

- task specification;
- model family/version;
- available tools and permissions;
- input artefacts;
- stopping rule;
- evaluator or verification procedure.

Order should be randomized or counterbalanced when carry-over is plausible.

## Minimum record

Each JSONL record contains:

- `pair_id`
- `task_id`
- `condition` = `control` or `kernel`
- `human_minutes`: active human attention, not elapsed wall time
- `verified_completion`: boolean outcome from a task-appropriate check
- `rework_count`: downstream repair events attributable to the output
- `boundary_violations`: hard permission/safety/authority violations
- `downstream_failures`: later failures that invalidate an apparently completed result

Optional provenance fields should point to commits, PRs, benchmark bundles, run IDs, or verification artefacts.

## Primary interpretation

For paired deltas computed as `kernel - control`:

- human minutes: negative is better;
- verified completion: positive is better;
- rework: negative is better;
- boundary violations: negative is better;
- downstream failures: negative is better.

No single scalar score is authoritative. A kernel that saves attention while increasing hard-boundary violations has not demonstrated improvement.

## Claim discipline

The reducer emits descriptive paired deltas. Fewer than five matched pairs are explicitly marked **descriptive-only**.

Five pairs is not a claim that statistical power is adequate. It is only a guard against interpreting one or two anecdotes as an experiment. Any inferential claim requires a pre-specified analysis plan appropriate to the outcome distributions, task heterogeneity, dependence structure, and sample size.

A useful release claim should require:

1. a preregistered or frozen analysis plan before inspecting final outcomes;
2. materially heterogeneous task families;
3. provenance-preserved raw records;
4. no regression on hard-boundary outcomes;
5. a practical effect on at least one claimed scarcity, such as human attention or downstream rework;
6. replication across more than one generator/model family before claiming generality.

## Falsification

The kernel's scarcity-displacement claim is weakened if it:

- reduces human minutes but increases downstream repair enough to erase the saving;
- improves model-judge scores without improving verified completion;
- merely shifts human work from execution into validation;
- improves one task family but fails to generalize to materially different work;
- causes more boundary violations, hidden failures, or brittle dependence on a specific evaluator.

## Tool

Run:

```bash
npm run summarize:kernel-consequences -- path/to/records.jsonl
```

The source JSONL remains authoritative. The summary can always be regenerated.

## Novelty boundary

This protocol does not claim novelty for paired experiments, randomized field experiments, counterbalancing, human-AI productivity measurement, or matched-outcome analysis.

The local contribution is narrower: **making Agalmic scarcity-displacement claims auditable by connecting the Cognitive Kernel experiment to the Frontier Throughput evidence model and preserving downstream consequences instead of stopping at prompt-level conformance.**

## References

- Dillon, E. W., Jaffe, S., Immorlica, N. & Stanton, C. T. (2025). *Shifting Work Patterns with Generative AI.* NBER Working Paper 33795. https://doi.org/10.3386/w33795
- Dell'Acqua, F. et al. (2026). *The Cybernetic Teammate: A Field Experiment on Generative AI and Teamwork.* Organization Science. https://doi.org/10.1287/orsc.2025.20702
- Cruces, G. et al. (2026). *Does Generative AI Narrow Education-Based Productivity Gaps? Evidence from a Randomized Experiment.* NBER Working Paper 34851. https://doi.org/10.3386/w34851
- Shao, Y. et al. (2026). *CollabSkill: Evaluating Human-Agent Collaboration On Real-World Tasks.* https://arxiv.org/abs/2606.09833
- Shi, L. et al. (2025). *Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge.* https://doi.org/10.18653/v1/2025.ijcnlp-long.18
- Moon, J. et al. (2026). *Don't Judge Code by Its Cover: Exploring Biases in LLM Judges for Code Evaluation.* https://doi.org/10.18653/v1/2026.findings-eacl.70
