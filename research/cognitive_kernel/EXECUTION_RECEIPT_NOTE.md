# From Isolation Claims to Execution Receipts

**Agalmic Research — 17 September 2026**

## Result

The Cognitive Kernel pilot now defines a machine-readable **sealed execution receipt**. Its purpose is deliberately narrow: record enough execution-time evidence to decide whether a control/Kernel run is admissible for paired analysis without reconstructing the run from memory.

A workspace identifier is not evidence of isolation. A successful final answer is not evidence that the declared tools were actually used. A trace is not automatically evidence that the evaluator or environment remained uncontaminated. The receipt therefore binds the experimental assignment to runtime identity, filesystem/network boundaries, capability manifest, trace and artefact hashes, terminal state, and an outcome seal.

## Minimum receipt

Each condition records:

1. pair, assignment, condition and context identity;
2. pinned base state plus immutable task and verification hashes;
3. model and harness identity/version;
4. workspace/filesystem boundary;
5. network policy and, when relevant, allowlist/log hash;
6. capability-manifest hash;
7. count of known cross-condition channels and declaration of shared mutable resources;
8. trace, artefact-manifest and terminal-state hashes;
9. a sealed outcome hash produced before peer-condition completion;
10. a content hash over the receipt itself.

The schema permits `unknown` and an admissibility result of `abstain`. Missing evidence must not be silently converted into evidence of absence.

## Admissibility rule

A receipt is necessary but not sufficient. A pair should be rejected or marked **ABSTAIN** when the claimed isolation property cannot be demonstrated. In particular, `cross_condition_channel_count = 0` is an observation supplied by instrumentation, not a metaphysical guarantee that no channel exists. The execution adapter remains responsible for making the declared boundary true.

This follows a broader lesson from current agent evaluation: evaluation increasingly needs executable environments, complete traces, terminal-state checks, and configuration-level provenance. Thinkingbox evaluates persistent backend state in isolated MCP-compatible sessions; ClawProBench treats the model-plus-runtime configuration and execution trace as the evaluation unit; Harness-Bench records traces, final artefacts and validator outputs; recent provenance surveys similarly argue that final-answer accuracy cannot reconstruct how an agent acted.

A further warning comes from reproducibility work: a runnable artefact or positive signal can remain semantically wrong. Receipts therefore establish **execution provenance**, not task correctness. Correctness still belongs to the separately frozen verification procedure and counterfactual/negative controls where appropriate.

## Novelty boundary

Cryptographic commitments, provenance records, sandbox manifests and execution traces are established ideas. The contribution here is not a new cryptographic primitive. It is the composition of these mechanisms into a small, falsifiable admissibility contract for paired human–AI cognitive-intervention experiments, with explicit ABSTAIN semantics when evidence is insufficient.

## References

- Li et al. (2026), *One Success Isn't Reliability: Thinkingbox, a Sandbox and Benchmark for Agents in Stateful Business Workflows*, arXiv:2608.19741.
- Xiao (2026), *ClawProBench: Trace-Aware Evaluation of AI Agents with Runtime Coverage and Frozen Workplace-Style Holdouts*, arXiv:2608.22510.
- *Harness-Bench: Measuring Harness Effects across Models in Realistic Agent Workflows* (2026), arXiv:2605.27922.
- Wang et al. (2026), *From Agent Traces to Trust: A Survey of Evidence Tracing and Execution Provenance in LLM Agents*, arXiv:2606.04990.
- Chen (2026), *From Runnable to Verifiable: An Independent Reproducibility Study of LLM/Agent-Driven Vulnerability Validation Artifacts*, arXiv:2608.09567.

## Next discriminating action

Implement a local execution adapter that generates this receipt from observed runtime events rather than caller-supplied assertions, validates paired receipts against the frozen plan, and refuses analysis on `fail` or `abstain`. Only then run the first consequence pair.
