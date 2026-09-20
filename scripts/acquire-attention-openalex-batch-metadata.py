#!/usr/bin/env python3
"""Acquire batched OpenAlex identity metadata for feasibility analysis only.

This script never requests citation outcomes. It uses OR-batched exact-title
filters, stores raw responses, tracks API budget, and stops on provider limits.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

USER_AGENT = "AgalmicResearch-AttentionAllocation/0.6"
DEFAULT_MAX_TOTAL_COST_USD = 0.09


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


def load_all_ledger(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return load_jsonl(path)


def latest_by_batch(
    rows: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        out[str(row["batch_id"])] = row
    return out


def append_ledger(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")
        f.flush()
        os.fsync(f.fileno())


def write_gzip_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".part")
    with gzip.open(tmp, "wt", encoding="utf-8", compresslevel=6) as f:
        json.dump(payload, f, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    tmp.replace(path)


def request_json(
    batch: dict[str, Any],
    api_key: str | None,
    timeout: float,
) -> tuple[dict[str, Any], dict[str, str]]:
    q = batch["query"]
    params = {
        "filter": str(q["filter"]),
        "select": str(q["select"]),
        "per_page": str(q.get("per_page", 100)),
    }
    url = str(q["endpoint"]) + "?" + urllib.parse.urlencode(params)
    headers = {"User-Agent": USER_AGENT}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read())
        rate = {
            "x_rate_limit_limit": resp.headers.get("X-RateLimit-Limit", ""),
            "x_rate_limit_remaining": resp.headers.get(
                "X-RateLimit-Remaining", ""
            ),
            "x_rate_limit_credits_used": resp.headers.get(
                "X-RateLimit-Credits-Used", ""
            ),
            "x_rate_limit_reset": resp.headers.get("X-RateLimit-Reset", ""),
        }
        return payload, rate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-query-manifest", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--identity-feasibility", action="store_true")
    parser.add_argument(
        "--max-total-cost-usd",
        type=float,
        default=DEFAULT_MAX_TOTAL_COST_USD,
    )
    parser.add_argument("--min-interval", type=float, default=0.25)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    if not args.identity_feasibility:
        raise SystemExit(
            "Identity metadata acquisition is feasibility-only. "
            "Use --identity-feasibility explicitly."
        )
    if args.max_total_cost_usd <= 0:
        raise SystemExit("--max-total-cost-usd must be positive")
    if args.min_interval < 0.1:
        raise SystemExit("--min-interval cannot be below 0.1 seconds")

    api_key = os.environ.get("OPENALEX_API_KEY") or None
    batches = load_jsonl(args.batch_query_manifest)

    raw_dir = args.out_dir / "batch_raw"
    ledger_path = args.out_dir / "batch_metadata_acquisition.jsonl"
    ledger_rows = load_all_ledger(ledger_path)
    latest = latest_by_batch(ledger_rows)
    prior_spent = sum(
        float(row.get("cost_usd") or 0.0)
        for row in ledger_rows
        if row.get("status") == "ok"
    )

    completed = skipped = failed = 0
    spent_this_run = 0.0
    stop_reason: str | None = None
    last_request = 0.0

    for index, batch in enumerate(batches, 1):
        batch_id = str(batch["batch_id"])
        target = raw_dir / f"{batch_id}.json.gz"
        prior = latest.get(batch_id)
        if prior and prior.get("status") == "ok" and target.exists():
            skipped += 1
            continue

        # Search-style title filters currently report ~0.001 USD/call.
        # Reserve that amount before each request so retries cannot silently
        # exceed the configured total cap.
        if prior_spent + spent_this_run + 0.001 > args.max_total_cost_usd:
            stop_reason = "CONFIGURED_TOTAL_COST_CAP_REACHED"
            break

        wait = args.min_interval - (time.monotonic() - last_request)
        if wait > 0:
            time.sleep(wait)
        last_request = time.monotonic()

        query_filter = str(batch["query"]["filter"])
        record: dict[str, Any] = {
            "batch_id": batch_id,
            "candidate_count": int(batch["candidate_count"]),
            "forum_ids": batch["forum_ids"],
            "query_filter_sha256": hashlib.sha256(
                query_filter.encode("utf-8")
            ).hexdigest(),
            "attempted_at_utc": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
            ),
            "api_key_present": bool(api_key),
        }

        try:
            payload, rate = request_json(
                batch, api_key, args.timeout
            )
            count = int(payload.get("meta", {}).get("count") or 0)
            if count > 100:
                record.update(
                    {
                        "status": "requires_rebatch",
                        "provider_result_count": count,
                        "reason": (
                            "result count exceeds per_page=100; rebatch "
                            "rather than silently truncate identity metadata"
                        ),
                    }
                )
                append_ledger(ledger_path, record)
                latest[batch_id] = record
                failed += 1
                stop_reason = "BATCH_RESULT_COUNT_EXCEEDS_100"
                break

            cost = float(payload.get("meta", {}).get("cost_usd") or 0.0)
            spent_this_run += cost
            write_gzip_json(target, payload)
            record.update(
                {
                    "status": "ok",
                    "cost_usd": cost,
                    "provider_result_count": count,
                    "raw_sha256": sha256_file(target),
                    "rate_limit": rate,
                }
            )
            append_ledger(ledger_path, record)
            latest[batch_id] = record
            completed += 1
            print(
                f"[{index}/{len(batches)}] ok {batch_id} "
                f"candidates={batch['candidate_count']} "
                f"results={count} cost_usd={cost:.4f}",
                flush=True,
            )
        except urllib.error.HTTPError as exc:
            body = exc.read(1000).decode("utf-8", errors="replace")
            record.update(
                {
                    "status": "http_error",
                    "http_status": exc.code,
                    "error_body_prefix": body,
                }
            )
            append_ledger(ledger_path, record)
            latest[batch_id] = record
            failed += 1
            print(
                f"[{index}/{len(batches)}] HTTP {exc.code} {batch_id}",
                flush=True,
            )
            if exc.code == 429:
                stop_reason = "PROVIDER_RATE_OR_DAILY_BUDGET_LIMIT"
                break
            if exc.code in {401, 403}:
                stop_reason = "PROVIDER_AUTH_OR_ACCESS_CONTROL"
                break
        except Exception as exc:
            record.update(
                {
                    "status": "error",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
            append_ledger(ledger_path, record)
            latest[batch_id] = record
            failed += 1
            print(
                f"[{index}/{len(batches)}] FAILED {batch_id}: "
                f"{type(exc).__name__}: {exc}",
                flush=True,
            )

    summary = {
        "schema_version": "0.1",
        "status": "IDENTITY_METADATA_ONLY_NO_CITATION_OUTCOMES",
        "batch_count": len(batches),
        "completed_this_run": completed,
        "skipped_existing": skipped,
        "failed_this_run": failed,
        "prior_recorded_cost_usd": round(prior_spent, 6),
        "spent_usd_this_run": round(spent_this_run, 6),
        "recorded_total_cost_usd": round(
            prior_spent + spent_this_run, 6
        ),
        "configured_max_total_cost_usd": args.max_total_cost_usd,
        "api_key_present": bool(api_key),
        "stop_reason": stop_reason,
        "outcomes_observed": False,
        "ledger": str(ledger_path),
        "raw_dir": str(raw_dir),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
