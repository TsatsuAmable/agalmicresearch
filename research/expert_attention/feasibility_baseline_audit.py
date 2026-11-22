#!/usr/bin/env python3
"""Phase 1C post-hoc structural-baseline falsification. Not preregistered.
Reuses frozen episodes and seeds. Never uses held-out rating to rank.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, statistics
from collections import defaultdict
from pathlib import Path

SEEDS=range(20261001,20261021)
BUDGETS=[i/100 for i in range(5,101,5)]
TARGET=.95

def load(path):
    spec=importlib.util.spec_from_file_location("frozen_review_value",path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def feasible(mean2):
    # For r3 in [0,1], midpoint crossing is possible iff 0.25 <= mean2 < 0.75.
    return .25 <= mean2 < .75

def discrete_feasible(year, mean2):
    """Can ANY legal third rating in the frozen year scale cause a crossing?

    Uses the year rating scale, never the held-out third rating.
    """
    n=len((1,3,6,8)) if year==2020 else 10
    for i in range(n):
        r3=i/(n-1)
        mean3=(2*mean2+r3)/3
        if (mean2 < .5 <= mean3) or (mean3 < .5 <= mean2):
            return True
    return False

def uniform_crossing_probability(year, mean2):
    """Exact crossing probability if the third score is uniform over legal levels.

    This is a transparent MODEL baseline, not a fitted or empirically calibrated
    probability. Uses only the two visible scores and frozen year scale.
    """
    n=4 if year==2020 else 10
    hits=0
    for i in range(n):
        r3=i/(n-1)
        mean3=(2*mean2+r3)/3
        hits+=int((mean2 < .5 <= mean3) or (mean3 < .5 <= mean2))
    return hits/n

def tie(seed, paper_id):
    return int(hashlib.sha256(f"feasible|{seed}|{paper_id}".encode()).hexdigest(),16)

def rank(episodes, seed, policy):
    groups=defaultdict(list)
    for e in episodes:
        groups[e["year"]].append(e)
    out={}
    for year, rows in groups.items():
        if policy=="feasible_random":
            key=lambda e:(int(feasible(e["mean2"])),tie(seed,e["paper_id"]),e["paper_id"])
        elif policy=="discrete_feasible_random":
            key=lambda e:(int(discrete_feasible(e["year"],e["mean2"])),tie(seed,e["paper_id"]),e["paper_id"])
        elif policy=="uniform_probability":
            key=lambda e:(uniform_crossing_probability(e["year"],e["mean2"]),tie(seed,e["paper_id"]),e["paper_id"])
        elif policy=="boundary":
            key=lambda e:(e["boundary_uncertainty"],e["paper_id"])
        elif policy=="random":
            key=lambda e:(e["random_score"],e["paper_id"])
        else:
            raise ValueError(policy)
        out[year]=sorted(rows,key=key,reverse=True)
    return out

def evaluate(ranked,budget):
    chosen=set()
    for year,rows in ranked.items():
        k=max(1,round(len(rows)*budget))
        chosen.update((year,e["paper_id"]) for e in rows[:k])
    crossings=[e for rows in ranked.values() for e in rows if e["midpoint_crossing"]]
    if not crossings: return None
    return sum((e["year"],e["paper_id"]) in chosen for e in crossings)/len(crossings)

def allocation_diagnostics(ranked, budget):
    """Report actual selected reviews and crossing events by year at nominal budget."""
    by_year = {}
    for year, rows in sorted(ranked.items()):
        selected = max(1, round(len(rows) * budget))
        events = sum(bool(e["midpoint_crossing"]) for e in rows)
        captured = sum(bool(e["midpoint_crossing"]) for e in rows[:selected])
        by_year[str(year)] = {"eligible": len(rows), "selected": selected,
            "crossings": events, "crossings_selected": captured,
            "recall": captured / events if events else None}
    eligible = sum(v["eligible"] for v in by_year.values())
    selected = sum(v["selected"] for v in by_year.values())
    return {"nominal_budget": budget, "eligible": eligible, "selected": selected,
        "actual_fraction_selected": selected / eligible if eligible else None,
        "actual_fraction_saved": 1 - selected / eligible if eligible else None,
        "by_year": by_year}

def min_budget(ranked):
    for budget in BUDGETS:
        recall=evaluate(ranked,budget)
        if recall is not None and recall>=TARGET:
            return budget
    return None

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--db",type=Path,required=True)
    p.add_argument("--phase1b-script",type=Path,default=Path("research/expert_attention/review_value_holdout.py"))
    p.add_argument("--out",type=Path,default=Path("research-output/expert-attention-feasibility-baselines"))
    a=p.parse_args()
    m=load(a.phase1b_script)
    expected="ceeaa4316f76f6a22a5856128f34e8c3f35693d145db756f9688eda42ee20ed2"
    actual=m.sha256_file(a.db)
    if actual != expected:
        raise SystemExit(f"Frozen input checksum mismatch: {actual} != {expected}")
    reviews=m.load_reviews(a.db)
    runs=[]
    for seed in SEEDS:
        eps=m.make_episodes(reviews,seed)
        for e in eps:
            if e["midpoint_crossing"] and not feasible(e["mean2"]):
                raise AssertionError("Crossing outside mathematically feasible band")
            if e["midpoint_crossing"] and not discrete_feasible(e["year"],e["mean2"]):
                raise AssertionError("Crossing impossible on frozen year rating scale")
        # Independent parity check against the frozen Phase 1C implementation.
        # A mismatch is a methodological failure, not a new result.
        for original_policy, local_policy in (("random","random"),("boundary_uncertainty","boundary")):
            ranked_original=rank(eps,seed,local_policy)
            for b in BUDGETS:
                old_recall=m.evaluate(eps,original_policy,b)["midpoint_crossing_recall"]
                new_recall=evaluate(ranked_original,b)
                if old_recall is None or new_recall is None:
                    if old_recall != new_recall:
                        raise AssertionError(f"Recall parity failure: {seed} {original_policy} {b}")
                elif abs(old_recall-new_recall)>1e-12:
                    raise AssertionError(f"Recall parity failure: {seed} {original_policy} {b}: {old_recall} != {new_recall}")
        for policy in ("random","feasible_random","discrete_feasible_random","uniform_probability","boundary"):
            ranked=rank(eps,seed,policy)
            budget=min_budget(ranked)
            runs.append(dict(seed=seed,policy=policy,min_budget=budget,
                rws95=None if budget is None else 1-budget,
                crossing_count=sum(e["midpoint_crossing"] for e in eps),
                feasible_count=sum(feasible(e["mean2"]) for e in eps),
                discrete_feasible_count=sum(discrete_feasible(e["year"],e["mean2"]) for e in eps),
                eligible_count=len(eps),
                recall_at_55pct=evaluate(ranked,.55),
                allocation_at_min_budget=allocation_diagnostics(ranked,budget) if budget is not None else None,
                per_year_recall_at_55pct={
                    str(y):evaluate({y:rows},.55) for y,rows in ranked.items()}))
    summary={}
    for policy in ("random","feasible_random","discrete_feasible_random","uniform_probability","boundary"):
        vals=[r["rws95"] for r in runs if r["policy"]==policy and r["rws95"] is not None]
        summary[policy]={"median_rws95":statistics.median(vals) if vals else None,
            "min_rws95":min(vals) if vals else None,"max_rws95":max(vals) if vals else None,
            "n_splits":len(vals)}
    result={"status":"POST_HOC_STRUCTURAL_BASELINE","input_sha256":m.sha256_file(a.db),
        "seeds":list(SEEDS),"budget_grid":BUDGETS,"target_pooled_recall":TARGET,
        "summary":summary,"runs":runs,
        "interpretation":"Retrospective synthetic hold-out; not prospective review savings; split repeats are not independent cohorts.",
        "falsifier":"If boundary does not beat feasibility-conditioned random (continuous or discrete-year-scale) materially, the advantage over unrestricted random is largely explained by mathematical event feasibility.",
        "uniform_probability_assumption":"Counterfactual third score equally likely at each legal year-scale level; NOT an empirical posterior or observed distribution.",
        "no_decision_or_citation_labels":True}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/"result.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(summary,indent=2,sort_keys=True))
if __name__=="__main__":
    main()
