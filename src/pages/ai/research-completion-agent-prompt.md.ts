import prompt from '../../../docs/RESEARCH_COMPLETION_AGENT_PROMPT.md?raw';

export async function GET() {
  return new Response(prompt, {
    headers: {
      'Content-Type': 'text/markdown; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
    },
  });
}
