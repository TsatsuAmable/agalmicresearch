# One + Machine Research Method

Version: 0.1  
Status: operating research method  
Date: 9 September 2026

## Purpose

Agalmic Research is a research programme with one primary human investigator and machine collaborators. Its method should exploit that structure rather than imitate a laboratory it does not possess.

The default is therefore:

> **Inherit evidence before creating it. Reanalyse before recollecting. Simulate before constructing. Replicate before extending. Spend scarce human expertise only where it can change the answer.**

Original research does not require original data collection. Contribution may lie in the question, synthesis, identification strategy, formalism, benchmark, reanalysis, robustness test, simulation, software, negative result or integration of previously disconnected evidence.

## Method hierarchy

Prefer methods roughly in this order when they can answer the question:

1. lineage review / systematic or scoping review;
2. evidence map or meta-analysis;
3. reanalysis of open or inherited datasets;
4. bibliometric / scientometric analysis;
5. replication and robustness testing;
6. retrospective computational experiments;
7. simulation and formal modelling;
8. benchmark construction from existing evidence;
9. small targeted expert validation or new data collection only for residual questions not answerable above.

This is a search order, not a rigid ladder. Some questions require a different method immediately.

## Scarcity Displacement Loop

Every substantial research task should run a second loop alongside the object-level inquiry.

### 1. Identify the binding scarcity

Ask what is presently limiting useful progress. Candidate scarcities include:

- human time and attention;
- domain expertise and epistemic authority;
- participant access;
- expert review capacity;
- literature coverage;
- data access, cleaning and integration;
- statistical or mathematical capability;
- software implementation capacity;
- compute, storage or money;
- coordination and project management;
- validation, replication and criticism;
- comprehension / assimilation;
- real-world implementation or institutional access.

Do not assume the most visible difficulty is the binding one.

### 2. Measure or operationalize it

State evidence that the constraint is actually binding. Prefer observable proxies: queue length, delay, expert-hours, unresolved claims, repeated failure, coverage gaps, analysis cost, error rate, inability to defend a claim, compute/storage limits, or dependency on unavailable collaborators.

### 3. Search inherited abundance

Before acquiring a new collaborator or collecting new data, search for already-abundant substitutes or complements:

- open datasets;
- public reviews and decisions;
- published effect estimates;
- existing benchmarks;
- public code and formal tools;
- scholarly graphs;
- machine-readable standards;
- simulation;
- synthetic controls or retrospective labels;
- automated literature / provenance / data-processing pipelines;
- machine cognition for search, critique, coding, translation and hypothesis generation.

### 4. Choose a displacement strategy

Possible actions:

- **remove** the need for the scarce input;
- **substitute** a machine/open-data mechanism for part of it;
- **augment** the scarce human so each unit has greater yield;
- **defer** human involvement until uncertainty or risk crosses a threshold;
- **batch** or compress the work presented to humans;
- **route** only candidates requiring a specific missing capability;
- **reuse** prior human effort embedded in datasets, reviews, standards or software;
- **learn** enough to reduce dependence on the scarce collaborator;
- **accept** the scarcity when substitution would invalidate the claim.

### 5. Test displacement

Compare the new mechanism with a simpler baseline. Measure whether the targeted scarcity actually became less binding and whether quality, fairness, calibration or safety degraded.

A speedup that creates hidden false negatives, authority laundering or downstream rework is not successful displacement.

### 6. Identify the next scarcity

Every successful abundance intervention can move the bottleneck. Record what now limits progress.

This recurrence is central:

> **A cognitive machine should not merely perform assigned work. It should help observe the work system, identify scarce complements to its own abundance, propose ways to relax them, and test whether the bottleneck moved.**

## Human boundary

Machine displacement is not an instruction to remove humans indiscriminately.

Human participation remains irreducible or deliberately retained where the claim depends on:

- normative or value judgments;
- lived experience or stakeholder preference;
- legal or institutional authority;
- real-world consequences that cannot be inferred retrospectively;
- domain warrant for which no defensible proxy exists;
- new measurements unavailable in inherited data;
- adversarial independent replication;
- accountability that cannot be delegated to a model.

The method should make these residual human requirements more legible and better targeted.

## Research substrate inventory

### Peer review and expert attention

- PeerRead: 14.7K paper drafts, accept/reject decisions and 10.7K textual reviews.
- OpenReview: public submissions, reviews, meta-reviews, rebuttals and decisions can be retrieved where venue visibility permits.

Uses: handoff triage, reviewer disagreement, escalation policies, false-negative auditing, credential/status effects where metadata permits, robustness of review allocation.

### Scholarly system

- OpenAlex: large open scholarly graph of works, authors, institutions, topics, funders, citations and related metadata; complete public snapshots are available.

Uses: epistemic abundance, publication/citation growth, collaboration, concentration, field expansion, distributed discovery, uptake and recognition lags.

### Existing research corpora

Use field-specific repositories, published supplementary data, benchmark datasets, replication archives and open code as inherited experimental infrastructure.

## Candidate research directions

These are **options, not simultaneous commitments**.

### A. Expert-Attention Handoff Triage

Retrospective benchmark using historical peer-review data. Ask whether candidate-level routing can improve useful review yield under simulated expert scarcity without destructive false negatives.

**Priority:** first research implementation of this method.

### B. Epistemic abundance scientometrics

Measure whether growth in candidate scholarly output is associated with changing review, citation, recognition, collaboration or concentration patterns. Avoid interpreting publication count alone as knowledge abundance.

### C. Reviewer disagreement as scarce epistemic information

Treat disagreement rather than majority decision as an outcome. Test whether triage mechanisms preferentially erase controversial candidates and whether disagreement predicts later influence, correction or instability.

### D. Distributed discovery and delayed recognition

Use citation and textual lineage graphs to study how precursor contributions are recognized, recombined and credited over time.

### E. Displaced-scarcity historical cases

Construct comparable case studies from existing economic and technological data in which one input became dramatically cheaper. Test whether complementary constraints became measurably more binding without assuming a new universal law.

### F. Authorial-capacity secondary studies

Reanalyse existing human-AI studies for divergence between assisted output quality, calibration, explanation, delayed retention and unaided transfer. Search for datasets before collecting new participants.

### G. Nemosyne / Moneta benchmark research

Use public datasets with known structure, anomalies or relationships to test representation selection and analytical efficiency before expensive VR user studies.

### H. Research-system self-study

Instrument Agalmic Research itself: time spent, unresolved authority gaps, research queues, machine contribution, review latency, abandoned branches and capability transfer. Treat this as operational evidence, not a universal population study.

## Programme rule

A new research direction should preferentially answer four questions before activation:

1. What is the object-level research question?
2. What existing evidence or data can answer most of it?
3. What scarce human input remains after machines and inherited evidence are used well?
4. What result would cause us to stop, retire the claim or choose a different method?

If these cannot be answered, preserve the idea as an option rather than turning it into another active project.
