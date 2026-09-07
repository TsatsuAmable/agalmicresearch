import graph from '../data/researchGraph.json';

export function GET() {
  return new Response(JSON.stringify(graph, null, 2), {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
    },
  });
}
