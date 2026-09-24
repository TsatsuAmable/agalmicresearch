#!/usr/bin/env python3
"""Frozen Phase 1B marginal-review-value benchmark.

Synthetic hold-out over real ICLR review scores. No conference decisions,
paper text, review text, author identity, or citation outcomes are used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sqlite3
import statistics
from collections import defaultdict
from pathlib import Path

YEARS = (2017, 2018, 2019, 2020, 2021)
BUDGETS = (0.05, 0.10, 0.20, 0.40)
PRIMARY_SEED = 20260924
SENSITIVITY_SEEDS = tuple(range(20260924, 20260944))
SCALES = {
    2017: (1,2,3,4,5,6,7,8,9,10),
    2018: (1,2,3,4,5,6,7,8,9,10),
    2019: (1,2,3,4,5,6,7,8,9,10),
    2020: (1,3,6,8),
    2021: (1,2,3,4,5,6,7,8,9,10),
}

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def hash_key(*parts: object) -> str:
    return hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()

def norm_rating(year: int, value: object) -> float:
    score = int(float(str(value)))
    scale = SCALES[year]
    if score not in scale:
        raise ValueError(f"rating {score} not in frozen {year} scale {scale}")
    return scale.index(score) / (len(scale) - 1)

def load_reviews(db: Path) -> dict[tuple[int,str], list[tuple[str,float]]]:
    con = sqlite3.connect(db)
    rows = con.execute(
        """select cast(s.conf_year as integer), s.id, r.id, r.rating_int
           from submissions s join reviews r on r.forum=s.id
           where s.conf_name='ICLR'
             and cast(s.conf_year as integer) between 2017 and 2021
             and r.rating_int is not null and trim(r.rating_int)<>''"""
    )
    out: dict[tuple[int,str], list[tuple[str,float]]] = defaultdict(list)
    for year, paper_id, review_id, rating in rows:
        out[(year, paper_id)].append((str(review_id), norm_rating(year, rating)))
    return {k:v for k,v in out.items() if len(v) >= 3}

def make_episodes(reviews, seed: int):
    episodes = []
    for (year, paper_id), rs in sorted(reviews.items()):
        ordered = sorted(rs, key=lambda x: (hash_key(seed, paper_id, x[0]), x[0]))
        (id1,r1),(id2,r2),(id3,r3) = ordered[:3]
        mean2 = (r1+r2)/2
        mean3 = (r1+r2+r3)/3
        disagreement = abs(r1-r2)
        boundary = max(0.0, 1.0 - 2.0*abs(mean2-0.5))
        episodes.append({
            "year":year, "paper_id":paper_id,
            "mean2":mean2, "disagreement":disagreement,
            "boundary_uncertainty":boundary,
            "hybrid":0.5*(disagreement+boundary),
            "absolute_update":abs(mean3-mean2),
            "midpoint_crossing":(mean2 < 0.5 <= mean3) or (mean3 < 0.5 <= mean2),
            "random_score":int(hash_key("route",seed,paper_id),16),
        })
    return episodes

def select_within_year(episodes, policy: str, budget: float) -> set[str]:
    chosen=set()
    by=defaultdict(list)
    for e in episodes: by[e["year"]].append(e)
    for year, rows in by.items():
        k=max(1, round(len(rows)*budget))
        if policy=="random":
            ranked=sorted(rows,key=lambda e:(e["random_score"],e["paper_id"]),reverse=True)
        else:
            ranked=sorted(rows,key=lambda e:(e[policy],e["paper_id"]),reverse=True)
        chosen.update(e["paper_id"] for e in ranked[:k])
    return chosen

def percentile_threshold(vals, q: float) -> float:
    vals=sorted(vals)
    return vals[max(0,min(len(vals)-1, math.ceil(q*len(vals))-1))]

def evaluate(episodes, policy: str, budget: float):
    chosen=select_within_year(episodes,policy,budget)
    total_gain=sum(e["absolute_update"] for e in episodes)
    captured=sum(e["absolute_update"] for e in episodes if e["paper_id"] in chosen)
    large=set()
    by=defaultdict(list)
    for e in episodes: by[e["year"]].append(e)
    for rows in by.values():
        t=percentile_threshold([e["absolute_update"] for e in rows],0.90)
        large.update(e["paper_id"] for e in rows if e["absolute_update"]>=t)
    crossings={e["paper_id"] for e in episodes if e["midpoint_crossing"]}
    return {
        "selected":len(chosen),
        "eligible":len(episodes),
        "update_mass_capture":captured/total_gain if total_gain else None,
        "large_update_recall":len(chosen & large)/len(large) if large else None,
        "midpoint_crossing_recall":len(chosen & crossings)/len(crossings) if crossings else None,
        "midpoint_crossings":len(crossings),
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--db",type=Path,required=True)
    ap.add_argument("--out",type=Path,default=Path("research-output/expert-attention-review-value"))
    args=ap.parse_args()
    reviews=load_reviews(args.db)
    counts={str(y):sum(1 for (yr,_),rs in reviews.items() if yr==y) for y in YEARS}
    policies=("random","disagreement","boundary_uncertainty","hybrid")
    all_runs=[]
    for seed in SENSITIVITY_SEEDS:
        episodes=make_episodes(reviews,seed)
        for policy in policies:
            for budget in BUDGETS:
                row={"seed":seed,"policy":policy,"budget":budget}
                row.update(evaluate(episodes,policy,budget))
                all_runs.append(row)
    primary=[r for r in all_runs if r["seed"]==PRIMARY_SEED]
    def at(seed,policy,budget):
        return next(r for r in all_runs if r["seed"]==seed and r["policy"]==policy and r["budget"]==budget)
    advantages=[]
    for seed in SENSITIVITY_SEEDS:
        d=at(seed,"disagreement",0.20)["update_mass_capture"]
        rnd=at(seed,"random",0.20)["update_mass_capture"]
        advantages.append(d-rnd)
    primary_adv=at(PRIMARY_SEED,"disagreement",0.20)["update_mass_capture"]-at(PRIMARY_SEED,"random",0.20)["update_mass_capture"]
    primary_lu_adv=at(PRIMARY_SEED,"disagreement",0.20)["large_update_recall"]-at(PRIMARY_SEED,"random",0.20)["large_update_recall"]
    h1=(primary_adv>=0.05 and statistics.median(advantages)>=0.05 and sum(x>0 for x in advantages)>=18)
    h2=primary_lu_adv>=0.05
    summary={
        "schema_version":"1.0",
        "status":"PHASE_1B_COMPLETE",
        "input":{"db":str(args.db),"sha256":sha256_file(args.db)},
        "design":{
            "years":list(YEARS),"budgets":list(BUDGETS),
            "primary_seed":PRIMARY_SEED,"sensitivity_seeds":list(SENSITIVITY_SEEDS),
            "policies":list(policies),
            "decision_labels_used":False,"citation_outcomes_used":False,
            "chronological_claim":False,
        },
        "eligible_papers_by_year":counts,
        "eligible_total":sum(counts.values()),
        "primary_results":primary,
        "hypotheses":{
            "H1":{
                "supported":h1,
                "primary_update_mass_advantage":primary_adv,
                "median_sensitivity_advantage":statistics.median(advantages),
                "positive_sensitivity_splits":sum(x>0 for x in advantages),
                "total_sensitivity_splits":len(advantages),
            },
            "H2":{
                "supported":h2,
                "primary_large_update_recall_advantage":primary_lu_adv,
            }
        },
        "sensitivity_disagreement_minus_random_20pct":advantages,
    }
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"result.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    (args.out/"all_runs.json").write_text(json.dumps(all_runs,indent=2,sort_keys=True)+"\n")
    focus=[r for r in primary if math.isclose(r["budget"],0.20)]
    lines=[
        "# Expert-Attention Phase 1B Result","",
        f"Eligible papers: **{summary['eligible_total']:,}**","",
        "## Primary 20% budget","",
        "| Policy | Update-mass capture | Large-update recall | Midpoint-crossing recall |",
        "|---|---:|---:|---:|",
    ]
    for r in focus:
        lines.append(f"| {r['policy']} | {r['update_mass_capture']:.1%} | {r['large_update_recall']:.1%} | {r['midpoint_crossing_recall']:.1%} |")
    lines += [
        "",
        "## Preregistered adjudication","",
        f"- H1 disagreement predicts marginal review value: **{'SUPPORTED' if h1 else 'NOT SUPPORTED'}**",
        f"- Primary disagreement minus random UMC: **{primary_adv:+.1%}**",
        f"- Median split-sensitivity advantage: **{statistics.median(advantages):+.1%}**",
        f"- Positive sensitivity splits: **{sum(x>0 for x in advantages)}/{len(advantages)}**",
        f"- H2 disagreement preserves large updates: **{'SUPPORTED' if h2 else 'NOT SUPPORTED'}**",
        f"- Primary large-update recall advantage: **{primary_lu_adv:+.1%}**","",
        "This is a synthetic hold-out benchmark over final stored reviewer ratings. It does not reconstruct review chronology and does not use conference decisions or citations.",
    ]
    (args.out/"report.md").write_text("\n".join(lines)+"\n")
    print(json.dumps(summary["hypotheses"],indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
