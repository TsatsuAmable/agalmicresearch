#!/usr/bin/env python3
"""
Phase-1 ICLR expert-attention preservation audit.

This script is deliberately descriptive. Reviewer scores and decisions are
post-review signals and MUST NOT be used as deployable triage features.

Data source:
  https://github.com/berenslab/iclr-dataset
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import requests

DATASETS = {
    "24v2": "https://raw.githubusercontent.com/berenslab/iclr-dataset/main/data/iclr24v2.parquet",
    "25v2": "https://raw.githubusercontent.com/berenslab/iclr-dataset/main/data/iclr25v2.parquet",
}
BUDGETS = (0.05, 0.10, 0.20, 0.40, 0.60, 0.80, 1.00)


def download(url: str, path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with requests.get(url, stream=True, timeout=120) as response:
            response.raise_for_status()
            with path.open("wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def find_column(df: pd.DataFrame, aliases: Iterable[str], required: bool = True) -> str | None:
    normalized = {re.sub(r"[^a-z0-9]", "", c.lower()): c for c in df.columns}
    for alias in aliases:
        key = re.sub(r"[^a-z0-9]", "", alias.lower())
        if key in normalized:
            return normalized[key]
    if required:
        raise KeyError(f"Could not find any of {list(aliases)} in columns: {list(df.columns)}")
    return None


def parse_scores(value) -> list[float]:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return []
    if isinstance(value, np.ndarray):
        value = value.tolist()
    if isinstance(value, (list, tuple)):
        out = []
        for x in value:
            try:
                out.append(float(x))
            except (TypeError, ValueError):
                pass
        return out
    if isinstance(value, str):
        text = value.strip()
        try:
            parsed = ast.literal_eval(text)
            if isinstance(parsed, (list, tuple, np.ndarray)):
                return parse_scores(parsed)
        except (ValueError, SyntaxError):
            pass
        return [float(x) for x in re.findall(r"(?<![\w.])-?\d+(?:\.\d+)?", text)]
    try:
        return [float(value)]
    except (TypeError, ValueError):
        return []


def accepted(decision) -> bool | None:
    if decision is None or (isinstance(decision, float) and math.isnan(decision)):
        return None
    s = str(decision).strip().lower()
    if not s or s in {"none", "nan", "unknown"}:
        return None
    if any(x in s for x in ("reject", "withdraw", "desk reject")):
        return False
    if any(x in s for x in ("accept", "poster", "spotlight", "oral")):
        return True
    return None


def zscore_within(group: pd.Series) -> pd.Series:
    sd = group.std(ddof=0)
    if not np.isfinite(sd) or sd == 0:
        return pd.Series(np.zeros(len(group)), index=group.index)
    return (group - group.mean()) / sd


def recall(mask: pd.Series, routed: pd.Series) -> float:
    denom = int(mask.sum())
    if denom == 0:
        return float("nan")
    return float((mask & routed).sum() / denom)


def route_top_fraction(score: pd.Series, fraction: float) -> pd.Series:
    n = len(score)
    k = max(1, int(round(fraction * n))) if fraction < 1 else n
    order = score.fillna(-np.inf).sort_values(ascending=False, kind="mergesort").index
    routed = pd.Series(False, index=score.index)
    routed.loc[order[:k]] = True
    return routed


def random_frontier(df: pd.DataFrame, rng: np.random.Generator, repeats: int) -> list[dict]:
    rows = []
    accepted_mask = df["accepted"] == True
    dissent_mask = df["high_disagreement"]
    labeled = df["topic"].notna()
    for b in BUDGETS:
        ar, dr, tmin = [], [], []
        k = max(1, int(round(b * len(df)))) if b < 1 else len(df)
        for _ in range(repeats):
            pick = rng.choice(len(df), size=k, replace=False)
            routed = pd.Series(False, index=df.index)
            routed.iloc[pick] = True
            ar.append(recall(accepted_mask, routed))
            dr.append(recall(dissent_mask, routed))
            topic_recalls = []
            for _, idx in df[labeled].groupby("topic").groups.items():
                topic_mask = pd.Series(False, index=df.index)
                topic_mask.loc[idx] = True
                topic_recalls.append(recall(topic_mask, routed))
            tmin.append(np.nanmin(topic_recalls) if topic_recalls else np.nan)
        rows.append({
            "policy": "random",
            "budget": b,
            "accepted_recall_mean": float(np.nanmean(ar)),
            "accepted_recall_sd": float(np.nanstd(ar)),
            "dissent_recall_mean": float(np.nanmean(dr)),
            "dissent_recall_sd": float(np.nanstd(dr)),
            "worst_topic_recall_mean": float(np.nanmean(tmin)),
        })
    return rows


def deterministic_frontier(df: pd.DataFrame, policy: str, score_col: str) -> list[dict]:
    rows = []
    accepted_mask = df["accepted"] == True
    dissent_mask = df["high_disagreement"]
    labeled = df["topic"].notna()
    for b in BUDGETS:
        routed = route_top_fraction(df[score_col], b)
        topic_recalls = []
        for _, idx in df[labeled].groupby("topic").groups.items():
            topic_mask = pd.Series(False, index=df.index)
            topic_mask.loc[idx] = True
            topic_recalls.append(recall(topic_mask, routed))
        rows.append({
            "policy": policy,
            "budget": b,
            "accepted_recall_mean": recall(accepted_mask, routed),
            "accepted_recall_sd": np.nan,
            "dissent_recall_mean": recall(dissent_mask, routed),
            "dissent_recall_sd": np.nan,
            "worst_topic_recall_mean": float(np.nanmin(topic_recalls)) if topic_recalls else np.nan,
        })
    return rows


def score_conditional_topic_spread(df: pd.DataFrame, min_topic_n: int) -> pd.DataFrame:
    x = df.dropna(subset=["mean_score", "accepted", "topic"]).copy()
    x["score_bin"] = (x["mean_score"] * 2).round() / 2
    g = (
        x.groupby(["year", "score_bin", "topic"], observed=True)
        .agg(n=("accepted", "size"), acceptance_rate=("accepted", "mean"))
        .reset_index()
    )
    eligible = g[g["n"] >= min_topic_n]
    spread = (
        eligible.groupby(["year", "score_bin"], observed=True)
        .agg(
            topics=("topic", "nunique"),
            papers=("n", "sum"),
            min_acceptance=("acceptance_rate", "min"),
            max_acceptance=("acceptance_rate", "max"),
        )
        .reset_index()
    )
    spread["acceptance_spread"] = spread["max_acceptance"] - spread["min_acceptance"]
    return spread


def make_report(out_dir: Path, dataset: str, sha256: str, df: pd.DataFrame,
                spread: pd.DataFrame, frontier: pd.DataFrame, cols: dict) -> None:
    n = len(df)
    complete_decisions = int(df["accepted"].notna().sum())
    reviewed = int(df["mean_score"].notna().sum())
    labeled = int(df["topic"].notna().sum())
    median_disagreement = float(df["score_sd"].median(skipna=True))
    high_dissent_threshold = float(df["score_sd"].quantile(0.90))
    max_spread = float(spread["acceptance_spread"].max()) if len(spread) else float("nan")
    focus = frontier[np.isclose(frontier["budget"], 0.20)]

    lines = [
        "# ICLR Expert-Attention Preservation Audit: Phase 1", "",
        f"Dataset: Berenslab ICLR `{dataset}`",
        f"SHA-256: `{sha256}`", "",
        "## Data audit", "",
        f"- Rows in analysis slice: **{n:,}**",
        f"- Rows with interpretable final decisions: **{complete_decisions:,}**",
        f"- Rows with at least one parsed reviewer score: **{reviewed:,}**",
        f"- Rows with a non-`unlabeled` topic: **{labeled:,}**",
        f"- Median within-paper reviewer-score SD: **{median_disagreement:.3f}**",
        f"- 90th-percentile disagreement threshold: **{high_dissent_threshold:.3f}**", "",
        "Resolved source columns:", "```json", json.dumps(cols, indent=2), "```", "",
        "## Construct-validity diagnostic", "",
        "Reviewer scores and decisions are post-review outcomes. They are used here only to diagnose",
        "measurement behaviour and to construct intentionally leaky comparison policies. They are not",
        "candidate features for a deployable pre-review triage system.", "",
    ]
    if np.isfinite(max_spread):
        lines += [
            "Among score/year cells with enough topic observations, the largest observed",
            "topic-to-topic acceptance-rate spread at approximately the same mean reviewer score was",
            f"**{max_spread:.1%}** in this dataset slice.", "",
        ]
    lines += [
        "## 20% expert-attention budget stress test", "",
        "| Policy | Accepted recall | High-disagreement recall | Worst topic recall |",
        "|---|---:|---:|---:|",
    ]
    for _, r in focus.iterrows():
        lines.append(
            f"| {r['policy']} | {r['accepted_recall_mean']:.1%} | "
            f"{r['dissent_recall_mean']:.1%} | {r['worst_topic_recall_mean']:.1%} |"
        )
    lines += [
        "", "Interpretation rule: a policy does not become desirable merely because it preserves accepted",
        "papers. If accepted-paper recall rises by sacrificing disagreement or starving some topics,",
        "it is evidence of gatekeeping mimicry rather than successful scarcity displacement.", "",
        "## Outputs", "",
        "- `yearly_summary.csv`: counts, acceptance, scores, and disagreement by year.",
        "- `topic_year_summary.csv`: the same quantities by topic and year.",
        "- `score_conditional_topic_spread.csv`: acceptance variation across topics at similar scores.",
        "- `preservation_frontier.csv`: random, raw-score, and topic-normalized-score stress tests.", "",
        "## Next empirical step", "",
        "Freeze these descriptive diagnostics, then build pre-review baselines using only information",
        "available before expert review: title, abstract, keywords/topic, and claim/evidence descriptors.",
        "Evaluate them on temporal splits. Add OpenAlex downstream outcomes only after the immediate",
        "preservation behaviour is understood.", "",
    ]
    (out_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", choices=DATASETS, default="25v2")
    p.add_argument("--cache-dir", type=Path, default=Path(".cache/agalmic-research"))
    p.add_argument("--out", type=Path, default=Path("research-output/iclr-preservation-audit"))
    p.add_argument("--min-year", type=int, default=2020)
    p.add_argument("--max-year", type=int, default=2025)
    p.add_argument("--random-repeats", type=int, default=250)
    p.add_argument("--seed", type=int, default=20260910)
    p.add_argument("--min-topic-cell", type=int, default=30)
    args = p.parse_args()

    url = DATASETS[args.dataset]
    source = args.cache_dir / f"iclr{args.dataset}.parquet"
    sha256 = download(url, source)
    raw = pd.read_parquet(source)

    year_col = find_column(raw, ["year"])
    decision_col = find_column(raw, ["decision", "status"])
    score_col = find_column(raw, ["scores", "ratings", "review_scores", "reviewer_scores"])
    topic_col = find_column(raw, ["labels", "label", "topic"], required=False)
    id_col = find_column(raw, ["id", "openreview_id", "forum"], required=False)

    df = pd.DataFrame(index=raw.index)
    df["paper_id"] = raw[id_col].astype(str) if id_col else raw.index.astype(str)
    df["year"] = pd.to_numeric(raw[year_col], errors="coerce").astype("Int64")
    df["decision_raw"] = raw[decision_col]
    df["accepted"] = raw[decision_col].map(accepted)
    df["scores"] = raw[score_col].map(parse_scores)
    df["n_reviews"] = df["scores"].map(len)
    df["mean_score"] = df["scores"].map(lambda x: float(np.mean(x)) if x else np.nan)
    df["score_sd"] = df["scores"].map(lambda x: float(np.std(x, ddof=0)) if len(x) >= 2 else np.nan)
    if topic_col:
        topic = raw[topic_col].astype("string")
        topic = topic.mask(topic.str.lower().isin(["unlabeled", "none", "nan", ""]))
        df["topic"] = topic
    else:
        df["topic"] = pd.Series(pd.NA, index=df.index, dtype="string")

    df = df[df["year"].between(args.min_year, args.max_year, inclusive="both")].copy()
    df = df[df["accepted"].notna() | df["mean_score"].notna()].copy()
    df["topic_year_score_z"] = df.groupby(["year", "topic"], dropna=False)["mean_score"].transform(zscore_within)
    threshold = df["score_sd"].quantile(0.90)
    df["high_disagreement"] = df["score_sd"].ge(threshold) & df["score_sd"].notna()

    yearly = df.groupby("year", observed=True).agg(
        papers=("paper_id", "size"), decisions=("accepted", "count"),
        acceptance_rate=("accepted", "mean"), reviewed=("mean_score", "count"),
        mean_score=("mean_score", "mean"), mean_score_sd=("score_sd", "mean"),
        labeled_topics=("topic", lambda s: s.notna().sum()),
    ).reset_index()

    topic_year = df.dropna(subset=["topic"]).groupby(["year", "topic"], observed=True).agg(
        papers=("paper_id", "size"), decisions=("accepted", "count"),
        acceptance_rate=("accepted", "mean"), reviewed=("mean_score", "count"),
        mean_score=("mean_score", "mean"), mean_disagreement=("score_sd", "mean"),
        high_disagreement_rate=("high_disagreement", "mean"),
    ).reset_index()

    spread = score_conditional_topic_spread(df, args.min_topic_cell)
    rng = np.random.default_rng(args.seed)
    frontier_rows = random_frontier(df, rng, args.random_repeats)
    frontier_rows += deterministic_frontier(df, "post_review_raw_score_DIAGNOSTIC_ONLY", "mean_score")
    frontier_rows += deterministic_frontier(df, "post_review_topic_normalized_score_DIAGNOSTIC_ONLY", "topic_year_score_z")
    frontier = pd.DataFrame(frontier_rows)

    args.out.mkdir(parents=True, exist_ok=True)
    yearly.to_csv(args.out / "yearly_summary.csv", index=False)
    topic_year.to_csv(args.out / "topic_year_summary.csv", index=False)
    spread.to_csv(args.out / "score_conditional_topic_spread.csv", index=False)
    frontier.to_csv(args.out / "preservation_frontier.csv", index=False)

    manifest = {
        "dataset": args.dataset, "source_url": url, "sha256": sha256,
        "parameters": vars(args) | {"cache_dir": str(args.cache_dir), "out": str(args.out)},
        "resolved_columns": {"year": year_col, "decision": decision_col, "scores": score_col,
                             "topic": topic_col, "paper_id": id_col},
    }
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    make_report(args.out, args.dataset, sha256, df, spread, frontier, manifest["resolved_columns"])
    print(f"Wrote audit to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
