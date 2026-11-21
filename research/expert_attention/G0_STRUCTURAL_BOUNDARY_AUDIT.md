# Phase 1B/1C adversarial G0 audit: structural boundary advantage

**Status:** bounded mathematical falsifier, 21 November 2026. **Decision:** publish a replication-grade *technical report*, not a novel algorithm paper, unless further independent evidence supports broader claims.

## Frozen inputs inspected
- [Phase 1B protocol](../../docs/EXPERT_ATTENTION_PHASE1B_REVIEW_VALUE_PROTOCOL.md), [negative findings](../../docs/EXPERT_ATTENTION_PHASE1B_FINDINGS.md), [implementation](review_value_holdout.py).
- [Phase 1C protocol](../../docs/EXPERT_ATTENTION_PHASE1C_BOUNDARY_PROTOCOL.md), [positive findings](../../docs/EXPERT_ATTENTION_PHASE1C_FINDINGS.md), [implementation](boundary_preservation.py).
- The reported 7,531 ICLR 2017–2021 eligible papers, 20 Phase 1B sensitivity seeds, and 20 *different* Phase 1C seeds are **repository-reported**, not independently recomputed here. The frozen SQLite input was not independently read in this audit. Its reported SHA-256 is `ceeaa4316f76f6a22a5856128f34e8c3f35693d145db756f9688eda42ee20ed2`.

## Structural falsifier: the event is mathematically confined near the boundary
Let the observed normalized pair mean be `m=(r1+r2)/2`, hidden rating `x∈[0,1]`, and three-review mean `m3=(2m+x)/3`. The code defines crossing as `(m<0.5<=m3) or (m3<0.5<=m)`.

For a crossing **from below**, `m<0.5` and `x>=1.5-2m`. Since `x<=1`, necessarily `m>=0.25`.

For a crossing **from above**, `m>=0.5` and `x<1.5-2m`. Since `x>=0`, necessarily `m<0.75`.

Thus **every possible crossing is confined to `0.25<=m<0.75`**, regardless of hidden-review distribution, year, or any predictive relationship. In particular, a policy prioritizing `|m-0.5|` has a built-in geometric advantage on the *same mathematical event it is scored against*. This is not label leakage: it is **target–feature structural alignment**, and its importance must be disclosed.

The Phase 1C ~45% median simulated work saving is not thereby false. Its interpretation changes: it may quantify how concentrated feasible crossings are near the boundary in this particular rating distribution, rather than discovering a generalizable information-value predictor.

## Required ablations before causal/predictive claims
1. **Feasibility-only baseline:** select all episodes with `0.25<=m<0.75` (and, if needed, rank within this band). Report the exact workload fraction and recall. This is a deterministic *guaranteed-100%-crossing-preservation* rule for the defined synthetic event, with no hidden-score learning.
2. **Within-feasible-band random baseline:** randomly select among episodes in the feasible band, year-stratified, at matched review budgets. Compare the boundary rule's *incremental* recall over this stronger baseline.
3. **Tie and equality sensitivity:** test the asymmetric equality convention `m<0.5<=m3` vs `m3<0.5<=m`; report counts exactly at 0.5 and sensitivity to treating equality as neither side.
4. **Per-year floor:** show per-year 95% recall thresholds, not just pooled 95%; Phase 1C already documents 2020/2021 below 95% at the pooled median budget.
5. **Split dependence:** 20 deterministic partitions reuse the same underlying papers and ratings; they are not 20 independent venue replications. Do not derive population confidence intervals from seed variability alone.

## Prior-art positioning (provisional, not a completed literature search)
The routing score is an elementary **uncertainty / margin sampling** rule, a well-established family in active learning. Review triage, selective prediction and human-in-the-loop escalation are adjacent mature families. The contribution should be positioned as a **specific reproducible benchmark and objective-dependent negative/positive comparison**, not an invented algorithm. A complete sourced prior-art matrix remains required for final G0 signoff.

## Gate disposition
**G0 provisional: technical-report route selected; not yet PASS** pending source/licensing check and prior-art citations. **G1–G5 not claimed.** Capability Transfer remains paused and intact. This audit introduces no new study, lane or dataset and changes no frozen protocol or outcome.

## One-command mathematical verifier
```python
python3 - <<'PY'
from itertools import product
grid=[i/100 for i in range(101)]
for m,x in product(grid,grid):
    m3=(2*m+x)/3
    crossing=(m<.5<=m3) or (m3<.5<=m)
    assert not crossing or (.25<=m<.75), (m,x)
print("PASS: all 10,201 grid combinations respect the feasible crossing band")
PY
```

**Next:** implement the feasibility-only and feasible-band random baselines in the existing deterministic pipeline; rerun against the frozen SHA-checked SQLite file and report the incremental value beyond mathematical feasibility. If incremental value vanishes, retain Phase 1B's negative result and publish the Phase 1C result as a descriptive structural benchmark rather than a predictive triumph.
