import operatingPack from '../../docs/AGALMIC_RESEARCH_OPERATING_PACK.md?raw';
import completionPrompt from '../../docs/RESEARCH_COMPLETION_AGENT_PROMPT.md?raw';
import reviewSwarm from '../../docs/COGNITIVE_REVIEW_SWARM_PROTOCOL.md?raw';
import scarcityPrompt from '../../docs/SCARCITY_DISPLACEMENT_AGENT_PROMPT.md?raw';
import externalReviewerPolicy from '../../docs/EXTERNAL_COGNITIVE_REVIEWER_POLICY.md?raw';

const sections = [
  ['AGALMIC RESEARCH OPERATING PACK', operatingPack],
  ['RESEARCH COMPLETION AGENT PROMPT', completionPrompt],
  ['COGNITIVE REVIEW SWARM PROTOCOL', reviewSwarm],
  ['SCARCITY-DISPLACEMENT AGENT PROMPT', scarcityPrompt],
  ['EXTERNAL COGNITIVE REVIEWER POLICY', externalReviewerPolicy],
];

const content = sections
  .map(([title, body]) => `\n\n===== ${title} =====\n\n${body.trim()}\n`)
  .join('');

export async function GET() {
  return new Response(content, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
    },
  });
}
