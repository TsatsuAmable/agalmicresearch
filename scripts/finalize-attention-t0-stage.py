#!/usr/bin/env python3
"""Finalize the outcome-blind Track A T0 stage after acquisition completes.

This orchestrator may freeze the technical cohort, build the final historical
representation, and reproduce preregistered policy selections. It never
acquires or evaluates downstream outcomes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ALLOWED = {
    "PASS_TECHNICAL_AVAILABILITY",
    "CONDITIONAL_TECHNICAL_AVAILABILITY",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def write_status(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--acquisition-ledger", type=Path, required=True)
    parser.add_argument("--extraction-ledger", type=Path, required=True)
    parser.add_argument("--content-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--year", type=int, default=2020)
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    scripts = root / "scripts"
    args.out_dir.mkdir(parents=True, exist_ok=True)

    audit = args.out_dir / "technical_availability_audit.json"
    cohort = args.out_dir / "frozen_t0_cohort.jsonl"
    representation = args.out_dir / "representation"
    policies = args.out_dir / "policies"
    precision_audit = args.out_dir / "design_precision_audit.json"
    status_path = args.out_dir / "finalization_status.json"

    run(
        [
            sys.executable,
            str(scripts / "audit-attention-t0-extraction.py"),
            "--candidates",
            str(args.candidates),
            "--acquisition-ledger",
            str(args.acquisition_ledger),
            "--extraction-ledger",
            str(args.extraction_ledger),
            "--year",
            str(args.year),
            "--out",
            str(audit),
        ]
    )

    audit_doc = json.loads(audit.read_text())
    if audit_doc.get("complete") is not True:
        write_status(
            status_path,
            {
                "schema_version": "0.1",
                "status": "WAITING_FOR_TERMINAL_T0_PIPELINE",
                "technical_adjudication": audit_doc.get("adjudication"),
                "technical_audit_sha256": sha256_file(audit),
                "outcomes_touched": False,
            },
        )
        raise SystemExit(2)

    adjudication = str(audit_doc.get("adjudication"))
    if adjudication not in ALLOWED:
        write_status(
            status_path,
            {
                "schema_version": "0.1",
                "status": "T0_TECHNICAL_GATE_STOP",
                "technical_adjudication": adjudication,
                "technical_audit_sha256": sha256_file(audit),
                "outcomes_touched": False,
            },
        )
        raise SystemExit(3)

    run(
        [
            sys.executable,
            str(scripts / "freeze-attention-t0-cohort.py"),
            "--candidates",
            str(args.candidates),
            "--acquisition-ledger",
            str(args.acquisition_ledger),
            "--extraction-ledger",
            str(args.extraction_ledger),
            "--technical-audit",
            str(audit),
            "--year",
            str(args.year),
            "--out",
            str(cohort),
        ]
    )

    run(
        [
            "uv",
            "run",
            "--with",
            "numpy",
            "--with",
            "scipy",
            "--with",
            "scikit-learn",
            "python3",
            str(scripts / "build-attention-t0-representation.py"),
            "--post-t0-gate",
            "--frozen-cohort",
            str(cohort),
            "--extraction-ledger",
            str(args.extraction_ledger),
            "--content-dir",
            str(args.content_dir),
            "--out-dir",
            str(representation),
        ]
    )

    run(
        [
            "uv",
            "run",
            "--with",
            "numpy",
            "python3",
            str(scripts / "select-attention-track-a-policies.py"),
            "--post-t0-gate",
            "--representation",
            str(representation / "representation.npz"),
            "--row-index",
            str(representation / "row_index.jsonl"),
            "--representation-manifest",
            str(representation / "representation_manifest.json"),
            "--out-dir",
            str(policies),
        ]
    )

    run(
        [
            sys.executable,
            str(scripts / "audit-attention-track-a-design-precision.py"),
            "--policy-selections",
            str(policies / "policy_selections.json"),
            "--policy-manifest",
            str(policies / "policy_manifest.json"),
            "--out",
            str(precision_audit),
        ]
    )

    cohort_manifest = cohort.with_suffix(cohort.suffix + ".manifest.json")
    rep_manifest = representation / "representation_manifest.json"
    policy_manifest = policies / "policy_manifest.json"
    precision_doc = json.loads(precision_audit.read_text())

    payload = {
        "schema_version": "0.1",
        "status": "OUTCOME_BLIND_T0_STAGE_COMPLETE",
        "technical_adjudication": adjudication,
        "outcomes_touched": False,
        "downstream_outcome_gate": "STILL_CLOSED_PENDING_BROADER_FEASIBILITY_REVIEW",
        "design_precision_status": precision_doc.get("status"),
        "artefacts": {
            "technical_audit_sha256": sha256_file(audit),
            "frozen_cohort_sha256": sha256_file(cohort),
            "frozen_cohort_manifest_sha256": sha256_file(cohort_manifest),
            "representation_manifest_sha256": sha256_file(rep_manifest),
            "policy_manifest_sha256": sha256_file(policy_manifest),
            "design_precision_audit_sha256": sha256_file(precision_audit),
        },
    }
    write_status(status_path, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
