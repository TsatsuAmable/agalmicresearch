#!/usr/bin/env python3
"""Evaluate frozen Track A policy selections against frozen C5 outcomes.

The evaluator supports either synthetic engineering fixtures or explicit
post-feasibility-gate execution. It never refits allocation policies.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import statistics
from pathlib import Path
from typing import Any

BOOTSTRAP_SEED = 20260920
PERMUTATION_SEED = 20260921
PRIMARY_BUDGET = "0.20"
STRUCTURED_POLICIES = (
    "centrality",
    "centroid_novelty",
    "local_sparsity",
    "kcenter_coverage",
    "exploration_quota",
)
BASELINE_POLICY = "seeded_random"
SMALLEST_EFFECT = 0.05


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def nearest_rank_threshold(values: list[int], percentile: float) -> int:
    if not values:
        raise ValueError("cannot threshold empty outcome set")
    ordered = sorted(values)
    rank = max(1, math.ceil(percentile * len(ordered)))
    return int(ordered[rank - 1])


def load_outcomes(
    outcome_dir: Path,
    allowed_status: str,
) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for path in sorted(outcome_dir.glob("*.json.gz")):
        with gzip.open(path, "rt", encoding="utf-8") as f:
            row = json.load(f)
        if row.get("status") != allowed_status:
            continue
        forum_id = str(row["forum_id"])
        if forum_id in out:
            raise RuntimeError(f"duplicate outcome for {forum_id}")
        out[forum_id] = row
    return out


def percentile(values, q: float) -> float:
    import numpy as np

    return float(np.percentile(values, q, method="linear"))


def recall_for_sample(
    sample_forum_ids: list[str],
    sample_c5: list[int],
    selected: set[str],
) -> float:
    threshold = nearest_rank_threshold(sample_c5, 0.90)
    high_positions = [
        index
        for index, value in enumerate(sample_c5)
        if value >= threshold
    ]
    if not high_positions:
        return float("nan")
    hit = sum(
        sample_forum_ids[index] in selected
        for index in high_positions
    )
    return hit / len(high_positions)


def holm_adjust(pvalues: dict[str, float]) -> dict[str, float]:
    ordered = sorted(pvalues.items(), key=lambda item: item[1])
    m = len(ordered)
    adjusted: dict[str, float] = {}
    running = 0.0
    for index, (name, pvalue) in enumerate(ordered):
        adjusted_value = min(1.0, (m - index) * pvalue)
        running = max(running, adjusted_value)
        adjusted[name] = running
    return adjusted


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy-selections", type=Path, required=True)
    parser.add_argument("--outcome-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--engineering-fixture", action="store_true")
    parser.add_argument("--post-feasibility-gate", action="store_true")
    parser.add_argument("--bootstrap-replicates", type=int, default=10000)
    parser.add_argument("--permutation-replicates", type=int, default=10000)
    args = parser.parse_args()

    if args.engineering_fixture == args.post_feasibility_gate:
        raise SystemExit(
            "choose exactly one of --engineering-fixture or "
            "--post-feasibility-gate"
        )
    if args.bootstrap_replicates < 1000:
        raise SystemExit("bootstrap replicates must be >= 1000")
    if args.permutation_replicates < 1000:
        raise SystemExit("permutation replicates must be >= 1000")

    try:
        import numpy as np
    except ImportError as exc:
        raise SystemExit(
            "numpy required; run with: uv run --with numpy python3 "
            "scripts/evaluate-attention-track-a-outcomes.py ..."
        ) from exc

    expected_status = (
        "ENGINEERING_FIXTURE_OUTCOME"
        if args.engineering_fixture
        else "FROZEN_C5_OUTCOME"
    )
    policies = json.loads(args.policy_selections.read_text())
    outcomes = load_outcomes(args.outcome_dir, expected_status)
    if not outcomes:
        raise RuntimeError("no admissible outcomes found")

    matched_ids = sorted(outcomes)
    c5_by_id = {
        forum_id: int(outcomes[forum_id]["c5_count"])
        for forum_id in matched_ids
    }
    c5_values = [c5_by_id[forum_id] for forum_id in matched_ids]
    high_threshold = nearest_rank_threshold(c5_values, 0.90)
    high_ids = {
        forum_id
        for forum_id in matched_ids
        if c5_by_id[forum_id] >= high_threshold
    }
    total_c5 = sum(c5_values)

    results: dict[str, Any] = {}
    selection_sets: dict[str, dict[str, set[str]]] = {}

    for budget_key in sorted(policies, key=float):
        results[budget_key] = {}
        selection_sets[budget_key] = {}
        for policy_name, selection in policies[budget_key].items():
            selected = {
                str(value)
                for value in selection["selected_forum_ids"]
            }
            selection_sets[budget_key][policy_name] = selected
            k = int(selection["k"])
            if len(selected) != k:
                raise RuntimeError(
                    f"{budget_key}/{policy_name}: unique forum ids "
                    f"{len(selected)} != k {k}"
                )

            selected_observed = sorted(selected & set(matched_ids))
            selected_high = selected & high_ids
            selected_c5 = [
                c5_by_id[forum_id]
                for forum_id in selected_observed
            ]
            recovered_c5 = sum(selected_c5)
            selected_breadth = [
                int(outcomes[forum_id].get("citation_year_breadth", 0))
                for forum_id in selected_observed
            ]

            results[budget_key][policy_name] = {
                "k": k,
                "selected_outcome_observable_count": len(
                    selected_observed
                ),
                "selected_outcome_observable_fraction": (
                    len(selected_observed) / k if k else None
                ),
                "high_recognition_recall": (
                    len(selected_high) / len(high_ids)
                    if high_ids
                    else None
                ),
                "high_recognition_selected_count": len(selected_high),
                "high_recognition_missed_count": (
                    len(high_ids) - len(selected_high)
                ),
                "c5_mass_recovered_fraction": (
                    recovered_c5 / total_c5
                    if total_c5
                    else None
                ),
                "mean_c5_selected_observed": (
                    statistics.fmean(selected_c5)
                    if selected_c5
                    else None
                ),
                "median_c5_selected_observed": (
                    statistics.median(selected_c5)
                    if selected_c5
                    else None
                ),
                "mean_citation_year_breadth_selected_observed": (
                    statistics.fmean(selected_breadth)
                    if selected_breadth
                    else None
                ),
            }

    if PRIMARY_BUDGET not in selection_sets:
        raise RuntimeError(
            f"primary budget {PRIMARY_BUDGET} missing"
        )
    primary_sets = selection_sets[PRIMARY_BUDGET]
    if BASELINE_POLICY not in primary_sets:
        raise RuntimeError("seeded random baseline missing")

    for policy in STRUCTURED_POLICIES:
        if policy not in primary_sets:
            raise RuntimeError(f"primary policy missing: {policy}")

    matched_forum = np.asarray(matched_ids, dtype=object)
    matched_c5 = np.asarray(c5_values, dtype=np.int64)
    n = len(matched_ids)

    bootstrap_rng = np.random.default_rng(BOOTSTRAP_SEED)
    bootstrap_deltas: dict[str, list[float]] = {
        policy: [] for policy in STRUCTURED_POLICIES
    }

    for _ in range(args.bootstrap_replicates):
        sample_idx = bootstrap_rng.integers(0, n, size=n)
        sample_ids = [
            str(value)
            for value in matched_forum[sample_idx].tolist()
        ]
        sample_values = [
            int(value)
            for value in matched_c5[sample_idx].tolist()
        ]
        baseline_recall = recall_for_sample(
            sample_ids,
            sample_values,
            primary_sets[BASELINE_POLICY],
        )
        for policy in STRUCTURED_POLICIES:
            policy_recall = recall_for_sample(
                sample_ids,
                sample_values,
                primary_sets[policy],
            )
            bootstrap_deltas[policy].append(
                policy_recall - baseline_recall
            )

    bootstrap_summary: dict[str, Any] = {}
    for policy, values in bootstrap_deltas.items():
        lower = percentile(values, 2.5)
        upper = percentile(values, 97.5)
        median_delta = percentile(values, 50.0)
        half_width = (upper - lower) / 2.0
        observed_delta = (
            results[PRIMARY_BUDGET][policy][
                "high_recognition_recall"
            ]
            - results[PRIMARY_BUDGET][BASELINE_POLICY][
                "high_recognition_recall"
            ]
        )
        bootstrap_summary[policy] = {
            "observed_delta": observed_delta,
            "bootstrap_median_delta": median_delta,
            "ci95": [lower, upper],
            "ci95_half_width": half_width,
            "smallest_effect_of_interest": SMALLEST_EFFECT,
            "precision_inadequate": half_width > SMALLEST_EFFECT,
        }

    # Secondary exchangeability test: permute C5 values over fixed candidate
    # identities, then recompute top-decile labels and recall deltas.
    observed_abs = {
        policy: abs(
            bootstrap_summary[policy]["observed_delta"]
        )
        for policy in STRUCTURED_POLICIES
    }
    exceed = {policy: 0 for policy in STRUCTURED_POLICIES}
    permutation_rng = np.random.default_rng(PERMUTATION_SEED)

    for _ in range(args.permutation_replicates):
        permuted = permutation_rng.permutation(matched_c5)
        threshold = nearest_rank_threshold(
            [int(value) for value in permuted.tolist()],
            0.90,
        )
        high_mask = permuted >= threshold
        high_count = int(high_mask.sum())
        if high_count == 0:
            continue

        def perm_recall(selected: set[str]) -> float:
            hits = 0
            for index, is_high in enumerate(high_mask):
                if bool(is_high) and matched_ids[index] in selected:
                    hits += 1
            return hits / high_count

        baseline = perm_recall(primary_sets[BASELINE_POLICY])
        for policy in STRUCTURED_POLICIES:
            delta = perm_recall(primary_sets[policy]) - baseline
            if abs(delta) >= observed_abs[policy] - 1e-15:
                exceed[policy] += 1

    raw_p = {
        policy: (exceed[policy] + 1)
        / (args.permutation_replicates + 1)
        for policy in STRUCTURED_POLICIES
    }
    adjusted_p = holm_adjust(raw_p)
    for policy in STRUCTURED_POLICIES:
        bootstrap_summary[policy][
            "exchangeability_randomization_p_two_sided"
        ] = raw_p[policy]
        bootstrap_summary[policy][
            "holm_adjusted_p"
        ] = adjusted_p[policy]

    payload = {
        "schema_version": "0.1",
        "status": (
            "ENGINEERING_FIXTURE_ONLY"
            if args.engineering_fixture
            else "POST_GATE_PRIMARY_ANALYSIS"
        ),
        "matched_outcome_count": len(matched_ids),
        "c5_high_recognition_threshold": high_threshold,
        "high_recognition_count": len(high_ids),
        "total_c5": total_c5,
        "primary_budget": PRIMARY_BUDGET,
        "smallest_effect_of_interest": SMALLEST_EFFECT,
        "bootstrap": {
            "replicates": args.bootstrap_replicates,
            "seed": BOOTSTRAP_SEED,
            "comparisons": bootstrap_summary,
        },
        "randomization": {
            "replicates": args.permutation_replicates,
            "seed": PERMUTATION_SEED,
            "null": (
                "C5 exchangeable across matched candidate identities; "
                "policy selections fixed"
            ),
        },
        "results_by_budget": results,
        "inputs": {
            "policy_selections_sha256": sha256_file(
                args.policy_selections
            ),
        },
    }
    rendered = json.dumps(
        payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
    ) + "\n"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
