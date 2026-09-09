const protocolIndex = {
  schema_version: '0.1',
  updated: '2026-09-09',
  programme: 'Agalmic Research',
  instruction: 'If asked to use the Agalmic research method, load research-operating-pack first, then load stage-specific protocols as needed. Treat deployed website resources as current unless the curator explicitly overrides them.',
  entrypoints: {
    compact: '/llms.txt',
    full: '/llms-full.txt',
    operating_pack: '/ai/research-operating-pack.md',
  },
  protocols: [
    {
      id: 'research-completion',
      url: '/ai/research-completion-agent-prompt.md',
      canonical_source: 'docs/RESEARCH_COMPLETION_AGENT_PROMPT.md',
      purpose: 'Drive a research-worthy idea from prior-art screening through analysis, adversarial review, cost accounting and publication or retirement.',
    },
    {
      id: 'cognitive-review-swarm',
      url: '/ai/cognitive-review-swarm.md',
      canonical_source: 'docs/COGNITIVE_REVIEW_SWARM_PROTOCOL.md',
      purpose: 'Recruit independent role-diverse cognitive reviewers at multiple research checkpoints and before publication.',
    },
    {
      id: 'scarcity-displacement',
      url: '/ai/scarcity-displacement-agent-prompt.md',
      canonical_source: 'docs/SCARCITY_DISPLACEMENT_AGENT_PROMPT.md',
      purpose: 'Identify binding human or material scarcity, search inherited abundance, test displacement and record the next bottleneck.',
    },
    {
      id: 'external-reviewer-policy',
      url: '/ai/external-reviewer-policy.md',
      canonical_source: 'docs/EXTERNAL_COGNITIVE_REVIEWER_POLICY.md',
      purpose: 'Use model-family diversity while controlling correlation, cost, confidentiality and provider data-governance risk.',
    },
  ],
  public_state: {
    corpus: '/corpus/',
    results_and_retirements: '/results/',
    method: '/method/',
    frontier: '/frontier/',
    lineage: '/lineage/',
  },
  authority_boundary: 'Machine reviewers and collaborators can discover errors and produce candidate claims, but cannot manufacture domain authority. The human curator remains responsible for claims and publication decisions.',
};

export async function GET() {
  return new Response(JSON.stringify(protocolIndex, null, 2) + '\n', {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
    },
  });
}
