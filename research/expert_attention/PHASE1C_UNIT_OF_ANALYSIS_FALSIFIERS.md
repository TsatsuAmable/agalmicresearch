# Phase 1C: independent unit-of-analysis and preservation-floor audit

**Status:** adversarial methodological finding, 22 November 2026. This note does not claim to rerun the frozen SQLite corpus. Sources: `docs/EXPERT_ATTENTION_PHASE1B_FINDINGS.md`, `docs/EXPERT_ATTENTION_PHASE1C_FINDINGS.md`, and the Phase 1C technical-report draft. The empirical observations below are quoted from those frozen reports, not newly estimated.

## Falsifier A: pooled recall is not a per-regime guarantee

Let `C_y` be the number of true hidden-third-review midpoint crossings in year `y`, and `S_y` the number of those crossings selected by the policy. Pooled recall is `sum_y S_y / sum_y C_y`; year-specific recall is `S_y/C_y` when `C_y>0`. Pooled recall is a crossing-count-weighted average of the year-specific recalls, **not their minimum**. Hence pooled recall >=0.95 does not imply any particular year's recall >=0.95. When `C_y=0`, that year's recall is undefined, not automatically 100%.

The frozen report's first fresh split at nominal 55% budget has reported recalls: 2017 100.0%, 2018 97.4%, 2019 99.4%, **2020 93.2%**, **2021 94.6%**. Thus the stronger within-year >=95% claim is **falsified at that budget** even if the preregistered pooled endpoint passes. These percentages are rounded; the original counts are required for exact independent adjudication. The report also says the first split reaches >=97.7% in each year at 65%, which does not establish that 65% suffices for every other split.

**Publication consequence:** report pooled RWS@95 as a retrospective endpoint only. Do not describe the 45% median as savings under a within-year safety floor. A separate `RWS@95_each_year` may be computed post hoc only after exact counts are reproduced, and must be labelled exploratory.

## Falsifier B: the 20 splits are not 20 independent samples

All 20 deterministic holdouts reuse the same eligible papers and reviewer-score corpus; the seed changes which stored rating is held out. Therefore the distribution of 20 RWS values measures *partition sensitivity conditional on this fixed corpus*, not between-conference variability or prospective generalization. A conventional confidence interval treating 20 seeds as independent conferences would be pseudoreplication. A paper-level resampling analysis would address within-corpus sampling uncertainty only if paper identifiers, clustering and the original sampling frame are correctly respected; it still would not establish venue transportability. Report the observed split range as descriptive, not as a 95% confidence interval.

## Falsifier C: review-work denominator and optimization target

At nominal budget `b`, the policy allocates `max(1, round(b*N_y))` slots within each year. Exact fraction of simulated third reviews saved is `1 - sum_y selected_y/sum_y N_y`, which need not equal `1-b`. The preregistered `RWS@95` based on tested nominal budgets must not silently be renamed exact saved fraction. The denominator is **one optional simulated third review per eligible episode**, not historical reviewer hours, all conference reviews, accepted papers, or total labor.

The crossing target is a deterministic function of first-two scores and the held-out third score; a boundary-based policy is structurally aligned with that target. It does not measure correctness of acceptance, review quality, fairness or value of scientific contributions. Compare against a feasibility-conditioned random allocator and retain the known equivalence of uniform legal-third-rating probability and midpoint proximity apart from ties; do not misrepresent the latter as independent predictive evidence.

## Minimum executable acceptance checks before release

1. Verify the frozen SQLite SHA-256 `ceeaa4316f76f6a22a5856128f34e8c3f35693d145db756f9688eda42ee20ed2`, eligible cohort N=7,531, source rights and exact split seeds.
2. For each seed, year, policy and budget, export integer `N_y`, selected slots, crossing events `C_y`, captured events `S_y`. Reject `S_y>C_y`, `S_y>selected_y`, missing strata, duplicated seeds and mismatched pooled totals.
3. Report both nominal RWS@95 and actual allocated-slot savings at the qualifying budget. Recompute exact pooled recall and every defined year-specific recall. Do not treat zero-event strata as successes.
4. Compare boundary proximity to the feasibility-conditioned randomized comparator with predeclared deterministic tie handling. Quantify paired per-seed differences without pretending seeds are independent datasets.
5. If exact input is inaccessible, publish a reproducible **methodological limitation and synthetic verifier** rather than an empirical replication claim. No retrospective 45% figure should be labelled independently verified.

**Decision:** the preregistered pooled result remains a reported positive finding, but within-year preservation at the median-budget example is contradicted. G0/G1 remain open until frozen-data reproduction and comparator analysis. This is a bounded adversarial audit, not an external review or public release.
