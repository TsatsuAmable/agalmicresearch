# Research Provenance Protocol

Version: 0.1
Status: exploratory operating protocol
Date: 7 September 2026

## Purpose

Agalmic Research uses machine cognition extensively. Git history records *what changed*, but not enough of *why an idea appeared*, *who contributed which part*, *who can defend which claim*, or *how a draft emerged from dialogue, criticism and revision*.

This protocol creates an examinable chain of intellectual custody for research objects. It treats the research process as a navigable graph rather than a flat author list.

The governing distinction is:

> **Contribution provenance and epistemic authority are separate records.**

A person or machine may materially contribute to an idea without possessing authority over its truth. A domain expert may later validate or reformulate the idea without becoming its originator.

## Core rules

1. **Preserve initiation.** Record who first introduced the question, distinction, conjecture or direction when that can be established.
2. **Do not launder authority into credit.** Later verification does not rewrite origination.
3. **Do not launder credit into authority.** Origination does not establish correctness, expertise or defensibility.
4. **Record machine contributions materially, not ceremonially.** If an AI system supplied terminology, structure, derivation, criticism, drafting or search, record those roles.
5. **Record human decisions.** Selection, rejection, reframing, prioritisation, publication and acceptance of responsibility are substantive contributions.
6. **Prefer evidence pointers over retrospective memory.** Link claims about contribution to conversation snapshots, quoted prompts, source files, commits, issues, notes or other durable records.
7. **Version the graph.** Provenance is corrigible. If an attribution is disputed or new evidence appears, append a correction rather than silently rewriting history.
8. **Keep epistemic status claim-sensitive.** A contributor can possess authority over one part of a work and not another.

## Actor types

- `human` — a person participating in origination, framing, evaluation, drafting, verification or publication.
- `ai_system` — a model or machine system materially contributing to search, reasoning, drafting, criticism, analysis or transformation.
- `external_source` — a paper, dataset, institution, codebase, interview, archive or other source that contributes evidence or prior art.
- `collective` — a team, review panel, community or institution whose contribution is best recorded jointly.

## Contribution roles

The vocabulary is intentionally richer than “author.” A research object may record any of the following:

- `initiator` — introduces the original question, anomaly, idea or direction.
- `framer` — turns an intuition into a tractable research question or conceptual distinction.
- `search_director` — chooses search branches, prompts, constraints and stopping conditions.
- `generator` — produces candidate arguments, models, text, code or representations.
- `selector` — chooses which candidates merit further development.
- `developer` — formalises, extends or strengthens a candidate.
- `terminology` — coins or proposes a useful term, label or compact formulation.
- `synthesizer` — joins previously separate ideas into a coherent structure.
- `critic` — identifies objections, failure modes, counterexamples or missing evidence.
- `verifier` — tests correctness, reproducibility, robustness or provenance.
- `domain_steward` — supplies relevant expertise and takes responsibility for interpretation in a domain.
- `editor` — materially shapes exposition without claiming origination of the underlying idea.
- `decision_maker` — accepts, rejects, prioritises or authorises publication of a research direction.
- `realizer` — turns sufficiently warranted knowledge into software, policy, experiment, institution or product.

These roles are descriptive, not rankings.

## Epistemic authority record

Authority is recorded separately for a claim or cluster of claims. Suggested statuses:

- `unassessed`
- `exploratory`
- `curator_defended`
- `externally_reviewed`
- `empirically_supported`
- `formally_verified`
- `reproduced`
- `contested`
- `superseded`

Each authority assertion should state its basis, such as direct expertise, adversarial defence, empirical evidence, formal proof, independent replication or peer review.

No global “trust score” is required or implied.

## Discovery-event model

Each meaningful intellectual transition is recorded as a node. Examples include:

- question
- intuition
- claim
- principle
- conjecture
- criticism
- evidence
- decision
- draft
- paper
- software artefact
- experiment
- institutional proposal

Nodes are connected with typed edges such as:

- `inspired_by`
- `derived_from`
- `formalizes`
- `names`
- `supports`
- `criticizes`
- `contradicts`
- `extends`
- `supersedes`
- `implemented_as`
- `published_as`
- `validated_by`
- `handoff_to`

This turns provenance into a graph that can later be rendered as a navigable “memory palace” of discovery.

## Minimum record for a research object

Every substantial paper, draft or software research object should eventually carry:

```yaml
research_object_id: AR-YYYY-NNN
title: ...
version: ...
epistemic_status: ...
contributors:
  - actor_id: ...
    actor_type: human | ai_system | external_source | collective
    roles: [...]
    contribution: ...
claims:
  - claim_id: ...
    statement: ...
    authority_status: ...
    authority_basis: ...
provenance_events: [...]
sources: [...]
repository:
  path: ...
  commit: ...
```

## Evidence and chain of custody

Git commits are necessary but not sufficient. Where possible, each research event should point to one or more of:

- a dated conversation export or transcript fragment;
- a Git commit SHA and file path;
- an issue, pull request or review comment;
- a source URL, DOI or archive identifier;
- a dated notebook entry;
- a generated artefact hash;
- an external review or replication record.

For AI-assisted sessions, the preferred record should include the provider/product, model when known, date, the material human prompt or question, a short description of the machine contribution, and the human decision taken afterwards.

A future automated system should capture these events at creation time. Retrospective reconstruction should be labelled as such.

## Attribution policy for current Agalmic Research work

For the September 2026 epistemic-stewardship sequence, the initial reconstruction uses the conversation record and repository history available at the time of writing.

Important examples:

- The human curator initiated the concern that machine-assisted work could exceed their ability to defend it and explicitly connected that concern to Dunning–Kruger and authorial capacity.
- ChatGPT proposed the compact formulation **“Epistemic authority should not exceed defensibility”** and developed the label **Principle of Defensible Stewardship**; the human curator selected and adopted the framing.
- The human curator introduced the deep-future possibility that epistemic authority itself may diminish on the human scale and suggested mathematics as an early domain in which this could become visible.
- ChatGPT formulated that line as the **Human-Scale Epistemic Horizon** conjecture.
- The human curator introduced the distinction between the initiator of an idea and those who possess epistemic authority over it, including the need to harness valuable low-authority contributions rather than discard them.
- ChatGPT formulated **“Origin deserves credit. Authority requires warrant,”** named **epistemic handoff**, and developed the **Epistemic Uptake Constraint** from that direction.
- The resulting papers are therefore not accurately described as either solely human-authored or solely machine-generated. They are machine-assisted research objects with identifiable human initiation, selection and publication decisions and identifiable machine contributions to terminology, synthesis, drafting, criticism and formalisation.

These attributions are themselves open to correction if better evidence becomes available.

## Publication contribution statement

Future papers should include a compact contribution declaration, for example:

> **Contribution provenance.** The human curator initiated the core research question, selected the research direction, supplied specified conjectures and authorised publication. OpenAI ChatGPT materially contributed to terminology, conceptual synthesis, drafting, adversarial criticism and literature discovery. External reviewers and sources are credited separately. These contribution roles do not imply equivalent epistemic authority over every claim.

The paper should link to its full graph record for inspection.

## Toward a navigable research memory palace

The long-term goal is not a bureaucratic ledger. It is a usable map of discovery.

A reader should be able to enter at any paper, principle or claim and navigate backward to:

- the question that produced it;
- competing formulations that were rejected;
- the human and machine contributors involved;
- criticism and evidence that changed it;
- the point at which it became a draft or publication;
- later work that inherited or challenged it.

The same graph should allow forward navigation from a raw intuition to every paper, experiment, implementation and institution that eventually descends from it.

That is the research analogue of a memory palace: not merely a store of conclusions, but a navigable structure of how knowledge was discovered.
