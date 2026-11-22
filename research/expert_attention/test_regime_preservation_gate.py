#!/usr/bin/env python3
"""Synthetic adversarial regression tests for the fail-closed per-year gate.

No frozen ICLR data are used. Execute: python -m unittest
research/expert_attention/test_regime_preservation_gate.py
"""
import unittest
from copy import deepcopy
try:
    from . import regime_preservation_gate as gate
except ImportError:
    import regime_preservation_gate as gate


def fixture():
    years = {y: dict(eligible=100, selected=95, crossings=20,
                     crossings_selected=20, recall=1.0)
             for y in sorted(gate.EXPECTED_YEARS)}
    runs = []
    for seed in sorted(gate.EXPECTED_SEEDS):
        runs.append(dict(seed=seed, policy='boundary', min_budget=.95,
                         crossing_count=100, eligible_count=500,
                         allocation_at_min_budget=dict(
                             nominal_budget=.95, eligible=500, selected=475,
                             actual_fraction_saved=.05, by_year=deepcopy(years))))
    return dict(input_sha256=gate.EXPECTED_SHA,
                seeds=sorted(gate.EXPECTED_SEEDS), budget_grid=[.95],
                target_pooled_recall=.95, runs=runs)


class RegimePreservationGateTests(unittest.TestCase):
    def test_valid_synthetic_pass(self):
        self.assertEqual(gate.audit(fixture())['status'], 'PASS')

    def test_pooled_99_percent_can_hide_zero_regime_recall(self):
        data = fixture()
        for row in data['runs']:
            years = row['allocation_at_min_budget']['by_year']
            for year in years.values():
                year.update(crossings=1, crossings_selected=1, recall=1.0)
            years['2017'].update(crossings=91, crossings_selected=91)
            years['2020'].update(crossings_selected=0, recall=0.0)
            row['crossing_count'] = 95
        report = gate.audit(data)
        self.assertEqual(report['status'], 'FAIL')
        self.assertEqual(len(report['failures']), 20)
        self.assertTrue(all(f[1] == '2020' for f in report['failures']))

    def test_zero_event_stratum_is_not_perfect_recall(self):
        data = fixture()
        for row in data['runs']:
            row['allocation_at_min_budget']['by_year']['2020'].update(
                crossings=0, crossings_selected=0, recall=None)
            row['crossing_count'] = 80
        report = gate.audit(data)
        self.assertEqual(report['status'], 'FAIL')
        self.assertEqual(len(report['failures']), 20)

    def test_inconsistent_selected_counts_rejected(self):
        data = fixture()
        data['runs'][0]['allocation_at_min_budget']['selected'] = 476
        with self.assertRaises(ValueError):
            gate.audit(data)

    def test_duplicate_seed_rejected(self):
        data = fixture()
        data['runs'][1]['seed'] = data['runs'][0]['seed']
        with self.assertRaises(ValueError):
            gate.audit(data)

    def test_nan_recall_rejected(self):
        data = fixture()
        data['runs'][0]['allocation_at_min_budget']['by_year']['2020']['recall'] = float('nan')
        with self.assertRaises(ValueError):
            gate.audit(data)

    def test_infinite_recall_rejected(self):
        data = fixture()
        data['runs'][0]['allocation_at_min_budget']['by_year']['2020']['recall'] = float('inf')
        with self.assertRaises(ValueError):
            gate.audit(data)

    def test_nan_savings_rejected(self):
        data = fixture()
        data['runs'][0]['allocation_at_min_budget']['actual_fraction_saved'] = float('nan')
        with self.assertRaises(ValueError):
            gate.audit(data)

    def test_boolean_recall_rejected(self):
        data = fixture()
        data['runs'][0]['allocation_at_min_budget']['by_year']['2020']['recall'] = True
        with self.assertRaises(ValueError):
            gate.audit(data)

    def test_nan_pooled_target_rejected(self):
        data = fixture()
        data['target_pooled_recall'] = float('nan')
        with self.assertRaises(ValueError):
            gate.audit(data)

    def test_missing_pooled_target_rejected(self):
        data = fixture()
        del data['target_pooled_recall']
        with self.assertRaises(ValueError):
            gate.audit(data)

    def test_nan_floor_rejected(self):
        with self.assertRaises(ValueError):
            gate.audit(fixture(), floor=float('nan'))

    def test_infinite_floor_rejected(self):
        with self.assertRaises(ValueError):
            gate.audit(fixture(), floor=float('inf'))


if __name__ == '__main__':
    unittest.main()
