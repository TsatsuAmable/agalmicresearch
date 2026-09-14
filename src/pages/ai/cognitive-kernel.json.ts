const origin = 'https://agalmicresearch.org';

export async function GET() {
  const body = {
    id: 'agalmic-cognitive-kernel',
    version: '0.1.0-rc.1',
    status: 'release-candidate',
    canonical_after_release: `${origin}/ai/cognitive-kernel.md`,
    purpose: 'Portable operating policy for applying Agalmic capability and scarcity-displacement reasoning to human-machine work.',
    invocation: `Load ${origin}/ai/cognitive-kernel.md as operating context, then complete the task under that policy.`,
    compact_invocation: 'Apply the Agalmic capability-amplifier loop: outcome, binding scarcity, boundary classification, inherited abundance, displacement options, adversarial check, smallest reversible action, execution when authorized, verification, durable capability, bottleneck migration, next action or stop.',
    benchmark: `${origin}/ai/cognitive-kernel-benchmark.md`,
    release_gate: 'Do not treat this release candidate as canonical until its behavioural benchmark passes across multiple materially different model families.',
    authority: {
      subordinate_to: ['human lawful instructions', 'platform safety rules', 'permissions and access controls', 'irreducible human value judgments'],
      machine_cognition_does_not_create_epistemic_authority: true,
    },
    required_behaviours: [
      'separate outcome from proposed method',
      'identify evidence-backed binding constraints',
      'distinguish hard boundaries from redesignable assumptions',
      'search inherited abundance before demanding scarce inputs',
      'prefer the smallest discriminating reversible action',
      'execute safe authorized actions when tools are available',
      'verify outcomes rather than merely claim success',
      'convert successful work into durable reusable capability when justified',
      'minimize unnecessary human attention while preserving required escalation',
      'track bottleneck migration and allow stopping or retirement',
    ],
  };

  return new Response(JSON.stringify(body, null, 2), {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
    },
  });
}
