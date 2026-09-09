# Handoff Retrospective Study

Status: Phase 0 — reproducibility / data audit

This directory is the executable research scaffold for `docs/HANDOFF_RETROSPECTIVE_STUDY_PROTOCOL.md`.

## First corpus

PeerRead (Kang et al., 2018): https://github.com/allenai/PeerRead

Why first:

- compact enough for a 1 + machine feasibility study;
- public research corpus with accept/reject outcomes;
- several venue sections include expert review text and numerical recommendation/confidence fields;
- historical labels allow simulated expert-attention budgets without recruiting new experts.

PeerRead is not treated as ground truth. Acceptance, reviewer scores, confidence and disagreement are separate historical outcomes.

## Phase 0 questions

Before any model is trained:

1. Which venue/split files are actually present without additional licensed downloads?
2. Which fields are available before review vs created during/after review?
3. How much missingness exists for recommendation, confidence, originality, soundness and other fields?
4. How many papers have multiple usable expert recommendations?
5. How much reviewer disagreement exists?
6. Are review entries duplicated within paper records?
7. Do schemas differ materially across venues and years?
8. Which sections are legally and practically suitable for a reproducible benchmark?

## Reproduce first

The original PeerRead paper reports 14.7K drafts, accept/reject decisions and 10.7K textual expert reviews across the full dataset. Some sections require separate downloads because of licensing constraints, so local audit totals may legitimately differ.

The first deliverable is therefore a **data inventory**, not a predictive model.

## Audit command

After cloning or downloading PeerRead:

```bash
python scripts/audit_peerread.py /path/to/PeerRead
```

The script uses only the Python standard library. It reports per-venue/split candidate counts, acceptance availability, numerical review fields, multi-review coverage, disagreement proxies and exact duplicate review entries.

## Pre-review / outcome firewall

Potential routing inputs:

- title;
- abstract;
- manuscript-derived features where available and licensed;
- references / lineage features derived from the candidate itself;
- field/venue only when it is part of the routing environment.

Historical outcomes that must never leak into routing features:

- `accepted`;
- reviewer recommendations;
- reviewer confidence;
- review/meta-review text;
- final decision comments;
- post-review histories.

Author/institution identity is excluded from the primary triage condition and reserved for explicit bias/sensitivity experiments.

## Next after audit

1. freeze a feasible corpus and hash/version the source;
2. write a normalized candidate/outcome table;
3. produce descriptive distributions and reviewer-disagreement statistics;
4. impose simulated review budgets;
5. run random allocation and a deliberately simple rule baseline;
6. draw the first attention-efficiency frontier;
7. only then introduce learned/model triage.

## Stop condition for PeerRead

Move to a more contemporary OpenReview corpus if PeerRead cannot support robust out-of-sample evaluation, disagreement measurement, or sufficiently clear pre-review/outcome separation. Do not keep repairing the dataset merely because it was the first candidate.
