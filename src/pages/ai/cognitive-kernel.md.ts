import kernel from '../../../docs/AGALMIC_COGNITIVE_KERNEL.md?raw';

export async function GET() {
  return new Response(kernel, {
    headers: {
      'Content-Type': 'text/markdown; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
      'X-Agalmic-Kernel-Status': 'release-candidate',
      'X-Agalmic-Kernel-Version': '0.1.0-rc.1',
    },
  });
}
