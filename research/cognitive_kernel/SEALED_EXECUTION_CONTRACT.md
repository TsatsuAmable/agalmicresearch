# Sealed Execution Contract for Cognitive-Intervention Experiments

**Agalmic Research — 16 September 2026**

## Claim

A fresh workspace is not an independent experimental condition unless the execution system can demonstrate what the condition could read, write, communicate with, and learn before its paired condition completed.

The Cognitive Kernel pilot therefore treats **execution isolation as evidence**, not as a label supplied by the runner.

## Threat model

A nominally isolated control can still be contaminated through at least five channels:

1. **filesystem/state leakage** — shared working trees, caches, databases, temporary files, environment variables, or mutable service state;
2. **evaluation leakage** — access to hidden tests, evaluator code, labels, future repository history, or reference solutions;
3. **communication leakage** — transcripts, shared memory, inter-agent messages, tool arguments, or artefacts crossing condition boundaries;
4. **retrieval leakage** — internet/search access retrieves benchmark answers or artefacts unavailable in the intended task;
5. **outcome leakage** — one condition, operator, or adaptive harness sees the other's result before the pair is sealed.

Recent agent benchmarks independently expose these failure classes. RewardHackingAgents instruments fresh workspaces, patch histories, file access, and a trusted evaluator because workspace mutability can corrupt the measurement itself. AgentLeak shows that final-output inspection misses leakage through internal agent channels. AgentAbstain regenerates paired sandbox tasks and uses deterministic replay partly to resist contamination. Multi-Docker-Eval and Terminal-Bench show that reproducible environment construction is itself a nontrivial systems problem.

These works support the engineering requirement below. They do **not** establish that the proposed Agalmic contract is novel, optimal, or sufficient.

## Minimum execution evidence

For every condition, an executor MUST emit a sealed execution receipt containing:

- pair, assignment, condition, context, and workspace identifiers;
- immutable base-state identifier;
- task-spec and verification-spec hashes;
- executor implementation/version hash;
- model/provider/version identity when observable;
- start and completion timestamps;
- declared filesystem roots and whether any writable root is shared;
- declared network policy;
- declared tool/capability set;
- hashes of produced artefacts;
- a transcript/trace hash or an explicit declaration that no auditable trace is available;
- the paired receipt identifier only after both conditions have completed;
- any isolation violation or uncertainty discovered at runtime.

The executor MUST NOT mark a condition admissible merely because a workspace ID differs.

## Pair sealing rule

A pair is **sealed** only when both condition receipts exist and all of the following hold:

1. both receipts bind to the same pair, assignment, base state, task-spec hash, and verification-spec hash;
2. conditions are exactly one `control` and one `kernel`;
3. context identifiers differ;
4. mutable workspace identifiers differ when mutable workspace state exists;
5. neither receipt reports shared writable state, cross-condition communication, premature outcome visibility, or an isolation violation;
6. verification occurs under the precommitted verification specification;
7. receipt hashes are computed before paired outcome analysis.

Otherwise the pair is **inadmissible**, not a failed efficacy observation. The provenance record remains public where safe to publish.

## Isolation levels are claims with different evidence burdens

`fresh-agent-context` requires evidence of separate conversational/model state and no shared mutable memory channel.

`fresh-workspace` additionally requires evidence that mutable execution state is separated from the same pinned base. A branch name alone is insufficient because branches may share an underlying working tree, cache, service, or database.

`independent-human-session` additionally requires that the human participant cannot transfer treatment-specific information across conditions. This is the hardest level and cannot generally be automated away.

## Network policy

Network access is task-dependent, so `network=false` is not a universal requirement. Instead the policy is precommitted:

- **offline** when the task does not require external information;
- **allowlisted** when specific external resources are part of the task;
- **open-recorded** only when open-web retrieval is intrinsic to the task and the retrieval trajectory can be retained sufficiently for audit.

A research-synthesis task with open retrieval is therefore not equivalent to an offline benchmark task. Results must be stratified rather than collapsed into a single scalar score.

## Why this matters to Agalmic Research

The scarce resource is not merely compute. It is trustworthy human attention. An experiment that appears automated but later requires a human to reconstruct whether its controls were contaminated has displaced execution while creating validation debt.

A sealed receipt moves that validation upstream. Machines may generate large numbers of observations, but only observations carrying adequate execution evidence earn analytical attention.

## Novelty boundary

The components are established practice: sandboxing, provenance, content hashing, deterministic replay, evaluator separation, network policy, and audit traces. The contribution here is a compact operational contract connecting those practices to the Agalmic rule that **evidence earns attention** in paired cognitive-intervention experiments.

This should be presented as an engineering synthesis and research method, not as a newly discovered experimental principle.

## References

- Atinafu, Y. & Cohen, R. (2026). *RewardHackingAgents: Benchmarking Evaluation Integrity for LLM ML-Engineering Agents*. arXiv:2603.11337.
- El Yagoubi, F., Al Mallah, R. & Badu-Marfo, G. (2026). *AgentLeak: A Full-Stack Benchmark for Privacy Leakage in Multi-Agent LLM Systems*. arXiv:2602.11510.
- Liu, X. et al. (2026). *AgentAbstain: Do LLM Agents Know When Not to Act?* arXiv:2607.10059.
- Fu, K. et al. (2025). *Multi-Docker-Eval: A Shovel of the Gold Rush Benchmark on Automatic Environment Building for Software Engineering*. arXiv:2512.06915.
- Terminal-Bench 2.0 (2025–2026). Containerized, human-verified terminal-agent evaluation suite.
