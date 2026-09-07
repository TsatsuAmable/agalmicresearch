# Memory Palace Continuation: Adversarial Constitutional Attention

**Parent session:** `ar-session-2026-09-07-epistemic-artefacts-constitutional-attention`  
**Event order:** continuation after initial provenance checkpoint  
**Date:** 7 September 2026  
**Status:** exploratory  
**Publication sensitivity:** public exploratory research record

## Triggering contribution

The human curator refined the earlier constitutional-attention idea into an explicitly **adversarial evolutionary system** and asked whether the project should create a room in the Memory Palace that records epistemic artefacts as soon as they appear.

The proposed selection target was described as humanity's determined meaningful future, with human attention directed toward defining that target and the system continuously searching for strategies that displace scarcity and expand frontiers.

## Refinement

The useful version should not assume that humanity has one globally valid scalar fitness function. The provisional architecture instead treats the constitution as a governed combination of:

- plural descriptions of worthwhile futures;
- hard safety, rights and legitimacy constraints;
- resource and externality limits;
- uncertainty and reversibility rules;
- escalation conditions;
- procedures for revising the constitution itself.

Within that constitution, two populations can co-evolve.

### Strategy population

Generate mechanisms, institutions, technologies, research moves or other strategies intended to displace current scarcities and expand reachable worthwhile futures.

### Adversary / test population

Generate counterexamples, failure scenarios, harms, externalities, excluded stakeholders, distribution shifts, specification gaming, brittleness and cases in which a candidate strategy ceases to be worthwhile.

The adversary is not an enemy of the objective. Its role is to make weak strategies fail early and to expose hidden costs before large commitments are made.

### Historical challenge archive

Retain old counterexamples, failures and strong adversaries across generations. A candidate should not appear to improve merely because the current adversary population has forgotten an old way of breaking it.

This is directly motivated by competitive co-evolution literature, where hall-of-fame archives and evaluation against past opponents are used to distinguish genuine progress from cycling or apparent progress.

## Provisional mechanism

A useful formalization target is therefore not simply:

`maximize one fitness score`

but something closer to:

`search for frontier-expanding strategies subject to constitutional constraints, plural objectives and adversarially generated tests`

A candidate earns greater resources or autonomy only if it survives increasingly strong attempts to expose unacceptable harms, hidden externalities, fragility or value failure.

Human attention is concentrated at the constitutional layer:

- determining and revising worthwhile-future criteria;
- adjudicating contested values;
- inspecting novel failure modes;
- deciding which constraints are hard versus negotiable;
- approving high-impact or irreversible transitions;
- auditing legitimacy, corrigibility and distributional consequences.

Routine candidate generation, provenance capture, low-risk evaluation, adversarial testing and ordinary rejection can increasingly be delegated.

## Preliminary lineage

This is not a novelty claim.

Important antecedent families include:

- **Competitive co-evolution.** Rosin and Belew, "New Methods for Competitive Coevolution," *Evolutionary Computation* 5(1), 1997. DOI: `10.1162/evco.1997.5.1.1`. Their work includes a hall-of-fame mechanism that preserves strong opponents across generations.
- **Adversarial optimization through co-evolution.** Later work explicitly treats competitive co-evolution as an adversarial optimization method and studies false progress, cycling and robustness.
- **Interactive evolutionary computation.** Human evaluation can guide evolutionary search when an adequate formal fitness function is unavailable, but human evaluation burden is a known problem.
- **Constitutional AI.** Explicit principles can guide machine critique/evaluation and reduce the need for direct human labeling, while leaving broader questions of legitimacy and value specification unresolved.
- **Selective / meaningful human oversight.** Existing governance approaches already move human intervention toward consequential, uncertain or irreversible decisions.

The possible Agalmic contribution is therefore narrower:

> **A constitutional, adversarial search architecture whose object is not merely better model behaviour or better candidate designs, but continuous discovery of strategies that displace scarcity and expand a plural set of worthwhile reachable futures, with provenance, selective escalation and historical failure memory built into the search process.**

Novelty remains unassessed.

## New epistemic artefact

`artefact:constitutional-attention-adversarial-search-2026-09-07`

- **Kind:** mechanism conjecture
- **Warrant:** exploratory
- **Understanding:** conceptually understood, not formalized
- **Novelty:** mature antecedent families + synthesis; novelty unassessed
- **Commitment:** option
- **Next route:** formalization + lineage review + adversarial comparison

## Epistemic Intake Room

A separate low-friction intake layer was created during this continuation.

Its rule is:

> **Capture first. Judge deliberately. Promote sparingly.**

The purpose is to record materially distinct epistemic artefacts at emergence time even when:

- warrant is unknown;
- understanding is incomplete;
- novelty is unassessed;
- no publication decision exists;
- no Active Frontier commitment has been made.

This separates **preservation cost** from **attention cost**. The project can remember cheaply while spending scarce human attention only when validation, assimilation, handoff or promotion justifies it.

The intake room is implemented as `src/data/epistemicArtefactInbox.json`, with a public page at `/intake/` and a companion protocol at `docs/EPISTEMIC_ARTEFACT_INTAKE.md`.

## Decision record

### `decision:adversarial-constitutional-refinement`

- **Decision:** refine constitutional attention from ordinary selective oversight into an adversarial co-evolutionary search conjecture.
- **Reason:** adversarial populations can search specifically for hidden failures and externalities rather than relying on a fixed evaluator.
- **Risk:** co-evolution can cycle, overfit to current adversaries or generate apparent rather than global progress.
- **Mitigation candidate:** historical challenge archive, diverse adversaries, external benchmarks and explicit progress measures.
- **Reversal condition:** abandon or narrow the mechanism if it offers no measurable advantage over established robust optimization, competitive co-evolution or scalable oversight methods.

### `decision:epistemic-intake-room`

- **Decision:** preserve material epistemic artefacts immediately without automatic promotion.
- **Reason:** candidate abundance and machine speed can exceed human attention; lossless low-cost capture is separable from expensive evaluation.
- **Risk:** intake becomes an unbounded junk drawer or creates triage debt.
- **Reversal condition:** redesign or retire the intake mechanism if capture/triage overhead exceeds the epistemic loss it prevents.

## Roads not taken

### Rejected

- Treating one scalar "humanity fitness" score as sufficient. It hides disagreement, hard constraints and distributional consequences.
- Requiring human review before an artefact can even be preserved. This makes memory scale with attention.

### Deferred

- A complete constitutional-governance mechanism.
- Formal multi-objective fitness/constraint equations.
- Autonomous constitutional mutation.
- Real-world deployment or resource allocation.

### Surfaced but unexamined

- Pareto, lexicographic, satisficing and viability-based alternatives to scalar fitness.
- Democratic or deliberative mechanisms for constructing the worthwhile-future set.
- Separate red-team populations for safety, epistemic validity, distributional harms and environmental externalities.
- Machine-generated constitutions versus human-governed constitutional revision.
- Whether historical challenge archives should be immutable, weighted or periodically revalidated.
- Whether Nemosyne/Moneta could visualize the evolving strategy/adversary landscape.

## Authority and handoff

Current authority remains **exploratory**. Promotion would require handoff or collaboration in:

- evolutionary computation / competitive co-evolution;
- robust and multi-objective optimization;
- AI safety / scalable oversight;
- governance and value aggregation;
- economics of externalities and induced innovation.

## Portfolio consequence

No fourth Active Frontier item is created. This continuation strengthens the existing preserved option `possibility:constitutional-attention-search` and the active programme-level question of how cognitive systems can increase the capacity to reach worthwhile futures.
