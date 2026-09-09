import operatingPack from '../../../docs/AGALMIC_RESEARCH_OPERATING_PACK.md?raw';

export async function GET() {
  return new Response(operatingPack, {
    headers: {
      'Content-Type': 'text/markdown; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
    },
  });
}
