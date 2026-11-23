
# CyberShield - Security Recommendation Engine

RECOMMENDATIONS = {
    "Password Security": [
        "Use unique, long passwords or passphrases for every account.",
        "Enable multi-factor authentication (MFA) wherever available.",
        "Use a trusted password manager for storing credentials."
    ],

    "Network Security": [
        "Enable and maintain firewalls on business networks.",
        "Keep routers, operating systems, and network devices updated.",
        "Separate guest Wi-Fi from internal business networks."
    ],

    "Data Protection": [
        "Encrypt sensitive business information at rest and in transit.",
        "Keep operating systems and applications updated.",
        "Train employees to recognize suspicious files and links."
    ],

    "Access Control": [
        "Give employees only the access necessary for their roles.",
        "Review user permissions regularly.",
        "Remove access promptly when employees leave the organization."
    ],

    "Backup & Recovery": [
        "Maintain regular backups of important business data.",
        "Keep at least one backup isolated from the main network.",
        "Test data restoration procedures periodically."
    ]
}


def generate_recommendations(risk_result):

    category_results = risk_result["category_results"]

    recommendations = []

    for category, details in category_results.items():

        risk_percentage = details["percentage"]

        if risk_percentage <= 20:
            priority = "Low"
        elif risk_percentage <= 40:
            priority = "Medium"
        elif risk_percentage <= 70:
            priority = "High"
        else:
            priority = "Critical"

        recommendations.append({
            "category": category,
            "risk_percentage": risk_percentage,
            "priority": priority,
            "recommendations": RECOMMENDATIONS.get(category, [])
        })

    priority_order = {
        "Critical": 0,
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    recommendations.sort(
        key=lambda item: (
            priority_order[item["priority"]],
            -item["risk_percentage"]
        )
    )

    return recommendations
