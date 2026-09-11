import benchmark from '../../../docs/AGALMIC_COGNITIVE_KERNEL_BENCHMARK.md?raw';

export async function GET() {
  return new Response(benchmark, {
    headers: {
      'Content-Type': 'text/markdown; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
      'X-Agalmic-Kernel-Status': 'release-candidate',
      'X-Agalmic-Kernel-Version': '0.1.0-rc.1',
    },
  });
}
