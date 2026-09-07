import index from '../data/knowledgeIndex.json';

export const prerender = true;

export function GET() {
  return new Response(JSON.stringify(index, null, 2), {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
    },
  });
}
