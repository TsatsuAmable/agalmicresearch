#!/usr/bin/env python3
"""Build an outcome-blind T0 candidate representation.

This builder intentionally uses only verified historical PDF extractions and
unsupervised corpus-internal text geometry. It refuses normal execution while
the empirical gate is closed; --engineering-fixture is required for smoke tests.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import platform
import re
import unicodedata
from pathlib import Path
from typing import Any


SEED = 20260920
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[^\s@]+@[^\s@]+\.[^\s@]+\b")
WS_RE = re.compile(r"\s+")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_latest_ledger(path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        out[str(row["revision_openreview_id"])] = row
    return out


def load_content(path: Path) -> dict[str, Any]:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def normalize_text(pages: list[str]) -> str:
    text = "\n\f\n".join(pages)
    text = unicodedata.normalize("NFKC", text).lower()
    text = URL_RE.sub(" URLTOKEN ", text)
    text = EMAIL_RE.sub(" EMAILTOKEN ", text)
    return WS_RE.sub(" ", text).strip()


def save_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--extraction-ledger", type=Path, required=True)
    parser.add_argument("--content-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--engineering-fixture", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    if not args.engineering_fixture:
        raise SystemExit(
            "Representation generation is gated. Use --engineering-fixture "
            "for protocol smoke tests only until the empirical gate is passed."
        )

    try:
        import numpy as np
        import scipy
        import sklearn
        from sklearn.decomposition import TruncatedSVD
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.neighbors import NearestNeighbors
        from sklearn.preprocessing import normalize as l2_normalize
    except ImportError as exc:
        raise SystemExit(
            "numpy, scipy and scikit-learn are required; run with: "
            "uv run --with numpy --with scipy --with scikit-learn python3 "
            "scripts/build-attention-t0-representation.py ..."
        ) from exc

    ledger = load_latest_ledger(args.extraction_ledger)
    rows = [
        row
        for row in ledger.values()
        if row.get("status") == "ok"
    ]
    rows.sort(key=lambda row: str(row["revision_openreview_id"]))
    if args.limit > 0:
        rows = rows[: args.limit]

    documents: list[str] = []
    row_index: list[dict[str, Any]] = []

    for row in rows:
        revision_id = str(row["revision_openreview_id"])
        content_path = args.content_dir / f"{revision_id}.json.gz"
        if not content_path.exists():
            raise RuntimeError(f"missing extracted content: {content_path}")
        payload = load_content(content_path)
        if payload.get("source_pdf_sha256") != row.get("source_pdf_sha256"):
            raise RuntimeError(
                f"source hash mismatch between ledger and content: {revision_id}"
            )
        pages = payload.get("pages")
        if not isinstance(pages, list):
            raise RuntimeError(f"invalid pages payload: {revision_id}")
        normalized = normalize_text([str(page) for page in pages])
        documents.append(normalized)
        row_index.append(
            {
                "row": len(row_index),
                "year": row.get("year"),
                "forum_id": row.get("forum_id"),
                "revision_openreview_id": revision_id,
                "source_pdf_sha256": row.get("source_pdf_sha256"),
                "extracted_text_sha256": row.get("text_sha256"),
                "content_file_sha256": sha256_file(content_path),
            }
        )

    if len(documents) < 10:
        raise RuntimeError(
            f"need at least 10 extracted documents for representation smoke test; "
            f"found {len(documents)}"
        )

    vectorizer = TfidfVectorizer(
        lowercase=False,
        ngram_range=(1, 2),
        min_df=5,
        max_df=0.95,
        max_features=50000,
        sublinear_tf=True,
        norm="l2",
    )
    tfidf = vectorizer.fit_transform(documents)
    if tfidf.shape[1] < 3:
        raise RuntimeError(f"TF-IDF vocabulary too small: {tfidf.shape}")

    max_components = min(128, tfidf.shape[0] - 1, tfidf.shape[1] - 1)
    if max_components < 2:
        raise RuntimeError(f"insufficient rank for SVD: {tfidf.shape}")

    svd = TruncatedSVD(
        n_components=max_components,
        algorithm="randomized",
        n_iter=7,
        random_state=SEED,
    )
    dense = svd.fit_transform(tfidf)
    dense = l2_normalize(dense, norm="l2", axis=1)

    centroid = np.asarray(dense.mean(axis=0)).reshape(-1)
    centroid_norm = np.linalg.norm(centroid)
    if centroid_norm == 0:
        centroid_distance = np.ones(dense.shape[0], dtype=np.float64)
    else:
        centroid_unit = centroid / centroid_norm
        centroid_similarity = np.asarray(dense @ centroid_unit).reshape(-1)
        centroid_distance = 1.0 - centroid_similarity

    neighbor_count = min(6, dense.shape[0])
    nn = NearestNeighbors(metric="cosine", n_neighbors=neighbor_count)
    nn.fit(dense)
    distances, indices = nn.kneighbors(dense)

    knn5_mean_distance = np.empty(dense.shape[0], dtype=np.float64)
    for i in range(dense.shape[0]):
        nonself = [
            float(distance)
            for distance, neighbor in zip(distances[i], indices[i])
            if int(neighbor) != i
        ][:5]
        knn5_mean_distance[i] = (
            float(np.mean(nonself)) if nonself else 0.0
        )

    char_count = np.asarray([len(doc) for doc in documents], dtype=np.int64)
    token_count = np.asarray(
        [len(doc.split()) for doc in documents], dtype=np.int64
    )
    page_count = np.asarray(
        [int(row.get("page_count", 0)) for row in rows], dtype=np.int64
    )
    tfidf_nnz = np.diff(tfidf.indptr).astype(np.int64)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    representation_path = args.out_dir / "representation.npz"
    row_index_path = args.out_dir / "row_index.jsonl"
    vocabulary_path = args.out_dir / "vocabulary.json"
    idf_path = args.out_dir / "idf.npy"
    manifest_path = args.out_dir / "representation_manifest.json"

    np.savez_compressed(
        representation_path,
        dense=dense.astype(np.float32),
        centroid_cosine_distance=centroid_distance.astype(np.float32),
        knn5_mean_cosine_distance=knn5_mean_distance.astype(np.float32),
        char_count=char_count,
        token_count=token_count,
        page_count=page_count,
        tfidf_nnz=tfidf_nnz,
        explained_variance_ratio=svd.explained_variance_ratio_.astype(np.float32),
    )
    row_index_path.write_text(
        "".join(
            json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n"
            for row in row_index
        ),
        encoding="utf-8",
    )
    save_json(vocabulary_path, {term: int(index) for term, index in vectorizer.vocabulary_.items()})
    np.save(idf_path, vectorizer.idf_.astype(np.float64))

    manifest = {
        "schema_version": "0.1",
        "status": "ENGINEERING_FIXTURE_ONLY",
        "random_seed": SEED,
        "corpus_size": len(documents),
        "tfidf_shape": list(tfidf.shape),
        "svd_components": int(max_components),
        "parameters": {
            "normalization": {
                "unicode": "NFKC",
                "lowercase": True,
                "replace_urls": "URLTOKEN",
                "replace_emails": "EMAILTOKEN",
                "collapse_whitespace": True,
            },
            "tfidf": {
                "ngram_range": [1, 2],
                "min_df": 5,
                "max_df": 0.95,
                "max_features": 50000,
                "sublinear_tf": True,
                "norm": "l2",
                "token_pattern": "sklearn-default",
            },
            "svd": {
                "algorithm": "randomized",
                "n_iter": 7,
                "random_state": SEED,
            },
            "nearest_neighbors": {
                "metric": "cosine",
                "k": 5,
            },
        },
        "versions": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "scikit_learn": sklearn.__version__,
        },
        "inputs": {
            "extraction_ledger_sha256": sha256_file(args.extraction_ledger),
            "content_count": len(documents),
        },
        "outputs": {
            "representation_npz_sha256": sha256_file(representation_path),
            "row_index_jsonl_sha256": sha256_file(row_index_path),
            "vocabulary_json_sha256": sha256_file(vocabulary_path),
            "idf_npy_sha256": sha256_file(idf_path),
        },
    }
    save_json(manifest_path, manifest)

    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
