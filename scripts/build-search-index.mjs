import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const root = process.cwd();
const dist = path.join(root, 'dist');
const knowledge = JSON.parse(fs.readFileSync(path.join(root, 'src/data/knowledgeIndex.json'), 'utf8'));

if (!fs.existsSync(dist)) {
  console.error('search-index error: dist/ does not exist; run Astro build first');
  process.exit(1);
}

const walk = (dir) => fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
  const target = path.join(dir, entry.name);
  return entry.isDirectory() ? walk(target) : [target];
});

const decode = (value = '') => value
  .replace(/&nbsp;/gi, ' ')
  .replace(/&amp;/gi, '&')
  .replace(/&lt;/gi, '<')
  .replace(/&gt;/gi, '>')
  .replace(/&quot;/gi, '"')
  .replace(/&#39;|&apos;/gi, "'")
  .replace(/&#(\d+);/g, (_, code) => String.fromCodePoint(Number(code)))
  .replace(/&#x([0-9a-f]+);/gi, (_, code) => String.fromCodePoint(Number.parseInt(code, 16)));

const plain = (value = '') => decode(value)
  .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ' ')
  .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, ' ')
  .replace(/<svg\b[^>]*>[\s\S]*?<\/svg>/gi, ' ')
  .replace(/<[^>]+>/g, ' ')
  .replace(/\s+/g, ' ')
  .trim();

const attr = (html, pattern) => decode(html.match(pattern)?.[1] ?? '').trim();

const routeFor = (file) => {
  const rel = path.relative(dist, file).split(path.sep).join('/');
  if (rel === 'index.html') return '/';
  if (rel.endsWith('/index.html')) return `/${rel.slice(0, -'index.html'.length)}`;
  return `/${rel.replace(/\.html$/, '/')}`;
};

const entries = walk(dist)
  .filter((file) => file.endsWith('.html'))
  .map((file) => {
    const html = fs.readFileSync(file, 'utf8');
    const title = plain(html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1] ?? '')
      .replace(/\s+·\s+Agalmic Research$/, '');
    const description = attr(html, /<meta\s+name=["']description["']\s+content=["']([^"']*)["'][^>]*>/i)
      || attr(html, /<meta\s+content=["']([^"']*)["']\s+name=["']description["'][^>]*>/i);
    const canonical = attr(html, /<link\s+rel=["']canonical["']\s+href=["']([^"']+)["'][^>]*>/i)
      || attr(html, /<link\s+href=["']([^"']+)["']\s+rel=["']canonical["'][^>]*>/i);
    let searchable = html.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i)?.[1] ?? html;
    searchable = searchable.replace(/<section\b[^>]*data-search-ignore[^>]*>[\s\S]*?<\/section>/gi, ' ');
    const body = plain(searchable).slice(0, 24000);
    return {
      url: canonical || routeFor(file),
      path: routeFor(file),
      title: title || routeFor(file),
      description,
      body,
    };
  })
  .filter((entry) => entry.path !== '/404/');

const byPath = new Map(entries.map((entry) => [entry.path.replace(/\/+$/, '') || '/', entry]));
const researchKinds = new Set(['research-note', 'working-paper', 'draft']);
const errors = [];

for (const item of knowledge.objects) {
  if (!item.href.startsWith('/') || item.href.startsWith('//')) continue;
  const normalized = item.href.replace(/[?#].*$/, '').replace(/\/+$/, '') || '/';
  const rendered = byPath.get(normalized);
  if (!rendered) {
    errors.push(`${item.id}: rendered route missing from dist: ${item.href}`);
    continue;
  }
  if (researchKinds.has(item.kind) && rendered.title !== item.title) {
    errors.push(`${item.id}: canonical title "${item.title}" differs from rendered title "${rendered.title}"`);
  }
}

if (errors.length > 0) {
  for (const error of errors) console.error(`search-index error: ${error}`);
  process.exit(1);
}

const payload = {
  schema_version: '0.1',
  generated_at: new Date().toISOString(),
  count: entries.length,
  entries,
};

fs.writeFileSync(path.join(dist, 'search-index.json'), `${JSON.stringify(payload)}\n`);
console.log(`search-index built: ${entries.length} rendered pages indexed`);
