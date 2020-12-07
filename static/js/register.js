/************************************************
 File: register.js
 Author: Dylan Bryan
 Date: 11/28/20, 1:36 PM
 Project: sdev-300-lab-seven
 Purpose: Script to add functionality to register
 form page
 ************************************************/

// ensure the script only starts after all the content on the page loads
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector('.form');
    const loginInfo = document.querySelector('.username-password-field');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('password-confirmation');
    const message = document.getElementById('password-message');
    const favoriteAnimal = document.getElementById('favorite-animal');
    const yearsOfStudy = document.getElementById('years-of-study');
    const submitBtn = document.getElementById('register-submit');
    const REGEX = "^(?=.{12}$)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[!|@|#|$|%]).*$";
    const checkOptionValue = (option) => (option.value === "");
    // set the button to enabled
    submitBtn.disabled = false;

    /**
     * Set the color for error message and inner text
     * @param element Element to change
     * @param message String to place
     * @param color Style to edit
     */
    function setMessageAndColor(element, message, color) {
        element.innerHTML = message;
        element.style.color = color;
    } // end setMessageAndColor function

    /**
     * Function to test whether passwords meet
     * standards for user requirements
     * @param pass Password
     * @param confirm Confirmed Password
     * @param regex Regular Expression
     * @returns {boolean}
     */
    const regexTest = (pass, confirm, regex) => (pass.match(regex) && confirm.match(regex));

    /**
     * Callback function to check that passwords match,
     * ensures to show user before they submit that
     * the password match or need to meet specification
     * @param e EVENT
     */
    function checkPasswordMatch(e) {

        // if passwords match, do not meet standard,
        // or do not match display to user
        if (password.value === confirmPassword.value &&
            password.value !== "" && confirmPassword.value !== "") {
            setMessageAndColor(message,
                "Passwords Match",
                "green");
        } else if (password.value === "" && confirmPassword.value === "") {
            setMessageAndColor(message,
                "Must have 12 characters in length, 1 lower, upper case, number and special character",
                "orange");
        } else {
            setMessageAndColor(message,
                "Passwords Do NOT Match",
                "red");
        } // end if/else if/else statement

        // check regex for complexity to re-enable button
        if (regexTest(password.value, confirmPassword.value, REGEX)) submitBtn.disabled = false;

    } // end checkPasswordMatch function

    /**
     * Callback function to confirm password matches specification
     * before submitting the form, will prevent form submission
     * if the password is incorrect
     * @param e EVENT
     */
    function confirmUserData(e) {
        const animalMessage = document.getElementById('animal-message');
        const studyMessage = document.getElementById('study-message');

        /**
         * Check to ensure default value is not
         * selected for favorite animal
         */
        if (checkOptionValue(favoriteAnimal)) {
            e.preventDefault();
            setMessageAndColor(animalMessage,
                "Please choose a favorite animal",
                "red");
        } else {
            setMessageAndColor(animalMessage, "", "none");
        }

        /**
         * Check to ensure default value is not
         * selected for years of study
         */
        if (checkOptionValue(yearsOfStudy)) {
            e.preventDefault();
            setMessageAndColor(studyMessage,
                "Please select total years of study",
                "red");
        } else {
            setMessageAndColor(studyMessage, "", "none");
        }

        /**
         * check that the passwords meet specifications for user profile
         */
        if (!(regexTest(password.value, confirmPassword.value, REGEX))) {
            e.preventDefault();
            setMessageAndColor(message,
                "Must have 12 characters in length, 1 lower, upper case, number and special character",
                "orange");
            // disable the button so they have to fix the password
            submitBtn.disabled = true;
        } // end if statement

    } // end confirmUserData function

    // event listeners for keyup and submit
    loginInfo.addEventListener('keyup', checkPasswordMatch);
    form.addEventListener('submit', confirmUserData);
}) // end DOM content loaded event listener

