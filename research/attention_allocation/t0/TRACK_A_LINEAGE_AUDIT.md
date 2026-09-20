# Track A Resubmission / Lineage Audit v0.1

**Date:** 20 September 2026  
**Scope:** ICLR 2020 T0 revision-reference cohort against later ICLR submissions, 2021–2026  
**Status:** outcome-free feasibility evidence; no citation outcomes were read.

## Result

Later ICLR manuscript lineage is detectable but uncommon in the Track A candidate frame.

Across 1,816 ICLR 2020 T0 candidates and 30,568 later ICLR records:

- **10 candidates** have a primary exact-title+author lineage match;
- **19 candidates** have a lineage match when the frozen near-title sensitivity rule is included;
- **3 candidates** have a later ACCEPT lineage under the sensitivity rule;
- **0 candidates** have a later ACCEPT lineage under the primary exact-title rule.

The sparse result is useful: resubmission lineage is real enough that it cannot be ignored, but it is not common enough in this conservative audit to dominate the cohort.

## Historical-decision incidence

### Primary exact lineage

| 2020 decision | Candidates with exact lineage | Total | Fraction |
|---|---:|---:|---:|
| ACCEPT | 0 | 549 | **0.00%** |
| REJECT | 10 | 1,267 | **0.79%** |

ACCEPT-minus-REJECT difference:

**-0.79 percentage points**

95% Newcombe-Wilson interval:

**[-1.45 pp, -0.01 pp]**

The exact-lineage incidence is detectably concentrated among historical REJECT candidates, but the magnitude is far inside the programme's ±5 percentage-point diagnostic margin.

### Exact + near-title sensitivity lineage

| 2020 decision | Candidates with lineage | Total | Fraction |
|---|---:|---:|---:|
| ACCEPT | 2 | 549 | **0.36%** |
| REJECT | 17 | 1,267 | **1.34%** |

ACCEPT-minus-REJECT difference:

**-0.98 percentage points**

95% interval:

**[-1.82 pp, +0.10 pp]**

The full interval lies inside ±5 percentage points.

## Later acceptance

No exact-title descendant is later accepted.

Under the frozen near-title sensitivity rule, **3 historical REJECT candidates** have later ACCEPT descendants:

1. *Regularization Matters in Policy Optimization*  
   → *Regularization Matters in Policy Optimization - An Empirical Study on Continuous Control*  
   Author overlap coefficient: 1.0.

2. *Self-Supervised State-Control through Intrinsic Mutual Information Rewards*  
   → *Mutual Information State Intrinsic Control*  
   Author overlap coefficient: 1.0.

3. *Deep symbolic regression*  
   → *Deep symbolic regression: Recovering mathematical expressions from data via risk-seeking policy gradients*  
   Author overlap coefficient: 1.0.

The historical ACCEPT stratum has 0 later ACCEPT descendants under the same sensitivity rule.

The resulting ACCEPT-minus-REJECT difference in later-accept lineage incidence is:

**-0.24 percentage points**

95% interval:

**[-0.69 pp, +0.48 pp]**

This is not a material imbalance relative to the frozen ±5-point diagnostic margin.

## Edge distribution

The 19 detected lineage edges occur mainly in the immediately following conference cycle:

- 2021: 17 edges
- 2022: 1 edge
- 2023: 1 edge
- 2024–2026: 0 edges under the frozen rules

Later ICLR decisions across those edges:

- ACCEPT: 3
- REJECT: 15
- WITHDRAWN: 1

This temporal concentration is consistent with resubmission/revision behavior rather than arbitrary long-range bibliographic coincidence.

## Adversarial interpretation

The audit is deliberately conservative.

The exact rule will miss genuine descendants whose titles change substantially. The sensitivity rule recovers a small number of plausible changed-title descendants, but it still prioritizes specificity over recall. Therefore:

- **absence of detected lineage is not proof of no lineage**;
- detected exact lineage is strong evidence of manuscript continuity;
- sensitivity-only lineage is evidence for a separate lineage sensitivity stratum, not automatic primary exclusion.

The observed later-accept cases also demonstrate the substantive problem the audit was designed to catch: a rejected 2020 scientific candidate can later be revised, renamed and accepted. Citations to that later manifestation are not clean evidence of value attributable solely to the 2020 manuscript state.

## Gate consequence

The lineage audit does **not** currently force ABSTAIN.

Primary exact lineage is rare, and both exact and sensitivity lineage differences remain well inside the programme's ±5-point materiality margin.

However, later accepted descendants exist. Therefore any downstream citation analysis must:

1. preserve the lineage flags;
2. report a sensitivity analysis excluding detected lineage candidates;
3. avoid treating later visibility as if it were unaffected by manuscript revision or later selection;
4. avoid causal language about value that would have been realised from the original 2020 state.

The three later-ACCEPT sensitivity descendants are especially important as an adversarial subset.

## Prior art

The linkage logic follows conservative bibliographic record-linkage practice rather than inventing a bespoke semantic classifier:

- Qi et al. (2013), *Rule-based deduplication of article records from bibliographic databases*, DOI 10.1093/database/bat086.
- Rathbone et al. (2015), *Better duplicate detection for systematic reviewers*, DOI 10.1186/2046-4053-4-6.
- ASySD (2023), which combines title/author blocking and fuzzy comparison for bibliographic deduplication: https://pmc.ncbi.nlm.nih.gov/articles/PMC10483700/

The present use differs from ordinary deduplication because later submissions are retained as lineage evidence rather than collapsed automatically.

## Evidence artefacts

Persistent research-data artefacts are stored outside the website repository:

- `track_a_lineage_edges.jsonl`
- `track_a_lineage_candidates.jsonl`
- `track_a_lineage_audit.json`

The repository contains the frozen protocol and deterministic audit script.

No OpenAlex citation outcome, citing-work list or future-value label was read by this audit.
