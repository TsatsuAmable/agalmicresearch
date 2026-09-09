import prompt from '../../../docs/SCARCITY_DISPLACEMENT_AGENT_PROMPT.md?raw';

export async function GET() {
  return new Response(prompt, {
    headers: {
      'Content-Type': 'text/markdown; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
    },
  });
}
