import protocol from '../../../docs/COGNITIVE_REVIEW_SWARM_PROTOCOL.md?raw';

export async function GET() {
  return new Response(protocol, {
    headers: {
      'Content-Type': 'text/markdown; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
    },
  });
}
