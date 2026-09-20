#!/usr/bin/env python3
"""Adjudicate the Track A broader pre-outcome feasibility gate.

This script combines already-frozen, outcome-free technical, observability,
lineage, construct and precision evidence. It never reads citation outcomes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

FORBIDDEN_ROW_INDEX_KEYS = {
    "decision",
    "historical_decision",
    "review_score",
    "reviewer_confidence",
    "citations",
    "cited_by_count",
    "c5_count",
    "future_value",
    "downstream_value",
    "acceptance_probability",
}
FOLLOWUP_START = "2019-09-26"
FOLLOWUP_END = "2024-09-25"
PRIMARY_OUTCOME = "C5"
SOEI = 0.05
PRIMARY_BUDGET = "0.20"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text().splitlines()
        if line.strip()
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalization-status", type=Path, required=True)
    parser.add_argument("--technical-audit", type=Path, required=True)
    parser.add_argument("--observability-audit", type=Path, required=True)
    parser.add_argument("--lineage-audit", type=Path, required=True)
    parser.add_argument("--design-precision-audit", type=Path, required=True)
    parser.add_argument("--representation-manifest", type=Path, required=True)
    parser.add_argument("--row-index", type=Path, required=True)
    parser.add_argument("--policy-manifest", type=Path, required=True)
    parser.add_argument("--outcome-preregistration", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    finalization = load_json(args.finalization_status)
    technical = load_json(args.technical_audit)
    observability = load_json(args.observability_audit)
    lineage = load_json(args.lineage_audit)
    precision = load_json(args.design_precision_audit)
    representation = load_json(args.representation_manifest)
    policy = load_json(args.policy_manifest)
    row_index = load_jsonl(args.row_index)
    outcome_prereg = args.outcome_preregistration.read_text()

    fatal: list[str] = []
    conditional: list[str] = []
    passes: list[str] = []

    # 1. Temporal integrity and outcome blindness.
    temporal_checks = {
        "finalization_complete": (
            finalization.get("status") == "OUTCOME_BLIND_T0_STAGE_COMPLETE"
        ),
        "finalizer_outcomes_untouched": (
            finalization.get("outcomes_touched") is False
        ),
        "representation_frozen_t0": (
            representation.get("status") == "FROZEN_T0_REPRESENTATION"
        ),
        "policy_selections_frozen_t0": (
            policy.get("status") == "FROZEN_T0_POLICY_SELECTIONS"
        ),
        "frozen_cohort_bound_to_representation": bool(
            representation.get("inputs", {}).get("frozen_cohort_sha256")
        ),
    }

    leaked_row_keys: set[str] = set()
    for row in row_index:
        leaked_row_keys.update(FORBIDDEN_ROW_INDEX_KEYS.intersection(row))
    temporal_checks["row_index_forbidden_keys_absent"] = not leaked_row_keys

    if all(temporal_checks.values()):
        passes.append("temporal_integrity")
    else:
        fatal.append("temporal_integrity_failed")

    # 2. Technical T0 availability.
    technical_status = str(technical.get("adjudication"))
    if not technical.get("complete"):
        fatal.append("technical_availability_incomplete")
    elif technical_status == "PASS_TECHNICAL_AVAILABILITY":
        passes.append("technical_availability")
    elif technical_status == "CONDITIONAL_TECHNICAL_AVAILABILITY":
        conditional.append("technical_availability_conditional")
    else:
        fatal.append(f"technical_availability:{technical_status}")

    # 3. Outcome support and differential observability.
    matched_count = int(observability.get("matched_identity_count") or 0)
    frozen_count = int(observability.get("frozen_cohort_count") or 0)
    by_decision = observability.get("by_historical_decision") or {}
    accept_matched = int(
        (by_decision.get("ACCEPT") or {}).get("matched_count") or 0
    )
    reject_matched = int(
        (by_decision.get("REJECT") or {}).get("matched_count") or 0
    )
    primary_policy_support = (
        observability.get("policy_selected_identity_support") or {}
    ).get(PRIMARY_BUDGET) or {}
    every_primary_policy_has_support = bool(primary_policy_support) and all(
        int((record or {}).get("matched_count") or 0) > 0
        for record in primary_policy_support.values()
    )

    outcome_support_ok = (
        matched_count > 0
        and frozen_count > 0
        and accept_matched > 0
        and reject_matched > 0
        and every_primary_policy_has_support
    )
    if outcome_support_ok:
        passes.append("nonzero_outcome_identity_support")
    else:
        fatal.append("outcome_identity_support_absent")

    observability_status = str(observability.get("observability_status"))
    all_policy_bias_inside = bool(
        observability.get("all_primary_observability_biases_inside_5pp")
    )
    if (
        observability_status
        == "OBSERVABILITY_NEUTRALITY_SUPPORTED_WITHIN_5PP"
    ):
        passes.append("differential_observability")
    elif outcome_support_ok and all_policy_bias_inside:
        conditional.append("observable_exact_matched_cohort_only")
    else:
        fatal.append("policy_contrast_observability_bias_not_controlled")

    # 4. Entity resolution.
    if observability.get("status") == "FROZEN_T0_IDENTITY_OBSERVABILITY_AUDIT":
        passes.append("exact_identity_resolution")
    else:
        fatal.append("identity_resolution_not_frozen")

    # 5. Lineage.
    lineage_status = str(lineage.get("gate_status"))
    lineage_policy_balance = bool(
        lineage.get(
            "policy_balance_ok_for_primary_and_sensitivity_lineage"
        )
    )
    if lineage_status == "LINEAGE_BALANCE_SUPPORTED_WITHIN_5PP":
        passes.append("lineage")
        conditional.append("later_accept_lineage_sensitivity_required")
    elif lineage_policy_balance:
        conditional.append("lineage_historical_balance_not_established")
        conditional.append("later_accept_lineage_sensitivity_required")
    else:
        fatal.append("lineage_ambiguity_affects_primary_policy_contrast")

    # 6. Common fixed coverage window.
    coverage_window_checks = {
        "start_present": FOLLOWUP_START in outcome_prereg,
        "end_present": FOLLOWUP_END in outcome_prereg,
        "primary_outcome_present": PRIMARY_OUTCOME in outcome_prereg,
    }
    if all(coverage_window_checks.values()):
        passes.append("fixed_coverage_window")
    else:
        fatal.append("fixed_coverage_window_not_frozen")

    # 7. Construct non-circularity.
    representation_inputs = representation.get("inputs") or {}
    construct_checks = {
        "representation_has_frozen_cohort_hash": bool(
            representation_inputs.get("frozen_cohort_sha256")
        ),
        "row_index_no_forbidden_outcome_keys": not leaked_row_keys,
        "policy_seed_frozen": int(policy.get("seed") or -1) == 20260920,
        "primary_budget_frozen": any(
            abs(float(x) - 0.20) < 1e-12
            for x in (policy.get("budget_fractions") or [])
        ),
    }
    if all(construct_checks.values()):
        passes.append("construct_non_circularity")
    else:
        fatal.append("construct_non_circularity_failed")

    # 8. Precision.
    precision_status = str(precision.get("status"))
    adequate_count = int(precision.get("adequate_comparison_count") or 0)
    comparison_count = int(precision.get("comparison_count") or 0)
    if (
        precision_status == "DESIGN_PRECISION_ADEQUATE"
        and comparison_count > 0
        and adequate_count == comparison_count
    ):
        passes.append("design_precision")
        precision_scope = "all_preregistered_primary_comparisons"
    elif (
        precision_status == "DESIGN_PRECISION_MIXED"
        and adequate_count > 0
    ):
        conditional.append("precision_restricted_to_adequate_comparisons")
        precision_scope = "adequate_primary_comparisons_only"
    else:
        fatal.append("design_precision_inadequate_for_frozen_5pp_effect")
        precision_scope = "none"

    if fatal:
        verdict = "ABSTAIN_PRE_OUTCOME"
        citation_authorized = False
    elif conditional:
        verdict = "CONDITIONAL_PASS_PRE_OUTCOME"
        citation_authorized = True
    else:
        verdict = "PASS_PRE_OUTCOME"
        citation_authorized = True

    payload = {
        "schema_version": "0.1",
        "status": "BROADER_PRE_OUTCOME_FEASIBILITY_ADJUDICATION",
        "verdict": verdict,
        "citation_outcome_acquisition_authorized": citation_authorized,
        "outcomes_observed": False,
        "primary_budget": PRIMARY_BUDGET,
        "smallest_effect_of_interest": SOEI,
        "fixed_followup_window": [FOLLOWUP_START, FOLLOWUP_END],
        "primary_outcome": PRIMARY_OUTCOME,
        "passes": passes,
        "conditional_restrictions": conditional,
        "fatal_reasons": fatal,
        "precision_scope": precision_scope,
        "temporal_checks": temporal_checks,
        "coverage_window_checks": coverage_window_checks,
        "construct_checks": construct_checks,
        "leaked_row_index_keys": sorted(leaked_row_keys),
        "outcome_support": {
            "frozen_cohort_count": frozen_count,
            "matched_identity_count": matched_count,
            "accept_matched_count": accept_matched,
            "reject_matched_count": reject_matched,
            "every_primary_policy_has_nonzero_identity_support":
                every_primary_policy_has_support,
        },
        "observability": {
            "status": observability_status,
            "all_primary_policy_observability_biases_inside_5pp":
                all_policy_bias_inside,
        },
        "lineage": {
            "status": lineage_status,
            "policy_balance_ok_for_primary_and_sensitivity":
                lineage_policy_balance,
        },
        "precision": {
            "status": precision_status,
            "adequate_comparison_count": adequate_count,
            "comparison_count": comparison_count,
        },
        "input_hashes": {
            "finalization_status_sha256": sha256_file(
                args.finalization_status
            ),
            "technical_audit_sha256": sha256_file(args.technical_audit),
            "observability_audit_sha256": sha256_file(
                args.observability_audit
            ),
            "lineage_audit_sha256": sha256_file(args.lineage_audit),
            "design_precision_audit_sha256": sha256_file(
                args.design_precision_audit
            ),
            "representation_manifest_sha256": sha256_file(
                args.representation_manifest
            ),
            "row_index_sha256": sha256_file(args.row_index),
            "policy_manifest_sha256": sha256_file(args.policy_manifest),
            "outcome_preregistration_sha256": sha256_file(
                args.outcome_preregistration
            ),
        },
        "interpretation": (
            "PASS/CONDITIONAL authorizes only the frozen descriptive "
            "outcome-recovery analysis and never a causal acceptance effect. "
            "ABSTAIN stops citation acquisition under protocol v0.1."
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
