#!/usr/bin/env python3
"""Acquire frozen five-year OpenAlex citation outcomes after the feasibility gate.

For each primary identity cluster, query every cluster member for citing works
inside the preregistered publication-date window, union citing work IDs across
cluster members, and deduplicate before computing C5.

This script refuses to run unless --post-feasibility-gate is supplied.
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
WINDOW_START = "2019-09-26"
WINDOW_END = "2024-09-25"
DEFAULT_MAX_COST_USD = 0.95
ESTIMATED_FILTER_COST_USD = 0.0001


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


def openalex_work_id(value: str) -> str:
    token = value.rstrip("/").split("/")[-1]
    if not token.startswith("W"):
        raise ValueError(f"unexpected OpenAlex work id: {value}")
    return token


def build_url(work_id: str, cursor: str) -> str:
    params = {
        "filter": (
            f"cites:{work_id},"
            f"from_publication_date:{WINDOW_START},"
            f"to_publication_date:{WINDOW_END}"
        ),
        "select": "id,publication_date",
        "per_page": "100",
        "cursor": cursor,
    }
    return (
        "https://api.openalex.org/works?"
        + urllib.parse.urlencode(params)
    )


def request_json(
    url: str,
    api_key: str | None,
    timeout: float,
) -> dict[str, Any]:
    headers = {"User-Agent": USER_AGENT}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--identity-jsonl", type=Path, required=True)
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
            "Citation outcome acquisition is gated. Run only after the "
            "Track A feasibility gate has explicitly passed."
        )
    if args.max_cost_usd <= 0:
        raise SystemExit("--max-cost-usd must be positive")
    if args.min_interval < 0.1:
        raise SystemExit("--min-interval cannot be below 0.1 seconds")

    api_key = os.environ.get("OPENALEX_API_KEY") or None
    rows = [
        row
        for row in load_jsonl(args.identity_jsonl)
        if row.get("status") == "MATCHED_PRIMARY_IDENTITY_CLUSTER"
    ]
    rows.sort(key=lambda row: str(row["forum_id"]))
    if args.limit > 0:
        rows = rows[: args.limit]

    raw_dir = args.out_dir / "citation_raw"
    outcome_dir = args.out_dir / "candidate_outcomes"
    ledger_path = args.out_dir / "citation_acquisition.jsonl"
    ledger = load_latest_ledger(ledger_path)

    spent = 0.0
    completed = skipped = failed = 0
    stop_reason: str | None = None
    last_request = 0.0

    for index, row in enumerate(rows, 1):
        forum_id = str(row["forum_id"])
        target = outcome_dir / f"{forum_id}.json.gz"
        prior = ledger.get(forum_id)
        if prior and prior.get("status") == "ok" and target.exists():
            skipped += 1
            continue

        citing: dict[str, str] = {}
        member_pages: dict[str, int] = {}
        member_counts: dict[str, int] = {}
        candidate_failed = False
        candidate_error: dict[str, Any] | None = None

        for member in row["identity_cluster"]:
            work_id = openalex_work_id(str(member["openalex_id"]))
            cursor = "*"
            page_number = 0
            member_seen: set[str] = set()

            while cursor:
                if (
                    spent + ESTIMATED_FILTER_COST_USD
                    > args.max_cost_usd + 1e-12
                ):
                    stop_reason = "CONFIGURED_COST_CAP_REACHED"
                    candidate_failed = True
                    candidate_error = {"reason": stop_reason}
                    break

                wait = args.min_interval - (
                    time.monotonic() - last_request
                )
                if wait > 0:
                    time.sleep(wait)
                last_request = time.monotonic()

                url = build_url(work_id, cursor)
                try:
                    payload = request_json(
                        url, api_key, args.timeout
                    )
                    call_cost = float(
                        payload.get("meta", {}).get("cost_usd") or 0.0
                    )
                    spent += call_cost
                    page_number += 1
                    raw_path = (
                        raw_dir
                        / forum_id
                        / work_id
                        / f"page-{page_number:04d}.json.gz"
                    )
                    write_gzip_json(raw_path, payload)

                    for result in payload.get("results") or []:
                        citing_id = str(result.get("id") or "")
                        publication_date = result.get("publication_date")
                        if not citing_id or not publication_date:
                            continue
                        if not (
                            WINDOW_START
                            <= str(publication_date)
                            <= WINDOW_END
                        ):
                            raise RuntimeError(
                                "provider returned citation outside "
                                "preregistered date window"
                            )
                        member_seen.add(citing_id)
                        citing[citing_id] = str(publication_date)

                    next_cursor = payload.get("meta", {}).get(
                        "next_cursor"
                    )
                    cursor = str(next_cursor) if next_cursor else ""
                except urllib.error.HTTPError as exc:
                    body = exc.read(1000).decode(
                        "utf-8", errors="replace"
                    )
                    candidate_failed = True
                    candidate_error = {
                        "work_id": work_id,
                        "http_status": exc.code,
                        "error_body_prefix": body,
                    }
                    if exc.code == 429:
                        stop_reason = (
                            "PROVIDER_RATE_OR_DAILY_BUDGET_LIMIT"
                        )
                    elif exc.code in {401, 403}:
                        stop_reason = (
                            "PROVIDER_AUTH_OR_ACCESS_CONTROL"
                        )
                    break
                except Exception as exc:
                    candidate_failed = True
                    candidate_error = {
                        "work_id": work_id,
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                    }
                    break

            member_pages[work_id] = page_number
            member_counts[work_id] = len(member_seen)
            if candidate_failed:
                break

        record: dict[str, Any] = {
            "forum_id": forum_id,
            "identity_cluster_size": len(row["identity_cluster"]),
            "identity_work_ids": [
                str(member["openalex_id"])
                for member in row["identity_cluster"]
            ],
            "window_start": WINDOW_START,
            "window_end": WINDOW_END,
            "attempted_at_utc": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
            ),
            "member_pages": member_pages,
            "member_raw_citation_counts": member_counts,
        }

        if candidate_failed:
            record.update(
                {
                    "status": "error",
                    "error": candidate_error,
                }
            )
            append_ledger(ledger_path, record)
            ledger[forum_id] = record
            failed += 1
            if stop_reason:
                break
            print(
                f"[{index}/{len(rows)}] FAILED {forum_id}",
                flush=True,
            )
            continue

        sorted_citing = [
            {
                "openalex_id": citing_id,
                "publication_date": citing[citing_id],
            }
            for citing_id in sorted(citing)
        ]
        years = sorted(
            {
                int(item["publication_date"][:4])
                for item in sorted_citing
            }
        )
        outcome = {
            "schema_version": "0.1",
            "status": "FROZEN_C5_OUTCOME",
            "forum_id": forum_id,
            "identity_work_ids": record["identity_work_ids"],
            "window_start": WINDOW_START,
            "window_end": WINDOW_END,
            "c5_count": len(sorted_citing),
            "citation_years": years,
            "citation_year_breadth": len(years),
            "citing_works": sorted_citing,
        }
        write_gzip_json(target, outcome)
        record.update(
            {
                "status": "ok",
                "c5_count": len(sorted_citing),
                "outcome_raw_sha256": sha256_file(target),
            }
        )
        append_ledger(ledger_path, record)
        ledger[forum_id] = record
        completed += 1
        print(
            f"[{index}/{len(rows)}] ok {forum_id} "
            f"C5={len(sorted_citing)}",
            flush=True,
        )

    print(
        json.dumps(
            {
                "matched_candidates_selected": len(rows),
                "completed_this_run": completed,
                "skipped_existing": skipped,
                "failed_this_run": failed,
                "spent_usd_this_run": round(spent, 6),
                "configured_max_cost_usd": args.max_cost_usd,
                "api_key_present": bool(api_key),
                "stop_reason": stop_reason,
                "ledger": str(ledger_path),
                "outcome_dir": str(outcome_dir),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
