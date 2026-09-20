#!/usr/bin/env python3
"""Create immutable outcome-directory views for frozen lineage sensitivities.

The script never changes outcome values. It creates hard-linked (or copied)
views that exclude prospectively flagged lineage candidates, allowing the same
frozen evaluator to be rerun without changing its primary semantics.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Any

MODES = {
    "exclude_any_lineage": "any_lineage_including_sensitivity",
    "exclude_later_accept_lineage":
        "any_later_accept_lineage_including_sensitivity",
}


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


def outcome_forum_id(path: Path) -> str:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        row = json.load(f)
    if row.get("status") != "FROZEN_C5_OUTCOME":
        raise RuntimeError(f"unexpected outcome status: {path}")
    return str(row["forum_id"])


def link_or_copy(source: Path, target: Path) -> str:
    if target.exists():
        target.unlink()
    try:
        os.link(source, target)
        return "hardlink"
    except OSError:
        shutil.copy2(source, target)
        return "copy"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outcome-dir", type=Path, required=True)
    parser.add_argument("--lineage-candidates", type=Path, required=True)
    parser.add_argument("--mode", choices=sorted(MODES), required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    lineage = {
        str(row["forum_id"]): row
        for row in load_jsonl(args.lineage_candidates)
    }
    flag = MODES[args.mode]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    existing = list(args.out_dir.glob("*.json.gz"))
    if existing:
        raise RuntimeError(
            "sensitivity output directory must be empty to avoid stale views"
        )

    source_files = sorted(args.outcome_dir.glob("*.json.gz"))
    if not source_files:
        raise RuntimeError("no frozen C5 outcomes found")

    included: list[str] = []
    excluded: list[str] = []
    missing_lineage: list[str] = []
    materialization_modes: dict[str, int] = {}

    for source in source_files:
        forum_id = outcome_forum_id(source)
        record = lineage.get(forum_id)
        if record is None:
            missing_lineage.append(forum_id)
            continue
        if bool(record.get(flag)):
            excluded.append(forum_id)
            continue
        mode = link_or_copy(source, args.out_dir / source.name)
        materialization_modes[mode] = (
            materialization_modes.get(mode, 0) + 1
        )
        included.append(forum_id)

    if missing_lineage:
        raise RuntimeError(
            f"lineage file missing {len(missing_lineage)} outcome IDs; "
            f"first={missing_lineage[:5]}"
        )

    manifest = {
        "schema_version": "0.1",
        "status": "FROZEN_LINEAGE_SENSITIVITY_OUTCOME_VIEW",
        "mode": args.mode,
        "lineage_flag": flag,
        "source_outcome_count": len(source_files),
        "included_count": len(included),
        "excluded_count": len(excluded),
        "excluded_forum_ids": sorted(excluded),
        "materialization_modes": materialization_modes,
        "inputs": {
            "lineage_candidates_sha256": sha256_file(
                args.lineage_candidates
            ),
        },
    }
    manifest_path = args.out_dir.parent / (
        args.out_dir.name + ".manifest.json"
    )
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
