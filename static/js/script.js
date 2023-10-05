document.addEventListener("DOMContentLoaded", function() {
    const passwordTypeSelect = document.getElementById("password-type");
    const passwordLengthInput = document.getElementById("password-length");
    const complexitySelect = document.getElementById("complexity");
    const includeUppercaseCheckbox = document.getElementById("include-uppercase");
    const includeDigitsCheckbox = document.getElementById("include-digits");
    const includeSymbolsCheckbox = document.getElementById("include-symbols");
    const customPasswordInput = document.getElementById("custom-password-input");
    const generateButton = document.getElementById("generate");
    const generatedPasswordInput = document.getElementById("generated-password");

    generateButton.addEventListener("click", function() {
        const passwordType = passwordTypeSelect.value;
        const passwordLength = parseInt(passwordLengthInput.value);
        const complexity = complexitySelect.value;
        const includeUppercase = includeUppercaseCheckbox.checked;
        const includeDigits = includeDigitsCheckbox.checked;
        const includeSymbols = includeSymbolsCheckbox.checked;

        let generatedPassword;

        if (passwordType === "custom") {
            generatedPassword = generateCustomPassword(customPasswordInput.value);
        } else if (passwordType === "memorable") {
            generatedPassword = generateMemorablePassword(passwordLength, complexity);
        } else {
            generatedPassword = generatePassword(passwordType, passwordLength, complexity, includeUppercase, includeDigits, includeSymbols);
        }

        generatedPasswordInput.value = generatedPassword;
    });

    function generatePassword(passwordType, length, complexity, includeUppercase, includeDigits, includeSymbols) {
        let charset = "";

        switch (passwordType) {
            case "random":
                charset = generateCharset(complexity, includeUppercase, includeDigits, includeSymbols);
                return generateRandomPassword(length, charset);

            case "memorable":
                // Implement memorable password generation logic.
                // Example: Combine random words or phrases.
                return generateMemorablePassword(length, complexity);

            case "pin":
                charset = "0123456789";
                return generateRandomPassword(length, charset);
            default:
                return "";
        }
    }

    function generateCharset(complexity, includeUppercase, includeDigits, includeSymbols) {
        const charsets = {
            easy: "abcdefghijklmnopqrstuvwxyz",
            medium: "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
            hard: "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+"
        };

        let charset = charsets[complexity] || charsets.easy;

        if (includeUppercase) {
            charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        }

        if (includeDigits) {
            charset += "0123456789";
        }

        if (includeSymbols) {
            charset += "!@#$%^&*()_+";
        }

        return charset;
    }

    function generateRandomPassword(length, charset) {
        let password = "";
        const charsetLength = charset.length;

        for (let i = 0; i < length; i++) {
            const randomIndex = Math.floor(Math.random() * charsetLength);
            password += charset.charAt(randomIndex);
        }

        return password;
    }

    function generateCustomPassword(customText) {
        // Generate random characters before and after the custom text.
        const prefix = generateRandomCharacters(3); // Change the number to control the prefix length.
        const suffix = generateRandomCharacters(3); // Change the number to control the suffix length.
        return `${prefix}${customText}${suffix}`;
    }

    function generateRandomCharacters(length) {
        const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+";
        let result = "";
        for (let i = 0; i < length; i++) {
            const randomIndex = Math.floor(Math.random() * charset.length);
            result += charset.charAt(randomIndex);
        }
        return result;
    }

    function generateMemorablePassword(length, complexity) {
        const wordLists = {
            easy: [
                "apple", "banana", "cherry", "dog", "elephant",
                "friday", "guitar", "happy", "icecream", "jazz"
            ],
            medium: [
                "apple", "banana", "cherry", "dog", "elephant",
                "friday", "guitar", "happy", "icecream", "jazz",
                "kangaroo", "lemon", "monkey", "notebook", "orange"
            ],
            hard: [
                "apple", "banana", "cherry", "dog", "elephant",
                "friday", "guitar", "happy", "icecream", "jazz",
                "kangaroo", "lemon", "monkey", "notebook", "orange",
                "penguin", "quilt", "rainbow", "sunshine", "tiger",
                "umbrella", "violin", "watermelon", "xylophone", "zebra"
            ]
        };

        const selectedWordList = wordLists[complexity] || wordLists.easy;

        let memorablePassword = "";

        while (memorablePassword.length < length) {
            const randomIndex = Math.floor(Math.random() * selectedWordList.length);
            const randomWord = selectedWordList[randomIndex];
            memorablePassword += randomWord;
        }

        return memorablePassword.slice(0, length);
    }
});
