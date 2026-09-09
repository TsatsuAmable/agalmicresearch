# Agalmic Research Completion Lifecycle

Version: 0.2  
Status: default operating rule  
Date: 9 September 2026

## Purpose

Agalmic Research should not accumulate a large queue of attractive paper ideas that have never been subjected to lineage, evidence or execution. When a conversation produces a serious candidate paper, or asks whether an idea is worth researching, the default response is to begin the research process immediately.

The lifecycle is designed for **one human curator + cognitive-machine collaborators**. It uses machine cognition and inherited evidence aggressively while preserving explicit human authority boundaries. It also recruits independent cognitive reviewers throughout development so abundant machine cognition is spent on criticism as well as production.

> **Do not queue a research idea merely because it sounds promising. Test it, narrow it, execute it, attack it, publish the defensible result, or retire it.**

## Trigger

The lifecycle begins automatically when any of the following happens:

- an idea is proposed as a possible paper;
- a concept appears potentially research-worthy;
- a novel mechanism, formalism, hypothesis or empirical regularity is suggested;
- the programme considers making a substantive novelty claim;
- an existing Agalmic concept needs evidence rather than further exposition.

Exploratory conversation can remain exploratory. The trigger is the move from “interesting thought” toward “this may support a research contribution.”

No additional `proceed` step is required merely to begin screening.

## Stage 1 — State the candidate contribution

Write the smallest defensible version of the idea:

- research question;
- candidate claim or contribution;
- why the answer could matter;
- what would count as no contribution;
- current epistemic status.

Do not begin by naming a field or mechanism more strongly than the evidence warrants.

## Stage 2 — Prior-art and lineage search

Search the closest scholarly and technical antecedents before developing the local terminology.

Required outputs:

- closest prior art, not just supportive literature;
- established constructs that already explain part of the idea;
- direct competitors or near-duplicates;
- methodological precedents;
- datasets, benchmarks, code and open research artefacts that can be inherited;
- provisional novelty classification.

Possible novelty classifications include:

- established / no distinct contribution;
- independent rediscovery;
- synthesis;
- extension;
- application;
- operationalization;
- measurement or benchmark contribution;
- plausible theoretical or empirical novelty;
- novelty unresolved.

Finding decisive prior art is a successful result.

### Cognitive review checkpoint A — novelty and construct attack

Before substantial analysis cost accumulates, recruit independent cognitive reviewers with distinct mandates. At minimum use:

- a prior-art hunter instructed to find work that makes the paper unnecessary;
- a theory/construct critic instructed to find renaming, circularity or invalid operationalization;
- an adversarial domain referee instructed to identify the strongest rejection case.

Capture these reviews independently before synthesis. Do not vote. One well-supported fatal objection can kill or radically narrow the study.

## Stage 3 — Adversarial null test

Steelman the case that the idea should **not** become a paper.

Test at least:

- Does ordinary existing theory already explain it?
- Is the proposed variable merely a renamed construct?
- Is the mechanism tautological or unfalsifiable?
- Is the empirical claim identifiable with available evidence?
- Are we confusing a proxy with the construct of interest?
- Would a simpler method produce the same useful outcome?
- Is the claimed effect merely selection, survivorship, measurement or publication bias?
- Does machine-generated fluency make the idea appear more coherent than it is?
- Is the proposed contribution important enough to justify another publication rather than a short research note or retirement record?

Disposition after this stage may already be `retire`, `fold into prior art`, `narrow`, or `continue`.

## Stage 4 — Scarcity and feasibility design

Apply the One + Machine Method and Scarcity-Displacement Loop.

Identify the binding resources:

- curator time and attention;
- domain expertise / epistemic authority;
- participant or collaborator access;
- data;
- statistical or mathematical skill;
- compute / storage / money;
- implementation capacity;
- independent validation;
- publication or institutional access.

Then ask which scarcities can be displaced using inherited abundance:

- systematic/scoping review or meta-analysis;
- open-data reanalysis;
- public scholarly graphs;
- replication archives;
- retrospective experiments;
- natural or quasi-experiments;
- simulation;
- formal analysis;
- benchmark construction;
- open-source tools;
- machine-assisted extraction, coding, criticism and robustness analysis.

Prefer designs that can be executed credibly by one curator + machines. Escalate to scarce humans only for residual questions whose answer genuinely changes the claim.

## Stage 5 — Freeze the study plan before outcome fishing

Before substantive analysis, record:

- primary research question;
- hypotheses or explicitly exploratory questions;
- data sources and access conditions;
- unit of analysis;
- inclusion/exclusion rules;
- outcome variables and proxies;
- planned baselines;
- statistical / computational methods;
- missing-data treatment;
- robustness and falsification tests;
- leakage risks;
- causal limits;
- stopping / retirement conditions;
- expected residual human validation.

Exploratory analyses are allowed, but they must be labelled exploratory rather than back-filled as confirmatory hypotheses.

### Cognitive review checkpoint B — design red team

Before looking at substantive outcomes, recruit independent reviewers such as:

- methods/statistics reviewer;
- data auditor;
- causal skeptic / alternative-explanation reviewer;
- baseline-and-simplicity critic.

Their job is to break the design while repair is still cheap. Freeze the resulting issue ledger and dispositions before the main analysis.

## Stage 6 — Acquire and audit inherited evidence

Before modelling:

- record source, version/date, licence and retrieval method;
- hash or otherwise identify frozen inputs where practical;
- inspect missingness, duplicates, schema drift and coverage;
- test whether the available fields actually operationalize the intended constructs;
- document any selection process that created the dataset;
- separate pre-outcome variables from downstream labels to prevent leakage.

A dataset that cannot answer the question should kill or redesign the study rather than quietly redefine the question around available columns.

## Stage 7 — Conduct the analysis

Run the simplest credible baseline first.

Then run the proposed method and required stress tests. Preserve code, parameters and intermediate artefacts needed for reproduction.

At minimum report:

- descriptive structure of the evidence;
- baseline result;
- proposed-method result;
- uncertainty;
- robustness / sensitivity analyses;
- important subgroup or heterogeneity findings when justified;
- null and negative findings;
- model failures or data defects;
- what the evidence cannot establish.

Do not hide the analysis path that makes the preferred interpretation weaker.

### Cognitive review checkpoint C — result attack

After a first complete analysis but before the narrative is fixed, recruit independent reviewers such as:

- methods/statistics reviewer;
- baseline-and-simplicity critic;
- causal skeptic;
- reproducibility/computational reviewer.

Where feasible, have the reproducibility reviewer regenerate key results from a clean environment or independent implementation. Require reviewers to state what evidence would make them withdraw each criticism.

## Stage 8 — Adversarial result review

Before writing the paper as a success story, attack the result again.

Ask:

- What alternative explanation survives?
- What analysis choice most threatens the conclusion?
- Does the effect survive reasonable specifications?
- Does a simpler baseline remove the claimed contribution?
- Are downstream outcomes being mistaken for ground truth?
- How dependent is the result on one dataset, venue, field or time period?
- What would an expert critic attack first?
- Has the analysis discovered something different from the original idea?

The final claim should follow the evidence, even when that means changing the paper’s title or retiring the original thesis.

## Stage 9 — Draft the terminal research object

Write the paper, preprint, research note, replication report, benchmark note, null result or retirement record that the evidence actually supports.

The draft must distinguish:

- findings from interpretation;
- confirmatory from exploratory analyses;
- evidence from proxy assumptions;
- machine contribution from epistemic authority;
- limitations that bound the result from defects that invalidate it.

## Stage 10 — Mandatory complete-paper cognitive swarm review

Every paper or preprint receives an adversarial review of the **finished manuscript** before publication.

Recruit a broad independent swarm. For a substantive paper, normally include at least:

- refreshed prior-art hunter;
- methods/statistics reviewer;
- theory/construct critic where relevant;
- adversarial domain referee;
- claim-to-evidence reviewer;
- reproducibility reviewer;
- hostile final referee instructed to find a publish-blocking flaw.

Reviewers should not see one another's outputs until independent reviews are captured. Where practical, vary model families, prompt framing, source subsets and analytic routes to reduce correlated errors.

Every reviewer returns a structured verdict: `no-blocker`, `minor`, `major`, or `fatal`, together with evidence, affected claim/analysis, a discriminating test or repair, confidence, and conditions under which the reviewer would withdraw the objection.

Do **not** majority-vote. A single well-supported fatal issue must receive an explicit disposition:

- fix and rerun;
- run a discriminating test;
- narrow the claim;
- add a limitation when the issue does not destroy the inference;
- obtain human domain authority;
- or retire the paper.

A paper is not `publishable` while an unresolved fatal issue remains.

The detailed orchestration protocol is defined in `docs/COGNITIVE_REVIEW_SWARM_PROTOCOL.md`.

## Stage 11 — Cost and scarcity account

Each completed investigation should report its research cost where measurable.

Track separately:

- human-curator time;
- machine/API/compute cost;
- cognitive-review swarm cost or usage band;
- paid data or software cost;
- storage/infrastructure cost;
- external expert or collaborator time;
- material or participant cost;
- important unpriced constraints.

Do not invent retrospective precision. Mark unknown historical costs as unknown. For new studies, measure them prospectively when practical.

Also record:

- which initial scarcity was displaced;
- what abundant resource displaced it;
- what bottleneck appeared next;
- the irreducible residual human role;
- whether additional machine reviewers were still finding new material defects near the end of the process.

This last quantity is a practical saturation signal: parallel cognitive review should expand while marginal defect discovery remains useful, then stop when extra reviewers mostly repeat already-known concerns.

## Stage 12 — Terminal publication decision

Every serious investigation should terminate in a durable research-corpus object rather than disappearing into chat history.

Valid terminal products include:

1. **paper / preprint** — a distinct contribution with evidence sufficient for a scholarly claim;
2. **research note** — useful synthesis, operational insight or bounded analysis that does not warrant a full paper;
3. **replication / robustness report** — a meaningful confirmation, failure or qualification of existing work;
4. **benchmark / dataset / software-method note** — reusable research infrastructure whose contribution is demonstrated;
5. **null / negative result** — the tested claim did not survive;
6. **retirement record** — prior art or analysis removes the need for the local concept;
7. **handoff package** — a residual claim is potentially valuable but requires expertise, authority or evidence unavailable to the programme.

“Still thinking about it” is not a terminal state.

## No-idle-queue rule

The Possibility Portfolio may preserve abundant ideas cheaply, but an idea explicitly raised as a candidate paper or research project receives immediate screening.

If the first stages show no viable contribution, retire or demote it promptly.

If a credible 1 + machine study exists and the required evidence is available, proceed into execution rather than adding another planning item.

If execution is blocked by an irreducible external dependency, record:

- the exact blocker;
- why inherited evidence cannot displace it;
- the minimum external action required;
- the evidence that would justify spending that scarce resource.

A blocker should be a specific dependency, not a euphemism for an unattended queue.

## Research Corpus record

Every screened research candidate that reaches substantive prior-art or empirical work should receive a structured corpus record containing at least:

- stable ID and title;
- question;
- lifecycle status;
- prior-art outcome;
- adversarial outcome;
- chosen design;
- source data / evidence;
- result or current finding;
- cost status;
- scarcity transition;
- cognitive-review checkpoints completed;
- reviewer roles / independent runs;
- fatal and major issues discovered and their dispositions;
- reproduction status;
- final prepublication review status;
- disposition;
- next action if non-terminal;
- links to paper, note, protocol, code, data, provenance, review summary or retirement record.

The public corpus should make negative and narrowed work visible alongside successful papers.

## Conversation behaviour

For Agalmic Research discussions, the default machine-collaborator behaviour is therefore:

> **When a paper idea or potentially research-worthy claim appears, begin the lifecycle automatically: search prior art, recruit independent cognitive critics, run the adversarial null test, refine the contribution, find the strongest credible 1 + machine design, red-team that design, identify and audit source data, conduct feasible analysis, independently attack and reproduce the result, draft the terminal research object, run a mandatory complete-paper adversarial swarm, account for cost and scarcity displacement, and publish or retire the appropriate object. Do not ask for another `proceed` merely to advance between these ordinary stages.**

Pause only for a genuinely irreducible decision, permission boundary, safety issue, unavailable external resource, or human judgment whose substitution would change the meaning of the research.
