#!/usr/bin/env python3
"""Exact finite-state independent checks for Phase 1C feasibility baselines."""
import importlib.util
import unittest
from fractions import Fraction
from pathlib import Path

PATH=Path(__file__).with_name("feasibility_baseline_audit.py")
spec=importlib.util.spec_from_file_location("feasibility_baseline_audit",PATH)
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class CrossingFeasibilityTests(unittest.TestCase):
    def test_all_frozen_year_scales_exhaustively(self):
        for year,n in [(2017,10),(2018,10),(2019,10),(2020,4),(2021,10)]:
            scores=[Fraction(i,n-1) for i in range(n)]
            for r1 in scores:
                for r2 in scores:
                    mean2=(r1+r2)/2
                    possible=any(
                        (mean2<Fraction(1,2)<=(r1+r2+r3)/3)
                        or ((r1+r2+r3)/3<Fraction(1,2)<=mean2)
                        for r3 in scores
                    )
                    self.assertEqual(possible,audit.discrete_feasible(year,float(mean2)),
                        (year,r1,r2))
                    if possible:
                        self.assertTrue(audit.feasible(float(mean2)))
    def test_tie_direction(self):
        self.assertTrue(audit.discrete_feasible(2017,.25))
        self.assertFalse(audit.discrete_feasible(2017,.75))
        self.assertTrue(audit.discrete_feasible(2020,.5))
    def test_budget_denominator(self):
        rows=[{"year":2017,"paper_id":str(i),"midpoint_crossing":i in (0,1)} for i in range(10)]
        ranked={2017:rows}
        self.assertEqual(audit.evaluate(ranked,.1),.5)
        self.assertEqual(audit.evaluate(ranked,.2),1.0)
        self.assertEqual(audit.min_budget(ranked),.2)
if __name__=="__main__":
    unittest.main()
