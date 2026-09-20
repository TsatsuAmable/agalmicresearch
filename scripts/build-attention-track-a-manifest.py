#!/usr/bin/env python3
"""Build a provenance-bound Track A cohort manifest from independent ICLR corpora.

The manifest freezes current observable records and audits source reconciliation.
It does NOT upgrade current snapshots to decision-time admissibility.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode()


def text_hash(value: Any) -> str | None:
    if value is None:
        return None
    return sha256_bytes(str(value).encode("utf-8"))


def value_hash(value: Any) -> str | None:
    if value is None:
        return None
    return sha256_bytes(canonical_json(value))


def normalize_title(value: str | None) -> str:
    return re.sub(r"\W+", " ", (value or "").casefold()).strip()


def decision_class(value: str | None) -> str:
    value = (value or "").strip()
    if value.startswith("Accept"):
        return "ACCEPT"
    if value == "Reject":
        return "REJECT"
    if value == "Withdrawn":
        return "WITHDRAWN"
    if value == "Desk rejected":
        return "DESK_REJECTED"
    return value.upper() or "MISSING"


def git_head(repo: Path) -> str:
    return subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()


def load_prrca(root: Path, years: set[int]) -> tuple[dict[tuple[int, str], dict[str, Any]], str]:
    corpus = root / "MetaReview_Generation_Corpus"
    records: dict[tuple[int, str], dict[str, Any]] = {}
    digest = hashlib.sha256()
    for year in sorted(years):
        for path in sorted(corpus.glob(f"{year}_*.json")):
            raw = path.read_bytes()
            doc = json.loads(raw)
            key = (year, str(doc["forum"]))
            if key in records:
                raise RuntimeError(f"duplicate PRRCA record {key}")
            digest.update(path.name.encode())
            digest.update(raw)
            records[key] = {
                "path": str(path.relative_to(root)),
                "sha256": sha256_bytes(raw),
                "title": doc.get("title"),
                "decision": doc.get("decision"),
            }
    return records, digest.hexdigest()


def load_berenslab(parquet: Path, years: set[int]) -> list[dict[str, Any]]:
    try:
        import pyarrow.parquet as pq
    except ImportError as exc:
        raise SystemExit(
            "pyarrow required; run with: uv run --with pyarrow python3 "
            "scripts/build-attention-track-a-manifest.py ..."
        ) from exc
    table = pq.read_table(
        parquet,
        columns=["year", "id", "title", "abstract", "keywords", "decision"],
    )
    rows = [r for r in table.to_pylist() if int(r["year"]) in years]
    rows.sort(key=lambda r: (int(r["year"]), str(r["id"])))
    return rows


def build_rows(
    berenslab: list[dict[str, Any]],
    prrca: dict[tuple[int, str], dict[str, Any]],
) -> list[dict[str, Any]]:
    out = []
    for row in berenslab:
        year, forum = int(row["year"]), str(row["id"])
        witness = prrca.get((year, forum))
        bdec = decision_class(row.get("decision"))
        pdec = decision_class(witness.get("decision")) if witness else None
        keywords = row.get("keywords")
        out.append(
            {
                "year": year,
                "forum_id": forum,
                "decision": bdec,
                "decision_raw": row.get("decision"),
                "primary_comparison_eligible": bdec in {"ACCEPT", "REJECT"},
                "berenslab_snapshot": {
                    "title_sha256": text_hash(row.get("title")),
                    "abstract_sha256": text_hash(row.get("abstract")),
                    "keywords_sha256": value_hash(keywords),
                    "keywords_present": bool(keywords),
                },
                "prrca_witness": {
                    "present": bool(witness),
                    "path": witness.get("path") if witness else None,
                    "sha256": witness.get("sha256") if witness else None,
                    "decision": pdec,
                    "decision_match": (pdec == bdec) if witness else None,
                    "normalized_title_match": (
                        normalize_title(witness.get("title"))
                        == normalize_title(row.get("title"))
                    )
                    if witness
                    else None,
                },
                "temporal_admissibility": {
                    "title": "CURRENT_ONLY",
                    "abstract": "CURRENT_ONLY",
                    "keywords": "CURRENT_ONLY" if keywords else "UNRESOLVED",
                    "decision": "OUTCOME_ONLY",
                },
            }
        )
    return out


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {"years": {}}
    for year in sorted({r["year"] for r in rows}):
        yr = [r for r in rows if r["year"] == year]
        eligible = [r for r in yr if r["primary_comparison_eligible"]]
        by_decision = Counter(r["decision"] for r in yr)
        witness = [r for r in yr if r["prrca_witness"]["present"]]
        mismatches = [
            r for r in witness if r["prrca_witness"]["decision_match"] is False
        ]
        title_mismatches = [
            r for r in witness if r["prrca_witness"]["normalized_title_match"] is False
        ]
        coverage = {}
        for d in ("ACCEPT", "REJECT"):
            denom = sum(r["decision"] == d for r in yr)
            numer = sum(
                r["decision"] == d and r["prrca_witness"]["present"] for r in yr
            )
            coverage[d] = {
                "observed": numer,
                "total": denom,
                "fraction": numer / denom if denom else None,
            }
        summary["years"][str(year)] = {
            "cohort_size": len(yr),
            "decision_counts": dict(sorted(by_decision.items())),
            "primary_comparison_size": len(eligible),
            "prrca_witness_count": len(witness),
            "prrca_witness_fraction_all": len(witness) / len(yr),
            "prrca_coverage_by_decision": coverage,
            "decision_mismatch_count": len(mismatches),
            "decision_mismatches": [
                {
                    "forum_id": r["forum_id"],
                    "canonical_decision": r["decision"],
                    "witness_decision": r["prrca_witness"]["decision"],
                }
                for r in mismatches
            ],
            "normalized_title_mismatch_count": len(title_mismatches),
            "normalized_title_mismatch_forum_ids": [r["forum_id"] for r in title_mismatches],
            "missing_keywords": sum(
                r["temporal_admissibility"]["keywords"] == "UNRESOLVED" for r in yr
            ),
        }
    return summary


def render_report(
    summary: dict[str, Any],
    provenance: dict[str, Any],
    manifest_sha: str,
) -> str:
    lines = [
        "# Track A Cohort Manifest Audit v0.1",
        "",
        "**Status:** feasibility artefact; empirical policy comparison remains gated.",
        "",
        "## Result",
        "",
        "A deterministic two-year cohort manifest now exists for ICLR 2020–2021, "
        "reconciled against two independent public corpora. The reconciliation improves "
        "coverage knowledge but does not establish decision-time provenance for title, "
        "abstract, or keywords. Those fields therefore remain CURRENT_ONLY; no allocator "
        "input is yet T0-admissible.",
        "",
        f"Manifest SHA-256: {manifest_sha}",
        "",
        "## Coverage",
        "",
        "| Year | Full cohort | Accept | Reject | Withdrawn | Desk reject | "
        "PRRCA witness | Accept witness | Reject witness |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for year, s in summary["years"].items():
        d = s["decision_counts"]
        a = s["prrca_coverage_by_decision"]["ACCEPT"]
        r = s["prrca_coverage_by_decision"]["REJECT"]
        lines.append(
            f"| {year} | {s['cohort_size']} | {d.get('ACCEPT', 0)} | "
            f"{d.get('REJECT', 0)} | {d.get('WITHDRAWN', 0)} | "
            f"{d.get('DESK_REJECTED', 0)} | {s['prrca_witness_count']} | "
            f"{a['observed']}/{a['total']} ({a['fraction']:.1%}) | "
            f"{r['observed']}/{r['total']} ({r['fraction']:.1%}) |"
        )
    lines += ["", "## Adversarial findings", ""]
    for year, s in summary["years"].items():
        lines.append(
            f"- {year}: independent witness coverage is materially higher for accepted "
            "papers than rejected papers; this source must not define the canonical candidate pool."
        )
        lines.append(
            f"- {year}: decision mismatches across overlapping records: "
            f"{s['decision_mismatch_count']}; normalized-title mismatches: "
            f"{s['normalized_title_mismatch_count']}."
        )
    lines += [
        "- The broader berenslab corpus supplies the full candidate frame used here, "
        "including withdrawn and desk-rejected records, but it is a later scrape and "
        "therefore freezes current snapshots rather than proving submission-time state.",
        "- PRRCA is useful as an independent identity/decision witness but is incomplete "
        "and outcome-differential for the primary ACCEPT/REJECT comparison.",
        "",
        "## Gate verdict",
        "",
        "**CONDITIONAL / NOT YET PASS.** Manifest construction, source hashing, exclusion "
        "accounting, and accepted/rejected coverage measurement are now complete for two years. "
        "The remaining blocker is temporal provenance: at least one allocator-visible "
        "submission field must be upgraded from CURRENT_ONLY to T0_OBSERVED or T0_DERIVABLE "
        "before empirical policy simulation.",
        "",
        "## Source provenance",
        "",
        f"- berenslab/iclr-dataset commit: {provenance['berenslab_commit']}; "
        f"parquet SHA-256: {provenance['berenslab_parquet_sha256']}.",
        f"- ntunlplab/PRRCA commit: {provenance['prrca_commit']}; "
        f"selected-file aggregate SHA-256: {provenance['prrca_selected_files_sha256']}.",
        "",
        "The manifest stores content hashes rather than treating later-scraped text as "
        "admissible historical evidence.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--berenslab-repo", type=Path, required=True)
    p.add_argument("--prrca-repo", type=Path, required=True)
    p.add_argument("--years", nargs="+", type=int, default=[2020, 2021])
    p.add_argument(
        "--out",
        type=Path,
        default=Path("research/attention_allocation/cohort"),
    )
    args = p.parse_args()
    years = set(args.years)
    parquet = args.berenslab_repo / "data" / "iclr26v1.parquet"
    berenslab = load_berenslab(parquet, years)
    prrca, prrca_digest = load_prrca(args.prrca_repo, years)
    rows = build_rows(berenslab, prrca)

    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    manifest = out / "track_a_2020_2021_manifest.jsonl"
    manifest_bytes = b"".join(canonical_json(row) for row in rows)
    manifest.write_bytes(manifest_bytes)
    manifest_sha = sha256_bytes(manifest_bytes)
    provenance = {
        "schema_version": "0.1",
        "years": sorted(years),
        "berenslab_commit": git_head(args.berenslab_repo),
        "berenslab_parquet": str(parquet.relative_to(args.berenslab_repo)),
        "berenslab_parquet_sha256": sha256_file(parquet),
        "prrca_commit": git_head(args.prrca_repo),
        "prrca_selected_files_sha256": prrca_digest,
        "manifest_sha256": manifest_sha,
        "temporal_policy": "CURRENT_ONLY snapshots are forbidden allocator inputs",
    }
    summary = summarize(rows)
    payload = {"provenance": provenance, **summary}
    (out / "track_a_2020_2021_summary.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    (out / "TRACK_A_COHORT_MANIFEST_AUDIT.md").write_text(
        render_report(summary, provenance, manifest_sha)
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
