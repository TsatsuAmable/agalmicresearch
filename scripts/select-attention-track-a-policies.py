#!/usr/bin/env python3
"""Generate preregistered outcome-blind allocation selections.

This script consumes only the frozen T0 representation. While the empirical
gate is closed, --engineering-fixture is required and outputs are explicitly
non-evidentiary.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

SEED = 20260920
PROTOCOL_VERSION = "0.1"
BUDGET_FRACTIONS = (0.05, 0.10, 0.20, 0.40, 0.80)
POLICIES = (
    "seeded_random",
    "centrality",
    "centroid_novelty",
    "local_sparsity",
    "kcenter_coverage",
    "exploration_quota",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def selected_hash(selected_rows: list[int]) -> str:
    return hashlib.sha256(canonical_bytes(selected_rows)).hexdigest()


def load_row_index(path: Path) -> list[dict[str, Any]]:
    rows = [
        json.loads(line)
        for line in path.read_text().splitlines()
        if line.strip()
    ]
    rows.sort(key=lambda row: int(row["row"]))
    for expected, row in enumerate(rows):
        if int(row["row"]) != expected:
            raise RuntimeError("row index is not contiguous and ordered")
        forbidden = {"decision", "review_score", "citations", "future_value"}
        leaked = forbidden.intersection(row)
        if leaked:
            raise RuntimeError(
                f"row index contains forbidden keys: {sorted(leaked)}"
            )
    return rows


def stable_rank(values, descending: bool):
    import numpy as np

    index = np.arange(len(values), dtype=np.int64)
    primary = -values if descending else values
    return np.lexsort((index, primary))


def kcenter_order(dense, centroid_distance, max_k: int) -> list[int]:
    import numpy as np

    n = dense.shape[0]
    if not 1 <= max_k <= n:
        raise ValueError((max_k, n))

    first = int(np.argmin(centroid_distance))
    selected = [first]
    selected_mask = np.zeros(n, dtype=bool)
    selected_mask[first] = True

    similarity = dense @ dense[first]
    min_distance = 1.0 - similarity
    min_distance[first] = -1.0

    while len(selected) < max_k:
        candidate_scores = np.where(selected_mask, -1.0, min_distance)
        nxt = int(np.argmax(candidate_scores))
        selected.append(nxt)
        selected_mask[nxt] = True
        new_distance = 1.0 - (dense @ dense[nxt])
        min_distance = np.minimum(min_distance, new_distance)
        min_distance[selected_mask] = -1.0

    return selected


def exploration_quota_selection(
    dense,
    centroid_distance,
    sparsity_rank,
    k: int,
) -> list[int]:
    import numpy as np

    n = dense.shape[0]
    if k <= 0 or k > n:
        raise ValueError((k, n))
    if k == 1:
        return [int(np.argmin(centroid_distance))]

    explore_k = max(1, int(0.25 * k))
    explore = [int(x) for x in sparsity_rank[:explore_k]]
    selected = list(explore)
    selected_mask = np.zeros(n, dtype=bool)
    selected_mask[selected] = True

    # Coverage begins from the fixed exploration set. This makes the quota
    # substantive rather than merely appending tail candidates to a completed
    # k-center solution.
    similarities = dense @ dense[selected].T
    min_distance = 1.0 - similarities.max(axis=1)
    min_distance[selected_mask] = -1.0

    while len(selected) < k:
        scores = np.where(selected_mask, -1.0, min_distance)
        nxt = int(np.argmax(scores))
        selected.append(nxt)
        selected_mask[nxt] = True
        new_distance = 1.0 - (dense @ dense[nxt])
        min_distance = np.minimum(min_distance, new_distance)
        min_distance[selected_mask] = -1.0

    return selected


def jaccard(a: list[int], b: list[int]) -> float:
    sa, sb = set(a), set(b)
    union = sa | sb
    return len(sa & sb) / len(union) if union else 1.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--representation", type=Path, required=True)
    parser.add_argument("--row-index", type=Path, required=True)
    parser.add_argument("--representation-manifest", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--engineering-fixture", action="store_true")
    args = parser.parse_args()

    if not args.engineering_fixture:
        raise SystemExit(
            "Policy selection is gated. Use --engineering-fixture for "
            "outcome-blind mechanics only until the feasibility gate passes."
        )

    try:
        import numpy as np
    except ImportError as exc:
        raise SystemExit(
            "numpy required; run with: uv run --with numpy python3 "
            "scripts/select-attention-track-a-policies.py ..."
        ) from exc

    rep_manifest = json.loads(args.representation_manifest.read_text())
    if rep_manifest.get("status") != "ENGINEERING_FIXTURE_ONLY":
        raise RuntimeError(
            "unexpected representation status; this selector currently "
            "accepts engineering fixtures only"
        )

    row_index = load_row_index(args.row_index)
    data = np.load(args.representation)
    dense = np.asarray(data["dense"], dtype=np.float64)
    centroid_distance = np.asarray(
        data["centroid_cosine_distance"], dtype=np.float64
    )
    local_sparsity = np.asarray(
        data["knn5_mean_cosine_distance"], dtype=np.float64
    )
    n = dense.shape[0]

    if n != len(row_index):
        raise RuntimeError(
            f"representation rows {n} != row index rows {len(row_index)}"
        )
    if centroid_distance.shape != (n,) or local_sparsity.shape != (n,):
        raise RuntimeError("descriptor shape mismatch")

    budgets = {
        f"{fraction:.2f}": max(1, int(fraction * n))
        for fraction in BUDGET_FRACTIONS
    }
    max_k = max(budgets.values())

    rng = np.random.default_rng(SEED)
    random_order = [int(x) for x in rng.permutation(n)]
    centrality_order = [
        int(x) for x in stable_rank(centroid_distance, descending=False)
    ]
    novelty_order = [
        int(x) for x in stable_rank(centroid_distance, descending=True)
    ]
    sparsity_order = [
        int(x) for x in stable_rank(local_sparsity, descending=True)
    ]
    coverage_order = kcenter_order(dense, centroid_distance, max_k)

    selections: dict[str, dict[str, Any]] = {}
    diagnostics: dict[str, Any] = {
        "schema_version": PROTOCOL_VERSION,
        "status": "ENGINEERING_FIXTURE_ONLY",
        "N": n,
        "budgets": budgets,
        "pairwise_jaccard": {},
    }

    static_orders = {
        "seeded_random": random_order,
        "centrality": centrality_order,
        "centroid_novelty": novelty_order,
        "local_sparsity": sparsity_order,
        "kcenter_coverage": coverage_order,
    }

    for budget_key, k in budgets.items():
        selections[budget_key] = {}
        selected_by_policy: dict[str, list[int]] = {}

        for policy, order in static_orders.items():
            selected_by_policy[policy] = order[:k]

        selected_by_policy["exploration_quota"] = (
            exploration_quota_selection(
                dense,
                centroid_distance,
                sparsity_order,
                k,
            )
        )

        for policy in POLICIES:
            selected = selected_by_policy[policy]
            if len(selected) != k:
                raise RuntimeError(
                    f"{policy} budget {budget_key}: selected "
                    f"{len(selected)} != {k}"
                )
            if len(set(selected)) != len(selected):
                raise RuntimeError(
                    f"{policy} budget {budget_key}: duplicate selection"
                )
            if any(index < 0 or index >= n for index in selected):
                raise RuntimeError(
                    f"{policy} budget {budget_key}: out-of-range row"
                )

            selections[budget_key][policy] = {
                "k": k,
                "selected_rows": selected,
                "selected_forum_ids": [
                    row_index[index]["forum_id"] for index in selected
                ],
                "selected_set_sha256": selected_hash(selected),
            }

        diagnostics["pairwise_jaccard"][budget_key] = {}
        for i, left in enumerate(POLICIES):
            for right in POLICIES[i + 1 :]:
                key = f"{left}__{right}"
                diagnostics["pairwise_jaccard"][budget_key][key] = jaccard(
                    selected_by_policy[left],
                    selected_by_policy[right],
                )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    selection_path = args.out_dir / "policy_selections.json"
    diagnostics_path = args.out_dir / "policy_diagnostics.json"
    manifest_path = args.out_dir / "policy_manifest.json"

    selection_path.write_bytes(canonical_bytes(selections))
    diagnostics_path.write_text(
        json.dumps(diagnostics, indent=2, sort_keys=True) + "\n"
    )

    manifest = {
        "schema_version": PROTOCOL_VERSION,
        "status": "ENGINEERING_FIXTURE_ONLY",
        "seed": SEED,
        "policies": list(POLICIES),
        "budget_fractions": list(BUDGET_FRACTIONS),
        "N": n,
        "budgets": budgets,
        "inputs": {
            "representation_sha256": sha256_file(args.representation),
            "row_index_sha256": sha256_file(args.row_index),
            "representation_manifest_sha256": sha256_file(
                args.representation_manifest
            ),
        },
        "outputs": {
            "policy_selections_sha256": sha256_file(selection_path),
            "policy_diagnostics_sha256": sha256_file(diagnostics_path),
        },
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )

    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
