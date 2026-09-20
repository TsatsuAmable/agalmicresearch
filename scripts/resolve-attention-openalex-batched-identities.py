#!/usr/bin/env python3
"""Resolve OR-batched OpenAlex identity metadata to per-candidate clusters.

Consumes only identity metadata. No citation outcome fields or policy outcomes
are read. Each candidate is matched within its own batch response using the
frozen exact-normalized-title + author-surname rule.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import unicodedata
from collections import Counter
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


def load_gzip_json(path: Path) -> dict[str, Any]:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def normalize_title(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).lower()
    value = re.sub(r"[^0-9a-z]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def surname_from_name(value: str | None) -> str | None:
    if not value:
        return None
    value = unicodedata.normalize("NFKC", value).strip()
    tokens = [
        re.sub(r"[^0-9A-Za-z'-]+", "", token)
        for token in value.split()
    ]
    tokens = [token for token in tokens if token]
    return tokens[-1].casefold() if tokens else None


def result_surnames(result: dict[str, Any]) -> set[str]:
    out: set[str] = set()
    for authorship in result.get("authorships") or []:
        author = authorship.get("author") or {}
        surname = surname_from_name(author.get("display_name"))
        if surname:
            out.add(surname)
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
    parser.add_argument("--candidate-query-manifest", type=Path, required=True)
    parser.add_argument("--batch-query-manifest", type=Path, required=True)
    parser.add_argument("--batch-raw-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    candidates = {
        str(row["forum_id"]): row
        for row in load_jsonl(args.candidate_query_manifest)
    }
    batches = load_jsonl(args.batch_query_manifest)

    forum_to_batch: dict[str, str] = {}
    batch_payloads: dict[str, dict[str, Any]] = {}
    missing_batches: set[str] = set()

    for batch in batches:
        batch_id = str(batch["batch_id"])
        for forum_id in batch["forum_ids"]:
            forum_id = str(forum_id)
            if forum_id in forum_to_batch:
                raise RuntimeError(f"candidate appears in multiple batches: {forum_id}")
            forum_to_batch[forum_id] = batch_id
        raw_path = args.batch_raw_dir / f"{batch_id}.json.gz"
        if raw_path.exists():
            batch_payloads[batch_id] = load_gzip_json(raw_path)
        else:
            missing_batches.add(batch_id)

    if set(candidates) != set(forum_to_batch):
        missing = sorted(set(candidates) - set(forum_to_batch))
        extra = sorted(set(forum_to_batch) - set(candidates))
        raise RuntimeError(
            f"batch membership mismatch; missing={missing[:5]} extra={extra[:5]}"
        )

    resolved: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()

    for forum_id in sorted(candidates):
        query = candidates[forum_id]
        batch_id = forum_to_batch[forum_id]

        if batch_id in missing_batches:
            row = {
                "forum_id": forum_id,
                "year": query.get("year"),
                "batch_id": batch_id,
                "status": "BATCH_METADATA_NOT_ACQUIRED",
                "identity_cluster": [],
                "identity_cluster_size": 0,
            }
            resolved.append(row)
            counts[row["status"]] += 1
            continue

        payload = batch_payloads[batch_id]
        candidate_title = str(query["normalized_title"])
        candidate_surnames = {
            str(value).casefold()
            for value in query.get("author_surnames") or []
        }

        members: list[dict[str, Any]] = []
        exact_title_result_count = 0

        for result in payload.get("results") or []:
            display_name = str(result.get("display_name") or "")
            exact_title = normalize_title(display_name) == candidate_title
            if exact_title:
                exact_title_result_count += 1
            if not exact_title:
                continue

            surnames = result_surnames(result)
            overlap = sorted(candidate_surnames & surnames)
            year = result.get("publication_year")
            in_year_window = (
                isinstance(year, int) and 2019 <= year <= 2022
            )
            if not (overlap and in_year_window):
                continue

            work_id = str(result.get("id") or "")
            if not work_id:
                continue
            members.append(
                {
                    "openalex_id": work_id,
                    "doi": result.get("doi"),
                    "display_name": display_name,
                    "publication_year": year,
                    "author_surname_overlap": overlap,
                    "author_surname_overlap_count": len(overlap),
                    "ids": result.get("ids") or {},
                    "updated_date": result.get("updated_date"),
                }
            )

        by_id = {member["openalex_id"]: member for member in members}
        members = [by_id[key] for key in sorted(by_id)]

        if members:
            status = "MATCHED_PRIMARY_IDENTITY_CLUSTER"
        elif exact_title_result_count:
            status = "EXACT_TITLE_NO_AUTHOR_OVERLAP"
        else:
            status = "NO_PRIMARY_MATCH"

        raw_path = args.batch_raw_dir / f"{batch_id}.json.gz"
        row = {
            "forum_id": forum_id,
            "year": query.get("year"),
            "batch_id": batch_id,
            "status": status,
            "query_normalized_title": candidate_title,
            "query_author_surnames": sorted(candidate_surnames),
            "provider_batch_result_count": int(
                payload.get("meta", {}).get("count") or 0
            ),
            "exact_title_result_count": exact_title_result_count,
            "identity_cluster": members,
            "identity_cluster_size": len(members),
            "batch_raw_sha256": sha256_file(raw_path),
        }
        resolved.append(row)
        counts[status] += 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(canonical_line(row) for row in resolved),
        encoding="utf-8",
    )

    matched = [
        row
        for row in resolved
        if row["status"] == "MATCHED_PRIMARY_IDENTITY_CLUSTER"
    ]
    cluster_sizes = Counter(
        str(row["identity_cluster_size"]) for row in matched
    )

    summary = {
        "schema_version": "0.1",
        "status": "BATCHED_IDENTITY_ONLY_NO_CITATION_OUTCOMES",
        "candidate_count": len(resolved),
        "batch_count": len(batches),
        "missing_batch_count": len(missing_batches),
        "status_counts": dict(sorted(counts.items())),
        "matched_primary_count": len(matched),
        "matched_primary_fraction": (
            len(matched) / len(resolved) if resolved else None
        ),
        "identity_cluster_size_counts": dict(sorted(cluster_sizes.items())),
        "candidate_query_manifest_sha256": sha256_file(
            args.candidate_query_manifest
        ),
        "batch_query_manifest_sha256": sha256_file(
            args.batch_query_manifest
        ),
        "resolved_jsonl_sha256": sha256_file(args.out),
        "outcomes_observed": False,
    }

    summary_path = args.out.with_suffix(args.out.suffix + ".summary.json")
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
