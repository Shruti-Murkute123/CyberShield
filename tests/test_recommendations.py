
import unittest
from risk_engine import calculate_risk
from recommendation_engine import generate_recommendations


class TestRecommendations(unittest.TestCase):

    def test_five_categories(self):
        answers = {f"q{i}": "No" for i in range(1, 16)}
        result = calculate_risk(answers)

        recommendations = generate_recommendations(result)

        self.assertEqual(len(recommendations), 5)

    def test_critical_priority(self):
        answers = {f"q{i}": "No" for i in range(1, 16)}
        result = calculate_risk(answers)

        recommendations = generate_recommendations(result)

        for item in recommendations:
            self.assertEqual(item["priority"], "Critical")

    def test_recommendations_exist(self):
        answers = {f"q{i}": "Partially" for i in range(1, 16)}
        result = calculate_risk(answers)

        recommendations = generate_recommendations(result)

        for item in recommendations:
            self.assertEqual(len(item["recommendations"]), 3)


if __name__ == "__main__":
    unittest.main()
