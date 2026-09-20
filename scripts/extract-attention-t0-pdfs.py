#!/usr/bin/env python3
"""Extract text from acquired T0 historical PDFs without outcome leakage.

The extractor is offline: it never fetches network content. It verifies each
PDF against the acquisition SHA-256, extracts page text in source order with
pypdf, writes gzip-compressed page JSON outside the repository, and records a
resumable extraction ledger.

Decision labels are deliberately not copied into extraction outputs.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_latest_ledger(path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        out[str(row["revision_openreview_id"])] = row
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


def extract_pdf(path: Path) -> tuple[list[str], list[dict[str, Any]]]:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise SystemExit(
            "pypdf required; run with: uv run --with pypdf python3 "
            "scripts/extract-attention-t0-pdfs.py ..."
        ) from exc

    reader = PdfReader(str(path), strict=False)
    pages: list[str] = []
    page_errors: list[dict[str, Any]] = []
    for index, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
            pages.append(text)
        except Exception as exc:
            pages.append("")
            page_errors.append(
                {
                    "page_index": index,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
    return pages, page_errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--acquisition-ledger", type=Path, required=True)
    parser.add_argument("--pdf-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    acquisitions = load_latest_ledger(args.acquisition_ledger)
    extraction_ledger_path = args.output_dir / "extraction.jsonl"
    existing = load_latest_ledger(extraction_ledger_path)

    rows = [
        row
        for row in acquisitions.values()
        if row.get("status") == "ok"
    ]
    rows.sort(key=lambda row: str(row["revision_openreview_id"]))
    if args.limit > 0:
        rows = rows[: args.limit]

    completed = skipped = failed = 0
    content_dir = args.output_dir / "text"

    for index, row in enumerate(rows, 1):
        revision_id = str(row["revision_openreview_id"])
        source_sha = str(row["sha256"])
        pdf_path = args.pdf_dir / f"{revision_id}.pdf"
        content_path = content_dir / f"{revision_id}.json.gz"

        prior = existing.get(revision_id)
        if (
            prior
            and prior.get("status") == "ok"
            and prior.get("source_pdf_sha256") == source_sha
            and content_path.exists()
        ):
            skipped += 1
            continue

        record: dict[str, Any] = {
            "revision_openreview_id": revision_id,
            "forum_id": row.get("forum_id"),
            "year": row.get("year"),
            "source_pdf_sha256": source_sha,
        }

        try:
            if not pdf_path.exists():
                raise FileNotFoundError(str(pdf_path))
            actual_sha = sha256_file(pdf_path)
            if actual_sha != source_sha:
                raise RuntimeError(
                    f"source PDF hash mismatch: ledger={source_sha} actual={actual_sha}"
                )

            pages, page_errors = extract_pdf(pdf_path)
            joined = "\n\f\n".join(pages)
            payload = {
                "schema_version": "0.1",
                "revision_openreview_id": revision_id,
                "source_pdf_sha256": source_sha,
                "pages": pages,
            }
            write_gzip_json(content_path, payload)
            nonempty_pages = sum(bool(page.strip()) for page in pages)
            char_count = sum(len(page) for page in pages)

            quality_flags: list[str] = []
            if char_count == 0:
                quality_flags.append("ZERO_TEXT")
            elif char_count < 1000:
                quality_flags.append("LOW_TEXT_LT_1000")
            if page_errors:
                quality_flags.append("PAGE_EXTRACTION_ERRORS")

            record.update(
                {
                    "status": "ok",
                    "page_count": len(pages),
                    "nonempty_page_count": nonempty_pages,
                    "char_count": char_count,
                    "text_sha256": sha256_text(joined),
                    "page_error_count": len(page_errors),
                    "page_errors": page_errors,
                    "quality_flags": quality_flags,
                    "content_file": str(content_path),
                }
            )
            append_ledger(extraction_ledger_path, record)
            existing[revision_id] = record
            completed += 1
            print(
                f"[{index}/{len(rows)}] ok {revision_id} "
                f"pages={len(pages)} chars={char_count} flags={quality_flags}",
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
            append_ledger(extraction_ledger_path, record)
            existing[revision_id] = record
            failed += 1
            print(
                f"[{index}/{len(rows)}] FAILED {revision_id} "
                f"{type(exc).__name__}: {exc}",
                flush=True,
            )

    print(
        json.dumps(
            {
                "selected_acquired_pdfs": len(rows),
                "completed_this_run": completed,
                "skipped_existing": skipped,
                "failed_this_run": failed,
                "extraction_ledger": str(extraction_ledger_path),
                "content_dir": str(content_dir),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
