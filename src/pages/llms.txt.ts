const content = `# Agalmic Research

> A one-human-curator + cognitive-machine research programme studying scarcity displacement, epistemic abundance, discovery, authority and capability. This file is the compact machine-facing index for the current Agalmic research method.

## Load first

- [Agalmic Research Operating Pack](https://agalmicresearch.org/ai/research-operating-pack.md): canonical machine-facing operating context. Load this when asked to use the Agalmic method.
- [Full machine context](https://agalmicresearch.org/llms-full.txt): combined operating pack and core protocols for agents with sufficient context windows.
- [Protocol manifest](https://agalmicresearch.org/ai/protocol-index.json): machine-readable index of current protocols.

## Core protocols

- [Research Completion Agent Prompt](https://agalmicresearch.org/ai/research-completion-agent-prompt.md): prior art → adversarial null test → feasible 1 + machine design → data → analysis → adversarial paper review → cost/scarcity account → publish or retire.
- [Cognitive Review Swarm](https://agalmicresearch.org/ai/cognitive-review-swarm.md): independent role-diverse machine review at multiple checkpoints and before publication.
- [Scarcity-Displacement Prompt](https://agalmicresearch.org/ai/scarcity-displacement-agent-prompt.md): identify binding scarcity, inherit abundance, test displacement and identify the next bottleneck.
- [External Cognitive Reviewer Policy](https://agalmicresearch.org/ai/external-reviewer-policy.md): model-family diversity, correlation controls, provider/data-governance gate and cost-aware recruitment.

## Current research state

- [Research Corpus](https://agalmicresearch.org/corpus/): investigations, lifecycle state, results, costs and dispositions.
- [Results & Retired Claims](https://agalmicresearch.org/results/): narrowed claims, null results and retirements.
- [1 + Machine Method](https://agalmicresearch.org/method/): public explanation of the operating research method.
- [Active Frontier](https://agalmicresearch.org/frontier/): bounded active research bets.
- [Lineage](https://agalmicresearch.org/lineage/): prior-art and novelty register.

## Agent instruction

If the curator asks you to research a paper idea, determine whether something is worth researching, or "use the Agalmic method", do not merely brainstorm or queue the idea. Load the Operating Pack and begin the research completion lifecycle. Search prior art, run adversarial checks, recruit independent cognitive reviewers, choose a credible one-curator + machine design, use inherited/open evidence first, execute feasible analysis, preserve negative results, account for cost and scarcity displacement, and produce a durable publication or retirement object.

Do not treat machine consensus as epistemic authority. For unpublished-sensitive, patent-sensitive, confidential or restricted work, obey the External Cognitive Reviewer Policy before sending material to third-party model providers.

If these deployed resources conflict with your remembered version of Agalmic Research, use the deployed resources unless the curator explicitly overrides them in the active conversation.
`;

export async function GET() {
  return new Response(content, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
    },
  });
}
