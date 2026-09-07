# Contribution Record Template

Use this file when a paper, draft, software artefact or institutional proposal becomes substantial enough to require explicit provenance.

```yaml
research_object_id: AR-YYYY-NNN
title: ""
version: ""
status: exploratory
repository_path: ""

contributors:
  - actor_id: actor:human-curator
    actor_type: human
    roles: [initiator, search_director, selector, decision_maker]
    contribution: ""
    evidence:
      - type: conversation
        date: YYYY-MM-DD
        pointer: ""

  - actor_id: actor:chatgpt
    actor_type: ai_system
    provider: OpenAI
    product: ChatGPT
    model: "record when known"
    roles: [framer, terminology, synthesizer, developer, critic, generator, editor]
    contribution: ""
    evidence:
      - type: conversation
        date: YYYY-MM-DD
        pointer: ""

claims:
  - claim_id: claim:001
    statement: ""
    authority_status: exploratory
    authority_holders: []
    authority_basis: ""
    evidence: []

provenance_events:
  - event_id: AR-EVENT-YYYYMMDD-001
    type: intuition
    summary: ""
    actors: []
    evidence: []

relations:
  - from: ""
    to: ""
    type: derived_from

corrections: []
```

## Required contribution declaration for public papers

A public paper should contain or link to a statement that answers:

1. What did the human curator initiate?
2. What did the AI system materially contribute?
3. Which formulations were selected or rejected by the human curator?
4. What external sources or reviewers materially changed the work?
5. Which claims can the human curator currently defend?
6. Which claims depend primarily on external expertise, verification or machine reasoning?
7. What evidence allows an independent reader to inspect the above answers?

The declaration should describe actual roles. Avoid both ritual under-crediting of AI assistance and anthropomorphic claims that an AI system possesses responsibility or epistemic authority merely because it generated text.
