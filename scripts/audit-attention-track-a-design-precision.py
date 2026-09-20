#!/usr/bin/env python3
"""Prospective precision audit for preregistered Track A policy contrasts.

This audit uses only frozen policy selections, cohort size, the preregistered
top-decile outcome fraction, and the smallest effect of interest. It does not
read or simulate realized citation values.

Under a design-null in which exactly H high-recognition labels are uniformly
distributed across N frozen candidates, the recall-difference variance between
two equal-budget fixed selections depends only on their symmetric difference.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

PRIMARY_BUDGET = "0.20"
HIGH_FRACTION = 0.10
SMALLEST_EFFECT = 0.05
Z_95 = 1.959963984540054
BASELINE = "seeded_random"
STRUCTURED = (
    "centrality",
    "centroid_novelty",
    "local_sparsity",
    "kcenter_coverage",
    "exploration_quota",
)


def null_recall_delta_se(
    n: int,
    h: int,
    symmetric_difference: int,
) -> float:
    """Exact SD under a fixed-H uniformly random high-label set.

    Each candidate in policy-only contributes +1/H; each candidate in
    baseline-only contributes -1/H. Equal budgets imply the finite-population
    weights sum to zero.
    """
    if not (0 < h < n):
        raise ValueError((n, h))
    if symmetric_difference < 0 or symmetric_difference > n:
        raise ValueError(symmetric_difference)
    variance = (
        symmetric_difference
        * (n - h)
        / (h * n * (n - 1))
    )
    return math.sqrt(max(0.0, variance))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy-selections", type=Path, required=True)
    parser.add_argument("--policy-manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    selections: dict[str, Any] = json.loads(
        args.policy_selections.read_text()
    )
    manifest = json.loads(args.policy_manifest.read_text())

    status = str(manifest.get("status"))
    if status not in {
        "FROZEN_T0_POLICY_SELECTIONS",
        "ENGINEERING_FIXTURE_ONLY",
    }:
        raise RuntimeError(f"unexpected policy manifest status: {status}")

    n = int(manifest["N"])
    if n < 10:
        raise RuntimeError(f"cohort too small for precision audit: {n}")
    h = max(1, math.ceil(HIGH_FRACTION * n))

    if PRIMARY_BUDGET not in selections:
        raise RuntimeError(f"missing primary budget {PRIMARY_BUDGET}")
    primary = selections[PRIMARY_BUDGET]
    if BASELINE not in primary:
        raise RuntimeError("seeded random baseline missing")

    baseline = set(primary[BASELINE]["selected_forum_ids"])
    k = int(primary[BASELINE]["k"])
    if len(baseline) != k:
        raise RuntimeError("baseline unique selection count != k")

    comparisons: dict[str, Any] = {}
    adequate_count = 0

    for policy in STRUCTURED:
        if policy not in primary:
            raise RuntimeError(f"missing structured policy: {policy}")
        selected = set(primary[policy]["selected_forum_ids"])
        if len(selected) != k:
            raise RuntimeError(f"{policy} unique selection count != k")

        overlap = len(selected & baseline)
        symmetric_difference = len(selected ^ baseline)
        se = null_recall_delta_se(n, h, symmetric_difference)
        half_width = Z_95 * se
        adequate = half_width <= SMALLEST_EFFECT
        adequate_count += int(adequate)

        comparisons[policy] = {
            "N": n,
            "H_design_top_decile": h,
            "k_primary_budget": k,
            "overlap_with_seeded_random": overlap,
            "symmetric_difference": symmetric_difference,
            "null_recall_delta_se": se,
            "normal_approx_ci95_half_width": half_width,
            "smallest_effect_of_interest": SMALLEST_EFFECT,
            "prospective_precision_adequate_for_5pp": adequate,
        }

    if adequate_count == len(STRUCTURED):
        precision_status = "DESIGN_PRECISION_ADEQUATE"
    elif adequate_count == 0:
        precision_status = "DESIGN_PRECISION_INADEQUATE"
    else:
        precision_status = "DESIGN_PRECISION_MIXED"

    payload = {
        "schema_version": "0.1",
        "status": precision_status,
        "policy_manifest_status": status,
        "primary_budget": PRIMARY_BUDGET,
        "high_recognition_design_fraction": HIGH_FRACTION,
        "high_recognition_design_count": h,
        "smallest_effect_of_interest": SMALLEST_EFFECT,
        "design_null": (
            "exactly H high-recognition labels uniformly distributed over "
            "the frozen cohort; policy selections held fixed"
        ),
        "comparisons_vs_seeded_random": comparisons,
        "adequate_comparison_count": adequate_count,
        "comparison_count": len(STRUCTURED),
        "interpretation": (
            "This is a pre-outcome design diagnostic, not a realized power "
            "calculation. Realized top-decile ties and paired bootstrap "
            "covariance may change final interval width."
        ),
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
