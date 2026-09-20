# T0 Candidate Representation Protocol v0.1

**Date frozen:** 20 September 2026  
**Scope:** ICLR 2020 historical pre-deadline PDFs that have passed acquisition and extraction integrity checks.  
**Status:** engineering protocol only. It does not license outcome analysis or policy ranking.

## Purpose

Construct a transparent, outcome-blind representation of each T0 paper so later allocation-policy experiments can operate on information available at the historical decision point without importing post-2020 model knowledge.

This protocol deliberately avoids pretrained language-model embeddings. A model trained after the simulated decision date can encode later scientific developments, citation patterns, terminology, or downstream popularity. That would blur the temporal firewall even if the source PDF itself is historical.

## Representation unit

The unit is one T0 historical submission PDF.

The input is the ordered page text produced by `scripts/extract-attention-t0-pdfs.py` after source-PDF SHA-256 verification.

No current OpenReview text, later arXiv version, reviews, decision, citations, author reputation, later venue, or post-decision metadata may enter this representation.

## Corpus rule

The representation is fitted **only on the eligible T0 cohort being analysed**.

For the primary feasibility cohort this means ICLR 2020 T0 PDFs that pass the frozen acquisition/extraction gate.

Because the intended first experiment is batch allocation at a common conference deadline, using the contemporaneous candidate pool to fit an unsupervised vocabulary is admissible. This protocol must not be reused unchanged for a sequential-arrival estimand.

## Text normalisation

For every extracted document:

1. concatenate pages in source order with explicit page separators;
2. Unicode-normalise with NFKC;
3. lowercase;
4. replace URLs and email addresses with fixed sentinel tokens;
5. collapse whitespace;
6. do not use outcome-conditioned cleaning;
7. do not remove references or equations solely because they look predictive.

The historical PDF itself is the admissible information boundary.

## Sparse lexical representation

Fit a deterministic TF-IDF representation over the eligible corpus:

- analyzer: word
- lowercase: already performed by the normaliser
- ngram range: (1, 2)
- min_df: 5
- max_df: 0.95
- max_features: 50,000
- sublinear_tf: true
- norm: l2
- token pattern: scikit-learn default word-token pattern

The fitted vocabulary and IDF vector are corpus artefacts and must be hashed.

## Dense geometry

Project the TF-IDF matrix with deterministic truncated SVD:

- components: 128, or the largest valid value below the matrix rank when the corpus is smaller
- algorithm: randomized
- random_state: 20260920
- n_iter: 7

L2-normalise the dense rows after projection.

This dense representation exists only to support geometry-based, transparent allocation baselines. It is not asserted to be a semantic ground truth.

## Frozen unsupervised descriptors

The representation builder may emit the following outcome-blind descriptors:

- document character count;
- token count;
- page count;
- TF-IDF nonzero count;
- cosine distance from the cohort centroid in SVD space;
- mean cosine distance to the five nearest other candidates in SVD space.

The last two are candidate novelty/density descriptors, not validated measures of scientific novelty. They must be labelled accordingly in later analysis.

No threshold for "novel", "minority", "high value", or "plausible" is defined here.

## Prohibited at this stage

Do not compute or use:

- conference decision;
- review score or reviewer confidence;
- later publication;
- later citations;
- author identity or institutional prestige;
- LLM embeddings;
- embeddings from any pretrained model;
- supervised acceptance prediction;
- downstream-value labels;
- post hoc novelty thresholds selected after outcome inspection.

## Output contract

Write artefacts outside git:

- `representation.npz`: dense SVD matrix and scalar descriptors;
- `row_index.jsonl`: row-to-forum/revision mapping with source text and source PDF hashes;
- `vocabulary.json`: fitted TF-IDF terms and indices;
- `idf.npy`: IDF vector;
- `representation_manifest.json`: all parameters, package versions, input hashes, output hashes, corpus size, and dimensionality.

Do not include historical decision labels in any representation artefact.

## Gate

This representation may be promoted from an engineering fixture to an empirical policy input only after:

1. bulk ICLR 2020 acquisition completes;
2. the extraction/missingness audit passes or yields a prospectively narrowed cohort;
3. the eligible cohort definition is frozen;
4. representation generation is rerun from that frozen cohort;
5. a leakage audit confirms that no FUTURE_OUTCOME or historical-decision field is reachable from the feature matrix.

Only after those conditions may allocation policies consume the representation.
