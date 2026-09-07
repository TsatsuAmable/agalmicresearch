import { defineConfig } from 'astro/config';
import agalmic from './packages/astro-agalmic/src/index.mjs';

export default defineConfig({
  site: 'https://agalmicresearch.org',
  integrations: [
    agalmic({
      registry: 'src/data/knowledgeIndex.json',
      history: 'src/data/knowledgeHistory.json',
      handoffs: 'src/data/handoffs.json',
      researchKinds: ['research-note', 'working-paper', 'draft'],
      search: {
        output: 'search-index.json',
        titleComparison: 'case-insensitive',
        maxBodyCharacters: 24000,
        ignoreAttribute: 'data-search-ignore',
      },
    }),
  ],
});
