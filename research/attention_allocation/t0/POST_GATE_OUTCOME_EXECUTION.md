# Post-Gate Outcome Execution v0.1

**Frozen implementation:** 20 September 2026  
**Scope:** Track A citation acquisition and evaluation after the broader pre-outcome feasibility verdict.

## Boundary

This stage is dormant unless `broader_pre_outcome_adjudication.json` explicitly contains:

- `citation_outcome_acquisition_authorized=true`;
- verdict `PASS_PRE_OUTCOME` or `CONDITIONAL_PASS_PRE_OUTCOME`;
- `outcomes_observed=false` at the moment authorization is issued.

An ABSTAIN verdict exits before any citation-network request is made.

The post-gate wrapper does not rebuild the representation, refit policies, change the outcome window, or redefine the primary endpoint.

## Frozen primary outcome

For every candidate in the final technically usable cohort with a primary exact OpenAlex identity cluster:

- follow-up window: **2019-09-26 through 2024-09-25 inclusive**;
- primary outcome: **C5**, the number of distinct OpenAlex works citing any member of that candidate's exact identity cluster inside the fixed window;
- multiple manifestations are unioned;
- citing work IDs are deduplicated per candidate.

Candidates without a primary exact identity remain unobserved. They are not assigned zero citations.

## Batched OpenAlex acquisition

The original per-work citation acquirer remains available as a simple reference implementation. The preferred executor now uses batched `cites` filters.

OpenAlex documents that OR filters may contain up to 100 values and that `referenced_works` exposes outgoing citation IDs:

- https://help.openalex.org/api/filtering/
- https://help.openalex.org/how-to/api-recipes/
- https://help.openalex.org/api/selecting-fields/

The batched executor therefore:

1. maps every exact identity-cluster work ID to exactly one frozen candidate;
2. fails closed if an OpenAlex work ID is shared across candidates;
3. sorts all unique work IDs and partitions them into batches of at most 100;
4. requests citing works using:
   - `cites:W1|W2|...`;
   - the frozen publication-date window;
   - `select=id,publication_date,referenced_works`;
5. attributes each citing work back to every target work actually present in its `referenced_works` list;
6. unions and deduplicates citing works across all manifestations of a candidate;
7. materializes the same per-candidate `FROZEN_C5_OUTCOME` files consumed by the frozen evaluator.

This reduces request overhead without changing the candidate-level outcome definition.

## Cost and provider controls

Default total OpenAlex budget for one execution is **$0.09**.

The executor:

- records per-batch API cost;
- records network-attempt and successful-page counts separately;
- freezes every raw response;
- stops on the configured total cost cap;
- stops on HTTP 429 rather than attempting a bypass;
- stops on authentication/access failures;
- resumes completed deterministic batches only when their target-work hash still matches.

A partial run never creates the final complete candidate-outcome set.

## Frozen evaluation

After complete acquisition, the existing evaluator runs unchanged with:

- 20% primary attention budget;
- top-decile high-recognition outcome;
- seeded-random baseline;
- five structured allocation policies;
- 10,000 paired bootstrap replicates, seed 20260920;
- 10,000 exchangeability randomizations, seed 20260921;
- five-percentage-point smallest effect of interest.

The evaluator never refits policy selections.

## Mandatory lineage sensitivities

After the primary analysis, the wrapper constructs two immutable outcome views without changing any outcome value:

1. **exclude_any_lineage**  
   Excludes every candidate flagged by the frozen exact + near-title lineage audit.

2. **exclude_later_accept_lineage**  
   Excludes candidates with a later ACCEPT descendant under the frozen lineage sensitivity rule.

The same frozen evaluator is rerun on both views.

Outcome files are hard-linked where possible, otherwise copied byte-for-byte. The sensitivity builder records exactly which candidate IDs were excluded.

These analyses satisfy the prospectively declared requirement that later manuscript evolution and later selection cannot be silently ignored.

## Fail-closed validation

The executor has been validated without opening Track A citation outcomes:

- an ABSTAIN fixture exits with `POST_GATE_OUTCOME_STAGE_NOT_AUTHORIZED` and zero network activity;
- an authorized fixture with a pre-request cost ceiling below one API call exits as a partial acquisition with zero network activity;
- synthetic citation-page attribution correctly assigns a citing work to multiple target candidates when its `referenced_works` contains multiple target IDs and deduplicates repeated citing IDs;
- lineage sensitivity views correctly exclude frozen lineage flags without changing the retained outcome files.

## Result status

The wrapper writes one of:

- `POST_GATE_OUTCOME_STAGE_NOT_AUTHORIZED`;
- `POST_GATE_CITATION_ACQUISITION_PARTIAL`;
- `POST_GATE_PRIMARY_ANALYSIS_COMPLETE`.

The final status binds the broader adjudication, acquisition manifest, primary analysis and lineage sensitivity analyses by hash.

## Interpretation

Even after authorization, the result remains a descriptive test of **recovery of observable downstream recognition under fixed attention budgets**.

It does not identify a causal effect of conference acceptance, reviewer attention, or allocation on scientific value.
