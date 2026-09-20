#!/usr/bin/env python3
"""Audit and adjudicate T0 PDF acquisition/extraction availability.

Historical decision labels are joined only for missingness diagnostics. They
never alter acquisition or extraction. Adjudication rules are frozen before
bulk acquisition completes.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

EQUIVALENCE_MARGIN = 0.05
PASS_MIN_USABLE = 0.95
CONDITIONAL_MIN_USABLE = 0.90
WILSON_Z = 1.959963984540054


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text().splitlines()
        if line.strip()
    ]


def latest_by_revision(
    rows: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        out[str(row["revision_openreview_id"])] = row
    return out


def safe_fraction(numer: int, denom: int) -> float | None:
    return numer / denom if denom else None


def wilson_interval(successes: int, total: int) -> tuple[float, float] | None:
    if total <= 0:
        return None
    p = successes / total
    z2 = WILSON_Z * WILSON_Z
    denom = 1.0 + z2 / total
    center = (p + z2 / (2.0 * total)) / denom
    radius = (
        WILSON_Z
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


def extraction_is_usable(extraction: dict[str, Any] | None) -> bool:
    if not extraction or extraction.get("status") != "ok":
        return False
    char_count = int(extraction.get("char_count", 0))
    page_errors = int(extraction.get("page_error_count", 0))
    return char_count >= 1000 and page_errors == 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--acquisition-ledger", type=Path, required=True)
    parser.add_argument("--extraction-ledger", type=Path, required=True)
    parser.add_argument("--year", type=int, default=2020)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    candidates = [
        row
        for row in load_jsonl(args.candidates)
        if int(row["year"]) == args.year
    ]
    acquisitions = latest_by_revision(load_jsonl(args.acquisition_ledger))
    extractions = latest_by_revision(load_jsonl(args.extraction_ledger))

    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        revision_id = str(candidate["revision_openreview_id"])
        acquisition = acquisitions.get(revision_id)
        extraction = extractions.get(revision_id)
        acquired = bool(
            acquisition and acquisition.get("status") == "ok"
        )
        extracted = bool(
            extraction and extraction.get("status") == "ok"
        )
        terminal_acquisition = acquisition is not None
        terminal_extraction = (not acquired) or (extraction is not None)

        rows.append(
            {
                "decision": candidate["decision"],
                "revision_openreview_id": revision_id,
                "acquisition_recorded": terminal_acquisition,
                "extraction_recorded_if_required": terminal_extraction,
                "acquired": acquired,
                "extracted": extracted,
                "usable_primary": extraction_is_usable(extraction),
                "zero_text": bool(
                    extraction
                    and extraction.get("status") == "ok"
                    and int(extraction.get("char_count", 0)) == 0
                ),
                "low_text_lt_1000": bool(
                    extraction
                    and extraction.get("status") == "ok"
                    and 0 < int(extraction.get("char_count", 0)) < 1000
                ),
                "page_errors": bool(
                    extraction
                    and extraction.get("status") == "ok"
                    and int(extraction.get("page_error_count", 0)) > 0
                ),
            }
        )

    def summarize(group: list[dict[str, Any]]) -> dict[str, Any]:
        total = len(group)
        acquired = sum(row["acquired"] for row in group)
        extracted = sum(row["extracted"] for row in group)
        usable = sum(row["usable_primary"] for row in group)
        zero_text = sum(row["zero_text"] for row in group)
        low_text = sum(row["low_text_lt_1000"] for row in group)
        page_errors = sum(row["page_errors"] for row in group)
        usable_ci = wilson_interval(usable, total)
        return {
            "candidate_count": total,
            "acquisition_record_count": sum(
                row["acquisition_recorded"] for row in group
            ),
            "extraction_terminal_count": sum(
                row["extraction_recorded_if_required"] for row in group
            ),
            "acquired_count": acquired,
            "acquired_fraction": safe_fraction(acquired, total),
            "extracted_count": extracted,
            "extracted_fraction_of_candidates": safe_fraction(
                extracted, total
            ),
            "extracted_fraction_of_acquired": safe_fraction(
                extracted, acquired
            ),
            "usable_primary_count": usable,
            "usable_primary_fraction": safe_fraction(usable, total),
            "usable_primary_wilson_ci95": list(usable_ci)
            if usable_ci
            else None,
            "zero_text_count": zero_text,
            "low_text_lt_1000_count": low_text,
            "page_error_record_count": page_errors,
        }

    by_decision = {
        decision: summarize(
            [row for row in rows if row["decision"] == decision]
        )
        for decision in ("ACCEPT", "REJECT")
    }
    overall = summarize(rows)

    complete = all(
        row["acquisition_recorded"]
        and row["extraction_recorded_if_required"]
        for row in rows
    )

    accept = by_decision["ACCEPT"]
    reject = by_decision["REJECT"]
    acquisition_gap = (
        accept["acquired_fraction"] - reject["acquired_fraction"]
        if accept["acquired_fraction"] is not None
        and reject["acquired_fraction"] is not None
        else None
    )
    extraction_gap = (
        accept["extracted_fraction_of_candidates"]
        - reject["extracted_fraction_of_candidates"]
        if accept["extracted_fraction_of_candidates"] is not None
        and reject["extracted_fraction_of_candidates"] is not None
        else None
    )
    usable_gap = (
        accept["usable_primary_fraction"]
        - reject["usable_primary_fraction"]
        if accept["usable_primary_fraction"] is not None
        and reject["usable_primary_fraction"] is not None
        else None
    )
    usable_gap_ci = newcombe_difference_interval(
        int(accept["usable_primary_count"]),
        int(accept["candidate_count"]),
        int(reject["usable_primary_count"]),
        int(reject["candidate_count"]),
    )

    if not complete:
        adjudication = "INCOMPLETE_DO_NOT_ADJUDICATE"
        reason = (
            "Not every candidate has terminal acquisition and required "
            "extraction state."
        )
    else:
        overall_usable = float(overall["usable_primary_fraction"] or 0.0)
        accept_usable = float(
            accept["usable_primary_fraction"] or 0.0
        )
        reject_usable = float(
            reject["usable_primary_fraction"] or 0.0
        )
        gap = float(usable_gap or 0.0)
        ci_within_margin = bool(
            usable_gap_ci
            and usable_gap_ci[0] >= -EQUIVALENCE_MARGIN
            and usable_gap_ci[1] <= EQUIVALENCE_MARGIN
        )

        if (
            overall_usable >= PASS_MIN_USABLE
            and accept_usable >= PASS_MIN_USABLE
            and reject_usable >= PASS_MIN_USABLE
            and ci_within_margin
        ):
            adjudication = "PASS_TECHNICAL_AVAILABILITY"
            reason = (
                "Primary-usable retention is >=95% overall and in both "
                "decision strata, and the 95% CI for the ACCEPT-minus-REJECT "
                "usable-fraction gap lies wholly inside +/-5 percentage points."
            )
        elif (
            overall_usable >= CONDITIONAL_MIN_USABLE
            and accept_usable >= CONDITIONAL_MIN_USABLE
            and reject_usable >= CONDITIONAL_MIN_USABLE
            and abs(gap) <= EQUIVALENCE_MARGIN
        ):
            adjudication = "CONDITIONAL_TECHNICAL_AVAILABILITY"
            reason = (
                "Retention is >=90% in both decision strata and the observed "
                "gap is within +/-5 percentage points, but the stricter PASS "
                "equivalence criterion is not met."
            )
        else:
            adjudication = "ABSTAIN_TECHNICAL_AVAILABILITY"
            reason = (
                "Usable-content retention or decision-stratum balance falls "
                "outside the pre-frozen technical availability bounds."
            )

    payload = {
        "schema_version": "0.2",
        "year": args.year,
        "status": "T0_TECHNICAL_AVAILABILITY_AUDIT",
        "complete": complete,
        "adjudication": adjudication,
        "adjudication_reason": reason,
        "gate_parameters": {
            "primary_usable_rule": (
                "extraction status ok, character count >=1000, "
                "page_error_count == 0"
            ),
            "pass_min_usable_fraction_each_stratum": PASS_MIN_USABLE,
            "conditional_min_usable_fraction_each_stratum":
                CONDITIONAL_MIN_USABLE,
            "decision_gap_equivalence_margin": EQUIVALENCE_MARGIN,
            "decision_gap_interval": "Newcombe-Wilson 95%",
        },
        "overall": overall,
        "by_decision": by_decision,
        "accept_minus_reject_acquisition_fraction": acquisition_gap,
        "accept_minus_reject_extraction_fraction": extraction_gap,
        "accept_minus_reject_usable_primary_fraction": usable_gap,
        "accept_minus_reject_usable_primary_ci95": list(usable_gap_ci)
        if usable_gap_ci
        else None,
        "quality_flag_counts": dict(
            Counter(
                flag
                for row in rows
                for flag, present in (
                    ("ZERO_TEXT", row["zero_text"]),
                    ("LOW_TEXT_LT_1000", row["low_text_lt_1000"]),
                    ("PAGE_ERRORS", row["page_errors"]),
                )
                if present
            )
        ),
        "gate_note": (
            "This adjudicates technical T0 content availability only. "
            "It does not by itself pass the broader outcome-support, "
            "entity-resolution, lineage, coverage-window, construct or "
            "precision requirements in PRE_OUTCOME_FEASIBILITY_GATE.md."
        ),
    }

    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
