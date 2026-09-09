# Cognitive Review Swarm Protocol

Version: 0.1  
Status: default quality-control layer for research papers  
Date: 9 September 2026

## Purpose

Agalmic Research is a one-human-curator research programme with access to abundant cognitive machinery. That asymmetry should be used not only to generate and execute work, but to attack it repeatedly from independent directions.

The default research lifecycle therefore recruits multiple cognitive reviewers at selected checkpoints. Their purpose is not to manufacture consensus or substitute for authoritative human peer review. Their purpose is to increase search breadth over failure modes, reduce dependence on one model trajectory, surface hidden assumptions early, and make scarce human curator attention land on disagreements that matter.

> **Parallel cognition should widen criticism before the curator narrows judgment.**

## Core rule: independence before synthesis

A review swarm is useful only when its members are given partially independent epistemic jobs.

Do not ask ten agents, "Is this paper good?" and average the answers.

Instead:

1. freeze the artefact or study state to be reviewed;
2. create a common evidence packet;
3. assign different reviewer mandates;
4. where practical, hide the drafter's preferred conclusion from reviewers whose task does not require it;
5. collect reviews separately before reviewers see one another's outputs;
6. synthesize conflicts only after independent reviews are complete;
7. preserve minority objections, especially objections tied to falsifiable failure modes;
8. require the curator or designated synthesis agent to record dispositions rather than silently smoothing disagreement away.

Model diversity is desirable when available, but role diversity and context independence are mandatory even when the same underlying model family must be reused.

## What counts as a cognitive reviewer

A reviewer may be:

- a separate model or model family;
- a separate session of the same model with an independent role and no hidden drafting context;
- a specialized research, statistics, coding, literature, or formal-reasoning agent;
- an external machine service capable of reproducing or critiquing an analysis;
- a human expert when the question requires authority that cognitive machinery cannot supply.

The word *reviewer* records a critical function, not epistemic authority. Machine review can discover defects. It cannot by itself convert a contested claim into domain warrant.

## Standard swarm roles

Use only roles relevant to the paper, but normally recruit at least four distinct mandates for a substantive empirical paper.

### 1. Prior-art hunter

Goal: find the strongest literature that makes the paper unnecessary, derivative, incorrectly framed, or misattributed.

Questions:

- What is the closest antecedent, not merely related work?
- Has the claimed mechanism already been named or tested elsewhere?
- Are there adjacent fields the authors have failed to search?
- Does a review, benchmark, theorem, dataset, or negative result already answer the question?
- Which novelty sentences should be weakened or deleted?

### 2. Theory / construct critic

Goal: attack conceptual coherence and measurement validity.

Questions:

- Is the construct distinct from established constructs?
- Do operational measures actually instantiate it?
- Are proxies being mistaken for the phenomenon?
- Is any definition circular, tautological, or post-hoc?
- What alternative conceptualization better explains the observations?

### 3. Methods and statistics reviewer

Goal: attack identification, statistical reasoning, uncertainty, multiplicity and robustness.

Questions:

- Is the design capable of answering the stated question?
- Are assumptions testable and reported?
- Are sample size, power, calibration and uncertainty adequate?
- Are researcher degrees of freedom controlled?
- Would reasonable alternative specifications erase the result?
- Is the paper making causal claims from associational evidence?

### 4. Data auditor

Goal: attack the evidence substrate before trusting the analysis.

Questions:

- What selection process created the data?
- Are there duplicates, missingness, leakage, schema drift or label contamination?
- Can the data reproduce the claimed unit of analysis?
- What records are systematically absent?
- Are joins, mappings or derived variables reproducible?

### 5. Baseline and simplicity critic

Goal: determine whether the special mechanism earns its complexity.

Questions:

- What is the strongest simple baseline?
- Can a rule, heuristic, linear model or established method achieve the same result?
- Is performance gain practically meaningful rather than statistically decorative?
- Does complexity merely create interpretive freedom?

### 6. Causal skeptic / alternative-explanation reviewer

Goal: construct rival explanations that fit the evidence.

Questions:

- What confounding, selection, survivorship, temporal or institutional mechanism could generate the same pattern?
- What negative control or falsification test would distinguish them?
- Which interpretation remains viable after the authors' preferred explanation is removed?

### 7. Adversarial domain referee

Goal: review the paper as a skeptical specialist asked to recommend rejection.

Questions:

- What would make a domain expert stop reading?
- Which literature omissions are embarrassing rather than cosmetic?
- Which claims exceed the curator's defensible authority?
- What disciplinary convention or technical detail has been misunderstood?
- What single fatal flaw would justify rejection?

### 8. Reproducibility / computational reviewer

Goal: independently reproduce as much of the paper as possible from frozen artefacts.

Tasks:

- run code from a clean environment where feasible;
- check dataset hashes, seeds, parameters and dependency versions;
- regenerate key tables and figures;
- compare reported values with outputs;
- identify manual steps and undocumented transformations;
- attempt a minimal independent reimplementation of the main result when practical.

### 9. Writing / claim-to-evidence reviewer

Goal: inspect every substantive claim for evidence alignment rather than polish alone.

Questions:

- Does each conclusion follow from the reported result?
- Are limitations stated where the inference changes category?
- Are abstracts and titles stronger than the body supports?
- Are null results and failed robustness checks represented fairly?
- Is rhetoric compensating for weak evidence?

### 10. Red-team editor / hostile final referee

Goal: attack the complete paper immediately before publication.

This reviewer should behave as though acceptance depends on finding a reason to reject. It should produce:

- fatal flaws;
- major revisions;
- minor revisions;
- missing citations or prior art;
- unsupported claims;
- reproducibility failures;
- likely reviewer objections;
- one-sentence strongest case against publication;
- one-sentence strongest surviving contribution if the paper is repaired.

## Review checkpoints

### Checkpoint A: after prior-art screening

Recruit at least:

- prior-art hunter;
- theory / construct critic;
- adversarial domain referee.

Purpose: kill derivative or incoherent ideas before analysis cost accumulates.

### Checkpoint B: after study design, before substantive analysis

Recruit at least:

- methods/statistics reviewer;
- data auditor;
- causal skeptic;
- baseline critic.

Purpose: freeze a design that can fail cleanly before outcome fishing begins.

### Checkpoint C: after first complete analysis

Recruit at least:

- methods/statistics reviewer;
- baseline critic;
- causal skeptic;
- reproducibility reviewer.

Purpose: determine whether the apparent result survives independent attack before narrative lock-in.

### Checkpoint D: complete-paper prepublication review

Mandatory for any paper/preprint.

Recruit a broad swarm including at minimum:

- prior-art hunter refreshed against current literature;
- methods/statistics reviewer;
- domain referee;
- claim-to-evidence reviewer;
- reproducibility reviewer;
- hostile final referee.

Do not publish until all fatal findings are either fixed, falsified, explicitly accepted as limitations that do not destroy the contribution, or used to retire/narrow the paper.

## Review packet

Each swarm run receives a versioned packet. Do not hand reviewers an unbounded conversation transcript unless their task requires provenance reconstruction.

The packet should contain:

- paper/study ID and version/hash;
- research question and current claim;
- novelty status;
- frozen study protocol;
- data-source manifest and licences;
- analysis code / reproduction command where available;
- key tables and figures;
- declared limitations;
- known unresolved questions;
- the reviewer's role-specific brief.

For independence, omit the drafting agent's self-justification and other reviewers' conclusions until the synthesis stage unless they are necessary evidence.

## Structured review output

Every cognitive reviewer should return:

- reviewer role;
- artefact version reviewed;
- verdict: `no-blocker`, `minor`, `major`, or `fatal`;
- top three concerns;
- evidence for each concern;
- exact claim, analysis, table, figure, or method affected;
- proposed discriminating test or repair;
- confidence in the criticism;
- what evidence would make the reviewer withdraw the criticism;
- any detected novelty/prior-art issue;
- any required human-expert escalation.

The reviewer should prefer falsifiable objections over vague dislike.

## Synthesis without majority voting

Do not count votes.

A single well-supported fatal criticism outweighs ten generic approvals.

The synthesis agent should cluster overlapping critiques, identify genuinely independent concerns, rank them by consequence and evidential support, and generate an issue ledger with one of these dispositions:

- `accept-fix`;
- `test`;
- `reject-critique` with evidence;
- `narrow-claim`;
- `add-limitation`;
- `requires-human-authority`;
- `retire-paper`.

Every `fatal` review must receive an explicit disposition before publication.

## Correlation controls

Massive parallelism can create the illusion of independent confirmation when reviewers share the same training priors, sources, prompts, or hidden context.

Mitigate this by varying:

- model families where available;
- reviewer roles;
- prompt framing;
- source subsets;
- order of evidence presentation;
- whether the preferred hypothesis is disclosed;
- analytic route, for example parametric vs non-parametric or predictive vs causal framing;
- reproduction implementation where feasible.

Record when reviewers are likely to be correlated. Do not translate agent count directly into confidence.

## Cost-aware scaling

Use cognitive abundance aggressively, but not theatrically.

Scale the swarm according to expected information value:

- trivial research note: 2 to 3 targeted reviewers;
- bounded empirical note: 4 to 6;
- substantive paper/preprint: 6 to 10 across checkpoints;
- high-stakes or unusually novel claim: additional independent model families, reproduction agents, and targeted human expert review.

Stop adding reviewers when new reviews are no longer discovering materially new failure modes. Track marginal defects found per additional reviewer or compute-cost band when practical.

## Human curator role

The curator does not need to personally redo every machine review. The irreducible role is to:

- choose and defend the research question;
- decide which claims Agalmic Research will stand behind;
- inspect high-consequence disagreements;
- recognize when machine reviewers are correlated or outside their competence;
- decide when genuine human domain authority is required;
- approve final publication, narrowing, handoff or retirement.

## Corpus integration

Each research-corpus record should preserve a compact review summary:

- checkpoints completed;
- reviewer roles recruited;
- number of independent review runs;
- fatal/major issues discovered;
- issues resolved, accepted or outstanding;
- whether an independent reproduction was attempted;
- whether human expert review remains necessary;
- final prepublication review status.

Detailed machine transcripts need not all be public. The public corpus should record enough to show that review occurred and what materially changed because of it.

## Default instruction for orchestrators such as Realise

When executing an Agalmic Research paper lifecycle, recruit independent cognitive reviewers at the specified checkpoints without waiting for the curator to request each review individually. Run role-specific reviews in parallel where the environment permits. Do not expose one reviewer's conclusions to another until independent outputs are captured. Synthesize disagreements into a repair/test ledger, execute feasible repairs and rerun affected checks.

Before publication, run the mandatory complete-paper adversarial swarm and do not mark the paper publishable while an unresolved fatal issue remains.

> **Use machine abundance not just to write faster, but to make it cheap for the work to encounter many intelligent ways of being wrong.**
