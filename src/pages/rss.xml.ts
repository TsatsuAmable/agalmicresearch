import index from '../data/knowledgeIndex.json';

export const prerender = true;

const site = 'https://agalmicresearch.org';
const publishableKinds = new Set(['research-note', 'working-paper', 'draft']);
const escapeXml = (value: string) => value.replace(/[<>&'\"]/g, (char) => ({
  '<': '&lt;', '>': '&gt;', '&': '&amp;', "'": '&apos;', '"': '&quot;'
}[char] ?? char));

export function GET() {
  const date = new Date(`${index.updated}T12:00:00Z`).toUTCString();
  const items = index.objects
    .filter((item) => publishableKinds.has(item.kind) && item.href.startsWith('/') && !item.href.startsWith('//'))
    .map((item) => {
      const url = new URL(item.href, site).toString();
      return [
        '    <item>',
        `      <title>${escapeXml(item.title)}</title>`,
        `      <link>${escapeXml(url)}</link>`,
        `      <guid isPermaLink="true">${escapeXml(url)}</guid>`,
        `      <pubDate>${date}</pubDate>`,
        `      <description>${escapeXml(item.summary)}</description>`,
        `      <category>${escapeXml(item.status)}</category>`,
        '    </item>'
      ].join('\n');
    }).join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n  <channel>\n    <title>Agalmic Research</title>\n    <link>${site}/</link>\n    <description>Open, lineage-aware research on epistemic abundance, discovery, provenance and realization.</description>\n    <lastBuildDate>${date}</lastBuildDate>\n${items}\n  </channel>\n</rss>\n`;
  return new Response(xml, { headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' } });
}
