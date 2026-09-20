# Temporal Observability Matrix v1

**Programme:** Attention Allocation Under Cognitive Abundance  
**Date:** 2026-09-20  
**Status:** feasibility artefact, not an outcome analysis

## Question

Can the ICLR 2017–2022 development cohort support a leakage-resistant retrospective test of attention-allocation policies?

This matrix separates *coverage* from *decision-time observability*. A dataset containing a review today does not establish that the stored value is the value an allocator could have observed at the simulated decision time.

## Admissibility vocabulary

- **T0_OBSERVED** — preserved value with evidence tying it to the relevant decision-time state.
- **T0_DERIVABLE** — value can be reconstructed from preserved, timestamped pre-decision records under a documented deterministic transformation.
- **CURRENT_ONLY** — value exists now, but its historical decision-time state is not established.
- **UNRESOLVED** — coverage or temporal provenance has not yet been demonstrated.

Only T0_OBSERVED and T0_DERIVABLE are admissible policy inputs.

## Evidence inventory

| Source | Years relevant here | Submission metadata | Decision | Review scores/text | Revision/time evidence | Role |
|---|---:|---|---|---|---|---|
| OpenReview official API / forum records | 2017–2022 | yes in principle | yes in principle | yes in principle | interface-dependent; historical versions require verification | primary authority |
| berenslab/iclr-dataset | 2017–2022 | title, abstract, keywords and IDs; placeholder abstracts excluded | yes | reviewer scores | no decision-time snapshot guarantee documented | coverage witness / derived corpus |
| ntunlplab/PRRCA | 2017–2022 | year-separated ICLR submission corpus | corpus includes peer-review/rebuttal material | yes by corpus purpose | historical snapshot semantics not established by repository description | coverage witness |
| Jasonpicky/openreview_raw | 2013–2025 | forum metadata | decision note type | reviews/comments/meta-reviews | `note_created` timestamps, but crawl-time/current-state preservation is not equivalent to revision history | timestamp witness, not automatically T0 |
| ErikBird/OpenReviewCrawler | historical OpenReview | submissions | notes include decisions | comments/reviews | explicitly models previous revisions for submissions and notes | reconstruction lead; provenance must be validated |
| Paper Copilot OpenReview archive | broad; timestamped ICLR subset is later than development cohort | yes | status/review signals | yes | timestamped subset does not cover 2017–2022 | method/coverage witness, not development-cohort T0 authority |

## Year-by-field matrix

The conservative classification below deliberately refuses to infer historical state from present availability.

| Field | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | Current verdict |
|---|---|---|---|---|---|---|---|
| submission/forum ID | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | identifiers are strongly covered, but source snapshots still need acquisition/provenance binding |
| title | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | likely stable, not yet proven decision-time immutable |
| abstract | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | revisions and placeholder filtering prevent automatic T0 admission |
| keywords | UNRESOLVED | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | availability varies; transformations in derived corpora must not become hidden inputs |
| review text | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | broad coverage exists, but overwritten/edited review state remains a temporal risk |
| review score | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | current score is not automatically the pre-discussion score |
| review confidence | UNRESOLVED | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | schema varies by year |
| rebuttal/discussion | UNRESOLVED | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | inherently post-review and phase-sensitive |
| final decision | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | suitable as an outcome label if provenance is bound; never an allocator input |
| note creation timestamp | UNRESOLVED | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | CURRENT_ONLY | timestamps can order surviving notes but do not prove absence of overwritten versions |
| revision history | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | reconstruction lead exists, but cohort-wide preservation has not been established |

## Adversarial finding

The existence of multiple independent ICLR corpora changes the bottleneck but does not remove it. **Coverage scarcity is substantially displaced; temporal provenance scarcity is not.** Several corpora demonstrate that submissions, decisions and reviews for the target years are recoverable at useful scale. None of the evidence inspected so far establishes, cohort-wide, that review scores/text represent the exact state available to an allocator at a chosen historical cut-off.

A tempting shortcut is to treat note creation timestamps as sufficient. That fails if a note was subsequently edited and only the latest content survives. Conversely, requiring complete review revision history for every experiment would be unnecessarily strict if an experiment uses only submission-time features.

## Feasible experimental fork

### Track A — submission-time allocator

Use only features demonstrably fixed or reconstructable before review: forum ID plus provenance-bound title/abstract/keywords or representations derived solely from their admitted versions. Final decision may be an outcome, never an input. This track can proceed once primary/independent records are reconciled and hashes/provenance are recorded.

### Track B — review-aware allocator

Any policy consuming scores, confidence, review text, rebuttal or discussion remains gated until the relevant pre-decision state is T0_OBSERVED or T0_DERIVABLE. Current-state review corpora are insufficient by themselves.

This fork prevents the richer but less observable Track B from blocking a narrower falsifiable Track A.

## Novelty challenge

Temporal versioning, event sourcing, leakage prevention and dataset provenance are established ideas. The contribution claimed here is narrower: an explicit *field × year × decision-time admissibility matrix* used as a precondition for retrospective attention-allocation experiments. No claim is made that the underlying provenance techniques are novel.

## Decision rule

The programme may advance to a Track A pilot when:

1. a deterministic cohort manifest for at least two target years is produced;
2. each allocator input is T0_OBSERVED or T0_DERIVABLE;
3. accepted/rejected coverage and exclusions are quantified;
4. raw-source hashes and acquisition provenance are preserved; and
5. no final-decision or post-review information can enter feature construction, including through pretrained/derived metadata without an explicit leakage audit.

Otherwise ABSTAIN rather than silently weakening the temporal standard.

## Sources inspected

- OpenReview documentation and public records (primary source; acquisition currently subject to interface/access issues documented elsewhere in this programme).
- González-Márquez & Kobak / `berenslab/iclr-dataset`, complete ICLR scrape with 2017–2026 submission metadata, decisions and reviewer scores: https://github.com/berenslab/iclr-dataset
- NTU NLP Lab PRRCA, year-separated ICLR 2017–2022 peer-review/rebuttal corpus: https://github.com/ntunlplab/PRRCA
- `Jasonpicky/openreview_raw`, OpenReview-derived note corpus with creation timestamps and note types: https://huggingface.co/datasets/Jasonpicky/openreview_raw
- `ErikBird/OpenReviewCrawler`, historical crawler explicitly representing prior revisions of submissions and notes: https://github.com/ErikBird/OpenReviewCrawler
- Paper Copilot OpenReview archive: https://github.com/papercopilot/openreview

Third-party sources above are evidence about coverage and possible reconstruction paths, not substitutes for primary provenance.
