# Site Knowledge Discovery Architecture

Version: 0.2  
Status: implemented information architecture  
Date: 7 September 2026

## Purpose

The Agalmic Research website should preserve a large and changing body of research while helping a reader or curator commit attention only to directionally meaningful material.

The design objective is:

> **Preserve the whole knowledge space. Make meaningful directions unusually easy to see.**

This is an application of established information-architecture, faceted-navigation, knowledge-management and progressive-disclosure ideas to the Agalmic Research process. It is not presented as a novel theory of website navigation.

## 1. Separate preservation from attention

The site distinguishes four functions that previously competed in one menu:

1. **Memory Palace** — preserve discovery topology: questions, branches, evidence, provenance, roads not taken and history.
2. **Knowledge Index / Explore** — make the preserved corpus discoverable through abstraction levels, topics, object type and commitment state.
3. **Active Frontier** — expose the deliberately small set of directions currently receiving scarce commitment.
4. **Knowledge Handoff Terminus** — expose research objects that need missing expertise, validation or realization capability rather than another local iteration.

The same object can appear in several projections without being duplicated conceptually.

## 2. Stable primary navigation

The primary menu is intentionally small and expected to remain stable as the corpus grows:

- **Explore** — semantic discovery across the knowledge space;
- **Publications** — durable research outputs;
- **Frontier** — current commitments;
- **Handoff** — current epistemic boundaries / requests for missing capability;
- **About** — research map, principles, lineage, provenance and Memory Palace machinery;
- **Search** — lexical full-text retrieval across rendered public pages.

The wordmark is the Start/home route. Detailed implementation machinery does not compete at top level.

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

## 4. Canonical semantic registry

`src/data/knowledgeIndex.json` is the canonical public semantic registry for reader-facing research identity and navigation.

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

The registry is not a replacement for W3C PROV, RO-Crate, CRediT or the historical discovery graph. Instead it supplies the stable public identity that those deeper records can reference.

The build validator enforces stable IDs, valid relationships, resolvable routes, Active Frontier WIP constraints, unique research-object canonical URLs and the presence of required discovery infrastructure.

## 5. Full-text search

Explore and Search solve different discovery problems.

- **Explore** operates over semantic metadata and abstraction.
- **Search** operates over the actual rendered text of the site.

After `astro build`, `scripts/build-search-index.mjs` walks the generated HTML, extracts searchable text and writes `/search-index.json`. The browser-side Search page performs local ranking with no backend and no external search service.

The build step also checks every indexed internal route against the generated site and requires canonical titles for papers, notes and drafts to match their rendered titles. This turns metadata drift into a build failure rather than a latent navigation bug.

The implementation is intentionally dependency-light. It can later be replaced by Pagefind or another static indexer without changing the information architecture.

## 6. Generated research-object context

Indexed papers, notes and drafts automatically receive a context terminus after their body. It answers three questions from the semantic registry:

1. **Where did this come from?** — lineage, provenance and registered history;
2. **What is related?** — semantic neighbours and handoffs;
3. **Where can I go next?** — the object's meaningful direction, relevant handoffs and Active Frontier.

This component is generated centrally from `Layout.astro`. Research pages do not maintain their own relationship arrays.

The same projection also emits basic Schema.org `ScholarlyArticle` JSON-LD for indexed research objects.

## 7. Knowledge history and supersession

`src/data/knowledgeHistory.json` stores visible semantic transitions such as renaming, narrowing, merging or supersession.

Each event records:

- a stable history ID and slug;
- date and transition state;
- previous and current titles;
- the reason for the transition;
- the current canonical destination;
- affected knowledge-object IDs;
- any real legacy URL paths that must remain addressable.

`/history/` presents the transition register and `/history/<slug>/` preserves each historical object as a readable page. Legacy paths should only be registered when such URLs actually existed; the architecture must not invent fake redirects.

## 8. Knowledge Handoff Terminus

`src/data/handoffs.json` stores public-safe open handoffs.

A handoff specifies:

- stable handoff ID;
- originating research object / possibility;
- precise question;
- missing expertise;
- what already exists;
- contribution requested;
- completion condition;
- evidence/context links.

A handoff is not a generic request for comments. It names the epistemic function the current project cannot adequately supply. The static endpoint `/handoffs.json` makes these boundaries machine-readable.

## 9. Relationship to the Memory Palace

The Memory Palace preserves temporal and causal discovery structure. The knowledge index provides a reader-oriented abstraction over that structure.

A research object should increasingly be navigable:

- backward to origins, sources and prior decisions;
- sideways to alternatives, objections and related branches;
- upward to a more abstract programme direction;
- downward to evidence and implementation detail;
- forward to Active Frontier next actions, handoffs, validation and realization.

The website should become a projection of the knowledge graph rather than a mirror of repository folders.

A graphical Memory Palace remains deliberately deferred. Relationship completeness and stable identity come before node-link visualization.

## 10. External discovery

The site now exposes:

- canonical URLs and OpenGraph metadata;
- scholarly JSON-LD for indexed research objects;
- `/sitemap.xml` generated from stable routes, semantic objects and knowledge history;
- `/rss.xml` for papers, notes and drafts;
- sitemap discovery through `robots.txt`.

Future durable releases can add DOI/Zenodo/OSF identifiers without changing the living website identity model.

## 11. Meaningful direction

“Meaningful” is deliberately not a universal relevance score.

It means that the object is useful for understanding the programme's present direction or is part of the current commitment frontier / authority boundary. The classification is corrigible and should change when evidence, goals, capacity or prior art changes.

## 12. Growth path

The next architectural improvements should be evolutionary rather than another redesign:

- enrich the canonical registry with explicit version, created/updated dates, epistemic status, lineage status, predecessor/successor and provenance references;
- progressively generate publication and notes index pages from the same registry;
- introduce explicit relation types where an untyped `related` edge becomes insufficient;
- add real legacy redirects when actual published URLs are superseded;
- connect public handoffs to external review workflows;
- integrate private-safe portfolio projections without leaking protected material;
- replace the simple full-text engine if corpus scale or retrieval quality warrants it;
- only then add graph/Memory Palace visualization over the same stable IDs.

The architecture should prefer a small number of reusable projections over adding new top-level pages for every research concept.
