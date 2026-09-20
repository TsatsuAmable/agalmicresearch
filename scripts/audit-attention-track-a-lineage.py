#!/usr/bin/env python3
"""Audit later ICLR resubmission/manuscript lineage for Track A.

This script is outcome-free with respect to downstream citations. It compares
the frozen ICLR 2020 T0 candidate frame with later ICLR metadata using a
pre-frozen exact-title rule and a conservative near-title sensitivity rule.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

Z95 = 1.959963984540054
EQUIVALENCE_MARGIN = 0.05
NEAR_TITLE_MIN = 0.97
AUTHOR_OVERLAP_MIN = 0.50
LATER_YEAR_MIN = 2021
LATER_YEAR_MAX = 2026


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


def canonical_line(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ) + "\n"


def normalize_title(value: str | None) -> str:
    text = unicodedata.normalize("NFKC", value or "").casefold()
    text = re.sub(r"[^0-9a-z]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def author_surnames(value: str | None) -> set[str]:
    if not value:
        return set()
    out: set[str] = set()
    for raw_name in str(value).split(","):
        name = unicodedata.normalize("NFKC", raw_name).strip()
        if not name:
            continue
        tokens = [
            re.sub(r"[^0-9A-Za-z'-]+", "", token)
            for token in name.split()
        ]
        tokens = [token for token in tokens if token]
        if tokens:
            out.add(tokens[-1].casefold())
    return out


def overlap_coefficient(left: set[str], right: set[str]) -> float:
    denom = min(len(left), len(right))
    if denom == 0:
        return 0.0
    return len(left & right) / denom


def decision_class(value: str | None) -> str:
    value = (value or "").strip()
    if value.startswith("Accept"):
        return "ACCEPT"
    if value == "Reject":
        return "REJECT"
    if value == "Withdrawn":
        return "WITHDRAWN"
    if value == "Desk rejected":
        return "DESK_REJECTED"
    return value.upper() or "MISSING"


def wilson_interval(successes: int, total: int) -> tuple[float, float] | None:
    if total <= 0:
        return None
    p = successes / total
    z2 = Z95 * Z95
    denom = 1.0 + z2 / total
    center = (p + z2 / (2.0 * total)) / denom
    radius = (
        Z95
        * math.sqrt(
            (p * (1.0 - p) / total)
            + (z2 / (4.0 * total * total))
        )
        / denom
    )
    return max(0.0, center - radius), min(1.0, center + radius)


def newcombe_difference_interval(
    success_a: int,
    total_a: int,
    success_b: int,
    total_b: int,
) -> tuple[float, float] | None:
    if total_a <= 0 or total_b <= 0:
        return None
    ia = wilson_interval(success_a, total_a)
    ib = wilson_interval(success_b, total_b)
    if ia is None or ib is None:
        return None
    pa = success_a / total_a
    pb = success_b / total_b
    diff = pa - pb
    lower = diff - math.sqrt(
        (pa - ia[0]) ** 2 + (ib[1] - pb) ** 2
    )
    upper = diff + math.sqrt(
        (ia[1] - pa) ** 2 + (pb - ib[0]) ** 2
    )
    return max(-1.0, lower), min(1.0, upper)


def summarize_boolean(
    rows: list[dict[str, Any]],
    field: str,
) -> dict[str, Any]:
    total = len(rows)
    hit = sum(bool(row[field]) for row in rows)
    ci = wilson_interval(hit, total)
    return {
        "candidate_count": total,
        "count": hit,
        "fraction": hit / total if total else None,
        "wilson_ci95": list(ci) if ci else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--metadata-parquet", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--year", type=int, default=2020)
    args = parser.parse_args()

    try:
        import pyarrow.parquet as pq
        from rapidfuzz import fuzz
    except ImportError as exc:
        raise SystemExit(
            "pyarrow and rapidfuzz required; run with: "
            "uv run --with pyarrow --with rapidfuzz python3 "
            "scripts/audit-attention-track-a-lineage.py ..."
        ) from exc

    candidates = [
        row
        for row in load_jsonl(args.candidates)
        if int(row["year"]) == args.year
    ]
    candidate_ids = {str(row["forum_id"]) for row in candidates}

    metadata = pq.read_table(
        args.metadata_parquet,
        columns=["year", "id", "title", "authors", "decision"],
    ).to_pylist()

    source_2020 = {
        str(row["id"]): row
        for row in metadata
        if int(row["year"]) == args.year
        and str(row["id"]) in candidate_ids
    }
    if set(source_2020) != candidate_ids:
        missing = sorted(candidate_ids - set(source_2020))
        raise RuntimeError(
            f"metadata missing {len(missing)} candidate records; "
            f"first={missing[:5]}"
        )

    later: list[dict[str, Any]] = []
    for row in metadata:
        year = int(row["year"])
        if not (LATER_YEAR_MIN <= year <= LATER_YEAR_MAX):
            continue
        norm_title = normalize_title(row.get("title"))
        surnames = author_surnames(row.get("authors"))
        if not norm_title or not surnames:
            continue
        later.append(
            {
                "year": year,
                "forum_id": str(row["id"]),
                "title": row.get("title"),
                "normalized_title": norm_title,
                "author_surnames": surnames,
                "decision": decision_class(row.get("decision")),
                "decision_raw": row.get("decision"),
            }
        )
    later.sort(key=lambda row: (row["year"], row["forum_id"]))

    exact_index: dict[str, list[int]] = defaultdict(list)
    later_titles: list[str] = []
    token_index: dict[str, set[int]] = defaultdict(set)
    for index, row in enumerate(later):
        title = row["normalized_title"]
        exact_index[title].append(index)
        later_titles.append(title)
        for token in set(title.split()):
            if len(token) >= 4:
                token_index[token].add(index)

    edges: list[dict[str, Any]] = []
    by_candidate_edge_keys: dict[str, set[tuple[str, str]]] = defaultdict(set)

    for candidate in sorted(candidates, key=lambda row: str(row["forum_id"])):
        forum_id = str(candidate["forum_id"])
        base = source_2020[forum_id]
        base_title = normalize_title(base.get("title"))
        base_authors = author_surnames(base.get("authors"))
        if not base_title or not base_authors:
            continue

        exact_later_indexes = exact_index.get(base_title, [])
        exact_index_set = set(exact_later_indexes)

        for index in exact_later_indexes:
            target = later[index]
            overlap = sorted(base_authors & target["author_surnames"])
            if not overlap:
                continue
            key = (target["forum_id"], "PRIMARY_EXACT_LINEAGE")
            if key in by_candidate_edge_keys[forum_id]:
                continue
            by_candidate_edge_keys[forum_id].add(key)
            edges.append(
                {
                    "source_year": args.year,
                    "source_forum_id": forum_id,
                    "source_historical_decision": candidate["decision"],
                    "target_year": target["year"],
                    "target_forum_id": target["forum_id"],
                    "target_decision": target["decision"],
                    "lineage_class": "PRIMARY_EXACT_LINEAGE",
                    "title_similarity": 1.0,
                    "author_overlap_coefficient": overlap_coefficient(
                        base_authors, target["author_surnames"]
                    ),
                    "author_overlap_surnames": overlap,
                }
            )

        block_indexes: set[int] = set()
        for token in set(base_title.split()):
            if len(token) >= 4:
                block_indexes.update(token_index.get(token, ()))
        # Very short titles are rare; fall back to the full later frame rather
        # than weakening recall for the pre-frozen 0.97 sensitivity rule.
        if not block_indexes:
            block_indexes = set(range(len(later_titles)))

        for index in sorted(block_indexes):
            if index in exact_index_set:
                continue
            target = later[index]
            overlap = sorted(base_authors & target["author_surnames"])
            author_overlap = overlap_coefficient(
                base_authors, target["author_surnames"]
            )
            if not overlap or author_overlap < AUTHOR_OVERLAP_MIN:
                continue
            score = fuzz.token_set_ratio(
                base_title, target["normalized_title"]
            ) / 100.0
            if score < NEAR_TITLE_MIN:
                continue
            key = (target["forum_id"], "SENSITIVITY_NEAR_LINEAGE")
            if key in by_candidate_edge_keys[forum_id]:
                continue
            by_candidate_edge_keys[forum_id].add(key)
            edges.append(
                {
                    "source_year": args.year,
                    "source_forum_id": forum_id,
                    "source_historical_decision": candidate["decision"],
                    "target_year": target["year"],
                    "target_forum_id": target["forum_id"],
                    "target_decision": target["decision"],
                    "lineage_class": "SENSITIVITY_NEAR_LINEAGE",
                    "title_similarity": score,
                    "author_overlap_coefficient": author_overlap,
                    "author_overlap_surnames": overlap,
                }
            )

    edges.sort(
        key=lambda row: (
            row["source_forum_id"],
            row["target_year"],
            row["target_forum_id"],
            row["lineage_class"],
        )
    )

    edges_by_candidate: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in edges:
        edges_by_candidate[edge["source_forum_id"]].append(edge)

    candidate_summary: list[dict[str, Any]] = []
    for candidate in sorted(candidates, key=lambda row: str(row["forum_id"])):
        forum_id = str(candidate["forum_id"])
        candidate_edges = edges_by_candidate.get(forum_id, [])
        exact = [
            edge
            for edge in candidate_edges
            if edge["lineage_class"] == "PRIMARY_EXACT_LINEAGE"
        ]
        near = [
            edge
            for edge in candidate_edges
            if edge["lineage_class"] == "SENSITIVITY_NEAR_LINEAGE"
        ]
        any_lineage = bool(exact or near)
        exact_accept = any(edge["target_decision"] == "ACCEPT" for edge in exact)
        sensitivity_accept = any(
            edge["target_decision"] == "ACCEPT" for edge in exact + near
        )
        years = [edge["target_year"] for edge in exact + near]

        candidate_summary.append(
            {
                "forum_id": forum_id,
                "historical_decision": candidate["decision"],
                "any_exact_lineage": bool(exact),
                "any_sensitivity_lineage": bool(near),
                "any_lineage_including_sensitivity": any_lineage,
                "any_later_accept_exact_lineage": exact_accept,
                "any_later_accept_lineage_including_sensitivity":
                    sensitivity_accept,
                "exact_lineage_count": len(exact),
                "sensitivity_lineage_count": len(near),
                "first_later_lineage_year": min(years) if years else None,
            }
        )

    by_decision: dict[str, Any] = {}
    for decision in ("ACCEPT", "REJECT"):
        group = [
            row
            for row in candidate_summary
            if row["historical_decision"] == decision
        ]
        by_decision[decision] = {
            "candidate_count": len(group),
            "any_exact_lineage": summarize_boolean(
                group, "any_exact_lineage"
            ),
            "any_lineage_including_sensitivity": summarize_boolean(
                group, "any_lineage_including_sensitivity"
            ),
            "any_later_accept_exact_lineage": summarize_boolean(
                group, "any_later_accept_exact_lineage"
            ),
            "any_later_accept_lineage_including_sensitivity":
                summarize_boolean(
                    group,
                    "any_later_accept_lineage_including_sensitivity",
                ),
        }

    def difference(metric: str) -> dict[str, Any]:
        a = by_decision["ACCEPT"][metric]
        r = by_decision["REJECT"][metric]
        gap = float(a["fraction"]) - float(r["fraction"])
        ci = newcombe_difference_interval(
            int(a["count"]),
            int(a["candidate_count"]),
            int(r["count"]),
            int(r["candidate_count"]),
        )
        equivalent = bool(
            ci
            and ci[0] >= -EQUIVALENCE_MARGIN
            and ci[1] <= EQUIVALENCE_MARGIN
        )
        return {
            "accept_minus_reject_fraction": gap,
            "newcombe_wilson_ci95": list(ci) if ci else None,
            "equivalence_margin": EQUIVALENCE_MARGIN,
            "equivalent_within_5pp": equivalent,
        }

    exact_edges = [
        edge for edge in edges
        if edge["lineage_class"] == "PRIMARY_EXACT_LINEAGE"
    ]
    near_edges = [
        edge for edge in edges
        if edge["lineage_class"] == "SENSITIVITY_NEAR_LINEAGE"
    ]

    summary = {
        "schema_version": "0.1",
        "status": "OUTCOME_FREE_LINEAGE_AUDIT",
        "source_year": args.year,
        "later_year_min": LATER_YEAR_MIN,
        "later_year_max": LATER_YEAR_MAX,
        "candidate_count": len(candidate_summary),
        "later_record_count": len(later),
        "primary_exact_lineage_edge_count": len(exact_edges),
        "sensitivity_near_lineage_edge_count": len(near_edges),
        "candidate_any_exact_lineage_count": sum(
            row["any_exact_lineage"] for row in candidate_summary
        ),
        "candidate_any_lineage_including_sensitivity_count": sum(
            row["any_lineage_including_sensitivity"]
            for row in candidate_summary
        ),
        "candidate_any_later_accept_exact_lineage_count": sum(
            row["any_later_accept_exact_lineage"]
            for row in candidate_summary
        ),
        "candidate_any_later_accept_including_sensitivity_count": sum(
            row["any_later_accept_lineage_including_sensitivity"]
            for row in candidate_summary
        ),
        "by_historical_decision": by_decision,
        "decision_differences": {
            "any_exact_lineage": difference("any_exact_lineage"),
            "any_lineage_including_sensitivity": difference(
                "any_lineage_including_sensitivity"
            ),
            "any_later_accept_exact_lineage": difference(
                "any_later_accept_exact_lineage"
            ),
            "any_later_accept_lineage_including_sensitivity": difference(
                "any_later_accept_lineage_including_sensitivity"
            ),
        },
        "edge_target_year_counts": dict(
            sorted(Counter(str(edge["target_year"]) for edge in edges).items())
        ),
        "edge_target_decision_counts": dict(
            sorted(Counter(edge["target_decision"] for edge in edges).items())
        ),
        "primary_rule": {
            "normalized_title_exact": True,
            "minimum_author_surname_overlap_count": 1,
        },
        "sensitivity_rule": {
            "rapidfuzz_token_set_similarity_min": NEAR_TITLE_MIN,
            "author_overlap_coefficient_min": AUTHOR_OVERLAP_MIN,
            "minimum_author_surname_overlap_count": 1,
        },
        "inputs": {
            "candidate_jsonl_sha256": sha256_file(args.candidates),
            "metadata_parquet_sha256": sha256_file(args.metadata_parquet),
        },
        "outcomes_observed": False,
        "interpretation": (
            "Lineage is a downstream manuscript-evolution diagnostic, not "
            "epistemic value. Detected lineage narrows interpretation but does "
            "not automatically exclude a candidate."
        ),
    }

    args.out_dir.mkdir(parents=True, exist_ok=True)
    edges_path = args.out_dir / "track_a_lineage_edges.jsonl"
    candidates_path = args.out_dir / "track_a_lineage_candidates.jsonl"
    summary_path = args.out_dir / "track_a_lineage_audit.json"

    edges_path.write_text(
        "".join(canonical_line(row) for row in edges),
        encoding="utf-8",
    )
    candidates_path.write_text(
        "".join(canonical_line(row) for row in candidate_summary),
        encoding="utf-8",
    )
    summary["outputs"] = {
        "edges_jsonl_sha256": sha256_file(edges_path),
        "candidates_jsonl_sha256": sha256_file(candidates_path),
    }
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
