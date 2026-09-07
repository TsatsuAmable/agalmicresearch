# Agalmic Research

**Agalmic Research** is an open research programme studying how knowledge, computation, energy, institutions, and human judgment can expand the set of worthwhile futures people can actually reach.

The programme starts from a simple direction:

> **The goal is not more ideas. It is greater capacity to reach worthwhile futures.**

Agalmic Research is interested in what happens when some historically scarce inputs become dramatically cheaper to create, copy, or access. Rather than assuming abundance removes scarcity, the research asks which constraints become decisive next: attention, judgment, verification, expertise, coordination, energy, capital, trust, realization, or something else.

Live site: **https://agalmicresearch.org**

## What this repository contains

This repository is both the source of the public website and part of the research record.

It contains:

- research papers, notes, drafts, and literature reviews;
- the intellectual-lineage and novelty machinery used to constrain claims;
- provenance and handoff records;
- the Possibility Portfolio and Active Frontier used to separate preserved possibilities from active commitments;
- the semantic knowledge index that powers Explore and generated research context;
- the source for agalmicresearch.org;
- open tools extracted from the research process, including `astro-agalmic`.

The public repository is intentionally inspectable. Corrections, superseded ideas, and changes of framing should remain visible where practical rather than being silently rewritten out of history.

## Research orientation

Agalmic Research studies several connected questions:

- **Economics of epistemic abundance:** when knowledge generation becomes cheaper, which complementary scarcities become binding?
- **Innovation as search:** how can human-machine systems expand the effective adjacent possible without collapsing into idea overload?
- **Selection under abundance:** how should scarce attention, expertise, and resources be directed among an expanding set of candidates?
- **Distributed discovery:** how should framing, generation, recognition, validation, contribution, authority, and realization be represented when discovery crosses people and machines?
- **Epistemic handoff:** how should work move toward missing expertise without losing provenance or contribution history?
- **Representation and discovery:** can better representations increase what people are able to notice, understand, test, and act upon?

The programme treats these as research questions, not settled doctrines.

## Manifesto, philosophy, and research

The **Manifesto** states the direction of travel. It argues that abundance is worth pursuing as a research and institutional direction, while explicitly distinguishing orientation from research evidence.

The repository also contains working philosophical material that explores the deeper implications of abundance, stewardship, capability multiplication, openness, selection, and handoff. These documents may remain repository-only while they are being studied and revised.

Research has a different standard. The intended path is:

**idea → question → lineage → explicit claim → method → evidence or argument → criticism → epistemic status**

Prior art is infrastructure. Novelty is a conclusion of search, not a tone of voice.

## Knowledge architecture

The site is designed to preserve a growing knowledge space without making every preserved object compete for active attention.

The main distinction is:

- **Explore** shows the wider knowledge space at several levels of abstraction.
- **Frontier** shows the small number of directions receiving substantial commitment now.
- **Handoff** exposes work that has reached the boundary of current authority and needs different expertise.
- **History, lineage, and provenance** preserve where ideas came from, how they changed, and what supports them.

A semantic registry gives research objects stable identities, relationships, commitment states, canonical URLs, and machine-readable projections. Full-text search complements this model by answering lexical retrieval questions across rendered pages.

The repository deliberately keeps the deeper machinery behind the reader-facing map rather than letting the navigation mirror the implementation history.

## Open tools

### `astro-agalmic`

`packages/astro-agalmic` is a reusable Astro integration extracted from the knowledge-discovery architecture developed for this site.

It provides:

- semantic knowledge-registry validation;
- relationship and canonical-identity checks;
- build-time full-text search generation from rendered HTML;
- reusable `Search.astro` and `KnowledgeContext.astro` components;
- history and handoff conventions;
- optional Astro content-collection schema helpers.

The package is licensed under **0BSD**. Use it, fork it, rename it, improve it, or absorb the useful parts into something better. Attribution is not required.

The source package is public and npm-ready. It should not be assumed to be published or reserved on npm until an actual npm release has occurred.

Package source: `packages/astro-agalmic/`

## Agalmic practice

A recurring operating principle is:

> **When we create a generally useful capability to advance our own work, extraction into a reusable public good should be a standard exit path.**

Papers can give away conclusions. Datasets can give away evidence. Tools can give away capability.

Openness is a strong presumption rather than a purity test. Security, privacy, safety, or consciously chosen temporary intellectual-property protection can still justify keeping some material outside the public projection.

## Nemosyne

[Nemosyne](https://nemosyne.world) is a related applied research and engineering project exploring spatial data navigation, representation intelligence, provenance, and human-machine discovery.

Within Agalmic Research it acts as a testbed for questions about representation, recognition, and whether tools can enlarge the set of meaningful structures analysts are able to notice and investigate.

Nemosyne source: https://github.com/TsatsuAmable/nemosyne

## Local development

Requirements:

- Node.js 22.12 or newer
- npm

Install and start the development server:

```sh
npm install
npm run dev
```

Run the complete production validation and build:

```sh
npm run build
```

The build currently runs the site-specific knowledge validation, `astro-agalmic` tests, a package tarball smoke check, and the Astro production build. The integration then generates the static full-text search index as part of Astro's build lifecycle.

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

docs/               research documents, literature reviews, architecture and working material
scripts/             repository-specific validation
public/              static public assets
```

## Publishing and provenance

The website is a canonical public index, not the only possible publication surface. Research objects may also be projected into working papers, journal articles, essays, datasets, software, talks, archives, or peer-review submissions.

Where mature standards already solve a problem, the project prefers to reuse them. Provenance work is standards-first, including W3C PROV, CRediT, and RO-Crate where appropriate, with local extensions only where the research process needs concepts those standards do not directly represent.

Stable releases can later be archived with persistent identifiers while the living source and revision history remain inspectable here.

## Contributing

Useful contributions include criticism, prior art, corrections, replication, implementation improvements, specialist review, and completion of open epistemic handoffs.

A contribution does not need to agree with the programme's current framing to be valuable. Strong counterexamples and evidence that narrow or retire a claim are successful research outcomes.

If you find a problem in the site or `astro-agalmic`, open an issue or pull request. If you have relevant expertise for an open handoff, the public Handoff register on the site identifies the requested contribution and completion condition.

## Licence and reuse

Individual research artefacts may carry their own publication or archive terms as the programme develops. The `astro-agalmic` software package is explicitly licensed under **0BSD**.

The broader preference is simple: preserve credit and provenance, avoid unnecessary enclosure, and make useful capabilities easier for the next person to possess.
