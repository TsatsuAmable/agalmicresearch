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
    def test_uniform_probability_all_exact_frozen_scales(self):
        for year,n in [(2017,10),(2018,10),(2019,10),(2020,4),(2021,10)]:
            scores=[Fraction(i,n-1) for i in range(n)]
            possible_pairs=0
            for a in scores:
                for b in scores:
                    mean2=(a+b)/2
                    count=sum(
                        (mean2<Fraction(1,2)<=(a+b+c)/3)
                        or ((a+b+c)/3<Fraction(1,2)<=mean2)
                        for c in scores
                    )
                    observed=audit.uniform_crossing_probability(year,float(mean2))
                    self.assertAlmostEqual(observed,count/n,places=12)
                    possible_pairs+=count>0
            self.assertEqual(possible_pairs,10 if year==2020 else 70)
    def test_uniform_probability_does_not_use_heldout_event(self):
        rows=[
            {"year":2017,"paper_id":"a","mean2":.5,"midpoint_crossing":False},
            {"year":2017,"paper_id":"b","mean2":.5,"midpoint_crossing":True},
        ]
        r1=audit.rank(rows,20261001,"uniform_probability")
        rows[0]["midpoint_crossing"]=True
        rows[1]["midpoint_crossing"]=False
        r2=audit.rank(rows,20261001,"uniform_probability")
        self.assertEqual([x["paper_id"] for x in r1[2017]],
                         [x["paper_id"] for x in r2[2017]])
    def test_tie_direction(self):
        self.assertTrue(audit.discrete_feasible(2017,.25))
        self.assertFalse(audit.discrete_feasible(2017,.75))
        self.assertTrue(audit.discrete_feasible(2020,.5))
    def test_budget_denominator(self):
        rows=[{"year":2017,"paper_id":str(i),"midpoint_crossing":i in (0,1)} for i in range(10)]
        ranked={2017:rows}
        self.assertEqual(audit.evaluate(ranked,.1),.5)
        self.assertEqual(audit.evaluate(ranked,.2),1.0)
        self.assertEqual(audit.min_budget(ranked),.15)  # Python round(10 * .15) selects two cases
    def test_pooled_recall_can_hide_total_regime_failure(self):
        # 19/20 crossing events preserved overall, but the second regime
        # loses its sole event. Pooled >=95% is NOT a per-regime guarantee.
        a=[{"year":2017,"paper_id":f"a{i}","midpoint_crossing":True}
           for i in range(19)]
        b=[{"year":2020,"paper_id":"b0","midpoint_crossing":True},
           {"year":2020,"paper_id":"b1","midpoint_crossing":False}]
        # At a 100% budget every event is selected, so instead exercise the
        # exact 50% selection rule with 38 cases in year 2017.
        a += [{"year":2017,"paper_id":f"n{i}","midpoint_crossing":False}
              for i in range(19)]
        ranked={2017:a,2020:[b[1],b[0]]}
        self.assertEqual(audit.evaluate(ranked,.5),19/20)
        self.assertEqual(audit.evaluate({2020:ranked[2020]},.5),0)
        self.assertEqual(audit.evaluate({2017:ranked[2017]},.5),1)
    def test_frozen_evaluator_parity_on_synthetic_years(self):
        # Exercise the original Phase 1B evaluator without needing private data.
        frozen=Path(__file__).with_name("review_value_holdout.py")
        original=audit.load(frozen)
        episodes=[]
        for year in (2017,2020,2021):
            for i in range(24):
                a=original.norm_rating(year,original.SCALES[year][i % len(original.SCALES[year])])
                b=original.norm_rating(year,original.SCALES[year][(i*3+1) % len(original.SCALES[year])])
                c=original.norm_rating(year,original.SCALES[year][(i*7+2) % len(original.SCALES[year])])
                m2=(a+b)/2
                m3=(a+b+c)/3
                episodes.append({"year":year,"paper_id":f"{year}-{i}",
                    "mean2":m2,"boundary_uncertainty":max(0,1-2*abs(m2-.5)),
                    "random_score":int(original.hash_key("route",20261001,f"{year}-{i}"),16),
                    "midpoint_crossing":(m2<.5<=m3) or (m3<.5<=m2),
                    "absolute_update":abs(m3-m2),"disagreement":abs(a-b),
                    "hybrid":0})
        self.assertGreater(sum(e["midpoint_crossing"] for e in episodes),0)
        for original_policy, local_policy in (("random","random"),("boundary_uncertainty","boundary")):
            ranked=audit.rank(episodes,20261001,local_policy)
            for budget in audit.BUDGETS:
                self.assertEqual(original.evaluate(episodes,original_policy,budget)["midpoint_crossing_recall"],
                                 audit.evaluate(ranked,budget),(original_policy,budget))

    def test_year_specific_rounding_is_not_exact_nominal_budget(self):
        # Frozen selection uses max(1, round(N_year*b)), not floor(b*N_total).
        ranked={2017:[{"year":2017,"paper_id":"a","midpoint_crossing":True}],
                2020:[{"year":2020,"paper_id":"b","midpoint_crossing":True}]}
        self.assertEqual(audit.evaluate(ranked,.05),1.0)
        # Both of two simulated third reviews selected at a nominal 5% budget.
        # RWS@95 is based on nominal grid, not exact fraction of reviews selected.
        self.assertEqual(audit.min_budget(ranked),.05)

    def test_actual_selected_denominator_and_year_events(self):
        ranked={
            2017:[{"year":2017,"paper_id":"a","midpoint_crossing":True},
                  {"year":2017,"paper_id":"b","midpoint_crossing":False},
                  {"year":2017,"paper_id":"c","midpoint_crossing":True}],
            2020:[{"year":2020,"paper_id":"d","midpoint_crossing":False}]}
        d=audit.allocation_diagnostics(ranked,.05)
        self.assertEqual(d["selected"],2)
        self.assertEqual(d["eligible"],4)
        self.assertEqual(d["actual_fraction_selected"],.5)
        self.assertEqual(d["actual_fraction_saved"],.5)
        self.assertEqual(d["by_year"]["2017"]["crossings"],2)
        self.assertEqual(d["by_year"]["2017"]["crossings_selected"],1)
        self.assertEqual(d["by_year"]["2017"]["recall"],.5)
        self.assertIsNone(d["by_year"]["2020"]["recall"])

    def test_no_event_is_not_perfect_recall(self):
        ranked={2017:[{"year":2017,"paper_id":"x","midpoint_crossing":False}]}
        self.assertIsNone(audit.evaluate(ranked,.5))
        self.assertIsNone(audit.min_budget(ranked))
if __name__=="__main__":
    unittest.main()
