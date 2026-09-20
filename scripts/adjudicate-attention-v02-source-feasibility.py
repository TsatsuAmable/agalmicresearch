#!/usr/bin/env python3
"""Adjudicate Track A v0.2 source feasibility without opening outcomes.

The gate combines verified pre-review snapshot coverage with the frozen v0.1
2020 T0 cohort and an optimistic upper bound for still-unresolved earlier
cohorts. It asks a deliberately conservative question: can the currently
admissible historical substrate possibly reach the prospectively required
exact-outcome-observable sample size?

Candidate counts are upper bounds on eventual exact-observable N. Therefore,
if even the optimistic upper bound is below the precision target, the design
must stop before further content acquisition or any citation query.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text().splitlines()
        if line.strip()
    ]


def count_jsonl(path: Path) -> int:
    return sum(1 for line in path.read_text().splitlines() if line.strip())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--snapshot-audit",
        type=Path,
        action="append",
        required=True,
    )
    parser.add_argument(
        "--v01-frozen-cohort",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--reviewed-version-audit",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--optimistic-unresolved-year",
        type=int,
        action="append",
        default=[],
    )
    parser.add_argument(
        "--required-exact-observable-n",
        type=int,
        default=4600,
    )
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    manifest = load_jsonl(args.manifest)
    manifest_by_year: dict[int, int] = {}
    for row in manifest:
        year = int(row["year"])
        manifest_by_year[year] = manifest_by_year.get(year, 0) + 1

    source_components: list[dict[str, Any]] = []
    verified_candidate_upper_bound = 0
    audited_years: set[int] = set()

    for audit_path in args.snapshot_audit:
        audit = json.loads(audit_path.read_text())
        year = int(audit["year"])
        audited_years.add(year)
        if audit.get("pre_review_clean") is not True:
            raise SystemExit(
                f"snapshot audit for {year} is not pre-review clean"
            )
        count = int(audit["matched_text_count"])
        verified_candidate_upper_bound += count
        source_components.append(
            {
                "year": year,
                "source": "pre_review_historical_snapshot_text",
                "candidate_upper_bound": count,
                "snapshot_lag_hours": audit["snapshot_lag_hours"],
                "pre_review_clean": True,
                "audit_sha256": sha256_file(audit_path),
            }
        )

    v01_count = count_jsonl(args.v01_frozen_cohort)
    verified_candidate_upper_bound += v01_count
    source_components.append(
        {
            "year": 2020,
            "source": "v01_frozen_decision_time_t0_cohort",
            "candidate_upper_bound": v01_count,
            "pre_review_clean": True,
            "cohort_sha256": sha256_file(args.v01_frozen_cohort),
        }
    )

    unresolved_upper_bound = 0
    unresolved_components: list[dict[str, Any]] = []
    for year in sorted(set(args.optimistic_unresolved_year)):
        if year in audited_years or year == 2020:
            raise SystemExit(
                f"year {year} cannot be both verified and unresolved"
            )
        count = manifest_by_year.get(year, 0)
        unresolved_upper_bound += count
        unresolved_components.append(
            {
                "year": year,
                "source": "raw_accept_reject_frame_optimistic_upper_bound",
                "candidate_upper_bound": count,
                "temporally_admissible": False,
            }
        )

    reviewed = json.loads(args.reviewed_version_audit.read_text())
    reviewed_admissible = bool(reviewed.get("primary_source_admissible"))
    reviewed_component = {
        "year": int(reviewed["year"]),
        "source": "openreview_reviewed_version_field",
        "candidate_count": int(reviewed["reviewed_version_count"]),
        "primary_source_admissible": reviewed_admissible,
        "adjudication": reviewed["adjudication"],
        "accept_minus_reject_availability":
            reviewed[
                "accept_minus_reject_reviewed_version_fraction"
            ],
        "audit_sha256": sha256_file(args.reviewed_version_audit),
    }

    optimistic_pre_review_candidate_upper_bound = (
        verified_candidate_upper_bound + unresolved_upper_bound
    )
    shortfall = (
        args.required_exact_observable_n
        - optimistic_pre_review_candidate_upper_bound
    )

    # The candidate upper bound is already more generous than the final target:
    # no technical attrition or exact-identity attrition is applied here.
    insufficient = optimistic_pre_review_candidate_upper_bound < (
        args.required_exact_observable_n
    )

    if insufficient and not reviewed_admissible:
        adjudication = (
            "SOURCE_FEASIBILITY_INADEQUATE_NEUTRAL_COHORT_REQUIRED"
        )
        proceed_to_bulk_content_acquisition = False
    elif insufficient:
        adjudication = (
            "SOURCE_FEASIBILITY_REQUIRES_ADMISSIBLE_2021_ROUTE"
        )
        proceed_to_bulk_content_acquisition = False
    else:
        adjudication = (
            "SOURCE_COUNT_PLAUSIBLE_PENDING_TEMPORAL_AND_IDENTITY_GATES"
        )
        proceed_to_bulk_content_acquisition = True

    result = {
        "schema_version": "0.1",
        "status": "V02_SOURCE_FEASIBILITY_ADJUDICATION",
        "adjudication": adjudication,
        "required_exact_observable_n": args.required_exact_observable_n,
        "verified_pre_review_candidate_upper_bound":
            verified_candidate_upper_bound,
        "optimistic_unresolved_candidate_upper_bound":
            unresolved_upper_bound,
        "optimistic_pre_review_candidate_upper_bound":
            optimistic_pre_review_candidate_upper_bound,
        "optimistic_shortfall_to_required_n": max(0, shortfall),
        "candidate_bound_is_before_identity_attrition": True,
        "source_components": source_components,
        "unresolved_components": unresolved_components,
        "reviewed_version_component": reviewed_component,
        "proceed_to_bulk_content_acquisition":
            proceed_to_bulk_content_acquisition,
        "citation_outcome_acquisition_authorized": False,
        "outcomes_observed": False,
        "inputs": {
            "manifest_sha256": sha256_file(args.manifest),
            "v01_frozen_cohort_sha256": sha256_file(
                args.v01_frozen_cohort
            ),
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
