# Phase 1C: uniform legal-score probability is not an independent ranking baseline

**Status:** exact, post-hoc mathematical falsification; no frozen ICLR data used. This corrects the interpretation of the proposed `uniform_probability` comparator in PR #69.

For a year with `n` equally spaced normalized legal ratings `c=k/(n-1)`, the frozen crossing event is `(m<1/2<= (2m+c)/3) or ((2m+c)/3<1/2<=m)`, where `m=(a+b)/2`. Exhaustive rational enumeration gives the number of legal third ratings that cause a crossing for each possible `m`:

- **Four levels (2020):** at means `0,1/6,1/3,1/2,2/3,5/6,1`, crossing counts are `0,0,1,2,1,0,0`.
- **Ten levels (other years):** at means `j/18` for `j=0,...,18`, crossing counts are `0,0,0,0,0,1,2,3,4,5,4,3,2,1,0,0,0,0,0`.

**Exact conclusion:** within either rating regime, crossing probability under a hypothetical uniform legal third score is a non-increasing function of `|m-1/2|`. Therefore sorting by `uniform_crossing_probability` and by frozen `boundary_uncertainty` produces **the same ordered score groups**. Their only differences are *within-group tie breaking*, not a competing allocation signal. This comparator cannot establish incremental predictive value of boundary proximity. In the current verifier the uniform-probability policy uses a seeded hash tie-breaker while boundary uses paper IDs, so any observed difference between them would be a **tie-order artifact**.

The same warning applies to interpreting score-level feasibility as a fully independent predictor. Feasibility-conditioned random allocation remains a meaningful but weaker structural null because it randomizes *within* the feasible group. A genuinely distinct comparator requires a policy based on observed-score information not deterministically monotone in midpoint distance, for example a training-only estimated conditional crossing rate with leakage-safe evaluation, or a prespecified operational heuristic. Such models need their own validity audit.

## Independent verification (standard-library Python)

```python
from fractions import Fraction as Q
for n in (4, 10):
    means = [Q(j, 2*(n-1)) for j in range(2*n-1)]
    counts = [sum((m < Q(1,2) <= (2*m+Q(k,n-1))/3)
                  or ((2*m+Q(k,n-1))/3 < Q(1,2) <= m)
                  for k in range(n)) for m in means]
    assert all(counts[i] >= counts[i-1] for i in range(1,n))
    assert counts == counts[::-1]
    print(n, counts)
```

**Falsification consequence:** retain the `uniform_probability` policy as a **tie sensitivity control**, not an independent stronger baseline. Report its paired difference as a tie-order effect. Do not claim it beats, validates or refutes boundary ranking independently. The frozen-data comparison with feasibility-conditioned random remains pending. The reported retrospective 45% simulated saving is not independently reproduced or altered by this mathematical result.
