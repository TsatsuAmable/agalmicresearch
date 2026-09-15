# Human Attention Is Not Wall Time

**Research note — 15 September 2026**

## Result

The Cognitive Kernel consequence pilot should treat **active human attention** as a scarce resource distinct from elapsed task duration, but it should not infer that quantity retrospectively from timestamps.

This distinction is not cosmetic. AI assistance can move work between coding, prompting, waiting, reviewing, verification, and repair. A system can reduce machine execution time while increasing scarce human supervision, or reduce hands-on work while increasing downstream rework. Conversely, elapsed time can include machine waiting that consumes little human attention. A single wall-clock measure therefore conflates materially different scarcity states.

The consequence protocol already names `human_minutes` as its primary scarcity outcome. This note tightens the measurement claim: **human minutes are admissible only when captured prospectively by an explicit attention-accounting procedure.** Otherwise the field is missing, not estimated.

## External evidence

Recent developer-productivity experiments demonstrate why perception and measurement must remain separate.

Becker et al. (METR, 2025) randomized 246 real repository tasks completed by 16 experienced open-source developers to AI-allowed or AI-disallowed conditions. Developers expected AI to reduce completion time by 24% and, after the study, believed it had reduced time by 20%; measured completion time instead increased by 19% in that particular early-2025 setting. The result is deliberately narrow, but the perception/measurement divergence is directly relevant to Agalmic consequence accounting.

Cui et al. (2025) pooled three field experiments at Microsoft, Accenture, and another Fortune 100 company, covering 4,867 developers, and estimated a 26.08% increase in completed tasks with an AI coding assistant, with substantial uncertainty and heterogeneity. A separate randomized trial involving 96 Google engineers estimated about a 21% reduction in time on a complex enterprise task, again with a wide confidence interval. These results point in a different direction from METR rather than cancelling it: **AI productivity effects are conditional on people, tools, tasks, context, and outcome definition.**

METR's February 2026 follow-up also reports a practical identification problem: widespread agentic-tool adoption made AI-disallowed task randomization increasingly difficult because developers became reluctant to work without AI. That is a warning for our own pilot. A clean control can become costly or behaviorally artificial as the intervention becomes normal infrastructure.

## Measurement rule

For each prospective task condition, record human attention using one of these admissible methods, in descending preference:

1. **Event-derived active attention.** Instrument explicit human interaction windows such as prompt composition, review, approval, manual editing, verification, debugging, or decision events. Preserve raw events and derive minutes reproducibly.
2. **Start/stop attention timer.** Human starts a dedicated timer when actively attending to the task and pauses it when attention leaves the task or autonomous execution begins.
3. **Contemporaneous activity ledger.** Short timestamped entries classify attention episodes immediately after they occur.

Do not use task `started_at` to `completed_at` as a proxy for human attention. Do not reconstruct attention minutes from memory after task completion except as a separately labelled exploratory estimate.

## Attention taxonomy

Record enough event information to derive, without forcing a scalar model:

- **instruction** — specifying goals, constraints, context, or corrections;
- **review** — reading or inspecting machine output;
- **verification** — running or interpreting checks needed to establish completion;
- **repair** — human work correcting machine-caused defects;
- **decision** — irreducible human judgement or authorization;
- **direct execution** — human performs task work that the machine did not perform.

Waiting for an autonomous process is not active attention unless the human is actually monitoring it. Machine runtime should be recorded separately when useful.

## Guard against observer burden

Measurement itself consumes the resource being measured. The instrumentation therefore fails its Agalmic purpose if logging overhead becomes substantial.

For the pilot:

- prefer automatic event derivation where trustworthy;
- otherwise use one-click/toggle timing rather than narrative diaries;
- separately record `measurement_overhead_seconds` when manual instrumentation is used;
- report attention both gross and, where defensible, net of measurement overhead;
- abandon or simplify instrumentation if logging materially changes task behavior.

## Design correction

The current 12-pair target remains a **coverage and feasibility target**, not a powered efficacy sample. Before any confirmatory study, use pilot observations to estimate within-pair variability, missingness, measurement burden, carry-over, and task-family heterogeneity.

The strongest next methodological improvement is random assignment of condition order within comparable task families where feasible. However, the Kernel is a policy/scaffold rather than a pill: exposure can teach habits that persist into a later control condition. Condition leakage and learning are therefore first-class threats. When washout is implausible, use fresh tasks and explicitly model/order-stratify the pilot rather than pretending independence.

## Novelty boundary

None of the individual measurement ideas above is novel. Time-on-task experiments, activity sampling, randomized productivity studies, and human-in-the-loop accounting are established methods. The plausible Agalmic contribution is narrower: a **scarcity-displacement consequence ledger** that refuses to equate automation with benefit and jointly tracks scarce human attention, verified completion, repair, authority violations, and downstream failure as constraints migrate through a human-machine system.

That contribution is methodological and remains unvalidated until real prospective records exist.

## References

- Becker, J., Rush, N., Barnes, E., & Rein, D. (2025). *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*. arXiv:2507.09089. https://doi.org/10.48550/arXiv.2507.09089
- METR (24 February 2026). *We are Changing our Developer Productivity Experiment Design*. https://metr.org/blog/2026-02-24-uplift-update/
- Cui, Z. K., Demirer, M., Jaffe, S., Musolff, L., Peng, S., & Salz, T. (2025). *The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments with Software Developers*. Microsoft Research working paper.
- *How Much Does AI Impact Development Speed? An Enterprise-Based Randomized Controlled Trial*. ICSE-SEIP 2025. DOI: 10.1109/ICSE-SEIP66354.2025.00060.

## Consequence for the pilot

A positive Kernel result cannot be claimed from shorter elapsed runs or subjective impressions. Evidence must show that a claimed scarcity actually moved, under a measurement procedure capable of distinguishing human attention from machine latency, while completion and boundary guardrails remain intact.
