#!/usr/bin/env python3
"""Batch frozen OpenAlex exact-title linkage queries using OR filters.

The input remains the per-candidate no-network query manifest. Batching reduces
API budget use while preserving the exact same title and author matching rules.
No network calls are made here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.parse
from pathlib import Path
from typing import Any

MAX_TITLES_PER_BATCH = 25
MAX_ENCODED_URL_LENGTH = 6500
OPENALEX_BASE = "https://api.openalex.org/works"
SELECT_FIELDS = (
    "id,doi,display_name,publication_year,authorships,ids,updated_date"
)


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


def query_filter(titles: list[str]) -> str:
    if any("|" in title for title in titles):
        raise ValueError("title contains OpenAlex OR separator '|'")
    # OpenAlex filter values containing commas must be quoted. Quote every
    # title consistently so batching is insensitive to punctuation, escaping
    # literal double quotes inside titles for the filter grammar.
    quoted = [f'"{title.replace(chr(34), chr(92) + chr(34))}"' for title in titles]
    return (
        "title.search.exact:"
        + "|".join(quoted)
        + ",publication_year:2019-2022"
    )


def url_length(titles: list[str]) -> int:
    params = {
        "filter": query_filter(titles),
        "select": SELECT_FIELDS,
        "per_page": "100",
    }
    return len(
        OPENALEX_BASE + "?" + urllib.parse.urlencode(params)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-query-manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--max-titles-per-batch",
        type=int,
        default=MAX_TITLES_PER_BATCH,
    )
    parser.add_argument(
        "--max-encoded-url-length",
        type=int,
        default=MAX_ENCODED_URL_LENGTH,
    )
    args = parser.parse_args()

    rows = [
        json.loads(line)
        for line in args.candidate_query_manifest.read_text().splitlines()
        if line.strip()
    ]
    rows.sort(key=lambda row: str(row["forum_id"]))

    batches: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []

    def flush() -> None:
        nonlocal current
        if not current:
            return
        titles = [str(row["title"]) for row in current]
        batch_index = len(batches) + 1
        batches.append(
            {
                "batch_id": f"batch-{batch_index:04d}",
                "forum_ids": [str(row["forum_id"]) for row in current],
                "candidate_count": len(current),
                "query": {
                    "provider": "OpenAlex",
                    "endpoint": OPENALEX_BASE,
                    "filter": query_filter(titles),
                    "select": SELECT_FIELDS,
                    "per_page": 100,
                },
            }
        )
        current = []

    for row in rows:
        proposed = current + [row]
        titles = [str(item["title"]) for item in proposed]
        too_many = len(proposed) > args.max_titles_per_batch
        too_long = url_length(titles) > args.max_encoded_url_length
        if current and (too_many or too_long):
            flush()
            proposed = [row]
            titles = [str(row["title"])]
        if url_length(titles) > args.max_encoded_url_length:
            raise RuntimeError(
                f"single-title query exceeds URL limit: {row['forum_id']}"
            )
        current = proposed
    flush()

    forum_ids = [
        forum_id
        for batch in batches
        for forum_id in batch["forum_ids"]
    ]
    if len(forum_ids) != len(rows) or len(set(forum_ids)) != len(rows):
        raise RuntimeError("batching lost or duplicated candidates")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(canonical_line(batch) for batch in batches),
        encoding="utf-8",
    )
    manifest = {
        "schema_version": "0.1",
        "status": "BATCH_QUERY_PREPARATION_ONLY_NO_NETWORK",
        "candidate_count": len(rows),
        "batch_count": len(batches),
        "max_titles_per_batch": args.max_titles_per_batch,
        "max_encoded_url_length": args.max_encoded_url_length,
        "candidate_query_manifest_sha256": sha256_file(
            args.candidate_query_manifest
        ),
        "batch_query_manifest_sha256": sha256_file(args.out),
        "network_calls_made": 0,
        "outcomes_observed": False,
    }
    manifest_path = args.out.with_suffix(args.out.suffix + ".manifest.json")
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
