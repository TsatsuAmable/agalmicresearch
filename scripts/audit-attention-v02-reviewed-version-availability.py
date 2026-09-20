#!/usr/bin/env python3
"""Audit ICLR 2021 reviewed-version availability before v0.2 source use.

This audit tests whether OpenReview's historical reviewed_version_(pdf)
field could serve as a decision-time text source without importing a
historical-decision-linked missingness mechanism.

It reads only the frozen ACCEPT/REJECT manifest and already archived OpenReview
root-note metadata. It does not query citations or inspect any downstream
recognition outcome.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
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


def wilson_interval(successes: int, total: int) -> tuple[float, float]:
    if total <= 0:
        return (0.0, 1.0)
    z = 1.959963984540054
    p = successes / total
    z2 = z * z
    denom = 1.0 + z2 / total
    center = (p + z2 / (2.0 * total)) / denom
    half = (
        z
        * math.sqrt(
            p * (1.0 - p) / total
            + z2 / (4.0 * total * total)
        )
        / denom
    )
    return (max(0.0, center - half), min(1.0, center + half))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--archive-res-dir", type=Path, required=True)
    parser.add_argument("--year", type=int, default=2021)
    parser.add_argument("--materiality-bound", type=float, default=0.05)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    eligible_rows = [
        row
        for row in load_jsonl(args.manifest)
        if int(row["year"]) == args.year
    ]
    eligible = {str(row["forum_id"]): row for row in eligible_rows}
    if not eligible:
        raise RuntimeError(f"no eligible candidates for year {args.year}")

    invitation = f"ICLR.cc/{args.year}/Conference/-/Blind_Submission"
    roots: dict[str, dict[str, Any]] = {}

    for path in sorted(args.archive_res_dir.glob("*.json")):
        forum_id = path.stem
        if forum_id not in eligible:
            continue
        try:
            payload = json.loads(path.read_text())
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        for note in payload.get("notes") or []:
            if (
                note.get("id") == forum_id
                and note.get("replyto") is None
                and note.get("invitation") == invitation
            ):
                roots[forum_id] = note
                break

    matched_ids = set(eligible) & set(roots)
    reviewed_ids = {
        forum_id
        for forum_id in matched_ids
        if roots[forum_id]
        .get("content", {})
        .get("reviewed_version_(pdf)")
    }

    by_decision: dict[str, dict[str, Any]] = {}
    for decision in ("ACCEPT", "REJECT"):
        ids = {
            forum_id
            for forum_id in matched_ids
            if eligible[forum_id].get("decision") == decision
        }
        available = ids & reviewed_ids
        lo, hi = wilson_interval(len(available), len(ids))
        by_decision[decision] = {
            "matched_root_count": len(ids),
            "reviewed_version_count": len(available),
            "reviewed_version_fraction": (
                len(available) / len(ids) if ids else 0.0
            ),
            "reviewed_version_fraction_ci95": [lo, hi],
        }

    accept_fraction = by_decision["ACCEPT"][
        "reviewed_version_fraction"
    ]
    reject_fraction = by_decision["REJECT"][
        "reviewed_version_fraction"
    ]
    difference = accept_fraction - reject_fraction
    neutral = abs(difference) <= args.materiality_bound

    result = {
        "schema_version": "0.1",
        "status": "V02_REVIEWED_VERSION_AVAILABILITY_AUDIT",
        "year": args.year,
        "eligible_candidate_count": len(eligible),
        "matched_root_count": len(matched_ids),
        "reviewed_version_count": len(reviewed_ids),
        "reviewed_version_fraction": (
            len(reviewed_ids) / len(matched_ids)
            if matched_ids
            else 0.0
        ),
        "by_historical_decision": by_decision,
        "accept_minus_reject_reviewed_version_fraction": difference,
        "materiality_bound": args.materiality_bound,
        "selection_neutral_within_materiality_bound": neutral,
        "primary_source_admissible": neutral,
        "adjudication": (
            "REVIEWED_VERSION_ROUTE_ADMISSIBLE"
            if neutral
            else "REVIEWED_VERSION_ROUTE_DISQUALIFIED_SELECTION_LINKED"
        ),
        "outcomes_observed": False,
        "inputs": {
            "manifest_sha256": sha256_file(args.manifest),
            "archive_res_dir": str(args.archive_res_dir),
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
