#!/usr/bin/env python3
"""Reconcile raw OpenAlex batch responses to the query-manifest version used.

This exists because the first feasibility run exposed an API grammar issue:
unquoted exact-title filter values containing commas were rejected. Successful
v0 batches were valid and preserved; failed batches were retried with quoted
v1 filters. The reconciler binds each retained raw response to the exact query
manifest version that produced it.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--v0-batch-manifest", type=Path, required=True)
    parser.add_argument("--v1-batch-manifest", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    v0 = {str(row["batch_id"]): row for row in load_jsonl(args.v0_batch_manifest)}
    v1 = {str(row["batch_id"]): row for row in load_jsonl(args.v1_batch_manifest)}
    if set(v0) != set(v1):
        raise RuntimeError("v0/v1 batch IDs differ")

    for batch_id in sorted(v0):
        if v0[batch_id]["forum_ids"] != v1[batch_id]["forum_ids"]:
            raise RuntimeError(f"batch membership changed: {batch_id}")

    ledger = load_jsonl(args.ledger)
    by_batch: dict[str, list[dict[str, Any]]] = {}
    for row in ledger:
        by_batch.setdefault(str(row["batch_id"]), []).append(row)

    retry_success_times: list[str] = []
    for batch_id, rows in by_batch.items():
        saw_failure = False
        for row in rows:
            if row.get("status") != "ok":
                saw_failure = True
            elif saw_failure:
                retry_success_times.append(str(row["attempted_at_utc"]))
                break

    if not retry_success_times:
        raise RuntimeError("cannot infer v1 retry transition from ledger")
    v1_transition_utc = min(retry_success_times)

    out_rows: list[dict[str, Any]] = []
    counts = {"v0_unquoted": 0, "v1_quoted": 0}

    for batch_id in sorted(v1):
        rows = by_batch.get(batch_id, [])
        successes = [row for row in rows if row.get("status") == "ok"]
        if not successes:
            raise RuntimeError(f"no successful acquisition for {batch_id}")
        success = successes[-1]
        acquired_at = str(success["attempted_at_utc"])
        source = "v0_unquoted" if acquired_at < v1_transition_utc else "v1_quoted"
        manifest_row = v0[batch_id] if source == "v0_unquoted" else v1[batch_id]
        raw_path = args.raw_dir / f"{batch_id}.json.gz"
        if not raw_path.exists():
            raise RuntimeError(f"missing raw file: {raw_path}")
        counts[source] += 1
        query_filter = str(manifest_row["query"]["filter"])

        out_rows.append(
            {
                "batch_id": batch_id,
                "forum_ids": manifest_row["forum_ids"],
                "candidate_count": int(manifest_row["candidate_count"]),
                "source_query_manifest_version": source,
                "acquired_at_utc": acquired_at,
                "query_filter_sha256": sha256_bytes(
                    query_filter.encode("utf-8")
                ),
                "raw_sha256": sha256_file(raw_path),
                "provider_result_count": int(
                    success.get("provider_result_count") or 0
                ),
                "cost_usd": float(success.get("cost_usd") or 0.0),
            }
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(canonical_line(row) for row in out_rows),
        encoding="utf-8",
    )
    summary = {
        "schema_version": "0.1",
        "status": "RECONCILED_BATCH_RAW_PROVENANCE",
        "v1_transition_utc": v1_transition_utc,
        "batch_count": len(out_rows),
        "source_version_counts": counts,
        "v0_batch_manifest_sha256": sha256_file(args.v0_batch_manifest),
        "v1_batch_manifest_sha256": sha256_file(args.v1_batch_manifest),
        "ledger_sha256": sha256_file(args.ledger),
        "provenance_jsonl_sha256": sha256_file(args.out),
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
