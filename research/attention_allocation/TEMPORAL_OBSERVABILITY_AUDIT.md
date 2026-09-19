# Temporal Observability Is a Feasibility Gate

**Agalmic Research — 19 September 2026**

## Result

The Attention Allocation programme needs a stricter distinction than “record available” versus “record missing.” For retrospective allocation experiments, a field is usable only if the value that was genuinely available at the simulated decision time can be reconstructed with defensible provenance.

This changes the acquisition target. A current OpenReview record may be perfectly useful for studying final peer-review outcomes while being inadmissible as decision-time evidence if its review, score, metadata, or discussion state was edited later.

## External evidence

OpenReview's current documentation provides supported retrieval procedures for both API2 and legacy API1 venues and explicitly recommends `get_all_notes`/reply retrieval for submissions, reviews, rebuttals and decisions. This supports continuing to treat the official API as the primary acquisition interface rather than inventing a scraper.

However, recent Paper Copilot work reports that historical review snapshots are not preserved on the official platform in the form needed to reconstruct score evolution: older versions can be overwritten during discussion. Its public archive contains timestamped snapshots for ICLR 2024–2026, not our 2017–2022 development cohort. This is useful evidence about the preservation problem, but it does not repair our historical cohort.

Independent public dumps exist. For example, `qhjqhj00/iclr-openreview-reviews` reports submissions/reviews/meta-reviews/decisions for ICLR 2020–2026 fetched from the public API, while a Kaggle corpus reports ICLR 2018–2023 papers and reviews. These are potentially valuable **coverage witnesses** and acquisition fallbacks for feasibility work. They are not automatically substitutes for the primary source because their crawl time, completeness, transformations and preservation of pre-decision versions differ.

## Novelty boundary

This is not a novel data-engineering insight. Versioned event sourcing, temporal databases, provenance and snapshotting already distinguish current state from historical state. The contribution here is narrower: making **decision-time reconstructability an explicit admissibility axis** for retrospective scientific-attention allocation experiments.

The programme should therefore avoid claiming that a temporal firewall alone solves leakage. A firewall prevents known future fields from entering a policy. It cannot recover a historical value that the source no longer preserves.

## Temporal observability classes

Every candidate policy field receives one of four states:

- **T0_OBSERVED** — value and timestamp/version evidence establish that this value was available at the simulated decision point.
- **T0_DERIVABLE** — raw evidence available at the decision point deterministically yields the value; derivation code/version is frozen and auditable.
- **CURRENT_ONLY** — a current/final value exists but the historical decision-time value cannot be established.
- **UNRESOLVED** — provenance is insufficient to distinguish the above.

Allocation policies may consume only `T0_OBSERVED` and `T0_DERIVABLE`. `CURRENT_ONLY` remains available for descriptive or outcome analysis when appropriate. `UNRESOLVED` is quarantined.

## Audit procedure

For each ICLR year 2017–2022 and each proposed decision-time field:

1. record the official API generation, invitation/schema and returned creation/modification timestamps;
2. determine whether edits create recoverable versions or overwrite prior state;
3. compare a sample of official current records against independently archived dumps where crawl dates are known;
4. classify each field using the four temporal-observability states;
5. report coverage by year and historical acceptance decision;
6. test whether temporal observability itself differs by acceptance status, year, or metadata availability;
7. hash the audit table before any allocation-policy result is inspected.

A third-party snapshot may upgrade a field to `T0_OBSERVED` only when its collection time precedes the simulated decision point, identity matching is independent of outcome, and its provenance/licence are adequate. A post-decision dump cannot reconstruct an overwritten pre-decision review merely because it contains the same note ID.

## Consequence for the planned experiment

The original programme lists contemporaneous reviews, scores, confidence and discussion/meta-review information among potential policy inputs. These are now **optional features pending temporal audit**, not assumed inputs.

A defensible experiment can still proceed without them if submission-time title, abstract, authors, keywords and other genuinely timestamped fields provide adequate support. This would narrow the estimand to allocation from submission-time information rather than allocation from the full historical review state.

If review-derived features are essential to a headline hypothesis and cannot be reconstructed for rejected as well as accepted papers, the correct result is CONDITIONAL PASS or ABSTAIN, not imputation from final reviews.

## Acquisition strategy

Primary: documented OpenReview API1/API2 retrieval after service/access recovery.

Secondary validation: independently archived public datasets may be used to estimate record coverage, detect source drift and test matching logic. They must carry source URL, crawl/publication date, licence, transformation history where known, and content hashes. They do not silently become canonical source data.

Do not spend further attention lowering request cadence absent a documented rate requirement. The present bottleneck is access plus historical-state preservation, not raw throughput.

## Sources

- OpenReview documentation, *How to Get all Notes (for submissions, reviews, rebuttals, etc.)*, current documentation retrieved 19 September 2026.
- OpenReview documentation, *How to Export All Reviews into a CSV*, current documentation retrieved 19 September 2026.
- Paper Copilot, *Tracking the Evolution of Peer Review in AI Conferences* and `papercopilot/openreview`, 2026. The archive reports timestamped ICLR snapshots for 2024–2026 and states that official historical snapshots can be overwritten.
- `qhjqhj00/iclr-openreview-reviews`, public OpenReview-derived ICLR 2020–2026 dump, inspected 19 September 2026.
- Montero et al., *ICLR papers and reviews data 2018–2023*, Kaggle, inspected 19 September 2026.

## Falsification condition

If the audit demonstrates reliable historical version recovery for the target fields and years, downgrade this concern. If it demonstrates that only current/final review state survives for material portions of 2017–2022, prohibit those fields from policy simulation and narrow or abstain from the affected claims.