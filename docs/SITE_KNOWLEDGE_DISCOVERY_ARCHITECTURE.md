# Site Knowledge Discovery Architecture

Version: 0.1  
Status: implemented experimental information architecture  
Date: 7 September 2026

## Purpose

The Agalmic Research website is growing faster than a flat navigation menu can remain useful. The site should preserve a large and changing body of research while helping a reader or curator commit attention only to directionally meaningful material.

The design objective is:

> **Preserve the whole knowledge space. Make meaningful directions unusually easy to see.**

This is an application of established information-architecture, faceted-navigation, knowledge-management and progressive-disclosure ideas to the Agalmic Research process. It is not presented as a novel theory of website navigation.

## 1. Separate preservation from attention

The site now distinguishes four functions that previously competed in one menu:

1. **Memory Palace** — preserve discovery topology: questions, branches, evidence, provenance, roads not taken and history.
2. **Knowledge Index / Explore** — make the preserved corpus discoverable through abstraction levels, topics, object type and commitment state.
3. **Active Frontier** — expose the deliberately small set of directions currently receiving scarce commitment.
4. **Knowledge Handoff Terminus** — expose research objects that need missing expertise, validation or realization capability rather than another local iteration.

The same object can appear in several projections without being duplicated conceptually.

## 2. Stable primary navigation

The primary menu is intentionally small and expected to remain stable as the corpus grows:

- **Explore** — discovery/search across the knowledge space;
- **Publications** — durable research outputs;
- **Frontier** — current commitments;
- **Handoff** — current epistemic boundaries / requests for missing capability;
- **About** — research map, principles, lineage, provenance and Memory Palace machinery.

The wordmark is the Start/home route.

Detailed implementation machinery no longer competes at top level.

## 3. Abstraction as a view, not deletion

The Explore interface exposes the same semantic index at several resolutions:

- **Orientation** — what the programme is trying to make possible;
- **Meaningful directions** — active, directionally important work;
- **Directions** — active, optional and parked research branches;
- **Research objects** — papers, notes and drafts;
- **Evidence** — literature reviews and supporting prior-art work;
- **Methods** — provenance, Memory Palace, portfolio and lineage machinery;
- **Everything** — the full public index.

Filtering information out of the current view does not retire or reject it.

## 4. Semantic knowledge index

`src/data/knowledgeIndex.json` is the initial public semantic registry.

Each object records at minimum:

- stable ID;
- title;
- object kind;
- abstraction layer;
- commitment state;
- whether it belongs in the default meaningful-direction view;
- topics;
- status;
- summary;
- meaningful direction / next purpose;
- canonical href;
- related object IDs.

The static endpoint `/knowledge-index.json` exposes the same projection to future agents, graph tools and search interfaces.

This is an indexing layer, not a replacement for W3C PROV, RO-Crate, CRediT or the historical discovery graph.

## 5. Knowledge Handoff Terminus

`src/data/handoffs.json` stores public-safe open handoffs.

A handoff should specify:

- stable handoff ID;
- originating research object / possibility;
- precise question;
- missing expertise;
- what already exists;
- contribution requested;
- completion condition;
- evidence/context links.

A handoff is not a generic request for comments. It names the epistemic function the current project cannot adequately supply.

The static endpoint `/handoffs.json` makes these boundaries machine-readable.

## 6. Relationship to the Memory Palace

The Memory Palace preserves temporal and causal discovery structure. The knowledge index provides a reader-oriented abstraction over that structure.

Long term, a research object should be navigable:

- backward to origins, sources and prior decisions;
- sideways to alternatives, objections and related branches;
- upward to a more abstract programme direction;
- downward to evidence and implementation detail;
- forward to Active Frontier next actions, handoffs, validation and realization.

The website should become a projection of the knowledge graph rather than a mirror of repository folders.

## 7. Meaningful direction

“Meaningful” is deliberately not a universal relevance score.

In the current implementation it means that the object is useful for understanding the programme's present direction or is part of the current commitment frontier / authority boundary.

The classification is corrigible and should change when evidence, goals, capacity or prior art changes.

## 8. Growth path

This v0.1 implementation uses an explicit semantic JSON registry and zero additional client framework dependencies.

Likely later improvements:

- move page metadata toward Astro content collections or another schema-validated canonical content layer;
- generate more of the index automatically from content metadata;
- add high-quality full-text indexing when corpus size warrants it;
- add relationship/graph exploration over the same IDs;
- add temporal views and supersession redirects;
- connect handoffs to external review workflows;
- integrate private-safe portfolio projections without leaking protected material.

The architecture should prefer a small number of reusable projections over adding new top-level pages for every new research concept.
