#!/usr/bin/env python3
"""Independent count-based audit of simulated midpoint-crossing preservation.

Input JSON: {"regimes": [{"name":"2017","crossings":100,"captured":98}, ...]}
Counts must be event counts from ONE holdout split and ONE fixed allocation budget.
No claims of independent evidence across reused-paper splits.
"""
import argparse
import json
import math
from statistics import NormalDist

def wilson(k, n, confidence=0.95):
    if not (type(k) is int and type(n) is int and 0 <= k <= n and n > 0):
        raise ValueError("require integer 0 <= captured <= crossings, crossings > 0")
    if not (0 < confidence < 1):
        raise ValueError("confidence must be between 0 and 1")
    z = NormalDist().inv_cdf((1 + confidence) / 2)
    p = k / n
    d = 1 + z*z/n
    center = (p + z*z/(2*n)) / d
    half = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return [center-half, center+half]

def audit(payload, floor=0.95):
    if not isinstance(floor, (int, float)) or isinstance(floor, bool) or not math.isfinite(floor) or not 0 <= floor <= 1:
        raise ValueError("floor must be finite and between 0 and 1")
    regimes = payload["regimes"]
    if not isinstance(regimes, list) or not regimes:
        raise ValueError("nonempty regimes required")
    seen = set()
    rows = []
    for r in regimes:
        name = r["name"]
        if not isinstance(name, str) or not name or name in seen:
            raise ValueError("regime names must be distinct nonempty strings")
        seen.add(name)
        k, n = r["captured"], r["crossings"]
        lo, hi = wilson(k, n)
        rows.append({"name":name, "captured":k, "crossings":n,
                     "recall":k/n, "wilson95": [lo, hi],
                     "point_floor_pass": k/n >= floor,
                     "lower_bound_floor_pass": lo >= floor})
    k = sum(r["captured"] for r in rows)
    n = sum(r["crossings"] for r in rows)
    return {"pooled": {"captured":k, "crossings":n, "recall":k/n,
                       "wilson95": wilson(k, n)},
            "regimes": rows,
            "all_regimes_point_floor_pass": all(r["point_floor_pass"] for r in rows),
            "all_regimes_lower_bound_floor_pass": all(r["lower_bound_floor_pass"] for r in rows),
            "caveat": "Wilson intervals assume independent Bernoulli events; papers, reviewers and splits may be dependent. These are diagnostics, not validated coverage guarantees."}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("input", help="JSON event counts from one fixed-budget holdout")
    p.add_argument("--floor", type=float, default=0.95)
    args = p.parse_args()
    if not math.isfinite(args.floor) or not 0 <= args.floor <= 1:
        p.error("floor must be finite and between 0 and 1")
    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)
    print(json.dumps(audit(data, args.floor), indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
