# Experimental Pair Planner

**16 September 2026**

The Cognitive Kernel pilot now has a machine-readable pre-outcome assignment layer.

The planner commits each pair to a pinned base state, immutable task-spec hash, immutable verification-spec hash, isolation level, two distinct context/workspace identifiers, and a deterministic pseudorandom assignment derived from a secret salt. Only a hash commitment to the salt is written into the plan, allowing later audit without making assignment trivially predictable before execution.

This does **not** claim to solve benchmark contamination generally. Current agent-evaluation work shows several distinct contamination channels: training-set exposure, search-time retrieval of public answers, leaked future repository history, leaked evaluation artefacts, and cross-run mutable state. Fresh workspaces address only the last two when correctly provisioned. Internet-enabled research tasks still require task-specific leakage controls.

The design therefore treats isolation as an admissibility property rather than an efficacy metric. A result can fail because the intervention is ineffective; an unisolated result fails earlier because it is not interpretable.

## Evidence

- NIST CAISI, *Examples of cheating in CAISI's agent evaluations* (2025): documents solution leakage through internet access, repository history, files and configuration.
- Badertdinov et al., *SWE-rebench* (NeurIPS 2025): continuously collected real-world tasks and decontaminated SWE-agent evaluation.
- White et al., *LiveBench* (ICLR 2025): frequently refreshed tasks and objective scoring to limit contamination.
- Wang et al., *Search-Time Contamination in Deep Research Agents* (2026): distinguishes retrieval-time leakage from training contamination and motivates transparent search trajectories and controlled benchmark access.

## Remaining gap

This planner creates an auditable experimental contract. It does not itself launch independent model sessions. The execution adapter must enforce the generated context/workspace identifiers and prevent cross-condition visibility.
