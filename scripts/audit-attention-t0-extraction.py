#!/usr/bin/env python3
"""Audit T0 PDF acquisition and extraction missingness by historical decision.

This is a diagnostic-only join. Decision labels are used only after acquisition
and extraction to measure missingness; they never alter extraction behavior.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text().splitlines()
        if line.strip()
    ]


def latest_by_revision(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        out[str(row["revision_openreview_id"])] = row
    return out


def safe_fraction(numer: int, denom: int) -> float | None:
    return numer / denom if denom else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--acquisition-ledger", type=Path, required=True)
    parser.add_argument("--extraction-ledger", type=Path, required=True)
    parser.add_argument("--year", type=int, default=2020)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    candidates = [
        row for row in load_jsonl(args.candidates)
        if int(row["year"]) == args.year
    ]
    acquisitions = latest_by_revision(load_jsonl(args.acquisition_ledger))
    extractions = latest_by_revision(load_jsonl(args.extraction_ledger))

    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        revision_id = str(candidate["revision_openreview_id"])
        acquisition = acquisitions.get(revision_id)
        extraction = extractions.get(revision_id)
        rows.append(
            {
                "decision": candidate["decision"],
                "revision_openreview_id": revision_id,
                "acquired": bool(
                    acquisition and acquisition.get("status") == "ok"
                ),
                "extracted": bool(
                    extraction and extraction.get("status") == "ok"
                ),
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
        zero_text = sum(row["zero_text"] for row in group)
        low_text = sum(row["low_text_lt_1000"] for row in group)
        page_errors = sum(row["page_errors"] for row in group)
        return {
            "candidate_count": total,
            "acquired_count": acquired,
            "acquired_fraction": safe_fraction(acquired, total),
            "extracted_count": extracted,
            "extracted_fraction_of_candidates": safe_fraction(extracted, total),
            "extracted_fraction_of_acquired": safe_fraction(extracted, acquired),
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

    accept = by_decision["ACCEPT"]
    reject = by_decision["REJECT"]
    acquisition_gap = None
    extraction_gap = None
    if (
        accept["acquired_fraction"] is not None
        and reject["acquired_fraction"] is not None
    ):
        acquisition_gap = (
            accept["acquired_fraction"] - reject["acquired_fraction"]
        )
    if (
        accept["extracted_fraction_of_candidates"] is not None
        and reject["extracted_fraction_of_candidates"] is not None
    ):
        extraction_gap = (
            accept["extracted_fraction_of_candidates"]
            - reject["extracted_fraction_of_candidates"]
        )

    payload = {
        "schema_version": "0.1",
        "year": args.year,
        "status": "DIAGNOSTIC_ONLY",
        "overall": overall,
        "by_decision": by_decision,
        "accept_minus_reject_acquisition_fraction": acquisition_gap,
        "accept_minus_reject_extraction_fraction": extraction_gap,
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
            "Do not promote empirical allocation while acquisition/extraction "
            "is incomplete or before missingness and quality flags are reviewed."
        ),
    }

    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
