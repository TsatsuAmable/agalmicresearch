# Agalmic Research

**Agalmic Research** is an open practice of disciplined inquiry and building that asks how available abundance can be converted into durable capability by identifying and relaxing real constraints.

Current compact form:

> **Use abundance to expand capability. Begin with the constraint in front of you.**

And a second operating maxim:

> **Seek contribution before novelty. Seek novelty only where contribution requires discovery.**

The programme now begins inwardly. It uses the practitioner's real work as the first testbed: identify what is actually limiting useful action, inherit the best existing knowledge and tools, apply abundant resources such as machine cognition against that constraint, and test whether understanding, judgment, skill or practical capacity increased durably.

Live site: **https://agalmicresearch.org**

## Current applications

The first capability domains are deliberately attached to real needs:

- **Scholarliness and epistemic judgment** — source evaluation, conceptual precision, calibration, synthesis, viva-style defence, authority boundaries and delayed unaided transfer.
- **Software development** — architecture, code reading, debugging, testing, performance, reliability, security and deeper systems understanding alongside AI-assisted delivery.
- **Engineering leadership** — technical strategy, prioritization, delegation, coaching, stakeholder alignment, risk leadership and judgment under uncertainty.
- **Nemosyne** — rapid AI-assisted discovery first, followed by epistemic reconstruction and selective rebuilding of the durable core.

The capability map is intentionally non-scalar. Different capabilities require different evidence and have different legitimate handoff boundaries.

## Discovery, assimilation and ownership

A recurring distinction is:

1. **Discovery** — use AI aggressively to search, prototype, compare and expose adjacent possibilities. Outputs are provisional candidates.
2. **Assimilation** — reconstruct surviving ideas, inspect lineage and evidence, surface assumptions, test understanding and identify missing expertise.
3. **Ownership** — make durable decisions and critical internals explainable, testable and maintainable by those accountable for them, with appropriate handoff where necessary.

> **Prototype to discover. Reconstruct to understand. Operate only what can be responsibly defended or appropriately handed off.**

This distinction is especially important for Nemosyne. Getting trapped in implementation detail too early can reduce discovery breadth; accepting machine-generated internals indefinitely can create an understanding gap. The project therefore permits those two concerns to be handled at different times.

## Research as method, not required product

Research remains important because it constrains self-deception:

**question → lineage → explicit claim → method → evidence or argument → criticism → epistemic status → revision or handoff**

But a paper is only one possible result.

Useful outcomes also include:

- stronger personal capability;
- reuse of an existing theory, tool or curriculum;
- a working implementation;
- an open protocol or teaching method;
- a negative result that closes an unproductive branch;
- a clearer authority boundary or expert handoff;
- a contribution back to infrastructure inherited from others;
- a public research artefact where publication genuinely adds value.

Prior art is infrastructure. Finding that someone has already solved part of the problem is a gain, not a defeat.

## Scholarliness and authority

The programme is interested in increasing the frontier of human scholarliness even as AI capability rises.

That can include subject mastery, conceptual precision, source and lineage judgment, methodological competence, argument analysis, calibration, synthesis, transfer and defensibility.

These are trainable capabilities. **Epistemic authority is not a score awarded by the training system.** It remains claim-sensitive and must not exceed the warrant supplied by evidence, methods, relevant expertise, criticism and appropriate verification or handoff.

## What this repository contains

This repository is both the source of the public website and part of the evolving record. It contains:

- the current Personal Capability Practice;
- earlier and current research papers, notes, drafts and literature reviews;
- intellectual-lineage and prior-art records;
- provenance and epistemic-handoff machinery;
- the Possibility Portfolio and Active Frontier;
- the semantic knowledge index used by Explore;
- the source for agalmicresearch.org;
- open tools extracted from the work, including `astro-agalmic`.

Earlier definitions and discarded framings are intentionally preserved where practical. The repository should show how the programme changed rather than presenting its latest wording as if it had always existed.

## Knowledge architecture

The public site separates:

- **Practice** — the current inward capability-building programme;
- **Explore** — the wider knowledge and research record;
- **Publications** — durable outward outputs;
- **Frontier** — possibilities receiving active commitment;
- **Lineage, provenance and handoff** — the machinery that records inheritance, warrant, contribution history and authority boundaries.

## Open tools

### `astro-agalmic`

`packages/astro-agalmic` is a reusable Astro integration extracted from the site's knowledge-discovery architecture.

It provides semantic registry validation, relationship and canonical-identity checks, build-time full-text search, reusable search/context components, history and handoff conventions, and optional Astro content-collection helpers.

The package is licensed under **0BSD**. Use it, rename it, improve it or absorb the useful parts into something better. Attribution is not required.

## Nemosyne

[Nemosyne](https://nemosyne.world) is a related AI-assisted discovery and engineering project exploring spatial data navigation, representation intelligence, provenance and human-machine discovery.

Its present relationship to Agalmic practice is explicitly two-phase:

- use AI capability first to explore the product and representation space without requiring every exploratory implementation to be cognitively assimilated immediately;
- once promising directions survive, use reconstruction, testing, selective rebuilding and adversarial review to increase the human curator's understanding of the durable internals.

Nemosyne source: https://github.com/TsatsuAmable/nemosyne

## Local development

Requirements:

- Node.js 22.12 or newer
- npm

```sh
npm install
npm run dev
```

Run the production validation and build:

```sh
npm run build
```

Preview the generated site:

```sh
npm run preview
```

## Repository structure

```text
src/
  components/       site components
  data/             semantic knowledge, portfolio, handoff and provenance data
  layouts/          Astro layouts
  pages/            public site routes
  styles/           site styles

packages/
  astro-agalmic/    reusable 0BSD Astro knowledge-discovery integration

docs/               definitions, research documents, session records and working material
scripts/             repository-specific validation
public/              static public assets
```

## Publishing, provenance and reuse

The website is a canonical public index, not the only publication surface. Outputs may also become papers, essays, datasets, software, talks, archives, curricula or upstream contributions to other projects.

Where mature standards already solve a problem, the project prefers to reuse them. Provenance work is standards-first, including W3C PROV, CRediT and RO-Crate where appropriate.

The broader preference is simple: preserve credit and provenance, avoid unnecessary enclosure, and make useful capabilities easier for the next person to possess.
