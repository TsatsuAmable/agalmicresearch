#!/usr/bin/env python3
"""Fail-closed post-hoc regime preservation audit of Phase 1C verifier output.

Reads the existing checksum-verified feasibility_baseline_audit.py result.json.
Does not re-estimate policies or claim prospective safety. No dependencies.
"""
import argparse
import json
import math
from pathlib import Path

EXPECTED_SHA = 'ceeaa4316f76f6a22a5856128f34e8c3f35693d145db756f9688eda42ee20ed2'
EXPECTED_SEEDS = set(range(20261001, 20261021))
EXPECTED_YEARS = {'2017', '2018', '2019', '2020', '2021'}


def audit(data, floor=0.95):
    if data.get('input_sha256') != EXPECTED_SHA:
        raise ValueError('Frozen database SHA-256 not verified')
    if set(data.get('seeds', [])) != EXPECTED_SEEDS:
        raise ValueError('Incomplete or altered holdout seed set')
    rows = [r for r in data['runs'] if r['policy'] == 'boundary']
    if len(rows) != 20 or {r['seed'] for r in rows} != EXPECTED_SEEDS:
        raise ValueError('Missing or duplicate boundary-policy runs')
    failures = []
    if not 0 < floor <= 1:
        raise ValueError('Invalid preservation floor')
    output = []
    for r in sorted(rows, key=lambda x: x['seed']):
        d = r.get('allocation_at_min_budget')
        if d is None or set(d.get('by_year', {})) != EXPECTED_YEARS:
            raise ValueError('Missing complete year diagnostics')
        if r.get('min_budget') not in data.get('budget_grid', []):
            raise ValueError('Qualifying budget absent from frozen grid')
        if d.get('nominal_budget') != r['min_budget']:
            raise ValueError('Allocation budget differs from qualifying budget')
        years = {}
        total_events = total_captured = total_eligible = total_selected = 0
        for year, v in sorted(d['by_year'].items()):
            n, selected = v['crossings'], v['crossings_selected']
            if not isinstance(n, int) or not isinstance(selected, int) or n < 0 or not 0 <= selected <= n:
                raise ValueError('Invalid crossing event counts')
            eligible, allocated = v['eligible'], v['selected']
            if not all(isinstance(x, int) and not isinstance(x, bool) for x in (n, selected, eligible, allocated)):
                raise ValueError('Non-integer count')
            if eligible <= 0 or not 0 <= allocated <= eligible or n > eligible or selected > allocated:
                raise ValueError('Impossible allocation counts')
            total_events += n
            total_captured += selected
            total_eligible += eligible
            total_selected += allocated
            if n == 0:
                years[year] = None
                failures.append([r['seed'], year, 'undefined: zero crossing events'])
            else:
                recall = selected / n
                if (not isinstance(v.get('recall'), (int, float)) or isinstance(v['recall'], bool)
                        or not math.isfinite(v['recall']) or abs(v['recall'] - recall) > 1e-12):
                    raise ValueError('Inconsistent per-year recall')
                years[year] = recall
                if recall < floor:
                    failures.append([r['seed'], year, f'{selected}/{n}'])
        if total_events == 0:
            raise ValueError('Undefined pooled crossing recall')
        if d.get('eligible') != total_eligible or d.get('selected') != total_selected:
            raise ValueError('Inconsistent pooled allocation counts')
        if r.get('crossing_count') != total_events or r.get('eligible_count') != total_eligible:
            raise ValueError('Inconsistent frozen cohort totals')
        if (not isinstance(d.get('actual_fraction_saved'), (int, float))
                or isinstance(d['actual_fraction_saved'], bool)
                or not math.isfinite(d['actual_fraction_saved'])
                or abs(d['actual_fraction_saved'] - (1 - total_selected / total_eligible)) > 1e-12):
            raise ValueError('Inconsistent actual review savings')
        if total_captured / total_events < data.get('target_pooled_recall', 0.95) - 1e-12:
            raise ValueError('Claimed qualifying budget does not preserve pooled target')
        output.append({'seed': r['seed'], 'nominal_budget': r['min_budget'],
                       'actual_fraction_saved': d['actual_fraction_saved'],
                       'recall_by_year': years})
    return {'status': 'FAIL' if failures else 'PASS',
            'criterion': 'per-year recall at each split pooled-qualifying budget',
            'floor': floor, 'n_splits': len(rows), 'failures': failures, 'runs': output,
            'interpretation': 'Post-hoc retrospective diagnostic; PASS does not establish prospective safety.'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('result_json', type=Path)
    p.add_argument('--out', type=Path)
    args = p.parse_args()
    result = audit(json.loads(args.result_json.read_text()))
    report = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.out:
        args.out.write_text(report)
    else:
        print(report, end='')
    raise SystemExit(0 if result['status'] == 'PASS' else 2)


if __name__ == '__main__':
    main()
