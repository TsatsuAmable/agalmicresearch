# Expert-attention preservation experiments

This directory contains executable research for the expert-attention triage validity benchmark in `docs/EXPERT_ATTENTION_TRIAGE_VALIDITY_BENCHMARK.md`.

## Phase 1: ICLR preservation audit

`iclr_preservation_audit.py` performs a descriptive audit over the public Berenslab ICLR dataset. It downloads a pinned dataset version, records its SHA-256 digest, normalizes decisions and review-score lists, and writes:

- yearly counts, acceptance rates, scores, and reviewer disagreement;
- topic/year summaries;
- score-conditional acceptance spreads across topics;
- preservation frontiers under fixed expert-attention budgets;
- a machine-readable manifest and human-readable report.

### Why this is deliberately not a prediction model

Reviewer scores and final decisions occur after expert review. They are therefore forbidden as candidate features in any deployable pre-review triage system. Phase 1 uses them only as diagnostic outcomes and as intentionally leaky comparison policies. The purpose is to measure what historical gatekeeping proxies preserve or erase before training any router.

### Reproduce

Python 3.11+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install pandas numpy requests pyarrow
python research/expert_attention/iclr_preservation_audit.py \
  --dataset 25v2 \
  --min-year 2020 \
  --max-year 2025
```

Outputs are written to `research-output/iclr-preservation-audit/` by default. Raw downloaded data is cached under `.cache/agalmic-research/` and is not committed.

The random-routing baseline is seeded (`20260910`) and repeated 250 times by default. All dataset bytes are hashed so a report can be tied to the exact source snapshot.

### Sanity checks from upstream

The Berenslab 2024v2 release reports 24,445 ICLR submissions from 2017–2024, 45 topic classes with 53.4% of papers labeled, an average 3.7 reviews among reviewed papers, and reviewer-score correlation of 0.40 across same-paper review pairs. These are useful external checks on ingestion, not targets to force-match after filtering.

### Interpretation discipline

A routing policy is not considered successful merely because it preserves papers that were historically accepted. A policy that improves accepted-paper recall while reducing high-disagreement recall or starving particular topics is evidence of gatekeeping mimicry, not successful scarcity displacement.

The first deployable baseline must use only information available before review, such as title, abstract, keywords/topic, and preregistered claim/evidence descriptors, with temporal train/test splits.

## Data sources

- Berenslab ICLR dataset: https://github.com/berenslab/iclr-dataset
- González-Márquez & Kobak, *Learning representations of learning representations*, ICLR DMLR Workshop 2024.
- Public OpenReview dump for later raw-note validation: https://github.com/qhjqhj00/iclr-openreview-reviews

Do not commit redistributed OpenReview paper/review content to this repository. Keep only analysis code, derived aggregates, manifests, and small non-identifying outputs needed for reproducibility.
