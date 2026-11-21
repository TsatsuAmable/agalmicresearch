# Phase 1C: exact null-model geometry (post-hoc falsification note)

**Scope:** mathematical audit of the *frozen* midpoint-crossing event, not an empirical reanalysis and not an additional study. This note is post-hoc and must not be represented as a preregistered Phase 1C finding.

## Exact enumeration

Let the first two normalized ratings be `a,b`, their mean be `m=(a+b)/2`, and the hidden third rating be `c`. The event is exactly

`(m < 1/2 <= (a+b+c)/3) OR ((a+b+c)/3 < 1/2 <= m)`.

For each frozen rating regime, enumerate **ordered** first-two pairs and all legal third-rating levels, giving `n^3` equally weighted triples under a **hypothetical independent uniform-ratings null**. This is an analytic null, **not** an estimate of reviewer behavior. All calculations below use exact rational arithmetic.

| Frozen years | Levels n | Ordered pairs | Pairs admitting at least one crossing | Crossing triples / all triples | Uniform-null event probability |
|---|---:|---:|---:|---:|---:|
| 2017, 2018, 2019, 2021 | 10 | 100 | 70 | 210 / 1000 | 21.000% |
| 2020 | 4 | 16 | 10 | 14 / 64 | 21.875% |

The values can be verified with the standard-library-only script below (or independently with `fractions.Fraction`). The 2020 4-level regime has a smaller *feasible-pair fraction* (62.5% versus 70%), while the uniform-null event prevalence is similar. These figures **do not imply** that real reviews have similar event prevalence, because real rating marginals, within-paper correlation, and reviewer selection are not uniform or independent.

```python
from fractions import Fraction
for n in (10, 4):
    levels = [Fraction(i, n-1) for i in range(n)]
    possible_pairs = crossing_triples = 0
    for a in levels:
        for b in levels:
            m = (a+b)/2
            hits = sum((m < Fraction(1,2) <= (a+b+c)/3) or
                       ((a+b+c)/3 < Fraction(1,2) <= m)
                       for c in levels)
            possible_pairs += hits > 0
            crossing_triples += hits
    print(n, possible_pairs, crossing_triples, n**3)
```

## Consequences for the publication claim

1. **Structural enrichment:** All crossing events are concentrated in 70% (ten-level) or 62.5% (four-level) of the ordered pair states under exhaustive support. An allocator which only knows feasibility can eliminate impossible states before learning anything about reviewer behavior. Therefore an unrestricted-random comparison overstates evidence for a novel predictive method.
2. **Probability versus feasibility:** The event's probability under uniform third ratings varies *within* the feasible band. A feasibility-only random baseline is weaker than a ranker based on exact legal-level crossing probability. Both must be compared to boundary proximity on the **observed frozen corpus**, not on this hypothetical null alone.
3. **Rating dependence:** The two visible ratings and held-out third rating come from the same paper; exchangeability across randomly selected reviews does not imply independent scores. The exact null prevalence cannot serve as a confidence bound or empirical expected recall.
4. **Ties and direction:** The event definition counts equality at 0.5 asymmetrically. A change to strict inequalities or to a different threshold changes the target; such tests are sensitivity analyses, not repairs to the frozen outcome.
5. **Budget denominator:** Phase 1C review work saved is `1 - minimum tested fraction of eligible paper episodes selected` at pooled crossing recall >= 0.95, not saved conference review hours or fraction of all reviews avoided. Split-level results are repeated simulations on the **same** underlying papers and must not be treated as independent external samples.

## Decision and falsifier

This exact derivation establishes a **material structural confound for interpretation**, not an empirical refutation of the reported 45% retrospective result. The pending checksum-verified frozen-data rerun in PR #69 must report boundary versus both discrete-feasibility-random and uniform-crossing-probability policies, with per-year recall and split-level paired differences. If these perform similarly, the strongest defensible output is a replication-grade technical report documenting the benchmark and its negative/positive findings, not algorithmic novelty.

**Reproduction status:** exact arithmetic independently checked on 21 November 2026. No access to the frozen SQLite corpus was used in deriving this note; empirical superiority and G0/G1 remain **ABSTAIN / OPEN**.
