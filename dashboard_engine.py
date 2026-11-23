import sqlite3
from contextlib import closing


def get_dashboard_data(database_path):
    with closing(sqlite3.connect(database_path)) as connection:
        connection.row_factory = sqlite3.Row
        assessment = connection.execute("""
            SELECT * FROM assessment_results ORDER BY id DESC LIMIT 1
        """).fetchone()
        phishing = connection.execute("""
            SELECT * FROM quiz_results ORDER BY id DESC LIMIT 1
        """).fetchone()
        total_assessments = connection.execute(
            "SELECT COUNT(*) FROM assessment_results"
        ).fetchone()[0]
        total_quizzes = connection.execute(
            "SELECT COUNT(*) FROM quiz_results"
        ).fetchone()[0]
        assessment_history = connection.execute("""
            SELECT id, risk_percentage, risk_level, created_at
            FROM assessment_results ORDER BY id DESC LIMIT 10
        """).fetchall()
        quiz_history = connection.execute("""
            SELECT id, percentage, awareness_level, created_at
            FROM quiz_results ORDER BY id DESC LIMIT 10
        """).fetchall()

        return {
            "assessment": dict(assessment) if assessment else None,
            "phishing": dict(phishing) if phishing else None,
            "total_assessments": total_assessments,
            "total_quizzes": total_quizzes,
            "assessment_history": [dict(row) for row in reversed(assessment_history)],
            "quiz_history": [dict(row) for row in reversed(quiz_history)],
        }
