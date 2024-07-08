// Variables
let currentWord = "";
let timeLeft = 30; 
let timer;
const wordElement = document.querySelector(".word");
const hintElement = document.querySelector(".hint span");
const timeLeftElement = document.querySelector(".hint strong");
const inputField = document.getElementById("input");
const shuffleButton = document.getElementById("btn_new");
const submitButton = document.getElementById("btn_check");

// Function to start a new round
function newRound() {
    currentWord = document.querySelector('.content').id;
    timeLeft = 30;
    inputField.value = "";
    inputField.removeAttribute("disabled");
    submitButton.removeAttribute("disabled");
    clearInterval(timer);
    timer = setInterval(updateTimeLeft, 1000);
}

// Function to update the time left
function updateTimeLeft() {
    if (timeLeft <= 0) {
        clearInterval(timer);
        inputField.setAttribute("disabled", "disabled");
        submitButton.setAttribute("disabled", "disabled");
        if (confirm(`Время вышло! ${currentWord.toUpperCase()} является правильным словом! Желаете сыграть еще раз?`)) {
            window.location.reload(true);
            newRound();
        }
    } else {
        timeLeft--;
        timeLeftElement.textContent = `${timeLeft} сек`;
    }
}

// Event listeners
shuffleButton.addEventListener("click", function () {
    window.location.reload(true);
    newRound();
});

submitButton.addEventListener("click", function () {
    const userGuess = inputField.value;
    console.log(userGuess);

    if (!userGuess) return swal({ text: "Пожалуйста введите слово!", icon: "error"});
    if (userGuess.toUpperCase() === currentWord.toUpperCase()) {
        clearInterval(timer);
        inputField.setAttribute("disabled", "disabled");
        submitButton.setAttribute("disabled", "disabled");
        if (confirm(`Поздравляем! ${userGuess.toUpperCase()} является правильным словом! Желаете сыграть еще раз?`)) {
            window.location.reload(true);
            newRound();
        }
    } else {
        alert(`${userGuess.toUpperCase()} это неправильное слово!`);
    }
});

// Initialize the game with the first word
newRound();
