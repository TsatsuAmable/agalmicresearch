#!/usr/bin/env python3
"""Run the frozen Track A downstream outcome stage after broader adjudication.

This wrapper is deliberately fail-closed. It reads the broader pre-outcome
adjudication and exits without network activity unless citation acquisition is
explicitly authorized. When authorized it runs the batched C5 acquisition,
then the frozen evaluator. It does not refit representation or policy choices.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--adjudication", type=Path, required=True)
    parser.add_argument("--frozen-cohort", type=Path, required=True)
    parser.add_argument("--identity-jsonl", type=Path, required=True)
    parser.add_argument("--policy-selections", type=Path, required=True)
    parser.add_argument("--lineage-candidates", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--max-total-cost-usd", type=float, default=0.09)
    parser.add_argument("--batch-size", type=int, default=100)
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    scripts = root / "scripts"
    args.out_dir.mkdir(parents=True, exist_ok=True)
    status_path = args.out_dir / "post_gate_outcome_status.json"

    adjudication = json.loads(args.adjudication.read_text())
    authorized = (
        adjudication.get("citation_outcome_acquisition_authorized") is True
        and adjudication.get("verdict")
        in {"PASS_PRE_OUTCOME", "CONDITIONAL_PASS_PRE_OUTCOME"}
        and adjudication.get("outcomes_observed") is False
    )

    if not authorized:
        payload = {
            "schema_version": "0.1",
            "status": "POST_GATE_OUTCOME_STAGE_NOT_AUTHORIZED",
            "network_activity_started": False,
            "adjudication_verdict": adjudication.get("verdict"),
            "citation_outcome_acquisition_authorized":
                adjudication.get(
                    "citation_outcome_acquisition_authorized"
                ),
            "fatal_reasons": adjudication.get("fatal_reasons") or [],
            "conditional_restrictions":
                adjudication.get("conditional_restrictions") or [],
            "adjudication_sha256": sha256_file(args.adjudication),
        }
        write_json(status_path, payload)
        print(json.dumps(payload, indent=2, sort_keys=True))
        raise SystemExit(3)

    acquisition_dir = args.out_dir / "openalex_c5"
    acquisition_manifest = (
        acquisition_dir / "citation_acquisition_manifest.json"
    )
    analysis_path = args.out_dir / "track_a_primary_analysis.json"

    run(
        [
            sys.executable,
            str(
                scripts
                / "acquire-attention-openalex-citations-batched.py"
            ),
            "--adjudication",
            str(args.adjudication),
            "--frozen-cohort",
            str(args.frozen_cohort),
            "--identity-jsonl",
            str(args.identity_jsonl),
            "--out-dir",
            str(acquisition_dir),
            "--max-total-cost-usd",
            str(args.max_total_cost_usd),
            "--batch-size",
            str(args.batch_size),
        ]
    )

    acquisition = json.loads(acquisition_manifest.read_text())
    if acquisition.get("status") != "FROZEN_C5_ACQUISITION_COMPLETE":
        payload = {
            "schema_version": "0.1",
            "status": "POST_GATE_CITATION_ACQUISITION_PARTIAL",
            "network_activity_started": bool(
                acquisition.get("network_activity_started")
            ),
            "adjudication_verdict": adjudication["verdict"],
            "acquisition_status": acquisition.get("status"),
            "stop_reason": acquisition.get("stop_reason"),
            "recorded_total_cost_usd":
                acquisition.get("recorded_total_cost_usd"),
            "adjudication_sha256": sha256_file(args.adjudication),
            "acquisition_manifest_sha256": sha256_file(
                acquisition_manifest
            ),
        }
        write_json(status_path, payload)
        print(json.dumps(payload, indent=2, sort_keys=True))
        raise SystemExit(4)

    run(
        [
            "uv",
            "run",
            "--with",
            "numpy",
            "python3",
            str(scripts / "evaluate-attention-track-a-outcomes.py"),
            "--post-feasibility-gate",
            "--policy-selections",
            str(args.policy_selections),
            "--outcome-dir",
            str(acquisition_dir / "candidate_outcomes"),
            "--out",
            str(analysis_path),
            "--bootstrap-replicates",
            "10000",
            "--permutation-replicates",
            "10000",
        ]
    )

    analysis = json.loads(analysis_path.read_text())

    sensitivity_results: dict[str, Any] = {}
    for mode in (
        "exclude_any_lineage",
        "exclude_later_accept_lineage",
    ):
        view_dir = args.out_dir / f"outcomes_{mode}"
        view_manifest = args.out_dir / f"outcomes_{mode}.manifest.json"
        sensitivity_analysis = (
            args.out_dir / f"track_a_{mode}_analysis.json"
        )
        if view_dir.exists():
            import shutil
            shutil.rmtree(view_dir)
        run(
            [
                sys.executable,
                str(
                    scripts
                    / "prepare-attention-lineage-sensitivity-outcomes.py"
                ),
                "--outcome-dir",
                str(acquisition_dir / "candidate_outcomes"),
                "--lineage-candidates",
                str(args.lineage_candidates),
                "--mode",
                mode,
                "--out-dir",
                str(view_dir),
            ]
        )
        run(
            [
                "uv",
                "run",
                "--with",
                "numpy",
                "python3",
                str(scripts / "evaluate-attention-track-a-outcomes.py"),
                "--post-feasibility-gate",
                "--policy-selections",
                str(args.policy_selections),
                "--outcome-dir",
                str(view_dir),
                "--out",
                str(sensitivity_analysis),
                "--bootstrap-replicates",
                "10000",
                "--permutation-replicates",
                "10000",
            ]
        )
        sensitivity_doc = json.loads(sensitivity_analysis.read_text())
        sensitivity_results[mode] = {
            "matched_outcome_count": sensitivity_doc.get(
                "matched_outcome_count"
            ),
            "high_recognition_count": sensitivity_doc.get(
                "high_recognition_count"
            ),
            "view_manifest_sha256": sha256_file(view_manifest),
            "analysis_sha256": sha256_file(sensitivity_analysis),
            "analysis": str(sensitivity_analysis),
        }

    payload = {
        "schema_version": "0.1",
        "status": "POST_GATE_PRIMARY_ANALYSIS_COMPLETE",
        "network_activity_started": True,
        "adjudication_verdict": adjudication["verdict"],
        "conditional_restrictions":
            adjudication.get("conditional_restrictions") or [],
        "matched_outcome_count": analysis.get("matched_outcome_count"),
        "high_recognition_count": analysis.get("high_recognition_count"),
        "c5_high_recognition_threshold":
            analysis.get("c5_high_recognition_threshold"),
        "adjudication_sha256": sha256_file(args.adjudication),
        "acquisition_manifest_sha256": sha256_file(
            acquisition_manifest
        ),
        "analysis_sha256": sha256_file(analysis_path),
        "primary_analysis": str(analysis_path),
        "lineage_sensitivity_analyses": sensitivity_results,
    }
    write_json(status_path, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
