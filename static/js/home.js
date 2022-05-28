/************************************************
 File: home.js
 Author: Dylan Bryan
 Date: 11/22/20, 1:30 PM
 Project: Lab-6
 Purpose: Scripts to add additional functionality to
 the project and make it interactive
 ************************************************/

// ensure the script only starts after all the content on the page loads
document.addEventListener("DOMContentLoaded", () => {
    const currentEventDate = document.getElementById('current-event-date');
    const timerSpan = document.getElementById('countdown');
    const deadline = new Date(`${currentEventDate.textContent} 12:00:00`).getTime();

    /**
     * Sets the time remaining until the event starts and changes
     * the time on the home page
     * @type {number}
     */
    function changeTime () {
        const now = new Date().getTime();
        const t = deadline - now;
        let days = Math.floor(t / (1000 * 60 * 60 * 24));
        let hours = Math.floor((t % (1000 * 60 * 60 *24)) / (1000 * 60 * 60));
        let minutes = Math.floor((t % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((t % (1000 * 60)) / 1000);
        timerSpan.innerHTML = days + " Days, " +
            hours + " Hours, " + minutes + " Minutes, " + seconds + " Seconds";
        if (t < 0) {
            clearInterval(interval);
            timerSpan.innerHTML = "The Event Has Started! Woo Hoo!"
        } // end if statement
    } // end changeTime function

    // call the function
    let interval = setInterval(changeTime);

}) // end DOM content loaded event listener
