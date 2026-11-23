
const assessmentQuestions = [
    {
        category: "Password Security",
        questions: [
            "Does your business use strong passwords containing different character types?",
            "Does your business use multi-factor authentication (MFA) for important accounts?",
            "Are passwords stored securely using a password manager?"
        ]
    },
    {
        category: "Network Security",
        questions: [
            "Is your business Wi-Fi protected with a strong password?",
            "Is your network equipment updated with the latest security patches?",
            "Is a firewall enabled to protect your business network?"
        ]
    },
    {
        category: "Data Protection",
        questions: [
            "Is sensitive business data encrypted?",
            "Does your business restrict access to confidential information?",
            "Is sensitive customer information handled securely?"
        ]
    },
    {
        category: "Access Control",
        questions: [
            "Does every employee use an individual account?",
            "Are employee access permissions reviewed regularly?",
            "Is access removed when an employee leaves the organization?"
        ]
    },
    {
        category: "Backup & Recovery",
        questions: [
            "Does your business regularly back up important data?",
            "Are backups stored separately from your main systems?",
            "Have you tested whether your backups can be restored?"
        ]
    }
];

document.addEventListener("DOMContentLoaded", function () {

    const questionsContainer =
        document.getElementById("questionsContainer");

    const securityForm =
        document.getElementById("securityForm");

    const formMessage =
        document.getElementById("formMessage");

    // Only run assessment code on assessment page
    if (!questionsContainer || !securityForm) return;

    function loadQuestions() {

        questionsContainer.innerHTML = "";

        let questionNumber = 1;

        assessmentQuestions.forEach(section => {

            const sectionDiv = document.createElement("div");
            sectionDiv.className = "question-section";

            const heading = document.createElement("h2");
            heading.textContent = section.category;

            sectionDiv.appendChild(heading);

            section.questions.forEach(question => {

                const questionDiv = document.createElement("div");
                questionDiv.className = "question-card";

                const questionHeading = document.createElement("h3");
                questionHeading.textContent =
                    `${questionNumber}. ${question}`;

                questionDiv.appendChild(questionHeading);

                const optionsDiv = document.createElement("div");
                optionsDiv.className = "answer-options";

                ["Yes", "Partially", "No"].forEach(option => {

                    const label = document.createElement("label");
                    label.className = "answer-option";

                    const input = document.createElement("input");
                    input.type = "radio";
                    input.name = `q${questionNumber}`;
                    input.value = option;
                    input.required = true;

                    label.appendChild(input);
                    label.appendChild(
                        document.createTextNode(option)
                    );

                    optionsDiv.appendChild(label);

                });

                questionDiv.appendChild(optionsDiv);
                sectionDiv.appendChild(questionDiv);

                questionNumber++;

            });

            questionsContainer.appendChild(sectionDiv);

        });

    }

    loadQuestions();

  
securityForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    if (!securityForm.reportValidity()) return;

    const formData = new FormData(securityForm);
    const answers = {};

    for (let i = 1; i <= 15; i++) {
        answers[`q${i}`] = formData.get(`q${i}`);
    }

    sessionStorage.setItem(
        "cyberShieldAnswers",
        JSON.stringify(answers)
    );

    formMessage.textContent = "Calculating your security risk...";

    try {

        const response = await fetch("/calculate-risk", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(answers)

        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Risk calculation failed");
        }

        console.log("CyberShield Assessment:", answers);

        console.log("Python Risk Analysis:", result);

        sessionStorage.setItem(
            "cyberShieldRiskResult",
            JSON.stringify(result)
        );

        formMessage.innerHTML = `
            <h2>Assessment Completed Successfully!</h2>
            <p>Total Risk Score: ${result.total_score}/150</p>
            <p>Risk Percentage: ${result.risk_percentage}%</p>
            <p>Risk Level: ${result.risk_level}</p>
        `;

        formMessage.className = "success-message";

        formMessage.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

    } catch (error) {

        console.error("Risk calculation error:", error);

        formMessage.textContent =
            "Unable to calculate risk. " + error.message;

        formMessage.className = "success-message";

    }

});


    // Reset form and previous success message
    securityForm.addEventListener("reset", function () {

        sessionStorage.removeItem("cyberShieldAnswers");

        formMessage.textContent = "";
        formMessage.className = "";

    });

});
