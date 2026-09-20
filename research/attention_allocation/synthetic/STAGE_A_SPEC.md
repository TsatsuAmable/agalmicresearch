# Stage A — Synthetic Allocation Benchmark

**Status:** engineering scaffold, non-evidentiary  
**Authority:** `PROGRAMME.md` and `PRE_OUTCOME_FEASIBILITY_GATE.md` remain binding.

## Purpose

Build a deterministic test harness for allocation mechanics before empirical policy comparison is licensed.

This stage is allowed to test software invariants:

- all policies receive the same candidate pool and the same validation budget;
- evaluator-only latent value is structurally unavailable to policy functions;
- seeded runs are reproducible;
- no policy can overspend the declared budget;
- selected candidates are unique;
- outcome metrics are computed only after selection;
- scenario assumptions are explicit and versioned.

It is **not** evidence that any policy is scientifically superior. Synthetic worlds encode assumptions. A policy that performs well here may simply match those assumptions.

## Gate discipline

The empirical programme currently prohibits substantive policy simulations until the feasibility gate is frozen and passed for the relevant claim class. Therefore the runner refuses execution unless `--engineering-fixture` is supplied.

That flag means: "exercise the harness and inspect mechanics only." Outputs must not be used as programme evidence, publication results, or grounds for choosing a preferred policy.

## Scenario families

The benchmark deliberately includes several synthetic worlds rather than one convenient world:

1. **neutral** — latent value is mostly independent of visible plausibility/novelty.
2. **legibility-aligned** — visible plausibility is informative about latent value.
3. **novelty-positive** — novelty contributes to latent value.
4. **costly-breakthrough** — novelty contributes to value while also increasing validation cost.

No scenario is asserted to describe science. They are adversarial fixtures for checking whether conclusions change when assumptions change.

## Candidate schema

Policy-visible fields:

- `id`
- `arrival_index`
- `plausibility`
- `novelty`
- `uncertainty`
- `minority`
- `validation_cost`
- component costs

Evaluator-only field:

- `latent_value`

The runner constructs a redacted immutable policy view, so a policy cannot inspect `latent_value`.

## Baseline policies

- FIFO
- seeded random
- plausibility
- plausibility-per-cost
- uncertainty
- diversity (novelty + minority indicator)
- exploration quota (bounded novelty/minority exploration plus plausibility exploitation)

These are baselines, not endorsed allocation rules.

## Metrics

After selection, the evaluator reports:

- budget spent and residual budget;
- selected count;
- realised latent value in the synthetic world;
- top-decile recovery;
- unconventional top-decile recovery;
- mean selected novelty;
- mean selected validation cost.

The primary Stage A acceptance criterion is **harness correctness**, not a winning policy.

## Run

```bash
npm run test:attention-synthetic
npm run bench:attention-synthetic
```

The second command runs only the engineering fixture and writes no canonical research conclusion.
