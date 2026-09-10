# Expert-Attention Preservation Benchmark: Phase-1 Findings

**Date:** 10 September 2026  
**Dataset:** Berenslab ICLR `25v2`, years 2020-2025  
**Dataset SHA-256:** `48215679d54ea788b8dfc1177850845f047c5810554708273b617b67ce321859`  
**Protocol:** `EXPERT_ATTENTION_PHASE1_RESEARCH_NOTE.md`  
**Executable:** `research/expert_attention/iclr_preservation_audit.py`

## Result

The phase-1 descriptive audit supports continuing the preservation programme, while rejecting any framing in which efficient reproduction of historical acceptance is itself successful scarcity displacement.

The analysis slice contains 33,043 submissions with interpretable decisions, 32,604 with parsed reviewer scores, and 17,983 with non-unlabeled topic assignments. Median within-paper reviewer-score standard deviation is 1.000; the 90th-percentile disagreement threshold is 1.789.

Across sufficiently populated score/year/topic cells, the largest observed topic-to-topic acceptance-rate spread at approximately the same mean reviewer score is 36.6 percentage points. This supports the construct-validity concern that raw reviewer scores are not exchangeable across topic strata.

At a 20% expert-attention budget:

| Diagnostic policy | Accepted recall | High-disagreement recall | Worst-topic recall |
| --- | ---: | ---: | ---: |
| Random allocation | 20.0% | 19.9% | 13.8% |
| Post-review raw-score ranking | 60.8% | 10.0% | 11.3% |
| Post-review topic-normalized score ranking | 60.2% | 10.0% | 16.5% |

The score-ranked policies therefore look highly efficient if acceptance preservation is the only objective, but destroy roughly half of the high-disagreement cases that random allocation would preserve at the same budget. Topic normalization materially repairs worst-topic preservation while leaving accepted-paper recall almost unchanged, but does not repair dissent loss.

These policies are deliberately leaky diagnostics. Reviewer scores are post-review outcomes and cannot be used by a prospective pre-review router.

## Preregistered hypothesis adjudication

### H1: score-conditional heterogeneity — supported descriptively

The observed maximum topic-to-topic acceptance spread of 36.6 percentage points within sufficiently populated approximate score/year cells is large enough to reject the working assumption that a single global score scale is an adequate allocation signal.

This does not establish a causal topic bias. Topic may proxy differences in submission quality, score interpretation, area-chair practice, reviewer calibration, or other venue mechanisms. The correct conclusion is narrower: global raw-score comparability is empirically unsafe for the benchmark.

### H2: dissent destruction under score-prioritized allocation — supported

At 20% budget, raw-score ranking preserves 60.8% of accepted papers but only 10.0% of high-disagreement papers. Random allocation preserves approximately 20% of each by construction. A policy can therefore triple apparent acceptance efficiency while halving preservation of contested cases.

This is the clearest phase-1 result. Optimization against a conventional institutional outcome can systematically consume the very cases for which additional expert cognition may be most informative.

### H3: topic starvation under global ranking — supported for the tested diagnostic

At 20% budget, worst-topic recall is 11.3% under raw-score ranking and 16.5% under topic-normalized ranking, while accepted recall changes only from 60.8% to 60.2%.

The gain is not proof that topic quotas or normalization are normatively correct. It demonstrates that a low-cost stratification intervention can substantially alter who retains access to scarce review without materially degrading the conventional target.

### H4: multidimensional evaluation is necessary — supported

Raw and topic-normalized score rankings have nearly identical accepted-paper recall at 20% budget but materially different worst-topic recall. Conversely, both preserve accepted papers far better than random allocation while preserving dissent far worse.

A single scalar such as acceptance recall, AUROC, or workload saved would rank these systems incorrectly for the preservation objective.

## What this does not show

The analysis does not show that high-disagreement papers are scientifically better, that rejected papers are undervalued, or that topic normalization improves scientific quality. It also does not yet evaluate a deployable triage model because all diagnostic policies use post-review outcomes.

The next model phase must use only pre-review information and temporal validation. Downstream outcomes such as later publication or field/age-normalized citation trajectories should be added as separate imperfect proxies, not collapsed into ground truth.

## Generalization test: Nemosyne engineering verification

Nemosyne provides an unusually useful second domain for the same preservation formalism because its verification architecture already distinguishes evidence classes and contains multiple fidelity tiers: deterministic unit/integration tests, desktop/browser tests, synthetic XR/simulator episodes, governed physical Quest validation, and human UX/comfort judgment.

The scarce resource is not merely CI compute. It is **high-fidelity verification attention**: physical headset time, human observation, difficult end-to-end reproduction, and expert interpretation of ambiguous failures.

A naive engineering optimizer can make the same mistake as acceptance prediction: maximize green CI throughput while suppressing rare, cross-layer, modality-specific, or difficult-to-simulate failures. Therefore the transferable object is not an AI bug triager. It is a **Verification Attention Preservation Benchmark**.

For each candidate validation scenario or observed failure `i`, define a cheap-evidence vector available before high-fidelity escalation:

- deterministic/unit/integration results;
- browser smoke results;
- simulator/XR-agent episode outcomes;
- changed subsystems and authority boundaries;
- historical failure frequency;
- novelty/coverage distance from existing scenarios;
- cross-modality disagreement;
- uncertainty or conflicting evidence classes.

The allocator chooses whether to consume a scarce lane such as physical Quest, human UX review, long-duration soak, specialist security review, or clean-production qualification.

### Directly transferred metrics

- **Hardware/Human Work Saved at Preservation r:** high-fidelity sessions avoided while retaining at least `r` of failures eventually confirmed by high-fidelity evidence.
- **Counter-Simulation Recall:** fraction of failures missed or passed by simulator/cheap evidence but later found on physical hardware that the allocator still escalated.
- **Disagreement Preservation Rate:** preservation of cases where simulator, browser, telemetry, or different interaction modalities disagree.
- **Evidence-Class Preservation Gap:** worst recall across physical Quest, browser, simulator, controller, hand, performance, UX, and analytical-authority strata.
- **Reject-Audit Discovery Rate:** random sample of scenarios the allocator would skip that are nevertheless run at high fidelity, estimating hidden misses.
- **Perturbation Sensitivity:** routing stability under harmless changes to scenario names, ordering, log verbosity, or other superficial engineering metadata.

### Why this is valid for Nemosyne

The current QV design explicitly exists to prevent expensive physical-device time from becoming anecdotal evidence and explicitly forbids simulator evidence from being upgraded into physical-device qualification. The XR Agent Harness likewise separates `MEASURED`, `OBSERVED`, and `SUGGESTED` evidence and retains real-hardware qualification as irreducible. These are already the trust boundaries needed for a preservation benchmark.

The allocator must never decide truth. It decides **where the next expensive measurement is most informative**.

### First Nemosyne experiment

Do not deploy an adaptive allocator yet. First construct a retrospective dataset from existing validation artefacts:

`scenario_id, build_id, cheap_evidence[], simulator_outcome, physical_outcome, modality, gate, subsystem, failure_class, duration_cost`

Then simulate constrained physical-validation budgets and compare:

1. run-everything oracle/cost ceiling;
2. random allocation;
3. fixed critical-gate priority;
4. failure/uncertainty priority;
5. diversity-stratified allocation;
6. eventually, learned allocation.

The first success criterion is not fewer headset runs. It is evidence that fewer headset runs can be chosen **without reducing discovery of hardware-only, disagreement-rich, or rare cross-layer failures** beyond a preregistered tolerance.

This is a useful transfer even if learning adds no value. If a simple stratified policy preserves the relevant failure classes, that policy should be preferred.

## Decision

Proceed to a pre-review temporal baseline for the ICLR benchmark and, independently, instrument Nemosyne validation artefacts so that a retrospective verification-attention benchmark can be computed. Do not couple either system to automatic promotion decisions until reject-audit behaviour and preservation gaps are measurable.
