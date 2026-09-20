#!/usr/bin/env python3
"""Prepare, but do not execute, OpenAlex outcome-linkage queries.

The output contains evaluation-only matching metadata and exact-title query
specifications. It performs no network calls and cannot expose citation
outcomes. This lets the linkage rules and query surface be frozen before
downstream data acquisition.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
import urllib.parse
from pathlib import Path
from typing import Any

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


def normalize_title(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).lower()
    value = re.sub(r"[^0-9a-z]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def author_surnames(value: str | None) -> list[str]:
    if not value:
        return []
    out: list[str] = []
    for raw_name in value.split(","):
        name = unicodedata.normalize("NFKC", raw_name).strip()
        if not name:
            continue
        tokens = [
            re.sub(r"[^0-9A-Za-z'-]+", "", token)
            for token in name.split()
        ]
        tokens = [token for token in tokens if token]
        if tokens:
            out.append(tokens[-1].casefold())
    return sorted(set(out))


def load_candidate_ids(path: Path, year: int) -> list[str]:
    ids = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if int(row["year"]) == year:
            ids.append(str(row["forum_id"]))
    return sorted(set(ids))


def load_metadata(
    parquet: Path,
    candidate_ids: set[str],
    year: int,
) -> list[dict[str, Any]]:
    try:
        import pyarrow.parquet as pq
    except ImportError as exc:
        raise SystemExit(
            "pyarrow required; run with: uv run --with pyarrow python3 "
            "scripts/prepare-attention-openalex-linkage.py ..."
        ) from exc

    rows = pq.read_table(
        parquet,
        columns=["year", "id", "title", "authors"],
    ).to_pylist()

    selected = [
        row
        for row in rows
        if int(row["year"]) == year and str(row["id"]) in candidate_ids
    ]
    selected.sort(key=lambda row: str(row["id"]))
    return selected


def query_url(title: str) -> str:
    # This is deliberately not requested here. The query manifest freezes the
    # intended evaluation-only API surface without acquiring outcomes.
    params = {
        "filter": (
            "title.search.exact:"
            + title
            + ",publication_year:2019-2022"
        ),
        "select": SELECT_FIELDS,
        "per_page": "25",
    }
    return OPENALEX_BASE + "?" + urllib.parse.urlencode(params)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-jsonl", type=Path, required=True)
    parser.add_argument("--metadata-parquet", type=Path, required=True)
    parser.add_argument("--year", type=int, default=2020)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    candidate_ids = load_candidate_ids(args.candidate_jsonl, args.year)
    metadata = load_metadata(
        args.metadata_parquet,
        set(candidate_ids),
        args.year,
    )

    found_ids = {str(row["id"]) for row in metadata}
    missing = sorted(set(candidate_ids) - found_ids)
    if missing:
        raise RuntimeError(
            f"missing {len(missing)} candidate IDs from metadata source; "
            f"first={missing[:5]}"
        )

    rows = []
    for row in metadata:
        title = str(row["title"] or "").strip()
        if not title:
            raise RuntimeError(f"empty title for {row['id']}")
        surnames = author_surnames(row.get("authors"))
        if not surnames:
            raise RuntimeError(f"no author surnames for {row['id']}")
        rows.append(
            {
                "forum_id": str(row["id"]),
                "year": int(row["year"]),
                "title": title,
                "normalized_title": normalize_title(title),
                "author_surnames": surnames,
                "query": {
                    "provider": "OpenAlex",
                    "endpoint": OPENALEX_BASE,
                    "filter": (
                        "title.search.exact:"
                        + title
                        + ",publication_year:2019-2022"
                    ),
                    "select": SELECT_FIELDS,
                    "per_page": 25,
                    "url_preview": query_url(title),
                },
                "matching_rule": {
                    "primary": (
                        "identity cluster of all exact-normalized-title matches "
                        "with >=1 exact author-surname overlap; exact persistent "
                        "IDs may seed the cluster but do not prevent exact-title "
                        "expansion"
                    ),
                    "fuzzy_sensitivity_only": {
                        "token_set_similarity_min": 0.97,
                        "author_surname_overlap_fraction_min": 0.50,
                        "minimum_matched_surnames": 1,
                        "runner_up_margin_min": 0.03,
                        "publication_year_min": 2019,
                        "publication_year_max": 2022,
                    },
                },
            }
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(
            json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n"
            for row in rows
        ),
        encoding="utf-8",
    )

    manifest = {
        "schema_version": "0.1",
        "status": "QUERY_PREPARATION_ONLY_NO_NETWORK",
        "year": args.year,
        "candidate_count": len(rows),
        "candidate_jsonl_sha256": sha256_file(args.candidate_jsonl),
        "metadata_parquet_sha256": sha256_file(args.metadata_parquet),
        "query_manifest_sha256": sha256_file(args.out),
        "provider": "OpenAlex",
        "network_calls_made": 0,
        "outcomes_observed": False,
    }
    manifest_path = args.out.with_suffix(args.out.suffix + ".manifest.json")
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
