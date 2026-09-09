#!/usr/bin/env python3
"""Audit a local PeerRead checkout for handoff-triage feasibility.

Usage:
    python scripts/audit_peerread.py /path/to/PeerRead

Standard-library only. The script does not train models or modify the dataset.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, pstdev
from typing import Any, Iterable

NUMERIC_REVIEW_FIELDS = (
    "RECOMMENDATION",
    "REVIEWER_CONFIDENCE",
    "ORIGINALITY",
    "SOUNDNESS_CORRECTNESS",
    "CLARITY",
    "MEANINGFUL_COMPARISON",
)


def iter_review_files(root: Path) -> Iterable[tuple[str, str, Path]]:
    data = root / "data"
    if not data.exists():
        raise SystemExit(f"PeerRead data directory not found: {data}")
    for venue in sorted(p for p in data.iterdir() if p.is_dir()):
        for split in ("train", "dev", "test"):
            reviews = venue / split / "reviews"
            if not reviews.exists():
                continue
            for path in sorted(reviews.glob("*.json")):
                yield venue.name, split, path


def canonical_review(review: dict[str, Any]) -> str:
    """Fingerprint a review while ignoring dictionary key order."""
    return json.dumps(review, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def usable_scores(reviews: list[dict[str, Any]], field: str) -> list[float]:
    values: list[float] = []
    for review in reviews:
        value = review.get(field)
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)) and math.isfinite(float(value)):
            values.append(float(value))
    return values


def hash_files(paths: Iterable[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(str(path).encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def audit(root: Path) -> dict[str, Any]:
    groups: dict[tuple[str, str], dict[str, Any]] = defaultdict(
        lambda: {
            "candidates": 0,
            "accepted_present": 0,
            "accepted_true": 0,
            "with_reviews": 0,
            "review_entries": 0,
            "meta_review_entries": 0,
            "papers_with_duplicate_reviews": 0,
            "duplicate_review_entries": 0,
            "papers_with_2plus_recommendations": 0,
            "recommendation_disagreement": [],
            "fields_present": Counter(),
        }
    )
    all_paths: list[Path] = []
    malformed: list[str] = []

    for venue, split, path in iter_review_files(root):
        all_paths.append(path)
        group = groups[(venue, split)]
        group["candidates"] += 1
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            malformed.append(f"{path}: {exc}")
            continue

        if "accepted" in record:
            group["accepted_present"] += 1
            if record.get("accepted") is True:
                group["accepted_true"] += 1

        reviews = record.get("reviews")
        if not isinstance(reviews, list):
            reviews = []
        reviews = [r for r in reviews if isinstance(r, dict)]
        if reviews:
            group["with_reviews"] += 1
        group["review_entries"] += len(reviews)
        group["meta_review_entries"] += sum(r.get("IS_META_REVIEW") is True for r in reviews)

        fingerprints = [canonical_review(r) for r in reviews]
        duplicate_entries = len(fingerprints) - len(set(fingerprints))
        if duplicate_entries > 0:
            group["papers_with_duplicate_reviews"] += 1
            group["duplicate_review_entries"] += duplicate_entries

        for field in NUMERIC_REVIEW_FIELDS:
            values = usable_scores(reviews, field)
            if values:
                group["fields_present"][field] += 1

        recommendations = usable_scores(reviews, "RECOMMENDATION")
        if len(recommendations) >= 2:
            group["papers_with_2plus_recommendations"] += 1
            group["recommendation_disagreement"].append(pstdev(recommendations))

    output_groups = []
    for (venue, split), group in sorted(groups.items()):
        disagreement = group.pop("recommendation_disagreement")
        fields = group.pop("fields_present")
        candidates = group["candidates"]
        output_groups.append(
            {
                "venue": venue,
                "split": split,
                **group,
                "accept_rate_when_observed": (
                    group["accepted_true"] / group["accepted_present"]
                    if group["accepted_present"]
                    else None
                ),
                "mean_recommendation_pstdev_for_multi_review_papers": (
                    mean(disagreement) if disagreement else None
                ),
                "paper_coverage_by_numeric_field": {
                    field: {
                        "papers": fields.get(field, 0),
                        "fraction": fields.get(field, 0) / candidates if candidates else None,
                    }
                    for field in NUMERIC_REVIEW_FIELDS
                },
            }
        )

    return {
        "peerread_root": str(root.resolve()),
        "review_json_file_count": len(all_paths),
        "review_files_sha256": hash_files(all_paths) if all_paths else None,
        "malformed_file_count": len(malformed),
        "malformed_files": malformed[:20],
        "groups": output_groups,
    }


def print_summary(result: dict[str, Any]) -> None:
    print("PeerRead feasibility audit")
    print("=" * 26)
    print(f"Root: {result['peerread_root']}")
    print(f"Review JSON files: {result['review_json_file_count']}")
    print(f"SHA-256 over review files: {result['review_files_sha256']}")
    print(f"Malformed files: {result['malformed_file_count']}")
    print()
    header = (
        "venue/split",
        "N",
        "accept",
        "reviews",
        "2+ recs",
        "dup papers",
        "mean rec sd",
    )
    print(" | ".join(header))
    print("-" * 110)
    for row in result["groups"]:
        accept = row["accept_rate_when_observed"]
        rec_sd = row["mean_recommendation_pstdev_for_multi_review_papers"]
        print(
            " | ".join(
                [
                    f"{row['venue']}/{row['split']}",
                    str(row["candidates"]),
                    f"{accept:.3f}" if accept is not None else "NA",
                    str(row["review_entries"]),
                    str(row["papers_with_2plus_recommendations"]),
                    str(row["papers_with_duplicate_reviews"]),
                    f"{rec_sd:.3f}" if rec_sd is not None else "NA",
                ]
            )
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("peerread_root", type=Path, help="Path to a PeerRead checkout")
    parser.add_argument(
        "--json",
        dest="json_path",
        type=Path,
        help="Optional output path for the complete machine-readable audit",
    )
    args = parser.parse_args()

    result = audit(args.peerread_root)
    print_summary(result)
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"\nWrote {args.json_path}")


if __name__ == "__main__":
    main()
