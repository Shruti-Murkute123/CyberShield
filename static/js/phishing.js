
document.addEventListener("DOMContentLoaded", function () {

    const quizContainer = document.getElementById("quizContainer");
    const quizResult = document.getElementById("quizResult");

    let questions = [];

    async function loadQuiz() {

        try {

            quizContainer.textContent = "Loading quiz...";

            const response = await fetch("/api/phishing-quiz");

            if (!response.ok) {
                throw new Error("Unable to load quiz");
            }

            questions = await response.json();

            displayQuestions();

        } catch (error) {

            quizContainer.textContent =
                "Error loading quiz: " + error.message;

        }

    }


    function displayQuestions() {

        quizContainer.innerHTML = "";

        const form = document.createElement("form");
        form.id = "phishingForm";

        questions.forEach((question, index) => {

            const card = document.createElement("div");
            card.className = "quiz-card";

            const heading = document.createElement("h3");
            heading.textContent =
                `${index + 1}. ${question.question}`;

            card.appendChild(heading);

            question.options.forEach(option => {

                const label = document.createElement("label");
                label.className = "quiz-option";

                const input = document.createElement("input");

                input.type = "radio";
                input.name = question.id;
                input.value = option.value;
                input.required = true;

                label.appendChild(input);

                label.appendChild(
                    document.createTextNode(option.label)
                );

                card.appendChild(label);

            });

            form.appendChild(card);

        });

        const submitButton = document.createElement("button");

        submitButton.type = "submit";
        submitButton.className = "btn-primary";
        submitButton.textContent = "Submit Quiz →";

        form.appendChild(submitButton);

        form.addEventListener("submit", submitQuiz);

        quizContainer.appendChild(form);

    }


    async function submitQuiz(event) {

        event.preventDefault();

        const formData = new FormData(event.target);

        const answers = {};

        questions.forEach(question => {

            answers[question.id] = formData.get(question.id);

        });

        try {

            const response = await fetch("/api/phishing-quiz", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({ answers: answers })

            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || "Quiz submission failed");
            }

            displayResults(result);

            console.log("Phishing Quiz Results:", result);

        } catch (error) {

            quizResult.textContent = error.message;
            quizResult.className = "success-message";

        }

    }


    function displayResults(result) {

        quizContainer.innerHTML = "";

        const resultCard = document.createElement("div");
        resultCard.className = "quiz-result-card";

        const heading = document.createElement("h2");
        heading.textContent = "Quiz Completed!";

        const score = document.createElement("h1");
        score.textContent =
            `${result.score}/${result.total}`;

        const percentage = document.createElement("h2");
        percentage.textContent =
            `${result.percentage}%`;

        const level = document.createElement("h3");
        level.textContent =
            `Awareness Level: ${result.awareness_level}`;

        resultCard.append(heading, score, percentage, level);

        const feedbackHeading = document.createElement("h2");
        feedbackHeading.textContent = "Answer Review";

        resultCard.appendChild(feedbackHeading);

        result.feedback.forEach((item, index) => {

            const feedbackCard = document.createElement("div");

            feedbackCard.className = "quiz-feedback";

            const question = questions[index];

            const questionText = document.createElement("h3");
            questionText.textContent = question.question;

            const answerText = document.createElement("p");
            answerText.textContent =
                `Your answer: ${item.selected} | Correct answer: ${item.correct_answer}`;

            const status = document.createElement("p");
            status.textContent =
                item.is_correct ? "Correct" : "Incorrect";

            status.className =
                item.is_correct ? "correct-answer" : "wrong-answer";

            const explanation = document.createElement("p");
            explanation.textContent = item.explanation;

            feedbackCard.append(
                questionText,
                answerText,
                status,
                explanation
            );

            resultCard.appendChild(feedbackCard);

        });

        const retakeButton = document.createElement("button");

        retakeButton.className = "btn-primary";
        retakeButton.textContent = "Retake Quiz";

        retakeButton.addEventListener("click", function () {

            quizResult.textContent = "";
            loadQuiz();

        });

        resultCard.appendChild(retakeButton);

        quizContainer.appendChild(resultCard);

    }


    loadQuiz();

});
