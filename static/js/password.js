
document.addEventListener("DOMContentLoaded", function () {

    const passwordInput = document.getElementById("passwordInput");
    const passwordResult = document.getElementById("passwordResult");

    // Show or hide password
    document.getElementById("showPassword").addEventListener(
        "change",
        function () {
            passwordInput.type = this.checked ? "text" : "password";
        }
    );

    // Password strength analyzer
    document.getElementById("checkPassword").addEventListener(
        "click",
        function () {

            const password = passwordInput.value;

            if (!password) {
                passwordResult.textContent = "Please enter a sample password.";
                return;
            }

            let score = 0;
            let suggestions = [];

            if (password.length >= 12) {
                score++;
            } else {
                suggestions.push("Use at least 12 characters.");
            }

            if (/[a-z]/.test(password) && /[A-Z]/.test(password)) {
                score++;
            } else {
                suggestions.push("Include uppercase and lowercase letters.");
            }

            if (/[0-9]/.test(password)) {
                score++;
            } else {
                suggestions.push("Include numbers.");
            }

            if (/[^A-Za-z0-9]/.test(password)) {
                score++;
            } else {
                suggestions.push("Include special characters.");
            }

            const commonPasswords = [
                "password",
                "password123",
                "123456",
                "12345678",
                "qwerty",
                "admin123",
                "welcome123"
            ];

            if (commonPasswords.includes(password.toLowerCase())) {
                score = 0;
                suggestions.push("Avoid commonly used passwords.");
            }

            let strength;

            if (score <= 1) {
                strength = "Weak";
            } else if (score === 2) {
                strength = "Moderate";
            } else if (score === 3) {
                strength = "Good";
            } else {
                strength = "Strong";
            }

            passwordResult.replaceChildren();

            const heading = document.createElement("h3");
            heading.textContent = "Password Strength: " + strength;

            const points = document.createElement("p");
            points.textContent = "Checklist Score: " + score + "/4";

            passwordResult.append(heading, points);

            suggestions.forEach(suggestion => {
                const p = document.createElement("p");
                p.textContent = "• " + suggestion;
                passwordResult.appendChild(p);
            });

            const note = document.createElement("p");
            note.textContent =
                "This is a basic educational check, not a guarantee of security.";
            passwordResult.appendChild(note);

        }
    );

    // Secure password generator
    document.getElementById("generatePassword").addEventListener(
        "click",
        function () {

            const characters =
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
                "abcdefghijklmnopqrstuvwxyz" +
                "0123456789" +
                "!@#$%^&*";

            const length = 20;
            const max = Math.floor(4294967296 / characters.length)
                * characters.length;

            let password = "";

            while (password.length < length) {

                const values = new Uint32Array(1);
                crypto.getRandomValues(values);

                if (values[0] < max) {
                    password += characters[
                        values[0] % characters.length
                    ];
                }
            }

            document.getElementById("generatedPassword").textContent =
                password;

        }
    );

});
