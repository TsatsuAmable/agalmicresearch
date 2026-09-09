# External Cognitive Reviewer Policy

Version: 0.1  
Status: companion policy to the Cognitive Review Swarm Protocol  
Date: 9 September 2026

## Purpose

Agalmic Research should use model diversity as well as role diversity when cognitive review has high expected information value. Repeating the same review through one model family can reproduce shared training priors, shared alignment preferences, shared blind spots and correlated reasoning failures.

The objective is not to count models as independent votes. It is to increase the probability that the work encounters materially different failure modes.

> **Model count is not independence. Diversity is useful when it changes the error surface.**

## Default diversity rule

For substantive papers and high-consequence research objects, the review orchestrator should preferentially recruit reviewers from at least three distinct model families or hosting routes when accessible at acceptable cost and data-governance risk.

A practical low-cost pool may include:

- the primary OpenAI model used by the research workflow;
- Google Gemini through a free developer/API tier where the current terms are acceptable for the artefact;
- open-weight or separately trained models exposed through Groq's free plan;
- free models available through OpenRouter's zero-price routing where model identity is recorded;
- occasional open models through Hugging Face inference when credits or local execution make this practical;
- locally runnable open-weight models when hardware permits.

Provider and free-tier availability changes. The orchestrator must verify current access, rate limits, model identity and data-use terms before each new integration rather than treating this list as permanent.

## Data-governance gate

Before sending an artefact to an external model provider, classify it:

### Public-safe

Already public or intentionally ready for public disclosure. May be sent to approved free-tier reviewers after current terms are checked.

### Unpublished-sensitive

Not yet public, but disclosure would not create material patent, confidentiality, contractual or participant risk. Use only providers whose current terms and controls are acceptable to the curator. Prefer zero-data-retention, paid/private, local or otherwise contractually suitable routes when available.

### Patent-sensitive / confidential / restricted

Do not send to third-party free APIs by default. Use local models, approved private endpoints, or the primary environment until the curator explicitly authorizes disclosure.

Free compute is not free if the price is unintended disclosure.

## Reviewer registration

Every external cognitive review run should record:

- provider;
- model identifier and version where exposed;
- access route (API, local, hosted inference, chat/manual);
- free/paid/local status;
- date of use;
- material model settings when known;
- whether the provider may retain or use prompts/outputs under the applicable terms;
- artefact sensitivity classification;
- reviewer role;
- artefact hash/version;
- prompt template version;
- review output hash or stored review record.

Do not describe two calls to the same underlying model through different routing services as two independent model families.

## Diversity dimensions

Use as many of these as practical:

1. **Model family diversity** — different base/training lineages.
2. **Provider diversity** — different serving/finetuning/alignment stacks.
3. **Role diversity** — prior-art, statistics, domain, data, causal, reproducibility, hostile referee, etc.
4. **Context diversity** — some reviewers see only the evidence packet, not the preferred conclusion.
5. **Source diversity** — reviewers may be assigned different literature/source subsets before synthesis.
6. **Method diversity** — request alternative statistical, formal or computational routes.
7. **Implementation diversity** — independent reproduction in different code paths or languages where worthwhile.

## Anti-correlation rules

- Capture reviews before showing reviewers one another's outputs.
- Do not seed every reviewer with the drafting model's rationale.
- Avoid identical generic prompts across all models.
- Record shared model ancestry when known.
- Treat convergence as suggestive, never as proof of correctness.
- Preserve minority objections when they are specific and falsifiable.
- A well-supported fatal criticism from one reviewer can block publication regardless of consensus.

## Cost-aware recruitment

Prefer free or already-available computation for broad early criticism, but route high-value unresolved questions to stronger or paid models when the expected information gain justifies it.

Track marginal defect discovery. Stop expanding the swarm when additional model families mostly repeat already-captured failure modes.

## Current low-cost recruitment strategy

For public-safe papers, a default prepublication panel can be assembled as:

1. primary OpenAI reviewer family;
2. Gemini reviewer;
3. one Groq-served open-weight reviewer from a distinct family;
4. one OpenRouter free-model reviewer selected to maximize lineage diversity from the previous three;
5. optional Hugging Face/local model for an independent reproduction or specialist critique.

The exact models should be selected at run time from currently available free tiers, not hard-coded permanently into the research method.

## Human boundary

Cross-model agreement still does not manufacture domain authority. External cognitive reviewers are a cheap search over possible defects. Human expert review remains necessary when the residual claim depends on professional authority, tacit domain judgment, real-world consequences, sensitive normative decisions, or evidence unavailable to the machines.
