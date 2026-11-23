import os
import sqlite3
from contextlib import closing
from datetime import datetime
from io import BytesIO

from flask import Flask, jsonify, render_template, request, send_file
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from dashboard_engine import get_dashboard_data
from demo_dashboard import get_demo_dashboard_data
from phishing_quiz import QUESTIONS, evaluate_quiz
from recommendation_engine import RECOMMENDATIONS, generate_recommendations
from risk_engine import calculate_risk

app = Flask(__name__)
DEMO_MODE = os.environ.get('DEMO_MODE', 'false').strip().lower() == 'true'
DATABASE_PATH = os.path.join(app.root_path, 'database', 'cybershield.db')


def initialize_database():
    if DEMO_MODE:
        return
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        with connection:
            connection.execute('''
                CREATE TABLE IF NOT EXISTS quiz_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    score INTEGER NOT NULL,
                    total INTEGER NOT NULL,
                    percentage INTEGER NOT NULL,
                    awareness_level TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            connection.execute('''
                CREATE TABLE IF NOT EXISTS assessment_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    total_score INTEGER NOT NULL,
                    maximum_score INTEGER NOT NULL,
                    risk_percentage REAL NOT NULL,
                    risk_level TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')


initialize_database()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', demo_mode=DEMO_MODE)


@app.route('/assessment')
def assessment():
    return render_template('assessment.html')


@app.route('/phishing')
def phishing():
    return render_template('phishing.html')


@app.route('/password')
def password_security():
    return render_template('password.html')


@app.route('/recommendations')
def recommendations_page():
    return render_template('recommendations.html')


@app.route('/calculate-risk', methods=['POST'])
def calculate_risk_api():
    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({'error': 'Invalid assessment data'}), 400
        result = calculate_risk(data)
        result['recommendations'] = generate_recommendations(result)
        if not DEMO_MODE and request.args.get('save', '1') == '1':
            with closing(sqlite3.connect(DATABASE_PATH)) as connection:
                with connection:
                    connection.execute('''
                        INSERT INTO assessment_results
                        (total_score, maximum_score, risk_percentage, risk_level, created_at)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        result['total_score'], result['maximum_score'],
                        result['risk_percentage'], result['risk_level'],
                        datetime.now().isoformat()
                    ))
        return jsonify(result)
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    except Exception:
        app.logger.exception('Risk calculation failed')
        return jsonify({'error': 'An internal error occurred'}), 500


@app.route('/api/phishing-quiz', methods=['GET', 'POST'])
def phishing_quiz_api():
    if request.method == 'GET':
        return jsonify([
            {'id': q['id'], 'question': q['question'], 'options': q['options']}
            for q in QUESTIONS
        ])
    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({'error': 'Invalid quiz data'}), 400
        result = evaluate_quiz(data.get('answers'))
        if not DEMO_MODE:
            with closing(sqlite3.connect(DATABASE_PATH)) as connection:
                with connection:
                    connection.execute('''
                        INSERT INTO quiz_results
                        (score, total, percentage, awareness_level, created_at)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        result['score'], result['total'], result['percentage'],
                        result['awareness_level'], datetime.now().isoformat()
                    ))
        return jsonify(result)
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    except Exception:
        app.logger.exception('Quiz processing failed')
        return jsonify({'error': 'Unable to process quiz'}), 500


@app.route('/api/dashboard')
def dashboard_api():
    try:
        data = get_demo_dashboard_data() if DEMO_MODE else get_dashboard_data(DATABASE_PATH)
        return jsonify(data)
    except Exception:
        app.logger.exception('Dashboard loading failed')
        return jsonify({'error': 'Unable to load dashboard'}), 500


@app.route('/download-report')
def download_report():
    if DEMO_MODE:
        return jsonify({'message': 'Reports are disabled in public demo mode.'}), 403
    try:
        data = get_dashboard_data(DATABASE_PATH)
        if not data['assessment']:
            return jsonify({'error': 'Complete an assessment before downloading a report.'}), 404
        assessment = data['assessment']
        phishing = data['phishing']
        buffer = BytesIO()
        document = SimpleDocTemplate(buffer, pagesize=(595, 842))
        styles = getSampleStyleSheet()
        elements = [
            Paragraph('CyberShield Security Readiness Report', styles['Title']),
            Spacer(1, 20),
            Paragraph('Educational cybersecurity assessment report', styles['Normal']),
            Spacer(1, 20),
        ]
        rows = [
            ['Metric', 'Result'],
            ['Overall Risk', assessment['risk_level']],
            ['Risk Percentage', f"{assessment['risk_percentage']}%"],
            ['Risk Score', f"{assessment['total_score']}/{assessment['maximum_score']}"],
            ['Assessment Date', assessment['created_at']],
        ]
        if phishing:
            rows.extend([
                ['Latest Phishing Awareness', f"{phishing['percentage']}%"],
                ['Awareness Level', phishing['awareness_level']],
            ])
        table = Table(rows, colWidths=[230, 250])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#17365D')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.extend([table, Spacer(1, 25), Paragraph('Recommended Security Actions', styles['Heading2'])])
        for category, actions in RECOMMENDATIONS.items():
            elements.append(Paragraph(category, styles['Heading3']))
            for action in actions:
                elements.append(Paragraph('- ' + action, styles['Normal']))
            elements.append(Spacer(1, 10))
        elements.extend([
            Spacer(1, 15),
            Paragraph(
                'Disclaimer: This is a preliminary educational assessment, not a '
                'professional security audit. Recommendations are general guidance.',
                styles['Italic'],
            ),
        ])
        document.build(elements)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True,
                         download_name='CyberShield_Security_Report.pdf',
                         mimetype='application/pdf')
    except Exception:
        app.logger.exception('Report generation failed')
        return jsonify({'error': 'Unable to generate report'}), 500


if __name__ == '__main__':
    app.run(debug=False)
