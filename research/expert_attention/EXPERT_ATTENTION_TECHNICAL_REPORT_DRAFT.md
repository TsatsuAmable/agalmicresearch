# What Does a Third Review Change? A Retrospective ICLR Rating-Triage Benchmark

**Agalmic Research | Technical report draft 0.1 | 22 November 2026 | NOT RELEASED**
**Status:** Phase 1B and 1C findings transcribed from frozen reports; stronger post-hoc baselines and independent fresh-checkout reproduction PENDING. This is a complete narrative draft, not an independently validated final report.

## Abstract
**Question:** Can two existing reviewer scores identify which papers merit a simulated third review? **Design:** A retrospective, deterministic synthetic holdout of stored ICLR reviewer ratings from 2017–2021, retaining one of three ratings as a hidden outcome. **Outcomes:** Absolute aggregate-score update, large-update recall, and crossing of the normalized recommendation midpoint. **Findings:** The frozen Phase 1B report covers 7,531 eligible papers. At a 20% simulated third-review budget, disagreement captured 22.4% of update mass versus 19.5% under random selection; its +2.9 percentage-point advantage missed the prespecified +5-point materiality rule. The frozen Phase 1C report finds that midpoint proximity reached at least 95% *pooled* crossing recall while retaining a median 45% of the simulated third-review slots across 20 fresh deterministic splits. **Critical qualification:** Crossing eligibility is mathematically constrained by the two observed scores, making proximity partly aligned with the definition of the target. Exact discrete-score enumeration shows 70 of 100 ordered first-two rating pairs can cross on ten-level scales, and 10 of 16 on the four-level 2020 scale. Whether proximity outperforms a feasibility-aware randomized baseline on the observed corpus is **UNKNOWN**; legal-score uniform crossing probability is rank-equivalent to midpoint proximity apart from ties, pending checksum-verified execution. **Conclusion:** The frozen evidence supports an objective-specific *retrospective* benchmark result, not an algorithmic novelty claim or a prospective reviewer-work saving.

## 1. Introduction and prior art
Allocating scarce expert attention is a selection problem. Standard active learning and uncertainty sampling prioritize cases whose labels are uncertain or expected to change a decision boundary. This broad family of approaches predates this report (Lewis and Gale, 1994; Settles, 2009). A near-midpoint rule is therefore **not** claimed as a new algorithm. The incremental question here is whether a particularly transparent, objective-specific heuristic is a useful retrospective baseline for *additional* expert review once two scores already exist.

The distinction between outcomes matters. A third review can change a mean substantially without changing which side of a recommendation midpoint it lies on; conversely, a small change near the midpoint can change its side. Neither score change nor midpoint crossing measures paper merit, actual acceptance, reviewer fairness, or the causal value of extra scrutiny. The empirical contribution, if reproduced, is a benchmark separating these objectives, preserving a preregistered negative result and a narrowly positive follow-up.

**Prior-art boundary:** Lewis and Gale's sequential text-classification selection and Settles's active-learning synthesis establish uncertainty-based selection as known. This draft does not yet contain a verified systematic prior-art review of reviewer triage or editorial allocation. **Novelty assessment remains OPEN** and should favor a replication-grade technical report rather than a methodological invention claim.

## 2. Data, design, and estimands
The canonical source is the frozen SQLite snapshot with SHA-256 `ceeaa4316f76f6a22a5856128f34e8c3f35693d145db756f9688eda42ee20ed2`. The original script selects ICLR submissions from 2017–2021 with at least three nonmissing valid reviewer ratings, normalizes each year by *rank on that year's allowed scale*, and creates one episode per eligible paper. The frozen Phase 1B report states N=7,531. Data access, licensing, lawful redistribution and independent source checks must be completed before release; the checksum is not evidence of redistribution permission.

For each deterministic split, a hash of seed, paper identifier and review identifier orders ratings. The first two normalized ratings `a,b` are visible; the third `c` is hidden from the ranking policy. Let `m2=(a+b)/2`, `m3=(a+b+c)/3`, and `u=|m3-m2|`. The midpoint-crossing indicator is `I[(m2<0.5<=m3) OR (m3<0.5<=m2)]`. Equality is asymmetric by definition and must not be silently changed.

At a budget fraction `b`, policies rank separately within year and select `max(1, round(b*N_year))` episodes. Update-mass capture is `sum(selected u)/sum(all u)`. Large-update recall is the fraction of within-year top-decile updates selected, with ties included. Midpoint-crossing recall is `number of crossing episodes selected / all crossing episodes` pooled across years. The denominator is **crossing episodes**, not selected papers, review hours, conference decisions or all submitted manuscripts.

Phase 1C tests budgets 0.05 through 1.00 in increments of 0.05. `RWS@95=1-minimum tested budget attaining >=0.95 pooled crossing recall`, and is zero if no tested budget qualifies. The work denominator is the *one simulated optional third review per eligible paper episode*. It is not a proportion of all historical reviews saved. Due to rounding by year, actual selected fraction can differ slightly from nominal budget.

The frozen policies are random, absolute first-two-score disagreement, midpoint proximity `max(0,1-2*abs(m2-0.5))`, and their half-weight hybrid. Phase 1B used primary seed 20260924 and 20 deterministic sensitivity seeds; Phase 1C used new seeds 20261001–20261020. Different seeds reuse the **same underlying papers**, so the 20 split outcomes are paired simulation variability, not 20 independent cohorts or an external-validation confidence interval.

## 3. Frozen findings
### Phase 1B: negative primary hypotheses
At a nominal 20% review budget, random versus disagreement respectively captured 19.5% versus 22.4% update mass and 19.6% versus 22.9% large updates. The preregistered 5-point materiality threshold was not met for either objective, despite positive direction across all 20 sensitivity splits. Thus H1 and H2 are **NOT SUPPORTED**; a stable small advantage is not a material success. The hybrid did not dominate simpler policies.

### Phase 1C: positive, restricted target
The frozen report gives median RWS@95 across fresh seeds of 0% random, 10% disagreement, 45% boundary proximity (range 45–50%), and 35% hybrid. All 20 boundary splits saved at least 30% of simulated slots while achieving the pooled threshold. These figures are **reported from the canonical frozen findings, not independently regenerated in this draft**.

The first fresh split at a 55% nominal budget reportedly yielded year-specific crossing recall of 100.0%, 97.4%, 99.4%, 93.2%, and 94.6% for 2017–2021 respectively. Hence 95% pooled recall does **not** guarantee a 95% floor in every year. A prospective policy must protect each rating regime separately.

## 4. Post-hoc mathematical falsification
A crossing requires that at least one legal third rating can move `m3` across 0.5. Since `c` is in [0,1], a necessary continuous condition is `0.25 <= m2 < 0.75`. Actual feasibility is stricter where the year-specific discrete scale excludes required values. Exact rational enumeration over ordered score pairs and all legal third scores gives:

| Normalized score levels | Ordered first-two pairs | Pairs admitting a crossing | Crossing triples / all uniform triples |
|---|---:|---:|---:|
| 10 (2017–2019, 2021) | 100 | 70 | 210/1000 |
| 4 (2020) | 16 | 10 | 14/64 |

These fractions describe an **independent uniform-score mathematical null**, not real score distributions or crossing frequencies. They establish a structural challenge: ranking near the midpoint uses information directly related to whether the event is even possible. An unrestricted random baseline does not isolate any additional predictive value beyond that geometry.

A post-hoc script in this branch, `feasibility_baseline_audit.py`, specifies three relevant competitors: (i) uniform random among mathematically feasible pairs, (ii) uniform random among pairs feasible on the actual year-specific legal rating scale, and (iii) ranking by crossing probability if the hidden score were hypothetically uniform over that legal scale. The third is **not** an estimated probability model or an independent predictive baseline: exact rational enumeration establishes the same ordering as midpoint proximity on both frozen legal rating scales, except for tie-breaking. It is retained solely as a tie-sensitivity control. All rankers use visible scores only; observed hidden scores enter evaluation only. The script checks original random and boundary recall parity on all frozen seeds and budget levels and aborts if the input checksum differs.

**Pending empirical cells:** paired per-split RWS@95 differences against the feasibility-conditioned randomized baselines; tie-order sensitivity for the uniform-probability control; per-year crossing counts and recall; sensitivity to midpoint tie conventions; empirical within-year score marginals; stability under paper-level resampling. These cells are UNKNOWN, not zero and not evidence of superiority. No retrospective result should be promoted to a prospective claim.

## 5. Statistical interpretation, adversarial checks, and limits
The unit of observation is a paper episode. The same papers recur across deterministic splits, so confidence intervals treating split summaries as independent observations would be invalid. Report the full paired split distribution as a *stability diagnostic*, and if inferential uncertainty is desired use a paper-level resampling or another dependence-respecting design, with year stratification and fixed policy rules. A 95% recall threshold is a design target, **not** a 95% statistical confidence bound.

Threats include exchangeable rather than chronological third-score withholding, review-selection bias, normalization differences across years, year-specific ties, threshold asymmetry, possible dependence between reviews of the same paper, target-policy mathematical coupling, and unknown representativeness outside ICLR 2017–2021. The benchmark does not measure actual workload hours, quality, fairness, or final acceptance. No publication, deployment, or externally reproduced effectiveness claim is justified.

A stringent falsifier is that boundary proximity offers no meaningful paired advantage over discrete-feasibility randomized baselines. Uniform-probability ranking is algebraically rank-equivalent and cannot independently falsify the boundary rule. Such an outcome would preserve the reported retrospective pooled result while removing any interpretation of special predictive value beyond score geometry. If the benchmark cannot be reproduced from a legally accessible source snapshot, report the frozen results as unverified and **ABSTAIN** on independent reproduction.

## 6. Discussion and conclusion
The strongest defensible insight is *objective specificity*: disagreement was weak at preserving broad update mass, while a boundary heuristic was strong at preserving midpoint-crossing events under the frozen synthetic holdout. The latter is partly expected from the event definition itself. A good benchmark must therefore compare policies to the strongest transparent geometry-aware null, not merely unrestricted random allocation.

The Phase 1C result is a bounded retrospective observation about stored scores and a chosen threshold. It is not a validated staffing recommendation. A separate prospective study would need sequentially observed reviews, within-regime recall floors, harms, cost in actual reviewer time, and independent governance; it is **not** a prerequisite to releasing a truthful retrospective technical report.

## 7. Reproducibility and declarations
Canonical scripts: `research/expert_attention/review_value_holdout.py`, `boundary_preservation.py`, and draft `feasibility_baseline_audit.py`. Frozen protocols and findings: `docs/EXPERT_ATTENTION_PHASE1B_REVIEW_VALUE_PROTOCOL.md`, `docs/EXPERT_ATTENTION_PHASE1C_BOUNDARY_PROTOCOL.md`, and their respective `*_FINDINGS.md`. Post-hoc exact arithmetic: `research/expert_attention/PHASE1C_EXACT_NULL_GEOMETRY.md`. Raw database redistribution is **not authorized by this draft**. Fresh-checkout pinned reproduction, data-source licensing, figure generation and independent adversarial review remain release gates.

No outside review, adoption, deployment, or prospective savings is claimed. No human-subject identity data is reproduced here.

## References
- Lewis, D. D., & Gale, W. A. (1994). A sequential algorithm for training text classifiers. *SIGIR '94*, 3–12. DOI: 10.1007/978-1-4471-2099-5_1.
- Settles, B. (2009). *Active Learning Literature Survey*. Computer Sciences Technical Report 1648, University of Wisconsin–Madison.
- Agalmic Research (2026). *Expert-Attention Phase 1B Findings: Marginal Review Value*. Frozen internal protocol and findings, 24 September.
- Agalmic Research (2026). *Expert-Attention Phase 1C Findings: Boundary Preservation*. Frozen internal protocol and findings, 24 September.

**Release gate:** G0 OPEN pending empirical stronger-baseline and prior-art/licensing audit; G1–G5 NOT PASSED.
