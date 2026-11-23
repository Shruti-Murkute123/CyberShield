# CyberShield — Cybersecurity Risk Assessment & Awareness Platform

CyberShield is a web-based cybersecurity awareness and risk assessment platform built with Python, Flask, SQLite, HTML, CSS, and JavaScript.

## Features

- **Cybersecurity Risk Assessment:** 15-question assessment across five security categories.
- **Risk Scoring Engine:** Calculates overall and category-level risk scores.
- **Phishing Awareness Quiz:** Interactive scenarios with scoring and feedback.
- **Password Security:** Password strength checklist and secure random password generator.
- **Personalized Recommendations:** Prioritized security improvement guidance.
- **Interactive Dashboard:** Visualizes assessment and phishing quiz history using Chart.js.
- **PDF Reports:** Generates downloadable cybersecurity readiness reports.
- **SQLite Storage:** Stores assessment and phishing quiz results.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| Charts | Chart.js |
| Reports | ReportLab |
| Testing | Python unittest |

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Shruti-Murkute123/CyberShield.git
cd CyberShield
```

2. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the application:

```bash
python app.py
```

5. Open `http://127.0.0.1:5000` in your browser.

## Automated Testing

```bash
python -m unittest discover -s tests -v
```

The project includes 15 automated unit and integration tests.



## Security and Privacy

- Actual SQLite database files and private datasets are excluded from version control.
- The password analyzer runs in the browser without storing entered passwords.
- Use synthetic demonstration data when sharing screenshots or publishing examples.
- This application is an educational prototype, not a substitute for a professional security audit.

## Future Improvements

- User authentication and role-based access
- Per-user assessment history
- Production database support
- Enhanced reporting and export options
- Stronger server-side security controls

## Disclaimer

CyberShield provides educational cybersecurity guidance. Risk scores and recommendations are simplified indicators and do not constitute a professional security assessment.