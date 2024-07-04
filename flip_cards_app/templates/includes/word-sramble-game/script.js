// List of words to choose from
const words = [
    { original: "APPLE", hint: "A popular fruit" },
    { original: "BANANA", hint: "Yellow fruit" },
    { original: "CHERRY", hint: "Small, red fruit" },
    { original: "GRAPE", hint: "Used to make wine" },
    { original: "KIWI", hint: "Small, green fruit" },
    { original: "ORANGE", hint: "Citrus fruit" },
    { original: "STRAWBERRY", hint: "Red, sweet fruit" },
];

// Function to scramble a word
function scrambleWord(word) {
    const array = word.split("");
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array.join("");
}

// Scramble the words in the array
words.forEach(wordObj => {
    wordObj.scrambled = scrambleWord(wordObj.original);
});

// Variables
let currentWordIndex = 0;
let currentWord = "";
let timeLeft = 30; 
let timer;
const wordElement = document.querySelector(".word");
const hintElement = document.querySelector(".hint span");
const timeLeftElement = document.querySelector(".hint strong");
const inputField = document.querySelector("input");
const shuffleButton = document.querySelector(".btn-secondary");
const submitButton = document.querySelector(".btn-dark");

// Function to start a new round
function newRound() {
    if (currentWordIndex >= words.length) {
        // If all words are used, reset the game
        currentWordIndex = 0;
        alert("Game Over! You've completed all words.");
    }

    currentWord = words[currentWordIndex];
    wordElement.textContent = currentWord.scrambled;
    hintElement.textContent = currentWord.hint;
    timeLeft = 30;
    inputField.value = "";
    inputField.removeAttribute("disabled");
    submitButton.removeAttribute("disabled");
    clearInterval(timer);
    timer = setInterval(updateTimeLeft, 1000);
    currentWordIndex++;
}

// Function to update the time left
function updateTimeLeft() {
    if (timeLeft <= 0) {
        clearInterval(timer);
        inputField.setAttribute("disabled", "disabled");
        submitButton.setAttribute("disabled", "disabled");
        alert("Time's up! Try the next word.");
        newRound();
    } else {
        timeLeft--;
        timeLeftElement.textContent = `${timeLeft} sec`;
    }
}

// Event listeners
shuffleButton.addEventListener("click", newRound);

submitButton.addEventListener("click", function () {
    const userGuess = inputField.value.toUpperCase();
    if (userGuess === currentWord.original) {
        clearInterval(timer);
        inputField.setAttribute("disabled", "disabled");
        submitButton.setAttribute("disabled", "disabled");
        alert("Correct! Next word.");
        newRound();
    } else {
        alert("Incorrect. Try again!");
    }
});

// Initialize the game with the first word
newRound();
