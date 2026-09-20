#!/usr/bin/env python3
"""Audit historical pre-review snapshot coverage for Track A v0.2.

This tool deliberately uses only frozen historical Git snapshots and
outcome-ineligible conference metadata. It does not query citations or any
downstream outcome source.

A snapshot is considered "pre-review clean" only when:
- the Git commit contains no official review records;
- the Git commit contains no public/official author-reviewer comments;
- the Git commit contains no decision records;
- all matched blind submissions are anonymous.

This is a provenance/coverage audit, not authorization to use the snapshot as
the final T0 substrate. The snapshot lag from the conference deadline is
reported explicitly so the protocol can decide whether a near-deadline,
pre-review state is scientifically admissible.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *args],
        text=True,
    )


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text().splitlines()
        if line.strip()
    ]


def walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def root_submission_invitation(year: int) -> str:
    return f"ICLR.cc/{year}/Conference/-/Blind_Submission"


def text_forum_id(path: str) -> str | None:
    prefix = "text/papers/pdf?id="
    if not path.startswith(prefix):
        return None
    value = path[len(prefix):]
    if value.endswith(".txt"):
        value = value[:-4]
    return value or None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--snapshot-repo", type=Path, required=True)
    parser.add_argument("--snapshot-commit", required=True)
    parser.add_argument("--deadline-utc", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    deadline = dt.datetime.fromisoformat(
        args.deadline_utc.replace("Z", "+00:00")
    )
    if deadline.tzinfo is None:
        raise SystemExit("--deadline-utc must include an offset or Z")

    manifest_rows = [
        row
        for row in load_jsonl(args.manifest)
        if int(row["year"]) == args.year
    ]
    eligible = {str(row["forum_id"]): row for row in manifest_rows}
    if not eligible:
        raise RuntimeError(f"no manifest rows for year {args.year}")

    commit = git(
        args.snapshot_repo,
        "rev-parse",
        args.snapshot_commit,
    ).strip()
    committed_at = dt.datetime.fromisoformat(
        git(
            args.snapshot_repo,
            "show",
            "-s",
            "--format=%cI",
            commit,
        ).strip()
    )
    lag_hours = (
        committed_at.astimezone(dt.timezone.utc)
        - deadline.astimezone(dt.timezone.utc)
    ).total_seconds() / 3600.0

    files = git(
        args.snapshot_repo,
        "ls-tree",
        "-r",
        "--name-only",
        commit,
    ).splitlines()

    note_files = sorted(
        path
        for path in files
        if re.fullmatch(r"notes\d*\.json", path)
    )
    if not note_files:
        raise RuntimeError("snapshot commit contains no notes*.json files")

    roots: dict[str, dict[str, Any]] = {}
    review_ids: set[str] = set()
    comment_ids: set[str] = set()
    decision_ids: set[str] = set()

    for path in note_files:
        payload = json.loads(
            git(args.snapshot_repo, "show", f"{commit}:{path}")
        )
        for record in walk(payload):
            record_id = record.get("id")
            invitation = str(record.get("invitation") or "")
            if record_id:
                low = invitation.casefold()
                if (
                    "official_review" in low
                    or "/official/review" in low
                ):
                    review_ids.add(str(record_id))
                if (
                    "official_comment" in low
                    or "/public/comment" in low
                ):
                    comment_ids.add(str(record_id))
                if (
                    "/decision" in low
                    or "acceptance_decision" in low
                    or "/acceptance" in low
                ):
                    decision_ids.add(str(record_id))

            if (
                record_id
                and record.get("forum") == record_id
                and record.get("replyto") is None
                and invitation == root_submission_invitation(args.year)
            ):
                roots[str(record_id)] = record

    text_ids = {
        forum_id
        for path in files
        if (forum_id := text_forum_id(path)) is not None
    }

    matched_ids = set(eligible) & set(roots)
    matched_text_ids = matched_ids & text_ids

    anonymous_ids = {
        forum_id
        for forum_id in matched_ids
        if roots[forum_id].get("content", {}).get("authors")
        == ["Anonymous"]
    }

    by_decision: dict[str, dict[str, int | float]] = {}
    for decision in ("ACCEPT", "REJECT"):
        ids = {
            forum_id
            for forum_id in eligible
            if eligible[forum_id].get("decision") == decision
        }
        root_ids = ids & matched_ids
        text_match = ids & matched_text_ids
        by_decision[decision] = {
            "eligible_count": len(ids),
            "snapshot_root_count": len(root_ids),
            "text_count": len(text_match),
            "text_fraction": (
                len(text_match) / len(ids) if ids else 0.0
            ),
        }

    pre_review_clean = (
        len(review_ids) == 0
        and len(comment_ids) == 0
        and len(decision_ids) == 0
        and len(anonymous_ids) == len(matched_ids)
    )

    result = {
        "schema_version": "0.1",
        "status": "V02_HISTORICAL_SNAPSHOT_AUDIT",
        "year": args.year,
        "snapshot_commit": commit,
        "snapshot_committed_at": committed_at.isoformat(),
        "deadline_utc": deadline.isoformat(),
        "snapshot_lag_hours": round(lag_hours, 3),
        "pre_review_clean": pre_review_clean,
        "eligible_candidate_count": len(eligible),
        "snapshot_root_count": len(roots),
        "matched_candidate_count": len(matched_ids),
        "matched_text_count": len(matched_text_ids),
        "matched_text_fraction": (
            len(matched_text_ids) / len(eligible)
        ),
        "anonymous_matched_count": len(anonymous_ids),
        "official_review_record_count": len(review_ids),
        "comment_record_count": len(comment_ids),
        "decision_record_count": len(decision_ids),
        "missing_snapshot_forum_ids": sorted(
            set(eligible) - matched_ids
        ),
        "missing_text_forum_ids": sorted(
            matched_ids - matched_text_ids
        ),
        "by_decision": by_decision,
        "inputs": {
            "manifest_sha256": sha256_file(args.manifest),
            "snapshot_repo": str(args.snapshot_repo),
        },
        "outcomes_observed": False,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
