#!/usr/bin/env python3
"""Audit OpenAlex identity-linkage support without reading citation outcomes.

Historical ACCEPT/REJECT labels are used only to diagnose whether identity
observability itself is outcome-differential. No citation fields are consumed.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

Z95 = 1.959963984540054
EQUIVALENCE_MARGIN = 0.05


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--resolved-identities", type=Path, required=True)
    parser.add_argument("--year", type=int, default=2020)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    candidates = {
        str(row["forum_id"]): row
        for row in load_jsonl(args.candidates)
        if int(row["year"]) == args.year
    }
    resolved = {
        str(row["forum_id"]): row
        for row in load_jsonl(args.resolved_identities)
        if int(row.get("year") or args.year) == args.year
    }

    if set(candidates) != set(resolved):
        missing = sorted(set(candidates) - set(resolved))
        extra = sorted(set(resolved) - set(candidates))
        raise RuntimeError(
            f"identity audit population mismatch; missing={missing[:5]} "
            f"extra={extra[:5]}"
        )

    rows: list[dict[str, Any]] = []
    for forum_id in sorted(candidates):
        candidate = candidates[forum_id]
        identity = resolved[forum_id]
        matched = (
            identity.get("status") == "MATCHED_PRIMARY_IDENTITY_CLUSTER"
        )
        rows.append(
            {
                "forum_id": forum_id,
                "decision": candidate["decision"],
                "matched": matched,
                "identity_status": identity.get("status"),
                "cluster_size": int(identity.get("identity_cluster_size", 0)),
            }
        )

    def summarize(group: list[dict[str, Any]]) -> dict[str, Any]:
        total = len(group)
        matched = sum(row["matched"] for row in group)
        ci = wilson_interval(matched, total)
        return {
            "candidate_count": total,
            "matched_count": matched,
            "matched_fraction": matched / total if total else None,
            "matched_wilson_ci95": list(ci) if ci else None,
            "status_counts": dict(
                sorted(Counter(str(row["identity_status"]) for row in group).items())
            ),
            "cluster_size_counts_among_matched": dict(
                sorted(
                    Counter(
                        str(row["cluster_size"])
                        for row in group
                        if row["matched"]
                    ).items()
                )
            ),
        }

    overall = summarize(rows)
    by_decision = {
        decision: summarize(
            [row for row in rows if row["decision"] == decision]
        )
        for decision in ("ACCEPT", "REJECT")
    }

    a = by_decision["ACCEPT"]
    r = by_decision["REJECT"]
    gap = (
        float(a["matched_fraction"]) - float(r["matched_fraction"])
        if a["matched_fraction"] is not None
        and r["matched_fraction"] is not None
        else None
    )
    gap_ci = newcombe_difference_interval(
        int(a["matched_count"]),
        int(a["candidate_count"]),
        int(r["matched_count"]),
        int(r["candidate_count"]),
    )
    balanced = bool(
        gap_ci
        and gap_ci[0] >= -EQUIVALENCE_MARGIN
        and gap_ci[1] <= EQUIVALENCE_MARGIN
    )

    if any(
        row["identity_status"] == "BATCH_METADATA_NOT_ACQUIRED"
        for row in rows
    ):
        coverage_status = "IDENTITY_METADATA_INCOMPLETE"
    elif balanced:
        coverage_status = "DECISION_BALANCE_EQUIVALENT_WITHIN_5PP"
    else:
        coverage_status = "DECISION_BALANCE_NOT_ESTABLISHED_WITHIN_5PP"

    payload = {
        "schema_version": "0.1",
        "status": "IDENTITY_SUPPORT_DIAGNOSTIC_NO_CITATION_OUTCOMES",
        "coverage_status": coverage_status,
        "year": args.year,
        "overall": overall,
        "by_decision": by_decision,
        "accept_minus_reject_match_fraction": gap,
        "accept_minus_reject_match_fraction_ci95": list(gap_ci)
        if gap_ci
        else None,
        "decision_balance_equivalence_margin": EQUIVALENCE_MARGIN,
        "decision_balance_equivalent_within_margin": balanced,
        "outcomes_observed": False,
        "interpretation": (
            "Identity-linkage support is not epistemic value. This audit asks "
            "whether downstream observability begins with materially different "
            "identity support across historical decision strata."
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
