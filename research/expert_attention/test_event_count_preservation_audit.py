"""Independent synthetic tests; NOT empirical ICLR reproduction."""
import unittest
from event_count_preservation_audit import audit, wilson

class PreservationAuditTests(unittest.TestCase):
    def test_pooled_pass_does_not_imply_regime_pass(self):
        result = audit({"regimes":[
            {"name":"large","captured":990,"crossings":1000},
            {"name":"small","captured":0,"crossings":10}]})
        self.assertGreaterEqual(result["pooled"]["recall"], .95)
        self.assertFalse(result["all_regimes_point_floor_pass"])
    def test_point_pass_does_not_imply_lower_bound_pass(self):
        result = audit({"regimes":[{"name":"small","captured":19,"crossings":20}]})
        self.assertTrue(result["all_regimes_point_floor_pass"])
        self.assertFalse(result["all_regimes_lower_bound_floor_pass"])
    def test_invalid_counts_rejected(self):
        for k,n in [(1,0),(3,2),(-1,4),(1.2,2)]:
            with self.subTest(k=k,n=n), self.assertRaises(ValueError):
                wilson(k,n)
    def test_identical_names_rejected(self):
        with self.assertRaises(ValueError):
            audit({"regimes":[{"name":"a","captured":1,"crossings":1},
                              {"name":"a","captured":1,"crossings":1}]})
if __name__ == "__main__":
    unittest.main()
