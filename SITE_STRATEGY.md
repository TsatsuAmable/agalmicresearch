# Agalmic Research: site direction

## Positioning

**Agalmic Research studies what happens when machine cognition lowers the cost of generating candidate knowledge, while attention, validation, trust, realization and other complements remain scarce.**

The site should feel like a research notebook that has acquired an address, not a startup landing page and not a simulated university institute. Its authority should come from clear claims, visible intellectual lineage, durable citations, open source, standards-compatible provenance, version history and the quality of the arguments.

The project should not manufacture novelty through vocabulary. Existing theory is an input. Finding that an idea already exists is a successful research result because it moves the project to a higher starting point.

## Core working hypothesis

The programme currently uses the **Displaced Scarcity Hypothesis**:

> When a previously binding constraint becomes sufficiently abundant, system performance and value become increasingly determined by complementary constraints that remain scarce.

This is a synthesis/generalization hypothesis, not a demonstrated law. Important antecedents include Herbert Simon on attention scarcity, David Teece on complementary assets, Martin Weitzman on idea recombination/processing and broader bottleneck/constraint traditions.

The paper programme must establish whether a non-trivial general result remains after those antecedents are fully incorporated.

## Research architecture

1. **Agalmic Economics** — the umbrella programme, explicitly acknowledging Robert Levin's earlier agalmics and related economics of non-rival information.
2. **Economics of Epistemic Abundance** — allocation when candidate knowledge becomes cheap while attention, verification, trust, interpretation, institutional capacity and realization remain scarce. This name is deliberately distinguished from Anna Grandori's established *Epistemic Economics*.
3. **Epistemic Stewardship & Handoff** — claim accountability, contribution, authority and routing toward missing expertise, grounded in epistemic-dependence, contributorship and knowledge-brokering traditions.
4. **Epistemic Uptake** — an AI-era extension of absorptive-capacity and knowledge-processing problems.
5. **Machine Cognition & Discovery Attribution** — whether machines discover knowledge, facilitate discovery or participate in distributed discovery; separate candidate generation, significance recognition, validation, integration and realization.
6. **Innovation Search Under AI** — extend established evolutionary-economics, recombinant-search and adjacent-possible literatures rather than claiming innovation-as-search as new.
7. **Attention and Selection** — build explicitly on Simon and subsequent attention-economy work.
8. **Representation as Discovery** — concrete formalisms and implementations only; broad claims about representations enabling discovery have extensive antecedents in EDA, visualization, information theory and representation learning.
9. **Institutions, IP and Rents** — machine-speed implications for disclosure, prior art, appropriability, patents and realization, grounded in established innovation economics and IP practice.

## Novelty gate

Before a concept enters the numbered publication sequence:

1. state the strongest proposed contribution in one sentence;
2. search exact terminology and conceptual synonyms;
3. search the nearest mature literatures, historical work, standards and institutional practices;
4. identify the closest antecedents;
5. classify the result as `established antecedent`, `independent rediscovery`, `synthesis`, `extension`, `application`, `operationalization`, `terminology candidate`, `novelty unassessed` or, only after substantial search, `candidate novelty`;
6. rename or narrow claims where established usage collides with project terminology;
7. cite antecedents generously and state exactly what remains to add;
8. preserve the search boundary and important databases/literatures not examined;
9. treat patent/legal novelty as a separate review where relevant;
10. visibly correct public claims when prior art changes them.

Governing rule:

> **Novelty is a conclusion of search, not a tone of voice.**

## Publication model

Treat each project as a canonical, versioned research object. Produce useful projections from it:

- working paper
- peer-reviewed article
- public essay
- policy brief
- talk
- formal model
- code / dataset / demonstration

The website is the index and connective tissue. GitHub is the living source and version history. Stable releases can be deposited in Zenodo, OSF, SSRN or other appropriate archives. Journal publication remains valuable but is not the sole gatekeeper of the work.

Every substantial public research object should include or reference:

- intellectual-lineage / novelty status;
- epistemic status;
- contribution roles;
- provenance metadata;
- evidence/source register;
- corrections/revisions;
- known search boundaries;
- relevant epistemic handoffs.

## Standards-first provenance

Do not create a new provenance standard where mature infrastructure already exists.

Use:

- **W3C PROV** for ordinary entities, activities, agents, derivations and associations;
- **CRediT** for standardized scholarly contribution roles;
- **RO-Crate** for packaging interoperable research objects;
- established claim/evidence and decision-provenance work as prior art for graph-based research records.

The Agalmic Research Memory Palace is an application profile and experimental extension. Local metadata should remain narrow, currently focusing on:

- claim-level epistemic authority;
- authority basis;
- epistemic handoff;
- branch state / roads not taken;
- search boundaries;
- reversal conditions;
- attribution confidence and contemporaneous/retrospective status.

The original local `researchGraph.json` remains part of the historical provenance. Do not rewrite it to pretend the standards-first design existed from the beginning.

## Machine cognition and discovery

Do not collapse "AI generated this" into "AI discovered this," and do not collapse human selection into sole discovery either.

Track separately:

1. candidate generation;
2. significance recognition;
3. validation;
4. integration with prior knowledge;
5. realization.

The philosophical question of whether current machine systems themselves know or discover remains open.

For novelty assessment:

> **A result is novel relative to prior knowledge, not because it surprised the human or machine that encountered it.**

If a model surfaces an old idea unknown to the curator, record independent rediscovery and use the prior art.

## Editorial rules

- State conjecture as conjecture.
- Separate evidence from rhetoric.
- Prefer a precise question over a grand claim.
- Search lineage before claiming contribution.
- Attribute extensively when prior work supplies machinery or framing.
- Prefer established terminology and standards.
- Publish early enough to establish provenance and invite criticism, but do not confuse publication with novelty, mastery or certification.
- Version rather than silently overwrite.
- Preserve corrections and roads not taken.
- Do not inflate the organization. Let the corpus create the institution.
- Use patents exceptionally, where exclusivity is plausibly required to finance or coordinate real-world implementation and after appropriate prior-art review.
- Do not make AGI a prerequisite. Study changes already created by inexpensive machine cognition.

## Visual direction

- Text first.
- No hero imagery unless it carries research information.
- Warm paper background, dark ink, one restrained green accent.
- System fonts only.
- Large editorial serif headlines, compact sans-serif metadata.
- Hairline rules and generous whitespace instead of product-dashboard ornament.
- Zero client JavaScript until there is a research reason for it.

## Information architecture

- `/` — programme thesis and correction posture
- `/research` — research tracks, antecedents and open questions
- `/publications` — lineage-gated paper sequence
- `/drafts` — exploratory work with maturity and lineage status
- `/lineage` — living intellectual-lineage and novelty register
- `/provenance` — standards-first provenance architecture and historical graph
- `/memory-palace-protocol` — reusable research-session protocol
- `/principles` — operating philosophy, novelty discipline, open research and IP stance

Add RSS/search only when the corpus justifies them.

## Domain strategy

Use **agalmicresearch.org** as the canonical public research address. Redirect secondary domains to it rather than fragmenting the identity. The `.com` can remain defensive or support future commercial tooling, but the research corpus should have one canonical home.