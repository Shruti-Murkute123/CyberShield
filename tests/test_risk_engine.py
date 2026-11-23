import unittest
from risk_engine import calculate_risk


class TestRiskEngine(unittest.TestCase):
    def test_all_yes(self):
        answers = {f"q{i}": "Yes" for i in range(1, 16)}
        result = calculate_risk(answers)
        self.assertEqual(result["total_score"], 0)
        self.assertEqual(result["risk_level"], "Low")

    def test_all_partially(self):
        answers = {f"q{i}": "Partially" for i in range(1, 16)}
        result = calculate_risk(answers)
        self.assertEqual(result["total_score"], 75)
        self.assertEqual(result["risk_level"], "High")

    def test_all_no(self):
        answers = {f"q{i}": "No" for i in range(1, 16)}
        result = calculate_risk(answers)
        self.assertEqual(result["total_score"], 150)
        self.assertEqual(result["risk_level"], "Critical")

    def test_missing_answer(self):
        answers = {f"q{i}": "Yes" for i in range(1, 15)}
        with self.assertRaises(ValueError):
            calculate_risk(answers)


if __name__ == "__main__":
    unittest.main()
