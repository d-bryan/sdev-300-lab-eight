/************************************************
 File: redirectHome.js
 Author: Dylan Bryan
 Date: 11/28/20, 11:48 AM
 Project: sdev-300-lab-seven
 Purpose: Script that redirects the user to the
 home page when landing on not found or
 unauthorized route after six seconds have passed
 ************************************************/

// ensure the script only starts after all the content on the page loads
document.addEventListener("DOMContentLoaded", () => {
    const timeSpan = document.getElementById('timer-information');
    let seconds = 6; // number of seconds to redirect
    const homeUrl = "/"; // home route

    /**
     * Redirects the user to the home page
     * after six seconds have passed
     */
    function redirect() {
        if (seconds <= 0) {
            window.location = homeUrl;
        } else {
            seconds--;
            timeSpan.innerHTML = seconds;
            setTimeout(redirect, 1000);
        } // end if/else statement
    } // end function redirect

    redirect();
}) // end DOM content loaded event listener