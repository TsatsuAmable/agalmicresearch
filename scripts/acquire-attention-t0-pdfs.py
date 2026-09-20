#!/usr/bin/env python3
"""Conservatively acquire T0 historical OpenReview PDFs.

Input must be the audited t0_revision_reference_candidates.jsonl file.
The downloader is resumable, rate-limited, hashes every PDF, and records
failures without weakening source controls.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

MIN_INTERVAL_SECONDS = 5.0
USER_AGENT = "AgalmicResearch-AttentionAllocation/0.2"
MAX_BYTES_DEFAULT = 100 * 1024 * 1024


def load_candidates(path: Path, year: int) -> list[dict]:
    rows = [
        json.loads(line)
        for line in path.read_text().splitlines()
        if line.strip()
    ]
    return [row for row in rows if int(row["year"]) == year]


def load_ledger(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        out[row["revision_openreview_id"]] = row
    return out


def append_ledger(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")
        f.flush()
        os.fsync(f.fileno())


def retry_after_seconds(headers, fallback: float) -> float:
    value = headers.get("Retry-After") if headers else None
    try:
        return max(fallback, float(value))
    except (TypeError, ValueError):
        return fallback


def download_one(url: str, target: Path, max_bytes: int) -> tuple[str, int]:
    tmp = target.with_suffix(target.suffix + ".part")
    h = hashlib.sha256()
    size = 0
    first = b""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp, tmp.open("wb") as f:
        content_type = resp.headers.get("Content-Type", "")
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            if not first:
                first = chunk[:8]
            size += len(chunk)
            if size > max_bytes:
                raise RuntimeError(f"PDF exceeded max bytes: {size} > {max_bytes}")
            h.update(chunk)
            f.write(chunk)
        f.flush()
        os.fsync(f.fileno())
    if not first.startswith(b"%PDF"):
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"not a PDF; first bytes={first!r}")
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp.replace(target)
    return h.hexdigest(), size


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--candidates",
        type=Path,
        default=Path(
            "research/attention_allocation/t0/"
            "t0_revision_reference_candidates.jsonl"
        ),
    )
    parser.add_argument("--year", type=int, default=2020)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--min-interval", type=float, default=MIN_INTERVAL_SECONDS)
    parser.add_argument("--max-bytes", type=int, default=MAX_BYTES_DEFAULT)
    parser.add_argument("--max-attempts", type=int, default=4)
    args = parser.parse_args()

    if args.min_interval < MIN_INTERVAL_SECONDS:
        raise SystemExit(
            f"min interval cannot be below {MIN_INTERVAL_SECONDS:.1f}s"
        )

    rows = load_candidates(args.candidates, args.year)
    if args.limit > 0:
        rows = rows[: args.limit]

    root = args.output_dir.expanduser().resolve()
    pdf_dir = root / "pdf"
    ledger_path = root / "acquisition.jsonl"
    pdf_dir.mkdir(parents=True, exist_ok=True)
    ledger = load_ledger(ledger_path)

    last_request = 0.0
    completed = skipped = failed = 0

    for index, row in enumerate(rows, 1):
        revision_id = row["revision_openreview_id"]
        prior = ledger.get(revision_id)
        target = pdf_dir / f"{revision_id}.pdf"

        if (
            prior
            and prior.get("status") == "ok"
            and target.exists()
            and target.stat().st_size == prior.get("size_bytes")
        ):
            skipped += 1
            continue

        record = {
            "year": row["year"],
            "forum_id": row["forum_id"],
            "decision": row["decision"],
            "revision_openreview_id": revision_id,
            "revision_tmdate_utc": row["revision_tmdate_utc"],
            "url": row["pdf_endpoint"],
            "attempted_at_utc": None,
        }

        success = False
        for attempt in range(1, args.max_attempts + 1):
            wait = args.min_interval - (time.monotonic() - last_request)
            if wait > 0:
                time.sleep(wait)
            last_request = time.monotonic()
            record["attempted_at_utc"] = time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
            )
            try:
                digest, size = download_one(
                    row["pdf_endpoint"], target, args.max_bytes
                )
                record.update(
                    {
                        "status": "ok",
                        "sha256": digest,
                        "size_bytes": size,
                        "attempt": attempt,
                    }
                )
                append_ledger(ledger_path, record)
                ledger[revision_id] = record
                completed += 1
                success = True
                print(
                    f"[{index}/{len(rows)}] ok {revision_id} "
                    f"{size} bytes {digest[:12]}",
                    flush=True,
                )
                break
            except urllib.error.HTTPError as exc:
                record.update(
                    {
                        "status": "http_error",
                        "http_status": exc.code,
                        "attempt": attempt,
                    }
                )
                if exc.code in {401, 403, 404}:
                    break
                delay = retry_after_seconds(
                    exc.headers, min(300.0, 15.0 * (2 ** (attempt - 1)))
                )
                time.sleep(delay)
            except Exception as exc:
                record.update(
                    {
                        "status": "error",
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                        "attempt": attempt,
                    }
                )
                time.sleep(min(300.0, 15.0 * (2 ** (attempt - 1))))

        if not success:
            target.with_suffix(target.suffix + ".part").unlink(missing_ok=True)
            append_ledger(ledger_path, record)
            ledger[revision_id] = record
            failed += 1
            print(
                f"[{index}/{len(rows)}] FAILED {revision_id} "
                f"{record.get('status')} {record.get('http_status', '')}",
                flush=True,
            )
            if record.get("http_status") == 403:
                raise SystemExit(
                    "OpenReview returned 403. Acquisition stopped rather than "
                    "attempting to bypass source controls."
                )

    print(
        json.dumps(
            {
                "year": args.year,
                "selected": len(rows),
                "completed_this_run": completed,
                "skipped_existing": skipped,
                "failed_this_run": failed,
                "ledger": str(ledger_path),
                "pdf_dir": str(pdf_dir),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
