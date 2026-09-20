# Track A Resubmission / Lineage Audit Protocol v0.1

**Frozen:** 20 September 2026  
**Scope:** ICLR 2020 T0 revision-reference cohort, searched against later ICLR submissions from 2021–2026.  
**Status:** outcome-free feasibility diagnostic. No citation outcomes are read.

## Why lineage matters

A rejected or withdrawn 2020 submission may later reappear as a revised submission, possibly under a changed title and possibly with a different conference decision.

That later manifestation is not an independent scientific object. If downstream bibliographic outcomes are attached to the later manifestation, retrospective evaluation can accidentally mix:

- value present in the 2020 candidate;
- improvements made after the simulated allocation decision;
- later conference selection and visibility;
- later author/title changes.

The purpose of this audit is therefore not to erase resubmissions. It is to quantify lineage and keep later outcome interpretation honest.

## Prior art

Bibliographic record linkage and deduplication commonly combine title and author evidence rather than relying on a single string field. Relevant precedents include:

- Qi et al., *Rule-based deduplication of article records from bibliographic databases* (Database, 2013), which compares identifiers, titles, author lists and other fields using approximate text matching: https://doi.org/10.1093/database/bat086
- Rathbone et al., *Better duplicate detection for systematic reviewers* (Systematic Reviews, 2015), which reports improved duplicate detection when title/author evidence is combined with fuzzy name handling: https://doi.org/10.1186/2046-4053-4-6
- ASySD (2023), which uses title/author blocking plus string-comparison evidence for bibliographic duplicate detection: https://pmc.ncbi.nlm.nih.gov/articles/PMC10483700/

Those systems target duplicate bibliographic records. This audit is narrower: it treats later submissions as possible descendants of a historical candidate and reports the evidence rather than collapsing records automatically.

## Data

Source: frozen `berenslab/iclr-dataset` parquet already used by Track A.

For each 2020 T0 candidate, compare against later ICLR records with:

- year in 2021–2026;
- title;
- author string;
- later ICLR decision.

Later decision is evaluation-side metadata only. It is never available to the allocation policy.

## Normalisation

### Title

- Unicode NFKC;
- lowercase;
- replace every non-alphanumeric run with one space;
- collapse whitespace;
- trim.

### Author surname set

For each comma-separated author name:

- Unicode NFKC;
- split on whitespace;
- strip punctuation other than apostrophe and hyphen;
- use the final non-empty token as the surname;
- lowercase;
- deduplicate into a set.

This is deliberately simple and auditable. It is not asserted to solve all international-name ambiguity.

## Primary lineage rule

A later ICLR record is a **PRIMARY_EXACT_LINEAGE** match when:

1. normalized title is exactly equal;
2. at least one author surname overlaps;
3. later year is 2021–2026.

All matches are retained. A candidate may have multiple later descendants.

This is the primary lineage definition because it prioritizes specificity over sensitivity.

## Sensitivity lineage rule

A later ICLR record not already matched by the primary rule is a **SENSITIVITY_NEAR_LINEAGE** match when all are true:

1. RapidFuzz token-set title similarity >= **0.97**;
2. author-surname overlap coefficient >= **0.50**, where overlap coefficient is `|A∩B| / min(|A|, |B|)`;
3. at least one surname overlaps;
4. later year is 2021–2026.

The 0.97 title threshold and 0.50 author-overlap threshold are frozen before the audit result is observed and mirror the already-frozen conservative fuzzy identity sensitivity philosophy used elsewhere in Track A.

Sensitivity matches never silently replace the exact-lineage primary analysis.

## Later-decision descriptors

For every lineage edge, record the later ICLR decision class:

- ACCEPT;
- REJECT;
- WITHDRAWN;
- DESK_REJECTED;
- other/missing.

For every 2020 candidate report:

- any later exact lineage;
- any later near-lineage sensitivity match;
- any later ACCEPT lineage;
- first later-lineage year;
- number of later lineage records.

These are lineage diagnostics, not outcome labels for allocation.

## Decision-linked lineage diagnostic

Report lineage incidence separately by the historical 2020 decision stratum.

Primary diagnostic:

`P(any exact lineage | 2020 ACCEPT) - P(any exact lineage | 2020 REJECT)`

with a 95% Newcombe-Wilson interval.

Also report:

`P(any later ACCEPT lineage | 2020 ACCEPT) - P(any later ACCEPT lineage | 2020 REJECT)`.

No equivalence claim is made unless the full interval lies inside the already-used ±5 percentage-point diagnostic margin.

## Candidate-level output

The audit writes:

- one outcome-free lineage edge file;
- one per-candidate lineage summary;
- aggregate decision-stratified audit;
- hashes of the candidate manifest and later ICLR metadata source.

No citation count, citing-work list, or OpenAlex outcome is read.

## Gate consequence

Lineage is not automatically an exclusion criterion.

Instead:

- **no detected lineage:** downstream identity may be interpreted as the observed later trajectory of the original candidate, subject to all other limitations;
- **detected exact lineage:** downstream outcomes are explicitly lineage-contaminated because later manuscript evolution and later selection may contribute;
- **sensitivity-only lineage:** primary analysis remains unchanged, but the candidate enters a lineage sensitivity analysis.

If later ACCEPT lineage is materially concentrated among historical REJECT candidates, downstream citation recovery cannot be interpreted as if all observable value arose from the 2020 submission state.

## Stop rule

Do not use lineage findings to retune allocation policies, representation parameters, identity thresholds, citation windows, or the high-recognition definition.

The audit may narrow claims, create a sensitivity stratum, or force ABSTAIN on a causal interpretation. It does not reopen the preregistered design.
