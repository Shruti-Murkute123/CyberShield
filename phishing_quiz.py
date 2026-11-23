
# CyberShield - Phishing Awareness Quiz

QUESTIONS = [
    {
        "id": "q1",
        "question": "You receive an email saying your bank account will be blocked unless you verify your details immediately. What should you do?",
        "options": [
            {"value": "A", "label": "Click the link immediately"},
            {"value": "B", "label": "Reply with your bank details"},
            {"value": "C", "label": "Contact the bank using its official website or number"},
            {"value": "D", "label": "Forward the email to colleagues"}
        ],
        "answer": "C",
        "explanation": "Urgent messages requesting sensitive information are common phishing tactics. Contact the bank through a trusted official channel."
    },
    {
        "id": "q2",
        "question": "Someone claiming to be IT support asks you to share your one-time password (OTP). What should you do?",
        "options": [
            {"value": "A", "label": "Share the OTP if they sound genuine"},
            {"value": "B", "label": "Never share the OTP and report the request"},
            {"value": "C", "label": "Send the OTP through email"},
            {"value": "D", "label": "Share it after checking their display name"}
        ],
        "answer": "B",
        "explanation": "An OTP is a private authentication code. Never disclose it to another person, even someone claiming to be IT support."
    },
    {
        "id": "q3",
        "question": "An email displays your CEO's name, but the sender address belongs to an unfamiliar domain. What is the safest action?",
        "options": [
            {"value": "A", "label": "Trust the display name"},
            {"value": "B", "label": "Open every attachment"},
            {"value": "C", "label": "Check the sender and verify through a trusted channel"},
            {"value": "D", "label": "Reply with confidential company information"}
        ],
        "answer": "C",
        "explanation": "Display names can be impersonated. Verify the actual sender address and confirm unusual requests independently."
    },
    {
        "id": "q4",
        "question": "You receive an unexpected email attachment asking you to enable macros to view an invoice. What should you do?",
        "options": [
            {"value": "A", "label": "Enable macros immediately"},
            {"value": "B", "label": "Download it on your personal laptop"},
            {"value": "C", "label": "Disable security software and open it"},
            {"value": "D", "label": "Avoid enabling macros and verify the attachment with the sender"}
        ],
        "answer": "D",
        "explanation": "Unexpected attachments requesting macros can execute malicious code. Verify the file through a trusted channel before opening it."
    },
    {
        "id": "q5",
        "question": "A website uses HTTPS and displays a padlock icon. Does this guarantee that the website is legitimate?",
        "options": [
            {"value": "A", "label": "Yes, every HTTPS website is trustworthy"},
            {"value": "B", "label": "No, HTTPS does not guarantee that a website is legitimate"},
            {"value": "C", "label": "Yes, it guarantees the website has no malware"},
            {"value": "D", "label": "Yes, it guarantees the website belongs to a bank"}
        ],
        "answer": "B",
        "explanation": "HTTPS encrypts the connection, but phishing websites can also use HTTPS. Always verify the website's domain and identity."
    }
]


def evaluate_quiz(answers):

    if not isinstance(answers, dict):
        raise ValueError("Invalid quiz answers")

    if set(answers.keys()) != {q["id"] for q in QUESTIONS}:
        raise ValueError("Please answer all quiz questions")

    score = 0
    feedback = []

    for question in QUESTIONS:

        selected = answers.get(question["id"])

        valid_options = [
            option["value"] for option in question["options"]
        ]

        if selected not in valid_options:
            raise ValueError("Invalid answer submitted")

        correct = selected == question["answer"]

        if correct:
            score += 1

        feedback.append({
            "question_id": question["id"],
            "selected": selected,
            "correct_answer": question["answer"],
            "is_correct": correct,
            "explanation": question["explanation"]
        })

    percentage = round((score / len(QUESTIONS)) * 100)

    if percentage >= 80:
        level = "Strong Awareness"
    elif percentage >= 60:
        level = "Good Awareness"
    elif percentage >= 40:
        level = "Needs Improvement"
    else:
        level = "At Risk"

    return {
        "score": score,
        "total": len(QUESTIONS),
        "percentage": percentage,
        "awareness_level": level,
        "feedback": feedback
    }
