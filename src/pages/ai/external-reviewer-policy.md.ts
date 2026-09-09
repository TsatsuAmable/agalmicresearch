import policy from '../../../docs/EXTERNAL_COGNITIVE_REVIEWER_POLICY.md?raw';

export async function GET() {
  return new Response(policy, {
    headers: {
      'Content-Type': 'text/markdown; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
    },
  });
}
