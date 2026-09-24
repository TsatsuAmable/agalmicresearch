#!/usr/bin/env python3
"""Frozen Phase 1C boundary-preservation follow-up."""
from __future__ import annotations
import argparse, json, statistics
from collections import defaultdict
from pathlib import Path
import importlib.util

SEEDS=tuple(range(20261001,20261021))
BUDGETS=tuple(x/100 for x in range(5,101,5))
POLICIES=("random","disagreement","boundary_uncertainty","hybrid")
TARGET=0.95

def load_phase1b(path: Path):
    spec=importlib.util.spec_from_file_location("review_value_holdout",path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def min_budget(rows):
    for r in sorted(rows,key=lambda x:x["budget"]):
        if r["midpoint_crossing_recall"] is not None and r["midpoint_crossing_recall"]>=TARGET:
            return r["budget"]
    return 1.0

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--db",type=Path,required=True)
    ap.add_argument("--phase1b-script",type=Path,default=Path("research/expert_attention/review_value_holdout.py"))
    ap.add_argument("--out",type=Path,default=Path("research-output/expert-attention-boundary-preservation"))
    args=ap.parse_args()
    m=load_phase1b(args.phase1b_script)
    reviews=m.load_reviews(args.db)
    runs=[]
    year_diag=[]
    for seed in SEEDS:
        eps=m.make_episodes(reviews,seed)
        for policy in POLICIES:
            for budget in BUDGETS:
                row={"seed":seed,"policy":policy,"budget":budget}
                row.update(m.evaluate(eps,policy,budget))
                runs.append(row)
    rws={}
    for policy in POLICIES:
        vals=[]
        for seed in SEEDS:
            rows=[r for r in runs if r["seed"]==seed and r["policy"]==policy]
            vals.append(1-min_budget(rows))
        rws[policy]=vals
    boundary=rws["boundary_uncertainty"]; random=rws["random"]
    median_boundary=statistics.median(boundary)
    median_random=statistics.median(random)
    support=(median_boundary>=0.40 and sum(x>=0.30 for x in boundary)>=18 and (median_boundary-median_random)>=0.30)
    mean_curve=[]
    for policy in POLICIES:
        for budget in BUDGETS:
            vals=[r["midpoint_crossing_recall"] for r in runs if r["policy"]==policy and r["budget"]==budget]
            mean_curve.append({"policy":policy,"budget":budget,"mean_midpoint_crossing_recall":statistics.mean(vals)})
    median_budget=1-median_boundary
    # Descriptive per-year diagnostic at the median boundary budget, using first fresh seed.
    eps=m.make_episodes(reviews,SEEDS[0])
    for year in m.YEARS:
        y=[e for e in eps if e["year"]==year]
        row=m.evaluate(y,"boundary_uncertainty",median_budget)
        year_diag.append({"year":year,"budget":median_budget,**row})
    result={
        "schema_version":"1.0","status":"PHASE_1C_COMPLETE",
        "input_db_sha256":m.sha256_file(args.db),
        "fresh_seeds":list(SEEDS),"budgets":list(BUDGETS),"target_recall":TARGET,
        "rws95_by_policy":rws,
        "summary":{
            p:{
                "median_rws95":statistics.median(v),
                "min_rws95":min(v),"max_rws95":max(v),
                "splits_at_least_30pct_saved":sum(x>=0.30 for x in v)
            } for p,v in rws.items()
        },
        "primary_hypothesis_supported":support,
        "median_boundary_minus_random_rws95":median_boundary-median_random,
        "mean_recall_curve":mean_curve,
        "year_diagnostic_at_median_boundary_budget":year_diag,
        "decision_labels_used":False,"citation_outcomes_used":False,"chronological_claim":False
    }
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"result.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    (args.out/"all_runs.json").write_text(json.dumps(runs,indent=2,sort_keys=True)+"\n")
    lines=[
        "# Expert-Attention Phase 1C Result","",
        f"Primary hypothesis: **{'SUPPORTED' if support else 'NOT SUPPORTED'}**","",
        "| Policy | Median RWS@95 | Range | Splits saving >=30% |",
        "|---|---:|---:|---:|",
    ]
    for p in POLICIES:
        s=result["summary"][p]
        lines.append(f"| {p} | {s['median_rws95']:.1%} | {s['min_rws95']:.1%}–{s['max_rws95']:.1%} | {s['splits_at_least_30pct_saved']}/20 |")
    lines += ["",f"Boundary minus random median RWS@95: **{result['median_boundary_minus_random_rws95']:+.1%}**","",
              "Fresh split seeds were not used in Phase 1B. This remains a synthetic hold-out over final stored ratings, not a chronological or causal review experiment."]
    (args.out/"report.md").write_text("\n".join(lines)+"\n")
    print(json.dumps({"supported":support,"summary":result["summary"],"boundary_minus_random":result["median_boundary_minus_random_rws95"]},indent=2))
if __name__=="__main__": main()
