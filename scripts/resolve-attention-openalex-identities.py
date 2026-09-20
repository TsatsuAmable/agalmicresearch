#!/usr/bin/env python3
"""Resolve frozen OpenAlex metadata responses into primary identity clusters.

This resolver consumes only identity metadata. It does not read citation fields
or policy selections. Multiple exact-title+author manifestations are retained
as one candidate cluster so later citation acquisition can union and deduplicate
their citing work IDs.
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


def load_gzip_json(path: Path) -> dict[str, Any]:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def canonical_line(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query-manifest", type=Path, required=True)
    parser.add_argument("--metadata-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    queries = [
        json.loads(line)
        for line in args.query_manifest.read_text().splitlines()
        if line.strip()
    ]
    queries.sort(key=lambda row: str(row["forum_id"]))

    resolved: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()

    for query in queries:
        forum_id = str(query["forum_id"])
        raw_path = args.metadata_dir / f"{forum_id}.json.gz"

        if not raw_path.exists():
            row = {
                "forum_id": forum_id,
                "status": "METADATA_NOT_ACQUIRED",
                "identity_cluster": [],
            }
            resolved.append(row)
            counts[row["status"]] += 1
            continue

        payload = load_gzip_json(raw_path)
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
            surnames = result_surnames(result)
            overlap = sorted(candidate_surnames & surnames)
            year = result.get("publication_year")
            in_year_window = (
                isinstance(year, int) and 2019 <= year <= 2022
            )
            if exact_title and overlap and in_year_window:
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

        by_id = {
            member["openalex_id"]: member
            for member in members
        }
        members = [by_id[key] for key in sorted(by_id)]

        if members:
            status = "MATCHED_PRIMARY_IDENTITY_CLUSTER"
        elif exact_title_result_count:
            status = "EXACT_TITLE_NO_AUTHOR_OVERLAP"
        else:
            status = "NO_PRIMARY_MATCH"

        row = {
            "forum_id": forum_id,
            "year": query.get("year"),
            "status": status,
            "query_normalized_title": candidate_title,
            "query_author_surnames": sorted(candidate_surnames),
            "provider_result_count": int(
                payload.get("meta", {}).get("count") or 0
            ),
            "exact_title_result_count": exact_title_result_count,
            "identity_cluster": members,
            "identity_cluster_size": len(members),
            "metadata_raw_sha256": sha256_file(raw_path),
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
        "status": "IDENTITY_ONLY_NO_CITATION_OUTCOMES",
        "candidate_count": len(resolved),
        "status_counts": dict(sorted(counts.items())),
        "matched_primary_count": len(matched),
        "matched_primary_fraction": (
            len(matched) / len(resolved) if resolved else None
        ),
        "identity_cluster_size_counts": dict(sorted(cluster_sizes.items())),
        "query_manifest_sha256": sha256_file(args.query_manifest),
        "resolved_jsonl_sha256": sha256_file(args.out),
    }
    summary_path = args.out.with_suffix(args.out.suffix + ".summary.json")
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
