#!/usr/bin/env python3
"""Audit lineage contamination on the final frozen T0 policy substrate.

This stage reads only frozen lineage flags, historical decision labels for
diagnostics, and outcome-blind policy selections. It never reads citation
outcomes.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

Z95 = 1.959963984540054
MARGIN = 0.05
PRIMARY_BUDGET = "0.20"
BASELINE = "seeded_random"
LINEAGE_FIELDS = (
    "any_exact_lineage",
    "any_lineage_including_sensitivity",
    "any_later_accept_exact_lineage",
    "any_later_accept_lineage_including_sensitivity",
)


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


def summarize(
    ids: list[str],
    lineage: dict[str, dict[str, Any]],
    field: str,
) -> dict[str, Any]:
    total = len(ids)
    count = sum(bool(lineage[candidate_id][field]) for candidate_id in ids)
    ci = wilson_interval(count, total)
    return {
        "candidate_count": total,
        "lineage_count": count,
        "lineage_fraction": count / total if total else None,
        "wilson_ci95": list(ci) if ci else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen-cohort", type=Path, required=True)
    parser.add_argument("--lineage-candidates", type=Path, required=True)
    parser.add_argument("--policy-selections", type=Path, required=True)
    parser.add_argument("--policy-manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    cohort_rows = load_jsonl(args.frozen_cohort)
    cohort_ids = {str(row["forum_id"]) for row in cohort_rows}
    if len(cohort_ids) != len(cohort_rows):
        raise RuntimeError("duplicate forum IDs in frozen cohort")

    lineage_all = {
        str(row["forum_id"]): row
        for row in load_jsonl(args.lineage_candidates)
    }
    if not cohort_ids <= set(lineage_all):
        missing = sorted(cohort_ids - set(lineage_all))
        raise RuntimeError(
            f"lineage file missing {len(missing)} frozen candidates; "
            f"first={missing[:5]}"
        )
    lineage = {
        candidate_id: lineage_all[candidate_id]
        for candidate_id in cohort_ids
    }

    for candidate_id, row in lineage.items():
        for field in LINEAGE_FIELDS:
            if field not in row:
                raise RuntimeError(
                    f"lineage field missing for {candidate_id}: {field}"
                )

    all_ids = sorted(cohort_ids)
    overall = {
        field: summarize(all_ids, lineage, field)
        for field in LINEAGE_FIELDS
    }

    by_decision: dict[str, Any] = {}
    for decision in ("ACCEPT", "REJECT"):
        ids = sorted(
            candidate_id
            for candidate_id in cohort_ids
            if lineage[candidate_id]["historical_decision"] == decision
        )
        by_decision[decision] = {
            "candidate_count": len(ids),
            **{
                field: summarize(ids, lineage, field)
                for field in LINEAGE_FIELDS
            },
        }

    decision_differences: dict[str, Any] = {}
    for field in LINEAGE_FIELDS:
        a = by_decision["ACCEPT"][field]
        r = by_decision["REJECT"][field]
        gap = (
            float(a["lineage_fraction"]) - float(r["lineage_fraction"])
            if a["lineage_fraction"] is not None
            and r["lineage_fraction"] is not None
            else None
        )
        ci = newcombe_difference_interval(
            int(a["lineage_count"]),
            int(a["candidate_count"]),
            int(r["lineage_count"]),
            int(r["candidate_count"]),
        )
        decision_differences[field] = {
            "accept_minus_reject_fraction": gap,
            "newcombe_wilson_ci95": list(ci) if ci else None,
            "equivalent_within_5pp": bool(
                ci and ci[0] >= -MARGIN and ci[1] <= MARGIN
            ),
        }

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
                    f"{budget_key}/{policy}: selected IDs outside frozen cohort"
                )
            ids = sorted(selected)
            policy_support[budget_key][policy] = {
                field: summarize(ids, lineage, field)
                for field in LINEAGE_FIELDS
            }

    if PRIMARY_BUDGET not in policy_support:
        raise RuntimeError(f"missing primary budget {PRIMARY_BUDGET}")
    primary = policy_support[PRIMARY_BUDGET]
    if BASELINE not in primary:
        raise RuntimeError("seeded random baseline missing")

    primary_differences: dict[str, Any] = {}
    for policy in sorted(primary):
        if policy == BASELINE:
            continue
        primary_differences[policy] = {}
        for field in LINEAGE_FIELDS:
            p = primary[policy][field]["lineage_fraction"]
            b = primary[BASELINE][field]["lineage_fraction"]
            gap = (
                float(p) - float(b)
                if p is not None and b is not None
                else None
            )
            primary_differences[policy][field] = {
                "policy_minus_random_fraction": gap,
                "inside_5pp": bool(
                    gap is not None and abs(gap) <= MARGIN
                ),
            }

    decision_balance_ok = all(
        decision_differences[field]["equivalent_within_5pp"]
        for field in (
            "any_exact_lineage",
            "any_lineage_including_sensitivity",
        )
    )
    policy_balance_ok = all(
        result[field]["inside_5pp"]
        for result in primary_differences.values()
        for field in (
            "any_exact_lineage",
            "any_lineage_including_sensitivity",
        )
    )

    if decision_balance_ok and policy_balance_ok:
        gate_status = "LINEAGE_BALANCE_SUPPORTED_WITHIN_5PP"
    else:
        gate_status = "LINEAGE_BALANCE_NOT_ESTABLISHED"

    payload = {
        "schema_version": "0.1",
        "status": "FROZEN_T0_LINEAGE_SUBSTRATE_AUDIT",
        "gate_status": gate_status,
        "outcomes_observed": False,
        "frozen_cohort_count": len(cohort_ids),
        "overall": overall,
        "by_historical_decision": by_decision,
        "decision_differences": decision_differences,
        "policy_lineage_support": policy_support,
        "primary_20pct_policy_vs_random": primary_differences,
        "decision_balance_ok_for_primary_and_sensitivity_lineage":
            decision_balance_ok,
        "policy_balance_ok_for_primary_and_sensitivity_lineage":
            policy_balance_ok,
        "margin": MARGIN,
        "interpretation": (
            "Lineage flags identify later manuscript evolution, not value. "
            "A balanced result permits lineage to remain a sensitivity stratum; "
            "it does not make later outcomes causal for the original manuscript."
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
