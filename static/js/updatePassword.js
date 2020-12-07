/************************************************
File: updatePassword.js
Author: Dylan Bryan
Date: 12/7/20, 10:14 AM
Project: sdev-300-lab-eight
Purpose: Password update scripts for HTML page
************************************************/

// ensure the script only starts after all the content on the page loads
document.addEventListener("DOMContentLoaded", () => {
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm-password');
    const passwordMessage = document.getElementById('password-message');
    const userInfo = document.querySelector('.username-password-field');
    const form = document.querySelector('.form');
    const updateBtn = document.getElementById('change-password-btn');
    const WEAKPASSWORD = "^\\w{1,9}$";
    const STRONGPASSWORD = "^(?=.{12}$)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[!|@|#|$|%]).*$";
    // set update button to enabled
    updateBtn.disabled = false;

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
     * Checks whether the passwords match
     * and re-enabled the update button
     * @param e EVENT
     */
    function checkPasswordMatch(e) {
        // ensure passwords match and are not empty
        if (password.value === confirmPassword.value &&
            password.value !== "" && confirmPassword.value !== "") {
            setMessageAndColor(passwordMessage, "Passwords MATCH", "green");
        } else { // otherwise the passwords do not match
            setMessageAndColor(passwordMessage, "Passwords DO NOT match", "red");
        } // end if/else statement

        // set the update button to enabled if the passwords match and are a strong password
        if (regexTest(password.value, confirmPassword.value, STRONGPASSWORD)) updateBtn.disabled = false;
    } // end checkPasswordMatch function

    /**
     * Confirms the users update data upon submission
     * of the form, if there are errors it will prevent
     * submission and disable the button
     * @param e EVENT
     */
    function confirmUserData(e) {
        // if the password matches the regex for a weak password on the list
        // prevent the form from submitting and let the user know
        if (regexTest(password.value, confirmPassword.value, WEAKPASSWORD)) {
            e.preventDefault();
            updateBtn.disabled = true;
            setMessageAndColor(passwordMessage,
                "Password is compromised, too weak, or does not meet specifications.<br>" +
                "Must have 12 characters in length, 1 lower, upper case, number and special character",
                "orange");
        } // end if statement

        // if passwords do not match prevent submission and disable the button
        if (password.value !== confirmPassword.value) {
            e.preventDefault();
            updateBtn.disabled = true;
            setMessageAndColor(passwordMessage,
                "Passwords DO NOT match",
                "red");
        } // end if statement

    } // end confirmUserData function

    // event listeners for the form
    userInfo.addEventListener('keyup', checkPasswordMatch);
    form.addEventListener('submit', confirmUserData);

}); // end document ready function