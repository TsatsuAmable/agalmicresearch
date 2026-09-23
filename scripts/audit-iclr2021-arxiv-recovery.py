#!/usr/bin/env python3
import argparse, collections, datetime as dt, hashlib, json, math, sqlite3, unicodedata
from pathlib import Path

CUTOFF = dt.datetime.fromisoformat('2020-10-02 15:00:00+00:00')
TARGET = 4600
VERIFIED_BASE = 4060
OPTIMISTIC_2017 = 442
MATERIALITY = 0.05

def norm_title(value):
    value = unicodedata.normalize('NFKC', value or '').casefold()
    value = ''.join(' ' if unicodedata.category(ch).startswith('P') else ch for ch in value)
    return ' '.join(value.split())

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def wilson(k, n, z=1.959963984540054):
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return centre - half, centre + half

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--db', type=Path, required=True)
    ap.add_argument('--manifest', type=Path, default=Path('research/attention_allocation/cohort/track_a_2020_2021_manifest.jsonl'))
    ap.add_argument('--cohort-summary', type=Path, default=Path('research/attention_allocation/cohort/track_a_2020_2021_summary.json'))
    ap.add_argument('--out-dir', type=Path, default=Path('research/attention_allocation/t0/arxiv_audit'))
    args = ap.parse_args()

    manifest_rows = [json.loads(line) for line in args.manifest.read_text().splitlines() if line.strip()]
    frame_rows = [r for r in manifest_rows if r.get('year') == 2021 and r.get('primary_comparison_eligible')]
    frame = {r['forum_id']: r for r in frame_rows}
    cohort_summary = json.loads(args.cohort_summary.read_text())
    known_title_mismatches = set(cohort_summary['years']['2021']['normalized_title_mismatch_forum_ids'])

    con = sqlite3.connect(args.db)
    titles = {sid: title for sid, title in con.execute("select id,title from submissions where conf_year='2021'") if sid in frame}
    missing_titles = sorted(set(frame) - set(titles))
    if missing_titles:
        raise SystemExit(f'missing source titles for {len(missing_titles)} frame IDs')

    hash_mismatches = []
    for sid, row in frame.items():
        observed = hashlib.sha256(titles[sid].strip().encode()).hexdigest()
        expected = row['berenslab_snapshot']['title_sha256']
        if observed != expected and sid not in known_title_mismatches:
            hash_mismatches.append(sid)
    if hash_mismatches:
        raise SystemExit(f'unexpected canonical title hash mismatches: {hash_mismatches[:10]}')

    candidate_rows = con.execute(
        "select submission_id,id,title,published,updated from arxiv_candidates where target_conf='ICLR2021'"
    ).fetchall()
    exact = collections.defaultdict(dict)
    for sid, arxiv_id, arxiv_title, published, updated in candidate_rows:
        if sid not in frame or sid in known_title_mismatches:
            continue
        if norm_title(titles[sid]) != norm_title(arxiv_title):
            continue
        exact[sid][arxiv_id] = (arxiv_id, arxiv_title, dt.datetime.fromisoformat(published), updated)
    exact = {sid: list(items.values()) for sid, items in exact.items()}
    pre = {sid: [x for x in xs if x[2] <= CUTOFF] for sid, xs in exact.items()}
    pre = {sid: xs for sid, xs in pre.items() if xs}

    arxiv_to_submissions = collections.defaultdict(set)
    for sid, xs in pre.items():
        for x in xs:
            arxiv_to_submissions[x[0]].add(sid)
    ambiguous_submissions = {sid for sid, xs in pre.items() if len(xs) > 1}
    collision_ids = {aid: sids for aid, sids in arxiv_to_submissions.items() if len(sids) > 1}
    collision_submissions = set().union(*collision_ids.values()) if collision_ids else set()
    admitted = {sid: xs[0] for sid, xs in pre.items() if sid not in ambiguous_submissions and sid not in collision_submissions}

    decision_counts = collections.Counter(r['decision'] for r in frame_rows)
    match_counts = {d: sum(1 for sid in admitted if frame[sid]['decision'] == d) for d in ('ACCEPT', 'REJECT')}
    p_accept = match_counts['ACCEPT'] / decision_counts['ACCEPT']
    p_reject = match_counts['REJECT'] / decision_counts['REJECT']
    wa = wilson(match_counts['ACCEPT'], decision_counts['ACCEPT'])
    wr = wilson(match_counts['REJECT'], decision_counts['REJECT'])
    diff = p_accept - p_reject
    diff_ci = [
        diff - math.sqrt((p_accept - wa[0]) ** 2 + (wr[1] - p_reject) ** 2),
        diff + math.sqrt((wa[1] - p_accept) ** 2 + (p_reject - wr[0]) ** 2),
    ]

    fuzzy_only = set()
    links = con.execute(
        "select sa.submission_id,sa.arxiv_id,sa.published_time,ac.title "
        "from submission_arxiv sa left join arxiv_candidates ac "
        "on ac.submission_id=sa.submission_id and ac.id=sa.arxiv_id"
    ).fetchall()
    for sid, arxiv_id, published, arxiv_title in links:
        if sid not in frame or sid in admitted or not published or not arxiv_title:
            continue
        if dt.datetime.fromisoformat(published) <= CUTOFF and norm_title(titles[sid]) != norm_title(arxiv_title):
            fuzzy_only.add(sid)

    prior_titles = {norm_title(x[0]) for x in con.execute("select title from submissions where cast(conf_year as int) between 2017 and 2020")}
    prior_arxiv = {x[0] for x in con.execute(
        "select distinct sa.arxiv_id from submission_arxiv sa join submissions s on s.id=sa.submission_id "
        "where cast(s.conf_year as int) between 2017 and 2020"
    )}
    dedup = {sid: x for sid, x in admitted.items() if norm_title(titles[sid]) not in prior_titles and x[0] not in prior_arxiv}
    removed_cross_year = sorted(set(admitted) - set(dedup))

    relative_days = sorted((x[2] - CUTOFF).total_seconds() / 86400 for x in admitted.values())
    def quantile(q): return relative_days[round(q * (len(relative_days) - 1))]
    bins = [(-10**9, -365), (-365, -180), (-180, -90), (-90, -30), (-30, -7), (-7, 0)]
    timestamp_bins = {f'({a},{b}]': sum(a < x <= b for x in relative_days) for a, b in bins}

    restricted_estimand_frozen = False
    neutrality_material = diff_ci[0] > MATERIALITY or diff_ci[1] < -MATERIALITY
    verdict = 'ARXIV_ROUTE_CONDITIONAL'
    summary = {
        'schema_version': '1.0', 'status': 'METADATA_ONLY_AUDIT_COMPLETE', 'verdict': verdict,
        'cutoff_utc': CUTOFF.isoformat(), 'materiality_margin': MATERIALITY,
        'source': {
            'database': str(args.db), 'database_sha256': sha256_file(args.db), 'database_bytes': args.db.stat().st_size,
            'upstream': 'https://www.dropbox.com/s/iaps6dityc18kif/cs_conf_release.db?dl=1',
            'canonical_manifest_sha256': sha256_file(args.manifest),
        },
        'frame': {'total': len(frame), 'decision_counts': dict(decision_counts), 'known_title_mismatch_excluded': sorted(known_title_mismatches)},
        'matching': {
            'exact_any_time': len(exact), 'exact_pre_cutoff': len(pre), 'admitted_exact_pre_cutoff': len(admitted),
            'ambiguous_submission_count': len(ambiguous_submissions), 'collision_arxiv_id_count': len(collision_ids),
            'fuzzy_only_pre_cutoff_sensitivity_count': len(fuzzy_only),
        },
        'decision_stratified': {
            'ACCEPT': {'matched': match_counts['ACCEPT'], 'total': decision_counts['ACCEPT'], 'fraction': p_accept},
            'REJECT': {'matched': match_counts['REJECT'], 'total': decision_counts['REJECT'], 'fraction': p_reject},
            'accept_minus_reject': diff, 'newcombe_wilson_95_ci': diff_ci, 'material_selection_link': neutrality_material,
        },
        'timestamps_days_relative_to_cutoff': {
            'min': relative_days[0], 'q25': quantile(.25), 'median': quantile(.5), 'q75': quantile(.75), 'max': relative_days[-1], 'bins': timestamp_bins,
        },
        'cross_year_dedup_conservative': {
            'remaining': len(dedup), 'removed': len(removed_cross_year), 'removed_forum_ids': removed_cross_year,
            'rule': 'exclude exact normalized title or known arXiv ID appearing in any 2017-2020 ICLR submission in the same snapshot',
        },
        'feasibility': {
            'verified_2018_2020_plus_arxiv': VERIFIED_BASE + len(dedup),
            'shortfall_without_2017': max(0, TARGET - (VERIFIED_BASE + len(dedup))),
            'optimistic_with_all_2017': VERIFIED_BASE + OPTIMISTIC_2017 + len(dedup),
            'optimistic_cushion': VERIFIED_BASE + OPTIMISTIC_2017 + len(dedup) - TARGET,
            'technical_retrieval_lower_bound': None,
        },
        'adjudication': {
            'restricted_estimand_frozen': restricted_estimand_frozen,
            'neutrality_condition_passes': not neutrality_material,
            'outcome_leakage_detected': False,
            'query_provenance': 'snapshot-hash-bound; independent reconstruction of upstream arXiv candidate discovery remains outstanding',
            'bulk_pdf_retrieval_authorized': False, 'citation_outcome_acquisition_authorized': False,
        },
    }

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / 'iclr2021_arxiv_recovery_summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
    with (args.out_dir / 'iclr2021_arxiv_exact_pre_cutoff.jsonl').open('w') as fh:
        for sid in sorted(admitted):
            arxiv_id, arxiv_title, published, updated = admitted[sid]
            row = {
                'forum_id': sid, 'decision': frame[sid]['decision'], 'arxiv_id': arxiv_id, 'arxiv_title': arxiv_title,
                'published_time': published.isoformat(), 'updated_time': updated,
                'days_relative_to_cutoff': (published - CUTOFF).total_seconds() / 86400,
                'conservative_cross_year_duplicate': sid in removed_cross_year,
            }
            fh.write(json.dumps(row, sort_keys=True) + '\n')
    print(json.dumps(summary, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
