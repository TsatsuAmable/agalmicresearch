# astro-agalmic

A small Astro integration for sites that need to preserve a growing knowledge space without turning their navigation into a mirror of their repository.

It packages the design pattern developed for Agalmic Research:

- a canonical semantic registry for knowledge objects;
- explicit relationships between objects, evidence, methods and handoffs;
- visible rename, narrowing and supersession history;
- build-time validation of identity and relationships;
- zero-backend full-text search generated from rendered HTML;
- reusable Search and KnowledgeContext Astro components;
- optional schemas for Astro content collections.

The package is licensed under **0BSD**. Use it, fork it, rename it, ship it, or absorb the useful pieces into something better. Attribution is not required.

## Status

`0.1.0` is an extracted, dogfooded first release candidate. Agalmic Research itself imports the integration directly from this package source.

## Install

When published to npm:

```sh
npm install astro-agalmic
```

Then add it to `astro.config.mjs`:

```js
import { defineConfig } from 'astro/config';
import agalmic from 'astro-agalmic';

export default defineConfig({
  integrations: [
    agalmic({
      registry: 'src/data/knowledgeIndex.json',
      history: 'src/data/knowledgeHistory.json',
      handoffs: 'src/data/handoffs.json',
    }),
  ],
});
```

The integration watches the declared data files, validates the semantic graph when Astro starts, and writes `search-index.json` after a production build.

## Minimal registry

```json
{
  "objects": [
    {
      "id": "note:attention",
      "title": "Attention Is the New Bottleneck",
      "kind": "research-note",
      "layer": "research-object",
      "commitment": "supporting",
      "meaningful": true,
      "topics": ["attention", "selection"],
      "status": "Research note",
      "summary": "A short description.",
      "direction": "Test whether the claim survives prior-art review.",
      "href": "/notes/attention/",
      "related": ["method:selection"]
    }
  ]
}
```

`related` IDs are checked during validation. Canonical research URLs must be unique.

## Search

Use the supplied Astro component:

```astro
---
import Search from 'astro-agalmic/components/Search.astro';
---

<Search />
```

The integration indexes rendered `<main>` text at build time. Any section marked `data-search-ignore` is excluded, which is useful for generated context, repeated navigation or other low-value search text.

Search deliberately complements rather than replaces semantic exploration:

- lexical search answers "where did we discuss this?";
- semantic metadata answers "what kind of thing is this, what is related, and where should I go next?"

## Generated knowledge context

The generic context component can project origins, neighbours, handoffs and next directions from the same registry:

```astro
---
import KnowledgeContext from 'astro-agalmic/components/KnowledgeContext.astro';
import registry from '../data/knowledgeIndex.json';
import history from '../data/knowledgeHistory.json';
import handoffs from '../data/handoffs.json';
---

<KnowledgeContext
  item={currentObject}
  registry={registry}
  history={history}
  handoffs={handoffs}
  routes={{
    lineage: '/lineage/',
    provenance: '/provenance/',
    frontier: '/frontier/',
    handoff: '/handoff/',
    history: '/history/',
  }}
/>
```

The component intentionally ships without a visual design system. Its CSS class names are stable enough for a host site to style, but the site owns appearance.

## Astro content collection schemas

Astro content collections are a natural future source of canonical metadata. The package provides schema factories without bundling a second Zod instance:

```ts
import { defineCollection } from 'astro:content';
import { file } from 'astro/loaders';
import { z } from 'astro/zod';
import { knowledgeObjectSchema } from 'astro-agalmic/schema';

const knowledge = defineCollection({
  loader: file('src/data/knowledgeObjects.json'),
  schema: knowledgeObjectSchema(z),
});

export const collections = { knowledge };
```

This allows a site to migrate from a JSON registry toward Astro's typed content layer without changing the public knowledge model.

## Options

```js
agalmic({
  registry: 'src/data/knowledgeIndex.json',
  history: null,
  handoffs: null,
  researchKinds: ['research-note', 'working-paper', 'draft'],
  validate: true,
  search: {
    output: 'search-index.json',
    titleComparison: 'case-insensitive',
    maxBodyCharacters: 24000,
    ignoreAttribute: 'data-search-ignore',
  },
})
```

Set `search: false` to use the validation layer without generating a lexical index.

## What this package does not try to own

It does not replace:

- W3C PROV or other provenance standards;
- CRediT contribution roles;
- RO-Crate packaging;
- Astro's content layer;
- specialist search engines such as Pagefind when a corpus outgrows the built-in index;
- graph visualization libraries.

The integration is glue around stable identity, selective attention and navigable knowledge history. Mature standards should remain the deeper substrate wherever they already solve the problem.

## Design principle

> Preserve the whole knowledge space. Make meaningful directions unusually easy to see.

The integration should remain small enough that another project can take the useful machinery without adopting Agalmic Research's vocabulary, philosophy or site design.
