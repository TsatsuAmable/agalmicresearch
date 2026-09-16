# Cognitive Kernel Pilot: Contamination-Control Amendment

**Agalmic Research — 16 September 2026**

## Decision

The original pilot's matched-pair language is too permissive for a persistent cognitive intervention.

A sequential `control -> kernel` or `kernel -> control` comparison performed by the same continuing agent/session can be contaminated by learning, strategy transfer, evaluator adaptation, cached context, or changed expectations. Unlike a transient treatment, the Cognitive Kernel is intended to alter reasoning behaviour. There is no defensible short "washout" that makes an exposed cognitive system naïve again.

Because **no outcome records have yet been collected**, this amendment is prospective rather than outcome-responsive.

## Revised pilot design

The unit remains a matched **task pair**, but the two conditions must be executed in **independent fresh contexts**.

For each pair:

1. Freeze a task specification and verification procedure.
2. Produce two equivalent task instances, or duplicate the same immutable task input where execution cannot mutate shared state.
3. Randomly assign one instance to `control` and one to `kernel`.
4. Run each condition in a fresh context with no access to the other condition's transcript, intermediate artefacts, or outcome.
5. Where repository or external state is mutable, isolate workspaces/branches/sandboxes and begin from the same pinned base state.
6. Verify each output using the same pre-specified procedure.
7. Record active human attention prospectively.
8. Reveal pair membership for analysis only after both records are complete.

If fresh-context independence cannot be established, the pair is inadmissible.

## Why counterbalancing alone is insufficient

Counterbalancing addresses order effects when repeated exposure is scientifically defensible. Crossover guidance warns that treatment persistence can contaminate later periods; when an intervention cannot be readily removed, crossover may be unsuitable. Cognitive prompting can create exactly this problem through retained context, learning, changed strategy, or human adaptation.

The earlier manifest's phrase "counterbalance condition order within each task family when carry-over is plausible" therefore understates the risk. For this intervention, plausible carry-over is a reason to **isolate conditions**, not merely alternate their order.

## Independence levels

Each record declares one of:

- **fresh-agent-context**: separate model session/context, identical frozen inputs and tools;
- **fresh-workspace**: above plus isolated mutable repository/filesystem state from a pinned base;
- **independent-human-session**: separate human exposure where the human component itself could learn the Kernel condition.

The pilot may mix levels across task families, but comparisons must state which level was used.

## Exclusion criteria

Reject a pair before analysis if:

- either condition can inspect the other's transcript or intermediate artefacts;
- mutable state differs at condition start;
- the verification rule changes after either output is seen;
- human attention is reconstructed retrospectively;
- the task instance materially advantages one condition;
- the intervention leaks into the nominal control instructions or context.

Excluded pairs remain in the provenance ledger with an exclusion reason; they are not silently deleted.

## Novelty boundary

This is not a novel experimental-design principle. Crossover, carry-over, period effects, counterbalancing, and contamination are established methodology.

The Agalmic contribution is operational: applying those constraints to persistent cognitive interventions and encoding independence/provenance requirements directly into an executable human–AI research pipeline.

## Evidence

- Dwan et al. (2019), CONSORT extension for randomized crossover trials. *BMJ* 366:l4378. https://doi.org/10.1136/bmj.l4378
- Brooks (2012), counterbalancing serial-order carryover effects. *Psychological Methods* 17(4):600–614. https://doi.org/10.1037/a0029310
- Shao et al. (2026), *CollabSkill: Evaluating Human-Agent Collaboration On Real-World Tasks*. https://arxiv.org/abs/2606.09833
- Kesgin (2026), *HCCD-DS v2: a transparent synthetic benchmark for human–AI decision support under contextual uncertainty*. *Scientific Reports* 16:24155. https://doi.org/10.1038/s41598-026-59232-0

## Consequence

The immediate bottleneck is no longer "find twelve tasks." It is **reliably spawning isolated, equivalently provisioned experimental contexts and capturing their provenance automatically**.
