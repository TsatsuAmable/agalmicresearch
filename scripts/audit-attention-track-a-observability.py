#!/usr/bin/env python3
"""Audit downstream identity observability on the frozen T0 policy substrate.

This stage reads only identity-match availability, historical decision labels
for diagnostics, and outcome-blind representation/policy artefacts. It does
not read citation outcomes.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

Z95 = 1.959963984540054
MARGIN = 0.05
HIGH_FRACTION = 0.10
PRIMARY_BUDGET = "0.20"
BASELINE = "seeded_random"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text().splitlines()
        if line.strip()
    ]


def wilson_interval(successes: int, total: int) -> tuple[float, float] | None:
    if total <= 0:
        return None
    p = successes / total
    z2 = Z95 * Z95
    denom = 1.0 + z2 / total
    center = (p + z2 / (2.0 * total)) / denom
    radius = (
        Z95
        * math.sqrt(
            (p * (1.0 - p) / total)
            + (z2 / (4.0 * total * total))
        )
        / denom
    )
    return max(0.0, center - radius), min(1.0, center + radius)


def newcombe_difference_interval(
    success_a: int,
    total_a: int,
    success_b: int,
    total_b: int,
) -> tuple[float, float] | None:
    if total_a <= 0 or total_b <= 0:
        return None
    ia = wilson_interval(success_a, total_a)
    ib = wilson_interval(success_b, total_b)
    if ia is None or ib is None:
        return None
    pa = success_a / total_a
    pb = success_b / total_b
    diff = pa - pb
    lower = diff - math.sqrt(
        (pa - ia[0]) ** 2 + (ib[1] - pb) ** 2
    )
    upper = diff + math.sqrt(
        (ia[1] - pa) ** 2 + (pb - ib[0]) ** 2
    )
    return max(-1.0, lower), min(1.0, upper)


def summarize_match(ids: list[str], matched: set[str]) -> dict[str, Any]:
    total = len(ids)
    hit = sum(candidate_id in matched for candidate_id in ids)
    ci = wilson_interval(hit, total)
    return {
        "candidate_count": total,
        "matched_count": hit,
        "matched_fraction": hit / total if total else None,
        "matched_wilson_ci95": list(ci) if ci else None,
    }


def matched_substrate_null_precision(
    n: int,
    selected_policy: set[str],
    selected_baseline: set[str],
    matched: set[str],
) -> dict[str, Any]:
    if n <= 1:
        raise ValueError("matched substrate too small")
    a = selected_policy & matched
    b = selected_baseline & matched
    a_only = len(a - b)
    b_only = len(b - a)
    rest = n - a_only - b_only
    if rest < 0:
        raise RuntimeError("selection sets exceed matched substrate")

    h = max(1, math.ceil(HIGH_FRACTION * n))
    sum_w = len(a) - len(b)
    mean_w = sum_w / n
    centered_ss = (
        a_only * (1.0 - mean_w) ** 2
        + b_only * (-1.0 - mean_w) ** 2
        + rest * (0.0 - mean_w) ** 2
    )
    variance = (
        (n - h)
        / (h * n * (n - 1))
        * centered_ss
    )
    se = math.sqrt(max(0.0, variance))
    half_width = Z95 * se
    expected_null_delta = sum_w / n

    return {
        "matched_substrate_N": n,
        "design_top_decile_H": h,
        "policy_matched_selected_count": len(a),
        "baseline_matched_selected_count": len(b),
        "policy_vs_baseline_matched_selected_difference": sum_w,
        "expected_null_recall_delta_due_to_observability": expected_null_delta,
        "normal_approx_ci95_half_width": half_width,
        "precision_adequate_for_5pp": half_width <= MARGIN,
        "observability_bias_inside_5pp": abs(expected_null_delta) <= MARGIN,
        "a_only_count": a_only,
        "b_only_count": b_only,
    }


def geometry_quintiles(
    representation: Path,
    row_index: Path,
    cohort_ids: set[str],
    matched: set[str],
) -> dict[str, Any]:
    import numpy as np

    data = np.load(representation)
    centroid = np.asarray(data["centroid_cosine_distance"], dtype=float)
    sparsity = np.asarray(data["knn5_mean_cosine_distance"], dtype=float)
    rows = load_jsonl(row_index)
    if len(rows) != len(centroid) or len(rows) != len(sparsity):
        raise RuntimeError("representation geometry length mismatch")

    forum_ids = [str(row["forum_id"]) for row in rows]
    if set(forum_ids) != cohort_ids:
        raise RuntimeError("row index does not match frozen cohort")

    def stratify(values) -> list[dict[str, Any]]:
        order = sorted(
            range(len(values)),
            key=lambda i: (float(values[i]), forum_ids[i]),
        )
        groups: list[dict[str, Any]] = []
        for q in range(5):
            lo = q * len(order) // 5
            hi = (q + 1) * len(order) // 5
            idx = order[lo:hi]
            ids = [forum_ids[i] for i in idx]
            summary = summarize_match(ids, matched)
            summary["quintile"] = q + 1
            summary["value_min"] = min(float(values[i]) for i in idx) if idx else None
            summary["value_max"] = max(float(values[i]) for i in idx) if idx else None
            groups.append(summary)
        return groups

    return {
        "centroid_cosine_distance_quintiles": stratify(centroid),
        "local_sparsity_quintiles": stratify(sparsity),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen-cohort", type=Path, required=True)
    parser.add_argument("--original-candidates", type=Path, required=True)
    parser.add_argument("--resolved-identities", type=Path, required=True)
    parser.add_argument("--policy-selections", type=Path, required=True)
    parser.add_argument("--policy-manifest", type=Path, required=True)
    parser.add_argument("--representation", type=Path)
    parser.add_argument("--row-index", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    cohort_rows = load_jsonl(args.frozen_cohort)
    cohort_ids = {str(row["forum_id"]) for row in cohort_rows}
    if len(cohort_ids) != len(cohort_rows):
        raise RuntimeError("duplicate forum IDs in frozen cohort")

    original = {
        str(row["forum_id"]): row
        for row in load_jsonl(args.original_candidates)
        if str(row["forum_id"]) in cohort_ids
    }
    if set(original) != cohort_ids:
        raise RuntimeError("original candidate labels do not cover frozen cohort")

    identities = {
        str(row["forum_id"]): row
        for row in load_jsonl(args.resolved_identities)
        if str(row["forum_id"]) in cohort_ids
    }
    if set(identities) != cohort_ids:
        raise RuntimeError("identity records do not cover frozen cohort")

    matched = {
        forum_id
        for forum_id, row in identities.items()
        if row.get("status") == "MATCHED_PRIMARY_IDENTITY_CLUSTER"
    }

    all_ids = sorted(cohort_ids)
    overall = summarize_match(all_ids, matched)
    by_decision = {}
    for decision in ("ACCEPT", "REJECT"):
        ids = sorted(
            forum_id
            for forum_id in cohort_ids
            if original[forum_id]["decision"] == decision
        )
        by_decision[decision] = summarize_match(ids, matched)

    a = by_decision["ACCEPT"]
    r = by_decision["REJECT"]
    decision_gap = (
        float(a["matched_fraction"]) - float(r["matched_fraction"])
        if a["matched_fraction"] is not None
        and r["matched_fraction"] is not None
        else None
    )
    decision_gap_ci = newcombe_difference_interval(
        int(a["matched_count"]),
        int(a["candidate_count"]),
        int(r["matched_count"]),
        int(r["candidate_count"]),
    )
    decision_equivalent = bool(
        decision_gap_ci
        and decision_gap_ci[0] >= -MARGIN
        and decision_gap_ci[1] <= MARGIN
    )

    policy_manifest = json.loads(args.policy_manifest.read_text())
    if policy_manifest.get("status") != "FROZEN_T0_POLICY_SELECTIONS":
        raise RuntimeError("policy manifest is not frozen T0 selections")
    if int(policy_manifest["N"]) != len(cohort_ids):
        raise RuntimeError("policy manifest N != frozen cohort size")

    selections = json.loads(args.policy_selections.read_text())
    policy_support: dict[str, Any] = {}
    for budget_key in sorted(selections, key=float):
        policy_support[budget_key] = {}
        for policy, selection in selections[budget_key].items():
            selected = {str(x) for x in selection["selected_forum_ids"]}
            if not selected <= cohort_ids:
                raise RuntimeError(
                    f"{budget_key}/{policy} selected IDs outside frozen cohort"
                )
            policy_support[budget_key][policy] = summarize_match(
                sorted(selected), matched
            )

    if PRIMARY_BUDGET not in selections:
        raise RuntimeError(f"primary budget {PRIMARY_BUDGET} missing")
    primary = selections[PRIMARY_BUDGET]
    if BASELINE not in primary:
        raise RuntimeError("seeded random baseline missing")

    baseline_selected = {
        str(x) for x in primary[BASELINE]["selected_forum_ids"]
    }
    primary_contrasts: dict[str, Any] = {}
    for policy, selection in primary.items():
        if policy == BASELINE:
            continue
        selected = {str(x) for x in selection["selected_forum_ids"]}
        primary_contrasts[policy] = matched_substrate_null_precision(
            len(matched),
            selected,
            baseline_selected,
            matched,
        )

    policy_bias_inside = all(
        row["observability_bias_inside_5pp"]
        for row in primary_contrasts.values()
    )
    precision_adequate_count = sum(
        row["precision_adequate_for_5pp"]
        for row in primary_contrasts.values()
    )

    geometry = None
    if bool(args.representation) != bool(args.row_index):
        raise SystemExit("--representation and --row-index must be supplied together")
    if args.representation and args.row_index:
        geometry = geometry_quintiles(
            args.representation,
            args.row_index,
            cohort_ids,
            matched,
        )

    if decision_equivalent and policy_bias_inside:
        observability_status = "OBSERVABILITY_NEUTRALITY_SUPPORTED_WITHIN_5PP"
    else:
        observability_status = "OBSERVABILITY_NEUTRALITY_NOT_ESTABLISHED"

    payload = {
        "schema_version": "0.1",
        "status": "FROZEN_T0_IDENTITY_OBSERVABILITY_AUDIT",
        "observability_status": observability_status,
        "outcomes_observed": False,
        "frozen_cohort_count": len(cohort_ids),
        "matched_identity_count": len(matched),
        "overall": overall,
        "by_historical_decision": by_decision,
        "accept_minus_reject_match_fraction": decision_gap,
        "accept_minus_reject_match_fraction_ci95": list(decision_gap_ci)
        if decision_gap_ci
        else None,
        "decision_balance_equivalent_within_5pp": decision_equivalent,
        "policy_selected_identity_support": policy_support,
        "primary_20pct_policy_vs_random": primary_contrasts,
        "all_primary_observability_biases_inside_5pp": policy_bias_inside,
        "primary_contrasts_precision_adequate_count": precision_adequate_count,
        "primary_contrast_count": len(primary_contrasts),
        "geometry_identity_support": geometry,
        "interpretation": (
            "This audit measures outcome observability on the frozen selection "
            "substrate before citations are opened. Failure of neutrality does "
            "not assign value to missing candidates; it narrows admissible claims."
        ),
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
