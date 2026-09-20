#!/usr/bin/env python3
"""Acquire frozen C5 citation outcomes efficiently after the broader gate.

This is the preferred post-gate acquisition path. It batches up to 100
OpenAlex work IDs in a single cites-filter request, attributes each citing work
back to the cited identity-cluster member via referenced_works, and writes the
same per-candidate FROZEN_C5_OUTCOME artefacts consumed by the frozen evaluator.

The script fails closed unless the broader pre-outcome adjudication explicitly
authorizes citation acquisition.
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
from collections import defaultdict
from pathlib import Path
from typing import Any

USER_AGENT = "AgalmicResearch-AttentionAllocation/0.10"
WINDOW_START = "2019-09-26"
WINDOW_END = "2024-09-25"
DEFAULT_MAX_TOTAL_COST_USD = 0.09
ESTIMATED_FILTER_COST_USD = 0.0001
MAX_OPENALEX_OR_VALUES = 100


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


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


def write_gzip_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".part")
    with gzip.open(tmp, "wt", encoding="utf-8", compresslevel=6) as f:
        json.dump(payload, f, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    tmp.replace(path)


def load_gzip_json(path: Path) -> Any:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def append_ledger(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")
        f.flush()
        os.fsync(f.fileno())


def openalex_work_token(value: str) -> str:
    token = value.rstrip("/").split("/")[-1]
    if not token.startswith("W"):
        raise ValueError(f"unexpected OpenAlex work id: {value}")
    return token


def batched(values: list[str], size: int) -> list[list[str]]:
    return [values[i : i + size] for i in range(0, len(values), size)]


def build_url(work_ids: list[str], cursor: str) -> str:
    if not work_ids or len(work_ids) > MAX_OPENALEX_OR_VALUES:
        raise ValueError("invalid OpenAlex cites batch size")
    params = {
        "filter": (
            "cites:"
            + "|".join(work_ids)
            + f",from_publication_date:{WINDOW_START}"
            + f",to_publication_date:{WINDOW_END}"
        ),
        "select": "id,publication_date,referenced_works",
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


def completed_batches(
    ledger_rows: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in ledger_rows:
        if row.get("status") == "ok":
            out[str(row["batch_id"])] = row
    return out


def attribute_page_results(
    results: list[dict[str, Any]],
    target_set: set[str],
    work_to_candidate: dict[str, str],
) -> dict[str, dict[str, str]]:
    attributed: dict[str, dict[str, str]] = defaultdict(dict)
    for result in results:
        citing_id = str(result.get("id") or "")
        publication_date = str(result.get("publication_date") or "")
        if not citing_id or not publication_date:
            continue
        if not (WINDOW_START <= publication_date <= WINDOW_END):
            raise RuntimeError(
                "provider returned a citing work outside "
                "the frozen publication-date window"
            )
        referenced = {
            openalex_work_token(str(value))
            for value in result.get("referenced_works") or []
            if str(value).rstrip("/").split("/")[-1].startswith("W")
        }
        for target in referenced & target_set:
            forum_id = work_to_candidate[target]
            attributed[forum_id][citing_id] = publication_date
    return attributed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--adjudication", type=Path, required=True)
    parser.add_argument("--frozen-cohort", type=Path, required=True)
    parser.add_argument("--identity-jsonl", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument(
        "--max-total-cost-usd",
        type=float,
        default=DEFAULT_MAX_TOTAL_COST_USD,
    )
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--min-interval", type=float, default=0.25)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    adjudication = json.loads(args.adjudication.read_text())
    if adjudication.get("outcomes_observed") is not False:
        raise SystemExit("adjudication is not outcome-blind")
    if adjudication.get("citation_outcome_acquisition_authorized") is not True:
        raise SystemExit(
            "citation acquisition is not authorized by the broader "
            "pre-outcome adjudication"
        )
    if adjudication.get("verdict") not in {
        "PASS_PRE_OUTCOME",
        "CONDITIONAL_PASS_PRE_OUTCOME",
    }:
        raise SystemExit(
            f"unexpected authorizing verdict: {adjudication.get('verdict')}"
        )
    if not (1 <= args.batch_size <= MAX_OPENALEX_OR_VALUES):
        raise SystemExit("--batch-size must be in [1, 100]")
    if args.max_total_cost_usd <= 0:
        raise SystemExit("--max-total-cost-usd must be positive")
    if args.min_interval < 0.1:
        raise SystemExit("--min-interval cannot be below 0.1 seconds")

    cohort_rows = load_jsonl(args.frozen_cohort)
    cohort_ids = {str(row["forum_id"]) for row in cohort_rows}
    if len(cohort_ids) != len(cohort_rows):
        raise RuntimeError("duplicate forum IDs in frozen cohort")

    identity_rows_all = load_jsonl(args.identity_jsonl)
    identity_rows = [
        row
        for row in identity_rows_all
        if str(row["forum_id"]) in cohort_ids
        and row.get("status") == "MATCHED_PRIMARY_IDENTITY_CLUSTER"
    ]
    identity_rows.sort(key=lambda row: str(row["forum_id"]))

    candidate_to_work_ids: dict[str, list[str]] = {}
    work_to_candidate: dict[str, str] = {}

    for row in identity_rows:
        forum_id = str(row["forum_id"])
        tokens = sorted(
            {
                openalex_work_token(str(member["openalex_id"]))
                for member in row.get("identity_cluster") or []
            }
        )
        if not tokens:
            raise RuntimeError(f"matched identity has no work IDs: {forum_id}")
        candidate_to_work_ids[forum_id] = tokens
        for token in tokens:
            prior = work_to_candidate.get(token)
            if prior is not None and prior != forum_id:
                raise RuntimeError(
                    "OpenAlex work identity is shared across frozen candidates: "
                    f"{token}: {prior}, {forum_id}"
                )
            work_to_candidate[token] = forum_id

    work_ids = sorted(work_to_candidate)
    batches = batched(work_ids, args.batch_size)
    if not batches:
        raise RuntimeError("no matched identities in frozen cohort")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = args.out_dir / "citation_batch_raw"
    batch_outcome_dir = args.out_dir / "citation_batch_outcomes"
    candidate_outcome_dir = args.out_dir / "candidate_outcomes"
    ledger_path = args.out_dir / "citation_batch_acquisition.jsonl"
    manifest_path = args.out_dir / "citation_acquisition_manifest.json"

    ledger_rows = load_jsonl(ledger_path) if ledger_path.exists() else []
    done = completed_batches(ledger_rows)
    prior_cost = sum(
        float(row.get("cost_usd") or 0.0)
        for row in ledger_rows
    )
    api_key = os.environ.get("OPENALEX_API_KEY") or None

    candidate_citing: dict[str, dict[str, str]] = defaultdict(dict)
    batch_records: list[dict[str, Any]] = []
    spent_this_run = 0.0
    network_attempts_this_run = 0
    successful_pages_this_run = 0
    stop_reason: str | None = None
    last_request = 0.0

    for batch_index, target_work_ids in enumerate(batches, 1):
        batch_id = f"batch-{batch_index:04d}"
        target_hash = sha256_text("|".join(target_work_ids))
        batch_output = batch_outcome_dir / f"{batch_id}.json.gz"

        prior = done.get(batch_id)
        if prior is not None:
            if prior.get("target_work_ids_sha256") != target_hash:
                raise RuntimeError(
                    f"completed batch membership drift: {batch_id}"
                )
            if not batch_output.exists():
                raise RuntimeError(
                    f"completed ledger batch missing outcome file: {batch_id}"
                )
            saved = load_gzip_json(batch_output)
            for forum_id, citing in saved["candidate_citing_works"].items():
                for item in citing:
                    candidate_citing[forum_id][
                        str(item["openalex_id"])
                    ] = str(item["publication_date"])
            batch_records.append(prior)
            continue

        batch_spent = 0.0
        batch_network_attempts = 0
        page = 0
        cursor = "*"
        candidate_batch_citing: dict[str, dict[str, str]] = defaultdict(dict)
        failed: dict[str, Any] | None = None

        while cursor:
            if (
                prior_cost
                + spent_this_run
                + ESTIMATED_FILTER_COST_USD
                > args.max_total_cost_usd + 1e-12
            ):
                stop_reason = "CONFIGURED_TOTAL_COST_CAP_REACHED"
                failed = {"reason": stop_reason}
                break

            wait = args.min_interval - (
                time.monotonic() - last_request
            )
            if wait > 0:
                time.sleep(wait)
            last_request = time.monotonic()

            url = build_url(target_work_ids, cursor)
            try:
                network_attempts_this_run += 1
                batch_network_attempts += 1
                payload = request_json(url, api_key, args.timeout)
                successful_pages_this_run += 1
                cost = float(
                    payload.get("meta", {}).get("cost_usd") or 0.0
                )
                batch_spent += cost
                spent_this_run += cost
                page += 1

                raw_path = (
                    raw_dir
                    / batch_id
                    / f"page-{page:04d}.json.gz"
                )
                write_gzip_json(raw_path, payload)

                target_set = set(target_work_ids)
                attributed = attribute_page_results(
                    payload.get("results") or [],
                    target_set,
                    work_to_candidate,
                )
                for forum_id, citing in attributed.items():
                    candidate_batch_citing[forum_id].update(citing)

                next_cursor = payload.get("meta", {}).get("next_cursor")
                cursor = str(next_cursor) if next_cursor else ""
            except urllib.error.HTTPError as exc:
                body = exc.read(1000).decode(
                    "utf-8", errors="replace"
                )
                failed = {
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
                failed = {
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
                break

        record: dict[str, Any] = {
            "batch_id": batch_id,
            "status": "error" if failed else "ok",
            "attempted_at_utc": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
            ),
            "target_work_id_count": len(target_work_ids),
            "target_work_ids_sha256": target_hash,
            "page_count": page,
            "network_attempt_count": batch_network_attempts,
            "cost_usd": round(batch_spent, 6),
            "api_key_present": bool(api_key),
        }

        if failed:
            record["error"] = failed
            append_ledger(ledger_path, record)
            batch_records.append(record)
            if stop_reason:
                break
            raise RuntimeError(
                f"citation batch failed without resumable stop: "
                f"{batch_id}: {failed}"
            )

        saved_payload = {
            "schema_version": "0.1",
            "status": "FROZEN_C5_BATCH_OUTCOME",
            "batch_id": batch_id,
            "target_work_ids": target_work_ids,
            "window_start": WINDOW_START,
            "window_end": WINDOW_END,
            "candidate_citing_works": {
                forum_id: [
                    {
                        "openalex_id": citing_id,
                        "publication_date": citing[citing_id],
                    }
                    for citing_id in sorted(citing)
                ]
                for forum_id, citing in sorted(
                    candidate_batch_citing.items()
                )
            },
        }
        write_gzip_json(batch_output, saved_payload)
        record["batch_outcome_sha256"] = sha256_file(batch_output)
        append_ledger(ledger_path, record)
        done[batch_id] = record
        batch_records.append(record)

        for forum_id, citing in candidate_batch_citing.items():
            candidate_citing[forum_id].update(citing)

        print(
            f"[{batch_index}/{len(batches)}] ok {batch_id} "
            f"targets={len(target_work_ids)} pages={page} "
            f"cost_usd={batch_spent:.4f}",
            flush=True,
        )

    completed_batch_ids = {
        str(row["batch_id"])
        for row in load_jsonl(ledger_path)
        if row.get("status") == "ok"
    }
    acquisition_complete = len(completed_batch_ids) == len(batches)

    final_ledger_rows = load_jsonl(ledger_path)
    total_recorded_cost = sum(
        float(row.get("cost_usd") or 0.0)
        for row in final_ledger_rows
    )
    total_network_attempts = sum(
        int(row.get("network_attempt_count") or 0)
        for row in final_ledger_rows
    )
    total_successful_pages = sum(
        int(row.get("page_count") or 0)
        for row in final_ledger_rows
        if int(row.get("page_count") or 0) > 0
    )

    if acquisition_complete:
        candidate_outcome_dir.mkdir(parents=True, exist_ok=True)
        for forum_id in sorted(candidate_to_work_ids):
            citing = candidate_citing.get(forum_id, {})
            items = [
                {
                    "openalex_id": citing_id,
                    "publication_date": citing[citing_id],
                }
                for citing_id in sorted(citing)
            ]
            years = sorted(
                {int(item["publication_date"][:4]) for item in items}
            )
            payload = {
                "schema_version": "0.2",
                "status": "FROZEN_C5_OUTCOME",
                "forum_id": forum_id,
                "identity_work_ids": [
                    f"https://openalex.org/{token}"
                    for token in candidate_to_work_ids[forum_id]
                ],
                "window_start": WINDOW_START,
                "window_end": WINDOW_END,
                "c5_count": len(items),
                "citation_years": years,
                "citation_year_breadth": len(years),
                "citing_works": items,
            }
            write_gzip_json(
                candidate_outcome_dir / f"{forum_id}.json.gz",
                payload,
            )

    manifest = {
        "schema_version": "0.2",
        "status": (
            "FROZEN_C5_ACQUISITION_COMPLETE"
            if acquisition_complete
            else "PARTIAL_CITATION_ACQUISITION"
        ),
        "gate_verdict": adjudication["verdict"],
        "citation_outcome_acquisition_authorized": True,
        "network_activity_started": total_network_attempts > 0,
        "outcomes_observed": total_successful_pages > 0,
        "frozen_cohort_count": len(cohort_ids),
        "matched_candidate_count": len(candidate_to_work_ids),
        "unique_identity_work_count": len(work_ids),
        "batch_size": args.batch_size,
        "batch_count": len(batches),
        "completed_batch_count": len(completed_batch_ids),
        "window_start": WINDOW_START,
        "window_end": WINDOW_END,
        "prior_recorded_cost_usd": round(prior_cost, 6),
        "spent_usd_this_run": round(spent_this_run, 6),
        "network_attempts_this_run": network_attempts_this_run,
        "successful_pages_this_run": successful_pages_this_run,
        "total_network_attempts": total_network_attempts,
        "total_successful_pages": total_successful_pages,
        "recorded_total_cost_usd": round(total_recorded_cost, 6),
        "configured_max_total_cost_usd": args.max_total_cost_usd,
        "api_key_present": bool(api_key),
        "stop_reason": stop_reason,
        "inputs": {
            "adjudication_sha256": sha256_file(args.adjudication),
            "frozen_cohort_sha256": sha256_file(args.frozen_cohort),
            "identity_jsonl_sha256": sha256_file(args.identity_jsonl),
        },
    }
    if acquisition_complete:
        manifest["candidate_outcome_count"] = len(
            list(candidate_outcome_dir.glob("*.json.gz"))
        )
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
