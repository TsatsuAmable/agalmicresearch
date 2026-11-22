# P0 source-lineage audit: frozen ICLR corpus (2026-11-22)

**Status:** independently checked repository documentation; **G1 NOT satisfied**. This is a source-feasibility finding, not a reproduction of Phase 1B/1C, a legal determination, or evidence of prospective reviewer savings.

## Evidence examined

- Canonical Phase 1B findings: `docs/EXPERT_ATTENTION_PHASE1B_FINDINGS.md` identify an input SQLite database with SHA-256 `ceeaa4316f76f6a22a5856128f34e8c3f35693d145db756f9688eda42ee20ed2`, 7,531 eligible papers and 2017–2021 ratings.
- Canonical Phase 1C findings: `docs/EXPERT_ATTENTION_PHASE1C_FINDINGS.md` report 20 deterministic seeds 20261001–20261020 and a retrospective pooled 95%-recall, median 45%-saved result; within-year recall fails 95% for 2020 and 2021 on the first split at the 55% budget.
- `research/expert_attention/review_value_holdout.py` requires SQLite tables `submissions` and `reviews` and uses `s.id`, `r.id`, `r.forum`, `r.rating_int` to select three reviews per paper, ordering by a hash of **review ID** and seed.
- `research/expert_attention/boundary_preservation.py` delegates episode construction to that Phase 1B script.
- Upstream Berenslab README: https://github.com/berenslab/iclr-dataset/blob/main/README.md . It describes a parquet dataset with a **list of reviewer scores**, not an independently documented stable review-ID-to-score mapping; it also records a May 2025 correction to scraping of 2017–2018 submissions and subsequent releases.
- Upstream LICENSE: https://github.com/berenslab/iclr-dataset/blob/main/LICENSE is MIT, but repository licensing alone does **not** settle the rights of underlying scraped OpenReview submissions/reviews or authorize their redistribution here.

## Reproducibility obstruction, not merely a missing download

The frozen simulation's deterministic assignment of first, second and hidden third ratings depends on stable individual `r.id` values. A parquet file containing only each paper's unordered score list cannot be assumed to reproduce the same episode assignment, even when paper/year counts agree. Generating arbitrary synthetic review IDs would create a **different experiment**, not an independent replication of the frozen result. Moreover, upstream revisions to 2017–2018 parsing mean that selecting the newest release is not a verified substitute for the original input.

The original SQLite bytes, their SHA-256, extraction/version provenance and review-ID mapping must therefore be recovered and verified before claiming exact reproduction. A fresh source reconstruction can be a separately labelled **robustness replication**, with new checksums and explicitly different episodes, not a silently substituted original dataset.

## Decision and falsifier

**ABSTAIN on G1 exact-reproduction and on any strengthened empirical claim** until the pinned SQLite corpus or a demonstrably byte-/episode-equivalent lawful source is available. This does not falsify the reported historical descriptive statistics. It prevents certification of their independent reproduction.

Required checks, in order:

1. Locate the authorized original SQLite input without copying private content into git; compute SHA-256 and compare with the canonical digest above.
2. Inspect SQLite schema and count eligible papers per year, review IDs, duplicate IDs, missing ratings and excluded records. Record the source/version and acquisition chain.
3. Run the frozen Phase 1B and 1C scripts and existing feasibility-conditioned comparator against the *same* verified bytes. Export aggregate, non-identifying counts and results only.
4. If original bytes cannot be recovered, document the gap; design a clearly labelled new-source robustness analysis, never an exact replication.
5. Resolve source-level redistribution and derived-output rights separately before a public data release. Upstream MIT licensing is not a blanket clearance for scraped third-party text or records.

**Gates:** G0 source feasibility partially audited; G1 blocked; G2–G5 not certified by this note. No prior work or results have been rewritten. Capability Transfer remains paused and P1 #68 unaffected.
