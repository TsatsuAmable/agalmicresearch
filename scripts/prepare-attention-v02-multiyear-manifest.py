#!/usr/bin/env python3
"""Prepare the outcome-labelled but policy-ineligible v0.2 cohort frame.

This stage reads only conference metadata needed to identify historical
ACCEPT/REJECT papers. It does not expose titles, abstracts, reviews, citations,
or other outcome features to the allocation policy.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

YEARS = (2017, 2018, 2019, 2020, 2021)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_line(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ) + "\n"


def classify_decision(value: str | None) -> str | None:
    value = (value or "").strip()
    if value.startswith("Accept"):
        return "ACCEPT"
    if value == "Reject":
        return "REJECT"
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata-parquet", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    try:
        import pyarrow.parquet as pq
    except ImportError as exc:
        raise SystemExit(
            "pyarrow required; run with: uv run --with pyarrow python3 "
            "scripts/prepare-attention-v02-multiyear-manifest.py ..."
        ) from exc

    rows = pq.read_table(
        args.metadata_parquet,
        columns=["year", "id", "decision"],
    ).to_pylist()

    manifest: list[dict[str, Any]] = []
    raw_counts: Counter[int] = Counter()
    eligible_counts: Counter[int] = Counter()
    accept_counts: Counter[int] = Counter()
    reject_counts: Counter[int] = Counter()

    seen: set[tuple[int, str]] = set()

    for row in rows:
        year = int(row["year"])
        if year not in YEARS:
            continue
        raw_counts[year] += 1
        decision = classify_decision(row.get("decision"))
        if decision is None:
            continue

        forum_id = str(row["id"])
        key = (year, forum_id)
        if key in seen:
            raise RuntimeError(f"duplicate year/forum ID: {key}")
        seen.add(key)

        eligible_counts[year] += 1
        if decision == "ACCEPT":
            accept_counts[year] += 1
        else:
            reject_counts[year] += 1

        manifest.append(
            {
                "year": year,
                "forum_id": forum_id,
                "decision": decision,
                "decision_raw": row.get("decision"),
                "primary_comparison_eligible": True,
                "policy_feature_eligible": False,
                "role": "HISTORICAL_DECISION_DIAGNOSTIC_ONLY",
            }
        )

    manifest.sort(key=lambda row: (row["year"], row["forum_id"]))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(canonical_line(row) for row in manifest),
        encoding="utf-8",
    )

    summary = {
        "schema_version": "0.1",
        "status": "V02_METADATA_ONLY_HISTORICAL_DECISION_FRAME",
        "years": list(YEARS),
        "eligible_candidate_count": len(manifest),
        "policy_feature_eligible": False,
        "outcomes_observed": False,
        "by_year": {
            str(year): {
                "raw_metadata_count": raw_counts[year],
                "eligible_accept_reject_count": eligible_counts[year],
                "accept_count": accept_counts[year],
                "reject_count": reject_counts[year],
            }
            for year in YEARS
        },
        "inputs": {
            "metadata_parquet_sha256": sha256_file(
                args.metadata_parquet
            ),
        },
        "outputs": {
            "manifest_sha256": sha256_file(args.out),
        },
    }
    summary_path = args.out.with_suffix(args.out.suffix + ".summary.json")
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
