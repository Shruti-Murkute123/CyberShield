import os
import sqlite3
import tempfile
import unittest
from contextlib import closing
from unittest.mock import patch

import app as cyber_app
from phishing_quiz import QUESTIONS


class TestFlaskIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_database = os.path.join(self.temp_dir.name, "test_cybershield.db")
        self.database_patch = patch.object(cyber_app, "DATABASE_PATH", self.test_database)
        self.database_patch.start()
        cyber_app.initialize_database()
        cyber_app.app.config["TESTING"] = True
        self.client = cyber_app.app.test_client()

    def tearDown(self):
        self.database_patch.stop()
        self.temp_dir.cleanup()

    def get_count(self, table):
        with closing(sqlite3.connect(self.test_database)) as connection:
            return connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    def test_home_page(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_assessment_saves_result(self):
        answers = {f"q{i}": "Yes" for i in range(1, 16)}
        response = self.client.post("/calculate-risk", json=answers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_count("assessment_results"), 1)

    def test_recommendations_do_not_duplicate(self):
        answers = {f"q{i}": "Yes" for i in range(1, 16)}
        response = self.client.post("/calculate-risk?save=0", json=answers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()["recommendations"]), 5)
        self.assertEqual(self.get_count("assessment_results"), 0)

    def test_phishing_quiz_saves_result(self):
        answers = {question["id"]: question["answer"] for question in QUESTIONS}
        response = self.client.post("/api/phishing-quiz", json={"answers": answers})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_count("quiz_results"), 1)

    def test_invalid_assessment(self):
        response = self.client.post("/calculate-risk", json={"q1": "Invalid"})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
