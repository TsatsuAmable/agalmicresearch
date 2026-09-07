# Epistemic Artefact Intake

Version: 0.1  
Status: experimental companion protocol  
Date: 7 September 2026

## Purpose

The intake layer exists to preserve potentially valuable outputs of human-machine search **before** the project has decided whether they are ideas, validated results, knowledge, publications or active commitments.

Its design objective is simple:

> **Capture quickly. Judge deliberately. Promote sparingly.**

The Memory Palace preserves discovery provenance. The Possibility Portfolio manages commitment. The **Epistemic Artefact Intake** sits between emergence and judgment so potentially valuable artefacts can be retained with almost no delay.

## What belongs in intake

Create an intake record when a session produces a materially distinct object that may carry epistemic value, for example:

- a conjecture;
- a conceptual distinction;
- a mathematical object or proof candidate;
- a model;
- an experiment or result;
- a dataset or transformed dataset;
- a causal hypothesis;
- a mechanism;
- an algorithm;
- a representation;
- an unexpected counterexample;
- a machine-generated result that no current human participant fully understands;
- a synthesis whose novelty or warrant has not yet been assessed.

Do not create an artefact for every sentence or stylistic reformulation.

## Minimal intake record

An intake record should be cheap enough to create at discovery time. Record only what can be stated without pretending to know more than is known:

- stable `id`;
- capture date or order;
- title;
- artefact kind;
- origin session;
- concise summary;
- provenance pointer;
- warrant status;
- understanding / assimilation status;
- novelty status;
- publication sensitivity;
- commitment state;
- next route;
- related possibility, research object or handoff where one exists.

`unknown`, `unassessed`, `opaque-to-current-curator`, `partially-assimilated` and similar explicit states are valid. They are preferable to invented certainty.

## Intake is not promotion

An artefact entering intake does **not** imply:

- truth;
- novelty;
- knowledge;
- human understanding;
- authorship;
- discovery credit;
- publication priority;
- Active Frontier status;
- implementation priority.

The purpose is to separate **preservation cost** from **attention cost**.

## Routing

Every artefact should eventually take one of a small number of routes:

- lineage review;
- validation;
- assimilation / explanation;
- experiment;
- formalization;
- handoff;
- possibility portfolio;
- publication review;
- IP review;
- realization;
- merge with an existing artefact;
- park;
- retire.

Routing may be delayed. Loss of provenance should not be.

## Relationship to knowledge

This protocol does not settle the philosophical definition of knowledge. It adopts an operational distinction useful for research management:

`possibility -> search -> epistemic artefact -> warrant -> assimilation -> capability -> reachable frontier`

The stages may branch, loop or be distributed across different agents. Strong warrant need not imply that a particular human understands the result. Human understanding need not imply strong warrant. Capability can sometimes precede complete assimilation. Those relationships are research questions, not assumptions hidden by the data model.

## Relationship to constitutional attention

Low-cost intake is one component of constitutional attention. If machine search becomes abundant, humans should not have to inspect every output merely to prevent its loss.

A constitutional search system can capture artefacts automatically, attach provenance, run low-risk evaluation and route routine cases. Scarce human attention is then reserved for constitutional design, contested values, high-impact or irreversible decisions, surprising anomalies, unresolved authority and cases that cross escalation thresholds.

## Short activation

> **Activate Epistemic Artefact Intake. When a materially distinct potentially valuable research output appears, capture it immediately with a provenance pointer and explicit warrant, understanding, novelty, sensitivity, commitment and routing states. Unknown and incomplete states are allowed. Intake does not imply knowledge, truth, novelty or commitment. Preserve first; spend attention only when routing, validation, assimilation, handoff or promotion justifies it.**
