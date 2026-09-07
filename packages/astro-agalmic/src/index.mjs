import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSearchIndex, readJsonFile, validateKnowledge } from './core.mjs';

export { buildSearchIndex, htmlToText, normalizePathname, readJsonFile, validateKnowledge } from './core.mjs';

const defaults = {
  registry: 'src/data/knowledgeIndex.json',
  history: null,
  handoffs: null,
  researchKinds: ['research-note', 'working-paper', 'draft'],
  validate: true,
  search: {},
};

const watchedPath = (root, source) => {
  if (!source) return null;
  if (path.isAbsolute(source)) return source;
  return path.join(fileURLToPath(root), source);
};

export default function astroAgalmic(userOptions = {}) {
  const options = {
    ...defaults,
    ...userOptions,
    search: userOptions.search === false ? false : { ...defaults.search, ...(userOptions.search ?? {}) },
  };
  let root;
  let registry;
  let history;
  let handoffs;

  const load = () => {
    registry = readJsonFile(root, options.registry);
    history = readJsonFile(root, options.history);
    handoffs = readJsonFile(root, options.handoffs);
  };

  return {
    name: 'astro-agalmic',
    hooks: {
      'astro:config:setup': ({ config, addWatchFile }) => {
        for (const source of [options.registry, options.history, options.handoffs]) {
          const watch = watchedPath(config.root, source);
          if (watch) addWatchFile(watch);
        }
      },
      'astro:config:done': ({ config, logger }) => {
        root = config.root;
        load();
        if (!options.validate) return;
        const result = validateKnowledge({
          registry,
          history,
          handoffs,
          researchKinds: options.researchKinds,
          requiredFields: options.requiredFields,
        });
        for (const warning of result.warnings) logger.warn(warning);
        if (result.errors.length > 0) {
          throw new Error(`astro-agalmic knowledge validation failed:\n${result.errors.join('\n')}`);
        }
        logger.info(`knowledge graph valid: ${result.counts.objects} objects, ${result.counts.handoffs} handoffs, ${result.counts.history} history events`);
      },
      'astro:build:done': ({ dir, logger }) => {
        if (options.search === false) return;
        load();
        const payload = buildSearchIndex({
          dir,
          registry,
          researchKinds: options.researchKinds,
          ...options.search,
        });
        logger.info(`full-text index built: ${payload.count} rendered pages`);
      },
    },
  };
}
