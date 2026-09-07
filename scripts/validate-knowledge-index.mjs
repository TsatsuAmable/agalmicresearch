import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const root = process.cwd();
const readJson = (file) => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));

const knowledge = readJson('src/data/knowledgeIndex.json');
const portfolio = readJson('src/data/possibilityPortfolio.json');
const handoffs = readJson('src/data/handoffs.json');
const history = readJson('src/data/knowledgeHistory.json');

const errors = [];
const warnings = [];
const fail = (message) => errors.push(message);
const warn = (message) => warnings.push(message);

const unique = (values, label) => {
  const seen = new Set();
  for (const value of values) {
    if (seen.has(value)) fail(`${label}: duplicate value ${value}`);
    seen.add(value);
  }
  return seen;
};

const routeExists = (href) => {
  if (!href.startsWith('/') || href.startsWith('//')) return true;
  const pathname = href.split(/[?#]/)[0];
  if (pathname === '/') return fs.existsSync(path.join(root, 'src/pages/index.astro'));
  const clean = pathname.replace(/^\/+|\/+$/g, '');
  const candidates = [
    `src/pages/${clean}.astro`,
    `src/pages/${clean}/index.astro`,
    `src/pages/${clean}.ts`,
    `src/pages/${clean}.js`,
  ];
  const segments = clean.split('/');
  if (segments.length > 1) {
    const parent = segments.slice(0, -1).join('/');
    candidates.push(
      `src/pages/${parent}/[slug].astro`,
      `src/pages/${parent}/[id].astro`,
      `src/pages/${parent}/[...slug].astro`,
    );
  }
  return candidates.some((candidate) => fs.existsSync(path.join(root, candidate)));
};

const handoffIds = unique(handoffs.handoffs.map((item) => item.id), 'handoff register');
const requiredKnowledgeFields = ['id', 'title', 'kind', 'layer', 'commitment', 'status', 'summary', 'direction', 'href'];
const allowedLayers = new Set(['orientation', 'direction', 'research-object', 'evidence', 'method']);
const researchKinds = new Set(['research-note', 'working-paper', 'draft']);

const knowledgeIds = unique(knowledge.objects.map((item) => item.id), 'knowledge index');
const relatedIds = new Set([...knowledgeIds, ...handoffIds]);
for (const item of knowledge.objects) {
  for (const field of requiredKnowledgeFields) {
    if (item[field] === undefined || item[field] === null || item[field] === '') fail(`${item.id}: missing ${field}`);
  }
  if (!allowedLayers.has(item.layer)) fail(`${item.id}: unknown layer ${item.layer}`);
  if (typeof item.meaningful !== 'boolean') fail(`${item.id}: meaningful must be boolean`);
  if (!Array.isArray(item.topics) || item.topics.length === 0) fail(`${item.id}: topics must be a non-empty array`);
  if (!Array.isArray(item.related)) fail(`${item.id}: related must be an array`);
  for (const related of item.related ?? []) {
    if (!relatedIds.has(related)) fail(`${item.id}: related object or handoff ${related} does not exist`);
  }
  if (!routeExists(item.href)) fail(`${item.id}: internal href does not resolve to a source route: ${item.href}`);
}

const researchHrefs = knowledge.objects
  .filter((item) => researchKinds.has(item.kind) && item.href.startsWith('/') && !item.href.startsWith('//'))
  .map((item) => item.href.replace(/[?#].*$/, '').replace(/\/+$/, '') || '/');
unique(researchHrefs, 'research-object canonical href');

const meaningful = knowledge.objects.filter((item) => item.meaningful);
if (meaningful.length > 8) warn(`default meaningful-direction view contains ${meaningful.length} objects; consider tightening abstraction`);

const possibilityIds = unique(portfolio.possibilities.map((item) => item.id), 'possibility portfolio');
if (portfolio.active_frontier.length > portfolio.wip_limit) {
  fail(`active frontier contains ${portfolio.active_frontier.length} items but WIP limit is ${portfolio.wip_limit}`);
}
for (const id of portfolio.active_frontier) {
  if (!possibilityIds.has(id)) fail(`active frontier references missing possibility ${id}`);
  const item = portfolio.possibilities.find((candidate) => candidate.id === id);
  if (item && item.state !== 'active') fail(`${id}: listed on active frontier but state is ${item.state}`);
}

const activeKnowledgeDirections = knowledge.objects.filter((item) => item.layer === 'direction' && item.commitment === 'active');
if (activeKnowledgeDirections.length > portfolio.wip_limit) {
  fail(`knowledge index exposes ${activeKnowledgeDirections.length} active directions but WIP limit is ${portfolio.wip_limit}`);
}
if (activeKnowledgeDirections.length !== portfolio.active_frontier.length) {
  warn(`knowledge index has ${activeKnowledgeDirections.length} active directions while portfolio has ${portfolio.active_frontier.length}; check projection drift`);
}

const knownOrigins = new Set([...knowledgeIds, ...possibilityIds]);
for (const handoff of handoffs.handoffs) {
  for (const field of ['id', 'title', 'state', 'origin', 'question', 'what_exists', 'requested_contribution', 'completion_condition']) {
    if (!handoff[field]) fail(`${handoff.id ?? 'handoff'}: missing ${field}`);
  }
  if (!Array.isArray(handoff.expertise_needed) || handoff.expertise_needed.length === 0) fail(`${handoff.id}: expertise_needed must be non-empty`);
  if (!Array.isArray(handoff.links) || handoff.links.length === 0) fail(`${handoff.id}: links must be non-empty`);
  if (!knownOrigins.has(handoff.origin)) warn(`${handoff.id}: origin ${handoff.origin} is not a current knowledge-index or portfolio ID`);
  for (const href of handoff.links) {
    if (!routeExists(href)) fail(`${handoff.id}: internal link does not resolve to a source route: ${href}`);
  }
}

const historyIds = unique(history.events.map((event) => event.id), 'knowledge history');
const historySlugs = unique(history.events.map((event) => event.slug), 'knowledge history slug');
const legacyPaths = [];
for (const event of history.events) {
  for (const field of ['id', 'slug', 'date', 'state', 'previous_title', 'current_title', 'reason', 'current_href']) {
    if (!event[field]) fail(`${event.id ?? 'history event'}: missing ${field}`);
  }
  if (!Array.isArray(event.object_ids) || event.object_ids.length === 0) fail(`${event.id}: object_ids must be non-empty`);
  if (!Array.isArray(event.legacy_paths)) fail(`${event.id}: legacy_paths must be an array`);
  for (const id of event.object_ids ?? []) {
    if (!knowledgeIds.has(id)) fail(`${event.id}: unknown current object ${id}`);
  }
  if (!routeExists(event.current_href)) fail(`${event.id}: current_href does not resolve: ${event.current_href}`);
  for (const legacyPath of event.legacy_paths ?? []) legacyPaths.push(legacyPath);
}
unique(legacyPaths, 'knowledge history legacy path');

if (!fs.existsSync(path.join(root, 'src/pages/search.astro'))) fail('full-text search route is missing');
if (!fs.existsSync(path.join(root, 'packages/astro-agalmic/src/index.mjs'))) fail('astro-agalmic integration is missing');
if (!fs.existsSync(path.join(root, 'packages/astro-agalmic/components/Search.astro'))) fail('astro-agalmic Search component is missing');
if (!fs.existsSync(path.join(root, 'packages/astro-agalmic/components/KnowledgeContext.astro'))) fail('astro-agalmic KnowledgeContext component is missing');
if (!fs.existsSync(path.join(root, 'src/pages/sitemap.xml.ts'))) fail('sitemap endpoint is missing');
if (!fs.existsSync(path.join(root, 'src/pages/rss.xml.ts'))) fail('RSS endpoint is missing');
if (historyIds.size > 0 && !fs.existsSync(path.join(root, 'src/pages/history/[slug].astro'))) fail('historical object route is missing');
if (historySlugs.size > 0 && !fs.existsSync(path.join(root, 'src/pages/history.astro'))) fail('knowledge history index is missing');

for (const message of warnings) console.warn(`knowledge-check warning: ${message}`);
if (errors.length > 0) {
  for (const message of errors) console.error(`knowledge-check error: ${message}`);
  console.error(`knowledge-check failed with ${errors.length} error(s)`);
  process.exit(1);
}

console.log(`knowledge-check passed: ${knowledge.objects.length} indexed objects, ${portfolio.possibilities.length} possibilities, ${handoffs.handoffs.length} handoffs, ${history.events.length} history events`);
