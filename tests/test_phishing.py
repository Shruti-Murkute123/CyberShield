
import unittest
from phishing_quiz import QUESTIONS, evaluate_quiz


class TestPhishingQuiz(unittest.TestCase):

    def test_all_correct(self):
        answers = {
            question["id"]: question["answer"]
            for question in QUESTIONS
        }

        result = evaluate_quiz(answers)

        self.assertEqual(result["score"], 5)
        self.assertEqual(result["percentage"], 100)
        self.assertEqual(
            result["awareness_level"],
            "Strong Awareness"
        )

    def test_all_wrong(self):
        answers = {}

        for question in QUESTIONS:
            answers[question["id"]] = next(
                option["value"]
                for option in question["options"]
                if option["value"] != question["answer"]
            )

        result = evaluate_quiz(answers)

        self.assertEqual(result["score"], 0)
        self.assertEqual(result["awareness_level"], "At Risk")

    def test_missing_answer(self):
        with self.assertRaises(ValueError):
            evaluate_quiz({})


if __name__ == "__main__":
    unittest.main()
