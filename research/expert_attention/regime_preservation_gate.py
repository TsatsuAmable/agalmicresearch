#!/usr/bin/env python3
"""Fail-closed post-hoc regime preservation audit of Phase 1C verifier output.

Reads the existing checksum-verified feasibility_baseline_audit.py result.json.
Does not re-estimate policies or claim prospective safety. No dependencies.
"""
import argparse
import json
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
    output = []
    for r in sorted(rows, key=lambda x: x['seed']):
        d = r.get('allocation_at_min_budget')
        if d is None or set(d.get('by_year', {})) != EXPECTED_YEARS:
            raise ValueError('Missing complete year diagnostics')
        years = {}
        for year, v in sorted(d['by_year'].items()):
            n, selected = v['crossings'], v['crossings_selected']
            if not isinstance(n, int) or not isinstance(selected, int) or n < 0 or not 0 <= selected <= n:
                raise ValueError('Invalid crossing event counts')
            if n == 0:
                years[year] = None
                failures.append([r['seed'], year, 'undefined: zero crossing events'])
            else:
                recall = selected / n
                if v.get('recall') is None or abs(v['recall'] - recall) > 1e-12:
                    raise ValueError('Inconsistent per-year recall')
                years[year] = recall
                if recall < floor:
                    failures.append([r['seed'], year, f'{selected}/{n}'])
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
