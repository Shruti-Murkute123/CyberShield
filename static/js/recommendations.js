
document.addEventListener("DOMContentLoaded", function () {

    const summary = document.getElementById("recommendationSummary");
    const container = document.getElementById("recommendationsContainer");

    const storedAnswers = sessionStorage.getItem("cyberShieldAnswers");

    if (!storedAnswers) {
        summary.textContent =
            "No assessment found. Please complete the security assessment first.";
        return;
    }

    async function loadRecommendations() {

        try {

            const answers = JSON.parse(storedAnswers);

           const response = await fetch("/calculate-risk?save=0", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(answers)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || "Unable to load recommendations");
            }

            sessionStorage.setItem(
                "cyberShieldRiskResult",
                JSON.stringify(result)
            );

            displayRecommendations(result);

        } catch (error) {
            summary.textContent = "Error: " + error.message;
        }
    }

    function displayRecommendations(result) {

        summary.replaceChildren();
        container.replaceChildren();

        const heading = document.createElement("h2");
        heading.textContent =
            `Overall Risk: ${result.risk_level} (${result.risk_percentage}%)`;

        summary.appendChild(heading);

        result.recommendations.forEach(item => {

            const card = document.createElement("div");
            card.className = "recommendation-card";

            const title = document.createElement("h2");
            title.textContent = item.category;

            const priority = document.createElement("p");
            priority.className = "recommendation-priority";
            priority.textContent =
                `Priority: ${item.priority} | Risk: ${item.risk_percentage}%`;

            const list = document.createElement("ul");

            item.recommendations.forEach(text => {

                const listItem = document.createElement("li");
                listItem.textContent = text;
                list.appendChild(listItem);

            });

            card.append(title, priority, list);
            container.appendChild(card);

        });

    }

    loadRecommendations();

});
