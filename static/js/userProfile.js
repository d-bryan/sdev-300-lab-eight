/************************************************
 File: userProfile.js
 Author: Dylan Bryan
 Date: 12/4/20, 1:18 PM
 Project: sdev-300-lab-seven
 Purpose: Sets the value of data to time created
 ************************************************/

// ensure the script only starts after all the content on the page loads
document.addEventListener("DOMContentLoaded", () => {
    const tableSquares = document.querySelectorAll('.date-created');

    /**
     * Sets the date that user profile was created
     */
    function setDate() {
        const date = new Date()
        const month = date.getMonth()
        const year = date.getFullYear()
        const day = date.getDay()
        const fullDate = `${month}/${day}/${year}`

        // loop over the date squares and set the values to date created
        for (let i = 0; i < tableSquares.length; i++) {
            tableSquares[i].innerHTML = fullDate;
        } // end for loop
    } // end setData function

    // check for empty value in table for date created before setting date
    if (tableSquares[0].innerHTML === "") {
        setDate(); // set the date created
    } // end if statement

})