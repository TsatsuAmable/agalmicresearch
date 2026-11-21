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
    reviews=m.load_reviews(a.db)
    runs=[]
    for seed in SEEDS:
        eps=m.make_episodes(reviews,seed)
        for e in eps:
            if e["midpoint_crossing"] and not feasible(e["mean2"]):
                raise AssertionError("Crossing outside mathematically feasible band")
        for policy in ("random","feasible_random","boundary"):
            ranked=rank(eps,seed,policy)
            budget=min_budget(ranked)
            runs.append(dict(seed=seed,policy=policy,min_budget=budget,
                rws95=None if budget is None else 1-budget,
                crossing_count=sum(e["midpoint_crossing"] for e in eps),
                feasible_count=sum(feasible(e["mean2"]) for e in eps),
                eligible_count=len(eps),
                recall_at_55pct=evaluate(ranked,.55),
                per_year_recall_at_55pct={
                    str(y):evaluate({y:rows},.55) for y,rows in ranked.items()}))
    summary={}
    for policy in ("random","feasible_random","boundary"):
        vals=[r["rws95"] for r in runs if r["policy"]==policy and r["rws95"] is not None]
        summary[policy]={"median_rws95":statistics.median(vals) if vals else None,
            "min_rws95":min(vals) if vals else None,"max_rws95":max(vals) if vals else None,
            "n_splits":len(vals)}
    result={"status":"POST_HOC_STRUCTURAL_BASELINE","input_sha256":m.sha256_file(a.db),
        "seeds":list(SEEDS),"budget_grid":BUDGETS,"target_pooled_recall":TARGET,
        "summary":summary,"runs":runs,
        "interpretation":"Retrospective synthetic hold-out; not prospective review savings; split repeats are not independent cohorts.",
        "falsifier":"If boundary does not beat feasible_random materially, the advantage over unrestricted random is largely explained by mathematical event feasibility.",
        "no_decision_or_citation_labels":True}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/"result.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(summary,indent=2,sort_keys=True))
if __name__=="__main__":
    main()
