
# CyberShield - Risk Scoring Engine

RISK_POINTS = {
    "Yes": 0,
    "Partially": 5,
    "No": 10
}

CATEGORIES = {
    "Password Security": [1, 2, 3],
    "Network Security": [4, 5, 6],
    "Data Protection": [7, 8, 9],
    "Access Control": [10, 11, 12],
    "Backup & Recovery": [13, 14, 15]
}


def calculate_risk(answers):

    total_risk = 0
    category_results = {}

    # Calculate category-wise risk

    for category, question_numbers in CATEGORIES.items():

        category_score = 0

        for number in question_numbers:

            answer = answers.get(f"q{number}")

            if answer not in RISK_POINTS:
                raise ValueError(
                    f"Invalid or missing answer for q{number}"
                )

            points = RISK_POINTS[answer]

            category_score += points

        category_percentage = (
            category_score / 30
        ) * 100

        category_results[category] = {
            "score": category_score,
            "percentage": round(category_percentage, 2)
        }

        total_risk += category_score

    # Calculate overall risk percentage

    risk_percentage = round(
        (total_risk / 150) * 100, 2
    )

    # Determine risk level

    if risk_percentage <= 20:
        risk_level = "Low"

    elif risk_percentage <= 40:
        risk_level = "Medium"

    elif risk_percentage <= 70:
        risk_level = "High"

    else:
        risk_level = "Critical"

    return {
        "total_score": total_risk,
        "maximum_score": 150,
        "risk_percentage": risk_percentage,
        "risk_level": risk_level,
        "category_results": category_results
    }
