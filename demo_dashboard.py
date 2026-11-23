"""Entirely fictional dashboard data for the public portfolio demo."""


def get_demo_dashboard_data():
    return {
        'assessment': {
            'id': 4, 'total_score': 45, 'maximum_score': 150,
            'risk_percentage': 30, 'risk_level': 'Medium',
            'created_at': '2026-11-20T10:00:00',
        },
        'phishing': {
            'id': 4, 'score': 4, 'total': 5,
            'percentage': 80, 'awareness_level': 'High',
            'created_at': '2026-11-20T10:15:00',
        },
        'total_assessments': 4,
        'total_quizzes': 4,
        'assessment_history': [
            {'id': 1, 'risk_percentage': 60, 'risk_level': 'High', 'created_at': '2026-11-17T10:00:00'},
            {'id': 2, 'risk_percentage': 50, 'risk_level': 'High', 'created_at': '2026-11-18T10:00:00'},
            {'id': 3, 'risk_percentage': 40, 'risk_level': 'Medium', 'created_at': '2026-11-19T10:00:00'},
            {'id': 4, 'risk_percentage': 30, 'risk_level': 'Medium', 'created_at': '2026-11-20T10:00:00'},
        ],
        'quiz_history': [
            {'id': 1, 'percentage': 40, 'awareness_level': 'Low', 'created_at': '2026-11-17T10:15:00'},
            {'id': 2, 'percentage': 60, 'awareness_level': 'Medium', 'created_at': '2026-11-18T10:15:00'},
            {'id': 3, 'percentage': 60, 'awareness_level': 'Medium', 'created_at': '2026-11-19T10:15:00'},
            {'id': 4, 'percentage': 80, 'awareness_level': 'High', 'created_at': '2026-11-20T10:15:00'},
        ],
    }
