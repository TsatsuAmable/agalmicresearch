#!/usr/bin/env python3
"""Acquire OpenAlex metadata for frozen linkage queries.

This script is deliberately hard-gated because OpenAlex is evaluation-only.
It fetches only identity metadata (no citation fields), stores raw responses,
tracks request cost, and stops rather than exceeding the configured spend cap
or attempting to route around provider limits.
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

USER_AGENT = "AgalmicResearch-AttentionAllocation/0.4"
DEFAULT_MAX_COST_USD = 0.95
ESTIMATED_SEARCH_COST_USD = 0.001


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


def load_latest_ledger(path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        out[str(row["forum_id"])] = row
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


def build_url(query: dict[str, Any]) -> str:
    endpoint = str(query["endpoint"])
    params = {
        "filter": str(query["filter"]),
        "select": str(query["select"]),
        "per_page": str(query.get("per_page", 25)),
    }
    return endpoint + "?" + urllib.parse.urlencode(params)


def request_json(
    url: str,
    api_key: str | None,
    timeout: float,
) -> tuple[dict[str, Any], dict[str, str]]:
    headers = {"User-Agent": USER_AGENT}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read()
        payload = json.loads(body)
        response_headers = {
            "x_rate_limit_limit": resp.headers.get("X-RateLimit-Limit", ""),
            "x_rate_limit_remaining": resp.headers.get(
                "X-RateLimit-Remaining", ""
            ),
            "x_rate_limit_credits_used": resp.headers.get(
                "X-RateLimit-Credits-Used", ""
            ),
            "x_rate_limit_reset": resp.headers.get("X-RateLimit-Reset", ""),
        }
        return payload, response_headers


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query-manifest", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--post-feasibility-gate", action="store_true")
    parser.add_argument(
        "--max-cost-usd",
        type=float,
        default=DEFAULT_MAX_COST_USD,
    )
    parser.add_argument("--min-interval", type=float, default=0.25)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    if not args.post_feasibility_gate:
        raise SystemExit(
            "OpenAlex linkage acquisition is gated. Re-run only after the "
            "Track A feasibility gate has explicitly passed."
        )
    if args.max_cost_usd <= 0:
        raise SystemExit("--max-cost-usd must be positive")
    if args.min_interval < 0.1:
        raise SystemExit("--min-interval cannot be below 0.1 seconds")

    api_key = os.environ.get("OPENALEX_API_KEY") or None
    rows = load_jsonl(args.query_manifest)
    if args.limit > 0:
        rows = rows[: args.limit]

    raw_dir = args.out_dir / "metadata_raw"
    ledger_path = args.out_dir / "metadata_acquisition.jsonl"
    ledger = load_latest_ledger(ledger_path)

    spent = 0.0
    completed = skipped = failed = 0
    stop_reason: str | None = None
    last_request = 0.0

    for index, row in enumerate(rows, 1):
        forum_id = str(row["forum_id"])
        target = raw_dir / f"{forum_id}.json.gz"
        prior = ledger.get(forum_id)
        if prior and prior.get("status") == "ok" and target.exists():
            skipped += 1
            continue

        if (
            spent + ESTIMATED_SEARCH_COST_USD
            > args.max_cost_usd + 1e-12
        ):
            stop_reason = "CONFIGURED_COST_CAP_REACHED"
            break

        wait = args.min_interval - (time.monotonic() - last_request)
        if wait > 0:
            time.sleep(wait)
        last_request = time.monotonic()

        url = build_url(row["query"])
        record: dict[str, Any] = {
            "forum_id": forum_id,
            "status": "attempted",
            "attempted_at_utc": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
            ),
            "api_key_present": bool(api_key),
            "query_filter": row["query"]["filter"],
        }

        try:
            payload, rate_headers = request_json(
                url, api_key, args.timeout
            )
            call_cost = float(payload.get("meta", {}).get("cost_usd") or 0.0)
            spent += call_cost
            write_gzip_json(target, payload)
            record.update(
                {
                    "status": "ok",
                    "cost_usd": call_cost,
                    "result_count": int(
                        payload.get("meta", {}).get("count") or 0
                    ),
                    "raw_sha256": sha256_file(target),
                    "rate_limit": rate_headers,
                }
            )
            append_ledger(ledger_path, record)
            ledger[forum_id] = record
            completed += 1
            print(
                f"[{index}/{len(rows)}] ok {forum_id} "
                f"results={record['result_count']} "
                f"cost_usd={call_cost:.4f}",
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
            ledger[forum_id] = record
            failed += 1
            if exc.code == 429:
                stop_reason = "PROVIDER_RATE_OR_DAILY_BUDGET_LIMIT"
                break
            if exc.code in {401, 403}:
                stop_reason = "PROVIDER_AUTH_OR_ACCESS_CONTROL"
                break
            print(
                f"[{index}/{len(rows)}] HTTP {exc.code} {forum_id}",
                flush=True,
            )
        except Exception as exc:
            record.update(
                {
                    "status": "error",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
            append_ledger(ledger_path, record)
            ledger[forum_id] = record
            failed += 1
            print(
                f"[{index}/{len(rows)}] FAILED {forum_id}: "
                f"{type(exc).__name__}: {exc}",
                flush=True,
            )

    summary = {
        "selected_queries": len(rows),
        "completed_this_run": completed,
        "skipped_existing": skipped,
        "failed_this_run": failed,
        "spent_usd_this_run": round(spent, 6),
        "configured_max_cost_usd": args.max_cost_usd,
        "api_key_present": bool(api_key),
        "stop_reason": stop_reason,
        "ledger": str(ledger_path),
        "raw_dir": str(raw_dir),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
