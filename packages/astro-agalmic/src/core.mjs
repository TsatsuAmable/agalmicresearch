import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const normalizeRegistry = (value) => Array.isArray(value) ? value : value?.objects ?? [];
const normalizeHandoffs = (value) => Array.isArray(value) ? value : value?.handoffs ?? [];
const normalizeHistory = (value) => Array.isArray(value) ? value : value?.events ?? [];

export function validateKnowledge({
  registry,
  handoffs,
  history,
  requiredFields = ['id', 'title', 'kind', 'layer', 'commitment', 'status', 'summary', 'direction', 'href'],
  researchKinds = ['research-note', 'working-paper', 'draft'],
} = {}) {
  const objects = normalizeRegistry(registry);
  const handoffItems = normalizeHandoffs(handoffs);
  const historyEvents = normalizeHistory(history);
  const errors = [];
  const warnings = [];
  const fail = (message) => errors.push(message);
  const warn = (message) => warnings.push(message);
  const unique = (values, label) => {
    const seen = new Set();
    for (const value of values) {
      if (!value) continue;
      if (seen.has(value)) fail(`${label}: duplicate value ${value}`);
      seen.add(value);
    }
    return seen;
  };

  const objectIds = unique(objects.map((item) => item.id), 'knowledge object id');
  const handoffIds = unique(handoffItems.map((item) => item.id), 'handoff id');
  const relatedIds = new Set([...objectIds, ...handoffIds]);

  for (const item of objects) {
    for (const field of requiredFields) {
      if (item?.[field] === undefined || item?.[field] === null || item?.[field] === '') {
        fail(`${item?.id ?? 'knowledge object'}: missing ${field}`);
      }
    }
    if (!Array.isArray(item?.topics) || item.topics.length === 0) fail(`${item?.id ?? 'knowledge object'}: topics must be a non-empty array`);
    if (!Array.isArray(item?.related)) fail(`${item?.id ?? 'knowledge object'}: related must be an array`);
    for (const related of item?.related ?? []) {
      if (!relatedIds.has(related)) fail(`${item.id}: related object or handoff ${related} does not exist`);
    }
  }

  const researchKindSet = new Set(researchKinds);
  const canonicalResearchHrefs = objects
    .filter((item) => researchKindSet.has(item.kind) && item.href?.startsWith('/') && !item.href.startsWith('//'))
    .map((item) => normalizePathname(item.href));
  unique(canonicalResearchHrefs, 'research object canonical href');

  for (const handoff of handoffItems) {
    if (!handoff?.id) fail('handoff: missing id');
    if (!handoff?.title) fail(`${handoff?.id ?? 'handoff'}: missing title`);
    if (!handoff?.origin) fail(`${handoff?.id ?? 'handoff'}: missing origin`);
    if (handoff?.origin && !objectIds.has(handoff.origin)) warn(`${handoff.id}: origin ${handoff.origin} is not a current knowledge object id`);
  }

  unique(historyEvents.map((event) => event.id), 'history event id');
  unique(historyEvents.map((event) => event.slug), 'history event slug');
  for (const event of historyEvents) {
    for (const field of ['id', 'slug', 'date', 'state', 'previous_title', 'current_title', 'reason', 'current_href']) {
      if (!event?.[field]) fail(`${event?.id ?? 'history event'}: missing ${field}`);
    }
    if (!Array.isArray(event?.object_ids) || event.object_ids.length === 0) fail(`${event?.id ?? 'history event'}: object_ids must be non-empty`);
    for (const id of event?.object_ids ?? []) {
      if (!objectIds.has(id)) fail(`${event.id}: unknown current object ${id}`);
    }
  }

  return { errors, warnings, counts: { objects: objects.length, handoffs: handoffItems.length, history: historyEvents.length } };
}

export function normalizePathname(href = '/') {
  const pathname = String(href).split(/[?#]/)[0] || '/';
  return pathname === '/' ? '/' : `/${pathname.replace(/^\/+|\/+$/g, '')}/`;
}

const decode = (value = '') => String(value)
  .replace(/&nbsp;/gi, ' ')
  .replace(/&amp;/gi, '&')
  .replace(/&lt;/gi, '<')
  .replace(/&gt;/gi, '>')
  .replace(/&quot;/gi, '"')
  .replace(/&#39;|&apos;/gi, "'")
  .replace(/&#(\d+);/g, (_, code) => String.fromCodePoint(Number(code)))
  .replace(/&#x([0-9a-f]+);/gi, (_, code) => String.fromCodePoint(Number.parseInt(code, 16)));

export function htmlToText(value = '') {
  return decode(value)
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, ' ')
    .replace(/<svg\b[^>]*>[\s\S]*?<\/svg>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

const attribute = (tag = '', name) => {
  const match = tag.match(new RegExp(`\\b${name}\\s*=\\s*(["'])(.*?)\\1`, 'i'));
  return decode(match?.[2] ?? '').trim();
};

const metadata = (html) => {
  const metaTags = html.match(/<meta\b[^>]*>/gi) ?? [];
  const linkTags = html.match(/<link\b[^>]*>/gi) ?? [];
  const descriptionTag = metaTags.find((tag) => attribute(tag, 'name').toLowerCase() === 'description');
  const canonicalTag = linkTags.find((tag) => attribute(tag, 'rel').toLowerCase().split(/\s+/).includes('canonical'));
  return {
    description: attribute(descriptionTag, 'content'),
    canonical: attribute(canonicalTag, 'href'),
  };
};

const walk = (dir) => fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
  const target = path.join(dir, entry.name);
  return entry.isDirectory() ? walk(target) : [target];
});

const routeFor = (dist, file) => {
  const rel = path.relative(dist, file).split(path.sep).join('/');
  if (rel === 'index.html') return '/';
  if (rel.endsWith('/index.html')) return `/${rel.slice(0, -'index.html'.length)}`;
  return `/${rel.replace(/\.html$/, '/')}`;
};

const sameTitle = (left, right, mode) => {
  if (mode === 'exact') return left === right;
  return left.localeCompare(right, undefined, { sensitivity: 'accent' }) === 0;
};

export function buildSearchIndex({
  dir,
  registry,
  output = 'search-index.json',
  researchKinds = ['research-note', 'working-paper', 'draft'],
  titleComparison = 'case-insensitive',
  maxBodyCharacters = 24000,
  ignoreAttribute = 'data-search-ignore',
} = {}) {
  const dist = dir instanceof URL ? fileURLToPath(dir) : String(dir);
  const objects = normalizeRegistry(registry);
  if (!fs.existsSync(dist)) throw new Error(`build output does not exist: ${dist}`);

  const ignorePattern = new RegExp(`<section\\b[^>]*${ignoreAttribute}[^>]*>[\\s\\S]*?<\\/section>`, 'gi');
  const entries = walk(dist)
    .filter((file) => file.endsWith('.html'))
    .map((file) => {
      const html = fs.readFileSync(file, 'utf8');
      const title = htmlToText(html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1] ?? '')
        .replace(/\s+·\s+[^·]+$/, '');
      const { description, canonical } = metadata(html);
      let searchable = html.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i)?.[1] ?? html;
      searchable = searchable.replace(ignorePattern, ' ');
      const body = htmlToText(searchable).slice(0, maxBodyCharacters);
      return {
        url: canonical || routeFor(dist, file),
        path: routeFor(dist, file),
        title: title || routeFor(dist, file),
        description,
        body,
      };
    })
    .filter((entry) => entry.path !== '/404/');

  const byPath = new Map(entries.map((entry) => [normalizePathname(entry.path), entry]));
  const researchKindSet = new Set(researchKinds);
  const errors = [];

  for (const item of objects) {
    if (!item.href?.startsWith('/') || item.href.startsWith('//')) continue;
    const rendered = byPath.get(normalizePathname(item.href));
    if (!rendered) {
      errors.push(`${item.id}: rendered route missing from build: ${item.href}`);
      continue;
    }
    if (researchKindSet.has(item.kind) && !sameTitle(rendered.title, item.title, titleComparison)) {
      errors.push(`${item.id}: canonical title "${item.title}" differs from rendered title "${rendered.title}"`);
    }
  }

  if (errors.length > 0) throw new Error(errors.join('\n'));

  const payload = {
    schema_version: '0.1',
    generated_at: new Date().toISOString(),
    count: entries.length,
    entries,
  };
  const destination = path.join(dist, output.replace(/^\/+/, ''));
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.writeFileSync(destination, `${JSON.stringify(payload)}\n`);
  return payload;
}

export function readJsonFile(root, source) {
  if (!source) return null;
  const rootPath = root instanceof URL ? fileURLToPath(root) : String(root);
  const filename = path.isAbsolute(source) ? source : path.join(rootPath, source);
  return JSON.parse(fs.readFileSync(filename, 'utf8'));
}
