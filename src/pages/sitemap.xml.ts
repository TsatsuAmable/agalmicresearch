import index from '../data/knowledgeIndex.json';
import history from '../data/knowledgeHistory.json';

export const prerender = true;

const site = 'https://agalmicresearch.org';
const staticRoutes = [
  '/', '/explore/', '/search/', '/publications/', '/frontier/', '/handoff/', '/about/',
  '/research/', '/notes/', '/drafts/', '/lineage/', '/provenance/', '/principles/',
  '/memory-palace-protocol/', '/history/'
];
const escapeXml = (value: string) => value.replace(/[<>&'\"]/g, (char) => ({
  '<': '&lt;', '>': '&gt;', '&': '&amp;', "'": '&apos;', '"': '&quot;'
}[char] ?? char));

export function GET() {
  const knowledgeRoutes = index.objects
    .map((item) => item.href)
    .filter((href) => href.startsWith('/') && !href.startsWith('//'))
    .map((href) => href.split(/[?#]/)[0]);
  const historyRoutes = history.events.map((event) => `/history/${event.slug}/`);
  const routes = [...new Set([...staticRoutes, ...knowledgeRoutes, ...historyRoutes])]
    .map((href) => href.endsWith('/') || href.includes('.') ? href : `${href}/`)
    .sort();
  const lastmod = index.updated;
  const body = routes.map((href) => `  <url><loc>${escapeXml(new URL(href, site).toString())}</loc><lastmod>${lastmod}</lastmod></url>`).join('\n');
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}
