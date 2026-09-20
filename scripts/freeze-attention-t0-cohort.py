#!/usr/bin/env python3
"""Freeze the outcome-blind T0 cohort after technical availability adjudication.

The output intentionally excludes historical decision labels. It can be used to
drive the final representation and policy-selection stages without re-exposing
the diagnostic outcome field used by the missingness audit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ALLOWED_ADJUDICATIONS = {
    "PASS_TECHNICAL_AVAILABILITY",
    "CONDITIONAL_TECHNICAL_AVAILABILITY",
}


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


def latest_by_revision(path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in load_jsonl(path):
        out[str(row["revision_openreview_id"])] = row
    return out


def canonical_line(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--acquisition-ledger", type=Path, required=True)
    parser.add_argument("--extraction-ledger", type=Path, required=True)
    parser.add_argument("--technical-audit", type=Path, required=True)
    parser.add_argument("--year", type=int, default=2020)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    audit = json.loads(args.technical_audit.read_text())
    if audit.get("complete") is not True:
        raise SystemExit("technical availability audit is incomplete")
    adjudication = str(audit.get("adjudication"))
    if adjudication not in ALLOWED_ADJUDICATIONS:
        raise SystemExit(
            f"technical availability adjudication does not permit cohort freeze: "
            f"{adjudication}"
        )

    candidates = [
        row
        for row in load_jsonl(args.candidates)
        if int(row["year"]) == args.year
    ]
    acquisitions = latest_by_revision(args.acquisition_ledger)
    extractions = latest_by_revision(args.extraction_ledger)

    frozen: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []

    for candidate in sorted(
        candidates,
        key=lambda row: (str(row["forum_id"]), str(row["revision_openreview_id"])),
    ):
        revision_id = str(candidate["revision_openreview_id"])
        forum_id = str(candidate["forum_id"])
        acquisition = acquisitions.get(revision_id)
        extraction = extractions.get(revision_id)

        acquired = bool(acquisition and acquisition.get("status") == "ok")
        extracted = bool(extraction and extraction.get("status") == "ok")
        char_count = int(extraction.get("char_count", 0)) if extraction else 0
        page_errors = (
            int(extraction.get("page_error_count", 0)) if extraction else 0
        )
        usable = (
            acquired
            and extracted
            and char_count >= 1000
            and page_errors == 0
        )

        if not usable:
            excluded.append(
                {
                    "forum_id": forum_id,
                    "revision_openreview_id": revision_id,
                    "reason": (
                        "acquisition_failed"
                        if not acquired
                        else "extraction_failed"
                        if not extracted
                        else "low_text_lt_1000"
                        if char_count < 1000
                        else "page_extraction_errors"
                    ),
                }
            )
            continue

        frozen.append(
            {
                "year": int(candidate["year"]),
                "forum_id": forum_id,
                "revision_openreview_id": revision_id,
                "revision_tmdate_utc": candidate["revision_tmdate_utc"],
                "source_pdf_sha256": extraction["source_pdf_sha256"],
                "extracted_text_sha256": extraction["text_sha256"],
                "page_count": int(extraction.get("page_count", 0)),
                "char_count": char_count,
                "technical_availability_adjudication": adjudication,
            }
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("".join(canonical_line(row) for row in frozen))
    excluded_path = args.out.with_suffix(args.out.suffix + ".excluded.jsonl")
    excluded_path.write_text("".join(canonical_line(row) for row in excluded))

    manifest = {
        "schema_version": "0.1",
        "status": "FROZEN_T0_OUTCOME_BLIND_COHORT",
        "year": args.year,
        "technical_availability_adjudication": adjudication,
        "candidate_count": len(candidates),
        "included_count": len(frozen),
        "excluded_count": len(excluded),
        "included_fraction": len(frozen) / len(candidates) if candidates else None,
        "outcome_fields_present": False,
        "inputs": {
            "candidates_sha256": sha256_file(args.candidates),
            "acquisition_ledger_sha256": sha256_file(args.acquisition_ledger),
            "extraction_ledger_sha256": sha256_file(args.extraction_ledger),
            "technical_audit_sha256": sha256_file(args.technical_audit),
        },
        "outputs": {
            "cohort_jsonl_sha256": sha256_file(args.out),
            "excluded_jsonl_sha256": sha256_file(excluded_path),
        },
    }
    manifest_path = args.out.with_suffix(args.out.suffix + ".manifest.json")
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
