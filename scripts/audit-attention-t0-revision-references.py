#!/usr/bin/env python3
"""Identify conservative pre-deadline OpenReview revision references for Track A.

This script does not download PDFs and does not promote a candidate to an
empirical policy input. It identifies historical revision references whose
OpenReview true-modification timestamp is no later than the conference paper
submission deadline. PDF acquisition, hashing, extraction, and leakage review
remain separate gates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

DEADLINES_UTC = {
    2020: "2019-09-25 15:00:00",
    2021: "2020-10-02 15:00:00",
}

DEADLINE_SOURCES = {
    2020: "https://iclr.cc/Conferences/2020/Dates",
    2021: "https://iclr.cc/Conferences/2021/Dates",
}

OPENREVIEW_TMDate_SOURCE = (
    "https://docs.openreview.net/reference/api-v1/entities/note/fields"
)
RESEARCH_ARCADE_SOURCE = (
    "https://github.com/ulab-uiuc/research-arcade/"
    "blob/ecf9c7c2490840b029bd2add4f02d04aca1d014e/"
    "research_arcade/openreview_utils/openreview_crawler.py"
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    )


def load_manifest(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def load_revision_index(path: Path) -> list[dict[str, Any]]:
    try:
        import pyarrow.parquet as pq
    except ImportError as exc:
        raise SystemExit(
            "pyarrow required; run with: uv run --with pyarrow python3 "
            "scripts/audit-attention-t0-revision-references.py ..."
        ) from exc
    return pq.read_table(path).to_pylist()


def build_candidates(
    manifest: list[dict[str, Any]],
    revisions: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    by_paper: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for revision in revisions:
        venue = str(revision.get("venue", ""))
        year = next(
            (year for year in DEADLINES_UTC if venue == f"ICLR.cc/{year}/Conference"),
            None,
        )
        if year is not None:
            by_paper[(year, str(revision["paper_openreview_id"]))].append(revision)

    candidates: list[dict[str, Any]] = []
    summary: dict[str, Any] = {"years": {}}

    for year in sorted(DEADLINES_UTC):
        deadline = DEADLINES_UTC[year]
        year_rows = [
            row
            for row in manifest
            if row["year"] == year and row["decision"] in {"ACCEPT", "REJECT"}
        ]

        for row in year_rows:
            revisions_for_paper = by_paper.get((year, row["forum_id"]), [])
            pre_deadline = [
                revision
                for revision in revisions_for_paper
                if str(revision["time"]) <= deadline
            ]
            if not pre_deadline:
                continue

            chosen = max(pre_deadline, key=lambda revision: str(revision["time"]))
            candidates.append(
                {
                    "year": year,
                    "forum_id": row["forum_id"],
                    "decision": row["decision"],
                    "revision_openreview_id": chosen["revision_openreview_id"],
                    "revision_tmdate_utc": chosen["time"],
                    "submission_deadline_utc": deadline,
                    "temporal_class": "T0_OBSERVED_REVISION_REFERENCE",
                    "pdf_endpoint": (
                        "https://openreview.net/references/pdf?id="
                        + str(chosen["revision_openreview_id"])
                    ),
                    "pdf_acquisition_status": "UNPROBED",
                }
            )

        year_candidates = [c for c in candidates if c["year"] == year]
        decision_counts = Counter(row["decision"] for row in year_rows)
        candidate_counts = Counter(c["decision"] for c in year_candidates)

        summary["years"][str(year)] = {
            "submission_deadline_utc": deadline,
            "primary_manifest_count": len(year_rows),
            "candidate_count": len(year_candidates),
            "candidate_fraction": (
                len(year_candidates) / len(year_rows) if year_rows else None
            ),
            "by_decision": {
                decision: {
                    "candidate_count": candidate_counts[decision],
                    "manifest_count": decision_counts[decision],
                    "fraction": (
                        candidate_counts[decision] / decision_counts[decision]
                        if decision_counts[decision]
                        else None
                    ),
                }
                for decision in ("ACCEPT", "REJECT")
            },
        }

    candidates.sort(key=lambda c: (c["year"], c["forum_id"]))
    return candidates, summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(
            "research/attention_allocation/cohort/"
            "track_a_2020_2021_manifest.jsonl"
        ),
    )
    parser.add_argument("--revision-index", type=Path, required=True)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("research/attention_allocation/t0"),
    )
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    revisions = load_revision_index(args.revision_index)
    candidates, summary = build_candidates(manifest, revisions)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    candidates_path = args.out_dir / "t0_revision_reference_candidates.jsonl"
    candidates_path.write_text(
        "".join(canonical_json(candidate) + "\n" for candidate in candidates)
    )

    payload = {
        "schema_version": "0.1",
        "status": "REFERENCE_IDENTIFICATION_ONLY",
        "manifest_sha256": sha256_file(args.manifest),
        "revision_index_sha256": sha256_file(args.revision_index),
        "revision_index_source": (
            "ulab-ai/ResearchArcade-openreview-papers-revisions"
        ),
        "research_arcade_source_code": RESEARCH_ARCADE_SOURCE,
        "openreview_tmdate_source": OPENREVIEW_TMDate_SOURCE,
        "deadline_sources": DEADLINE_SOURCES,
        "candidate_file_sha256": sha256_file(candidates_path),
        **summary,
    }
    summary_path = args.out_dir / "t0_revision_reference_summary.json"
    summary_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
